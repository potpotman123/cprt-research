# Historical baseline repair and remaining identification gap

28 September 2026. Bounded local arithmetic only; no web scrape, OCR, paid retrieval, Excel design or calibration search.

## What changed

The old reconstruction used FY25 revenue by quarter as unit seasonality, applied modeled carrier capture by quarter, and normalized everything to FY26Q4 dollars. That is not a measured quarterly unit baseline. Revenue already combines activity, fees, mix and timing. Consequently, the error cannot safely be attributed to claims or repaired by changing the damage distribution. Nor is exact double-counting empirically proven.

There are now three separate outputs:

1. **Reported history and operating attribution:** `historical_operating_bridge.csv`. Prior-year dollars, compatible fee-unit/RPU growth observations, derived counterpart, interaction and missing attribution. These reconcile accounting; they do not validate the damage engine.
2. **Original reconstruction:** `quarterly_results.csv` and the existing historical error explanation remain unchanged, with the original errors. Its FY27 dollar outputs are superseded as the working presentation baseline, not deleted.
3. **Same-quarter forecast bridge:** `reconciled_quarterly_service.csv`. Historical rows show reported geography dollars. Forecast rows apply explicit modeled changes to the matching reported quarter, without interpreting historical revenue as unit seasonality.

## Historical evidence restored

| US period | Fee units YoY | Fee RPU YoY | Evidence |
|---|---:|---:|---|
| FY26Q1 | −7.46% | +7.50% | Company RPU; units derived from revenue identity |
| FY26Q2 | −9.00% | +3.73% | Previously verified Stephens historical fee units; RPU derived |
| FY26Q3 | −3.30% | +3.05% | Previously verified Stephens historical fee units; RPU derived |
| FY26Q4 | Unknown | Unknown | −$6.991m revenue change remains unallocated |

These are all-US fee activity, not US insurance-only vehicles or all vehicles including purchased units. They are YoY growth observations, not sequential quarter levels. International uses company RPU growth of 8.1%, 7.6%, 10.5%, 3.5%, with fee-unit growth derived from the revenue identity. Original transcript paths and the prior broker verification are recorded in the CSV. Rounded disclosures limit precision. The US Q2/Q3 broker data are not upgraded to company disclosures.

## Forecast equations

For FY27 quarter q, let b be the matching FY26 quarter. US insurance service revenue is:

`Reported_US_services[b] × assumed_insurance_share × exposure_frequency_ratio × TLF_ratio × capture_ratio × all_in_insurance_RPU_ratio`.

Every ratio is modeled q divided by modeled b, not divided by FY26Q4. The RPU calculation still comes from selected vehicle prices, the buyer fee grid, seller fees, title and delivery assumptions. No independent service-growth percentage is added. Routing and consignment are constant in this version and cancel; quarter-varying versions would require explicit additional ratios.

Other-US revenue is `Reported_US_services[b] × (1 − assumed_share) × activity_ratio × fee_ratio`. International is `Reported_international_services[b] × activity_ratio × fee_ratio × FX_ratio`. With their current flat driver assumptions, these branches are flat YoY, rather than inheriting Q4's prior-year growth in all quarters.

The existing raw intermediates can compute these ratios because the same-quarter revenue seasonal factor and common absolute normalization cancel. Tests deliberately distort FY25 seasonal inputs and confirm that the revised forecast is unaffected. Capture appears once in the insurance growth bridge; it is not applied to other-US or international revenue.

## This is a baseline repair, not an independently rebuilt historical unit census

The same-quarter anchor is an explicit calibration choice. It carries forward unmodeled historical level differences proportionately for one year. This would fail if an omitted historical CAT, fee, timing or mix effect reverses. The output exposes each branch's **anchor-to-raw-base ratio**, making that transfer auditable rather than hiding it as a claims input.

The 90% insurance share, formerly applied at Q4, is now provisionally applied to each matching historical revenue anchor. That is a new application of an existing assumption, not observed quarterly segment data. Historical insurance dollars remain blank in the reported rows. No absolute units or historical ancillary split have been identified. Thus the user's eventual fully bottom-up operating build remains unfinished even though the working dollar forecast now has a coherent starting point.

Do not claim the original historical reconstruction has passed. Its total-service errors remain +$56.565m, +$98.916m, +$15.586m and approximately zero. A table populated with reported history has no reconstruction error by definition; that is not predictive evidence.

## Mechanical effect on provisional outputs

USD millions, legacy service revenue only; not adopted forecasts or newly discovered investment alpha.

| Quarter | Original convention | Revised same-quarter baseline | Difference |
|---|---:|---:|---:|
| FY27Q1 | 993.990 | 940.572 | −53.418 |
| FY27Q2 | 998.473 | 904.991 | −93.481 |
| FY27Q3 | 1,043.574 | 1,028.648 | −14.927 |
| FY27Q4 | 965.104 | 965.104 | 0.000 |

Q4 is unchanged because both conventions already use that quarter as the anchor. The reductions elsewhere remove the extrapolated baseline discrepancy; they are not evidence supporting a short. The inherited capture ratios still imply about −6.78%, −6.46%, −3.46%, −0.62% YoY, and remain provisional assumptions. They dominate this default case; they have not been independently proven by fixing the baseline. Fleet/repair and service-adoption thesis forecasts still need evidence-supported inputs.

## Verification and next boundary

22 adapter checks pass: eight historical accounting reconciliations, missing Q4 split retained, errors preserved, no historical insurance split invented, branch and units/RPU reconciliation, invariance to arbitrary old seasonal-proxy changes, unchanged-driver flat-YoY behavior, and capture acting once on insurance only. These are correctness checks, not empirical validation. The existing economics/calibration checks remain applicable and are separately rerun.

Next evidence needs are compatible historical insurance activity and capture timing, followed by identifying whether unmodeled base-quarter effects persist. Without those observations, we cannot explain away the historical reconstruction errors or claim all revenue has been independently generated from physical quantities. Keep the original residual audit available while using the revised bridge for further model development. The acquisition overlay remains separate and gated by classification.
