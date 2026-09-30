# Aftermarket substitution: an explicit bridge into Copart revenue

**Parameter audit (29 September):** the hypothetical source mix, 40% eligible repair-bill exposure, 25% donor exposure and 1.5× contribution multiplier are not measured CCC inputs. New primary evidence constrains total parts spending but does not validate these parameters. See [parameter provenance and offset tests](../../docs/aftermarket_parameter_audit_2026-09-29/README.md) and the linked CCC interview brief.

**CCC data update:** [New age/body calibration and connected revenue scenarios](../ccc_age_body_2026-09-29/README.md) incorporate the user-supplied September 29 workbook. Original scenarios below remain the prior comparison; do not mix their reference with the new outputs.

29 September 2026. Additive extension of `../revenue_architecture_2026-09-28/`; historical calibration and existing outputs are unchanged.

**The mechanism can produce material downside to both units and RPU. Available evidence does not yet identify the size, or guarantee both signs.** This implementation replaces arbitrary repair/salvage shocks with explicit component transfers, donor economics, competing bids and stabilizing feedback. Every new behavioral input remains an assumption. No empirically validated forecast or equity-price implication is claimed.

## Results and the pitch hurdle

All deltas below are relative to the saved FY27 reference: $4,105.80m legacy service revenue, +3.7% uniform realized insurance auction prices, unchanged decision-stage salvage, neutral carrier allocation, international continuation and unchanged other branches. The reference itself is conditional. Source transfers are **additional FY27 physical substitutions within an assumed eligible component basket**, not a replay of observed 2024–25 changes already embedded in history.

| Conditional full-year case | OEM → aftermarket, pp | Recycled → aftermarket, pp | Complete repair cost | US insurance units | US insurance all-in RPU | Global service delta | Gap to dated JPM services |
|---|---:|---:|---:|---:|---:|---:|---:|
| Small shift | 2.0 | 0.5 | −0.50% | −0.84% | −0.25% | −$33.86m | +0.27% |
| Larger shift | 4.0 | 1.5 | −1.03% | −2.06% | −0.89% | −$90.66m | −1.13% |
| Large stress | 6.0 | 2.5 | −1.56% | −3.27% | −1.51% | −$146.28m | −2.50% |
| 3% JPM-miss hurdle | 4.0 | **3.17** | −1.11% | −3.30% | −2.16% | −$166.67m | −3.00% |

JPM's September 11 FY27 service forecast is $4,061m, explicitly excluding ACV. The source file/hash was rechecked; no newer local JPM report was found. This is a **dated named benchmark**, not verified current consensus or what the stock prices in. CapIQ's unresolved acquisition/service perimeter is not used to claim a miss. The 3% threshold is an analytical materiality choice, not a user-specified investment criterion.

The hurdle requires removing **31.7% of recycled quantities in the assumed substitutable basket**, which begins at a 10% physical recycled share. It also requires the donor exposure, auction transmission, price expectations and selection assumptions below. This is a reverse-solved requirement, not an estimate. The rounded published 0.6 → 0.5 recycled counts cannot validate a 15%, 25% or 31.7% causal decline.

The larger case gives $4,015.15m services. Its $90.66m decline comprises **$63.68m from fewer units, $27.54m from lower all-in fees per unit, and a +$0.57m multiplication interaction**. Fees use the inherited posted fee bands; an auction-price decline is not passed one-for-one to revenue. Fixed fees and assumed ancillary fees remain. Q1 RPU still grows **0.62% year over year**: a negative thesis contribution does not automatically mean outright falling reported RPU.

## What is actually assumed

| Input | Value in the three illustrative cases | Evidence status |
|---|---:|---|
| Eligible basket's share of the complete repair bill | 40% | Assumed; excludes all other operations |
| Initial physical OEM / aftermarket / recycled mix within that basket | 65% / 25% / 10% | Assumed; NOT CCC dollar shares |
| Equivalent delivered prices versus OEM | 1.00 / 0.50 / 0.60 | Assumed; no matched recycled price established |
| Donor's expected net parts contribution exposed to this basket | 25% | Unknown; mechanical parts, scrap and other demand held constant |
| Total expected net parts contribution / donor hammer bid | 1.5× | Assumed; contribution is after variable fulfillment costs, before acquisition |
| Recycler influence on marginal auction prices | 50% | Assumed reduced-form transmission weight; NOT buyer/winner/domestic share |
| Rebuilder repair bill / donor hammer bid | 1.0× | Assumed; same percentage saving as insured repair basket |
| Extra repaired-job demand captured by the eligible market | 100% | Assumed; all converted totals treated as completed repairs |
| Price support per log decline in modeled total-loss supply | 0.25 | Assumed, tested at 0 and 0.5 |
| Insurer expected-salvage response to realized-price shock | 100% | Assumed immediate update; zero-update case also shown |
| Claims following inherited threshold response | 100% | Calibrated levels, unvalidated derivative; 50% and 0% cases shown |

These are transparent scenarios chosen to expose dependencies, not central estimates, confidence intervals or probabilities. Uniform exposure across US insurance cohorts is an additional approximation; body, age, component and destination exposure have not been measured.

## How the connection works

For fixed physical quantities and equivalent-quality prices, basket cost is `Σ source share × price`. Moving OEM and recycled quantities separately into aftermarket gives:

`repair change = eligible bill share × (new basket cost / old basket cost − 1)`.

The larger case moves 4 OEM and 1.5 recycled units out of a hypothetical 100-component basket. Cost falls from $8,350 to $8,135; weighting this by 40% produces a **1.03%** complete-bill saving. It requires aftermarket to be cheaper than the displaced component. Recycled parts can instead be cheaper; a test confirms that such substitution can increase repair costs.

The engine's economic decision rule compares repair cost with vehicle value less expected net salvage. Cheaper repair and lower expected salvage both reduce totaling. The actual distribution near that boundary remains unobserved; no historical refit was performed.

For the price closure, let `r` be recycled quantity retained, `J` repaired-job demand relative to reference, `Q` total-loss supply relative to reference, `e` donor contribution exposure, `L` contribution/bid ratio, `w` auction transmission weight, `B` rebuilder repair/bid ratio, and `s` the positive repair saving:

`recycler bid change = e × L × (r × J − 1)`

`auction price change = w × recycler bid change + (1−w) × B × s − k × log(Q)`.

This is a reduced-form **scenario closure**, not an auction-clearing model estimated from bid data. The solution uses the equal-quarter average price shock, feeds the specified fraction into insurer expected salvage, and reruns selection until consistent. Modeled insurance total losses proxy donor availability in the scarcity term; other donor sources and geographic exposure are not estimated. Source prices stay fixed: further recycled-price adjustment, labor, supplements, inventory liquidation and exporter reactions remain outside this closure.

In the larger case, extra repairs recover some demand, leaving eligible recycled demand down about 14.5%. The assumed recycler maximum bid falls 5.43%, while rebuilder willingness to pay rises 1.03%. Scarcity adds about 0.52 percentage points of price support. The net uniform auction shock is **−1.68% relative to reference**; changed selection takes aggregate selected ASP down about 1.93%. The reference's +3.7% price continuation remains separately identifiable.

Fewer donor vehicles and more repaired vehicles both stabilize donor economics. Consequently the proposed downward spiral is not automatic. Even the direct multiplication of lower units and lower RPU has a positive cross term relative to summing isolated declines.

## Robustness and timing

Holding the larger source transfer fixed:

- Half the claims follow the inherited switching rule: **−$62.82m** services. No claims switch: **−$31.55m**.
- Recycler auction transmission falls from 50% to 10%: **−$27.38m**, with **RPU +0.19%** versus reference. This is a direct counterexample to guaranteed joint downside.
- No scarcity support: **−$104.27m**. Stronger scarcity response of 0.5: **−$79.42m**.
- Insurers have not updated expected salvage: **−$70.74m**; the repair-cost channel remains active.
- Only OEM is displaced (4pp): **−$20.99m**, with RPU **+0.25%**. Aftermarket growth alone does not establish donor impairment.
- Lower the inherited insurance share of US services from 90% to 80%: downside becomes **−$80.58m** versus that case's own reference.

Delaying half the incremental unit effect by one quarter reduces the larger case's FY downside to **$83.05m** and Q1 downside from $22.91m to $14.93m. Delaying all of it gives $75.43m FY and $6.96m Q1 downside. Deferred units are conserved beyond year-end. This overlay keeps current-quarter fee economics and is not a measured physical backlog forecast. No dated adoption trigger, assignment lag or insurer revision lag has been established.

## Evidence decision and next use

The existing CCC observations support researching a sourcing shift. They do not establish same-component substitution, a causal repair saving or a donor bid elasticity. Newly checked recycler systems identify a better evidence route: **component sell-through, net contribution and donor bid records**, rather than more auction listings. See [EVIDENCE.md](EVIDENCE.md) for source admissions, searches, disconfirmation and the precise interview request.

The model now gives the pitch a quantitative conditional claim: *additional substitution can pressure both total-loss assignments and fee yield if donor economics weaken enough to overcome rebuilders and supply scarcity*. A $90.7m service headwind is possible under the larger illustrative case; a 3% miss against the dated JPM benchmark needs substantially more recycled displacement under these parameters. Neither amount is evidence-backed forecast alpha yet.

For the CCC interview, prioritize the **magnitude of recycled displacement within eligible components and near-threshold claims**, rather than another national aftermarket percentage. To validate the RPU leg, the missing observation is the affected donor's contribution and the response of marginal bids. One cannot be inferred from the other.

## Files and checks

`inputs.json` records assumptions; `bridge.py` connects to the existing architecture. `scenario_summary.csv`, `quarterly_results.csv` and `scenario_details.json` preserve results and channel accounting. `direct_shock_grid.csv` separates required repair/price shocks from parts assumptions. `materiality_hurdle.json`, `incremental_timing.csv` and `allocation_sensitivity.json` retain the bounded sensitivities. `manifest.json` hashes inputs and reused sources.

Run `python3 model/aftermarket_bridge_2026-09-29/bridge.py`, then `python3 model/aftermarket_bridge_2026-09-29/test_bridge.py`. **28 checks passed**, including an independently hand-calculated basket, saved-reference parity, zero-shock behavior, population/ledger conservation, sign-reversing cases and hurdle accuracy. These validate arithmetic and implementation, not the causal coefficients. Spreadsheet presentation remains with Fable.
