# Repair/value validation — 2026-09-28

Cheap existing-input audit; no acquisition, OCR, workbook edits or forecast replacement. Reproduction: `repair_value_check.py`; output: `repair_value_results.json`. Source JSON is hashed. Original nine-state units and RPU reproduce the saved validator.

## Main finding: TLF calibration does not validate repair economics

The linked engine fits six log-repair medians to CCC age-specific total-loss rates. It assumes a lognormal dispersion of 1.5702, car ACV of $10,000 at age ten with exponential depreciation, fixed body-value and repair ratios, and recovery declining from 40% to 20% with damage rank. Seller proceeds are 96% of hammer value. None of fitting the total-loss rates proves these separate quantities are correct.

We added an independent output check: integrate repair costs ONLY over states classified repairable, then divide by repairable counts. This is a truncated lognormal first moment, not the mean of the full latent damage distribution (which includes hypothetical bills for totaled vehicles). Cohort weights are fixed at FY26Q4; 2,048 damage intervals are used.

| Repairable population | Model mean | CCC CY2025 reference |
|---|---:|---:|
| Vehicles 0–6 years | $3,897 | $5,721 |
| Vehicles 7+ years | $2,407 | $3,682 |

CCC source: saved `raw/ccc/crash-course-2026.txt`, line 277; https://www.cccis.com/reports/crash-course-2026. Older mean is derived as $5,721 less $2,039. These references were already retained in repair_cost_reference/README.md. Different period, age/body weights, claim selection and coverage scope prevent calling the gap a matched-population residual. Nonetheless both age groups fall materially short. Do not resolve this by blindly raising all repair costs: without re-examining ACV/dispersion this would destroy the TLF calibration.

## Numerical check

Increasing damage intervals from nine to 2,048 changes core revenue level by approximately +0.14%, with units down approximately 0.06%. At 4,096 intervals core revenue differs from 2,048 by less than 0.001%. The baseline numerical error is small relative to economic-input uncertainty. This does not prove convergence for every future price shock. Keep the higher-resolution calculation as a research reference, not evidence that 2,048 states are economically observed. No need to expose thousands of rows in Fable's workbook.

## Equal-size economic shocks

Fixed FY26Q4 claims/exposure mix and allocation, no recalibration or dollar re-anchoring; core US insurance auction-service revenue only, excluding separately modeled services. Uniform 5% changes are diagnostic perturbations, not forecasts or confidence limits.

| Assumed change | Units | Core RPU | Core revenue |
|---|---:|---:|---:|
| Repair cost +5% | +3.99% | +0.44% | +4.45% |
| Repair cost -5% | -4.10% | -0.46% | -4.54% |
| ACV +5% | -3.90% | +1.82% | -2.15% |
| ACV -5% | +4.20% | -1.94% | +2.17% |
| Repair cost and ACV both +5% | 0.00% | +2.30% | +2.30% |

An ACV increase raises the assumed repair threshold while increasing auction prices for remaining total losses; in this parameterization the unit effect dominates. Higher repair costs admit marginal vehicles that were previously repairable. Their higher assumed recovery fractions can increase RPU. Thus this is NOT evidence that worse damage increases a given vehicle's price. Aggregate RPU also includes age/body selection. Fee schedules are evaluated for each state.

Common scaling of repair costs and ACV leaves units invariant under the model's proportional-recovery rule. This identity was checked, as was units × RPU = revenue. It exposes an identification problem: TLF alone cannot determine absolute repair/ACV scale. Independent value and repair-bill evidence is necessary.

## Priority for strengthening the build

1. Add selected repairable means as validation targets alongside TLF, maintaining their age, coverage and period labels. This check is now implemented in the research calculation.
2. Align historical claim weights/coverage as closely as existing evidence permits before fitting those means. Current forecast-quarter weights versus annual all-loss means are insufficient for a definitive calibration.
3. Then test whether the assumed ACV level and dispersion can jointly fit rates and repairable costs. Preserve multiple compatible fits if needed; do not present a fitted repair elasticity as measured.
4. Retain body-specific value ratios as proxies, with the two-model crossover panel and F150 panel limitations explicit. The older value audit declined to validate them fleet-wide; the linked model subsequently used them as working assumptions, not new evidence.
5. Keep salvage recovery separately identified from ACV. A higher value, stronger salvage recovery, and a higher repair bill can have different unit/RPU effects. Additional model granularity cannot substitute for evidence on these inputs.

The best next step is a small historical joint-calibration feasibility check, not broad scraping of itemized estimates. It should report which assumptions fit both outputs, whether fits imply implausible ACVs or dispersion, and how much their projected response differs. Existing model inputs remain untouched until this is assessed.
