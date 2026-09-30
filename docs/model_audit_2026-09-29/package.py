"""Curated handoff: avoid raw/licensed files and competing historical models."""
import hashlib
import json
from pathlib import Path
import zipfile

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
files={}
for folder in ['model/revenue_architecture_2026-09-28','model/aftermarket_bridge_2026-09-29',
               'docs/aftermarket_transition_evidence_2026-09-29',
               'docs/aftermarket_parameter_audit_2026-09-29',
               'docs/bidmate_adoption_2026-09-29',
               'docs/catalyst_assessment_2026-09-29',
               'docs/pitch_audit_2026-09-29',
               'model/ccc_age_body_2026-09-29']:
    for p in (ROOT/folder).iterdir():
        if p.is_file() and p.suffix in ['.py','.json','.csv','.md']:files[str(p.relative_to(ROOT))]=p.read_bytes()
for name in [
    'RESEARCH_STATE.md',
    'model/integrated_service_2026-09-28/engine.py',
    'model/integrated_service_2026-09-28/assumptions.json',
    'model/integrated_service_2026-09-28/connected_quarterly_bridge.csv',
    'model/integrated_service_2026-09-28/reconciled_quarterly_service.csv',
    'model/integrated_service_2026-09-28/historical_operating_bridge.csv',
    'model/linked_service_revenue_2026-09-28/inputs.json',
    'docs/fleet_selection_2026-09-28/age_constrained_engine_results.json',
    'docs/fleet_selection_2026-09-28/AGE_CONSTRAINED_ENGINE.md',
    'docs/fleet_selection_2026-09-28/age_value_holdout_results.json',
    'docs/historical_body_births_2026-09-28/candidate_body_births.csv',
    'docs/historical_body_births_2026-09-28/README.md',
    'docs/consensus_review_2026-09-28/total_revenue_consensus.csv',
    'docs/repair_salvage_execution_2026-09-28/MIX_SEGMENTATION.md',
    'data/csv/copart_fee_grid_2026-09.csv',
    'data/csv/ccc_tl_share_by_age_2020_2025.csv',
    'docs/model_audit_2026-09-29/AUDIT.md',
    'docs/model_audit_2026-09-29/FABLE_HANDOFF.md',
    'docs/model_audit_2026-09-29/audit_checks.py',
    'docs/model_audit_2026-09-29/audit_checks.json',
    'docs/model_audit_2026-09-29/financial_controls_checked.csv',
    'docs/model_audit_2026-09-29/source_hashes.json',
    'docs/model_audit_2026-09-29/before_hashes.json']:
    files[name]=(ROOT/name).read_bytes()
files['REPRODUCE.py']=(HERE/'REPRODUCE.py').read_bytes()
files['START_HERE.md']=b'''# Copart revenue model: audited scenario handoff

Start with RESEARCH_STATE.md, docs/pitch_audit_2026-09-29/README.md,
then docs/model_audit_2026-09-29/FABLE_HANDOFF.md and AUDIT.md.
Publication refreshed 30 September: no established measurable forecast error
linked to an observable near-term catalyst. Reporting windows are not catalysts
without an identifiable surprise. Preserve this concern in the pitch.
Architecture and arithmetic checked; causal forecast evidence remains incomplete.
Scope is legacy service revenue, with separately identified purchased/acquisition overlays.
This package is for an editable scenario workbook, not an approved investment forecast.

Run python3 REPRODUCE.py from this directory. Python 3.9+; standard library only.
Uses saved dated evidence; raw licensed reports and private workbooks are excluded.
Do not run predecessor model mains or treat archived fixture outputs as forecasts.
FILE_MANIFEST.json lists all packaged files and hashes, excluding itself.
'''
manifest={'as_of':'2026-09-30','status':'Conditional revenue scenario model; empirical and catalyst gaps remain',
          'files':{k:hashlib.sha256(v).hexdigest() for k,v in sorted(files.items())}}
files['FILE_MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
dest=HERE/'CPRT_revenue_Fable_handoff_2026-09-29.zip'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for name,data in sorted(files.items()):
        info=zipfile.ZipInfo('cprt_revenue_model/'+name,date_time=(2026,9,29,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
(HERE/'package_manifest.json').write_text(json.dumps(dict(filename=dest.name,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),files=len(files),bytes=dest.stat().st_size,raw_licensed_files_included=False),indent=2)+'\n')
print(json.dumps({'file':str(dest),'files':len(files),'bytes':dest.stat().st_size}))
