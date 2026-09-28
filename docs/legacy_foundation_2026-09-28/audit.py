"""Bounded existing-record audit. No workbook mutation or network access."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent
CONTROL = ROOT / 'data/csv/segment_service_rev_8k.csv'
VALIDATION = ROOT / 'model/linked_service_revenue_2026-09-28/validation.json'
with CONTROL.open() as f:
    controls = list(csv.DictReader(f))
model = json.loads(VALIDATION.read_text())['quarter_results']
dates = ['2025-11-20', '2026-02-19', '2026-05-21', '2026-09-10']
# Explicit transcriptions from existing original call texts. None is missing, not zero.
us_rpu = [.075, None, None, None]
intl_rpu = [.081, .076, .105, .035]
us_total_units = [-.079, -.095, -.042, -.057]
us_ins_units = [-.095, -.107, -.042, -.075]
intl_total_units = [None, None, .059, .10]
rows = []
for i, c in enumerate(controls):
    for region, rpus, totals in [('us', us_rpu, us_total_units), ('intl', intl_rpu, intl_total_units)]:
        revenue = float(c[f'{region}_service_k']) / 1000
        prior = float(c[f'prior_{region}_service_k']) / 1000
        rg = revenue / prior - 1
        rpu = rpus[i]
        fg = None if rpu is None else (1+rg)/(1+rpu)-1
        implied_rpu_on_total_units = None if totals[i] is None else (1+rg)/(1+totals[i])-1
        # RPU disclosure rounded to nearest 0.1 percentage point, conditional tolerance.
        lower = None if rpu is None else (1+rg)/(1+rpu+.0005)-1
        upper = None if rpu is None else (1+rg)/(1+rpu-.0005)-1
        rows.append(dict(period=f'FY26Q{i+1}', region=region, service_musd=revenue,
            prior_service_musd=prior, service_yoy=rg, disclosed_fee_rpu_yoy=rpu,
            inferred_fee_units_yoy=fg, inferred_fee_units_low=lower, inferred_fee_units_high=upper,
            disclosed_total_units_yoy=totals[i],
            service_per_total_unit_yoy_NOT_fee_rpu=implied_rpu_on_total_units,
            source=f'raw/transcripts/call_{dates[i]}.txt',
            status='Inferred fee units require matching service/RPU scope; total units not substituted'))
        if fg is not None:
            assert abs(prior*(1+fg)*(1+rpu)-revenue)<1e-8

def write_csv(name, records):
    with (OUT/name).open('w') as f:
        w=csv.DictWriter(f, fieldnames=records[0].keys(), lineterminator='\n'); w.writeheader(); w.writerows(records)
write_csv('historical_controls.csv', rows)

residuals=[]
for i,c in enumerate(controls):
    q=model[i]; actual=float(c['us_service_k'])/1000
    share_only=model[3]['insurance_m']*q['share']/model[3]['share']+model[3]['other_us_m']
    modeled=q['insurance_m']+q['other_us_m']
    residuals.append(dict(period=f'FY26Q{i+1}', actual_us_service_musd=actual,
        modeled_insurance_musd=q['insurance_m'], assumed_other_us_musd=q['other_us_m'],
        modeled_us_musd=modeled,residual_musd=modeled-actual,
        other_us_needed_if_insurance_model_held_fixed_musd=actual-q['insurance_m'],
        insurance_model_units=q['units'], modeled_insurance_rpu=q['rpu'],
        allocation_only_us_musd=share_only,
        residual_after_removing_fleet_and_rpu_change_musd=share_only-actual))
write_csv('historical_residuals.csv',residuals)

# Conditional composition check: identical insurance/noninsurance/total populations required.
prior_weight=(-.057-.002)/(-.075-.002)
current_weight=prior_weight*(1-.075)/(1-.057)
relative_rpu_for_90pct_dollars=.9/.1*(1-current_weight)/current_weight
intl_actual=sum(float(c['intl_service_k'])/1000 for c in controls)
intl_flat=[model[4+i]['intl_m'] for i in range(4)]
intl_seasonal=[float(c['intl_service_k'])/1000 for c in controls]
summary={
 'us_q4_conditional_prior_insurance_unit_weight':prior_weight,
 'us_q4_conditional_current_insurance_unit_weight':current_weight,
 'insurance_to_other_rpu_needed_for_90pct_dollar_share_IF_fee_scope_matches':relative_rpu_for_90pct_dollars,
 'historical_us_residual_sum_musd':sum(r['residual_musd'] for r in residuals),
 'historical_us_absolute_residual_sum_musd':sum(abs(r['residual_musd']) for r in residuals),
 'historical_modeled_insurance_units_sum':sum(q['units'] for q in model[:4]),
 'flat_q4_international_fy27_yoy':sum(intl_flat)/intl_actual-1,
 'flat_q4_international_h1_yoy':sum(intl_flat[:2])/sum(intl_seasonal[:2])-1,
 'repeat_prior_year_intl_instead_of_flat_q4_h1_delta_musd':sum(intl_seasonal[:2])-sum(intl_flat[:2]),
 'repeat_prior_year_intl_instead_of_flat_q4_fy27_delta_musd':sum(intl_seasonal)-sum(intl_flat),
 'note':'Repeat-prior-year international is a diagnostic, not adopted forecast or evidence of seasonality alone.',
 'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [CONTROL,VALIDATION]+[ROOT/f'raw/transcripts/call_{d}.txt' for d in dates]},
 'checks':'Service identities reconcile; Q4 international inferred fee-unit interval overlaps disclosed 11.5% rounded interval.'
}
q4=rows[-1]
assert max(q4['inferred_fee_units_low'],.1145)<=min(q4['inferred_fee_units_high'],.1155)
assert abs(residuals[3]['residual_musd'])<1e-8
(OUT/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='source_hashes'},indent=2))
print('Fee-unit inferred growth:',[(r['period'],r['region'],r['inferred_fee_units_yoy']) for r in rows])
