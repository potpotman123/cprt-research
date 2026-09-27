from pathlib import Path
import re,csv,json,hashlib,shutil
p=Path(__file__).parent
text=(p/'raw/ccc2018_figure32.txt').read_text()
lines=[l for l in text.splitlines() if l.startswith('MY15-MY16') and '%' in l]
assert len(lines)==4
low=[.01,500.01,1000.01,2000.01,3000.01,4000.01,5000.01,6000.01,10000.01,15000.01,20000.01]
high=[500,1000,2000,3000,4000,5000,6000,10000,15000,20000,30000]
mid=[(a+b)/2 for a,b in zip(low,high)]
raw=[];summ=[];scaled=[]
bench={'CCC_2025_age7plus_all_loss':5721-2039,'Mitchell_Q2_2026_US_ICE_all_age':4955}
for j,line in enumerate(lines):
 ident=f'sedan_{j//2+1}_'+('no_adas' if 'NO ADAS' in line else 'adas')
 vals=[float(n) for n in re.findall(r'([0-9.]+)%',line)];assert len(vals)==11
 total=sum(vals);assert abs(total-100)<=.55
 w=[v/total for v in vals]
 mean=sum(a*b for a,b in zip(w,mid));lo=sum(a*b for a,b in zip(w,low));hi=sum(a*b for a,b in zip(w,high))
 summ.append({'reference':ident,'printed_percent_sum':total,'midpoint_mean_2017':mean,'lower_endpoint_mean':lo,'upper_endpoint_mean':hi,'printed_share_cost_above_6000_pct':sum(vals[7:])})
 for i in range(11):raw.append({'reference':ident,'bin':i+1,'lower_usd':low[i],'upper_usd':high[i],'printed_pct':vals[i],'normalized_share':w[i],'midpoint_assumption_usd':mid[i]})
 for label,target in bench.items():
  factor=target/mean
  assert abs(sum(wi*mi*factor for wi,mi in zip(w,mid))-target)<1e-8
  for i in range(11):scaled.append({'reference':ident,'benchmark':label,'benchmark_mean_usd':target,'scale_factor_NOT_inflation':factor,'bin':i+1,'normalized_share':w[i],'scenario_lower_usd':low[i]*factor,'scenario_upper_usd':high[i]*factor,'scenario_midpoint_usd':mid[i]*factor,'status':'assumed_shape_transfer_and_mean_alignment_not_observed_front_cohort'})
for name,rows in [('historical_bins.csv',raw),('historical_summary.csv',summ),('benchmark_aligned_bins.csv',scaled)]:
 with (p/name).open('w') as f:
  writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
(p/'qa.json').write_text(json.dumps({'four_source_series':len(lines),'eleven_bins_each':True,'printed_sums':[r['printed_percent_sum'] for r in summ],'normalization':'each percentage divided by its series sum; printed values retained','benchmark_means_reconcile':True,'estimated_population_mean':False,'no_tail_extrapolation':True},indent=2))
print(json.dumps(summ,indent=2))
