"""Small accounting checks; no estimated causal coefficients or new forecasts."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
source = ROOT / 'raw/ccc/crash-course-2024-q4.txt'
rows = []
for coverage, exposure, claims in [('collision', -2.0, -5.7), ('property_damage', -2.7, -3.6), ('comprehensive', -2.4, -2.8)]:
    e, c = 1 + exposure / 100, 1 + claims / 100
    frequency = c / e
    assert abs(e * frequency - c) < 1e-12
    rows.append({'coverage': coverage, 'exposure_change_pct': exposure,
                 'paid_claim_count_change_pct': claims,
                 'implied_paid_frequency_change_pct': 100 * (frequency - 1)})

# Published rounded claim shares, NOT policy shares. These scenarios prove non-identification.
s0, s1 = .245, .281
odds_change = (s1 / (1 - s1)) / (s0 / (1 - s0))
result = {
    'source': str(source.relative_to(ROOT)),
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'source_location': 'line 105; Q4 2024 report, through Q2 2024, annualized exposures',
    'warning': 'Arithmetic within the reported aggregate; not an accident/filing decomposition or a current forecast.',
    'coverage_rows': rows,
    'collision_to_property_damage_exposure_ratio_change_pct': 100 * (.98 / .973 - 1),
    'deductible_identification': {
        'source': 'data/csv/ccc_deductible_share_quarterly.csv, 2024Q4 and 2025Q4',
        'observed_high_deductible_repairable_claim_share_start': s0,
        'observed_high_deductible_repairable_claim_share_end': s1,
        'relative_claim_share_odds_change_pct': 100 * (odds_change - 1),
        'interpretation': 'Observed claim odds = covered exposure odds times relative repairable-claim incidence. Neither factor separately identified.',
        'example_exposure_odds_factor_if_relative_claim_incidence_unchanged': odds_change,
        'example_exposure_odds_factor_if_relative_claim_incidence_falls_10pct': odds_change / .9,
        'example_relative_claim_incidence_factor_if_exposure_odds_unchanged': odds_change,
        'status': 'Illustrative identification examples, not estimated behavioral changes.'
    }
}
Path(__file__).with_name('coverage_screen_results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
