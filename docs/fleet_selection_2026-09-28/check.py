"""Existing-input composition diagnostic. No network, workbook access or refitting."""
import bisect
import hashlib
import json
import math
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'model/linked_service_revenue_2026-09-28/inputs.json'
d = json.loads(SOURCE.read_text())
n = NormalDist()

def grid(kind, preferred=False):
    return sorted([r for r in d['fees'] if
        (('high' in r['page']) if preferred else r['page'] == 'non-licensed')
        and r['title_group'] == 'non-clean' and r['vehicle_class'] == 'standard'
        and r['fee_type'] == kind
        and (kind != 'buyer_fee' or r['payment_method'] == 'secured')],
        key=lambda r: float(r['band_low_usd']))

standard, preferred, virtual = grid('buyer_fee'), grid('buyer_fee', True), grid('virtual_bid_pre_bid')
def fee(p, g):
    r = g[bisect.bisect_right([float(x['band_low_usd']) for x in g], p)-1]
    return float(r['fee_usd'] or 0) + p*float(r['fee_pct'] or 0)/100

# Fixed cohort outcomes: probability and expected revenue per claim share the same states.
outcomes = {}
for b in range(4):
    for k in range(6):
        acv = 10000*math.exp(-.1*(d['calibration'][k]['representative_age']-10))*d['value_ratios'][b]
        mu = d['calibration'][k]['log_repair_median'] + math.log(d['repair_ratios'][b])
        units = revenue = proceeds = 0
        for j in range(9):
            recovery = .3 + .2*(.5-(j+.5)/9)
            cutoff = n.cdf((math.log(acv*(1-recovery*.96))-mu)/d['sigma'])
            probability = max(0, (j+1)/9-max(j/9, cutoff))
            price = acv*recovery
            rate = .5*(fee(price, standard)+fee(price, preferred))+fee(price, virtual)+110+.04*price
            units += probability
            revenue += probability*rate
            proceeds += probability*price
        outcomes[b,k] = (units, revenue, proceeds)

def stocks(p):
    return {(r['body'],r['age']):sum(x*w for x,w in zip(r['births'], d['periods'][p]['weights']))
            *r['survival']*d['split'][r['body']] for r in d['fleet']}

base = stocks(3)
def distribution(s):
    total = sum(s.values())
    by_age = {a:sum(s[b,a] for b in range(4)) for a in range(46)}
    return total, {a:by_age[a]/total for a in by_age}, {
        (b,a):s[b,a]/by_age[a] if by_age[a] else 0 for b,a in s}

base_n, base_age, base_body = distribution(base)
def evaluate(s):
    units = revenue = proceeds = claims = 0
    for r in d['fleet']:
        weight = s[r['body'],r['age']]*r['relative_claim_weight']
        u,rev,p = outcomes[r['body'],r['bucket']]
        claims += weight
        units += weight*u
        revenue += weight*rev
        proceeds += weight*p
    return dict(raw_units=units,raw_core_revenue=revenue,core_rpu=revenue/units,
                asp=proceeds/units,claim_weighted_tlf=units/claims)

validated = json.loads((SOURCE.parent/'validation.json').read_text())['quarter_results']
results=[]
for p in range(8):
    s=stocks(p); total, age, body=distribution(s)
    actual=evaluate(s)
    assert math.isclose(actual['core_rpu']+55,validated[p]['rpu'],rel_tol=1e-10)
    assert math.isclose(actual['raw_units']*validated[p]['share'],validated[p]['rawunits'],rel_tol=1e-10)
    if p<4: continue
    worlds={}
    for name, ap, bp in [('frozen_mix',base_age,base_body),('age_only',age,base_body),
                         ('body_only',base_age,body),('both',age,body)]:
        s2={(b,a):total*ap[a]*bp[b,a] for b,a in s}
        assert math.isclose(sum(s2.values()),total,rel_tol=1e-12)
        worlds[name]=evaluate(s2)
    assert math.isclose(worlds['both']['raw_core_revenue'],actual['raw_core_revenue'],rel_tol=1e-12)
    f=worlds['frozen_mix']; a=worlds['age_only']; b=worlds['body_only']; both=worlds['both']
    attribution={
        'age_pp':100*(a['raw_core_revenue']/f['raw_core_revenue']-1),
        'body_within_age_pp':100*(b['raw_core_revenue']/f['raw_core_revenue']-1),
        'interaction_pp':100*(both['raw_core_revenue']-a['raw_core_revenue']-b['raw_core_revenue']+f['raw_core_revenue'])/f['raw_core_revenue']}
    combined=100*(both['raw_core_revenue']/f['raw_core_revenue']-1)
    assert math.isclose(sum(attribution.values()),combined,abs_tol=1e-10)
    results.append({'quarter':d['periods'][p]['label'],'worlds':worlds,'attribution':attribution,
                    'combined_revenue_change_pct':combined,
                    'units_change_pct':100*(both['raw_units']/f['raw_units']-1),
                    'core_rpu_change_pct':100*(both['core_rpu']/f['core_rpu']-1)})

h1_f=sum(r['worlds']['frozen_mix']['raw_core_revenue'] for r in results[:2])
h1={name:100*(sum(r['worlds'][name]['raw_core_revenue'] for r in results[:2])/h1_f-1)
    for name in ['age_only','body_only','both']}
output={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'status':'Conditional core US insurance diagnostic; not observed volume, dollar forecast or consensus delta',
        'checks':'All eight quarters reproduce prior validated units and RPU; composition worlds preserve stock totals; attribution reconciles',
        'h1_revenue_change_pct_vs_frozen_Q4_mix':h1,'quarters':results}
Path(__file__).with_name('results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'h1':h1,'quarters':[{k:v for k,v in r.items() if k!='worlds'} for r in results]},indent=2))
