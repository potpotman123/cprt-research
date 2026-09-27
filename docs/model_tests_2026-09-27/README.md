# Cheap revenue-driver, composition and selection tests

Executed 27 September 2026. User authorized the simple tests and asked which current assumptions affect revenue most. No new collection, OCR, paid data, Excel redesign or external forecast retrieval. The production workbook is unchanged. These are model diagnostics, not new empirical estimates.

## Inputs, provenance and reproducibility

Run `python3 docs/model_tests_2026-09-27/run_tests.py` from the repository using Python with openpyxl available. The script runs the existing read-only workbook validator, reuses its numerical primitives and independently reconstructs the current model with parameter overrides. The validator refreshes its identical validation JSON. The input snapshot is `model/service_revenue_2026-09-27/model_inputs.json`; its SHA256 is recorded in results.json. The source populations and assumptions remain those in the current research handoff and model README. All outputs here use $millions, except explicitly labeled ratios and probability shifts.

No data were fitted beyond the existing CCC bucket calibration. Runtime was below one second locally. Twenty-four existing-input cases, four composition worlds, two forecast-only TLF shocks, two forecast-only value shocks and twelve deterministic severity scenarios were evaluated. Scenario endpoints are diagnostic choices, not confidence intervals or equally plausible shocks. No claim of a universal largest driver is possible without specifying the allowed changes.

## 1. Existing-input sensitivity

Baseline H1 FY27 service revenue is $1,970.6114m. Each input changes alone. Structural parameters change throughout modeled history and forecast, with the workbook's 2025 CCC bucket calibration repeated. Reported historical company revenue is never changed. Forecast growth controls change only projected quarters.

| Assumption and specified change | H1 service revenue change, $m |
|---|---:|
| US baseline growth -1 / +1 percentage point | -16.743 / +16.743 |
| International baseline growth -1 / +1 percentage point | -2.689 / +2.689 |
| CY26 and CY27 births compound -10% / +10% annually from CY25 | -1.555 / +1.557 |
| Claim-age decay -20% / +20% | +0.169 / -0.154 |
| SUV/car ACV 1.20x / 1.80x versus 1.50x | -0.060 / +0.111 |
| All LT repair costs -10% / +10% | +0.060 / -0.055 |
| Common gross salvage recovery 25% / 35% versus 30% | +0.091 / +0.088 |
| Insured-service exposure 80% / 100% versus 90% | +0.076 / -0.076 |

Additional dispersion, survival, value-level and seller-fee tests are in results.json. Fee bands are nonlinear, so up/down changes need not have opposite signs. The large effect of US growth is mechanical: it applies to the whole US dollar base. The smaller economic-input effects do not show those inputs are unimportant to actual auction economics. They show that permanent level differences largely cancel in this specific history-to-forecast growth bridge, while calibration absorbs some changes into the starting probabilities. A uniform change in all bodies' repair costs would cancel in the relative-cost calibration; it is not represented as a new within-cohort repair-inflation shock.

## 2. Exact composition attribution

Factor each quarterly fleet as total vehicles N(t) times age distribution P(age,t) times conditional body distribution P(body|age,t). Quarterly cells are the same monthly-midpoint interpolation of annual stocks used by the workbook. Freeze either distribution at Q4 FY26 for all modeled periods, including the year-ago comparisons; allow N(t) to change in every world. Hold claims, calibration, probabilities and fees at their baseline values. Recompute each world's own reference-quarter and forecast growth before applying the existing dollar bridge.

This is a statistical counterfactual, not a physically possible fleet roll. It isolates age and body-within-age rather than claiming a unique causal decomposition. The conditioning order matters. A separate residual preserves the age/body and bridge interactions rather than silently assigning them to one driver.

| Contribution relative to the mechanical revenue baseline | Q1 FY27 $m | Q2 FY27 $m | H1 $m |
|---|---:|---:|---:|
| Fleet size only | +0.02149 | +0.03966 | +0.06115 |
| Age distribution, holding conditional body mix fixed | -0.30365 | -0.58105 | -0.88470 |
| Body distribution within age, holding age mix fixed | +0.02810 | +0.05415 | +0.08225 |
| Interaction | +0.01962 | +0.03810 | +0.05772 |
| Total incremental fleet adjustment | -0.23443 | -0.44915 | -0.68359 |

Thus body mix is not the source of the negative incremental H1 adjustment in this implementation. That is not proof that replacing cars with SUVs increases the level of revenue per claim: a structural adverse level effect can coexist with a positive change relative to an already-adverse reference growth rate. All four quarters, unit growth and RPU growth by world are retained in results.json. The full-changing world exactly reconstructs the baseline.

## 3. Timing and calibration tests

To demonstrate what the current permanent-input sensitivities omit, freeze historical calibration and introduce new economics only in FY27. These are extensions to the diagnostic script, not existing workbook controls or adopted forecasts.

- Add/subtract one absolute percentage point to every age/body total-loss probability in forecast quarters only, with fees and exposure fixed: H1 services change +/-$74.472m. A 0.1-point shock scales to +/-$7.447m while probabilities remain interior. Holding fees fixed deliberately omits any change in the salvage values of the newly selected vehicles.
- Change SUV/car ACV only in the forecast from 1.50x to 1.20x: H1 services rise $59.023m. Change it to 1.80x: services fall $55.129m. Car latent severity calibration, SUV repair bills and recovery fractions stay fixed; SUV sale proceeds change with value. This is an immediate 20% relative-value move, not evidence that such a move is plausible. Lower value increases totaling enough to outweigh lower modeled fees in this test.

The same numerical change can therefore answer two entirely different questions: was our historical cross-sectional ratio wrong, or will economics change after the calibration date? Recalibrating new forecast-period shocks back to unchanged historical TLF targets would erase the mechanism being tested. Conversely, treating a revised estimate of a longstanding ratio as a sudden shock would manufacture a catalyst.

## 4. Damage selection illustration

Use one age-10 car/SUV comparison. Car ACV=$10,000; SUV/car ACV=1.20x or 1.50x; repair ratios are the existing working-case values. Construct an illustrative latent lognormal repair distribution with inherited sigma, calibrated ONCE so the car at constant 30% gross recovery reproduces baseline age-10 car TLF. This is not an observed repairable histogram and is not an empirical latent distribution. Apply the same severity quantile to both bodies, scaled by their repair-cost ratio.

For severity rank u, gross salvage/ACV = 0.30 + slope*(0.5-u). Slopes 0, 0.2 and 0.4 imply constant 30%, roughly 20–40%, and roughly 10–50% recovery. Higher-severity claims get lower recovery. The unconditional mean across all hypothetical accident severities remains 30%, but the mean among totaled vehicles changes. Total if repair cost > ACV - bid*(1-seller fee). Compute the actual fee schedule at three bid nodes conditional on each severity, using the existing seller rate. The same residual bid dispersion convention applies to both bodies.

| Severity/recovery slope | SUV/car ACV | SUV/car service revenue per accident exposure |
|---|---:|---:|
| 0 (constant recovery) | 1.20x | 0.9533x |
| 0.2 | 1.20x | 0.9428x |
| 0.4 | 1.20x | 0.9261x |
| 0 (constant recovery) | 1.50x | 0.8822x |
| 0.2 | 1.50x | 0.8597x |
| 0.4 | 1.50x | 0.8236x |

This demonstrates a possible channel for stronger negative per-exposure economics. It is not a forecast of the fleet effect. Changing the slope changes both selected recovery levels and the totaling decision; this is not a covariance-only experiment holding selected means constant. Demand differences, body-specific repair-severity distributions and recovery functions remain unmeasured. Aggregate composition and changes over time still determine materiality.

## Checks and decision

- Baseline matches the independently validated workbook within $0.0000001m per quarter.
- Full composition world reconstructs baseline; four components sum to each quarter's adjustment within $0.00000001m.
- Damage quadrature used 2,001 then 8,001 equal-probability midpoint nodes. SUV/car revenue ratios differed by less than 0.003x. This is numerical convergence, not sampling precision.
- No production Excel formulas or assumptions were changed. No empirical claims were upgraded based on the scenarios.

Priority: replace the undifferentiated US-growth carry-forward with an evidenced explanation of forward changes in claims, TLF and allocation; distinguish that work from refining permanent body-level differences. For the repair/vehicle mechanism, test historical within-age TLF changes against value/repair/recovery changes without refitting away those changes. The selection illustration justifies a bounded evidence search only if its plausible effect, multiplied by the actual near-term mix change, is material. Do not treat the larger hypothetical shocks as discovered downside or stack them on a baseline already containing the same effect. A dated comparable external forecast remains necessary to claim a revisions opportunity.
