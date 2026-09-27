"""Bounded, local sensitivity of the prior E1 model; no source mutation/network."""
import ast, csv, hashlib, io, json, math, pathlib, statistics, subprocess, time
from pypdf import PdfReader
ROOT=pathlib.Path('/Users/kwu/cprt');OUT=pathlib.Path(__file__).resolve().parent
started=time.perf_counter()
ref='origin/claude/jolly-edison-4f0gk9'
source=subprocess.check_output(['git','show',f'{ref}:scripts/experiments/e1_body_propensity.py'],cwd=ROOT,text=True)
ns={'__file__':str(ROOT/'scripts/experiments/e1_body_propensity.py')}
# The inspected prefix only loads compact local tables and defines the cohort model.
exec(compile(source.split('print("1. σ_eff')[0],'<prior model setup>','exec'),ns)
tree=ast.parse(source)
funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('split','roll')]
exec(compile(ast.Module(body=funcs,type_ignores=[]),'<prior model functions>','exec'),ns)
ages=ns['bucket_mean_age'](2024);buckets=ns['BUCK']
_,gamma,_=ns['ols']([ages[b] for b,_,_ in buckets],[ns['Phi_inv'](ns['CCC'][b]['cy2024']) for b,_,_ in buckets])
sigma=0.11/gamma
baseline=ns['roll'](1.0,{a:(ns['Pf'](a),ns['Pf'](a),0) for a in ns['AGES']})

def model(repair=1.01,value=1.5,price=None,sig=None):
    """value = effective total-loss threshold ratio, price = auction ASP ratio."""
    price=value if price is None else price
    shift=math.log(value/repair)/(sigma if sig is None else sig)
    curves=ns['split'](2024,1.0,shift);r=ns['roll'](1.0,curves)
    a,b=r[2026],r[2027]
    units=100*((b[0]-a[0])-(baseline[2027][0]-baseline[2026][0]))/a[0]
    asp=100*(price-1)*(b[2]-a[2])/(1+(price-1)*a[2])
    rpu=.514*asp
    return {'repair_ratio':repair,'threshold_ratio':value,'auction_price_ratio':price,'sigma':sigma if sig is None else sig,'units_effect_pct':units,'rpu_effect_pct':rpu,'revenue_additive_pct':units+rpu,'revenue_compounded_pct':100*((1+units/100)*(1+rpu/100)-1),'tlf_2027_pct':100*b[0]}

def break_even(value,price=None,sig=None):
    lo,hi=.5,2.5
    assert model(lo,value,price,sig)['revenue_compounded_pct']<0<model(hi,value,price,sig)['revenue_compounded_pct']
    for _ in range(45):
        mid=(lo+hi)/2
        if model(mid,value,price,sig)['revenue_compounded_pct']<0:lo=mid
        else:hi=mid
    return (lo+hi)/2

# Transcribe only class aggregates from the actual table, retaining raw licensed PDF locally.
text=PdfReader(ROOT/'raw/hldi/Collision_summary_2025.pdf').pages[2].extract_text()
lines=[l.strip() for l in text.splitlines()]
def block(start,end):
    return '\n'.join(lines)[('\n'.join(lines)).index(start):('\n'.join(lines)).index(end)]
import re
def triples(start,end):return [tuple(map(int,m)) for m in re.findall(r'(\d+)\s+(\d+)\s+(\d+)\s*$',block(start,end),re.M)]
classes={'four_door':triples('Four-door cars','Station wagons'),'pickups':triples('Pickups Small','SUVs Mini'),'suv':triples('SUVs Mini','Luxury SUVs Small'),'minivan':triples('Minivans Very large','Sports cars Mini')}
assert {k:len(v) for k,v in classes.items()}=={'four_door':5,'pickups':3,'suv':5,'minivan':1}
means={k:{'frequency_mean':statistics.mean(x[0] for x in v),'paid_severity_mean':statistics.mean(x[1] for x in v),'size_rows':len(v)} for k,v in classes.items()}
lt_rows=classes['pickups']+classes['suv']+classes['minivan']
paid_ratio=statistics.mean(x[1] for x in lt_rows)/means['four_door']['paid_severity_mean']
equal_class_ratio=statistics.mean(means[k]['paid_severity_mean'] for k in ['pickups','suv','minivan'])/means['four_door']['paid_severity_mean']
prior_car_rows=classes['four_door'][1:] # Earlier report explicitly uses mini-to-large: excludes microcars.
prior_paid_ratio=statistics.mean(x[1] for x in lt_rows)/statistics.mean(x[1] for x in prior_car_rows)
assert abs(prior_paid_ratio-1.01)<.005
oldcsv=subprocess.check_output(['git','show',f'{ref}:data/csv/body_mix_tlf_asp_2015_2030.csv'],cwd=ROOT,text=True)
old=next(x for x in csv.DictReader(l for l in oldcsv.splitlines() if not l.startswith('#')) if x['year']=='2027')
base=model()
assert abs(base['revenue_additive_pct']-float(old['revenue_effect_pct']))<.00051
grid=[model(c,v) for v in [1.3,1.5,1.7] for c in [1.0,1.01,1.05,1.10,1.15,1.20,1.30,1.50]]
thresholds=[{'value_and_price_ratio':v,'repair_break_even':break_even(v)} for v in [1.3,1.5,1.7]]
dispersion=[{'sigma':s,'base_revenue_pct':model(sig=s)['revenue_compounded_pct'],'repair_break_even':break_even(1.5,sig=s)} for s in [1.05,sigma,2.0]]
# Coherent illustrative recovery changes: car net recovery/ACV=.30, LT ACV/car=1.50.
# Auction price ratio follows net recovery ratio assuming equal proportional deductions.
recovery=[]
for lt_fraction in [.20,.25,.30,.35,.40]:
    threshold=1.5*(1-lt_fraction)/.70
    auction=1.5*lt_fraction/.30
    recovery.append({'car_net_recovery_fraction':.30,'lt_net_recovery_fraction':lt_fraction,**model(1.01,threshold,auction)})
# Sign checks: equal cost/threshold removes the body propensity split; greater repair raises modeled units.
assert abs(model(1.5,1.5)['units_effect_pct'])<1e-9
assert all(model(c,1.5)['revenue_compounded_pct']<model(c+.01,1.5)['revenue_compounded_pct'] for c in [1,1.1,1.2])
out={'source_ref':ref,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'sigma':sigma,'baseline_replication':base,'class_means_from_primary_table':means,'prior_mini_to_large_car_severity_mean':statistics.mean(x[1] for x in prior_car_rows),'prior_mini_to_large_car_frequency_mean':statistics.mean(x[0] for x in prior_car_rows),'prior_paid_ratio_excluding_microcars':prior_paid_ratio,'paid_ratio_including_microcars':paid_ratio,'paid_severity_ratio_equal_classes_including_microcars':equal_class_ratio,'include_microcars_scenario':model(paid_ratio),'arithmetic_audit':'Prior 1.01 ratio is reproducible. Initial apparent discrepancy was microcar inclusion, not an arithmetic error. Neither population supplies repair-only severity.','grid':grid,'repair_break_even':thresholds,'dispersion':dispersion,'recovery':recovery,'elapsed_seconds':time.perf_counter()-started,'scope':'Sensitivity of prior all-light-truck model; not a newly estimated SUV-specific causal model'}
(OUT/'body_sensitivity_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k not in ['grid','source_sha256']},indent=2))
