"""Run the curated revenue package without network or licensed raw materials."""
import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys

parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path);args=parser.parse_args()
root=args.root or Path(__file__).resolve().parent
if not (root/'model').exists():root=root.parents[1]
steps=[['model/revenue_architecture_2026-09-28/test_model.py'],
       ['model/revenue_architecture_2026-09-28/run.py','--reuse-saved-evidence'],
       ['model/aftermarket_bridge_2026-09-29/bridge.py'],
       ['model/aftermarket_bridge_2026-09-29/test_bridge.py'],
       ['model/ccc_age_body_2026-09-29/integrate.py']]
for step in steps:
    r=subprocess.run([sys.executable,*step],cwd=root,capture_output=True,text=True)
    if r.returncode:
        print(r.stdout[-2000:]);print(r.stderr[-2000:]);raise SystemExit(r.returncode)
    print('Passed:',step[0],flush=True)
def get(path,name):
    with (root/path).open() as f:return next(x for x in csv.DictReader(f) if x['scenario']==name)
ref=get('model/revenue_architecture_2026-09-28/scenario_summary.csv','price_3p7_intl_continuation')
large=get('model/aftermarket_bridge_2026-09-29/scenario_summary.csv','larger_shift')
assert abs(float(ref['FY_legacy_service_musd'])-4105.804039246686)<1e-6
assert abs(float(large['FY_legacy_service_musd'])-4015.1481728478084)<1e-6
assert abs(float(large['FY_delta_vs_reference_musd'])+90.65586639887806)<1e-6
print(json.dumps({'status':'pass','reference_service_musd':float(ref['FY_legacy_service_musd']),
                  'larger_case_service_musd':float(large['FY_legacy_service_musd']),
                  'scope':'Snapshot reproduction only; no fresh empirical validation'}))
