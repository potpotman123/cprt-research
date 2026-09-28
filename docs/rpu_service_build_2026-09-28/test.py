"""Small conditional cost-to-revenue screen; not an estimate of reported service revenue."""
import csv,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=Path(__file__).parent
rows=[]
for quarter,cost,prior in [('FY26Q3',15,898.625),('FY26Q4',17,824.813)]:
 for attributable in [.5,1]:
  for margin in [0,.1,.2,.3]:
   revenue=cost*attributable/(1-margin)
   rows.append(dict(quarter=quarter,reported_delivery_cost_increase_musd=cost,
    assumed_share_linked_to_incremental_completed_jobs=attributable,
    assumed_constant_gross_margin=margin,conditional_revenue_increase_musd=revenue,
    contribution_to_us_service_growth_pp=revenue/prior*100,
    status='Conditional US allocation and constant margin; not company revenue disclosure'))
with (O/'delivery_cases.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
for row in rows:
 assert abs(row['conditional_revenue_increase_musd']*(1-row['assumed_constant_gross_margin'])-row['reported_delivery_cost_increase_musd']*row['assumed_share_linked_to_incremental_completed_jobs'])<1e-10
# Exact margin-change identity example, intentionally illustrative.
example={'prior_revenue_ASSUMED':40,'prior_margin_ASSUMED':.2,'current_margin_ASSUMED':.1,'cost_increase':15}
example['delta_revenue']=(15+40*(.1-.2))/(1-.1)
files=[R/'raw/transcripts'/f'call_{x}.txt' for x in ['2025-02-20','2026-02-19','2026-05-21','2026-09-10']]
(O/'provenance.json').write_text(json.dumps({'inputs':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'margin_change_example':example,'checks':'Constant margin arithmetic identities passed'},indent=2)+'\n')
print(json.dumps([r for r in rows if r['assumed_share_linked_to_incremental_completed_jobs']==1 and r['assumed_constant_gross_margin']==.2],indent=2))
