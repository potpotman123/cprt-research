"""Calibrate 16 scalar level offsets, preserving inherited response shapes.

New CCC data calibrate frequencies and claim weights, not damage elasticities.
The broad 7+ bucket retains the prior within-group age composition as a proxy.
"""
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'model/aftermarket_bridge_2026-09-29'))
import bridge
m=bridge.m
ANCHOR=str((HERE/'cohort_anchor.json').relative_to(ROOT))

def write_csv(name, rows):
    with (HERE/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)

def econ(b,k,mult,nodes=1):
    return m.cell_economics(b,k,mult,1.,1.,1.,.5,.04,0.,110.,1.,'sep2026_snapshot',nodes)

def main():
    with (HERE/'source_cells.csv').open() as f:source=list(csv.DictReader(f))
    latest=[r for r in source if int(r['year'])==2025]
    d,e,inherited=m.old.load()
    prior={(b,k):e['relative_claim_weights'][k]*e['body_weights'][str(k)][b] for b in range(4) for k in range(6)}
    cells=[]; fits=[]
    for r in latest:
        b=int(r['model_body']);a=int(r['age_group']);ks=[a] if a<3 else [3,4,5]
        target=float(r['tlf']);group_weight=float(r['derived_claim_weight'])
        splits={k:prior[b,k]/sum(prior[b,j] for j in ks) for k in ks}
        def prob(log_mult):return sum(splits[k]*econ(b,k,math.exp(log_mult))['TLF'] for k in ks)
        lo,hi=-4.,4.
        assert prob(lo)<target<prob(hi)
        # One level per observed age/body cell. No fitting of dispersion or elasticity.
        for _ in range(42):
            mid=(lo+hi)/2
            if prob(mid)<target:lo=mid
            else:hi=mid
        mult=math.exp((lo+hi)/2)
        fits.append(dict(source_body=r['source_body'],age_group=a,observed_tlf=target,
            previous_shape_tlf=prob(0),calibrated_tlf=prob(math.log(mult)),repair_multiplier=mult,
            derived_claim_weight=group_weight,observed_tl_mix=float(r['tl_mix'])))
        for k in ks:cells.append(dict(body=b,age=k,claim_weight=group_weight*splits[k],repair_multiplier=mult))
    anchor=dict(status='CCC 2025 frequency/claim-mix calibration case; population and body mapping provisional, response shape inherited.',
        fleet_reference_weights=[0,0,1,0,0],cells=cells,
        source_sha256=json.loads((HERE/'source_manifest.json').read_text())['source_sha256'],
        source='model/ccc_age_body_2026-09-29/source_cells.csv',
        older_age_split='Inherited relative claims weights conditional on body and 7+; not observed in this workbook.')
    (HERE/'cohort_anchor.json').write_text(json.dumps(anchor,indent=2)+'\n')
    write_csv('calibration_cells.csv',fits)
    # Repaired means and selected values are no longer forced to the predecessor targets.
    diagnostic=[]
    for label,ks,target in [('0-6',[0,1,2],5721),('7+',[3,4,5],3682)]:
        numerator=denominator=0.
        for c in cells:
            b,k=c['body'],c['age']
            if k not in ks:continue
            row=e['cohorts'][k];sigma=row['sigma'];mu=row['log_car_repair_median']+math.log(e['repair_ratios'][b]*c['repair_multiplier'])
            u=1-econ(b,k,c['repair_multiplier'])['TLF'];w=c['claim_weight']
            numerator+=w*math.exp(mu+sigma*sigma/2)*m.old.N.cdf(m.old.N.inv_cdf(u)-sigma);denominator+=w*u
        diagnostic.append(dict(metric='repairable_mean',group=label,new_implied=numerator/denominator,previous_target=target,status='Cross-population diagnostic; no longer calibration target in CCC case'))
    for a,ks in enumerate([[0],[1],[2],[3,4,5]]):
        num=den=0.
        for c in cells:
            b,k=c['body'],c['age']
            if k in ks:
                mass=c['claim_weight']*econ(b,k,c['repair_multiplier'])['TLF']
                num+=mass*e['cohorts'][k]['car_ACV']*e['value_ratios'][b];den+=mass
        diagnostic.append(dict(metric='selected_vehicle_value',group=str(a),new_implied=num/den,previous_target=e['selected_value_checks'][a],status='Cross-population diagnostic; inherited values not refitted'))
    write_csv('economic_crosschecks.csv',diagnostic)
    oldref=bridge.engine_run(1,1,1)
    newref=bridge.engine_run(1,1,1,anchor_path=ANCHOR)
    p=json.loads((ROOT/'model/aftermarket_bridge_2026-09-29/inputs.json').read_text());p['cohort_anchor_path']=ANCHOR
    (HERE/'aftermarket_inputs.json').write_text(json.dumps(p,indent=2)+'\n')
    config=bridge.reference(ANCHOR);config.update(name='ccc_2025_age_body_reference',status=anchor['status'])
    (HERE/'reference_config.json').write_text(json.dumps(config,indent=2)+'\n')
    summaries=[];quarters=[]
    for name,params,o,r in [('ccc_reference',p,0,0)]+[(f'ccc_{case["name"]}',p,case['oem_to_aftermarket'],case['recycled_to_aftermarket']) for case in p['cases']]:
        sol=bridge.solve(params,o,r);rows=bridge.forecast_result(params,sol)
        summary=bridge.summarize(name,params,sol,rows);summaries.append(summary)
        quarters += [dict(scenario=name,**row) for row in rows]
    half=copy.deepcopy(p);half['threshold_responsive_fraction']=.5
    sol=bridge.solve(half,.04,.015);rows=bridge.forecast_result(half,sol)
    summaries.append(bridge.summarize('ccc_larger_half_switching',half,sol,rows))
    quarters += [dict(scenario='ccc_larger_half_switching',**row) for row in rows]
    write_csv('scenario_summary.csv',summaries);write_csv('quarterly_results.csv',quarters)
    write_csv('base_component_ledger.csv',newref['base_ledger'])
    # Verify the source anchor at its actual 2025 fleet point, not a fiscal-quarter proxy.
    mass=sum(c['claim_weight']*econ(c['body'],c['age'],c['repair_multiplier'])['TLF'] for c in cells)
    checks={
        'all_16_source_tlfs_reproduce':max(abs(x['calibrated_tlf']-x['observed_tlf']) for x in fits)<1e-10,
        'claim_weights_sum_one':abs(sum(c['claim_weight'] for c in cells)-1)<1e-12,
        'all_16_total_loss_mix_cells_reproduce':max(abs(x['derived_claim_weight']*x['calibrated_tlf']/mass-x['observed_tl_mix']) for x in fits)<1e-10,
        'prior_reference_reproduces':abs(sum(q['legacy_service_musd'] for q in oldref['quarters'])-4105.804039246686)<1e-6,
        'historical_reported_dollars_preserved':all(abs(sum(a.values())-sum(b.values()))<1e-8 for a,b in zip(oldref['base_ledger'],newref['base_ledger'])),
        'zero_shift_matches_own_reference':abs(summaries[0]['FY_delta_vs_reference_musd'])<1e-5,
        'ccc_reference_used_for_thesis_deltas':all(abs(s['FY_legacy_service_musd']-s['FY_delta_vs_reference_musd']-summaries[0]['FY_legacy_service_musd'])<1e-5 for s in summaries),
    }
    # Economic invariants through the new integration, not only level-fitting checks.
    price=bridge.engine_run(1,1,1.03,anchor_path=ANCHOR)
    cheaper=bridge.engine_run(.99,1,1,anchor_path=ANCHOR)
    checks['price_only_preserves_units']=all(abs(a['modeled_insurance_sales']-b['modeled_insurance_sales'])<1e-7 for a,b in zip(newref['quarters'],price['quarters']))
    checks['cheaper_repairs_reduce_totals']=all(b['totals']<a['totals'] for a,b in zip(newref['operating'][4:],cheaper['operating'][4:]))
    checks['forward_changes_preserve_new_base']=newref['base_ledger']==cheaper['base_ledger']==price['base_ledger']
    assert all(checks.values()),checks
    result=dict(checks=checks,anchor_tlf=mass,
        previous_reference_service_musd=sum(q['legacy_service_musd'] for q in oldref['quarters']),
        ccc_reference_service_musd=sum(q['legacy_service_musd'] for q in newref['quarters']),
        economic_crosschecks=diagnostic,
        status='Conditional CCC composition/level case. Not a measured aftermarket forecast; old exact repair/value calibration does not transfer.',
        source_manifest_sha256=hashlib.sha256((HERE/'source_manifest.json').read_bytes()).hexdigest())
    (HERE/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
    dependencies=[HERE/'source_cells.csv',HERE/'source_manifest.json',HERE/'cohort_anchor.json',
        HERE/'integrate.py',m.HERE/'model.py',m.HERE/'scenario_configs.json',m.HERE/'evidence_manifest.json',
        ROOT/'model/aftermarket_bridge_2026-09-29/bridge.py',ROOT/'model/aftermarket_bridge_2026-09-29/inputs.json',
        m.LEGACY/'engine.py',m.LEGACY/'assumptions.json',m.old.OLD,m.old.ECON,m.old.BIRTHS,
        ROOT/'docs/consensus_review_2026-09-28/total_revenue_consensus.csv']
    (HERE/'runtime_manifest.json').write_text(json.dumps({'status':result['status'],
        'dependencies':{str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in dependencies}},indent=2)+'\n')
    print(json.dumps(dict(results=summaries,checks=result),indent=2))

if __name__=='__main__':main()
