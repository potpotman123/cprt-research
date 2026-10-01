from pathlib import Path
import copy,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'model/revenue_architecture_2026-09-28'))
import model as m
ref=json.loads((ROOT/'model/ccc_age_body_2026-09-29/reference_config.json').read_text())
a={}
for k in ['premium','income','vehicle_value','deductible']:
    a[k]=[100.]*4;a['reference_'+k]=[100.]*4
# All behavioral probabilities, exposure, slopes and lag are illustrative.
a.update(baseline_coverage_probability=.8,baseline_repairable_filing_probability=.9,affected_baseline_claim_fraction=.5,quarterly_adjustment_fraction=.5,coverage_income_slope=1.,coverage_value_slope=1.,coverage_payoff_slope=1.,filing_income_slope=1.,filing_deductible_slope=1.,excess_lien_free_fraction=[0.]*4,claims_excludes_premium_channels=False,status='All behavioral inputs ASSUMED; indices relative to explicit reference')
cases={'same_as_reference':copy.deepcopy(a),'premiums_10pct_above_reference':copy.deepcopy(a),'filing_only':copy.deepcopy(a),'premiums_5pct_below_reference':copy.deepcopy(a),'income_catches_up':copy.deepcopy(a),'payoff_10pp_above_reference':copy.deepcopy(a),'shock_then_relief':copy.deepcopy(a)}
cases['premiums_10pct_above_reference']['premium']=[110.]*4
cases['filing_only']['premium']=[110.]*4;cases['filing_only']['coverage_income_slope']=0.;cases['filing_only']['coverage_value_slope']=0.
cases['premiums_5pct_below_reference']['premium']=[95.]*4
cases['income_catches_up']['premium']=[110.]*4;cases['income_catches_up']['income']=[110.]*4;cases['income_catches_up']['vehicle_value']=[110.]*4;cases['income_catches_up']['deductible']=[110.]*4
cases['payoff_10pp_above_reference']['excess_lien_free_fraction']=[.1]*4
cases['shock_then_relief']['premium']=[110.,110.,100.,100.]
base=m.run(ref);annual=lambda r:sum(q['legacy_service_musd'] for q in r['quarters']);out={}
for name,assumptions in cases.items():
 c=copy.deepcopy(ref);c['premium_assumptions']=assumptions;r=m.run(c)
 assert r['base_ledger']==base['base_ledger']
 out[name]={'service_musd':annual(r),'delta_musd':annual(r)-annual(base),'quarters':[{'period':q['period'],'units_vs_reference':q['modeled_insurance_sales']/b['modeled_insurance_sales']-1,'tlf':q['TLF']} for q,b in zip(r['quarters'],base['quarters'])],'premium_diagnostics':r['premium_diagnostics']}
for k in ['same_as_reference','income_catches_up','filing_only']:assert abs(out[k]['delta_musd'])<1e-8
assert out['premiums_10pct_above_reference']['delta_musd']<0<out['premiums_5pct_below_reference']['delta_musd']
assert out['filing_only']['quarters'][0]['tlf']>out['same_as_reference']['quarters'][0]['tlf']
x=out['shock_then_relief']['quarters'];assert x[1]['units_vs_reference']<x[2]['units_vs_reference']<x[3]['units_vs_reference']<0
for bad in ['nonfiling','claims']:
 c=copy.deepcopy(ref);c['premium_assumptions']=a;c[bad][4:]=[.1 if bad=='nonfiling' else .9]*4
 try:m.run(c)
 except ValueError:pass
 else:raise AssertionError('Double counting accepted')
for key in ['affected_baseline_claim_fraction','quarterly_adjustment_fraction']:
 c=copy.deepcopy(ref);b=copy.deepcopy(cases['premiums_10pct_above_reference']);b[key]=0;c['premium_assumptions']=b
 assert abs(annual(m.run(c))-annual(base))<1e-8
c=copy.deepcopy(ref);b=copy.deepcopy(a);b['premium'][0]=-1;c['premium_assumptions']=b
try:m.run(c)
except ValueError:pass
else:raise AssertionError('Invalid premium accepted')
assert 'premium_assumptions' not in ref
(HERE/'assumptions.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'results.json').write_text(json.dumps({'checks':'PASS','forecast_admission':False,'cases':out},indent=2)+'\n')
print(json.dumps({k:round(v['delta_musd'],4) for k,v in out.items()},indent=2))
