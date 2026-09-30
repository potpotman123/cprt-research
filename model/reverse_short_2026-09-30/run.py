"""Bounded, offline reverse stress through the existing quarterly engine.

Solve an operating hurdle, not an empirical coefficient. All scenario outputs
stay here; no changes to the saved reference, history, calibration or workbook.
"""
from pathlib import Path
import copy
import csv
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'model/revenue_architecture_2026-09-28'))
import model as m


def total(result):
    return sum(q['legacy_service_musd'] for q in result['quarters'])


def insurance(q):
    return q['insurance_core_musd'] + q['title_musd'] + q['delivery_musd']


def csv_write(name, rows):
    with (HERE / name).open('w') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0], lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    a = json.loads((HERE / 'assumptions.json').read_text())
    ref = json.loads((ROOT / a['reference']).read_text())
    benchmark = float(json.loads((ROOT / a['benchmark']).read_text())[a['benchmark_field']])
    dependencies = json.loads((ROOT / 'model/ccc_age_body_2026-09-29/runtime_manifest.json').read_text())['dependencies']
    paths = [ROOT / p for p in dependencies] + [ROOT / a['reference'], ROOT / a['benchmark']]
    fingerprints = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    data, _, _ = m.old.load()
    ramp = a['unit_shortfall_ramp_fy27']
    assert len(ramp) == 4 and all(0 <= v <= 1 for v in ramp)
    assert ref['carrier_mode'] == 'same_quarter_neutral' and not ref['carrier_terms']
    assert ref['sales_timing']['mode'] == 'sale_equivalent'
    assert ref['title']['basis'] == ref['delivery']['basis'] == 'sales'

    def config(name, terminal=0.0, price=False):
        c = copy.deepcopy(ref)
        c.update(name=name, status=a['status'])
        if price:
            c['realized_salvage'][4:] = a['price_driver_fy27']
        if terminal:
            assert 0 <= terminal < 1
            for carrier in data['carriers']:
                hist = carrier['allocations'][:4]
                c['allocation_overrides'][carrier['name']] = hist + [
                    hist[q] * (1 - terminal * ramp[q]) for q in range(4)]
        return c

    configs = {'reference': config('reference'), 'price_only': config('price_only', price=True)}
    results = {name: m.run(c) for name, c in configs.items()}
    base = results['reference']
    priced = results['price_only']
    assert abs(total(base) - 4093.077730243895) < 1e-6
    # Exact under uniform allocation scaling, common cohort economics and
    # unchanged per-sale ancillary services. Validate against the full engine.
    exposure = sum(insurance(q) * ramp[i] for i, q in enumerate(priced['quarters']))
    hurdles = []
    for miss in a['target_miss_fractions']:
        target = benchmark * (1 - miss)
        terminal = (total(priced) - target) / exposure
        assert 0 <= terminal < 1
        name = f'joint_target_{100*miss:g}pct'
        configs[name] = config(name, terminal, True)
        results[name] = m.run(configs[name])
        assert abs(total(results[name]) - target) < 1e-6
        hurdles.append(dict(target_miss_pct=100*miss, target_service_musd=target,
                            terminal_unit_shortfall_pct=100*terminal,
                            q1_unit_shortfall_pct=100*terminal*ramp[0],
                            q2_unit_shortfall_pct=100*terminal*ramp[1],
                            q3_unit_shortfall_pct=100*terminal*ramp[2],
                            q4_unit_shortfall_pct=100*terminal*ramp[3],
                            own_reference_delta_musd=target-total(base),
                            named_benchmark_gap_musd=target-benchmark,
                            status='ASSUMED target; reverse-solved operating hurdle, NOT a forecast'))
    selected = next(h for h in hurdles if abs(h['target_miss_pct']/100-a['display_target_miss_fraction']) < 1e-10)
    configs['units_only'] = config('units_only', selected['terminal_unit_shortfall_pct']/100)
    results['units_only'] = m.run(configs['units_only'])
    joint_name = f"joint_target_{100*a['display_target_miss_fraction']:g}pct"
    annual, quarterly = [], []
    for name, result in results.items():
        assert result['base_ledger'] == base['base_ledger']
        assert result['base_modeled_units'] == base['base_modeled_units']
        for i, q in enumerate(result['quarters']):
            b = base['quarters'][i]
            assert abs(q['TLF']-b['TLF']) < 1e-12
            assert q['other_us_musd'] == b['other_us_musd']
            assert q['intl_service_musd'] == b['intl_service_musd']
            units = q['modeled_insurance_sales']
            base_units = b['modeled_insurance_sales']
            rpu = insurance(q)*1e6/units
            base_rpu = insurance(b)*1e6/base_units
            quarterly.append(dict(case=name, period=q['period'],
                legacy_service_musd=q['legacy_service_musd'],
                service_delta_vs_reference_musd=q['legacy_service_musd']-b['legacy_service_musd'],
                insurance_units_vs_reference_pct=100*(units/base_units-1),
                insurance_units_yoy_pct=100*(q['insurance_sales_factor']-1),
                allin_insurance_RPU=rpu,
                allin_RPU_vs_reference_pct=100*(rpu/base_rpu-1),
                realized_price_driver_pct=100*(configs[name]['realized_salvage'][i+4]-1),
                status=a['status']))
        annual.append(dict(case=name, FY27_service_musd=total(result),
            delta_vs_reference_musd=total(result)-total(base),
            gap_vs_JPM_musd=total(result)-benchmark,
            gap_vs_JPM_pct=100*(total(result)/benchmark-1), status=a['status']))
    interaction = total(results[joint_name])-total(results['units_only'])-total(priced)+total(base)
    expected_interaction = sum((insurance(base['quarters'][i])-insurance(priced['quarters'][i])) *
        selected['terminal_unit_shortfall_pct']/100*ramp[i] for i in range(4))
    assert abs(interaction-expected_interaction) < 1e-6
    assert abs(total(results[joint_name])-total(base) -
               ((total(results['units_only'])-total(base))+(total(priced)-total(base))+interaction)) < 1e-6
    assert all(abs(q['modeled_insurance_sales']-base['quarters'][i]['modeled_insurance_sales']) < 1e-6
               for i, q in enumerate(priced['quarters']))
    assert all(abs(r['quarters'][0]['legacy_service_musd']-base['quarters'][0]['legacy_service_musd']) < 1e-6
               for r in results.values())
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == sha for p, sha in fingerprints.items())
    checks = dict(reference_reproduced=True, historical_levels_preserved=True,
        targets_match_full_engine=True, exact_four_case_interaction=True,
        first_quarter_unchanged=True, price_only_preserves_units=True,
        selection_and_other_branches_unchanged=True, source_hashes_unchanged=True,
        selected_joint_case=joint_name, interaction_musd=interaction,
        forecast_admission=False, catalyst_verified=False)
    for name, obj in [('scenario_configs.json', configs), ('checks.json', checks),
                      ('source_manifest.json', fingerprints)]:
        (HERE/name).write_text(json.dumps(obj, indent=2)+'\n')
    csv_write('hurdles.csv', hurdles)
    csv_write('scenario_summary.csv', annual)
    csv_write('quarterly_results.csv', quarterly)
    print(json.dumps({'hurdles':hurdles, 'annual':annual, 'checks':checks}, indent=2))


if __name__ == '__main__':
    main()
