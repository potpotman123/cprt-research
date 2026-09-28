"""Age-constrained research engine. No workbook or legacy forecast overwrite."""
import bisect,hashlib,json,math
from pathlib import Path
from statistics import NormalDist
P=Path(__file__).parent;ROOT=P.parents[1];N=NormalDist()
source=ROOT/'model/linked_service_revenue_2026-09-28/inputs.json'
d=json.loads(source.read_text());hold=json.loads((P/'age_value_holdout_results.json').read_text())
# Annual model body-within-age mix; not observed insurance exposure.
bw={k:[sum(r['births'][2]*r['survival']*d['split'][b]*r['relative_claim_weight'] for r in d['fleet'] if r['body']==b and r['bucket']==k) for b in range(4)] for k in range(6)}
body={k:[v/sum(bw[k]) for v in bw[k]] for k in range(6)}
# Match observed four-group TL mix; retain explicit annual all-loss split inside 7+.
older=[.209,.199,.318]
tlmix=hold['observed_mix'][:3]+[hold['observed_mix'][3]*x/sum(older) for x in older]
claims=[w/c['target'] for w,c in zip(tlmix,d['calibration'])]
targets=hold['observed_values']
def cutoff(mu,value,sigma):
    lo,hi=1e-12,1-1e-12
    for _ in range(44):
        u=(lo+hi)/2
        if mu+sigma*N.inv_cdf(u)<math.log(value*(.616+.192*u)):lo=u
        else:hi=u
    return (lo+hi)/2
def base(sigma):
    rows=[]
    for k,c in enumerate(d['calibration']):
        car=10000*math.exp(-.1*(c['representative_age']-10))
        def stats(mu):
            t=cost=selected_value=0.
            for b in range(4):
                value=car*d['value_ratios'][b];m=mu+math.log(d['repair_ratios'][b]);u=cutoff(m,value,sigma)
                t+=body[k][b]*(1-u)
                selected_value+=body[k][b]*(1-u)*value
                cost+=body[k][b]*math.exp(m+.5*sigma*sigma)*N.cdf(N.inv_cdf(u)-sigma)
            return t,cost,selected_value
        lo,hi=0.,15.
        for _ in range(48):
            mu=(lo+hi)/2
            if stats(mu)[0]<c['target']:lo=mu
            else:hi=mu
        t,cost,value=stats(mu)
        assert abs(t-c['target'])<1e-9
        rows.append({'age_bucket':c['age_bucket'],'sigma':sigma,'car_ACV':car,'log_car_repair_median':mu,'TLF':t,'repairable_mean':cost/(1-t),'selected_ACV':value/t})
    scales=[targets[k]/rows[k]['selected_ACV'] for k in range(3)]
    oldmean=sum(tlmix[k]*rows[k]['selected_ACV'] for k in range(3,6))/sum(tlmix[3:])
    scales.extend([targets[3]/oldmean]*3)
    for r,s in zip(rows,scales):
        r['car_ACV']*=s;r['log_car_repair_median']+=math.log(s);r['repairable_mean']*=s;r['selected_ACV']*=s
    return rows
def repair_mean(rows,ks):
    w=[claims[k]*(1-rows[k]['TLF']) for k in ks]
    return sum(x*rows[k]['repairable_mean'] for x,k in zip(w,ks))/sum(w)
rows=[];solves=[]
for ks,target in [(range(3),5721),(range(3,6),3682)]:
    lo,hi=.35,3.
    assert repair_mean(base(lo),ks)>target>repair_mean(base(hi),ks)
    for _ in range(26):
        mid=(lo+hi)/2;r=base(mid)
        if repair_mean(r,ks)>target:lo=mid
        else:hi=mid
    rows.extend(r[k] for k in ks)
    solves.append({'age_group':'0-6' if ks.start==0 else '7+','sigma':mid,'target':target,'fitted':repair_mean(r,ks)})
for r in solves:assert abs(r['target']-r['fitted'])<.01
def grid(kind,preferred=False):
    return sorted([r for r in d['fees'] if (('high' in r['page']) if preferred else r['page']=='non-licensed') and r['title_group']=='non-clean' and r['vehicle_class']=='standard' and r['fee_type']==kind and (kind!='buyer_fee' or r['payment_method']=='secured')],key=lambda r:float(r['band_low_usd']))
std,pref,virtual=grid('buyer_fee'),grid('buyer_fee',True),grid('virtual_bid_pre_bid')
def fee(price,g):
    r=g[bisect.bisect_right([float(x['band_low_usd']) for x in g],price)-1]
    return float(r['fee_usd'] or 0)+price*float(r['fee_pct'] or 0)/100
def evaluate(repair=1,value=1,nodes=2048):
    units=proceeds=rev=0.
    for k,r in enumerate(rows):
        for b in range(4):
            acv=r['car_ACV']*d['value_ratios'][b]*value
            mu=r['log_car_repair_median']+math.log(d['repair_ratios'][b]*repair)
            cut=cutoff(mu,acv,r['sigma']);w=claims[k]*body[k][b];mass=w*(1-cut)
            units+=mass;proceeds+=mass*acv*(.3-.1*cut)
            for j in range(nodes):
                u=cut+(1-cut)*(j+.5)/nodes;price=acv*(.4-.2*u)
                rate=.5*(fee(price,std)+fee(price,pref))+fee(price,virtual)+110+.04*price
                rev+=mass/nodes*rate
    return {'units':units,'ASP':proceeds/units,'core_RPU':rev/units,'core_revenue':rev}
baseline=evaluate();fine=evaluate(nodes=4096)
changes={}
for name,r,v in [('repair_plus_5pct',1.05,1),('value_plus_5pct',1,1.05),('both_plus_5pct',1.05,1.05)]:
    result=evaluate(r,v);changes[name]={k:100*(result[k]/baseline[k]-1) for k in result}
    assert math.isclose((1+changes[name]['units']/100)*(1+changes[name]['core_RPU']/100),1+changes[name]['core_revenue']/100,abs_tol=1e-10)
assert abs(changes['both_plus_5pct']['units'])<1e-8
fitted_values=[r['selected_ACV'] for r in rows[:3]]+[sum(tlmix[k]*rows[k]['selected_ACV'] for k in range(3,6))/sum(tlmix[3:])]
assert max(abs(a-b) for a,b in zip(fitted_values,targets))<.01
out={'status':'Revised research component; constrained hybrid-population calibration, not independently validated forecast.',
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'age_value_source':'age_value_holdout_results.json; CCC Figure 6 through October 2025 noncomp',
 'TLmix':tlmix,'relative_claim_weights':claims,'body_weights':body,'value_ratios':d['value_ratios'],'repair_ratios':d['repair_ratios'],
 'cohorts':rows,'repair_checks':solves,'selected_value_checks':fitted_values,'baseline_core':baseline,'scenario_changes_pct_NOT_forecasts':changes,
 'single_dispersion_crosschecks':[{'sigma':s['sigma'],'younger_mean':repair_mean(base(s['sigma']),range(3)),'older_mean':repair_mean(base(s['sigma']),range(3,6))} for s in solves],
 'fee_integration_4096_vs_2048_revenue_pct':100*(fine['core_revenue']/baseline['core_revenue']-1),
 'free_assumptions':['All-loss TLF and repair targets versus noncomp value/mix, periods differ','7+ internal age split and original .10 log value slope retained','Body weights, body repair/value ratios, single ACV per cohort','Recovery .4-.2u; seller 4%; fee mix and fixed fees inherited','Two fitted dispersions replace single shared dispersion; no new empirical damage data'],
 'handoff':'Use cohort car_ACV, log_car_repair_median and sigma with inherited body ratios. Damage cutoff equation in script. Keep service adoption and allocation separate. Do not dollar-reanchor legacy workbook without review.'}
(P/'age_constrained_engine_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'repairs':solves,'values':fitted_values,'scenarios':changes,'fee_check_pct':out['fee_integration_4096_vs_2048_revenue_pct']},indent=2))
