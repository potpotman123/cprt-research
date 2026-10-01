"""Reproduce the audit comparisons and exact interaction-aware attribution."""
import copy
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import scenarios as s


def write_csv(path, rows):
    with path.open('w') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)


def main():
    a = json.loads((s.HERE/'assumptions.json').read_text())
    ref_config, p, premiums = s.load()
    factors = a['factors']; results = {}; summaries = {}; quarter_rows = []; feedback = {}
    reference = s.m.run(ref_config)
    for mask in range(16):
        flags = {name:bool(mask & (1 << i)) for i,name in enumerate(factors)}
        c = s.configure(flags, a)
        r = s.run_aftermarket(c,p,a['oem_to_aftermarket'],a['recycled_to_aftermarket']) if flags['aftermarket'] else s.m.run(c)
        if r['base_ledger'] != reference['base_ledger']:
            raise AssertionError('Thesis combination changed the common historical ledger')
        results[mask] = r
        name = c['name']; summaries[mask] = dict(mask=mask,scenario=name,**s.annual(r))
        if flags['aftermarket']:
            feedback[name] = r['aftermarket_feedback']
        for q in r['quarters']:
            quarter_rows.append(dict(mask=mask,scenario=name,period=q['period'],service_musd=q['legacy_service_musd'],
                insurance_units=q['modeled_insurance_sales'],TLF=q['TLF'],insurance_ASP=q['insurance_ASP']))
    base, bear = results[0], results[15]
    attribution = []
    for i, name in enumerate(factors):
        contributions = {key:0. for key in ['service_musd','modeled_insurance_units','insurance_allin_RPU']}
        for mask in range(16):
            if mask & (1 << i): continue
            n = bin(mask).count('1')
            weight = math.factorial(n)*math.factorial(3-n)/math.factorial(4)
            for key in contributions:
                contributions[key] += weight*(summaries[mask | (1 << i)][key]-summaries[mask][key])
        delta = summaries[15]['service_musd']-summaries[0]['service_musd']
        attribution.append(dict(factor=name,service_contribution_musd=contributions['service_musd'],
            share_of_net_shortfall=contributions['service_musd']/delta,
            modeled_unit_contribution=contributions['modeled_insurance_units'],
            allin_RPU_contribution_usd=contributions['insurance_allin_RPU'],
            standalone_service_delta_musd=summaries[1 << i]['service_musd']-summaries[0]['service_musd']))
    if abs(sum(x['service_contribution_musd'] for x in attribution)-(summaries[15]['service_musd']-summaries[0]['service_musd'])) > 1e-7:
        raise AssertionError('Factor attribution does not reconcile')
    bridge = []; previous=0
    for i,name in enumerate(factors):
        current=previous | (1 << i)
        bridge.append(dict(step=name,from_mask=previous,to_mask=current,
            delta_musd=summaries[current]['service_musd']-summaries[previous]['service_musd'],
            ending_service_musd=summaries[current]['service_musd']))
        previous=current
    diagnostics = {}
    def diagnostic(name,c,against=reference):
        result=s.m.run(c); diagnostics[name]=s.effects(result,against)
        diagnostics[name]['quarterly_TLF']=[q['TLF'] for q in result['quarters']]
        return result
    c=copy.deepcopy(ref_config);c['nonfiling']=s.m.forecast(.1,0.)
    diagnostic('10pct_repairable_nonfiling_only',c)
    for key in ['repair','expected_salvage','realized_salvage']:
        c=copy.deepcopy(ref_config);c[key][4:]=[x*1.05 for x in c[key][4:]]
        diagnostic(key+'_plus5pct',c)
    c=copy.deepcopy(ref_config);c['expected_salvage'][4:]=c['realized_salvage'][4:]
    diagnostic('reference_expected_salvage_catches_up_to_realized',c)
    d,_,_=s.m.old.load()
    c=copy.deepcopy(ref_config);c['carrier_mode']='inherited_runoff'
    for carrier in d['carriers']:
        c['allocation_overrides'][carrier['name']]=carrier['allocations'][:4]+[carrier['allocations'][3]]*4
    hold=diagnostic('hold_all_Q4_allocations_and_carrier_mix',c)
    c=copy.deepcopy(ref_config);c['carrier_mode']='inherited_runoff'
    runoff=diagnostic('inherited_PGR_runoff_only',c)
    diagnostics['PGR_remaining_runoff_vs_Q4_hold']=s.effects(runoff,hold)
    c['carrier_terms_by_period']={'Progressive':[{} for _ in range(4)]+[{'seller_pct':.0375} for _ in range(4)]}
    diagnostic('assumed_PGR_25bp_seller_concession_vs_runoff',c,runoff)
    c=copy.deepcopy(ref_config);c['fleet_period_weights']=[x['weights'] for x in d['periods'][:4]]*2
    frozen=s.m.run(c);diagnostics['existing_fleet_roll_vs_frozen']=s.effects(reference,frozen)
    c=copy.deepcopy(ref_config)
    for k in ['intl_units','intl_rpu']: c[k][4:]=[1.]*4
    flat_intl=s.m.run(c)
    diagnostics['inherited_international_continuation_musd']=s.annual(reference)['service_musd']-s.annual(flat_intl)['service_musd']
    # Sourcing countercases use the same premium/allocation/fleet context.
    context=s.configure({x:True for x in factors},a); context_base=s.m.run(context)
    variants=[('OEM_only',p,a['oem_to_aftermarket'],[0.]*4),
              ('weak_recycler_transmission',dict(p,recycler_price_transmission_weight=.1),a['oem_to_aftermarket'],a['recycled_to_aftermarket']),
              ('no_threshold_switching',dict(p,threshold_responsive_fraction=0.),a['oem_to_aftermarket'],a['recycled_to_aftermarket']),
              ('full_shift_all_year',p,[.04]*4,[.015]*4)]
    for name,params,o,r in variants:
        diagnostics['aftermarket_'+name+'_vs_same_context']=s.effects(s.run_aftermarket(context,params,o,r),context_base)
    output=dict(as_of=a['as_of'],forecast_admission=False,status=a['status'],
        saved_CCC_reference=s.annual(reference),recovery_comparator=s.annual(base),combined_case=s.annual(bear),
        combined_vs_comparator=s.effects(bear,base),combined_vs_saved_reference=s.effects(bear,reference),
        factor_attribution=attribution,sequential_bridge=bridge,diagnostics=diagnostics,
        attribution_note='Shapley averages each factor over all 24 orders; negative net-share values are offsets. No allocation of this accounting identity establishes causation.')
    # Mask 10 has the existing fleet roll and no extra premium relief, exactly
    # the saved CCC reference. Only allocation and sourcing are incremental to it.
    if abs(summaries[10]['service_musd']-s.annual(reference)['service_musd']) > 1e-8:
        raise AssertionError('Saved reference no longer maps to subset 10')
    output['attribution_vs_saved_reference'] = {
        'market_allocation_musd': .5*((summaries[11]['service_musd']-summaries[10]['service_musd'])+(summaries[15]['service_musd']-summaries[14]['service_musd'])),
        'aftermarket_musd': .5*((summaries[14]['service_musd']-summaries[10]['service_musd'])+(summaries[15]['service_musd']-summaries[11]['service_musd'])),
        'premium_recovery_musd': 0., 'fleet_mix_musd': 0.,
        'interpretation': 'Premium non-recovery and fleet roll are already in the saved reference. Their diagnostic comparator contributions must not be added again.'}
    (s.HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n')
    write_csv(s.HERE/'factor_attribution.csv',attribution)
    write_csv(s.HERE/'scenario_summary.csv',list(summaries.values()))
    write_csv(s.HERE/'quarterly_results.csv',quarter_rows)
    (s.HERE/'aftermarket_feedback.json').write_text(json.dumps(feedback,indent=2)+'\n')
    # Save the exact two end configurations, rather than modifying the old reference.
    end_configs={name:s.configure({f:bool(mask & (1 << i)) for i,f in enumerate(factors)},a) for name,mask in [('recovery_comparator',0),('combined_before_aftermarket',15)]}
    (s.HERE/'endpoint_configs.json').write_text(json.dumps(end_configs,indent=2)+'\n')
    dependencies=[s.HERE/'assumptions.json',s.HERE/'scenarios.py',s.HERE/'run.py',s.ROOT/'model/revenue_architecture_2026-09-28/model.py',s.ROOT/'model/revenue_architecture_2026-09-28/premium_channels.py',s.ROOT/'model/aftermarket_bridge_2026-09-29/bridge.py',s.ROOT/'model/ccc_age_body_2026-09-29/reference_config.json',s.ROOT/'model/ccc_age_body_2026-09-29/cohort_anchor.json',s.ROOT/'model/ccc_age_body_2026-09-29/aftermarket_inputs.json',s.ROOT/'model/premium_scenarios_2026-10-01/assumptions.json',s.ROOT/'model/integrated_service_2026-09-28/engine.py',s.ROOT/'model/integrated_service_2026-09-28/assumptions.json',s.ROOT/'model/linked_service_revenue_2026-09-28/inputs.json',s.ROOT/'docs/historical_body_births_2026-09-28/candidate_body_births.csv',s.ROOT/'docs/fleet_selection_2026-09-28/age_constrained_engine_results.json',s.ROOT/'docs/consensus_review_2026-09-28/total_revenue_consensus.csv']
    (s.HERE/'runtime_manifest.json').write_text(json.dumps({'as_of':a['as_of'],'scope':'Common-reference audit reproduction, no raw-source refresh','dependencies':{str(p.relative_to(s.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}},indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ['saved_CCC_reference','recovery_comparator','combined_case','factor_attribution']},indent=2),flush=True)

if __name__=='__main__':main()
