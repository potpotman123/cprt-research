# Did higher total-loss frequency mean more total-loss activity?

28 September 2026. Continued the existing-file check; no collection, OCR, new regression or Excel work. Source is the locally saved CCC Crash Course 2026 text. A live web check returned 403, so the findings below rely on the preserved source, not a newly fetched page. Source hash and reproducible arithmetic are in `claims_count_results.json` and `claims_count_check.py`.

## Directly reported CY2025 versus CY2024 observations

| CCC measure | All loss categories | Non-comprehensive |
|---|---:|---:|
| Total-loss share of claims, 2024 | 22.3% | 22.9% |
| Total-loss share of claims, 2025 | 23.1% | 23.9% |
| Total-loss valuation volume change | -2.9% | -0.2% |
| Repairable claim volume change | -9.7% | -8.0% |

Source: `raw/ccc/crash-course-2026.txt`, lines 183–184 (valuation volume and TLF), line 264 (repairables). Original URL: https://www.cccis.com/reports/crash-course-2026. The text explicitly characterizes filing behavior as affecting the ratio. It does not establish that all the repairable decline was caused by deductibles or affordability.

This is substantially more informative than multiplying a Progressive frequency series by industry TLF: **reported TLF increased while the reported valuation-volume proxy declined.** Non-comprehensive valuations were approximately flat, although their corresponding reported TLF rose one percentage point. These are CCC valuation counts, not independently verified unique totaled vehicles, completed settlements, auction assignments, or Copart sold units. The results describe 2025, not a forecast for FY27.

## Population compatibility test

For a common exhaustive claim population, `TLF = total losses / (total losses + repairables)`. Normalize 2024 total claims to 100 purely for arithmetic and apply the reported category count changes. If valuation counts measured exactly the total-loss numerator and repairable counts measured its complementary denominator, the two series would reproduce 2025 TLF.

They do not:

| Scope | TLF calculated from the two count changes | Reported TLF | Difference |
|---|---:|---:|---:|
| All loss categories | 23.583% | 23.1% | +0.483 pp |
| Non-comprehensive | 24.368% | 23.9% | +0.468 pp |

This is too large to silently treat the figures as an exact reconciliation. Possible differences include valuations versus claims flagged total loss, reporting samples, timing, development or definitions; this test does not identify which. Do not force a balancing adjustment or assume duplicates explain it without evidence.

Using all-category repairable decline and the reported TLF instead would imply total-loss counts down 5.49%, rather than the reported valuation proxy down 2.9%. Non-comprehensive would imply -2.72% rather than -0.2%. These are **incompatible conditional identities**, not alternative equally valid forecasts or an empirical uncertainty interval.

## What the evidence distinguishes

The old interpretation that a higher TLF necessarily creates more auction supply fails. These disclosures are consistent with repairable activity contracting faster than total-loss activity. They do not rule out genuine economic-threshold changes at the same time: repair/value economics could produce additional totals relative to a counterfactual while aggregate volume still declines.

Similarly, the prior within-age-group finding does not prove more severe crashes or repair inflation. Removing small claims within an age group raises that group's measured TLF even with an unchanged damage distribution among all accidents. Exact age/body/carrier/coverage changes may also contribute. The all-category and non-comprehensive differences warn against treating catastrophe-sensitive comprehensive activity as a stable collision proxy.

## Claims architecture decision

Use a consistent claim definition at every stage:

`covered vehicle exposure × accident/incident incidence × probability the event generates a recorded relevant claim = modeled claims`

`modeled claims × total-loss probability conditional on that recorded population = total losses`

The filing probability can depend on damage severity. Raising a deductible can remove minor claims; the remaining claims then have a different severity distribution. The damage-selection engine must calculate both denominator and total-loss numerator from that selected distribution, rather than multiplying unrelated aggregate forecasts and independently adding a deductible TLF uplift.

When the available input is already **reported claims frequency per earned vehicle-year**, it already includes filing/coverage/sample effects in that series. Multiply by compatible exposure to obtain claims; do not add a second filing-rate multiplier for the same mechanism. An exposure count is needed: a carrier with falling frequency can still have more claims if insured exposure expands. Premium growth or raw policy counts are imperfect substitutes for matching covered earned vehicle-years.

Keep three evidence series separate for validation: CCC valuation-volume changes; CCC TLF; and industry/carrier claims-frequency changes. Mark mismatched populations, coverages and calendar/fiscal periods. Do not force all three to tie or treat Progressive alone as industry frequency.

For scale only, 22.3% to 23.1% TLF requires matching total claim counts to decline by less than 3.46% for total-loss counts to grow. The non-comprehensive break-even is -4.18%. This follows from the identity `(1 + claims growth) × TLF_new / TLF_old`; it is not an observed claim-count estimate.

## Next useful test

Inventory the existing repair-cost and pre-loss-value history by period and population. Check whether their directions support a changing economic threshold alongside claim selection. Keep the observed age-rate history as a validation target. A relationship between broad price indices and TLF does not identify a repair premium or its causal coefficient, but can reject inconsistent explanations before investing in more granular data.

No forecast-input changes yet. The immediate improvement is the claim-population contract and three independent validation targets. Remaining gaps are compatible claim counts/exposures and evidence on damage-dependent filing. The model should state assumptions where those remain unavailable.
