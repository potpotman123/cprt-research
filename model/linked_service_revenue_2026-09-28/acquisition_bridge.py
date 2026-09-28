"""Small read-only bridge; source workbook is never modified. USD millions.

Equal monthly allocation is a timing convention, not measured seasonality.
Management projections are not our adopted forecast. No valuation assigned to ACV.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/acv_reconciliation_2026-09-28'
SOURCE = ROOT / 'data/csv/acv_14d9_projections.csv'
OUT.mkdir(exist_ok=True)
with SOURCE.open() as f:
    projections = {int(r['fiscal_year'][:4]): r for r in csv.DictReader(line for line in f if not line.startswith('#'))}

rows = []
for start in [(2026, 11), (2027, 1), (2027, 4)]:
    for fy in (2027, 2028):
        for q in range(1, 5):
            first = (fy - 1) * 12 + 7 + (q - 1) * 3  # August, zero-based month
            months = [divmod(first + i, 12) for i in range(3)]
            active = [(y, m + 1) for y, m in months if (y, m + 1) >= start]
            revenue = sum(float(projections[y]['revenue_musd']) / 12 for y, m in active)
            ebitda = sum(float(projections[y]['adj_ebitda_unburdened_sbc_musd']) / 12 for y, m in active)
            fcf = None if any(not projections[y]['unlevered_fcf_musd'] for y, m in active) else sum(float(projections[y]['unlevered_fcf_musd']) / 12 for y, m in active)
            rows.append(dict(first_consolidated_month=f'{start[0]}-{start[1]:02}', fiscal_period=f'FY{fy}Q{q}', consolidated_months=len(active), revenue_musd=revenue, adjusted_ebitda_ex_sbc_musd=ebitda, source_defined_ufcf_musd=fcf, status='Management standalone projection; uniform monthly timing assumption'))
with (OUT / 'acquisition_timing.csv').open('w') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator='\n'); writer.writeheader(); writer.writerows(rows)

jan = [r for r in rows if r['first_consolidated_month']=='2027-01']
assert abs(sum(r['revenue_musd'] for r in jan[:4]) - 964*7/12) < 1e-8
assert jan[0]['revenue_musd'] == 0
assert jan[1]['consolidated_months'] == 1
assert abs(sum(r['revenue_musd'] for r in jan[4:]) - (964*5+1116*7)/12) < 1e-8
assert rows[1]['source_defined_ufcf_musd'] is None  # CY26 FCF unavailable
summary = {
    'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'source': str(SOURCE),
    'first_consolidated_month_assumption': '2027-01',
    'fy27_acv_revenue_musd': sum(r['revenue_musd'] for r in jan[:4]),
    'fy28_acv_revenue_musd': sum(r['revenue_musd'] for r in jan[4:]),
    'fy27_acv_source_defined_ufcf_musd': sum(r['source_defined_ufcf_musd'] for r in jan[:4]),
    'capiq_fy27_total_revenue_quarter_sum_musd': 4860.97,
    'capiq_plus_acv_if_all_contributors_exclude_acv_musd': 4860.97 + sum(r['revenue_musd'] for r in jan[:4]),
    'warning': 'CapIQ acquisition perimeter unverified; illustrative addition must not be labelled consensus.',
    'checks': 'Quarter mapping, fiscal sums, zero pre-close revenue, and missing CY26 FCF propagation passed.'
}
(OUT / 'calculations.json').write_text(json.dumps(summary, indent=2)+'\n')
print(json.dumps(summary, indent=2))
