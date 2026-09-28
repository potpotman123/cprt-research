"""Out-of-calibration value diagnostic; coverage mismatch explicit."""
import hashlib,json,shutil
from pathlib import Path
P=Path(__file__).parent
source=P/'joint_calibration_results.json';d=json.loads(source.read_text())
image=Path('/tmp/cprt_ccc_figure22.webp')
saved=P/'ccc_2026_figure22.webp'
if image.exists():shutil.copyfile(image,saved)
rows=[]
for name,j in d['joint_fits_not_adopted'].items():
    value=j['selected_total_loss_ACV_at_original_scale']*j['common_scale']
    anchored=13610/j['selected_total_loss_ACV_at_original_scale']
    original=min(d['cases'][name],key=lambda r:abs(r['sigma']-1.5702059479932844))
    rows.append({'weights':name,'original_dispersion_selected_value':original['selected_total_loss_ACV_at_original_scale'],
                 'joint_fit_selected_value':value,'difference_vs_noncomp_benchmark_pct':100*(value/13610-1),
                 'ACV_anchored_scale_at_joint_fit_dispersion':anchored,
                 'ACV_anchored_repairable_means':[g['model_repairable_mean_at_original_value_scale']*anchored for g in j['group_results']],
                 'warning':'Anchored outputs hold joint-fit dispersion fixed, not a new constrained optimum. Benchmark noncomp versus model all-loss age calibration.'})
out={'benchmark':{'value':13610,'period':'CY2025 through December','scope':'CCC national non-comprehensive total-loss vehicle valuations; average adjusted vehicle value',
 'report':'https://www.cccis.com/reports/crash-course-2026','figure':22,
 'image_url':'https://cdn.prod.website-files.com/677e7ecbb3dbbe98615cde30/69cada2ee6e49394a5609441_Picture22-p-1600.webp',
 'method':'Single image visually inspected; no OCR. Report HTML fetched earlier in repository; live report returned 403; CDN image succeeded.',
 'image_sha256':hashlib.sha256(saved.read_bytes()).hexdigest()},
 'calibration_results_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'rows':rows,
 'conclusion':'Joint fits do not pass this provisional value cross-check. Not an exact matched-population rejection. No forecast change.'}
(P/'selected_value_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(rows,indent=2))
