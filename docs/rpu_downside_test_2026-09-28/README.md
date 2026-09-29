# Next-quarter negative RPU: price, selection and offset hurdles

28 September 2026. Target: FY27Q1 (August–October 2026), compared with FY26Q1. Existing data and small local calculations only. These are conditional tests, not an adopted −2% forecast. They test what would have to change before collecting more evidence.

## Results

**A price-driven −2% RPU outcome requires roughly a 3.3–5.5% uniform auction-price decline in our illustrative distributions.** The reference case requires −4.09%. At −5% prices, its RPU falls 2.45%. This is not a statistical confidence interval or a prediction: it spans 36 assumed distributions and buyer/seller configurations, retaining the existing $55 assumed ancillary revenue per unit and unchanged posted schedules.

The reference distribution uses median $3,500, log-sigma0.8, 50% preferred buyers and a 4% seller fee. None of those mix/contract inputs is established as Copart's actual population. Exact integration over posted bands is preferable to applying a fee to average ASP: it counts vehicles crossing each threshold. Only a uniform price shift with unchanged shape is tested. A change in mean ASP caused by vehicle composition can have a different fee effect.

Existing insurance selection engine, FY27Q1 versus FY26Q1:

| Conditional change | Selected insurance ASP | Insurance sale-equivalent units | Insurance RPU including assumed services | Insurance service revenue |
|---|---:|---:|---:|---:|
| Existing fleet roll only | −0.01% | +0.06% | −0.08% | −0.02% |
| Realized salvage prices −5%, expectations unchanged | −5.01% | +0.06% | −2.45% | −2.38% |
| Repair costs −3% | −0.59% | −3.88% | −0.37% | −4.24% |
| Expected and realized salvage values both −5% | −5.16% | −2.04% | −2.53% | −4.52% |
| Realized salvage prices +3.7%, expectations unchanged | +3.69% | +0.06% | +1.52% | +1.59% |

These engine outputs are **insurance only**, with neutral carrier allocation, assumed common carrier economics, unchanged $55 service revenue per sale and same-quarter sale-equivalent treatment. They are not all-U.S. forecasts and do not incorporate a measured assignment-to-sale delay. FY27Q1 differences include the existing small fleet roll; `selection_cases.csv` also gives RPU differences from that reference. No new adverse carrier assumption creates these outcomes.

## Why selection matters

The engine totals a vehicle when repair cost exceeds vehicle value minus expected net salvage recovery. If repairs become cheaper, borderline claims become repairable. The surviving auction population is more severely damaged under the engine's assumed damage/recovery relationship, and its salvage prices are somewhat lower. Here that produces a large unit effect and a relatively small RPU effect. It does not justify the earlier intuition that more severe damage must increase fees.

If salvage recovery falls, the insurer expects to recover less by declaring a total loss. The repair-cost threshold for totaling rises, reducing total losses. If realized auction prices also fall, Copart earns less per surviving sale. Thus units and RPU can fall together: they are not invariably a hedge. However, this next-quarter result assumes expected recovery adjusts promptly and affected assignments sell in the quarter. Slower insurer updates or processing would delay the unit effect.

**The magnitude of that unit response is not independently validated.** The engine's marginal damage distribution and perfect within-cell damage/recovery rank relationship are assumptions. Calibrating an age-specific total-loss rate does not validate its response to a new shock. The price-only fee calculation and the selection model also share the fee schedule: agreement near −2.45% is not independent empirical confirmation.

## What the comparison base and evidence say

- FY26Q1 U.S. service revenue was $855.534m. The November20,2025 call, lines208–210, reports U.S. fee RPU +7.5% and insurance ASP +8.4%. Those are growth rates, not the base RPU/ASP dollar levels. A prior +7.5% does not mechanically imply a future decline, and it must not be subtracted from a forward scenario already measured relative to FY26Q1.
- The September10,2026 call, lines217–220, reports Q4 U.S. insurance ASP +3.7%, all-US ASP +4.2%, noninsurance ASP +5.9%. These are different populations and quarters. They are not compatible measurements of all-US fee-vehicle prices, nor evidence of a coming 4–5% price decline. Latest reviewed company evidence therefore challenges, rather than validates, the price-down scenario.
- The same call, lines207–214, reports dealer and bank/fleet unit growth, alongside declining purchased Copart Direct units. Do not infer fee-vehicle mix from combined purchased/fee volumes. Neither these disclosures nor our fleet roll establish a large negative all-US mix contribution next quarter.
- Pricing-anniversary and service-identification limitations remain in `docs/rpu_composition_2026-09-28/README.md`. No old fee increase is newly lapped again in this calculation.

## If prices do not fall, how much additional weakness is needed?

For an explicitly assumed ancillary share `a` of base RPU, total growth equals `(1−a) × core growth + a × ancillary revenue-per-sold-unit growth`. At flat core prices/fees, a −2% total RPU target requires ancillary-per-unit revenue to fall 40%, 20% or 13.3% if its starting share is respectively 5%, 10% or 15%.

The positive-price case requires an even larger contraction; exact hurdles are in `offset_hurdles.csv`. Each row rescales the base service dollars to its assumed share before calculating the price contribution. These shares are not measured, and the exercise does not assert service contraction. It makes clear why growth in adoption merely stopping is not enough: existing revenue remains. No delivery collection was reopened.

For all-US scale only, at an assumed −1% fee-unit change, −2% versus +2% RPU means **$830.0m versus $863.9m next-quarter U.S. service revenue**, a **$33.9m difference**. This identity uses the actual $855.534m base, not the uncertain insurance split. It is not a consolidated forecast or a measured consensus gap; other revenues are outside this calculation.

## Decision and next discriminating evidence

The most concrete negative-RPU route from these tests is **weaker salvage realizations**, especially if insurers also reduce expected recoveries. Cheaper repairs is mainly a unit thesis in the current engine. Existing fleet roll is too small to explain −2% RPU here. The positive-price case remains a live competing outcome.

Next bounded discovery should seek evidence about **within-cohort salvage prices**, rather than assume a marketwide decline: (1) completed salvage proceeds from auction/insurer sources; (2) dismantler procurement and parts resale economics; (3) exporter landed costs, buyer demand and destination restrictions. These actors observe different links in bidder willingness to pay. Used-wholesale indices can provide context but are not direct salvage-price estimates. Ranked ideal observation: realized sale price, age/model, damage, title and sale date for compatible year-ago/current samples, plus whether unsold vehicles are excluded. Source availability must be checked before collection. No broad listings scrape or paid acquisition is authorized by this note; previously rejected pre-auction price fields remain unusable as realizations.

## Reproduction and provenance

`run.py` reuses the exact fee-integrator definitions from `docs/auction_price_test_2026-09-28/run.py` without executing or overwriting its original experiment, and calls the existing `model/revenue_architecture_2026-09-28/model.py`. Source hashes are in `results.json`; inherited model input provenance remains in that model's manifests. Outputs: `price_hurdles.csv`, `selection_cases.csv`, `offset_hurdles.csv`.

Checks: all 36 inverse price roots hit −2% RPU within 1e−10; unchanged prices give unchanged RPU; positive/negative price shifts have the expected signs. Selected engine cases were refined from 1,024 to 2,048 arithmetic nodes with RPU growth differences below 0.02 percentage points. This verifies numerical stability, not the economic assumptions. No historical schedule vintage, service base, claim curve or production forecast was changed.
