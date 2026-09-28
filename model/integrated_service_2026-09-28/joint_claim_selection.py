"""Small retrospective identification screen; no production forecast edits."""
import csv, hashlib, json, math
import engine as m

def main():
 d,e,c=m.load(); N=m.N
 path=m.ROOT/'data/csv/ccc_tl_share_by_age_2020_2025.csv'
 with path.open() as f: rates={r['age_bucket']:r for r in csv.DictReader(x for x in f if not x.startswith('#'))}
 weights={(b,k):e['relative_claim_weights'][k]*e['body_weights'][str(k)][b] for k in range(3,6) for b in range(4)}
 z=sum(weights.values());weights={key:w/z for key,w in weights.items()}
 cells=[];rebases=[];checks=[]
 # Conditional 2024 reference: preserve shapes/values/body weights, reset age TLF only.
 for k in range(3,6):
  row=e['cohorts'][k];target=float(rates[row['age_bucket']]['cy2024'])/100
  def ageprob(shift):
   return sum(e['body_weights'][str(k)][b]*(1-m.cutoff(row['log_car_repair_median']+math.log(e['repair_ratios'][b])+shift,row['car_ACV']*e['value_ratios'][b],row['sigma'],c['seller_fee_fraction'])) for b in range(4))
  lo,hi=-1.,1.
  for _ in range(48):
   mid=(lo+hi)/2
   if ageprob(mid)<target:lo=mid
   else:hi=mid
  shift=(lo+hi)/2
  assert abs(ageprob(shift)-target)<1e-9
  checks.append('2024 age TLF anchor '+row['age_bucket'])
  rebases.append(dict(age_bucket=row['age_bucket'],log_repair_shift=shift,target_TLF=target))
  for b in range(4):cells.append(dict(k=k,b=b,w=weights[b,k],mu=row['log_car_repair_median']+math.log(e['repair_ratios'][b])+shift,acv=row['car_ACV']*e['value_ratios'][b],sigma=row['sigma']))
 def economics(r,v):
  out=[]
  for x in cells:
   mu=x['mu']+math.log(r);acv=x['acv']*v;s=x['sigma'];u=m.cutoff(mu,acv,s,c['seller_fee_fraction'])
   out.append(dict(**x,u=u,mean_factor=math.exp(mu+s*s/2),value=acv))
  return out
 def evaluate(eco,f):
  tl=rep=cost=val=0.;ages={k:[0.,0.] for k in range(3,6)}
  for x in eco:
   u=x['u'];assert f<u # remove only low-rank repairable incidents
   w=x['w'];p=1-u
   tl+=w*p;rep+=w*(u-f);val+=w*p*x['value']
   cost+=w*x['mean_factor']*(N.cdf(N.inv_cdf(u)-x['sigma'])-(N.cdf(N.inv_cdf(f)-x['sigma']) if f else 0))
   ages[x['k']][0]+=w*p;ages[x['k']][1]+=w*(1-f)
  return dict(TLF=tl/(tl+rep),totals=tl,repairables=rep,claims=tl+rep,repair_mean=cost/rep,selected_ACV=val/tl,age_TLF={k:a/b for k,(a,b) in ages.items()})
 baseeco=economics(1,1);base=evaluate(baseeco,0)
 targets={k:float(rates[e['cohorts'][k]['age_bucket']]['cy2025'])/100 for k in range(3,6)}
 rows=[];cache={}
 # Analyst-chosen diagnostic range, NOT empirical confidence bounds.
 for ri in range(-4,13):
  r=1+ri*.005
  for vi in range(-6,7):
   v=1+vi*.005;eco=economics(r,v);cache[ri,vi]=eco
   for fi in range(13):
    f=fi*.005;a=evaluate(eco,f)
    errors=[100*(a['age_TLF'][k]-targets[k]) for k in range(3,6)]
    repair=100*(a['repair_mean']/base['repair_mean']-1);value=100*(a['selected_ACV']/base['selected_ACV']-1)
    score=sum((x/.25)**2 for x in errors)+((repair-1)/.5)**2+((value+.5)/.5)**2
    rows.append(dict(ri=ri,vi=vi,fi=fi,repair_input_pct=100*(r-1),value_input_pct=100*(v-1),low_rank_removed_pct=100*f,TLF_7_9_residual_pp=errors[0],TLF_10_12_residual_pp=errors[1],TLF_13plus_residual_pp=errors[2],repair_mean_growth_pct=repair,selected_ACV_growth_pct=value,total_loss_growth_pct=100*(a['totals']/base['totals']-1),repairable_count_growth_pct=100*(a['repairables']/base['repairables']-1),reported_claim_growth_pct=100*(a['claims']/base['claims']-1),score=score,inside_screen=all(abs(x)<=.25 for x in errors) and abs(repair-1)<=.5 and abs(value+.5)<=.5))
 families={'economics_only':[x for x in rows if x['fi']==0],'filing_only':[x for x in rows if x['ri']==0 and x['vi']==0],'combined':rows}
 selected=[];grids=m.fee_grids(d)
 def fees(eco):
  units=rev=proceeds=0
  for x in eco:
   p=1-x['u'];buyer=0.;nodes=c['fee_integration_nodes']
   for j in range(nodes):
    rank=x['u']+p*(j+.5)/nodes;price=x['value']*(.4-.2*rank)
    buyer+=((1-c['preferred_buyer_fraction'])*m.fee(price,grids[0])+c['preferred_buyer_fraction']*m.fee(price,grids[1])+m.fee(price,grids[2])+c['gate_environment_fee'])/nodes
   asp=x['value']*(.3-.1*x['u']);units+=x['w']*p;rev+=x['w']*p*(buyer+c['seller_fee_fraction']*asp);proceeds+=x['w']*p*asp
  return dict(units=units,RPU=rev/units,revenue=rev,ASP=proceeds/units)
 basefee=fees(baseeco)
 for family,rr in families.items():
  best=min(rr,key=lambda x:x['score']);ff=fees(cache[best['ri'],best['vi']]);out=dict(family=family,**best,cases=len(rr),passing_cases=sum(x['inside_screen'] for x in rr))
  for key in ['RPU','revenue','ASP']:out[key+'_growth_pct']=100*(ff[key]/basefee[key]-1)
  assert m.close(ff['units']/basefee['units']*ff['RPU']/basefee['RPU'],ff['revenue']/basefee['revenue']);checks.append(family+' revenue identity')
  selected.append(out)
 # A filing filter changes reported denominator, not totals or selected total values.
 filtered=evaluate(baseeco,.03)
 assert m.close(filtered['totals'],base['totals']) and m.close(filtered['selected_ACV'],base['selected_ACV']);checks.append('filing preserves totals and selected ACV')
 assert filtered['repair_mean']>base['repair_mean'] and filtered['TLF']>base['TLF'];checks.append('minor removal raises both conditional means')
 scaled=evaluate(economics(1.02,1.02),0)
 assert m.close(scaled['totals'],base['totals']);checks.append('equal cost/value scale preserves totals')
 for rr in rows:
  assert m.close((1+rr['total_loss_growth_pct']/100)*base['totals']+(1+rr['repairable_count_growth_pct']/100)*base['repairables'],1+rr['reported_claim_growth_pct']/100)
 checks.append('all grid count identities')
 m.save_csv('joint_claim_selection_grid.csv',rows);m.save_csv('joint_claim_selection_comparison.csv',selected)
 sources=[path,m.ECON,m.OLD,m.HERE/'assumptions.json',m.ROOT/'raw/ccc/crash-course-2026.txt',m.ROOT/'docs/fleet_selection_2026-09-28/ccc_2026_figure22.webp',m.HERE/'joint_claim_selection.py']
 robustness={}
 for tol in [.25,.5]:
  accepted=[x for x in rows if max(abs(x[key]) for key in ['TLF_7_9_residual_pp','TLF_10_12_residual_pp','TLF_13plus_residual_pp'])<=tol and abs(x['repair_mean_growth_pct']-1)<=.5 and abs(x['selected_ACV_growth_pct']+.5)<=.5]
  robustness[str(tol)]={'accepted_count':len(accepted),'note':'Analyst tolerance, not a confidence interval','unit_growth_range_pct':[min(x['total_loss_growth_pct'] for x in accepted),max(x['total_loss_growth_pct'] for x in accepted)] if accepted else None}
 out=dict(tolerance_robustness=robustness,status='Retrospective diagnostic, mismatched populations; no forecast adoption',grid_count=len(rows),baseline=base,rebases=rebases,selected=selected,checks=checks,checks_passed=len(checks),sources={str(p.relative_to(m.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
 (m.HERE/'joint_claim_selection_results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
