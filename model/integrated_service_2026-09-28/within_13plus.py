"""Existing-cohort composition check; monotone probability bounds, no fitting."""
import csv,json,hashlib,math
import engine as m
import vintage_body_integration as v

def main():
 d,e,c=m.load()
 with v.BIRTHS.open() as f: births={(int(r['year']),r['body']):float(r['births_thousands']) for r in csv.DictReader(f)}
 _,raw=m.stock(d,[0,0,1,0,0]);cw={(b,k):e['relative_claim_weights'][k]*e['body_weights'][str(k)][b] for b in range(4) for k in range(6)}
 norm=sum(cw.values());correction={key:w/norm/raw[key] for key,w in cw.items()}
 eco=m.economics(d,e,c,1,1);details=[];summaries=[];checks=[];segments=[]
 for name,data in [('fixed_body_split',d),('vintage_body_split',v.adapt(d,births))]:
  for mode in ['fleet','raw_claim_proxy','calibrated_claim_proxy']:
   states=[]
   for year,j in [(2024,1),(2025,2)]:
    mass={}
    for r in data['fleet']:
     if r['age']<13:continue
     b=r['body'];a=r['age'];w=r['births'][j]*data['split'][b]*r['survival']
     if mode!='fleet':w*=r['relative_claim_weight']
     if mode=='calibrated_claim_proxy':w*=correction[b,5]
     mass[b,a]=w
    z=sum(mass.values());dist={key:w/z for key,w in mass.items()};states.append(dist)
    assert m.close(sum(dist.values()),1);checks.append(name+mode+str(year)+' normalization')
    for (b,a),w in dist.items():details.append(dict(case=name,weighting=mode,year=year,body=v.BODY[b],age=a,birth_year=year-a,raw_mass=mass[b,a],share_within_13plus=w))
    for lo,hi in [(13,15),(16,19),(20,24),(25,45)]:segments.append(dict(case=name,weighting=mode,year=year,age_segment=f'{lo}-{hi}',share=sum(w for (b,a),w in dist.items() if lo<=a<=hi)))
   old,new=states;ages=range(13,46)
   a0={a:sum(old[b,a] for b in range(4)) for a in ages};a1={a:sum(new[b,a] for b in range(4)) for a in ages}
   tails={t:sum(a1[a]-a0[a] for a in ages if a>=t) for t in ages}
   # Any fixed nondecreasing P(a) in [0,1] is a mixture of threshold steps plus constant.
   upper=max(0,max(tails.values()));lower=min(0,min(tails.values()))
   threshold=max(tails,key=tails.get)
   mean0=sum(a*w for a,w in a0.items());mean1=sum(a*w for a,w in a1.items())
   legacy=lambda a:.048+(.480-.048)/(1+math.exp(-(a-9.22)/3.73))
   smooth=sum((a1[a]-a0[a])*legacy(a) for a in ages)
   assert lower-1e-12<=smooth<=upper+1e-12;checks.append(name+mode+' smooth curve within monotone bound')
   # Also allow a different monotone curve for each body, with joint shares changing.
   jointbound=sum(max(0,max(sum(new[b,a]-old[b,a] for a in ages if a>=t) for t in ages)) for b in range(4))
   bodyonly=sum((new[b,a]-old[b,a])*eco[b,5]['probability'] for b,a in old)
   # Current production model has fixed TLF across ages within each body/13+ cell.
   row=dict(case=name,weighting=mode,mean_age_2024=mean0,mean_age_2025=mean1,mean_age_change=mean1-mean0,age13_share_2024=a0[13],age13_share_2025=a1[13],common_monotone_upper_pp=100*upper,common_monotone_lower_pp=100*lower,upper_step_age=threshold,body_specific_monotone_upper_pp=100*jointbound,legacy_smooth_curve_mix_pp=100*smooth,frozen_body_cell_TLF_change_pp=100*bodyonly,unrestricted_common_curve_upper_pp=100*sum(max(0,a1[a]-a0[a]) for a in ages))
   summaries.append(row)
   # Threshold attains common upper; constant curve has zero composition effect.
   assert m.close(sum((a1[a]-a0[a])*(a>=threshold) for a in ages),upper)
   assert m.close(sum(a1[a]-a0[a] for a in ages),0);checks.append(name+mode+' bound and constant checks')
 m.save_csv('within_13plus_single_age.csv',details);m.save_csv('within_13plus_segments.csv',segments);m.save_csv('within_13plus_comparison.csv',summaries)
 paths=[m.OLD,m.ECON,v.BIRTHS,m.HERE/'within_13plus.py',m.ROOT/'docs/AGE_CURVES.md',m.ROOT/'raw/ccc/crash-course-2026.txt']
 out=dict(status='Modeled composition only, not observed claims microdata; production unchanged',comparison='CY2024 to CY2025 annual snapshots',observed_13plus_TLF_change_pp=1.7,results=summaries,checks_passed=len(checks),checks=checks,source_hashes={str(p.relative_to(m.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
 (m.HERE/'within_13plus_results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'results':summaries,'checks_passed':len(checks)},indent=2))
if __name__=='__main__':main()
