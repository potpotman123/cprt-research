"""Bounded mechanism checks; new sources supply direction/schema, not shocks."""
from pathlib import Path
import sys,csv,json,hashlib,copy
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'model/revenue_architecture_2026-09-28'))
import model as m

def write(name,rows):
 with (OUT/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)

# Fixed operation quantities, fungible sourcing: all inputs illustrative.
# p is initial total-bill share for this substitutable parts basket; s is
# alternative sourcing within it, and d the discount versus an OEM unit.
parts=[]
for p in [.3,.4,.5]:
 for d in [.2,.4,.6]:
  s=.3
  for shift in [.05,.1]:
   before=1-s*d; after=1-(s+shift)*d
   change=p*(after/before-1)
   required=.03*before/(p*d)
   assert abs(change-(-p*shift*d/before))<1e-12
   parts.append(dict(initial_parts_bill_share=p,initial_alternative_quantity_share=s,
       alternative_discount=d,share_shift_pp=100*shift,total_repair_cost_change=change,
       share_shift_pp_for_minus3_bill=100*required,feasible_within_basket=required<=1-s))
write('parts_substitution_hurdles.csv',parts)

# Dollar threshold arithmetic independent of the engine's damage distribution.
gap=[]
for ratio in [.2,.3,.4]:
 v=10000;sn=ratio*v;c=v-sn; saving=.03*c
 gap.append(dict(pre_loss_value=v,expected_net_salvage_share=ratio,threshold_repair_cost=c,
    repair_saving=saving,required_net_salvage_increase=saving,
    required_net_salvage_growth=saving/sn,change_in_margin_if_both_three_pct=-saving+.03*sn))
write('decision_margin_hurdles.csv',gap)

def reference():
 c=m.configuration();c['name']='reference';c['status']='Conditional; no new source-derived shock'
 c['realized_salvage']=m.forecast(1.037)
 data,_,_=m.old.load()
 intl_growth=data['actuals'][3]['intl_service']/data['prior_actuals'][3]['intl_service']
 c['intl_units']=m.forecast(intl_growth/1.035);c['intl_rpu']=m.forecast(1.035)
 return c

# Solve the model's aggregate insurance unit-neutral salvage offset. Use one
# price node only during root-finding: TLF and assignments do not use price nodes.
base=reference(); b=copy.deepcopy(base);b['nodes']=1
target=m.operating(b)[0][4]['assignments']
def units(expected):
 c=copy.deepcopy(b);c['repair']=m.forecast(.97);c['expected_salvage']=m.forecast(expected)
 return m.operating(c)[0][4]['assignments']
lo,hi=1.,1.3
assert units(lo)<target<units(hi)
for _ in range(30):
 mid=(lo+hi)/2
 if units(mid)<target:lo=mid
 else:hi=mid
offset=(lo+hi)/2
assert abs(units(offset)/target-1)<1e-8

configs={}
for name,repair,expected,realized in [
 ('reference',1.,1.,1.037),('repair_only',.97,1.,1.037),
 ('salvage_only',1.,1.03,1.037*1.03),('joint',.97,1.03,1.037*1.03),
 ('repair_salvage_unit_neutral',.97,offset,1.037*offset)]:
 c=reference();c.update(name=name,repair=m.forecast(repair),expected_salvage=m.forecast(expected),realized_salvage=m.forecast(realized))
 configs[name]=c
results={name:m.run(c) for name,c in configs.items()}
rows=[]
for name,r in results.items():
 for i,q in enumerate(r['quarters']):
  op=r['operating'];baseop=op[i];now=op[i+4]
  rows.append(dict(scenario=name,period=q['period'],insurance_unit_growth=q['insurance_sales_factor']-1,
      insurance_selected_ASP_growth=now['ASP']/baseop['ASP']-1,
      insurance_core_RPU_growth=q['insurance_core_RPU_factor']-1,
      insurance_RPU_with_assumed_services_growth=(now['core_RPU']+55)/(baseop['core_RPU']+55)-1,
      title_musd=q['title_musd'],delivery_musd=q['delivery_musd'],
      us_service_musd=q['us_service_musd'],global_legacy_service_musd=q['legacy_service_musd'],
      legacy_total_musd=q['legacy_total_musd'],jpm_total_gap_musd=q['jpm_legacy_total_gap_musd'],
      capiq_gap_CONDITIONAL_musd=q['capiq_conditional_gap_musd'],
      delta_service_vs_reference_musd=q['legacy_service_musd']-results['reference']['quarters'][i]['legacy_service_musd']))
write('quarterly_cases.csv',rows)
delta=lambda name,i:results[name]['quarters'][i]['legacy_service_musd']-results['reference']['quarters'][i]['legacy_service_musd']
interaction=[dict(period=f'FY2027Q{i+1}',repair_delta=delta('repair_only',i),salvage_delta=delta('salvage_only',i),
    joint_delta=delta('joint',i),interaction=delta('joint',i)-delta('repair_only',i)-delta('salvage_only',i)) for i in range(4)]
write('interaction.csv',interaction)
# Illustrative timing of the INCREMENTAL unit change only; baseline is not lagged
# again. Price changes apply in sale quarter. Deferred units retain that quarter's
# scenario RPU. This is not a measured physical-inventory reconstruction.
timing=[]
r=results['joint'];r0=results['reference']
du=[a['modeled_insurance_sales']-b['modeled_insurance_sales'] for a,b in zip(r['quarters'],r0['quarters'])]
for same in [1.,.5,0.]:
 for i,q in enumerate(r['quarters']):
  current=same*du[i]+(1-same)*(du[i-1] if i else 0.)
  usales=r0['quarters'][i]['modeled_insurance_sales']+current
  fee=r['operating'][i+4]['core_RPU']+55
  adjusted=q['legacy_service_musd']+(usales-q['modeled_insurance_sales'])*fee/1e6
  if same==1:assert abs(adjusted-q['legacy_service_musd'])<1e-9
  timing.append(dict(scenario='joint_incremental_timing',same_quarter_fraction=same,period=q['period'],
      global_legacy_service_musd=adjusted,delta_vs_reference_musd=adjusted-r0['quarters'][i]['legacy_service_musd'],
      delta_deferred_beyond_fy_units=(1-same)*du[-1] if i==3 else 0))
 assert abs(sum(same*du[i]+(1-same)*(du[i-1] if i else 0) for i in range(4))+(1-same)*du[-1]-sum(du))<1e-8
write('timing_cases.csv',timing)
# Verify dollar identity and no changes to historical reference allocations.
for r in results.values():
 assert r['base_ledger']==results['reference']['base_ledger']
 for q in r['quarters']:
  assert abs(q['legacy_service_musd']-(q['insurance_core_musd']+q['title_musd']+q['delivery_musd']+q['other_us_musd']+q['intl_service_musd']))<1e-8
summary=dict(status='Conditional mechanism tests; new evidence did not identify a forecast coefficient',
    unit_neutral_expected_salvage_growth=offset-1,
    first_quarter=[row for row in rows if row['period']=='FY2027Q1'],
    joint_timing_q1=[row for row in timing if row['period']=='FY2027Q1'],interaction=interaction,
    checks=['Parts-basket arithmetic','Dollar cancellation','Unit-neutral root','Frozen historical base','Revenue identity','Timing identity/conservation'],
    source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'model/revenue_architecture_2026-09-28/model.py',ROOT/'model/revenue_architecture_2026-09-28/manifest.json']})
(OUT/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
(OUT/'scenario_inputs.json').write_text(json.dumps(configs,indent=2)+'\n')
print(json.dumps(summary,indent=2))
