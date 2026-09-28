# Connected fleet, selection and quarterly service revenue

28 September 2026. Default engine now uses corrected cohort claim mass and the existing vintage body-mix proxy. No new source estimates or recalibration. Existing carrier allocation and service assumptions remain provisional.

## Calculation and evidence boundary

Historical car/light-truck sales → candidate subtype births → survival → exact-age/body fleet → combined relative claims propensity × fixed cell correction → claims → economic total-loss selection → selected auction prices and fee schedules → units × RPU → same-quarter historical revenue anchor.

Corrections remain those derived from the original CY2025 fixed-body calibration. They are not refitted to hide vintage-mapping target drift. The age/body masses now determine both aggregate claim activity and claim composition, replacing aggregate fleet growth as the activity driver. Incremental repairable-only nonfiling still changes reported claims and TLF together and leaves total-loss sales unchanged.

Sales totals are historical inputs; subtype births transfer EPA model-year production shares onto sales totals. They are not observed registrations by subtype. Survival and claims propensity are fitted. SUVs are pooled, vans inherit minivan economics, recent subtype mix holds2024, and2026–27 sales hold2025. Annual fleet snapshots are interpolated into quarters; actual accident-to-sale timing is unmeasured.

Damage selection and fees were already implemented; this change supplies them with consistent cohort claim quantities. Body/age economics remain calibrated assumptions, not independently measured damage distributions. No additional claim-frequency, repair/value inflation or adoption growth is assumed by the default multipliers.

## Quarterly outputs

Use `reconciled_quarterly_service.csv` for the headline history/forecast, and `connected_quarterly_bridge.csv` for attribution. `connected_bridge_steps.csv` exposes intermediate insurance revenue, units and RPU ratios. `quarterly_results.csv` remains the raw absolute-reconstruction diagnostic, not the headline forecast.

| $m, legacy total service revenue | FY27Q1 | FY27Q2 | FY27Q3 | FY27Q4 |
|---|---:|---:|---:|---:|
| Current provisional forecast | 939.531 | 903.998 | 1027.435 | 963.849 |
| Change from prior architecture | -1.041 | -0.993 | -1.213 | -1.256 |
| Fleet-only change versus prior-year service base | -0.140 | -0.403 | -0.828 | -1.137 |
| Carrier allocation contribution | -52.173 | -47.650 | -27.817 | -4.558 |

Bridge order: total surviving fleet size → exact-age fleet mix → body mix within exact age → combined frequency → repair cost → vehicle value → carrier allocation → title adoption → delivery adoption. Then add other-US and international changes. Interactions belong to the later step; contributions are order-dependent accounting attribution, not uniquely identified causal effects. Fee schedules and contractual fee parameters stay fixed. Nonfiling's pure repairable-removal contribution is zero by construction.

Fleet-only diagnostic changes fleet size/age/body and holds frequency, economics, allocation, adoption and other businesses at same-quarter prior-year levels. Its first-half delta is -$0.544m versus a $1943.896m prior-year total service base (about -0.028%). Allocation contributes -$99.823m. This is not a newly evidenced fleet short; it exposes dependence on inherited allocation assumptions. Zero default contributions elsewhere mean unchanged assumptions, not evidence of no economic effect.

## Validation and remaining gaps

20 attribution checks passed, including exact quarterly reconciliation, units×RPU, and agreement with the previously saved vintage-body candidate. All74 structural and69 nonfiling integration checks passed. Source hashes are recorded in `connected_bridge_results.json` and refreshed engine/history manifests.

Historical revenue anchors still do not identify absolute claims or insurance units. The raw model's FY26Q2 total-service reconstruction error is about+$99.507m; it is disclosed rather than fitted away. Historical insurance share remains90% assumed. International and other-US still have simple activity/fee adapters, not granular theses. Acquisition revenue is excluded from the legacy service forecast. Connection and arithmetic validation do not establish forecasting accuracy.

Next analytical priority: independently improve consequential repair/value/selection or adoption changes, or validate carrier allocation. Do not deepen fleet detail merely to manufacture a larger effect.
