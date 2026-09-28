"""Bounded shape check prompted by HLDI's older-age collision comparison."""
import csv,hashlib,json,math
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
source=ROOT/'model/integrated_service_2026-09-28/within_13plus_single_age.csv'
rows=list(csv.DictReader(source.open()));ages=range(13,46)
ds={y:{a:0. for a in ages} for y in [2024,2025]}
for x in rows:
 if x['case']=='vintage_body_split' and x['weighting']=='calibrated_claim_proxy':ds[int(x['year'])][int(x['age'])]+=float(x['share_within_13plus'])
for d in ds.values():assert math.isclose(sum(d.values()),1,abs_tol=1e-10)
delta={a:ds[2025][a]-ds[2024][a] for a in ages};results=[]
for peak in [18,19,20,21,22]:
 best=max((sum(delta[a] for a in range(lo,hi+1)),lo,hi) for lo in range(13,peak+1) for hi in range(peak,46))
 ceiling=max(0,best[0])
 # Independently evaluate smooth fixed hump-shaped test functions at several widths.
 for width in [1,3,8,20]:
  change=sum(delta[a]*math.exp(-((a-peak)/width)**2) for a in ages)
  assert change<=ceiling+1e-10
 results.append({'assumed_peak_age':peak,'unimodal_0_to_1_upper_pp':100*ceiling,'maximizing_interval':[best[1],best[2]]})
out={'status':'Shape-only ceiling, not empirical fit; no baseline TLF constraint','results':results,'method':'A bounded nonnegative curve increasing to a fixed peak then decreasing is a layer-cake mixture of interval indicators containing the peak. Max interval mass change bounds any such fixed common curve.','inputs':str(source.relative_to(ROOT)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'checks_passed':22,'limitations':['CY2020 source motivates shape but cannot establish CY2024-25 curve','Single common age curve, no body-specific shape changes','No digitized HLDI chart values adopted','Fitted claim weights and survival unchanged','Age tail to 45 is modeled; HLDI comparison curve extends only to 30']}
(P/'unimodal_bound.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['results'],indent=2))
