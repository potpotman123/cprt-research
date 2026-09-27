# CPRT research execution plan: cohorts, claims, auction economics and usable capacity

Prepared September 26, 2026. This is a proposed research pipeline, not an execution report. It supersedes the priority ordering in the earlier discovery plan; its 14 hypotheses remain a reference menu. No new experiments, collection, or workbook rebuilding were performed to prepare this document.

## 1. Objective and architecture

The first objective is to establish whether changing vehicle composition and the diminishing contribution from claims-age mix can support a differentiated investment thesis. The second is to identify operating consequences that a revenue-only model would miss: contribution per vehicle, yard occupancy, throughput, development spending, free cash flow and returns on incremental capital. Repair-cost measurement tests the first mechanism. Delivery and carrier contracts test how the resulting auction value is divided. Usable capacity receives a dedicated operating build, rather than being deferred to a generic CapEx assumption.

The model will be detailed where evidence supports detail. It will not create apparently measured carrier-by-body-by-age-by-yard estimates from unrelated aggregate data. The initial core dimensions are calendar year, age group and body type. Carrier and geography modules connect through explicit allocation assumptions; they become joint dimensions only if data justify that connection.

Proposed forecast resolution: historical annual cohort reconstruction, eight forecast fiscal quarters for the investment horizon and timing, and five annual forecast years for capital requirements and valuation. Longer-lived cohort effects enter transparent terminal sensitivities, not a precisely estimated perpetual growth rate. Annual cohort data alone do not identify quarterly seasonality.

The causal chain is:

**Vehicle cohorts → insured exposure → claims → totaling decisions → Copart assignments → arrivals and processing → sales and pickup → fees and operating costs → capacity additions and working capital → cash flow and valuation.**

Alongside that chain, delivery affects buyer delivered cost and potentially bids; contracts affect allocation and seller charges. Those feedbacks are introduced as bounded scenarios until independently supported.

Every input carries its population, period, unit, source and status: directly observed, derived from observations, fitted, assumed or unavailable. A fitted parameter is not relabeled as measured because the workbook balances.

## 2. What 'best method' means

There is no method that simultaneously maximizes precision, credibility and cheapness. The preferred sequence uses existing work to identify the uncertainty that can change the investment conclusion, then seeks the least expensive evidence that resolves it.

A direct claim panel could be more informative than public proxies but unavailable or expensive. A regression could produce a narrower numerical confidence interval while remaining causally misleading. An algebraic bound can be cheap and decisive without proving the mechanism. Each stage below explains its role and its alternatives; methods change if a better actual source becomes available.

Research costs have three separate components: data/license expenditure, local computation, and assistant effort reviewing sources and resolving definitions. Initial screens assume zero paid-data expenditure. Small tabulations should be inexpensive computationally, but source review can still consume substantial usage. Time ranges later in this document are work caps, not credit quotes. No large collection, paid purchase or external outreach is authorized by this planning document.

## 3. Shared preparation and materiality screen

### S1. Reconcile the existing evidence and freeze the starting version

**Method.** Read the latest handoff alongside the body-mix report, CCC decomposition, vintage-price analysis, fee analysis and their underlying tables. Build a compact discrepancy register. Check definitions and arithmetic from existing outputs before rerunning scripts. Keep raw sources and existing workbooks unchanged. Distinguish annual from quarterly growth, TLF percentage points from percent growth, insurance units from all units, and US metrics from global metrics.

**Why it contributes.** The project contains findings that were subsequently revised. We need one starting interpretation so that subsequent changes reflect new evidence rather than different definitions. In particular, the age-composition contribution, body-mix contribution and model-year price effect must remain separate.

**Alternative and tradeoff.** Rebuilding everything would be costly and would reproduce errors before identifying them. Reading only the final handoff is cheaper but misses assumptions and overstatements. Targeted reconciliation of consequential inputs is the better first pass.

**Output/gate.** One source-and-definition table, a list of unresolved contradictions, and an explicit baseline. Any population mismatch remains unresolved rather than being bridged silently.

### S2. Establish where the thesis would have to differ from expectations

**Method.** Extract units, price/RPU, costs, CapEx and acquisition assumptions from named, dated forecasts already held. Missing driver assumptions remain missing. Use the reverse DCF when available to show combinations of operating outcomes consistent with price; do not infer a unique market belief from one valuation equation. Refresh market data and primary disclosures only when execution requires them.

**Why it contributes.** A negative demographic contribution matters differently if forecasts already assume weak units than if they extrapolate a large secular increase. Long-term valuation impact and near-term estimate revisions are distinct outputs.

**Alternative and tradeoff.** Treating a historical growth rate as consensus is easy but not reliable. A broker's explicit model offers a traceable comparator, although one broker is not the market. Both the named forecast comparison and valuation sensitivity should be shown.

**Output/gate.** A dated expectation map. Do not claim an earnings surprise against an outdated pre-event estimate without labeling that limitation.

### S3. Calculate bounds before collecting new data

**Method.** Construct small, transparent sensitivities around the existing body-mix outputs, repair-cost alternatives, delivery break-even and capacity turnover. Translate each into affected-segment revenue, contribution and group EBIT using ranges for incremental costs. Avoid assuming that a 1% segment revenue change equals a 1% EPS change.

**Why it contributes.** It tells us which uncertain parameter could change the conclusion and which interesting mechanism is probably too small to lead the memo.

**Alternative and tradeoff.** A large simulation of poorly known distributions creates many results without better evidence. Begin with break-even equations and a few defensible parameter combinations. Expand only if nonlinearities or interactions change the ranking.

**Output/gate.** For each mechanism: downside/base/upside range, the parameter most responsible for uncertainty, and the observation needed to narrow it. A provisional relevance screen is roughly 2% of next-12-month group EBIT or 5% of equity value under moderate assumptions, subject to user review. These are prioritization thresholds, not statistical tests. Smaller mechanisms can remain supporting model components.

## 4. Track A — vehicle type, fleet aging and manufacturing-cohort effects

### A1. Define comparable cohorts and inspect the composition evidence

**Method.** Start with cars, SUVs/crossovers, pickups and vans. Use the existing listing classifier and retain an unknown category. Reconcile classification conventions with sales and insurance sources. Tabulate composition by capture date, age, title category and source coverage. Keep repeated snapshots separate from unique vehicle flows. Use the existing CCC age buckets first; single-year ages are justified only where the data support them.

**Why.** The observed transition is primarily toward SUVs/crossovers; applying pickup economics to it could give the wrong answer. Listing composition can also change because one vehicle type stays listed longer or a carrier's allocation changes, not solely because the physical fleet changes.

**Best initial method / alternatives.** Reusing classifications and auditing consequential ambiguous models is cheaper than relabeling every vehicle with a language model. A vehicle-identification-number decoder could improve classification if VINs and legitimate access exist, but it does not fix listing selection or missing exposures. No fresh archive scrape is needed for this first step.

**Output/gate.** Composition tables with coverage, unknown share and classification sensitivities. If the apparent trend disappears under reasonable classification or consistent coverage, revise the premise before estimating economics.

### A2. Reconstruct the exposure entering the claims funnel

**Method.** Use historical sales and survival assumptions to roll vehicle cohorts forward. Reconcile stock totals and age composition against independent fleet observations already available. Then distinguish registered stock from insured vehicle-years, driving exposure and reported claims. Add coverage or frequency data where directly available; otherwise vary them transparently rather than attributing all differences to totaling propensity.

**Why.** A body type can produce fewer auction vehicles because it is less likely to be insured, driven, involved in a reported claim, or totaled conditional on a claim. Those explanations imply different future behavior.

**Best initial method / alternatives.** A cohort roll is more interpretable than extrapolating average fleet age: the same average age can describe very different numbers of vehicles in high-totaling groups. But survival curves fitted to aggregate totals are not uniquely identified. Direct insured exposure by age/body would be preferable if accessible. Until then, competing exposure assumptions are bounds, not measured denominators.

**Output/gate.** Cohort stock and claim-exposure scenarios, showing measured and assumed layers. Do not claim an independently estimated body-specific TLF if its denominator is generated by unsupported frequency assumptions.

### A3. Reassess the historical aging decomposition

**Method.** Reproduce the existing CCC decomposition from its stored tables: changing age weights versus changing totaling rates within age groups. Show alternative decomposition orders or a symmetric allocation of the interaction. Reconcile the chart populations and differences between reconstructed and published totals. Keep the broad 13+ group visible as a limitation.

**Why.** This distinguishes an older claims population from a higher probability of totaling within similar age groups. It also checks whether the claimed fading tailwind is recent, already largely absent, or projected only under the cohort model.

**Best initial method / alternatives.** An accounting decomposition is cheaper and less assumption-heavy than a regression attributing TLF to average fleet age. It is not fully causal: within-group age, damage and carrier composition can still change. More granular source data would improve attribution; a more elaborate regression on the same broad buckets would not necessarily do so.

**Output/gate.** Historical contributions and a separate forward cohort contribution. Never turn 'little recent contribution' into 'a large new negative inflection' without a dated cohort mechanism.

### A4. Determine whether different body types really have different totaling economics

**Method.** Evaluate pre-accident value, estimated repair cost and expected net salvage recovery jointly for comparable age/damage groups. The simplified economic comparison is cost of repair versus pre-accident value less expected net salvage recovery, with relevant additional claim costs and legal/operational rules considered separately. Begin by auditing the existing proxies and calculating the relative repair-cost/recovery combinations that reverse the current result.

**Why.** Higher pre-accident value alone does not establish lower totaling frequency. Repair complexity and salvage recovery could offset it. Paid claim severity, which includes total-loss settlements, is not a direct measure of the cost to repair vehicles that were instead totaled.

**Best initial method / alternatives.** A sensitivity over the uncertain repair/value/recovery relationships is preferable to another fitted probability curve using the same aggregate targets. The superior evidence would be a panel containing insured exposures or claims, body/age, damage, pre-decision repair estimates, valuation and disposition. If unavailable, report partial bounds. A sample of auctioned salvage vehicles cannot identify the probability of entering that sample.

**Output/gate.** A sign map and a list of decisive missing fields. Proceed to intensive collection only if a realistic, obtainable field could settle the sign or material magnitude. If all plausible assumptions leave the effect immaterial, retain a small model adjustment.

### A5. Estimate the fee and contribution consequences with the same cohort weights

**Method.** Combine each cohort's assignment/sale probability with a sale-price distribution, actual fee schedules, seller-fee scenarios and incremental costs. Keep body mix separate from manufacturing-cohort price changes. Compute buyer fees over the price distribution rather than applying a fee to average price. Add title/payment/buyer-tier distinctions only when they materially change the result and can be bounded or observed.

**Why.** The thesis concerns total economics per insured exposure, not just higher auction ASP. The same population must determine both the number of vehicles and their price mix. More valuable vehicles might generate fewer transactions but more revenue per transaction; labor, transport and yard occupancy determine the profit result.

**Best initial method / alternatives.** Existing fee grids and a few bounded distributions are cheap and reproducible. Actual completed-sale distributions are better if accessible. The fitted historical RPU elasticity is a cross-check, not a second additive benefit. Undisclosed seller fees remain sensitivities, and observed price mix cannot establish demand effects by itself.

**Output/gate.** Units, fees, contribution and occupied space-days per 1,000 insured vehicle-years, by cohort where identifiable. If insured exposure cannot be measured, label the exposure base as modeled and also show the observable per-sale results.

### A6. Validate, forecast and compare with expectations

**Method.** Freeze assumptions before reserving a genuinely separate period or source for validation. Do not validate with the listings used to choose frequency ratios. Roll observed birth cohorts forward, vary survival/coverage/future sales, and report age, body and manufacturing-cohort contributions separately. Translate annual effects into quarters using supported assignment-to-sale timing; otherwise provide timing ranges.

**Why.** This determines whether the mechanism forecasts an outcome beyond the data used to construct it and whether it affects the investment horizon rather than only later years.

**Best initial method / alternatives.** A simple forecast with explicit uncertainty is preferable to an overfit joint distribution. If no independent source exists, label the model calibrated and partially checked, not validated. A future observation can serve as a prospective test.

**Output/gate.** An eight-quarter earnings bridge, annual demographic path and a clear counterfactual holding body or age composition fixed. Integrate interactions once; do not add several overlapping demographic penalties to the historical TLF trend.

## 5. Track B — repair costs, claim selection and the meaning of TLF

### B1. Establish which statistic could actually suffer from selection

**Method.** Inspect the definitions of average completed-repair cost, preliminary repair estimates, insurance paid severity and the repair-price index used in the repository. Determine whether each includes total losses, changes its vehicle/damage mix, or prices a defined service basket. Align loss categories, periods and claim-count definitions.

**Why.** The claim that expensive repairs leave the sample applies directly to a repaired-claims average. It cannot automatically be applied to a separately constructed consumer price index. This distinction could invalidate the proposed critique of a particular model input before any computation.

**Best initial method / alternatives.** Reading source methodology is more accurate and cheaper than correlating series whose populations differ. If the existing forecast uses an index unaffected by the proposed sample mechanism, redirect the question to the statistic it actually explains.

**Output/gate.** A population crosswalk and explicit statement of which forecasting inference is being tested.

### B2. Write distinguishable predictions and reconcile counts

**Method.** Compare three explanations: lower growth in comparable repair input costs; expensive claims becoming total losses; and small repairs disappearing through coverage/deductible/filing changes. Reconcile repairable and total-loss counts where populations match. Only then use TLF = total losses / all corresponding claims. A small illustrative distribution can explain predicted signs but is never treated as estimated data.

**Why.** The same average repair cost can arise from several mechanisms with different implications for auction supply. Rising TLF can also accompany fewer total-loss vehicles if the claims denominator falls faster.

**Best initial method / alternatives.** Joint counts, mix and cost movements discriminate better than one repair-cost regression. National correlations or searched lags cannot establish a claim-filing mechanism. If consistent counts are unavailable, present the ambiguity rather than reconstructing incompatible populations.

**Output/gate.** A prediction table identifying which available observation would contradict each explanation. Stop if all observations fit all explanations equally well.

### B3. Seek fixed-composition or pre-decision evidence

**Method.** First reweight available comparable age/body/damage groups to common weights. If that cannot separate repair-cost change from claim disposition, propose a small claim-level sample containing both repaired and totaled vehicles and their pre-decision estimates. Include missingness and selection explicitly.

**Why.** Reweighting tests observed composition cheaply; pre-decision information addresses the missing upper part of the repair distribution. Neither solves unobserved damage differences automatically.

**Best initial method / alternatives.** Existing grouped data are cheaper than a licensed panel, but less precise for matched repairs. A paid panel is justified only after confirming coverage, fields and rights with a sample. More public auction records cannot replace the absent repairable-claims denominator.

**Output/gate.** A supported correction or range for the repair/totaling relationship. If evidence is insufficient, this remains an uncertainty in Track A rather than an independent bullish or bearish adjustment.

### B4. Feed the result back into the forecast

**Method.** Change the relevant repair-cost or claim-selection input and re-estimate the implied total-loss counts while holding unrelated mechanisms constant. Check against Track A so body and age selection are not counted again. Translate assignment timing into sold units and incremental profit.

**Output.** The extent to which corrected measurement strengthens, offsets or leaves unchanged the demographic thesis, with an independently testable next observation.

## 6. Track C — usable capacity, operating costs and CapEx

This track begins with a modest feasibility screen alongside Track A. Full site modeling follows once the unit scenarios and data access are clearer.

### C1. Define the physical operating states and collect the available clocks

**Method.** Distinguish assignment, physical arrival, title/processing readiness, auction, completed sale and physical pickup. Inventory changes with physical arrivals and departures, not merely sales. Split occupied time into waiting for processing/title, waiting for sale, and waiting after sale for pickup where actual timestamps exist. Record the treatment of cancellations, transfers, repeat auctions and vehicles still present at the observation end.

**Why.** This identifies what consumes yard space and which delay can be changed. A sale does not necessarily release a space immediately; faster auctions do not resolve a long pickup delay.

**Best initial method / alternatives.** Actual provider/company timestamps are preferable. A website's first-seen date is not arrival, and disappearance is not verified sale or pickup. Prospectively observing listings could bound a listing interval but cannot recover unobserved pre-listing occupancy. Survival/time-to-event methods are useful only after the clocks and censoring are understood.

**Output/gate.** An operational data dictionary and a classification of measurable, bounded and unavailable durations. No national listing collection unless it can answer the chosen physical-capacity question.

### C2. Separate available land from usable operating capacity

**Method.** Screen at most 12 facilities across explicitly selected conditions: relevant existing operations, potential wholesale conversion, reported expansion and a contrasting location. For each, record source-supported location, owned/leased status, development/operating status, capabilities and any disclosed usable spaces. Check catchment assumptions at several radii. Treat catastrophe reserve capacity separately.

**Why.** National acreage cannot establish whether capacity exists near incremental volume or whether conversion requires spending. Deliberate reserve land is not necessarily idle economic waste.

**Best initial method / alternatives.** A purposive screen answers whether site evidence is obtainable; it is not a representative estimate for the whole network. A full parcel map is expensive and still does not reveal usable spaces, permits or processing bottlenecks. Aerial area can be a bound, not an automatic vehicle-space count. Expand only where geography changes the investment conclusion.

**Output/gate.** A facility evidence matrix and a feasibility judgment. Unknown usable capacity stays unknown. Do not extrapolate 12 facilities to the network without a justified sampling design.

### C3. Translate unit scenarios into occupancy and bottlenecks

**Method.** Build an inventory roll: opening physical inventory + arrivals − physical departures = closing physical inventory. Under reasonably stable flow, average occupied spaces approximately equal daily arrivals multiplied by average occupied days. For growth or catastrophe surges, use the dated arrival/departure profile rather than that steady-state shortcut. Compare space needs with processing/title/transport capacity, and use the tightest supported constraint.

**Why.** This converts Track A's units into resource demand. Fewer but longer-staying vehicles may consume more space. Larger vehicles could consume more area, but body-specific space factors must be measured or shown as optional sensitivities, not assumed as an additional bearish effect.

**Best initial method / alternatives.** Aggregate occupancy arithmetic and a handful of scenarios are enough initially. A discrete-event simulation is more expensive and false precision if arrivals and service-time distributions are unknown. It becomes useful only if measured peaks/queues drive the capital decision.

**Output/gate.** Average and peak occupancy, throughput, days occupied, processing constraints and surplus/deficit by supported geography. If only network totals are available, do not claim local congestion.

### C4. Compare operational improvement with capital expansion

**Method.** Evaluate three ways to accommodate volume: reduce an identified waiting interval, convert/develop an existing site, or add capacity in another location. Model time to implement, spend, operating costs and capacity added. Separate maintenance/replacement, systems/equipment, development and land acquisition. Tie depreciation to placed-in-service assets and useful-life assumptions. Keep leased facilities and lease cash costs visible.

**Why.** This makes CapEx a consequence of required capacity and chosen operating actions. Shorter stays can avoid spending, but may also change storage revenue or require additional labor/technology. Vehicle inventory held for consignment is not automatically Copart-owned inventory for working-capital purposes.

**Best initial method / alternatives.** Historical disclosed projects or specific development costs provide better ranges than a fixed CapEx/revenue ratio. If project detail is unavailable, use comparable cost ranges and explicit uncertainty. Retain a revenue-ratio forecast only as a reconciliation benchmark, not proof of needed spending.

**Output/gate.** Annual maintenance and growth CapEx, cash timing, depreciation, cost per incremental throughput unit and operational alternatives. No presumed project permissions, costs or delivery dates.

### C5. Calculate the return and identify the near-term evidence

**Method.** Compare incremental after-tax operating profit with incremental capital required, and calculate cash payback under each throughput path. For existing spare land, distinguish incremental cash return from an economic return including the land's opportunity cost. Link shorter dwell times to storage revenue/cost consequences. Identify a disclosed opening, conversion, cost change or reporting period that could test the estimate within 12 months.

**Output/gate.** A capacity-to-CapEx-to-FCF bridge. Avoid adding the value of operating land to a DCF whose cash flows already depend on that land. A long-term efficiency possibility without measurable timing remains a valuation sensitivity rather than a near-term catalyst.

## 7. Track D — delivery's direct profit and auction-side effects

### D1. Identify what business is actually being operated

**Method.** Separate inbound towing from outbound delivery; distinguish owned transport, third-party procurement and brokerage. Reconcile what available disclosures say about revenue, direct costs and start-up spending. Do not assign Copart an industry-analogy margin as if it were disclosed.

**Why / method choice.** Route utilization matters differently for a fleet owner than for a broker. Reading the service and accounting descriptions is cheaper and more informative initially than mapping routes for an unconfirmed operating model.

**Output.** A supported service/cost map, with unknown attach rates and costs explicitly bounded.

### D2. Calculate what improvement would justify the spending

**Method.** Model direct delivery contribution and separately the possible auction effects: transport savings, additional buyer participation, hammer-price changes, fee changes and incremental completed sales. Allocate the transport saving among buyer profit, insurer proceeds and Copart earnings rather than crediting all of it to Copart. Include subsidy cases.

**Why / method choice.** Break-even arithmetic can reject unrealistic required benefits before obtaining shipment data. Generic logistics synergy percentages or combined vehicle counts do not establish savings.

**Output/gate.** Required transport savings, delivery adoption or auction improvement. Stop if benefits must exceed defensible ranges.

### D3. Test a specific rollout only if an observable contrast exists

**Method.** Locate documented service eligibility, timing and transport offers. If accessible, compare similar vehicles/routes newly offered the service with eligible not-yet-served comparisons, checking prior trends and concurrent changes. Actual adoption is selected by buyers, so adopter/non-adopter comparisons alone are insufficient. Check route, equipment and timing compatibility before claiming backhaul savings.

**Why / alternatives.** A small credible rollout contrast is more informative than a national correlation between delivery revenue and ASP. Randomized rollout would be stronger but is not something we control. If selection cannot be addressed, retain bounds and descriptive evidence.

**Output.** Delivery EBIT, auction contribution, operational requirements and feedback into Track C. Each saving enters the model once.

## 8. Track E — carrier contracts and buyer-fee responses

### E1. Separate contract scope, new units and retained units

**Method.** Use existing carrier disclosures and contract commentary to distinguish whole-account, regional and incremental-only concessions. Calculate incremental contribution on new units less concessions on the retained book. Keep assignments separate from sales and introduce supported timing ranges.

**Why / alternatives.** The scope of repricing can dominate the profit from a modest volume gain. Scenario arithmetic is the cheapest first screen. Aggregate RPU cannot uniquely reveal undisclosed contract terms; another regression does not solve that missing information.

**Output/gate.** Contract-scope break-even and a list of evidence that could distinguish the cases. Stop at scenarios if no public or legitimately accessible evidence identifies scope.

### E2. Model fees and bidding jointly

**Method.** For a documented fee change, calculate buyer all-in spending, hammer bids, seller proceeds and platform fees under alternative bidding responses. Lower hammer bids do not erase a fee increase dollar-for-dollar. Earnings effects require changes in price-linked fees, additional concessions, volume or costs, which must be shown separately.

**Why / alternatives.** This identifies the actual channel before searching for data. Assuming buyers absorb all charges or insurers absorb all charges is cheaper but prejudges the answer.

**Output.** A transparent distribution of the economic burden and a break-even test for the additional channel needed to change Copart earnings.

### E3. Conduct an event study only after establishing access and identification

**Method.** Require dated fee schedules and comparable completed sales. Assign treatment exposure using pre-event predicted price/category/tier, not realized post-event price. Check pre-trends, vehicle mix and concurrent market changes. A competitor changing fees at the same time is not an untreated control. Buyer tiers may be unavailable; investigate whether bounds suffice before buying data.

**Why / alternatives.** This is more credible than before/after average ASP comparisons. If no comparison group or actual schedule history exists, additional observations cannot rescue the design.

**Output.** A supported fee response or an explicitly unidentified range, linked to carrier contribution rather than added as an arbitrary RPU adjustment.

## 9. Integrate the evidence into one financial model

### F1. Make the operating modules reconcile

Keep three distinct clocks: claims/assignment, physical arrival/departure, and revenue recognition. Buyer fees generally connect to completed sales; other services may connect to towing, storage or processing activity under their actual recognition rules. Do not allocate every service dollar to sold units merely because an RPU KPI divides by sales.

Use indexed unit paths when absolute volumes are not disclosed; the absolute unit level and fee level cannot both be solved uniquely from revenue alone. Label any estimated scale. Reconcile insurance/non-insurance, domestic/international and consignment/purchased-vehicle operations separately. The demographic mechanism should affect only its supported population.

### F2. Forecast metrics beyond revenue

| Operating or financial output | Underlying build | What it contributes |
|---|---|---|
| Claims and total losses by supported cohort | Exposure, frequency and totaling | Separates demographic supply from claim and repair cycles |
| Fee dollars and contribution per insured exposure | Cohort sale probability, fee distribution and incremental costs | Tests whether higher-value vehicles compensate for fewer transactions |
| ASP at constant composition and actual composition | Price distribution with fixed versus changing weights | Separates market pricing from cohort changes |
| Physical inventory and occupied days | Arrival/departure and process-stage timing | Explains space requirements and delays |
| Average/peak occupancy and practical throughput | Usable spaces, dwell time and process bottlenecks | Identifies where volume can grow without expansion |
| Contribution per vehicle and per occupied space-day | Recognized fees and activity-driven costs | Tests whether seemingly attractive units consume disproportionate capacity |
| Delivery contribution and required auction uplift | Transport economics and buyer responses | Distinguishes profitable growth from subsidized activity |
| Maintenance/development/expansion CapEx and depreciation | Supported projects and operating capacity requirements | Replaces an unexplained revenue-percentage forecast |
| FCF, cash payback and return on incremental capital | Operating earnings, investment, funding and working capital | Connects operating discoveries to shareholder value |

Only outputs with adequate inputs receive point estimates. Others remain ranges or unavailable. A forecast's granularity is not evidence of its accuracy.

### F3. Translate into expectations, valuation and a falsifiable memo

Compare next-two-quarter and next-12-month earnings with dated forecasts. Carry supported differences through annual cash flows. Show valuation sensitivity separately for persistent operating effects, temporary investment, acquisition/funding and terminal assumptions. Do not change the multiple simply because the story sounds more negative.

The reverse DCF supplies a boundary: combinations of growth, margins and reinvestment consistent with value. It does not identify which combination investors actually believe. A subtle demographic mechanism may matter because it changes the credibility of long-run growth; that must be shown explicitly rather than inferred from a small near-term revenue effect.

The eventual two-page memo should contain one causal thesis, its strongest discriminating exhibit, an earnings/cash-flow bridge, the competing explanation and a condition that would change our view. If the best result is small or unidentified, report that outcome rather than escalating model complexity.

## 10. Work sequence, bounded first stages and approval points

The following are proposed selectable packages, not work started by this plan. Local checks reuse compact existing tables; no package includes a new full archive scrape or national provider panel. Initial dollar expenditure is zero. Source counts are caps, not targets.

| Order/package | Proposed first-stage scope | Cap and output | What justifies the next stage |
|---|---|---|---|
| 1. Shared audit | S1–S2 using existing sources | 30–45 minutes; definition/expectation register | Consequential inputs reconcile or have explicit uncertainties |
| 2. Demographic feasibility | A1–A4 audit and S3 bounds; no full refit | 60–90 minutes; existing tables only; sign/materiality map | A material result turns on a field we can plausibly obtain |
| 3. Capacity feasibility | C1–C2 source/clock audit | 45–60 minutes; at most 12 facilities and 6 targeted public documents | Usable spaces or operational timing can be measured or usefully bounded |
| 4. Repair measurement | B1–B2, then B3 only with existing grouped data | 45–60 minutes; at most 4 targeted methodology/source documents | The sample mechanism applies to a consequential input and predictions differ |
| 5. Auction monetization | D1–D2 and E1–E2 | 60–90 minutes; existing notes/grids, at most 4 primary documents | Required improvements are plausible and events/contract scope are observable |

The exact order after package 2 should respond to its findings. Capacity starts early because the user wants an operating and capital model, but a full national facility build is not a prerequisite for the cohort test. Across all packages, shared sources are cached and reviewed once; the same methods section should not be repeatedly read by separate tasks.

For every first-stage package, return: what was observed; which explanations remain; the sign and magnitude range; the decisive missing information; and a recommendation to advance, narrow, park or stop. Do not run all packages merely because they appear here.

Before a substantial second-stage study, submit a concrete proposal stating:

1. The exact unanswered question and how different answers would change the model.
2. Existing evidence and the specific missing columns/population/time coverage.
3. The proposed source, sample selection, collection size, license/financial cost and access feasibility.
4. Cleaning, linkage, comparison group, estimation, validation and financial translation steps from end to end.
5. Cheaper alternatives, their inferential limitations, and why they are insufficient if escalation is recommended.
6. Expected local runtime, source-review workload and any reliably available usage estimate; disclose when credits cannot be estimated.
7. Failure conditions and a collection cap, including what happens if the sample lacks essential fields.

Wait for approval before that larger study. No sample-size commitment should precede a pilot establishing field coverage, effect variability and the number of genuinely independent observations. Thousands of repeated listings are not thousands of independent vehicle outcomes.

## 11. Recommended starting decision

Begin with the shared audit and demographic feasibility, then the bounded capacity screen. This preserves the distinctive existing thesis, tests its most consequential assumptions, and establishes whether operational data can support a meaningful CapEx and returns build. Repair measurement follows closely because it can change the interpretation of the same supply forecast. Delivery and contracts are retained as potential earnings mechanisms, with deeper work conditional on evidence and materiality.

The ambition is a complicated enough model to represent the mechanism accurately, with a small enough set of uncertain inputs that we can explain exactly what would make the investment conclusion wrong.
