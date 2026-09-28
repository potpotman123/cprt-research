"""Fee thresholds: concentration, aggregate smoothing and prototype node diagnostics."""
import contextlib,io,runpy,json,csv,math
from pathlib import Path
import openpyxl
HERE=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()): a=runpy.run_path(str(HERE/'run.py'))
N=a['N']; std=a['standard'];pref=a['preferred'];virt=a['virtual'];root=a['ROOT']
def fee(p,g):
 r=next(r for r in reversed(g) if p>=float(r['band_low_usd']))
 return float(r['fee_usd'] or 0)+p*float(r['fee_pct'] or 0)/100
def buyer(p):return .5*fee(p,std)+.5*fee(p,pref)+fee(p,virt)+110
thresholds=sorted(set(float(r['band_low_usd']) for g in [std,pref,virt] for r in g if float(r['band_low_usd'])>0))
jumps={t:buyer(t)-buyer(t-1e-7) for t in thresholds}
records=[]
median=3500;sigma=.8
base=a['amounts'](median,sigma,.5,.04)
for shock in [.01,.03,.05]:
 for t in thresholds:
  mass=N.cdf(math.log(t/median)/sigma)-N.cdf(math.log(t/(1+shock)/median)/sigma)
  records.append({'price_shift':shock,'threshold_usd':t,'buyer_fee_jump_usd':jumps[t],
   'assumed_crossing_fraction':mass,'mean_buyer_fee_contribution_usd':mass*jumps[t]})
with (HERE/'threshold_crossings.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=records[0],lineterminator='\n');w.writeheader();w.writerows(records)
summary=[]
for shock in [.01,.03,.05]:
 rr=[r for r in records if r['price_shift']==shock]
 delta=a['amounts'](median*(1+shock),sigma,.5,.04)[0]-base[0]
 top=sorted(rr,key=lambda r:r['mean_buyer_fee_contribution_usd'],reverse=True)[:5]
 summary.append({'price_shift':shock,'buyer_fee_delta_usd':delta,'buyer_growth':delta/base[0],
  'jump_component_usd':sum(r['mean_buyer_fee_contribution_usd'] for r in rr),
  'continuous_percentage_component_usd':delta-sum(r['mean_buyer_fee_contribution_usd'] for r in rr),
  'top_five':top})
# A narrow mass around a boundary is a stress case, not an empirical price histogram.
stress=[{'threshold_usd':t,'jump_usd':jumps[t],
 'crossing_fraction_for_1pct_reference_rpu':.01*base[1]/jumps[t]} for t in thresholds if jumps[t]>=25]
# Read 216 already modeled Q4 price states; no auction listings or new collection.
p=root/'outputs/cprt-linked-20260928/CPRT_Linked_Service_Revenue.xlsx'
w=openpyxl.load_workbook(p,data_only=True,read_only=True);s=w['Damage Engine']
nodes=[(row[0],row[6]) for row in s.iter_rows(min_row=654,max_row=869,min_col=15,max_col=21,values_only=True)];w.close()
def smoothfee(p,width):
 if width==0:return buyer(p)
 lo=p*(1-width);hi=p*(1+width)
 cuts=[lo]+[t for t in thresholds if lo<t<hi]+[hi]
 # Midpoint is exact within each linear segment of a uniform price interval.
 return sum((y-x)*buyer((x+y)/2) for x,y in zip(cuts,cuts[1:]))/(hi-lo)
node_tests=[]
for width in [0,.025,.05,.1]:
 b=sum(smoothfee(p,width)*u for p,u in nodes)/sum(u for p,u in nodes)
 for shock in [.01,.03,.05]:
  after=sum(smoothfee(p*(1+shock),width)*u for p,u in nodes)/sum(u for p,u in nodes)
  node_tests.append({'within_node_uniform_halfwidth':width,'price_shift':shock,'buyer_fee_growth':after/b-1})
out={'reference_distribution':{'median':median,'log_sigma':sigma,'preferred_fraction':.5,'seller_rate_ASSUMED':.04,'fixed_services_ASSUMED':55},
 'reference_buyer_fee':base[0],'reference_rpu':base[1],'aggregate_tests':summary,
 'concentration_stress':stress,'prototype_node_tests':node_tests,
 'interpretation':'Thresholds are real. Aggregate timing/concentration and within-node price dispersion are assumptions, not measured catalysts.'}
(HERE/'catalyst_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'reference_rpu':base[1],'aggregate':[{k:v for k,v in r.items() if k!='top_five'} for r in summary],'top_3pct':summary[1]['top_five'],'nodes':node_tests},indent=2))
