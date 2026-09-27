from pathlib import Path
import zipfile,csv,io,json,collections,itertools,hashlib,datetime,shutil
root=Path(__file__).parent;prev=root.parent/'repair_frequency_feasibility'
z=zipfile.ZipFile(prev/'raw/ciss2024.zip')
def read(n):return list(csv.DictReader(io.TextIOWrapper(z.open(n+'.csv'),encoding='utf-8-sig')))
gv,cdc,crash=read('GV'),read('CDC'),read('CRASH')
key=lambda r:(r['CASEID'],r['VEHNO'])
assert len(set(map(key,gv)))==len(gv)
cm={r['CASEID']:r for r in crash};assert len(cm)==len(crash)
front=collections.defaultdict(list)
for r in cdc:
 if r['CDCPLANE']=='F':front[key(r)].append(r)
result={}
for body,codes in [('Car',set(range(1,10))|{17}),('SUV',{14,15,16,19})]:
 eligible=[r for r in gv if int(r['BODYTYPE']) in codes and 7<=int(cm[r['CASEID']]['CRASHYEAR'])-int(r['MODELYR'])<=9]
 have=[r for r in eligible if key(r) in front]
 ev=[e for r in have for e in front[key(r)]]
 result[body]={'all_age_body_vehicle_records':len(eligible),'vehicles_with_any_recorded_front_CDC':len(have),'front_CDC_records':len(ev),'vehicles_multiple_front_CDC':sum(len(front[key(r)])>1 for r in have),'inspection_status_among_front_vehicles':dict(collections.Counter(r['INSPTYPE'] for r in have)),'front_event_extent_codes':dict(collections.Counter(e['CDCEXTENT'] for e in ev)),'front_event_A_pillar_codes':dict(collections.Counter(e['DAMAPILLAR'] for e in ev))}
(root/'ciss_completeness.json').write_text(json.dumps({'status':'unweighted field-availability audit, not frequency estimates; any recorded front event, not initial impact; all case categories retained','cohorts':result},indent=2))
# Exhaustive 10-percentage-point grid: no designated central/base distribution.
dists=[{'exterior':a/10,'intermediate':b/10,'extensive':(10-a-b)/10} for a in range(11) for b in range(11-a)]
assert len(dists)==66 and all(abs(sum(d.values())-1)<1e-12 for d in dists)
rows=[]
for i,(car,suv) in enumerate(itertools.product(dists,dists)):
 r={'case_id':i+1}
 for body,d in [('car',car),('suv',suv)]:
  for k,v in d.items():r[body+'_'+k+'_share']=v
 rows.append(r)
with (root/'scope_grid.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
config={'status':'UNVALIDATED SCENARIO INPUTS, NOT ESTIMATED PROBABILITIES','population':'hypothetical front-impact cases, conditional on front impact; target 7-9-year-old cars and SUVs','scope_definitions':{'exterior':'Provisional exterior-only complete repair bundle; precise component list and equipment still to be priced','intermediate':'Provisional mutually exclusive complete bundle with additional lamp/reinforcement/cooling work; NOT exterior costs added twice','extensive':'Provisional complete deeper-damage bundle; structural inclusion to be specified'},'costs_usd':{'car':dict.fromkeys(dists[0]),'suv':dict.fromkeys(dists[0])},'model_rule':'average_front_cost = sum(scope_share * complete_scope_cost); missing costs produce unavailable, not zero','car_vs_suv_rule':'SUV average minus car average; divide by car average only if positive','all_impact_rule':'Not calculated: CRSS crash weights are not claims weights, and rear/side/other costs remain missing','total_loss_rule':'Not calculated: need same-population ACV, salvage and cost distributions, including total losses','grid_step_pp':10,'base_case':None,'probability_assigned_to_grid_cases':None}
(root/'scope_inputs.json').write_text(json.dumps(config,indent=2))
# Identity tests for later implementation, NOT empirical cost assumptions.
def cost(d,c):return sum(d[k]*c[k] for k in d)
assert cost({'exterior':1,'intermediate':0,'extensive':0},{'exterior':2,'intermediate':5,'extensive':9})==2
assert abs(cost({'exterior':.5,'intermediate':.3,'extensive':.2},{'exterior':2,'intermediate':5,'extensive':9})-4.3)<1e-12
assert len(rows)==4356
(root/'qa.json').write_text(json.dumps({'distribution_count':66,'paired_cases':4356,'shares_sum_to_one':True,'nonnegative_shares':True,'arithmetic_identity_checks':True,'costs_calibrated':False},indent=2))
print(json.dumps(result,indent=2));print('Built 4356 assumption combinations; no empirical cost premium produced.')
