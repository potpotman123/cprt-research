"""Structural acceptance checks, not investment-thesis sensitivity analysis."""
import copy,json,math
from pathlib import Path
import engine as m

d,e,c=m.load();base=m.run(d,e,c);passed=[]
def check(name,condition):
    if not condition:raise AssertionError(name)
    passed.append(name)
def rejected(config):
    try:m.run(d,e,config)
    except ValueError:return True
    return False
check('Eight quarters and 24 economic cells per quarter',len(base['quarters'])==8 and len(base['cohorts'])==192)
for i,q in enumerate(base['quarters']):
    rr=[r for r in base['cohorts'] if r['period']==q['period']]
    cc=[r for r in base['carriers'] if r['period']==q['period']]
    check(q['period']+' component quantities reconcile',m.close(sum(r['fee_sales_raw'] for r in rr),q['fee_sales_raw']) and m.close(sum(r['claim_weight'] for r in rr),1))
    check(q['period']+' carrier capture once',m.close(sum(r['total_loss_weight_proxy'] for r in cc),1) and m.close(sum(r['capture_contribution'] for r in cc),q['effective_capture']))
    if i>=4:
        for r,x in zip(cc,d['carriers']):
            check(q['period']+' allocation '+x['name'],r['allocation']==x['allocations'][i if x['name']=='Progressive' else 3])
check('Base-dollar anchor explicit and unique',m.close(base['quarters'][3]['us_musd'],d['actuals'][3]['us_service']))
check('Earlier historical errors not plugged',any(abs(r['us_residual_musd'])>1 for r in base['quarters'][:3]))
check('Physical inventory not invented in bypass',all(r['physical_opening_inventory'] is None for r in base['quarters']))

# Check calibration population separately from forecast-quarter weights.
eco=m.economics(d,e,c,1,1);selected=[];repairmeans=[];rates=[]
for k,row in enumerate(e['cohorts']):
    tw=tv=rc=rm=0.
    for b in range(4):
        w=e['body_weights'][str(k)][b];x=eco[b,k];u=1-x['probability'];sigma=row['sigma']
        mu=row['log_car_repair_median']+math.log(e['repair_ratios'][b])
        tw+=w*(1-u);tv+=w*(1-u)*x['ACV'];rc+=w*u
        rm+=w*math.exp(mu+.5*sigma*sigma)*m.N.cdf(m.N.inv_cdf(u)-sigma)
    rates.append(tw);selected.append(tv/tw);repairmeans.append(rm/rc)
check('Six calibration TLF targets preserved',max(abs(a-r['target']) for a,r in zip(rates,d['calibration']))<1e-9)
oldvalue=sum(e['TLmix'][k]*selected[k] for k in range(3,6))/sum(e['TLmix'][3:])
check('Four selected age-value targets preserved',max(abs(a-b) for a,b in zip(selected[:3]+[oldvalue],e['selected_value_checks']))<.01)
for ks,target in [(range(3),5721),(range(3,6),3682)]:
    weights=[e['relative_claim_weights'][k]*(1-rates[k]) for k in ks]
    mean=sum(w*repairmeans[k] for w,k in zip(weights,ks))/sum(weights)
    check('Repairable mean '+str(target),abs(mean-target)<.01)

# Input propagation is a plumbing check; do not publish scenario returns as evidence.
x=copy.deepcopy(c);x['quarter_drivers']['repair_cost'][4]=1.01;changed=m.run(d,e,x)
check('Forecast-only change preserves history and fixed normalization',changed['quarters'][:4]==base['quarters'][:4] and changed['claim_scale']==base['claim_scale'])
check('Forecast economic input reaches revenue',changed['quarters'][4]['insurance_musd']!=base['quarters'][4]['insurance_musd'])
x=copy.deepcopy(c);x['quarter_drivers']['reported_claim_frequency'][4]=None
check('Missing claims input rejected, not zero-filled',rejected(x))
x=copy.deepcopy(c);x['timing_mode']='physical_inventory'
check('Unsupported physical timing blocked',rejected(x))
x=copy.deepcopy(c);x['quarter_drivers']['title_adoption_multiplier'][4]=3
check('Impossible adoption rejected',rejected(x))
x=copy.deepcopy(c);x['fee_integration_nodes']=4096;fine=m.run(d,e,x)
fee_error=max(abs(a['core_RPU']/b['core_RPU']-1) for a,b in zip(base['quarters'],fine['quarters']))
check('Fee integration stable within 0.05%',fee_error<.0005)
ar=m.acquisition_rows(d,c)
check('Pre-close acquired revenue zero',all(r['classified_service_musd']==0 for r in ar if r['active_months']==0))
check('Unclassified acquired service remains missing',all(r['classified_service_musd'] is None for r in ar if r['active_months']>0))
x=copy.deepcopy(c);x['acquisition']['classified_service_fraction']=1;x['acquisition']['intercompany_eliminations_musd']=0
testar=m.acquisition_rows(d,x)
check('Acquisition classification adapter works',all(m.close(r['classified_service_musd'],r['management_total_revenue_musd']) for r in testar))
# Round-trip a bundled title convention; no added title dollars when already included.
x=copy.deepcopy(c);x['title']['included_in_seller_fee']=True;t=m.run(d,e,x)
check('Bundled title not billed twice',all(q['title_musd']==0 for q in t['quarters']))
out={'passed':True,'checks_passed':len(passed),'checks':passed,'max_fee_integration_relative_error':fee_error,
     'not_tested':['Predictive validity','True service adoption and unit levels','Actual assignment-to-sale lag','Economic thesis impact or consensus gap'],
     'historical_US_residual_musd':[q['us_residual_musd'] for q in base['quarters'][:4]],
     'historical_international_residual_musd':[q['intl_residual_musd'] for q in base['quarters'][:4]]}
(m.HERE/'checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'}))
