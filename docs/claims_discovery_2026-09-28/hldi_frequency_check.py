"""Three approximate visual readings, not precise digitized source observations."""
import json,math,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
source=ROOT/'raw/hldi/hldi_39_07_2022.pdf';inp=ROOT/'model/linked_service_revenue_2026-09-28/inputs.json'
d=json.loads(inp.read_text());r={x['age']:x['relative_claim_weight'] for x in d['fleet'] if x['body']==0}
readings={13:(3.6,3.45,3.75),20:(2.15,2.0,2.3),25:(1.5,1.35,1.65)}
rows=[]
for a,(point,lo,hi) in readings.items():
 ratio=point/readings[13][0];model=r[a]/r[13]
 bounds=[lo/readings[13][2],hi/readings[13][1]] if a!=13 else [1,1]
 residual=model/ratio
 row={'age':a,'approx_claims_per_100_insured_vehicle_years':point,'visual_reading_interval':[lo,hi],'frequency_relative_to_age13':ratio,'frequency_ratio_interval':bounds,'model_claim_propensity_relative_to_age13':model,'hypothetical_residual_factor':residual,'residual_interval':[model/bounds[1],model/bounds[0]],'status':'Illustrative comparability test; residual is NOT an observed coverage ratio'}
 assert bounds[0]<=ratio<=bounds[1]
 assert math.isclose(residual*ratio,model)
 rows.append(row)
out={'source_url':'https://platform.vox.com/wp-content/uploads/sites/2/chorus/uploads/chorus_asset/file/24341429/39_07.pdf','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'model_input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),'source_locator':'HLDI April 2022 Bulletin 39(7), printed p4 Figure5, all-vehicles black curve, CY2020','method':'Visual reading of rendered chart at ages13,20,25; ±0.15 claims per100 selected as reading allowance, not a statistical confidence interval. No interpolation or forecast adoption. Normalize at13 to avoid age0 half-year convention.','rows':rows,'checks_passed':6,'identification':'R(age)/R(13) divided by F_insured(age)/F_insured(13). Could represent relative collision coverage ONLY with compatible year, population, damage/coverage scope and exposure definitions; current model and HLDI are not matched.'}
(P/'hldi_frequency_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(rows,indent=2))
