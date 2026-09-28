"""Small conditional identification exercise; no forecast inputs overwritten."""
import csv, hashlib, json, math
from pathlib import Path
from statistics import NormalDist
ROOT=Path(__file__).resolve().parents[2]; N=NormalDist()
src=ROOT/'model/linked_service_revenue_2026-09-28/inputs.json'
d=json.loads(src.read_text())
sp=ROOT/'data/csv/ccc_tl_valuation_share_by_age_2020_2025.csv'
with sp.open() as f: shares={r['age_bucket']:float(r['cy2025'])/100 for r in csv.DictReader(l for l in f if not l.startswith('#'))}
weights={(b,k):sum(r['births'][2]*r['survival']*d['split'][b]*r['relative_claim_weight'] for r in d['fleet'] if r['body']==b and r['bucket']==k) for b in range(4) for k in range(6)}
body={k:[weights[b,k]/sum(weights[z,k] for z in range(4)) for b in range(4)] for k in range(6)}
inferred=[shares[c['age_bucket']]/c['target'] for c in d['calibration']]
model=[sum(weights[b,k] for b in range(4)) for k in range(6)]
def cutoff(mu,acv,sigma,recovery_center=.3):
    lo,hi=1e-12,1-1e-12
    for _ in range(42):
        u=(lo+hi)/2
        # recovery .4-.2u; repair threshold = ACV*(.616+.192u)
        if mu+sigma*N.inv_cdf(u)<math.log(acv*(1-.96*(recovery_center+.1)+.192*u)):lo=u
        else:hi=u
    return (lo+hi)/2
continuous_cutoff=cutoff
def fit(sigma,ageweights,value_slope=.1,recovery_center=.3):
    cutoff=lambda mu,acv,sigma:continuous_cutoff(mu,acv,sigma,recovery_center)
    mus=[];means=[]; acvs=[]
    for k,c in enumerate(d['calibration']):
        vals=[10000*math.exp(-value_slope*(c['representative_age']-10))*v for v in d['value_ratios']];acvs.append(vals)
        lo,hi=0.,15.
        for _ in range(48):
            mu=(lo+hi)/2
            t=sum(body[k][b]*(1-cutoff(mu+math.log(d['repair_ratios'][b]),vals[b],sigma)) for b in range(4))
            if t<c['target']:lo=mu
            else:hi=mu
        mu=(lo+hi)/2;mus.append(mu)
        cost=0.
        for b in range(4):
            mb=mu+math.log(d['repair_ratios'][b]);u=cutoff(mb,vals[b],sigma)
            cost+=body[k][b]*math.exp(mb+.5*sigma*sigma)*N.cdf(N.inv_cdf(u)-sigma)
        means.append(cost/(1-c['target']))
    groups=[]
    for ks,target in [(range(3),5721),(range(3,6),3682)]:
        rw=[ageweights[k]*(1-d['calibration'][k]['target']) for k in ks]
        mean=sum(w*means[k] for w,k in zip(rw,ks))/sum(rw)
        groups.append({'model_repairable_mean_at_original_value_scale':mean,'reference':target,'required_common_ACV_and_repair_scale':target/mean})
    def response(r,v):
        units=proceeds=0.
        for k in range(6):
            for b in range(4):
                acv=acvs[k][b]*v;u=cutoff(mus[k]+math.log(d['repair_ratios'][b]*r),acv,sigma)
                w=ageweights[k]*body[k][b]
                units+=w*(1-u);proceeds+=w*(1-u)*acv*(recovery_center-.1*u)
        return units,proceeds/units
    base=response(1,1)
    responses={name:{'units_pct':100*(response(r,v)[0]/base[0]-1),'ASP_pct':100*(response(r,v)[1]/base[1]-1)} for name,r,v in [('repair_plus_5pct',1.05,1),('value_plus_5pct',1,1.05)]}
    # Verify the continuous implementation hits each total-loss target.
    error=max(abs(sum(body[k][b]*(1-cutoff(mus[k]+math.log(d['repair_ratios'][b]),acvs[k][b],sigma)) for b in range(4))-d['calibration'][k]['target']) for k in range(6))
    assert error<1e-9
    selected=[]
    for k in range(6):
        mass=[body[k][b]*(1-cutoff(mus[k]+math.log(d['repair_ratios'][b]),acvs[k][b],sigma)) for b in range(4)]
        selected.append(sum(mass[b]*acvs[k][b] for b in range(4))/sum(mass))
    selected_mean=sum(ageweights[k]*d['calibration'][k]['target']*selected[k] for k in range(6))/sum(ageweights[k]*d['calibration'][k]['target'] for k in range(6))
    return {'sigma':sigma,'group_results':groups,'max_TLF_error':error,'responses_at_original_scale':responses,'selected_total_loss_ACV_at_original_scale':selected_mean,'selected_total_loss_ACV_by_age_at_original_scale':selected}
out={'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [src,sp]},'status':'Conditional feasibility only. Inferred CCC age weights require compatible populations; 2025 model body weights remain assumptions. No empirical best fit selected.', 'cases':{label:[fit(s,w) for s in [.6,.9,1.2,d['sigma'],2.0]] for label,w in [('conditional_CCC_age_weights',inferred),('model_2025_age_weights',model)]}}
out['joint_fits_not_adopted']={}
for label,w in [('conditional_CCC_age_weights',inferred),('model_2025_age_weights',model)]:
    lo,hi=1.57,2.
    for _ in range(22):
        s=(lo+hi)/2;res=fit(s,w)
        a,b=[g['required_common_ACV_and_repair_scale'] for g in res['group_results']]
        if a<b:lo=s
        else:hi=s
    scale=(a+b)/2
    res['common_scale']=scale;res['implied_age10_car_ACV']=10000*scale
    res['repaired_mean_max_error_usd']=max(abs(g['model_repairable_mean_at_original_value_scale']*scale-g['reference']) for g in res['group_results'])
    assert res['repaired_mean_max_error_usd']<.01
    out['joint_fits_not_adopted'][label]=res
Path(__file__).with_name('joint_calibration_results.json').write_text(json.dumps(out,indent=2)+'\n')
for name,rows in out['cases'].items():
    print(name)
    for r in rows:print(round(r['sigma'],3),[round(g['required_common_ACV_and_repair_scale'],3) for g in r['group_results']],round(r['responses_at_original_scale']['repair_plus_5pct']['units_pct'],3))
print('joint fits',json.dumps(out['joint_fits_not_adopted'],indent=2))
