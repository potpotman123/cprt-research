# Revised age-constrained repair/value engine

2026-09-28. Executable research revision and Fable handoff, using existing sources only. `age_constrained_engine.py` writes `age_constrained_engine_results.json`; no workbook design or legacy dollar forecast overwrite.

## Revision

Replace the single cross-age value curve with three independently constrained young-age levels (current year, 1–3, 4–6) and a constrained 7+ aggregate. Match **selected total-loss values**, not unconditional exposure values. Model body ratios and selection are applied before comparing with each CCC value. The original .10 log-depreciation slope remains only within the three older buckets; one common scale constrains their combined selected value to $9,122. This older internal shape remains an assumption.

Use the four CCC through-October 2025 non-comprehensive total-loss mix weights. Split the 7+ weight using annual all-loss shares 20.9:19.9:31.8. Infer relative claim weights by dividing resulting total-loss weights by the six CCC2025 age TLFs. This is an explicit hybrid-population calibration, not a newly observed claims distribution. Body-within-age weights retain CY2025 modeled exposures/relative claim weights.

For each candidate dispersion, fit six repair medians to TLF. Scale each young age bucket's repair distribution and ACV together to its selected-value target. Apply one common scale to older buckets. These paired scalings preserve TLF. Then fit two dispersions to the average bill among repaired vehicles: one for ages 0–6, one for 7+. Repairable means use claims × (1−TLF) weights and truncated lognormal moments.

## Reconciliation

| Target | Source value | Revised model |
|---|---:|---:|
| Current-year selected AAVV | $40,187 | $40,187 |
| Age 1–3 selected AAVV | $30,259 | $30,259 |
| Age 4–6 selected AAVV | $20,328 | $20,328 |
| Age 7+ selected AAVV | $9,122 | $9,122 |
| Age 0–6 repaired mean | $5,721 | $5,721 |
| Age 7+ repaired mean | $3,682 | $3,682 |

Six age TLF targets also match. All of these are calibration targets now; they are not held-out validation. Parameters: six medians, four value levels/scales, and two dispersions for twelve targets. Exact in-sample agreement is expected, not evidence of certainty.

Selected value source: CCC Q4 2025 Figure 6 through October; prior saved image and transcription in `age_value_holdout_results.json`. Repair means and TLF: CCC annual 2026 report, CY2025 all-loss definitions; source files retained in repository. Coverage/period discrepancies are unresolved. The four observed age values and mix imply ~$13,706, versus chart aggregate $13,700 due rounding; do not additionally force the December $13,610 aggregate onto October constraints.

## Why two dispersions

Fitted log-repair dispersions: 1.25154 for younger vehicles; 0.91509 for older vehicles. A single dispersion fitted to younger bills produces only $2,962 for older repaired vehicles. A single dispersion fitted to older bills produces $7,589 for younger vehicles. Thus one shared spread does not reconcile these targets under the retained assumptions. Separate spreads are a transparent fitted degree of freedom, not observed evidence that older vehicles intrinsically have less variable crash damage.

## Conditional economics

Fixed calibrated historical claim weights, carrier allocation and service assumptions; no refitting after shocks. Core auction service revenue uses inherited buyer fee schedules, 50/50 buyer mix, virtual fee, $110 fixed amount and 4% seller fee. Ancillary service adoption is excluded.

| Uniform hypothetical shock | Units | Core RPU | Core revenue |
|---|---:|---:|---:|
| Repair bills +5% | +6.48% | +0.53% | +7.05% |
| Pre-loss ACV +5% | -6.27% | +1.79% | -4.60% |
| Both +5% | 0.00% | +2.30% | +2.30% |

These are diagnostic responses, not forecasts, confidence limits, consolidated revenue effects or consensus deltas. Larger repair sensitivity than earlier fits is a consequence of fitted distributions, not new observed elasticity evidence. More repair cost can admit marginal higher-recovery cars to auction; it does not imply worsening damage raises the price of the same car.

## QA and implementation

Continuous damage cutoff solved by bisection; analytical selected repair means and ASP. Fee schedules integrated over selected damage ranks at 2,048 points; doubling to 4,096 changes baseline core revenue by 0.00035%. Checked TLF within 1e-9, mean/value targets within one cent, revenue = units × RPU, and common repair/value scaling leaves units unchanged. Runtime around 1.5 seconds. No scrape, new download, OCR or paid resource.

JSON supplies the six age cohort `car_ACV`, `log_car_repair_median` and `sigma` parameters, body ratios/weights, relative claim weights, validation outputs, and scenarios. For Fable, consume this revision as a separate research component; keep assumptions/evidence separate from the engine and summary. For a quarterly forecast, freeze these calibration parameters, propagate actual cohort mix and explicitly forecast economic drivers; do not refit to a desired quarterly revenue target.

## Remaining restrictions

Single value per age/body cohort, unverified within-7+ curve, transferred repair/body ratios, assumed recovery decreasing from 40% to 20% with damage rank, inferred claim weights, and coverage mismatch. Seller net costs beyond the inherited 4% treatment are not newly measured. The model is now constrained by more observed outputs, but its response to future shocks still requires validation. The revision is ready for further research integration; it is not a certified replacement for the full quarterly revenue forecast.
