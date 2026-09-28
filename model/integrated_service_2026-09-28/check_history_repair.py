"""Meaningful invariance and missing-data tests for the revised historical adapter."""
import copy,json
import engine as m
import history_repair as h

d,e,c=m.load();raw=m.run(d,e,c);rows=h.build(d,c,raw);checks=[]
def check(name,ok):
    if not ok:raise AssertionError(name)
    checks.append(name)
for r in h.operating_bridge(d):
    parts=[r[k] or 0 for k in ['volume_change_musd','RPU_change_musd','interaction_musd','unallocated_change_musd']]
    check(r['period']+r['geography']+' accounting attribution reconciles',m.close(r['prior_service_musd']+sum(parts),r['reported_service_musd']))
q4=h.operating_bridge(d)[3]
check('Missing US Q4 split remains missing',q4['fee_unit_growth'] is None and q4['fee_RPU_growth'] is None and abs(q4['unallocated_change_musd'])>0)
check('Original historical reconstruction errors preserved',all(m.close(r['original_reconstruction_error_musd'],a['us_residual_musd']+a['intl_residual_musd']) for r,a in zip(rows[:4],raw['quarters'][:4])))
check('No invented historical insurance revenue split',all(r['insurance_musd'] is None for r in rows[:4]))
for r in rows[4:]:
    check(r['period']+' branch sum',m.close(r['legacy_service_musd'],r['insurance_musd']+r['other_us_musd']+r['intl_musd']))
    check(r['period']+' units times RPU bridge',m.close(r['insurance_musd'],r['assumed_insurance_base_musd']*r['insurance_units_factor']*r['insurance_RPU_factor']))

# Arbitrarily distort the old seasonal proxy: forward ratios must not change.
distorted=copy.deepcopy(d)
for i,a in enumerate(distorted['prior_actuals']):
    a['us_service']*=1+.2*i;a['intl_service']*=1+.3*i
changed=h.build(distorted,c,m.run(distorted,e,c))
check('Old revenue seasonal proxy cannot drive revised forecasts',all(m.close(a['legacy_service_musd'],b['legacy_service_musd']) for a,b in zip(rows[4:],changed[4:])))

# Freeze all forward operating states to the matching historical quarter.
flat=copy.deepcopy(d);cc=copy.deepcopy(c)
for i in range(4,8):
    flat['periods'][i]['weights']=flat['periods'][i-4]['weights'][:]
    for key in cc['quarter_drivers']:cc['quarter_drivers'][key][i]=cc['quarter_drivers'][key][i-4]
fr=m.run(flat,e,cc)
# Hold capture at the matching quarter without altering the production carrier convention.
for i in range(4,8):
    q,b=fr['quarters'][i],fr['quarters'][i-4]
    q['effective_capture']=b['effective_capture']
flatrows=h.build(flat,cc,fr)
check('Unchanged operating drivers produce unchanged same-quarter revenue',all(m.close(r['legacy_service_musd'],a['us_service']+a['intl_service']) for r,a in zip(flatrows[4:],d['actuals'])))

# Perturb just capture: affects insurance only, exactly once, with history untouched.
rr=copy.deepcopy(raw);rr['quarters'][4]['effective_capture']*=.9
shock=h.build(d,c,rr)
check('Capture decline applied once to insurance, not other branches',m.close(shock[4]['insurance_musd'],rows[4]['insurance_musd']*.9) and shock[4]['other_us_musd']==rows[4]['other_us_musd'] and shock[4]['intl_musd']==rows[4]['intl_musd'] and shock[:4]==rows[:4])
out={'passed':True,'checks_passed':len(checks),'checks':checks,'limitation':'Adapter correctness, not historical causal identification or predictive validation'}
(m.HERE/'history_repair_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
