# Historical reconstruction errors — size and mechanical explanation

28 September 2026. Existing model outputs and filing-derived controls only. No forecast assumptions changed. `explain_history.py` reproduces the arithmetic and picture; `historical_error_explanation.json` preserves full-precision results. A small Pillow chart is supplied; no OCR, data collection or expensive experiments. These are retrospective reconstruction errors, not out-of-sample forecasts.

## Size, using matching denominators

| FY26 | Reported US services | Model US services | US error | US error % | Reported total services | Total service error | Total error % |
|---|---:|---:|---:|---:|---:|---:|---:|
| Q1 | $855.534m | $902.520m | +$46.986m | +5.49% | $991.845m | +$56.565m | +5.70% |
| Q2 | $819.467m | $908.765m | +$89.298m | +10.90% | $952.051m | +$98.916m | +10.39% |
| Q3 | $895.464m | $914.384m | +$18.920m | +2.11% | $1,056.080m | +$15.586m | +1.48% |
| Q4 | $817.822m | $817.822m | $0 | Calibrated | $969.544m | $0 | Calibrated |

Q2 total company revenue including purchased vehicles was $1,121.674m in the saved financial controls. This model projects service revenue only; comparing its service error with that broader total would dilute the percentage without improving model accuracy. The appropriate Q2 US denominator is $819.467m, and total-service denominator $952.051m.

## Exact US error bridge

Start at Q4 US revenue multiplied by the FY25 quarter/Q4 revenue ratio. Subtract actual quarter revenue. Then apply changes relative to Q4 sequentially to the insurance branch in this order: fleet exposure, cohort TLF, effective capture, all-in RPU. The other-US branch follows the seasonal proxy only under present defaults. Each contribution is the difference after versus before that step; their sum exactly equals the error. Interaction allocation is order-dependent, not unique causal attribution.

| Mechanical contribution, $m | Q1 | Q2 | Q3 |
|---|---:|---:|---:|
| Q4 anchor × prior-year seasonal revenue proxy, less actual | -2.833 | +41.305 | -4.456 |
| Fleet exposure change beyond seasonal proxy | -1.221 | -0.835 | -0.435 |
| Cohort TLF change | +0.024 | +0.163 | +0.115 |
| Inherited carrier capture relative to Q4 | +50.606 | +48.362 | +23.538 |
| All-in insurance RPU change | +0.410 | +0.303 | +0.158 |
| Total US error | +46.986 | +89.298 | +18.920 |

### What the first row means

The model transfers last year's service-revenue shape into an activity-seasonality assumption. For Q2, FY25Q2 services were 1.052517× FY25Q4. Applying that to FY26Q4's $817.822m gives approximately $860.772m, already $41.305m above FY26Q2 actual. The prior-year shape includes pricing, carrier mix, catastrophe and other conditions, not only recurring seasonality. It cannot be called a measured claims profile.

### What the capture row means

Inherited effective capture is 60.11% in Q2 versus 56.58% in Q4, a 6.25% relative increase. Since the model is normalized at Q4, the stronger inherited Q2 capture increases reconstructed Q2 insurance sales/revenue. It adds $48.362m in this ordering. These capture levels are modeled, not observed company market shares. The calculation does not establish that the allocation path is false: weaker true industry claims, different fees, a different anchor or timing could offset it.

The prior-year revenue shape can itself embed allocation/fee effects, so adding a distinct capture path may duplicate or mis-time part of the historical pattern. That is a compatibility risk to test, not a proven exact double count.

### What the small repair/RPU rows do and do not establish

The present reconstruction leaves frequency, within-cohort repair/value changes, pricing and service adoption flat. Age/body movements barely change TLF/RPU between these quarters. This explains why the integrated model's shape is primarily driven by its seasonal proxy and capture path. It does not establish that actual economic repair costs or RPU were stable, nor that the repair model's absolute level is accurate. Level errors can be absorbed by Q4 normalization and affect the inferred unit scale.

## International

International has no carrier engine. It repeats Q4's revenue level using FY25 geography revenue shape. This imposes the Q4 YoY revenue factor on every historical quarter when activity/fee/FX multipliers equal one. Actual Q1/Q2 growth was lower; Q3 was higher. The resulting errors are +$9.580m, +$9.618m and -$3.334m. This is a known simplistic time-profile assumption, not an identified error in a physical international unit forecast.

## What cannot fix Q2 alone

Modeled US insurance services = $822.688m; all reported US services = $819.467m. Holding insurance unchanged would require other-US services of -$3.221m. Thus reducing the positive other-US branch alone cannot reconcile Q2.

If other-US revenue and RPU were held fixed, insurance activity would have to be 10.85% lower to close Q2. This is a diagnostic residual, NOT a measured claims decline or an adopted forecast adjustment. Equally, lower fees, different service composition, a different 90% anchor share or capture/timing assumptions could explain portions of the gap.

## Decision and next work

The miss is large enough that precise thesis deltas should not be trusted yet. Prioritize reconstructing the historical activity/time profile and checking capture's assignment-versus-sale basis. Use available reported fee-unit/RPU controls and compatible industry counts, leaving missing quarters explicit. Treat the prior-year revenue seasonal template as a temporary assumption, not the ground truth. Do not delete the capture path merely because doing so improves errors; do not refit repair distributions to these dollar misses; do not overwrite residuals with fitted quarterly claims inputs and call that a backtest.

For historical presentation, reported dollars stay reported. The reconstructed operating history stays alongside them as a diagnostic. No historical or forward model inputs changed in this pass; the chart and bridge explain the problem without disguising it.
