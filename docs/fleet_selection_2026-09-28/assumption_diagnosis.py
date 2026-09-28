"""Competing one-structural-change fits; diagnostic, not causal identification."""
import contextlib,io,json,runpy
from pathlib import Path
P=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()): env=runpy.run_path(str(P/'joint_calibration.py'))
fit=env['fit'];w=env['inferred']
def evaluate(slope,center):
    def gap(s):
        r=fit(s,w,slope,center)
        a,b=[g['required_common_ACV_and_repair_scale'] for g in r['group_results']]
        return a-b,r
    lo,hi=.35,3.
    gl,_=gap(lo);gh,_=gap(hi)
    if gl*gh>0:return {'slope':slope,'recovery_center':center,'status':'No equal-scale root in tested sigma interval [.35,3]'}
    for _ in range(24):
        mid=(lo+hi)/2;gm,r=gap(mid)
        if gm*gl>0:lo=mid;gl=gm
        else:hi=mid
    scale=sum(g['required_common_ACV_and_repair_scale'] for g in r['group_results'])/2
    value=r['selected_total_loss_ACV_at_original_scale']*scale
    return {'slope':slope,'recovery_center':center,'sigma':mid,'scale':scale,'selected_ACV':value,'value_gap_pct':100*(value/13610-1),'repair_shock_units_pct':r['responses_at_original_scale']['repair_plus_5pct']['units_pct'],'status':'Both repair means and age TLF fitted'}
rows=[evaluate(s,.3) for s in [.04,.06,.08,.1,.12,.14]]+[evaluate(.1,c) for c in [.1,.2,.4,.5]]
roots=[]
for kind,lo,hi in [('slope',.08,.1),('recovery',.1,.3)]:
    def ev(x):return evaluate(x,.3) if kind=='slope' else evaluate(.1,x)
    l,h=ev(lo),ev(hi)
    if 'value_gap_pct' not in l or 'value_gap_pct' not in h or l['value_gap_pct']*h['value_gap_pct']>0:continue
    for _ in range(20):
        mid=(lo+hi)/2;r=ev(mid)
        if r['value_gap_pct']*l['value_gap_pct']>0:lo=mid;l=r
        else:hi=mid
    roots.append({'changed_structural_assumption':kind,**r})
out={'status':'Conditional on CCC inferred age weights and unmatched noncomp value anchor. No fit adopted. Grid points not empirical ranges.','grid':rows,'three_target_solutions':roots}
(P/'assumption_diagnosis_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
