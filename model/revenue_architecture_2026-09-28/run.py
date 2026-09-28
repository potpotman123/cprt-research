"""Generate explicit scenarios, ledgers, interactions and source fingerprints."""
import copy
import hashlib
import json
import model as m
import evidence


def reference(name, international=False, price=1.):
    c=m.configuration();c['name']=name
    c['realized_salvage']=m.forecast(price)
    if international:
        d,_,_=m.old.load()
        growth=d['actuals'][3]['intl_service']/d['prior_actuals'][3]['intl_service']
        c['intl_units']=m.forecast(growth/1.035)
        c['intl_rpu']=m.forecast(1.035)
    return c


def totals(r):
    keys=['legacy_service_musd','legacy_total_musd','capiq_conditional_gap_musd','jpm_legacy_total_gap_musd']
    return {'H1_'+k:sum(x[k] for x in r['quarters'][:2]) for k in keys} | {
        'FY_'+k:sum(x[k] for x in r['quarters']) for k in keys}


def main():
    ev=evidence.build()
    cases={}
    cases['flat_branches']=reference('flat_branches')
    cases['intl_continuation']=reference('intl_continuation',True)
    cases['price_3p7_intl_continuation']=reference('price_3p7_intl_continuation',True,1.037)
    cases['price_6_intl_continuation']=reference('price_6_intl_continuation',True,1.06)
    # Realized-price scenarios hold expected salvage fixed to isolate price pass-through.
    # They are not full anticipated-demand forecasts.
    pivot=cases['price_3p7_intl_continuation']
    for name,overrides in {
        'repair_down_3':{'repair':m.forecast(.97)},
        'expected_salvage_up_3':{'expected_salvage':m.forecast(1.03)},
        'repair_down_3_salvage_up_3':{'repair':m.forecast(.97),'expected_salvage':m.forecast(1.03)},
        'salvage_both_down_3':{'expected_salvage':m.forecast(.97),'realized_salvage':m.forecast(1.037*.97)},
        'claims_down_2':{'claims':m.forecast(.98)},
        'inherited_carrier':{'carrier_mode':'inherited_runoff'},
    }.items():
        c=copy.deepcopy(pivot);c.update(overrides);c['name']=name;cases[name]=c
    adoption=copy.deepcopy(pivot);adoption['name']='service_adoption_up_10_relative'
    adoption['title']['adoption']=m.forecast(.55,.5)
    adoption['delivery']['adoption']=m.forecast(.11,.1)
    cases[adoption['name']]=adoption
    low=copy.deepcopy(pivot);low['name']='insurance_split_80';low['insurance_service_fraction']=.8;cases[low['name']]=low
    for delta in [-.05,.05]:
        name='other_us_activity_'+('down' if delta<0 else 'up')+'_5'
        co=copy.deepcopy(pivot);co['name']=name;co['other_us_units']=m.forecast(1+delta);cases[name]=co
    purchase=copy.deepcopy(pivot);purchase['name']='purchased_JPM_annual_growth_proxy'
    d,_,_=m.old.load()
    pbase=sum(x['us_vehicle']+x['intl_vehicle'] for x in d['actuals'])
    # Comparison overlay only: allocate broker annual growth proportionally, not a new disclosed quarterly forecast.
    purchase['purchased_asp']=m.forecast(ev['jpm_fy27_purchased_musd']/pbase)
    cases[purchase['name']]=purchase
    results={name:m.run(c) for name,c in cases.items()}
    rows=[];summary=[]
    for name,r in results.items():
        rows += r['quarters']
        t=totals(r)
        summary.append(dict(scenario=name,**t,
            FY_service_gap_vs_JPM_musd=t['FY_legacy_service_musd']-ev['jpm_fy27_service_musd'],
            FY_total_gap_vs_JPM_annual_musd=t['FY_legacy_total_musd']-ev['jpm_fy27_total_musd'],
            H1_delta_vs_price3p7_case_musd=t['H1_legacy_service_musd']-totals(results['price_3p7_intl_continuation'])['H1_legacy_service_musd'],
            status='Conditional scenarios, not probabilities or adopted forecast'))
    m.write_csv(m.HERE/'quarterly_scenarios.csv',rows)
    m.write_csv(m.HERE/'scenario_summary.csv',summary)
    ledger=[]
    for name in ['flat_branches','insurance_split_80']:
        for q,row in enumerate(results[name]['base_ledger']):
            ledger.append(dict(scenario=name,period=f'FY2026Q{q+1}',**row,
                assumed_insurance_fraction=cases[name]['insurance_service_fraction'],
                modeled_units=results[name]['base_modeled_units'][q],status='Conditional allocation of observed total; components unmeasured'))
    m.write_csv(m.HERE/'base_component_ledger.csv',ledger)
    # Alternative international and starting-scale cases explicitly modify the hurdle.
    benchmarks=list(__import__('csv').DictReader((m.HERE/'benchmark_perimeter.csv').open()))[:2]
    hurdles=[]
    for scenario in ['flat_branches','intl_continuation','insurance_split_80']:
        r=results[scenario]
        B=sum(sum(r['base_ledger'][q][k] for k in ['insurance_core','title','delivery']) for q in range(2))
        rest=sum(x['other_us_musd']+x['intl_service_musd']+x['purchased_musd'] for x in r['quarters'][:2])
        for name,target in [('CapIQ conditional',sum(float(x['capiq_total_musd']) for x in benchmarks)),('JPM ex-ACV',sum(float(x['jpm_total_musd']) for x in benchmarks))]:
            for u in [-.05,0,.05]:
                fee=(target-rest)/B/(1+u)-1
                assert abs(B*(1+u)*(1+fee)+rest-target)<1e-8
                hurdles.append(dict(scenario=scenario,benchmark=name,unit_growth=u,required_allin_insurance_RPU_growth=fee,
                    status='Uniform H1 driver requirement, not inferred analyst units/RPU'))
    m.write_csv(m.HERE/'hurdles.csv',hurdles)
    ref=totals(results['price_3p7_intl_continuation'])['H1_legacy_service_musd']
    a=totals(results['repair_down_3'])['H1_legacy_service_musd']
    b=totals(results['expected_salvage_up_3'])['H1_legacy_service_musd']
    both=totals(results['repair_down_3_salvage_up_3'])['H1_legacy_service_musd']
    interaction=dict(reference_H1_musd=ref,repair_delta_musd=a-ref,salvage_delta_musd=b-ref,
        combined_delta_musd=both-ref,interaction_musd=both-a-b+ref,
        status='Unvalidated response elasticities; shocks illustrative, not estimated')
    (m.HERE/'interaction.json').write_text(json.dumps(interaction,indent=2)+'\n')
    (m.HERE/'scenario_configs.json').write_text(json.dumps(cases,indent=2)+'\n')
    sources=[m.HERE/'model.py',m.HERE/'run.py',m.HERE/'evidence.py',m.HERE/'fee_schedule_registry.json',m.old.OLD,m.old.ECON,m.old.BIRTHS,
             m.LEGACY/'assumptions.json',m.ROOT/'docs/consensus_review_2026-09-28/total_revenue_consensus.csv']
    (m.HERE/'manifest.json').write_text(json.dumps(dict(status='Executable conditional architecture; evidence limitations remain',
        sources={str(p.relative_to(m.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        scenarios=len(cases),no_legacy_outputs_overwritten=True),indent=2)+'\n')
    print(json.dumps({'benchmarks':{k:ev[k] for k in ['jpm_fy27_service_musd','service_growth_vs_reported_FY26','capiq_minus_jpm_fy27_musd']},
        'scenarios':summary,'interaction':interaction},indent=2))


if __name__=='__main__':main()
