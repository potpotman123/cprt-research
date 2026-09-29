# Repair/salvage execution: evidence, dollar offsets and quarterly timing

28 September2026. Completed the authorized bounded discovery, schema checks, mechanism arithmetic and quarterly scenario integration. **No new evidence justifies adopting −3% repair costs, −5% salvage prices or a precise switching elasticity as a forecast.** The useful new findings are source-specific pricing differences, a tighter offset calculation, and the importance of timing. See [EVIDENCE.md](EVIDENCE.md) for prior-work decisions, exact searches, access failures and source admissions.

## What changed in the explanation

PartsTrader's fixed-basket discussion distinguishes OEM/recycled inflation from flatter aftermarket prices. This weakens a broad parts-price-deflation claim while leaving a narrower sourcing-substitution mechanism open. Its separate operations discussion suggests increased replacement can counteract cheaper sourcing. These are provider observations/commentary with incomplete quantitative methodology, not observed older-vehicle insurer-approved repair-cost changes.

LKQ's annual report confirms that recycler bid setting considers inventory, historical demand and recent prices, and that exporters/rebuilders compete for donor vehicles. That supplies operational support for modelling buyer economics, but not a numerical relationship between parts-price inflation and salvage bids. PartsTrader and LKQ measure different populations; neither validates the other's coefficient.

The emerging research fork is consequently **sourcing savings versus replacement complexity and donor demand**. New aftermarket substitution could reduce repair costs without directly requiring salvage donors. Recycled substitution could simultaneously reduce a repair bill relative to OEM and support donor demand. Their effects on total losses can offset in dollars, while auction fees still rise. Neither path is selected as the empirical forecast.

## New calculation1: cheaper parts do not reduce the entire repair bill proportionately

Hold vehicle, damage, operations and quantities fixed. Let p be the initial bill share of an eligible substitutable parts basket; s its alternative-parts quantity share; d the discount to an equivalent OEM unit. Increasing s by Δs changes the complete bill by:

`ΔC / C = −p × Δs × d / (1 − s × d)`.

All inputs in this test are hypothetical; p refers only to the eligible basket and is not a measured national parts share. It assumes comparable quality/fit and no change in labor, supplements, calibration, time costs or quantities.

Example: p40%, s30%, d40%. A five-percentage-point sourcing shift lowers the whole bill by **0.91%**. Reaching a3% whole-bill saving requires **16.5 percentage points** of substitution, before any offsetting cost increases. Across the documented grid, results differ substantially. LKQ's reported APU is not used to set s; its definition/population does not establish this basket's quantity mix. `parts_substitution_hurdles.csv` exposes every input.

## New calculation2: the salvage offset must be measured in dollars

At the simplified economic boundary, C=V−S_net. For a hypothetical vehicle worth$10,000, a3% repair saving requires:

| Net salvage / pre-loss value | Boundary repair bill | Repair saving | Required net salvage increase |
|---|---:|---:|---:|
|20%|$8,000|$240|12%|
|30%|$7,000|$210|7%|
|40%|$6,000|$180|4.5%|

These ratios are illustrative, not an estimate of actual recoveries. A3% increase in salvage is not automatically enough to offset a3% repair saving. Absolute pre-loss value cancels from the proportional calculation, but must be controlled when estimating real changes.

With the current calibrated cohort distributions, fixed carrier allocation and unchanged historical fit, the aggregate FY27Q1 unit-neutral expected-salvage increase for a3% repair reduction is **9.15%**. This is a conditional root of our existing model, not independently measured elasticity or evidence salvage will rise that much. The solver isolates assignment/selection quantities; it does not require a parallel realized-price increase. The separate illustrative revenue case assumes both expected and realized salvage move by that amount and is clearly labelled.

## Quarterly integration

Reference reused from the existing architecture: realized insurance prices +3.7% versus each prior-year quarter; expected salvage unchanged; neutral carrier allocation; unchanged paid-service adoption/fees; international Q4 growth continued; other-US and purchased revenue flat. All are scenario assumptions, not guidance. Historical dollar/component allocations remain frozen. Repair−3% and salvage+3% shocks below are deliberately round diagnostic stresses, **not extracted from PartsTrader**. Salvage shock applies to both expected and realized recovery; realized prices compound on the reference1.037 factor.

FY27Q1 outputs:

| Case | Insurance units YoY | Insurance RPU including assumed services YoY | Global legacy service revenue | Change from reference |
|---|---:|---:|---:|---:|
| Reference | +0.06% | +1.52% | $1,025.1m | — |
| Repair costs−3% only | −3.88% | +1.20% | $992.0m | −$33.2m |
| Expected/realized salvage+3% only | +1.37% | +2.92% | $1,046.3m | +$21.1m |
| Both | −2.62% | +2.62% | $1,012.4m | −$12.8m |

Joint interaction is −$0.71m, so summing isolated effects is not exact. Source components and all four quarterly outputs are in `quarterly_cases.csv`; core RPU and title/delivery contributions are separate. RPU including services uses the inherited unmeasured$55 per-sale assumption.

The joint case produces $1,175.6m legacy total revenue, $4.4m below JPM's dated ex-ACV Q1 forecast of$1,180m, or about0.38%. Its $7.5m difference from CapIQ total is conditional on compatible acquisition treatment. **This is not a material, established alpha result.** A $12.8m deterioration from our reference is not the same thing as a $12.8m miss versus consensus. Full-year JPM service and quarterly total comparisons retain their distinct definitions; no quarterly service consensus is invented.

## Timing can reverse the first-quarter sign

An illustrative timing overlay delays only the incremental unit change from the joint shock; the baseline is not lagged again. Auction prices affect sales in the current quarter. Same-quarter realization of100%,50%,0% of the incremental unit change gives Q1 service differences from reference of **−$12.8m, −$2.2m, +$8.4m**, respectively. Remaining incremental units enter the following quarter; beyond-horizon amounts are recorded.

This is a timing sensitivity, not an observed backlog model. It assumes affected sales in each quarter have that quarter's scenario fee economics and unchanged services per sale. The real opening mix, assignment-vintage prices and transition date remain unknown. Insurer revisions could lag actual bids as well. The result demonstrates why the pitch needs a dated trigger and processing evidence before promising a next-quarter miss.

## What can enter the model now

- **Observed/documented:** source-specific qualitative price direction, methodology scope and bidding-workflow descriptions; source availability/rejections.
- **Derived:** substitution hurdles, dollar cancellation and internally consistent scenario/timing results.
- **Assumed:** cohort repair shocks, recovery shocks, price continuation, damage response, source shares/discounts, product fees/adoption, timing and other-branch growth.
- **Unknown:** fixed-scope allowed-cost time trend, matched realized salvage price trend, joint pre-disposition cost-gap distribution and updated expected-recovery timing.

No production forecast coefficient is changed. No public threshold histogram or suitable historical joint holdout was found. The two new auction sources fail the accepted-proceeds gate, so no10–20 record collection or expensive fitting was performed. More listing data would not repair the missing claims denominator.

## Decision

Do not promote the generic repair-relief/salvage-weakness short. New evidence makes a selective aftermarket-substitution mechanism more credible than blanket cost deflation, while also supplying countervailing replacement and recycled-price mechanisms. Strong salvage demand remains a competing positive explanation. A measurable parts-source/operation change linked to marginal claims would be the most useful next input; a matched realized-price series could independently advance RPU even if unit sensitivity remains bounded.

The next acquisition decision should be schema-led: an existing insurer/estimating export with pre-disposition C,V,S_net, estimate stage, disposition and dates, or aggregate gap bins for both repaired and totaled cases. No access is assumed and nobody was contacted. Before any paid/bulk acquisition, require a redacted field list or sample, explicit panel/period definitions, an information-gain case, uncertain cost and a stop rule. Do not pay for a large auction dataset that only adds retail asks, minimum bids or additional images.

## Reproduction

`calculate.py` reuses the existing model, freezes the historical ledger and writes parts/decision hurdles, quarterly cases, interaction and timing cases. `results.json` records model/source hashes and checks; `scenario_inputs.json` records all forward assumptions. Arithmetic, root, historical-base, revenue identity and incremental-timing conservation checks passed. These checks are not predictive validation. Prior empirical failures and unrelated repository changes remain untouched.

## Subsequent parts-mix segmentation

See [MIX_SEGMENTATION.md](MIX_SEGMENTATION.md): CCC aftermarket usage rose while recycled usage fell in 2025; Mitchell repaired-part share rose. Separate sourcing, operation counts and labor-dollar shares. These observations do not validate a positive salvage-demand coefficient or the prior illustrative repair/salvage shocks.

### Cohort test follow-up
[COHORT_TEST.md](COHORT_TEST.md): source-reported declines within age groups rule out between-age composition alone. Full age × damage/component test remains unperformed for lack of joint data; total-loss selection within age remains viable. Mitchell provides a competing shop-utilization/margin mechanism, not a calibrated coefficient.
