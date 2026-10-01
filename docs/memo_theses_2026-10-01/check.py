from pathlib import Path
import csv,json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
cells=list(csv.DictReader((ROOT/'model/ccc_age_body_2026-09-29/source_cells.csv').open()));years={}
for r in cells:years.setdefault(int(r['year']),{})[(r['source_body'],r['age_group'])]={k:float(r[k]) for k in ['tlf','tl_mix','derived_claim_weight']}
results=[]
for a,b in [(2020,2025),(2024,2025)]:
 x,y=years[a],years[b];p0=sum(v['tlf']*v['derived_claim_weight'] for v in x.values());p1=sum(v['tlf']*v['derived_claim_weight'] for v in y.values());within=sum((y[k]['tlf']-x[k]['tlf'])*(y[k]['derived_claim_weight']+x[k]['derived_claim_weight'])/2 for k in x);mix=sum((y[k]['derived_claim_weight']-x[k]['derived_claim_weight'])*(y[k]['tlf']+x[k]['tlf'])/2 for k in x)
 assert abs(within+mix-(p1-p0))<1e-12
 results.append(dict(start=a,end=b,tlf_start=p0,tlf_end=p1,within_group_pp=within*100,composition_pp=mix*100,composition_fraction_of_change=mix/(p1-p0),status='Derived symmetric decomposition; common-population assumption and broad age buckets; not causal'))
series=['CUSR0000SETE','CUSR0000SETA01','CUSR0000SETA02'];data={}
with (ROOT/'raw/bls/cu.data.14.USTransportation').open() as f:
 for raw in csv.DictReader(f,delimiter='\t'):
  r={k.strip():v.strip() for k,v in raw.items()}
  if r['series_id'] in series:
   try:data[(r['series_id'],r['year'],r['period'])]=float(r['value'])
   except ValueError:pass
prices=[]
for s in series:
 a,b,c=(data[(s,y,m)] for y,m in [('2020','M01'),('2025','M08'),('2026','M08')]);prices.append(dict(series=s,jan2020=a,aug2025=b,aug2026=c,change_since_jan2020_pct=100*(c/a-1),aug2026_yoy_pct=100*(c/b-1),adjustment='Seasonally adjusted; saved BLS vintage; index is not a household premium quote or income-relative affordability measure'))
out=dict(checks='PASS',decomposition=results,cpi=prices,car_age4to6_tlf={str(y):years[y][('Car','2')]['tlf'] for y in [2020,2025]},forecast_inputs_changed=False)
(P/'checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
