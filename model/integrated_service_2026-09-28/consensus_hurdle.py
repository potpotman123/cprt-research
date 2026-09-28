"""Conditional revenue identity, not a forecast or inferred Street driver model."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def main():
    actuals = json.loads((ROOT / 'model/linked_service_revenue_2026-09-28/inputs.json').read_text())['actuals']
    with (ROOT / 'docs/consensus_review_2026-09-28/total_revenue_consensus.csv').open() as f:
        consensus = list(csv.DictReader(f))[:4]
    rows = []
    checks = 0
    # Ranges are transparent scenarios, not estimated bounds or probabilities.
    for share in [.8, .9, 1.0]:
        for other_growth in [0, .05]:
            for unit_growth in [-.05, 0, .05]:
                for indices, period in [([0], 'FY2027Q1'), ([1], 'FY2027Q2'), ([0, 1], 'H1FY2027')]:
                    insurance = sum(actuals[i]['us_service'] * share for i in indices)
                    other = sum(actuals[i]['us_service'] * (1-share) + actuals[i]['intl_service'] for i in indices)
                    purchased = sum(actuals[i]['us_vehicle'] + actuals[i]['intl_vehicle'] for i in indices)
                    target = sum(float(consensus[i]['total_revenue_mean_m']) for i in indices)
                    required_insurance = target - purchased - other * (1+other_growth)
                    rpu_growth = required_insurance / (insurance * (1+unit_growth)) - 1
                    reconstructed = insurance * (1+unit_growth) * (1+rpu_growth) + purchased + other * (1+other_growth)
                    assert abs(reconstructed-target) < 1e-8
                    checks += 1
                    rows.append(dict(period=period,assumed_insurance_fraction_us_service=share,
                        assumed_other_service_growth=other_growth,assumed_insurance_unit_growth=unit_growth,
                        prior_insurance_service_musd=insurance,required_insurance_RPU_growth=rpu_growth,
                        total_consensus_musd=target,reconstructed_total_musd=reconstructed))
    with (HERE / 'consensus_hurdles.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    print(json.dumps({'identity_checks':checks,'central_H1':[r for r in rows if r['period']=='H1FY2027' and r['assumed_insurance_fraction_us_service']==.9 and r['assumed_other_service_growth']==0]},indent=2))


if __name__ == '__main__':
    main()
