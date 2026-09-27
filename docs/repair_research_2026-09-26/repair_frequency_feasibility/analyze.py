"""CRSS2024 feasibility: observed fields, vehicle-level domains, PSU-linearized SEs."""
from pathlib import Path
import zipfile,csv,io,json,collections,math,hashlib
root=Path(__file__).parent
z=zipfile.ZipFile(root/'raw/crss2024.zip')
def read(name):return list(csv.DictReader(io.TextIOWrapper(z.open('CRSS2024CSV/'+name+'.csv'),encoding='utf-8-sig')))
a=read('accident');v=read('vehicle');am={r['CASENUM']:r for r in a}
assert len(am)==len(a)
assert len({(r['CASENUM'],r['VEH_NO']) for r in v})==len(v)
psus=collections.defaultdict(set)
for r in a:psus[r['PSUSTRAT']].add(r['PSU_VAR'])
assert all(len(p)>1 for p in psus.values())
ex=collections.Counter();clean=[];mapping={**{i:'Car' for i in [1,2,3,4,5,6,7,8,9,17]},**{i:'SUV' for i in [14,15,16,19]},**{i:'Pickup' for i in [32,33,34,39]},20:'Minivan'}
for r in v:
 crash=am[r['CASENUM']]
 assert float(r['WEIGHT'])==float(crash['WEIGHT'])
 for key in ['PSUSTRAT','PSU_VAR']:assert r[key]==crash[key]
 b=mapping.get(int(r['BODY_TYP']))
 if not b:ex['body_outside_selected_or_unknown']+=1;continue
 year=int(r['MOD_YEAR']);cy=int(crash['YEAR'])
 if not 1900<=year<=cy+1:ex['missing_invalid_model_year']+=1;continue
 age=max(0,cy-year)
 if year>cy:ex['next_model_year_assigned_age_zero']+=1
 agebin=next(label for hi,label in [(3,'0-3'),(6,'4-6'),(9,'7-9'),(12,'10-12'),(999,'13+')] if age<=hi)
 impact=int(r['IMPACT1']);dam=int(r['DEFORMED'])
 clean.append(dict(body=b,age=agebin,w=float(r['WEIGHT']),h=r['PSUSTRAT'],p=r['PSU_VAR'],front=impact in [11,12,1],rear=impact in [5,6,7],unknown_impact=impact in [98,99],disabling=dam==6,unknown_damage=dam in [7,8,9]))
def calc(rows,metric):
 total=sum(r['w'] for r in rows);num=sum(r['w']*r[metric] for r in rows);ratio=num/total
 u=collections.defaultdict(float)
 for r in rows:u[(r['h'],r['p'])]+=r['w']*(r[metric]-ratio)/total
 variance=0
 for h,ps in psus.items():
  vals=[u[(h,p)] for p in ps];mean=sum(vals)/len(vals)
  variance+=len(vals)/(len(vals)-1)*sum((x-mean)**2 for x in vals)
 return ratio,math.sqrt(variance)
output=[]
for body in ['Car','SUV','Pickup','Minivan']:
 for age in ['0-3','4-6','7-9','10-12','13+']:
  rows=[r for r in clean if r['body']==body and r['age']==age]
  o={'body':body,'age':age,'sample_n':len(rows),'weighted_vehicle_involvements':sum(r['w'] for r in rows)}
  for m in ['front','rear','unknown_impact','disabling','unknown_damage']:
   q,se=calc(rows,m);o[m+'_share']=q;o[m+'_se']=se
  output.append(o)
with (root/'cohort_table.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(output[0]));w.writeheader();w.writerows(output)
qa={'accident_rows':len(a),'vehicle_rows':len(v),'retained_rows':len(clean),'exclusions_and_age_flags':dict(ex),'strata':len(psus),'variance_psus':sum(map(len,psus.values())),'unique_keys':True,'all_vehicle_crash_weights_and_design_ids_match':True,'method':'ratio linearization, with-replacement stratified PSU totals; zero residuals for out-of-domain PSUs; no FPC; SEs not full nonsampling uncertainty'}
(root/'qa.json').write_text(json.dumps(qa,indent=2))
print(json.dumps(qa))
for r in output:
 if r['age'] in ['7-9','10-12'] and r['body']!='Minivan':print(r['body'],r['age'],'n',r['sample_n'],*[f'{k} {100*r[k+"_share"]:.1f}% SE {100*r[k+"_se"]:.1f}pp' for k in ['front','rear','disabling','unknown_damage']])
