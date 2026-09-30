# Conditional short: the assumptions required, not a manufactured catalyst

30 September 2026. User-requested changes to forward assumptions, implemented in separate runnable configurations using the existing revenue engine. **The 3% miss case produces FY27 legacy service revenue of $3,939.17m, $121.83m below the dated JPM forecast. It requires a 6.46% terminal insurance-unit shortfall versus our reference, plus the price-driver path below. These inputs are reverse-solved hypotheses, not newly measured forecasts.**

The existing reference, historical evidence and model coefficients are intact. `forecast_admission=false` and `catalyst_verified=false` explicitly preserve the distinction between achieving a numerical miss and supporting a trade. No probability, earnings revision, valuation or price target is assigned.

## Assumptions changed in the new configurations

| FY27 quarter | Q1 | Q2 | Q3 | Q4 |
|---|---:|---:|---:|---:|
| Existing fixed-mix realized-price driver | +3.70% | +3.70% | +3.70% | +3.70% |
| New realized-price driver, ASSUMED | +3.70% | +1.85% | 0.00% | 0.00% |
| Insurance units versus reference, reverse-solved 3% miss case | 0.00% | −3.23% | −6.46% | −6.46% |
| Implied modeled insurance sold-unit growth YoY | −0.30% | −3.51% | −6.77% | −6.82% |
| All-in insurance RPU versus reference, model output | 0.00% | −0.81% | −1.60% | −1.60% |
| Legacy service revenue, $m | 1,021.58 | 950.95 | 1,024.98 | 941.67 |

The +1.85% step is a hypothetical halfway point, not a measured trend. Zero refers to the fixed-mix price **driver**, not an assertion that reported insurance ASP will be exactly flat: composition also affects ASP. The engine applies the actual saved fee brackets, so price and fee RPU do not move one-for-one.

The unit shock scales every carrier's forward reference allocation by the same proportion, with half the terminal reduction in Q2 and the full reduction in Q3–Q4. This is a transparent aggregate exposure stress, **not an assertion that every carrier reduces allocation or that a particular contract has been lost**. Historical allocation vectors are copied unchanged. Q2/Q3 are sale-equivalent realization assumptions beginning November 2026/February 2027, not verified announcement dates or measured assignment-to-sale lags.

Claims, repair costs, expected salvage, the selection distribution, seller fees, buyer mix, title/delivery pricing and adoption, other-US activity and international growth retain reference settings. In particular, the price-only shock leaves total-loss selection unchanged. This isolates required operating outcomes; it does **not** validate aftermarket adoption, recycled displacement or a joint price/selection mechanism. Lower expected salvage is not silently added as another headwind.

## Four common-base cases for the 3% target

| Case | FY27 services, $m | Change versus reference, $m | Gap versus JPM, $m |
|---|---:|---:|---:|
| Existing CCC reference | 4,093.08 | — | +32.08 |
| Unit shortfall only | 3,968.38 | −124.70 | −92.62 |
| Price slowdown only | 4,062.06 | −31.02 | +1.06 |
| Both | 3,939.17 | −153.91 | −121.83 |

Exact interaction is **+$1.807m**: fewer units reduce the dollars exposed to weaker prices. Consequently the two standalone losses cannot simply be added. These are four **operating-driver cases**, not evidence-validated implementations of thesis A and thesis B.

The strongest result is that the price-only case essentially meets JPM. To make this a material short, the unit path must do most of the work. The target of 3% is illustrative, not evidence that such a miss would be material to the share price.

## Reverse-solved hurdles

All rows use the same quarterly price path and unit ramp. JPM's **11 September 2026, ex-ACV service forecast is $4,061m**; its value is loaded from the existing evidence manifest, not replaced by current consensus.

| Assumed FY27 miss versus JPM | Target service, $m | Q2 units below reference | Q3/Q4 units below reference |
|---|---:|---:|---:|
| 2% | 3,979.78 | 2.16% | 4.32% |
| 3% | 3,939.17 | 3.23% | 6.46% |
| 5% | 3,857.95 | 5.36% | 10.72% |

These are algebraic operating hurdles, not estimates of account-loss probabilities. The reference repeats same-quarter historical allocations; it is not a named broker's carrier build. Therefore a 6.46% reduction versus reference is **not automatically incremental to Barclays' already assumed 2.5–3.5% net contract drag**. Compare actual carrier exposure and timing before making that claim. Likewise, the 6.46% is a relative change, not a 6.46-percentage-point loss of market share.

## What would make the case catalyst-backed

1. **An incremental contract problem:** a named award, weaker win realization or documented seller terms with exposure/effective dates beyond the already expected transition. There is no verified new account event in the current evidence. Do not attribute this anonymous unit stress to State Farm, GEICO or Progressive without support.
2. **A compatible operating reveal:** FY27 Q2 results, expected February 2027 but exact date unconfirmed in the prior review, would need insurance sold units around **−3.5% YoY** to track this case, followed by roughly **−6.8%** in Q3/Q4. These are the model's required outcomes, not broker-disclosed expectations. Reconcile CAT, claim frequency, timing and win/loss effects before attributing a weak print to competition.
3. **Price/fee evidence:** the same observation window must support fading auction economics on a comparable population. Recycled collision contribution and donor-bid evidence could support the parts mechanism; a lower blended ASP alone cannot. The previously documented LKQ October 29 window remains an observation opportunity, not a known adverse disclosure.

**Falsification:** if compatible insurance units stay near the reference (approximately flat) and pricing continues near the reference, this short case fails. If Q2 units recover rather than deteriorate, reset the stress assessment instead of moving its unchanged ramp into later quarters. A price slowdown without the required unit gap leaves the quantified short largely unsupported. A macro or CAT unit decline may create a miss without validating either proposed thesis.

## Reproduction, checks and scope

Run `python3 model/reverse_short_2026-09-30/run.py`. Editable hypotheses are in [assumptions.json](assumptions.json); fully executable engine configurations in [scenario_configs.json](scenario_configs.json); results in [quarterly_results.csv](quarterly_results.csv), [scenario_summary.csv](scenario_summary.csv), and [hurdles.csv](hurdles.csv).

The terminal unit reduction is solved directly from price-case insurance revenue exposure, then checked against full engine runs. This avoids an unnecessary optimizer or new empirical fit. The existing fee schedule handles price pass-through. Checks confirm reference reproduction, unchanged historical levels, exact target hits and interaction, unchanged Q1, preserved unit counts in the price-only case, and unchanged selection/other branches and upstream source hashes. The existing core engine checks were also run. Arithmetic correctness does not validate the forward assumptions.

Horizon is the existing **FY27 through July 2027**, whose final results would ordinarily be observed around September; no precise release date is asserted. No FY28 extension, acquisition consolidation, dated actual-carrier contract or aftermarket adoption path has been fabricated. A genuine forecast through September 2027 and the next forward year still requires those original admission steps. The workbook was not edited.

Sources: [dated expectations](../../reports/expectations_sheet_2026-10.md), [catalyst evidence and limitations](../../reports/catalyst_scorecard_2026-10.md), saved [CCC reference](../ccc_age_body_2026-09-29/reference_config.json). This follow-up is local modeling only; no new internet requests, data collection, outreach or agents.
