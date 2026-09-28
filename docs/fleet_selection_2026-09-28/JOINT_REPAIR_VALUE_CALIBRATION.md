# Joint repair/value calibration feasibility

2026-09-28. Existing inputs only; no downloads, OCR, paid resources, workbook edits or production forecast changes. `joint_calibration.py` reproduces `joint_calibration_results.json`. Input hashes retained. This is a conditional calibration exercise, not a new empirically validated base case.

## Historical alignment

Body weights within each age bucket use CY2025 model births (`births[2]`), survival and the existing relative claim weights. These are modeled claim weights, not observed insurance claims. Two alternative age-weight methods were compared:

1. CY2025 model claim weights.
2. Conditional CCC CY2025 age weights, proportional to total-loss valuation age share divided by age-specific TLF. This requires compatible chart populations. As earlier documented, the reconstructed aggregate TLF does not exactly reconcile; these weights are a diagnostic, not newly measured claims. Body weights remain modeled under either approach.

Repairable means are aggregated using claim weight × (1 − age-specific TLF), not fleet weights or total-loss weights. Reference means: $5,721 for ages 0–6 and $3,682 for ages 7+, from saved `raw/ccc/crash-course-2026.txt`, line 277. The older mean is derived from the reported $2,039 gap. Reference URL: https://www.cccis.com/reports/crash-course-2026. Rates use the existing six CCC2025 age targets.

## Method

Preserve the four body repair/value ratios, the age-value slope, and the assumed salvage recovery curve. Let damage rank u range from zero to one. Repair bill = exp(mu + sigma × normal quantile(u)); recovery fraction = 0.4 − 0.2u. Net salvage is 96% of hammer value. The total-loss threshold is ACV × (0.616 + 0.192u).

Solve the continuous crossing for each cohort; integrate repair bills analytically below it using the truncated lognormal first moment. The crossing is unique for the tested dispersions: the derivative of log repair with rank exceeds the derivative of log threshold. This avoids the old nine-state threshold approximation. First fit six age-specific repair medians to six TLF targets for each assumed dispersion. Then compute the two selected-repairable means.

Scaling both ACV and the repair distribution equally leaves all total-loss probabilities unchanged and scales selected repair bills proportionally. Consequently each mean identifies a required common scale *conditional on dispersion and all other assumptions*. Solve for the dispersion where both age groups require the same scale.

## Findings

At the existing dispersion of 1.5702, the required scales are:

| Weights | Ages 0–6 | Ages 7+ |
|---|---:|---:|
| Conditional CCC age weights | 1.469× | 1.513× |
| CY2025 model weights | 1.474× | 1.530× |

Historical alignment therefore does not remove the low modeled repair means. No single common scale at the existing dispersion matches both group means exactly.

Allowing dispersion to move produces exact conditional fits:

| Weights | Fitted dispersion | Common ACV/repair scale | Implied age-ten car ACV |
|---|---:|---:|---:|
| Conditional CCC | 1.795 | 1.694× | $16,938 |
| CY2025 model | 1.855 | 1.762× | $17,624 |

All six total-loss rates reproduce to within 1e-9 probability; both repair means reproduce to within one cent. This precision is numerical only. There are eight fitted parameters (six medians, dispersion, scale) for eight targets. These are in-sample fits, not out-of-sample validation. Real parameter uncertainty is substantially larger, including the recovery curve, body ratios, age-value slope and claims-population mismatch.

The age-ten car values are well above the old $10,000 assumption. An existing convenience check of 2016 Camry/Accord dealer-retail prices averaged $13,695, but that is not matched insurer ACV or a representative car fleet. It is a reason to seek better value anchoring, not a proof these fits are impossible. See `../repair_research_2026-09-26/value_recovery_audit/README.md`. Do not adopt the fitted values merely because they close the equations.

## Response identification

A 5% repair-cost increase gives approximately +4.0% units under the original dispersion, versus +3.35% to +3.49% under the joint fits. Common scaling does not affect this relative unit response. The unit effect is smaller by about one-sixth under these fits; this is conditional and not an empirical revision.

The deliberately broad diagnostic dispersion grid (0.6, 0.9, 1.2, 1.5702, 2.0) can match all six TLFs yet produces +3.1% to +11.7% unit responses to the same 5% repair shock. Those grid cases do NOT all fit both repair means and are NOT plausible confidence bounds. They demonstrate why matching TLF alone was inadequate.

ASP responses were calculated under the same proportional recovery function, but no new fee/RPU or revenue forecast is adopted. Rescaling vehicle values would move fees between brackets, requiring a fresh fee integration and anchor review. Quoting the earlier +4.45% revenue sensitivity as robust after this calibration would be inappropriate.

## Decision and next useful evidence

Retain the original model as a labeled working case and archive both joint fits as alternatives. The repair/value engine now has a second calibration requirement, proper repairable weights, and an explicit identification diagnostic. It does not yet have a validated repair-cost elasticity.

Next priority: independently anchor pre-loss ACV by age for the claims population, and distinguish observed repairable costs from fitted latent bills. First inspect existing CCC AAVV age data and ask whether they describe already-selected total losses. If they do, compare them with model-selected total-loss ACV, not with unconditional exposure ACV. A compatible selected-value target can test the common scale without pretending auction-selected values describe every insured vehicle. Use a small local evidence check before acquiring any new panel. Reconsider recovery and value slope if these outputs cannot jointly reconcile; do not conceal disagreement by adding unsupported cohort parameters.
