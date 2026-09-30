# Testing the 5.5-point adoption scenario and Bidmate evidence

29 September 2026. User authorized public research, not outreach, account creation, paid access or bulk collection. Prior parameter audits were reused. No model coefficients or revenue outputs changed.

## Adoption: what now supports the scale, and what does not

Reinspection of saved CCC Figure 38 gives aftermarket replacement-dollar shares of 21.3%, 19.0%, 18.0%, 19.7%, 21.0%, 22.7% in 2020–2025. The increase is 4.7 percentage points from 2022 but only 1.4 points from 2020. Recycled spending share is 9.9% in 2022 and 10.5% in 2025. These observations support multi-year aftermarket growth/recovery, not necessarily recycled displacement. [CCC source](https://www.cccis.com/reports/crash-course-2026).

The existing 5.5 pp input instead represents a future physical-source shift inside a hypothetical eligible basket, fully applied in FY27: 4 pp from OEM and 1.5 pp from recycled. Dollar-share history cannot validate either the denominator or the split. Starting from the 2022 trough alone would overstate evidence for a persistent secular trend. Historical 2022–2025 gains are already embedded in the latest starting point.

A conditional route to a smaller national footprint is concentration. If the eligible basket represents fraction g of ALL replacement quantities, weights remain fixed and nothing changes outside it, national AM quantity share rises by g × 5.5 pp:

| Eligible quantity fraction, assumed | All-parts quantity increase, derived |
|---|---:|
| 25% | 1.375 pp |
| 35% | 1.925 pp |
| 50% | 2.750 pp |
| 75% | 4.125 pp |

The 35% example is close to the roughly 1.9 pp change derived from CCC's rounded 2024–2025 count table. It is a measurement target, not evidence that eligibility is 35%. Quantity eligibility is distinct from the adapter's 40% eligible repair-bill DOLLAR share; both would need to reconcile in the same component panel. Do not choose g merely to make 5.5 fit.

Alternatively, investigate a multi-year cumulative 5.5 pp endpoint with measured annual increments and quarterly timing. That changes the revenue path; it cannot inherit the current immediate full-year downside. No such adoption path has been estimated in this pass.

Mitchell's 2026 discussion reports approximately +1.5 pp US utilization of aftermarket, recycled and remanufactured parts together, with more consistent parts supply. That supports broader alternatives, not a 5.5 pp AM-only increase or recycled-to-AM substitution. [Primary transcript, pp3–4](https://www.mitchell.com/print/pdf/node/30026).

State Farm's current policy accepts specified certified non-OEM component categories but also recycled parts. It supplies an eligibility gate, not an adoption rate. Earlier policy rollout dates surfaced in trade reporting are already historical and not a new FY27 catalyst. [Current policy](https://www.statefarm.com/claims/auto/replacement-parts).

## Bidmate: evidence of actual calculation methods

The public May 2008 Bidmate newsletter describes two approaches: deduct chosen overhead and profit from estimated parts value, or apply a configured cost-of-goods percentage. Users can use fixed or percentage settings and adjust them using their own results. Scrap, cores and minor parts can be added as an ancillary recovery allowance or inventoried separately. Its screenshot settings are examples, not measured industry parameters. [Original newsletter](https://products.car-part.com/newsletters/bidmate/bsn20080501.html).

The April 2007 example uses $1,500 expected parts value and $500 vehicle cost (about 33%). That is gross sales/acquisition arithmetic, not 3× net contribution/hammer. This provides a worked mechanism, not validation of 1.5×. [Original newsletter](https://products.car-part.com/newsletters/bidmate/bsn20070401.html).

Analytical implication: the response also depends on the purchasing rule. For a fixed acquisition/sales ratio B=cS, percentage changes in B follow percentage changes in S. If B=S−fixed costs−fixed required profit, dollar changes pass through differently. Thus a contribution/bid ratio alone does not identify auction-price elasticity; realized prices additionally depend on competitors. Do not infer the existing 25% exposure or 1.5× response simply from software's ability to calculate them.

## Reports that can replace assumptions

| Publicly documented report / data | What it could establish with an authorized recycler export | Remaining gap |
|---|---|---|
| Inventory Analysis | Acquisition cost, projected/current sales, stock age and break-even; isolate vehicle cohorts | Confirm fee/tow scope; distinguish cash recovery, accounting profit and net contribution |
| Projected Sales Comparison | Compare Bidmate/Partmate/Checkmate projections against results | Detailed documentation returned HTTP401; no user data acquired |
| Buyers Profitability / Vehicles By Detail | Buyer and vehicle-level purchasing outcomes | Public index confirms report availability, not its complete fields or population |
| 20 Popular Collision Parts | Identify frequently sought collision components and corresponding stock | Inventory/search data are not sales or contribution weights |
| Advanced Bidmate request data | Requests by interchange, locally scaled from wider marketplace searches | Searches are not unique purchases; need conversion, fulfillment, duplication and stock controls |

[Report index](https://products.car-part.com/checkmate/training_reports.html). [Inventory Analysis documentation, pp49–50](https://products.car-part.com/trainingdocs/checkmate/Checkmate_2025R3_NewFeatures.pdf). The latter explicitly distinguishes projections, sales to date and remaining inventory, and recommends older entry cohorts for cost-of-goods analysis. Screenshot values are not admitted as a representative sample.

The [20 Popular Collision Parts announcement](https://products.car-part.com/newsletters/scoop/cps20240910.html) also identifies a competing explanation: parts without suitable grades or visible prices may be filtered out or passed over for another source. Lower recycled usage can reflect listing/fulfillment problems, not just cheaper aftermarket supply. [Advanced Bidmate explanation](https://products.car-part.com/newsletters/scoop/cps20140407.html) confirms global request statistics are algorithmically scaled to a yard; do not treat those scaled figures as national demand counts.

## Concrete next acquisition, prepared but not sent

Request an existing anonymized export from a willing Bidmate/Checkmate recycler, with linked donor IDs, actual hammer and fees/tow, acquisition dates, projected parts sales, actual sales/returns, remaining stock, component/interchange and fulfillment costs. Compare cohorts with equivalent time to sell; include weak/unsold vehicles. Identify which components have an accepted aftermarket alternative. A demonstration extract establishes fields; multiple representative cohorts are needed for coefficients.

Compute exposed contribution / total contribution for the 25% question, and total pre-acquisition net contribution / hammer for the 1.5× question. Recover bid-rule settings as well, since the ratio is not itself a behavioral elasticity. Separately ask Car-Part whether anonymized aggregate request-to-sale/stock statistics are available; access and commercial terms are unknown.

For CCC tomorrow: request matched component/carrier/age quarterly quantities and available-source data to measure eligible g, its baseline source shares, growth, and which source lost share. Ask specifically whether any measured subgroup has grown by 5.5 pp within a year, and whether that subgroup is large enough in quantity AND bill dollars to match the scenario. Request contrary/stable groups as controls. Avoid asking the interviewee simply to endorse 5.5.

## Status

This pass found useful operational evidence and a concrete report-based acquisition route. It did not obtain live recycler transactions or independently substantiate 25%, 1.5×, or the full-year 5.5 pp forecast. Further empirical progress requires a compatible export or published dataset, not additional flexible fitting. Raw public source captures and hashes are preserved; `observations_and_hurdles.json` separates observations from conditional arithmetic. Exact searches and the HTTP401 failure are in `source_manifest.json`.
