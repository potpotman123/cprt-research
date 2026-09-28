# Auction-price pass-through test

28 September 2026. User's “offset price” interpreted in context as auction-price changes. Existing September 26 fee snapshot only; no new scraping, OCR, paid data or Excel mutation. Exact probability integration, 216 small arithmetic scenarios. One 10,000-node deterministic arithmetic check (not 10,000 vehicle listings) completed in well under a second.

## Mechanism and method

Each posted buyer-price band has either a fixed fee or percentage fee. Integrate the fee across an assumed lognormal auction-price distribution, then shift all prices proportionately while holding sold vehicles, buyer mix and schedules fixed. Average fee of the distribution is not fee at average price. Exact normal probabilities give band mass; truncated lognormal first moments give the percentage-fee contribution. This avoids random sampling and unstable results from a few price nodes straddling thresholds.

Source: `data/csv/copart_fee_grid_2026-09.csv`, read September 26 from public fee pages in earlier work; SHA256 in results.json. Non-clean title, standard vehicles, secured payment. Buyer fee includes posted standard/preferred buyer charge, prebid virtual fee, $95 gate and $15 environmental fee. Conditional late payment/relisting and other unmodeled charges excluded. Fee bands use next lower bound as the upper integration limit; continuous-dollar approximation ignores penny gaps, a negligible distinction for a continuous distribution.

Assumed price medians $2,500/$3,500/$5,000, log sigmas 0.8/1.0, preferred buyer fractions 0/50/100%. These are alternative scenarios, not measured price distributions or statistical confidence intervals. Price changes tested: -10%, zero, +4.1%, +6%, +8.4%, +10%. Seller fee 0% or 4% and fixed additional-service revenue $55 are illustrative inherited sensitivities, not validated contract terms or observed service revenue. No international fee extrapolation.

## Results

| Uniform auction-price increase | Buyer-fee growth across scenarios | Illustrative all-in RPU growth range | Reference illustrative RPU growth |
|---|---:|---:|---:|
| 4.1% | 1.55–2.02% | 1.46–2.45% | 1.97% |
| 6.0% | 2.26–2.96% | 2.12–3.59% | 2.88% |
| 8.4% | 3.14–4.13% | 2.95–5.02% | 4.02% |
| 10.0% | 3.73–4.91% | 3.49–5.97% | 4.77% |

Reference uses median $3,500, sigma0.8, 50% preferred, seller fee4%, fixed services$55. It is a convenient scenario, not a fitted estimate. “All-in” here refers only to the components included in the illustrative formula; it is not an empirically complete estimate of company service RPU.

Because fixed fees do not increase with price inside their bands, auction-price growth does not pass through one-for-one. Some vehicles cross fee thresholds, raising mean fees. A percentage seller fee increases proportionately with price; fixed service revenue dilutes overall sensitivity. Shape, title, payment and buyer-tier changes can produce different outcomes even for the same average ASP growth. These tests hold those fixed.

## Comparison with historical bridge

US insurance ASP growth was +8.4%, +6.0%, +4.1% in FY26Q1–Q3. The historical all-US fee-RPU bridge gives +7.50%, +3.73%, +3.05%, respectively (Q1 company-disclosed; Q2/Q3 implied from broker historical fee units and reported service revenue). The reference scenario price-only responses are +4.02%, +2.88%, +1.97%.

DO NOT subtract these and call the difference Title Express or service adoption. Insurance ASP is not the price distribution of all US fee vehicles. The current schedule is not a historical fee-change series. Buyer mix, noninsurance vehicles, catastrophe composition, contract terms and service activity can all explain differences. The figures are a plausibility screen: this mechanism can dampen RPU growth as ASP growth slows, but it does not identify the historical service contribution or prove future slowdown.

This also corrects overly strong language in `reports/E6_fee_grid.md`: elasticity around0.4–0.5 was simulated under distribution assumptions, not guaranteed for every plausible distribution; the international RPU observations listed there cannot be grouped with US Q1 as a common US series. A prior regression coefficient is not used as validation here.

## Model implication

Keep direct fee-schedule integration as the buyer-fee mechanism. For price-only attribution, freeze selected vehicles and weights; do not re-run total-loss selection, because that would blend price pass-through with a volume/mix change. For the full economic forecast, run a separate joint-selection case where repair/value/recovery changes alter both selected units and prices. Report the difference as selection, not pure fee pass-through.

Our nine-severity-node engine can have threshold artifacts: a price bump moves a whole node across a fee band. Before adopting its precise price elasticity, compare against a modest refinement or integrate within price states. Today's smooth-distribution test avoids that artifact but does not validate the engine's actual selected-price distribution.

Next high-value step: obtain a compatible all-US fee-vehicle ASP series or isolate insurance service RPU, then distinguish documented fee changes from residual mix/service effects. Where that cannot be observed, retain explicit separately bounded assumptions; do not infer service adoption as an exact residual. No expansive listing scrape is required to make this limitation explicit or to use the fee mechanism in conditional forecasts.

## Verification

Zero price shocks produce zero fee changes; positive/negative price shocks move fees in the expected direction in all scenarios. Exact standard buyer-fee expectation was within $0.06 of a deterministic 10,000-quantile check. Outputs in fee_response.csv and results.json. No source data or workbooks altered. This is a fixed-schedule arithmetic experiment, not a stock-price forecast or an econometric causal estimate.
