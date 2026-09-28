"""Small conditional identities; no network, dependencies or workbook changes."""
import json
from pathlib import Path

cost_increase = 17_000_000  # Company call: YoY delivery-related facility cost.
margin = 0.20  # Analyst industry analogy, not measured Copart margin.
conditional_revenue = cost_increase / (1 - margin)
price_cases = []
for price in (300, 600, 900):  # Illustrative; not quotes or an empirical range.
    jobs = conditional_revenue / price
    price_cases.append({
        "assumed_revenue_per_vehicle": price,
        "conditional_additional_deliveries": jobs,
        "penetration_change_pp_if_1m_eligible_and_other_factors_constant": jobs / 1_000_000 * 100,
    })
    assert abs(jobs * price - conditional_revenue) < 1e-6

waiver_cases = []
for fraction in (0, 0.5, 1):
    added_billings = 10_000 * 300
    waived_gate = 10_000 * fraction * 95
    net = added_billings - waived_gate
    waiver_cases.append({"assumed_waiver_fraction": fraction,
                         "added_billings_usd": added_billings,
                         "waived_gate_usd": waived_gate,
                         "net_addition_before_other_offsets_usd": net})
assert [x["net_addition_before_other_offsets_usd"] for x in waiver_cases] == [3_000_000, 2_525_000, 2_050_000]

result = {
    "status": "Conditional arithmetic only; no adopted forecast or measured adoption",
    "conditional_revenue_increase_usd": conditional_revenue,
    "price_identification_cases": price_cases,
    "separate_waiver_cases_do_not_automatically_overlay_cost_bridge": waiver_cases,
    "checks": "Revenue/job identities and waiver arithmetic passed",
}
Path(__file__).with_name("delivery_identification_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
