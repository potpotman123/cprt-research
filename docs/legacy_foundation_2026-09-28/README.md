# Legacy model foundation: first historical control pass

28 September 2026. Bounded work on existing local files; no scraping, OCR, paid data, simulations or Excel mutations. This is an evidence and architecture repair, not a new investment forecast. Original model remains available for comparison. Calculations reproduce with `audit.py` in this directory; inputs are hashed in `results.json`.

## What changed in our understanding

### 1. Total units and fee units cannot be interchanged

Original call evidence:

| Observation | Local source |
|---|---|
| FY26Q1 global total units -6.7%, fee units -6.3% | `raw/transcripts/call_2025-11-20.txt`, line 161 |
| FY26Q1 US total units -7.9%, US fee RPU +7.5% | same file, lines 177 and 209–210 |
| FY26Q1 international fee RPU +8.1%; some purchased contracts migrated to consignment | same file, lines 219–223 |
| FY26Q2 international fee RPU +7.6% | `call_2026-02-19.txt`, lines 184–185 |
| FY26Q3 international fee RPU +10.5%, total units +5.9% | `call_2026-05-21.txt`, lines 178–184 |
| FY26Q4 international total units +10%, fee units +11.5%, purchased units +0.2%, fee RPU +3.5% | `call_2026-09-10.txt`, lines 223 and 232–235 |

Dollar source: `data/csv/segment_service_rev_8k.csv`, paired US/international service revenues for FY25 and FY26. We reread original local calls, not just the older derivative unit tables. These remain transcript-derived disclosures; original audio has not been checked. Exact filing-derived dollars take precedence over rounded spoken dollar descriptions.

The two-way seller classification (insurance/noninsurance) is distinct from the ownership classification (consignment/purchased). Neither is a geography classification. The intended foundational dimensions are geography × seller type × ownership basis × fiscal period. Referral, registration and other non-unit service revenue require separate rows where applicable. Do not assume all noninsurance units are fee units or all insurance units are necessarily fee units in every market.

### 2. We can infer some historical fee-unit changes without knowing absolute counts

For matching populations and recognition definitions:

`1 + fee-unit growth = (current service revenue / prior service revenue) / (1 + fee-RPU growth)`.

| Period | US inferred fee-unit growth | International inferred fee-unit growth |
|---|---:|---:|
| FY26Q1 | -7.46% | -0.20% |
| FY26Q2 | unavailable | +0.06% |
| FY26Q3 | unavailable | +6.71% |
| FY26Q4 | unavailable | +11.56% |

These are algebraic inferences from disclosed RPU, not independent unit observations. Rounded RPU inputs produce intervals in `historical_controls.csv`. Q4 international overlaps the independently disclosed rounded +11.5% fee-unit growth. That cross-check supports the denominator distinction. The growth identity alone is not independent validation because one input was solved from the other two.

US Q1 total-unit growth is -7.9%, compared with inferred fee-unit growth -7.46%; international Q3 total-unit growth is +5.9%, compared with inferred fee-unit growth +6.71%. Applying total units to service revenue would contaminate the apparent fee growth. US Q2–Q4 service-per-total-unit ratios are recorded as diagnostics, explicitly NOT reported fee RPU. Do not plug global RPU or insurance ASP into those gaps.

These year-over-year observations do not identify sequential quarterly unit levels or seasonal unit shares. One independently normalized unit base per prior-year quarter is required before constructing a seasonal unit history. Do not chain four year-over-year rates as if they were sequential growth.

### 3. An annual revenue tie hides a poor quarterly reconstruction

Existing model minus reported US service revenue:

| FY26 | Q1 | Q2 | Q3 | Q4 |
|---|---:|---:|---:|---:|
| Residual, $m | +10.23 | +44.04 | -56.15 | 0.00 |

Annual signed error is only -$1.88m, but the sum of absolute quarterly errors is $110.42m. Q4 matches by construction. It is not evidence of a validated annual or quarterly forecast.

The existing model holds other-US service revenue at $81.78m per quarter and historical insurance RPU nearly flat ($871.74 to $871.24). Most modeled sequential insurance-revenue change tracks the assumed carrier allocation path. `historical_residuals.csv` records the allocation-only counterfactual to isolate the smaller fleet/RPU changes. Removing those small changes does not explain the large quarter-specific errors. This identifies a structural omission; it does not uniquely identify claims seasonality, weather, fees or carrier timing as the cause.

Holding the insurance model fixed and assigning the entire unexplained amount to noninsurance produces an implied residual stream, also recorded in the CSV. That is a diagnostic, NOT measured noninsurance revenue. Do not adopt it as historical truth or forecast its growth.

### 4. The flat international branch embeds growth

FY26 international service revenue totals $581.233m. Repeating FY26Q4's $151.722m four times produces $606.888m, or +4.41% FY27 growth, even though the activity and price assumptions say flat. First-half growth is +12.85% because the earlier comparison quarters were lower.

Repeating the prior year's quarterly revenues instead, purely as a zero-growth diagnostic, lowers H1 FY27 international revenue by $34.549m and FY27 by $25.655m versus the prototype. Neither rule is an adopted forecast. The difference demonstrates that the starting-quarter convention can overwhelm a subtle fleet-mix thesis. It does not prove the pattern is recurring seasonality: actual unit, fee, FX, contract-conversion and growth trends may explain it.

Required replacement: compatible quarterly fee units × fee RPU × currency translation, with purchase-to-consignment conversions explicit. Forecast each quarter from its matching historical period or use independently estimated sequential seasonality and trend. Do not hardcode revenue seasonality and also apply seasonal unit/RPU adjustments for the same effect.

### 5. The 90% insurance-dollar assumption needs separate evidence

Q4 US total units -5.7%, insurance units -7.5%, noninsurance units +0.2% imply approximately 76.62% prior-year and 75.16% current-year insurance unit weights IF these cover identical, exhaustive populations. Inputs are rounded; this is not an exact company disclosure.

If that current unit mix were also the relevant fee-unit mix, 90% of service dollars coming from insurance would require insurance RPU to be roughly 2.97× other-US RPU. The condition may fail because purchased vehicles and non-unit service revenue affect the populations. The ratio therefore does not disprove 90%; it shows why the assumption cannot be validated by an unrelated global insurance unit share.

The prototype infers 3.510m annual US insurance units from assumed fees and its dollar allocation. Copart's statement that global units exceeded four million is a lower-bound disclosure, not an exact count that can validate or reject 3.510m. The skeleton's four-million global anchor is also an assumption. Do not treat agreement between two assumed anchors as independent evidence.

## Foundation architecture decisions

1. Historical controls are source observations, separate from modeled reconstruction. `historical_controls.csv` is a review artifact; when implementing in Excel, underlying reported observations go into Source Data and the growth calculations into a historical build. Checks remain terminal and never supply business inputs.
2. Distinguish reported dollar history, observed/derived unit-growth history, normalized unit levels, and modeled claim/damage states. A normalized level is explicitly conditional. The damage engine explains changes around that base; it must not silently manufacture observed historical counts.
3. Keep insurance and noninsurance seller branches, but add explicit fee/purchased scope. The carrier build applies to eligible insurance flows; it does not allocate every US service dollar. Purchased units have their own gross-sales bridge.
4. Keep non-unit service revenue outside sold-units × auction RPU unless the reported RPU definition includes it; document that denominator. Separately identify fee-basis conversions so reported revenue changes are not mistaken for loss of economic activity.
5. A period-matched historical service-revenue bridge precedes forward forecasting. Attribute revenue growth to matching fee-unit growth, fee RPU growth and their interaction. Do not label the insurance ASP growth rate as RPU growth.
6. Audit carrier allocations against observed insurance growth with matched year-over-year periods. The current workbook only has FY26–FY27 allocation paths; it cannot validate FY26 year-over-year share changes without FY25 counterparts. Build that source history rather than interpreting sequential path declines as year-over-year facts.
7. Use a separate base-dollar allocation assumption until insured fee units and fees can identify it. Sensitivity of that split must be reported separately from genuine forward driver effects. Do not recalibrate the base unit scale every time a forecast service-adoption input changes.

## Immediate next bounded tasks

| Task | Source/method | Why first | Completion condition |
|---|---|---|---|
| Recover missing US fee-unit or RPU disclosures | Search already-held quarter calls, earnings tables and broker operating tables for exact denominator/period | Avoid artificial RPU growth from purchased-unit mix | Observed fee units or observed fee RPU, otherwise explicit missing value |
| Resolve FY25–FY26 carrier timing | Friend workbook quote bank and event ramps; original local carrier contract passages | Test allocations against matched insurance unit growth | Assignment/sales definition and effective dates documented; no second lag |
| Identify insurance fee-unit dollar base | Existing broker unit assumptions and company fee/purchase disclosure, triangulated rather than asserted | Replace or bound 90% dollar allocation | Independently supported range or explicit non-identification |
| Explain international quarterly change | Existing calls for fee units, RPU, FX and purchase-to-consignment conversion | Remove hidden run-rate growth | A quarterly unit/fee/FX identity with separate conversion treatment |
| Rebuild forward quarterly foundation | Populate source history and linked engines only after those checks | Preserve mechanism attribution | Model errors exposed by quarter; no fitted unexplained revenue-growth plug |

The work is deliberately more useful than another large scrape at this stage: it clarifies which observations can constrain the model. No new damage/repair parameters or service-adoption prices are promoted to empirical facts in this pass.

## Verification and limitations

Executed exact revenue growth identities for available RPU pairs; tested rounding overlap on international Q4 against disclosed fee-unit growth; reproduced Q4 calibration and all four US residuals; verified the flat-quarter international arithmetic. Source snapshots hashed. No Excel files edited or recalculated. Calculations use the previously validated workbook's exported baseline results. This does not validate the prototype forecast, carrier allocations, seasonality or causal thesis.
