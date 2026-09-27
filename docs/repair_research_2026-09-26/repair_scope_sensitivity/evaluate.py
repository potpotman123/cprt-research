"""Evaluate explicit scope sensitivities only after documented complete-bundle costs exist."""
from pathlib import Path
import csv,json,math
p=Path(__file__).parent
cfg=json.loads((p/'scope_inputs.json').read_text());costs=cfg['costs_usd'];scopes=['exterior','intermediate','extensive']
missing=[f'{b}.{s}' for b in ['car','suv'] for s in scopes if costs[b][s] is None]
if missing:raise SystemExit('No cost estimate generated. Missing complete-bundle costs: '+', '.join(missing))
assert all(isinstance(costs[b][s],(int,float)) and math.isfinite(costs[b][s]) and costs[b][s]>=0 for b in costs for s in scopes)
rows=list(csv.DictReader((p/'scope_grid.csv').open()))
for r in rows:
 for b in ['car','suv']:
  assert abs(sum(float(r[f'{b}_{s}_share']) for s in scopes)-1)<1e-10
  r[b+'_average_front_cost']=sum(float(r[f'{b}_{s}_share'])*costs[b][s] for s in scopes)
 r['suv_minus_car']=r['suv_average_front_cost']-r['car_average_front_cost']
 r['suv_premium']=r['suv_average_front_cost']/r['car_average_front_cost']-1 if r['car_average_front_cost']>0 else None
with (p/'evaluated_cost_cases.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Evaluated scenario cases; no likelihoods assigned, no single base case selected.')
