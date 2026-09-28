"""Exact integration of piecewise posted fees over assumed price distributions.
No sampling, listings, scraping, OCR or spreadsheet mutation.
"""
import csv,json,math,hashlib
from pathlib import Path
from statistics import NormalDist
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
P=ROOT/'data/csv/copart_fee_grid_2026-09.csv'
with P.open() as f: rows=list(csv.DictReader(x for x in f if not x.startswith('#')))
N=NormalDist()
def grid(page,kind):
 return sorted([r for r in rows if r['page']==page and r['title_group']=='non-clean' and r['vehicle_class']=='standard' and r['fee_type']==kind and (kind!='buyer_fee' or r['payment_method']=='secured')],key=lambda r:float(r['band_low_usd']))
standard=grid('non-licensed','buyer_fee')
preferred=grid(next(r['page'] for r in rows if 'high' in r['page']),'buyer_fee')
virtual=grid('non-licensed','virtual_bid_pre_bid')
def expectation(g,median,sigma):
 mu=math.log(median);mean=math.exp(mu+sigma*sigma/2);total=0
 for i,r in enumerate(g):
  lo=float(r['band_low_usd']);hi=float(g[i+1]['band_low_usd']) if i+1<len(g) else math.inf
  zl=-math.inf if lo==0 else (math.log(lo)-mu)/sigma
  zh=math.inf if math.isinf(hi) else (math.log(hi)-mu)/sigma
  mass=N.cdf(zh)-N.cdf(zl)
  value_mass=mean*(N.cdf(zh-sigma)-N.cdf(zl-sigma))
  total+=float(r['fee_usd'] or 0)*mass+float(r['fee_pct'] or 0)/100*value_mass
 return total
def amounts(median,sigma,pref,seller):
 mean=median*math.exp(sigma*sigma/2)
 buyer=(1-pref)*expectation(standard,median,sigma)+pref*expectation(preferred,median,sigma)+expectation(virtual,median,sigma)+110
 return buyer,buyer+seller*mean+55
results=[]
for median in [2500,3500,5000]:
 for sigma in [.8,1.0]:
  for pref in [0,.5,1]:
   for seller in [0,.04]:
    b0,r0=amounts(median,sigma,pref,seller)
    for shock in [-.1,0,.041,.06,.084,.1]:
     b1,r1=amounts(median*(1+shock),sigma,pref,seller)
     results.append(dict(median_usd=median,log_sigma=sigma,preferred_fraction=pref,seller_pct=seller,
      fixed_service_usd_ASSUMED=55,asp_change=shock,buyer_fee_before=b0,buyer_fee_after=b1,
      buyer_fee_growth=b1/b0-1,illustrative_rpu_before=r0,illustrative_rpu_after=r1,illustrative_rpu_growth=r1/r0-1))
     assert (abs(b1-b0)<1e-9 if shock==0 else (b1-b0)*shock>0)
with (OUT/'fee_response.csv').open('w') as f:
 z=csv.DictWriter(f,fieldnames=results[0].keys(),lineterminator='\n');z.writeheader();z.writerows(results)
summary=[]
for shock in [.041,.06,.084,.1]:
 rr=[r for r in results if r['asp_change']==shock]
 base=next(r for r in rr if r['median_usd']==3500 and r['log_sigma']==.8 and r['preferred_fraction']==.5 and r['seller_pct']==.04)
 summary.append(dict(asp_change=shock,buyer_growth_range=[min(r['buyer_fee_growth'] for r in rr),max(r['buyer_fee_growth'] for r in rr)],
  illustrative_rpu_range=[min(r['illustrative_rpu_growth'] for r in rr),max(r['illustrative_rpu_growth'] for r in rr)],reference_rpu_growth=base['illustrative_rpu_growth']))
# Deterministic midpoint check of exact integration; 10k arithmetic nodes, not a listing sample.
g=standard;prices=[3500*math.exp(.8*N.inv_cdf((i+.5)/10000)) for i in range(10000)]
def lookup(p):
 r=next(r for r in reversed(g) if p>=float(r['band_low_usd']))
 return float(r['fee_usd'] or 0)+p*float(r['fee_pct'] or 0)/100
approx=sum(lookup(p) for p in prices)/len(prices);exact=expectation(g,3500,.8)
assert abs(approx-exact)<.5,(approx,exact)
output={'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'scenarios':len(results),'summary':summary,
 'check_exact_vs_deterministic_quadrature_usd':abs(approx-exact),
 'limits':'September schedule held fixed; distributions and seller/service terms assumed; no changes to units, damage selection, bidder budgets or buyer mix; insurance ASP versus all-US RPU not population matched.'}
(OUT/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
