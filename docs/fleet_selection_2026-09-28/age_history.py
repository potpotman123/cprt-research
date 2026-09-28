"""Recheck CCC age-mix versus within-bucket rates using existing data only."""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
paths=[ROOT/'data/csv/ccc_tl_share_by_age_2020_2025.csv',
       ROOT/'data/csv/ccc_tl_valuation_share_by_age_2020_2025.csv']
def read(p):
    with p.open() as f:
        return {r['age_bucket']:r for r in csv.DictReader(l for l in f if not l.startswith('#'))}
rates,shares=map(read,paths)
buckets=[b for b in rates if b!='total']
years=[2022,2023,2024,2025]
prob={y:{b:float(rates[b][f'cy{y}'])/100 for b in buckets} for y in years}
weights={};levels=[]
for y in years:
    raw={b:float(shares[b][f'cy{y}'])/prob[y][b] for b in buckets}
    total=sum(raw.values()); weights[y]={b:v/total for b,v in raw.items()}
    assert math.isclose(sum(weights[y].values()),1,abs_tol=1e-12)
    reconstructed=100*sum(weights[y][b]*prob[y][b] for b in buckets)
    reported=float(rates['total'][f'cy{y}'])
    levels.append(dict(year=y,reconstructed_pct=reconstructed,chart_total_pct=reported,
                       residual_pp=reconstructed-reported))

decompositions=[]
for start,end in [(2022,2025),(2023,2024),(2024,2025)]:
    rows=[]
    for b in buckets:
        w0,w1=weights[start][b],weights[end][b]
        p0,p1=prob[start][b],prob[end][b]
        rows.append(dict(age_bucket=b,rate_start_pct=100*p0,rate_end_pct=100*p1,
            rate_change_pp=100*(p1-p0),claim_weight_start_pct=100*w0,claim_weight_end_pct=100*w1,
            mix_pp=100*(w1-w0)*(p1+p0)/2,
            within_bucket_pp=100*(p1-p0)*(w1+w0)/2))
    mix=sum(r['mix_pp'] for r in rows);within=sum(r['within_bucket_pp'] for r in rows)
    change=100*sum(weights[end][b]*prob[end][b]-weights[start][b]*prob[start][b] for b in buckets)
    assert math.isclose(mix+within,change,abs_tol=1e-12)
    decompositions.append(dict(start=start,end=end,mix_pp=mix,within_bucket_pp=within,
        reconstructed_change_pp=change,
        reported_change_pp=float(rates['total'][f'cy{end}'])-float(rates['total'][f'cy{start}']),rows=rows))

output={'status':'Reported within-bucket rates; aggregate attribution conditional on compatible chart populations',
 'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
 'years_used':years,'note':'2020 excluded; prior notes disagree about its 10-12 rate. No source edits or override needed here.',
 'levels':levels,'decompositions':decompositions,
 'checks':'Weights sum to one; symmetric attribution reconciles; no calibration or workbook changes'}
Path(__file__).with_name('age_history_results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'levels':levels,'decompositions':[{k:v for k,v in x.items() if k!='rows'} for x in decompositions]},indent=2))
