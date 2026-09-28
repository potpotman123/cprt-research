# Age composition versus changes within age groups

28 September 2026. Recomputed an existing repository finding rather than collecting new data. Used CCC Crash Course 2026 Figures 18 and 19 for CY2022–2025. Both stored chart images were inspected. The spreadsheet skill's read-only analysis conventions were used; no workbook was created or edited. The small calculation is in `age_history.py`, with input hashes and all contributions in `age_history_results.json`.

## Direct evidence

Figure 19 reports total losses as a share of claims within six vehicle-age groups, all loss categories. These are age-group rates, not exact-age probabilities, collision-only rates or Copart's own rates.

| Age at claim | CY2022 | CY2024 | CY2025 | 2024–25 change, percentage points |
|---|---:|---:|---:|---:|
| Current year or newer | 9.2% | 9.7% | 9.6% | -0.1 |
| 1–3 | 8.9% | 10.2% | 10.7% | +0.5 |
| 4–6 | 13.3% | 15.4% | 15.7% | +0.3 |
| 7–9 | 19.1% | 22.8% | 23.4% | +0.6 |
| 10–12 | 26.5% | 31.5% | 32.3% | +0.8 |
| 13+ | 37.8% | 43.6% | 45.3% | +1.7 |

The rate rose in all six groups from 2022 to 2025 and five of six from 2024 to 2025. Moving more claims between these six groups cannot alone explain these within-group changes. This does not hold exact age, vehicle model, damage, insurance coverage or carrier mix constant.

Example: in a normalized population of 10,000 claims involving 7–9-year-old vehicles, the reported rates correspond to 2,280 totals in 2024 and 2,340 in 2025. The extra 60 is a same-claim-count illustration, not an observed increase in counts. Actual claim volumes could fall enough for totals to decline despite the higher rate.

## Conditional aggregate decomposition

Figure 18 gives shares of total-loss valuations by age. If its population is compatible with Figure 19, implied claim weights are proportional to valuation share divided by the corresponding total-loss rate. Normalize those six quantities to sum to one. This is an inferred claim distribution, not the registered fleet distribution or independently observed insured exposure.

Overall rate is the sum of each claim weight times its age-group total-loss rate. To separate changes, use the symmetric decomposition: age-mix effect is the change in weights times the average of starting/ending rates; within-group effect is the change in rates times the average of starting/ending weights. This divides the interaction equally and reconciles exactly to the reconstructed change. It is an accounting decomposition, not causal identification.

| Window | Age-mix effect | Within-group effect | Reconstructed total change | Figure 19 total change |
|---|---:|---:|---:|---:|
| 2022–2025 | +0.329 pp | +3.834 pp | +4.163 pp | +4.300 pp |
| 2023–2024 | +0.162 pp | +1.904 pp | +2.066 pp | +2.100 pp |
| 2024–2025 | +0.027 pp | +0.683 pp | +0.710 pp | +0.800 pp |

The reconstruction differs from the reported total by +0.057 pp in 2022, +0.044 in 2023, +0.010 in 2024 and -0.080 in 2025. The 2024–25 change therefore leaves approximately 0.090 pp unreconciled, larger than the estimated age-mix contribution. Possible rounding and population/methodology differences are not separately identified. CCC warns that its age calculation is a proxy and is not exactly comparable to its other reporting. Do not force the residual into age or within-age economics.

Thus the defensible result is that **changes within broad age groups dominate this recent reconstruction**. An exact statement that 96% of actual industry growth is economic rather than demographic is too strong. Earlier repository descriptions that the close tie “validates” the population match, or that fleet aging is permanently “over,” should not be used. Those conclusions are superseded here.

CY2020 is deliberately outside this calculation: previous notes disagree about the 10–12-year label. No override or source edit is needed for the recent-period finding.

## Competing explanations and the tests they require

| Explanation | Mechanism | Evidence that distinguishes it |
|---|---|---|
| Repair-versus-value economics | At a comparable damage level, repairs become expensive relative to pre-loss value less expected net salvage, crossing the totaling threshold. Lower ACV or higher expected salvage can also move the threshold. | Matched age/body/condition repair estimates, pre-loss values and salvage, with claim/disposition populations defined. Repairable-only average costs do not identify repair costs for vehicles totaled. |
| Fewer small claims reported | Higher deductibles or reduced coverage remove inexpensive repairable claims from the denominator. Total-loss share rises even if total-loss counts do not. | Compatible repairable and total-loss counts, coverage/deductible composition and frequency; do not infer counts from TLF alone. |
| Different vehicles or accidents within an age group | A 7–9 group shifts toward age 9, different body types or more damaging incidents. The 13+ category is particularly broad. | Exact-age composition or narrower age groups, body mix, loss cause and damage mix. Broad buckets cannot rule this out. |
| Carrier/process mix | Different insurers, thresholds, catastrophe exposure or claim practices change the observed pool. | Consistent carrier/loss-category panels or transparent controls. Do not assign all of the residual to repair inflation. |

The data establish the need for a time-varying within-group rate. They do not select one explanation yet, and they do not establish a long or short forecast.

## Architecture implications

1. The fleet/coverage/claim-frequency calculation produces claim counts by age and body. Its age mix is one input, not a substitute for total-loss economics.
2. The damage-selection engine produces time-varying total-loss probability within those groups and the auction-value distribution of selected vehicles. Fit the historical reference once; do not recalibrate every new shock away.
3. Include claim-selection changes in claim counts or the conditional damage distribution as appropriate. If smaller claims disappear from the modeled denominator, do not also add an independent TLF uplift for the same event.
4. Multiply claim counts by totaling probability, auction eligibility and allocation, then apply timing. Pass the selected sale-price distribution through the fee schedule to obtain core revenue. A rate uplift cannot be converted directly into identical RPU growth.
5. Use the available annual CCC histories as validation targets. Do not repeat the 2024–25 increase mechanically into FY27 quarters, relabel annual calendar rates as fiscal-quarter observations, or add a second broad TLF-growth adjustment on top of the modeled mechanisms.

Priority now is a cheap inventory of already-held claims-frequency/claim-count and repair/vehicle-value history, with population and period alignment. That determines whether the main historical movement resembles a changing economic threshold, changing claims selection, or remains unresolved. Fine single-age interpolation comes after that test; smoother curves alone cannot identify the cause.

## Sources and verification

- `raw/ccc/img/cc2026_fig19_tl_share_by_age.png`: directly reported rates and methodology warning.
- `raw/ccc/img/cc2026_fig18_tl_valuations_by_age.png`: total-loss valuation composition.
- `data/csv/ccc_tl_share_by_age_2020_2025.csv` and `ccc_tl_valuation_share_by_age_2020_2025.csv`: existing transcription; recent-year inputs agree with inspected labels.
- CCC source page stored at `raw/ccc/crash-course-2026.html` and `.txt`; original https://www.cccis.com/reports/crash-course-2026.

Checks: normalized claim weights sum to one; symmetric contributions reproduce reconstructed changes to numerical tolerance. No population compatibility, causal effect or future growth claim is validated by those arithmetic checks. No production model inputs, shared raw tables or workbooks changed.
