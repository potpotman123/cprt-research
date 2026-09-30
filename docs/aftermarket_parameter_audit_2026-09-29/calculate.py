import json,sys,csv,copy
from pathlib import Path
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'model/aftermarket_bridge_2026-09-29'));import bridge as b
p=json.loads((root/'model/ccc_age_body_2026-09-29/aftermarket_inputs.json').read_text())
rows=[];detail={}
for name,changes,o,r in [('half_eligible_bill_exposure',{'eligible_parts_bill_share':.2},.04,.015),('zero_exposed_donor_contribution',{'donor_contribution_exposed_fraction':0},.04,.015),('oem_displacement_only',{},.04,0)]:
 q=dict(p,**changes);s=b.solve(q,o,r);out=b.summarize(name,q,s,b.forecast_result(q,s));rows.append(out);detail[name]={'parameter_changes':changes,'oem_to_aftermarket':o,'recycled_to_aftermarket':r,'solution':s};print(name,out['FY_delta_vs_reference_musd'],flush=True)
dest=root/'docs/aftermarket_parameter_audit_2026-09-29'
with (dest/'diagnostic_sensitivities.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
(dest/'diagnostic_sensitivities.json').write_text(json.dumps({'status':'Hypothetical diagnostics, not new calibrated parameters','reference':'CCC-based FY27 legacy service case','cases':detail},indent=2)+'\n')
