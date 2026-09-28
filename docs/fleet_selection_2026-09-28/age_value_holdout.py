"""Fixed-parameter age value holdout; no refit to the new chart."""
import contextlib,hashlib,io,json,runpy,shutil
from pathlib import Path
P=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()):e=runpy.run_path(str(P/'joint_calibration.py'))
candidate=json.loads((P/'assumption_diagnosis_results.json').read_text())['three_target_solutions'][0]
observed=[40187,30259,20328,9122];mix=[.021,.107,.149,.723]
models=[('original_curve_refitted_TLF',e['d']['sigma'],.1,1.),('flatter_curve_candidate',candidate['sigma'],candidate['slope'],candidate['scale'])]
rows=[]
for name,sigma,slope,scale in models:
    r=e['fit'](sigma,e['inferred'],slope,.3)
    vals=[v*scale for v in r['selected_total_loss_ACV_by_age_at_original_scale']]
    older=sum(e['shares'][e['d']['calibration'][k]['age_bucket']]*vals[k] for k in range(3,6))/sum(e['shares'][e['d']['calibration'][k]['age_bucket']] for k in range(3,6))
    v=vals[:3]+[older]
    rows.append({'name':name,'fixed_sigma':sigma,'fixed_slope':slope,'fixed_scale':scale,'selected_values':v,
                 'difference_pct':[100*(a/b-1) for a,b in zip(v,observed)],
                 'mean_using_observed_four_group_mix':sum(a*b for a,b in zip(v,mix)),
                 'young_to_old_value_ratio':v[0]/v[3]})
source=Path('/tmp/cprt_age_values.webp');target=P/'ccc_2025q4_age_values.webp'
if source.exists():shutil.copyfile(source,target)
out={'status':'Held-out age dollars, parameters fixed. Period/coverage mismatches remain; not formal statistical validation.',
 'source':{'report':'https://www.cccis.com/reports/crash-course-2025/q4','figure':6,'population':'National non-comprehensive total-loss valuations','period':'YTD through October 2025',
 'method':'Visually read printed 2025 dollar labels and mix from one image; no OCR.',
 'image_url':'https://cdn.prod.website-files.com/677e7ecbb3dbbe98615cde30/6930b1fd32ab4cfa6443fc96_Total%20Loss%20Values%20%26%20Mix%E2%80%8B.webp','image_sha256':hashlib.sha256(target.read_bytes()).hexdigest()},
 'observed_age_labels':['current_year','1-3','4-6','7_plus'],'observed_values':observed,'observed_mix':mix,
 'observed_all_age_value':13700,'weighted_observed_value_from_rounded_labels':sum(a*b for a,b in zip(observed,mix)),
 'observed_young_to_old_ratio':observed[0]/observed[3], 'models':rows,
 'limitations':['Model CY2025 all-loss TLF and valuation-age weights versus noncomp YTD October benchmark.', 'Older within-group 7-9/10-12/13+ shares remain all-loss; observed chart only supplies 7+.', 'Current-year-or-newer model bucket versus current-year chart label.', 'Model body weights and representative ages remain assumptions.', 'Candidate was calibrated to related CCC annual aggregate, so held-out age detail is not an independent data provider.']}
(P/'age_value_holdout_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
