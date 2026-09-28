"""Cheap numerical and economic diagnostics; baseline inputs remain unchanged."""
import bisect, hashlib, json, math
from pathlib import Path
from statistics import NormalDist

ROOT=Path(__file__).resolve().parents[2]
src=ROOT/'model/linked_service_revenue_2026-09-28/inputs.json'
d=json.loads(src.read_text()); N=NormalDist()
def grid(kind, preferred=False):
    return sorted([r for r in d['fees'] if (('high' in r['page']) if preferred else r['page']=='non-licensed') and r['title_group']=='non-clean' and r['vehicle_class']=='standard' and r['fee_type']==kind and (kind!='buyer_fee' or r['payment_method']=='secured')],key=lambda r:float(r['band_low_usd']))
std,pref,virt=grid('buyer_fee'),grid('buyer_fee',True),grid('virtual_bid_pre_bid')
def fee(p,g):
    r=g[bisect.bisect_right([float(x['band_low_usd']) for x in g],p)-1]
    return float(r['fee_usd'] or 0)+p*float(r['fee_pct'] or 0)/100
def outcome(b,k,repair=1,value=1,nodes=2048):
    acv=10000*math.exp(-.1*(d['calibration'][k]['representative_age']-10))*d['value_ratios'][b]*value
    mu=d['calibration'][k]['log_repair_median']+math.log(d['repair_ratios'][b]*repair)
    u=rev=proceeds=0
    for j in range(nodes):
        recovery=.4-.2*(j+.5)/nodes
        cut=N.cdf((math.log(acv*(1-.96*recovery))-mu)/d['sigma'])
        probability=max(0,(j+1)/nodes-max(j/nodes,cut))
        price=acv*recovery
        rate=.5*(fee(price,std)+fee(price,pref))+fee(price,virt)+110+.04*price
        u+=probability;rev+=probability*rate;proceeds+=probability*price
    return u,rev,proceeds
weights={}
for b in range(4):
    for k in range(6):
        weights[b,k]=sum(sum(x*w for x,w in zip(r['births'],d['periods'][3]['weights']))*r['survival']*d['split'][b]*r['relative_claim_weight'] for r in d['fleet'] if r['body']==b and r['bucket']==k)
def evaluate(repair=1,value=1,nodes=2048):
    totals=[0.,0.,0.]
    for (b,k),weight in weights.items():
        for i,x in enumerate(outcome(b,k,repair,value,nodes)):totals[i]+=weight*x
    units,rev,proceeds=totals
    return dict(raw_units=units,raw_core_revenue=rev,core_rpu=rev/units,asp=proceeds/units,tlf=units/sum(weights.values()))
baseline=evaluate()
convergence={str(n):evaluate(nodes=n) for n in [9,512,4096]}
scenarios={}
for name,r,v in [('repair_minus_5pct',.95,1),('repair_plus_5pct',1.05,1),('value_minus_5pct',1,.95),('value_plus_5pct',1,1.05),('both_plus_5pct',1.05,1.05)]:
    result=evaluate(r,v)
    scenarios[name]={key:100*(result[key]/baseline[key]-1) for key in ['raw_units','core_rpu','raw_core_revenue','asp']}
    assert math.isclose((1+scenarios[name]['raw_units']/100)*(1+scenarios[name]['core_rpu']/100),1+scenarios[name]['raw_core_revenue']/100,abs_tol=1e-12)
assert abs(scenarios['both_plus_5pct']['raw_units'])<1e-8
assert scenarios['repair_plus_5pct']['raw_units']>0 and scenarios['value_plus_5pct']['raw_units']<0
prior=json.loads((src.parent/'validation.json').read_text())['quarter_results'][3]
assert math.isclose(convergence['9']['core_rpu']+55,prior['rpu'],rel_tol=1e-10)
assert math.isclose(convergence['9']['raw_units']*prior['share'],prior['rawunits'],rel_tol=1e-10)
cohorts=[]
for k in range(6):
    cohorts.append({'age_bucket':d['calibration'][k]['age_bucket'],'car_acv_assumed':10000*math.exp(-.1*(d['calibration'][k]['representative_age']-10)), 'car_repair_median_fitted':math.exp(d['calibration'][k]['log_repair_median']), 'car_repair_mean_latent_fitted':math.exp(d['calibration'][k]['log_repair_median']+.5*d['sigma']**2)})
out={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'scope':'Fixed FY26Q4 claim weights and allocation; core auction service revenue only. Hypothetical uniform 5% shocks, not forecasts; no re-fitting or dollar re-anchoring.', 'baseline_2048':baseline,'convergence':convergence,'scenario_changes_pct':scenarios,'car_cohort_inputs':cohorts,'checks':'Nine-state baseline matches saved validator; units-times-RPU identity; common repair/value scale preserves units.'}
repair_groups={g:[0.,0.] for g in ['age_0_to_6','age_7_plus']}
def moment(p,mu):
    if p<=0:return 0.
    if p>=1:return math.exp(mu+.5*d['sigma']**2)
    return math.exp(mu+.5*d['sigma']**2)*N.cdf(N.inv_cdf(p)-d['sigma'])
for (b,k),weight in weights.items():
    acv=10000*math.exp(-.1*(d['calibration'][k]['representative_age']-10))*d['value_ratios'][b]
    mu=d['calibration'][k]['log_repair_median']+math.log(d['repair_ratios'][b])
    g='age_0_to_6' if k<3 else 'age_7_plus'
    for j in range(2048):
        recovery=.4-.2*(j+.5)/2048
        cut=N.cdf((math.log(acv*(1-.96*recovery))-mu)/d['sigma'])
        low=j/2048; high=min((j+1)/2048,cut)
        if high>low:
            repair_groups[g][0]+=weight*(high-low)
            repair_groups[g][1]+=weight*(moment(high,mu)-moment(low,mu))
out['selected_repairable_mean_check']={g:{'model_mean':v[1]/v[0], 'CCC_2025_reference':5721 if g=='age_0_to_6' else 3682} for g,v in repair_groups.items()}
out['selected_repairable_mean_caveat']='FY26Q4 model mixture versus CY2025 all-loss reference; directional cross-check, not matched-population error. CCC raw report line 277. No repair-cost scale refitted.'
Path(__file__).with_name('repair_value_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['selected_repairable_mean_check'],indent=2))
