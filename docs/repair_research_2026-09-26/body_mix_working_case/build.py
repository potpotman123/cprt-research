from pathlib import Path
import csv,json,math,ast,subprocess,hashlib
p=Path(__file__).parent;base=p.parent;repo=Path('/Users/kwu/cprt')
impact=list(csv.DictReader((base/'repair_frequency_feasibility/cohort_table.csv').open()))
weights={r['body']:{'front':float(r['front_share']),'rear':float(r['rear_share']),'other':1-float(r['front_share'])-float(r['rear_share'])} for r in impact if r['age']=='7-9'}
aaa=json.loads((base/'repair_pilot/aaa_scenario_results.json').read_text())['rows'];front=aaa[0];rear=aaa[2]
ratios={'Car':dict(front=1,rear=1,other=1),'SUV':dict(front=front['rogue']/front['camry'],rear=rear['rogue']/rear['camry'],other=1.10),'Pickup':dict(front=front['f150']/front['camry'],rear=rear['f150']/rear['camry'],other=1.15)}
ratios['Minivan']=ratios['SUV'].copy()
relative_car_cost={'front':1,'rear':.60,'other':.80}
car_mean=3682 # derived CCC2025 7+ all-loss mean, assigned to car cohort as a WORKING ASSUMPTION
scale=car_mean/sum(weights['Car'][k]*relative_car_cost[k] for k in relative_car_cost)
car_cost={k:v*scale for k,v in relative_car_cost.items()}
rows=[];costs={};fixedmix={}
for b in ratios:
 costs[b]=sum(weights[b][k]*car_cost[k]*ratios[b][k] for k in car_cost)
 fixedmix[b]=sum(weights['Car'][k]*car_cost[k]*ratios[b][k] for k in car_cost)
 for k in car_cost:rows.append({'body':b,'impact':k,'impact_share_assumed_transfer_from_CRSS':weights[b][k],'car_scope_mean_usd_assumed':car_cost[k],'relative_repair_cost':ratios[b][k],'body_scope_mean_usd':car_cost[k]*ratios[b][k],'weighted_contribution_usd':weights[b][k]*car_cost[k]*ratios[b][k]})
# Listed pool composition is deliberately used as a fixed proxy, not claimed exposure weighting.
lt_raw={'SUV':.409,'Pickup':.109,'Minivan':.047};ltw={k:v/sum(lt_raw.values()) for k,v in lt_raw.items()}
ltcost=sum(ltw[b]*costs[b] for b in ltw);repair=ltcost/car_mean
ref='origin/claude/jolly-edison-4f0gk9';commit=subprocess.check_output(['git','rev-parse',ref],cwd=repo,text=True).strip()
source=subprocess.check_output(['git','show',f'{commit}:scripts/experiments/e1_body_propensity.py'],cwd=repo,text=True)
(p/'prior_model_source.py.txt').write_text(source)
ns={'__file__':str(repo/'scripts/experiments/e1_body_propensity.py')}
# Freeze inherited compact inputs before loading the prior model.
inputs=p/'inherited_inputs';inputs.mkdir(exist_ok=True)
import shutil
for name in ['ornl_tedb40_survival_by_age.csv','light_vehicle_sales_by_year.csv','age_curves.csv','ccc_tl_share_by_age_2020_2025.csv']:
 if not (inputs/name).exists():shutil.copy2(repo/'data/csv'/name,inputs/name)
prefix=source.split('print("1. σ_eff')[0].replace("D = ROOT / 'data/csv'", 'D = pathlib.Path('+repr(str(inputs.resolve()))+')')
exec(compile(prefix,'<prior setup>','exec'),ns)
funcs=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in ('split','roll')]
exec(compile(ast.Module(body=funcs,type_ignores=[]),'<prior functions>','exec'),ns)
ages=ns['bucket_mean_age'](2024);_,gamma,_=ns['ols']([ages[b] for b,_,_ in ns['BUCK']],[ns['Phi_inv'](ns['CCC'][b]['cy2024']) for b,_,_ in ns['BUCK']]);sig=.11/gamma
baseline=ns['roll'](1,{a:(ns['Pf'](a),ns['Pf'](a),0) for a in ns['AGES']})
def run(r):
 curves=ns['split'](2024,1,math.log(1.5/r)/sig);roll=ns['roll'](1,curves);a,b=roll[2026],roll[2027]
 u=((b[0]-a[0])-(baseline[2027][0]-baseline[2026][0]))/a[0]
 asp=.5*(b[2]-a[2])/(1+.5*a[2]);rpu=.514*asp;rev=(1+u)*(1+rpu)-1
 return {'repair_ratio':r,'unit_growth_contribution_pp':100*u,'asp_mix_contribution_pct':100*asp,'rpu_growth_contribution_pp':100*rpu,'revenue_growth_contribution_pp':100*rev,'revenue_change_per_1bn_exposed_service_usd':1e9*rev,'lt_share_total_losses_2026':a[2],'lt_share_total_losses_2027':b[2],'tlf_2026':a[0],'tlf_2027':b[0]}
new=run(repair);old=run(1.01)
assert abs(run(1.5)['unit_growth_contribution_pp'])<1e-8
assert all(abs(sum(w.values())-1)<1e-12 for w in weights.values())
assert abs(costs['Car']-car_mean)<1e-8 and abs(sum(ltw.values())-1)<1e-12
out={'status':'ASSUMPTION-DRIVEN WORKING BASE, NOT OBSERVED CAUSAL PREMIUM','body_average_cost_usd':costs,'body_repair_premium_pct':{b:100*(c/car_mean-1) for b,c in costs.items()},'same_impact_mix_premium_pct':{b:100*(c/car_mean-1) for b,c in fixedmix.items()},'light_truck_weights':ltw,'light_truck_cost_usd':ltcost,'light_truck_repair_premium_pct':100*(repair-1),'new_2027_bridge':new,'old_2027_bridge':old,'inherited_sigma':sig,'prior_model_commit':commit,'assumptions':{'other_impact_SUV_premium':.10,'other_impact_pickup_premium':.15,'minivan_cost_ratio_proxy':'SUV','car_rear_to_front_cost':.60,'car_other_to_front_cost':.80,'AAA_new_to_old_relative_cost_transfer':1,'threshold_and_auction_price_ratio':1.5,'relative_claim_frequency':1,'fee_elasticity':.514,'cohort_transfer':'7-9 age ratios held constant across model ages','van_proxy':'listed vans bucket treated as minivans for repair weighting','claims_exposure_proxy':'current listed-body shares fixed within LT, despite disposal selection'},'checks':'shares sum, car mean reconciliation, equal cost/threshold eliminates modeled unit difference'}
(p/'results.json').write_text(json.dumps(out,indent=2))
with (p/'repair_cost_build.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Apply the chosen front mean to one historical histogram, retaining shape as the user's reference convention.
h=list(csv.DictReader((base/'repair_cost_reference/historical_bins.csv').open()));h=[r for r in h if r['reference']=='sedan_1_no_adas'];mean=sum(float(r['normalized_share'])*float(r['midpoint_assumption_usd']) for r in h)
hr=[]
for b in ratios:
 factor=car_cost['front']*ratios[b]['front']/mean
 for r in h:hr.append({'body':b,'share':r['normalized_share'],'front_cost_midpoint_usd':float(r['midpoint_assumption_usd'])*factor,'status':'assumed historical shape; repairable reference, not latent all-crash cost distribution'})
with (p/'front_reference_distribution.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(hr[0]));w.writeheader();w.writerows(hr)
# Snapshot compact inherited data for reproduction; no changes to repository model/workbook.
inputs=p/'inherited_inputs';inputs.mkdir(exist_ok=True)
import shutil
# Snapshot already loaded above; do not overwrite it on later runs.
print(json.dumps(out,indent=2))
