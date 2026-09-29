"""Bounded inverse-fee arithmetic and existing selection-engine scenarios."""
import ast, csv, hashlib, json, sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
# Reuse only definitions/setup, stopping before the original experiment's writes.
source=ROOT/'docs/auction_price_test_2026-09-28/run.py'
tree=ast.parse(source.read_text()); prefix=[]
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='results' for t in node.targets): break
    prefix.append(node)
ns={'__file__':str(source)}
exec(compile(ast.Module(body=prefix,type_ignores=[]),str(source),'exec'),ns)
amounts=ns['amounts']
def growth(shock,median,sigma,pref,seller):
    return amounts(median*(1+shock),sigma,pref,seller)[1]/amounts(median,sigma,pref,seller)[1]-1
def root(fn,target):
    lo,hi=-.4,.4
    assert fn(lo)<target<fn(hi)
    for _ in range(48):
        mid=(lo+hi)/2
        if fn(mid)<target: lo=mid
        else: hi=mid
    ans=(lo+hi)/2
    assert abs(fn(ans)-target)<1e-10
    return ans
rows=[]
for median in [2500,3500,5000]:
 for sigma in [.8,1.]:
  for pref in [0,.5,1]:
   for seller in [0,.04]:
    fn=lambda x:growth(x,median,sigma,pref,seller)
    rows.append(dict(median=median,sigma=sigma,preferred_fraction=pref,seller_fraction=seller,
        price_change_for_minus2_rpu=root(fn,-.02),rpu_at_price_minus5=fn(-.05),
        rpu_at_price_flat=fn(0),rpu_at_price_plus3p7=fn(.037)))
def write(name,rows):
 with (OUT/name).open('w') as f:
    w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
write('price_hurdles.csv',rows)
sys.path.insert(0,str(ROOT/'model/revenue_architecture_2026-09-28'))
import model as m
base=m.configuration();q0,_=m.operating(base)
scenarios=[]
for name,overrides in [('fleet_only',{}),('price_down5',{'realized_salvage':.95}),
    ('repair_down3',{'repair':.97}),('expected_and_realized_salvage_down5',{'expected_salvage':.95,'realized_salvage':.95}),
    ('price_up3p7',{'realized_salvage':1.037})]:
 c=m.configuration()
 for k,v in overrides.items(): c[k]=m.forecast(v)
 q,_=m.operating(c)
 a,b=q[0],q[4]
 r=(b['core_RPU']+55)/(a['core_RPU']+55)-1
 u=b['assignments']/a['assignments']-1
 scenarios.append(dict(scenario=name,insurance_sale_equivalent_unit_growth=u,
    selected_insurance_ASP_growth=b['ASP']/a['ASP']-1,
    insurance_core_RPU_growth=b['core_RPU']/a['core_RPU']-1,
    insurance_RPU_with_assumed55_services_growth=r,
    insurance_service_revenue_growth=(1+u)*(1+r)-1,
    insurance_RPU_delta_vs_fleet=r-((q0[4]['core_RPU']+55)/(q0[0]['core_RPU']+55)-1)))
write('selection_cases.csv',scenarios)
# For a given positive core-price contribution, quantify the non-price offset.
# These assumed service weights are hurdles, not observed service revenue splits.
ref=next(r for r in rows if r['median']==3500 and r['sigma']==.8 and r['preferred_fraction']==.5 and r['seller_fraction']==.04)
offsets=[]
for price in [0,.037]:
 core0=amounts(3500,.8,.5,.04)[1]-55
 core1=amounts(3500*(1+price),.8,.5,.04)[1]-55
 for share in [.05,.10,.15]:
    g=(core1/core0-1)*(1-share)
    offsets.append(dict(price_growth=price,assumed_service_share=share,
      price_only_RPU_growth=g,required_service_revenue_per_unit_growth=(-.02-g)/share))
write('offset_hurdles.csv',offsets)
# Node refinement checks numerical stability, not the calibrated damage curve.
refinement=[]
for name,ov in [('fleet_only',{}),('repair_down3',{'repair':.97}),('expected_and_realized_salvage_down5',{'expected_salvage':.95,'realized_salvage':.95})]:
 c=m.configuration();c['nodes']=2048
 for k,v in ov.items(): c[k]=m.forecast(v)
 q,_=m.operating(c)
 g=(q[4]['core_RPU']+55)/(q[0]['core_RPU']+55)-1
 before=next(x for x in scenarios if x['scenario']==name)['insurance_RPU_with_assumed55_services_growth']
 refinement.append(dict(scenario=name,RPU_growth_difference_pp=100*(g-before)))
 assert abs(g-before)<.0002
# Actual FY26Q1 US service base; -1% fee-unit scenario used solely for scale.
base_us=855.534;unit_growth=-.01
revenue_minus2=base_us*(1+unit_growth)*.98
revenue_plus2=base_us*(1+unit_growth)*1.02
result=dict(price_hurdle_range=[min(r['price_change_for_minus2_rpu'] for r in rows),max(r['price_change_for_minus2_rpu'] for r in rows)],
    reference=ref,selection=scenarios,offsets=offsets,refinement=refinement,
    all_US_scale=dict(base_musd=base_us,assumed_unit_growth=unit_growth,revenue_at_minus2=revenue_minus2,
       revenue_at_plus2=revenue_plus2,delta_musd=revenue_minus2-revenue_plus2),
    scope='FY27Q1 vs FY26Q1. Price-grid scenarios hypothetical compatible pool; engine insurance only. No adopted forecast.',
    source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,ROOT/'data/csv/copart_fee_grid_2026-09.csv',ROOT/'model/revenue_architecture_2026-09-28/model.py']})
assert all(abs(r['rpu_at_price_flat'])<1e-12 for r in rows)
assert all(r['rpu_at_price_minus5']<0<r['rpu_at_price_plus3p7'] for r in rows)
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
