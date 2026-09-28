# Within-age repair, value and claim-selection check

September 28, 2026. Existing local sources only, including one saved CCC chart visually inspected. Five bounded economic cases; no new scrape, paid source, optimizer, parameter fit or workbook. Production forecasts unchanged.

## 1. Historical age result rechecked

Reran `docs/fleet_selection_2026-09-28/age_history.py`. Results are unchanged: the conditional CY2024–2025 decomposition assigns +0.683 percentage points of TLF to changes within broad age groups and +0.027 points to changes between groups. The reconstructed increase is +0.710 points versus +0.800 reported, leaving +0.090 points unresolved. Claim weights are inferred from total-loss valuation shares divided by age-specific TLF; compatibility is assumed, not independently measured.

The finding supports looking beyond aging alone. It does not establish repair inflation as the cause: exact-age/body composition, claim reporting, coverage, damage and carrier mix can change within broad age groups.

## 2. Existing evidence and permitted use

| Input | Period/population | Finding | Permitted use and limit |
|---|---|---|---|
| CCC age TLF, Figure 19 | CY2024 and CY2025, all loss categories | Increases in five of six age groups | Historical validation targets, not forward assumptions |
| CCC repair means, annual text line 277 | CY2025 YoY, repaired vehicles | Current/newer −0.4%; ages 1–3 +1.9%; 4–6 +2.3%; 7+ approximately +1% | Selected repairable outcomes, not same-damage repair inflation across all incidents |
| CCC Figure 22, saved image | CY2025 vs 2024, noncomprehensive total-loss valuations | 7+ values −0.5%; overall $13,469 to $13,610; 0–6 described as higher | Selected valuation outcomes; broad 7+ change is not exact-age unconditional vehicle inflation |
| BLS repair and used-vehicle NSA indices, saved CSV | Matched months of CY2025 vs 2024 | Repair +6.129%; used vehicles +2.682% | Broad price proxies, not matched insurer repair costs/ACV |
| Same saved indices | Calendar Q2 2026 vs Q2 2025 | Repair +6.104%; used vehicles −2.150% | Observed index ratios; neither Copart fiscal-quarter inputs nor FY27 forecasts |
| CCC valuation and repairable counts | CY2025 YoY | All-category valuations −2.9%, repairables −9.7% | Evidence against equating rising TLF with growing counts; the series do not exactly reconcile |
| Salvage recovery by matched age/body/damage | No compatible history identified in current inputs | Missing | Keep a separate assumption; aggregate Copart ASP cannot be substituted as an exogenous recovery curve |

The BLS annual comparison uses eleven matched months, excluding October from both years because October 2025 repair CPI is missing. It is a ratio of matched-period average index levels, not an average of monthly percentage changes or a complete annual comparison. The recent calendar quarter contains all three months. Earlier summary CSV growth measures therefore need not have exactly the same values.

Sources: `raw/ccc/crash-course-2026.txt`, `docs/fleet_selection_2026-09-28/ccc_2026_figure22.webp`, `data/csv/ccc_tl_share_by_age_2020_2025.csv`, `data/csv/cprt_cpi_three_series.csv`. Figure 22 was visually rechecked, including the footnote saying older vehicles fell 0.5%. No live source refresh is claimed.

## 3. Economic tests: keep the 2025 calibration fixed and reconstruct 2024

The model is calibrated to 2025 age TLF and hybrid-period value/repair targets. We freeze those parameters and the calibration claim weights, then divide repair and value levels by the candidate growth factors to construct a 2024 comparison. This is a retrospective proxy test, not out-of-sample validation: the 2025 endpoint was calibrated, historical body and damage mix are held fixed, and source populations remain imperfectly aligned.

Three alternatives are kept separate:

1. **Broad indices:** apply repair +6.129% and vehicle value +2.682% uniformly. This produces a +0.977-point modeled TLF change at fixed calibration weights. That aggregate resemblance to the reported increase hides age-specific errors and repair-cost mismatch.
2. **CCC repairable means plus broad vehicle index:** transfer each reported repairable-mean increase directly to latent repair costs, retaining +2.682% value growth. This produces falling TLF in every age group, whereas five reported groups increased. This joint proxy specification fails the direction check. It does not prove that either individual series is wrong.
3. **Older-vehicle CCC pair:** for 7+ only, transfer approximately +1% repairable mean growth and −0.5% selected value growth to latent repair/value levels. Hold younger cohorts fixed in this diagnostic because no precise younger value-growth number was retrieved. This is a narrower source match, still not a matched constant-damage dataset.

| Age | Reported TLF increase, pp | Broad-index model, pp | Older CCC pair, pp |
|---|---:|---:|---:|
| Current/newer | −0.100 | +0.456 | Not tested |
| 1–3 | +0.500 | +0.495 | Not tested |
| 4–6 | +0.300 | +0.655 | Not tested |
| 7–9 | +0.600 | +1.186 | +0.542 |
| 10–12 | +0.800 | +1.422 | +0.648 |
| 13+ | +1.700 | +1.606 | +0.729 |

The older pair is closer for 7–12, but the 13+ movement remains substantially unexplained. More importantly, the older-pair model predicts repairable mean growth of about +0.08%, −0.04%, −0.17% for the three older buckets, rather than the roughly +1% reported for 7+ overall. The modeled total-loss threshold removes expensive repairs, changing the average of the remaining repaired vehicles. Consequently, a reported repairable-mean change cannot simply be entered as the latent repair-cost multiplier and expected to reproduce itself.

Do not select the best-looking TLF fit and call the economics validated. The meaningful requirement is joint compatibility with TLF, conditional repair costs and selected vehicle values, with population/period differences exposed. We have not yet achieved that.

## 4. Competing explanation: fewer small claims, with no extra totals

For a normalized initial claim population, suppose only repairable claims disappear and total-loss counts are unchanged. Then the fraction of original claims removed is `1 − TLF_2024 / TLF_2025`. This is an identity-based limiting case, not an estimate of customer behavior.

| Age | Original claims removed to reproduce TLF | Original repairables removed |
|---|---:|---:|
| 1–3 | 4.67% | 5.20% |
| 4–6 | 1.91% | 2.26% |
| 7–9 | 2.56% | 3.32% |
| 10–12 | 2.48% | 3.62% |
| 13+ | 3.75% | 6.65% |

This mechanism reproduces the five increases arithmetically with **zero additional total-loss supply**. It cannot explain the current/newer group's decline through removal alone. It also does not establish zero actual growth: observed claim counts and damage/coverage changes can coexist. The previously documented CCC count/TLF mismatch prevents treating this table as a measured decomposition.

Removing only minor repairables does not change auction ASP or RPU if the total-loss population is untouched. Coverage losses are different: they may remove severe incidents too. Keep coverage, reporting selection and economic totaling decisions distinct. Do not add a filing haircut to a reported-frequency input that already incorporates filing and then independently add a TLF uplift for the same event.

## 5. Could within-age economics be material? Conditional transmission only

Applying the observed broad calendar-Q2-2026 index ratios to the fixed calibration produces modeled TLF +2.489 points, total-loss units per reference claim +10.876%, core RPU −0.195%, and core auction revenue per reference claim +10.660%. This is **not a FY27 prediction**: the ratios are broad proxies, applied to an illustrative fixed reference population rather than an observed matched Q2 cohort, and claim activity/capture/adoption are held constant.

This answers only the architecture question: the repair-versus-value mechanism can move the model materially, unlike the small default six-month fleet-composition change. The model's sensitivity is not evidence that the real-world effect is that large. The historical compatibility failures above prevent importing those percentages into the revenue forecast.

A separate unobserved diagnostic increases salvage recovery by 1% relatively at every damage rank, keeping repair and pre-accident value unchanged. The same recovery factor enters insurer net salvage and auction prices. It produces units per claim +0.430%, core RPU +0.481%, and core revenue per claim +0.913%. This is a plumbing/mechanism test, not a forecast or sourced recovery estimate. In this model salvage can support both units and fees; offsetting units/RPU behavior is not guaranteed.

## 6. Forecast decision and next discriminating evidence

No FY27 driver changes are adopted from these tests. Do not automatically carry CY2025 growth or calendar-Q2-2026 index movements into the next Copart quarters.

The most useful next evidence is repeated **same-age conditional values and repair means with consistent loss coverage**, especially the 13+ group, plus compatible claim/valuation counts. Existing broad 7+ value data improve on all-age used-car CPI but cannot resolve age changes within 13+ or repair-selection effects. A targeted source request should seek these tables and definitions, not more unrelated repair invoices or a large auction scrape.

In the architecture, retain three separately identified blocks: constant-damage repair/vehicle-value/recovery assumptions; severity-dependent recorded-claim selection; and the resulting conditional repair/total-loss populations. Calibration should be tested against all available conditional outputs. Neither observed TLF nor repaired average cost should be inserted as an independent growth layer on top of the mechanism producing it.

## Files and checks

`within_age_economics.py` produces `within_age_backcast.csv`, `within_age_filing_alternative.csv` and `within_age_economics_results.json`. JSON preserves source hashes, matched months, case inputs and limitations. Thirteen checks cover native-engine equivalence, units-times-RPU identities, equal repair/value scale invariance and filing arithmetic. The prior age decomposition was rerun unchanged. No production forecast, source observation or fitted parameter was overwritten.
