"""Cheap retrospective compatibility test; no fitted allocation or workbook writes."""
import csv,json,hashlib
from pathlib import Path
import openpyxl
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).parent
P=Path('/Users/kwu/Library/Messages/Attachments/53/03/CDE4DBC0-6774-4ABD-860B-E12504CAF220/CPRT_share_sidebuild.xlsx')
w=openpyxl.load_workbook(P,data_only=True);s=w.worksheets[0]
weights={c:[s.cell(r,c).value for r in range(119,129)] for c in range(3,12)}
alloc={c:[s.cell(r,c).value for r in range(130,140)] for c in range(3,12)}
def share(ww,aa):return sum(x*y for x,y in zip(ww,aa))/sum(ww)
shares={c:share(weights[c],alloc[c]) for c in weights}
panel=list(csv.DictReader(open(ROOT/'data/csv/units_decomp_panel_v2.csv')))[2:]
records=[]
for i,r in enumerate(panel):
 c=i+4; actual=float(r['cprt_us_ins_asrep'])/100
 # Only Q4 has a matching prior-year share column. Other periods stay unavailable.
 sg=shares[c]/shares[c-4]-1 if c-4 in shares else None
 for label in ['fasttrack_collision','ccc_all_coverage','ccc_non_comp']:
  claims=float(r['claims__'+label])/100; tlf=float(r['tlf_yoy_rel_pct'])/100
  pool=(1+claims)*(1+tlf)-1
  pred=(1+pool)*(1+sg)-1 if sg is not None else None
  records.append(dict(quarter=r['cprt_fq'],pool_case=label,actual_insurance_yoy=actual,
   claims_proxy=claims,tlf_relative_change=tlf,pool_proxy=pool,carrier_share_yoy=sg,
   modeled_yoy=pred,error_pp=None if pred is None else (pred-actual)*100,
   required_effective_capture_yoy=(1+actual)/(1+pool)-1,
   status='Conditional retrospective diagnostic; pool populations not matched; Q4 allocation fitted to print' if sg is not None else 'Missing prior-year share; cannot backtest',
   tlf_status=r['tlf_source']))
def save(name,rr):
 with (OUT/name).open('w') as f:
  z=csv.DictWriter(f,fieldnames=rr[0].keys(),lineterminator='\n');z.writeheader();z.writerows(rr)
save('historical_test.csv',records)
model=json.load(open(ROOT/'model/linked_service_revenue_2026-09-28/validation.json'))['quarter_results']
forward=[]
for i,c in enumerate(range(8,12)):
 known=alloc[7].copy();known[1]=alloc[c][1] # PGR only; retain inherited path, not reverified.
 cases={'Friend base':shares[c],'Freeze all at FY26Q4':shares[7],
        'PGR runoff only; fixed carrier mix':share(weights[7],known)}
 for name,a in cases.items():
  insurance=model[i+4]['insurance_m']*a/shares[c]
  forward.append(dict(quarter=f'FY27Q{i+1}',case=name,allocation_level=a,
   allocation_yoy=a/shares[c-4]-1,insurance_revenue_musd=insurance,
   service_revenue_delta_vs_friend_musd=insurance-model[i+4]['insurance_m'],
   scope='Prototype frozen claim/damage/RPU and 90% dollar split; mechanical comparison, not forecast'))
save('forward_comparison.csv',forward)
out={'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),
 'q4_history':[r for r in records if r['quarter']=='FY26Q4'],
 'h1_revenue_delta_musd':{name:sum(r['service_revenue_delta_vs_friend_musd'] for r in forward if r['case']==name and r['quarter'] in ['FY27Q1','FY27Q2']) for name in cases},
 'q1_q3_required_capture_range':{f'FY26Q{i}':[min(r['required_effective_capture_yoy'] for r in records if r['quarter']==f'FY26Q{i}'),max(r['required_effective_capture_yoy'] for r in records if r['quarter']==f'FY26Q{i}')] for i in range(1,4)}}
assert all(abs(sum(x)-1)<1e-9 for x in weights.values())
assert all(r['carrier_share_yoy'] is None for r in records if r['quarter']!='FY26Q4')
assert all(abs(r['service_revenue_delta_vs_friend_musd'])<1e-8 for r in forward if r['case']=='Friend base')
(OUT/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
