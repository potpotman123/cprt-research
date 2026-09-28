# Input, population and assumption register

As of 28 September 2026. Source hashes in manifest.json. This register governs interpretation of assumptions.json and the output tables. No fresh source verification or external collection was performed in this integration pass.

| Input / parameter | Population, date and basis | Status / source | How used |
|---|---|---|---|
| FY25/FY26 US and international service dollars | Fiscal quarters ending October/January/April/July; USD millions; service revenue only | Filing-derived controls in legacy inputs; source paths exported to historical_controls.csv | Historical comparison and one FY26Q4 level anchor |
| Purchased-vehicle revenue | Same financial periods | Reported control, explicitly excluded | Guard against treating all sold units as fee units |
| 90% US insurance service share | FY26Q4 service dollars | Assumption, inherited; not the insurance unit share | Sets insurance anchor; remaining 10% assigned to mutually exclusive other-US perimeter |
| Fee sales and claims absolute scale | Modeled US insurance consignment-equivalent activity | Derived from assumed split and all-in fee economics | Normalized units, not independently observed counts |
| Fleet births and survival | CY2023–27 source stock estimates, age/body detail | Existing fleet research; future births fixed at CY2025, fitted survival | Fleet total change is a proxy for covered exposure change; no separate fleet growth multiplier |
| Relative claim weights | Six age × four body cells | CCC-selected-mix calibration with modeled body weights, hybrid populations | Historical reference weights; shifted by relative changes in fleet claim-weighted composition, then normalized |
| Broad age mix of total losses | Noncomp through October 2025, four groups | CCC Figure 6, saved image and transcription | Calibration reference, not independent forecast inputs |
| Within-7+ age shares | All-loss CY2025 split 7–9/10–12/13+ | CCC annual chart; transferred to noncomp population by assumption | Retained older internal distribution |
| TLF targets | Six CY2025 all-loss age buckets | CCC chart transcription | Calibration only; not an independent extra forecast growth driver |
| Selected vehicle values | CCC noncomp valuations through October2025 | Four held-out observations subsequently used as calibration targets | Defines selected-value constraints; not unconditional per-vehicle ACV measurements |
| Repairable mean targets | All-loss CY2025 age0–6 $5,721; age7+ $3,682 derived | CCC report and prior research | Two fitted dispersion targets; no claim of measured latent distributions |
| Cohort car ACV / log repair median / sigma | Six age buckets; four body ratios applied | Fitted age-constrained output | Frozen calibration passed into quarterly engine; not refitted to quarterly dollars |
| Body repair ratios | Car/SUV/pickup/minivan, transferred scenario costs | AAA/CRSS working proxies; not measured national repair premiums | Multiplicative repair differences; source limitations retained |
| Body value ratios | Small older-vehicle retail convenience panel; van assumed | Proxy, not insurer values | Within-age relative values; calibrated selected mean accounts for selection |
| Claim frequency quarter drivers | US insurance claim events per exposure proxy | Assumed 1 throughout; explicit editable arrays | Reported-frequency convention already includes filing; no second coverage/filing factor |
| FY25 seasonal template | Geography service dollars, relative to Q4 | Observed revenue shape transferred to activity by assumption | Proxy, includes historic fee/mix/trend effects; not identified claim seasonality; repeats by fiscal quarter |
| CAT treatment | Combined claims pool | No separate incremental CAT factor | No claim of ex-CAT forecasting; avoids mismatched separate uplift |
| Carrier weights and allocations | Friend scenario; historical path and future PGR runoff | Proxy and assumptions; not verified assignments | Forecast Q4 carrier weights frozen, other allocations frozen, PGR inherited; common cohort mix across carriers |
| Routing and consignment fractions | US insurance fee-unit perimeter | Both 100%, explicit assumptions | Eligibility and ownership mapping once; potentially embedded in effective capture |
| Timing | Sale-equivalent capture | Explicit neutral convention | No second lag; physical inventory unavailable rather than invented zero balances |
| Recovery / net salvage | Gross recovery 40%→20% as damage rank rises; seller4% deducted | Unmeasured functional assumption | Same selected states drive total-loss decision and auction price; other net costs omitted |
| Buyer schedules | September2026 non-clean standard vehicle secured/prebid fee grid | Posted schedule data in legacy inputs | Applied per selected price; historical schedules not reconstructed |
| Buyer mix, fixed fee, seller fee | 50% preferred, $110 gate/environment, 4% seller | Assumptions / inherited conventions | Buyer fees distinct from seller proceeds; no contract concession claim |
| Title services | Insurance sales-associated title jobs | 50% × $50 net incremental, assumed | Sale-attached recognition; bundled-title switch suppresses incremental title dollars if included in seller fees |
| Delivery services | Insurance sales-associated external jobs | 10% × $300 gross, zero waiver, assumed | Same-quarter attached recognition; explicit fee-waiver deduction; not verified gross accounting or adoption |
| Other-US activities | Noninsurance consignment, related services and non-unit services, excluding insurance branch | Base residual dollars, $500 activity-equivalent fee and flat drivers | Equivalent counts not true auction units; noninsurance service attachments stay in this branch |
| International | Aggregate service perimeter, all relevant service activity | $750 equivalent fee, flat activity/fee/FX multipliers; seasonality proxy | No inferred real unit census; fee/unit/FX factorization provisional; contract conversion not separately forecast |
| Acquisition timing | ACV Auctions; first included month January2027 | Existing management projection and assumed monthly timing | Separate optional overlay; no fresh closing-status assertion |
| Acquired service classification/eliminations | Post-control external service revenue only | Missing: null, not zero | Consolidated-service output remains unavailable after assumed close until populated |

Dollar overlap controls: insurance branch owns its modeled core fees, attached title and delivery only. Other-US owns all other US service revenue including noninsurance ancillary activity and non-unit services. International owns its geography. These exclusivity boundaries are imposed model definitions, not disclosed company component splits. If better service data span multiple branches, allocate them before adding them.

The inherited gross delivery fee may require net presentation; this is an unresolved accounting assumption, not permission to treat transportation billings automatically as revenue. The service normalization depends on that choice. Changes to historical base assumptions require an explicit normalization rerun; forecast-only changes leave normalization fixed.
