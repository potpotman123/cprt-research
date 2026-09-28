"""Bounded structural diagnostics. No source or forecast outputs overwritten."""
import copy
import hashlib
import json
import math
from pathlib import Path

import engine


def same(a, b):
    return math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-8)


def main():
    d, e, c = engine.load()
    baseline = engine.run(d, e, c)
    dc = copy.deepcopy(d)
    for carrier in dc['carriers']:
        carrier['allocations'][4:] = [.5] * 4
    allocation = engine.run(dc, e, c)
    # Non-PGR forecasts freeze Q4 allocation; Progressive changes in this test.
    assert any(not same(a['fee_sales_raw'], b['fee_sales_raw']) for a, b in zip(baseline['quarters'][4:], allocation['quarters'][4:]))
    assert all(same(a['insurance_allin_RPU'], b['insurance_allin_RPU']) for a, b in zip(baseline['quarters'], allocation['quarters']))
    cc = copy.deepcopy(c)
    cc['title']['adoption'] *= 1.1
    title = engine.run(d, e, cc)
    assert all(same(a['fee_sales_raw'], b['fee_sales_raw']) for a, b in zip(baseline['quarters'], title['quarters']))
    cs = copy.deepcopy(c)
    cs['insurance_share_of_us_service_base'] = .8
    split = engine.run(d, e, cs)
    i = c['base_period_index']
    assert same(baseline['quarters'][i]['us_musd'], split['quarters'][i]['us_musd'])
    assert not same(baseline['quarters'][i]['normalized_fee_sales'], split['quarters'][i]['normalized_fee_sales'])
    assert all(r['physical_opening_inventory'] is None and r['physical_ending_inventory'] is None for r in baseline['quarters'])
    files = [engine.HERE/'engine.py',engine.HERE/'history_repair.py',engine.HERE/'assumptions.json',engine.OLD,engine.ECON,engine.BIRTHS]
    result = {
        'status': 'Structural diagnostics only; none validates an economic forecast.',
        'findings': {
            'allocation_changes_units_but_not_RPU': True,
            'title_adoption_changes_no_raw_sale_units': True,
            'different_insurance_split_same_Q4_US_revenue_different_normalized_units': True,
            'physical_inventory_unavailable': True,
            'forecast_multiplier_arrays_all_one': {k: all(x == 1 for x in v[4:]) for k,v in c['quarter_drivers'].items()},
            'quarter_driver_names': list(c['quarter_drivers']),
            'no_independent_salvage_demand_quarter_driver': 'salvage_demand' not in c['quarter_drivers'],
            'no_time_varying_buyer_mix_or_fee_schedule_driver': not any(k in c['quarter_drivers'] for k in ['preferred_buyer_fraction','fee_schedule']),
        },
        'normalized_units_ratio_80_vs_90pct_insurance_split': split['quarters'][i]['normalized_fee_sales']/baseline['quarters'][i]['normalized_fee_sales'],
        'source_hashes': {str(p.relative_to(engine.ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        'no_model_inputs_or_existing_outputs_changed': True,
    }
    (engine.HERE/'architecture_audit_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['findings'],indent=2))


if __name__ == '__main__':
    main()
