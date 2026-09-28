# Carrier compatibility test and simplified working allocation

28 September 2026. User authorizes testing and simplifying this non-core step rather than overinvesting in it. No scraping, OCR, new data purchase, model refit or Excel modifications. Existing source workbook was read only. `run.py` reproduces the CSVs and results from local sources; source workbook SHA256 is recorded.

## Decision

Use **PGR runoff only, with fixed carrier mix and all other allocations held at FY26Q4** as the proposed working allocation path for the next forecast revision. Keep the friend's complete model as a comparison. This is a simplification of an inherited scenario, not a newly validated allocation forecast. Do not call the Progressive ramp confirmed merely because it is retained. The current Excel forecast has not yet been switched.

No arbitrary adverse share drift is added to strengthen a short. No separate Progressive haircut is applied after allocation. Carrier-specific RPU changes are not manufactured: the current calculation holds the prototype's fee economics fixed. If research later requires carrier-specific fees or vehicle mix, restore those distinctions in the revenue engine rather than adding an unexplained global RPU adjustment.

## Historical test

The original carrier engine has FY25Q4 onward history (main sheet row105, C:O), not a full prior-year comparison for FY26Q1–Q3. Share is independently reconstructed from normalized salvage weights (rows119:128) times allocations (rows130:139). Therefore only FY26Q4 has an available same-quarter prior-year share ratio. Earlier quarters are unavailable, not backfilled by extending FY25Q4 backward.

For Q4, inherited claims change -4.5% × relative TLF change +4.02% produces total-loss pool change -0.6609%. Applying friend share change -6.5079% gives modeled unit growth -7.1258%, versus reported -7.5%, a 0.3742 percentage-point miss.

This is a conditional retrospective compatibility result. It is NOT an out-of-sample backtest: the Progressive ramp was calibrated to the Q4 print according to the source review, and claims changes are proxies with population and timing mismatches. Three Q4 cases in the old panel use identical inputs; they are not independent corroborating datasets.

Historical actuals are as-reported US insurance units (-9.5%, -10.7%, -4.2%, -7.5%), not ex-CAT. Pool inputs in `units_decomp_panel_v2.csv` are not all matched as-reported claim counts: annual CCC figures are repeated across quarters, collision frequency is not all-coverage count, CY/FY overlap is imperfect, and some TLF values are modeled. Consequently the diagnostic residual also contains timing, routing, exposure and measurement differences; it is not measured market share.

Using the alternative existing pool proxies, the effective capture change needed to explain Q1 ranges from -7.82% to -2.87%; Q2 from -8.28% to -2.27%. These are proxy-case ranges, not statistical confidence intervals. Their width is a reason to avoid fitting a detailed new allocation model to this panel. Q3's repeated proxy gives -4.43%, not independent precision.

## Forward simplification screen

All cases hold the prototype's claim/damage/RPU outputs and assumed 90% insurance-dollar allocation fixed. Since allocation currently affects units proportionately, insurance revenue is rescaled by candidate allocation / original allocation. This is exact for the frozen prototype but excludes carrier-specific value/fee effects and nonlinear lag changes.

| FY27 H1 case | Service revenue delta versus full friend build |
|---|---:|
| Full friend Base | $0m |
| PGR inherited runoff only; freeze Q4 carrier weights and all other allocations | +$3.829m |
| Freeze all Q4 allocations and carrier weights | +$12.961m |

Against the existing $1,926.462m H1 prototype service forecast, these are approximately +0.20% and +0.67%. These denominators are conditional model outputs, not adopted forecasts. The case differences are not uncertainty bounds; all cases inherit the same starting share estimate.

Keeping only PGR preserves the principal near-term transition while removing speculative offsetting events and premium-share growth assumptions. The small net difference does not prove each discarded event is individually immaterial; wins and losses can offset. It establishes that the current full package's net H1 impact beyond the simplified path is small. Event-level reinstatement can be reconsidered when evidence materially changes.

## Integration contract for the next model revision

1. Freeze each carrier weight at FY26Q4 rather than extrapolate premium-share changes as insured-vehicle growth.
2. Freeze all allocations except Progressive; use the inherited forward PGR path as a transparent scenario. Once that path reaches its assumed endpoint, keep it flat absent new evidence.
3. Compute aggregate effective allocation once; do not also apply the friend's aggregate share-growth output.
4. Retain the historical carrier path solely as labeled reconstruction, not observed share. Explain that continued year-over-year declines can occur despite flat sequential allocation because earlier comparison quarters had higher allocations.
5. Treat the path as a sale-equivalent allocation scenario for now so no second lag is silently imposed. A future assignment/inventory engine must revisit that convention explicitly.
6. Keep unknown absolute market-share level separate from the observed service-dollar anchor. Calibration does not identify true share or absolute industry claims.
7. Limit further carrier research unless a new source changes near-term economics materially. Move research effort to joint damage selection and realized RPU attribution.

## Next substantive research

Use the historical service bridge to test the RPU mechanism. The engine must explain the effects of selected vehicle values, posted fee brackets, seller mix and additional-service revenue, not merely reproduce revenue by solving a residual. Start with a bounded ASP-to-buyer-fee calculation, keeping company aggregate fee RPU distinct from insurance ASP. Keep price/mix/service contributions separately identified or explicitly unidentified. No large listing scrape is needed to establish the first arithmetic bounds.

## Checks and limits

Carrier weights sum to one; friend Base revenue deltas reproduce zero; unavailable historical comparisons stay blank; exact multiplicative growth is used rather than additive gaps. Historical and forward outputs use separate populations and are not presented as one validated time series. No forecast workbook or source observations were overwritten. The only delivered changes are reproducible diagnostics and this working integration decision.
