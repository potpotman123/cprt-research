# Copart pitch audit — 29 September 2026

**Conclusion confirmed with the user on 30 September:** We have an intellectually interesting structural pitch, but have not established one measurable forecast error supported by evidence and tied to a sufficiently observable near-term catalyst. There is not yet a demonstrated actionable reason for investors to adopt our view within twelve months. Reporting dates are observation windows, not proof of a thesis-specific surprise. This is a central unresolved investment issue, not a presentation problem; do not lose it when transferring the model to Fable or preparing the pitch.

**PM judgment: retain as a research candidate; do not yet present it as a high-conviction, catalyst-backed 12-month short.** The revenue architecture can represent the proposed mechanisms. The evidence does not yet identify the combined forecast, incremental miss versus expectations, or timing strongly enough to support that conviction. More model complexity is unlikely to close those gaps.

Scope is the revenue model and the two competition theses. “Insurance competition” is interpreted as Copart/IAA competition for carrier assignments and contract terms, including changes in carrier composition. Earnings, cash flow, WACC and valuation remain the user's later work. Their absence is not a revenue-model defect, but this review cannot establish investment payoff without that later bridge. This is an adversarial internal review using a PM perspective, not external assurance.

**Overall assessment**

| Dimension | Assessment | Investment implication |
|---|---|---|
| Economic architecture | Coherent for conditional scenarios | Retain the engine and its accounting/timing guards |
| Aftermarket differentiation | Potentially interesting | The donor-demand mechanism is more distinctive than another generic claim-frequency short |
| Aftermarket evidence | Adoption observed; causal transmission substantially assumed | Do not adopt the larger scenario as a central forecast |
| Insurance competition evidence | Stronger direct operating evidence | Competition exists; the variant must be worse outcomes than already expected |
| Model calibration | Levels calibrated; response derivatives not independently validated | A close historical fit cannot determine marginal switching |
| Revenue materiality | Potentially meaningful relative to own reference; smaller against the dated broker benchmark | Quote both comparisons, never only the largest delta |
| Twelve-month catalyst | Observation windows exist; thesis-specific surprise and timing unproven | A calendar alone is insufficient |
| Comparison with reviewed winning pitches | Detailed mechanism, weaker evidence-to-expectation and evidence-to-event links | More decisive proof is worth more than another submodel |

**What was reused and checked**

Reviewed the current architecture/evidence notes, CCC integration, aftermarket adapter and parameter/adoption work, carrier tests, contract-concession screen, consensus review, catalyst assessment and the prior competition-anatomy review. Selectively read the selection, feedback and carrier-term implementation. Used saved scenario outputs; did not refit or regenerate models merely to become familiar with them.

Existing checks cover 43 core structural cases, 28 aftermarket cases, 42 source/calibration audit checks and 10 CCC integration checks; these categories overlap and are not independent empirical validations. The earlier portable reproduction also passed. In this pass, all 12 recorded aftermarket dependency hashes and all 15 CCC runtime hashes matched. Each of the five CCC scenarios' four quarters sums exactly to its saved annual service revenue. The accompanying checks.json preserves this limited new verification.

The original calibration's twelve exact targets belong to the original family. The CCC family fits the 16 age/body TLF cells and associated total-loss mix; it retains disclosed residuals against older repair/value targets. Do not claim one version simultaneously fits everything. No new arithmetic failure was found in the reviewed path. This is not an exhaustive new audit of every raw observation or workbook formula.

**1. Aftermarket thesis: plausible mechanism, not yet an identified negative loop**

The supported observation is increasing aftermarket usage in some recent national measures. CCC replacement-dollar share rose from 18.0% in 2022 to 22.7% in 2025, a 4.7-point gain; from 2020's 21.3%, the gain is only 1.4 points. Recycled dollar share was 9.9% in 2022 and 10.5% in 2025. Those data allow aftermarket growth alongside recycled growth. The 2024–25 recycled decline, 10.7% to 10.5%, is much smaller than the hypothetical displacement driving the model. [Preserved adoption evidence](../bidmate_adoption_2026-09-29/README.md); [CCC source](https://www.cccis.com/reports/crash-course-2026).

The chain requiring proof is:

Aftermarket adoption → comparable repair-cost savings and/or recycled contribution loss → changed marginal total-loss decisions and bidder willingness to pay → changed completed units and fee revenue.

Each arrow has an alternative explanation or offset:
- AM can primarily replace OEM. This supports repair savings but does not demonstrate lost recycled sales.
- Additional repaired vehicles create demand for parts. The adapter includes repair-job recapture, but assumes comparable parts usage per incremental job.
- Lower donor supply can support prices; lower repair bills can improve rebuilder economics.
- Domestic collision-part demand is only part of donor value. Mechanical parts, cores, scrap, export and whole-car rebuilding have different economics.
- Lower recycled usage can reflect availability, grading, delivery or fulfillment rather than durable cost competition.
- Lower expected salvage can make fewer cars economical to total. Expected salvage need not update immediately with auction prices.
- Changes in selected damage and vehicle mix can move observed ASP independently of like-for-like demand.

The adapter recognizes several offsets. Its weighted recycler/rebuilder bid response and scarcity term are assumed reduced-form relationships, not an estimated auction. The recycler transmission weight is not identifiable from winner share or buyer nationality. A solver that converges does not establish the economic coefficients or a dynamic spiral.

**The model's own countercases matter more than the complexity of its central case.** Under the CCC composition:

| Existing saved case | FY27 legacy service revenue | Delta versus own reference | Gap versus dated JPM $4,061m |
|---|---:|---:|---:|
| Reference | $4,093.08m | — | +$32.08m / +0.79% |
| Larger aftermarket shift | $4,002.41m | −$90.66m / −2.22% | −$58.59m / −1.44% |
| Larger shift, half switching response | $4,030.08m | −$62.99m | −$30.92m / −0.76% |
| OEM displacement only | $4,072.50m | −$20.58m | +$11.50m / +0.28% |
| Zero exposed donor contribution | $4,069.56m | −$23.52m | +$8.56m / +0.21% |

These are conditional diagnostics, not probabilities or confidence intervals. The last two cases produce a modest increase in insurance RPU, rather than a decline. The paired units/RPU downside therefore depends materially on the assumed recycled-demand channel. Sources: [CCC scenarios](../../model/ccc_age_body_2026-09-29/scenario_summary.csv), [parameter diagnostics](../aftermarket_parameter_audit_2026-09-29/diagnostic_sensitivities.csv).

The dated JPM forecast explicitly excludes ACV and already forecasts only about 2.3% FY27 service growth. The larger case does not demonstrate a $91m miss versus JPM: $91m is the effect against our higher reference. CapIQ's consolidated quarterly totals have a different, unresolved perimeter. Neither benchmark is automatically the expectation embedded in the stock. [Benchmark evidence](../../model/revenue_architecture_2026-09-28/EVIDENCE_UPDATE.md).

**Calibration priorities for this thesis**

A national adoption forecast is sufficient for the pitch. It does not require a separate forecast for every bumper or headlamp. It does require consistent denominators and evidence for what increased AM usage displaces.

1. Use a national quantity measure where possible, retaining rounding and composition limitations. Keep spending shares separate. Project future incremental adoption from the latest starting point; historical gains already in the revenue anchor are not fresh headwinds.
2. Separate the total adoption path from the OEM/recycled split and from eligible repair-bill spending. The hypothetical 65/25/10 quantity basket and 40% eligible bill share are not measured national inputs. CCC all-parts spending of roughly 36–44% by age does not establish that nearly all those dollars are substitutable.
3. Retain 25% donor contribution exposure and 1.5× contribution-to-hammer response as sensitivities until actual economics support them. Public Bidmate documents validate the workflow, not those coefficients. Purchasing rules differ; an accounting ratio alone is not a bid elasticity.
4. Use an all-claim near-threshold distribution to constrain switching. The CCC workbook improves levels and composition, not the number of claims that change disposition after a 1% cost shock. Fitting a more flexible curve to a few annual aggregate observations would add precision without identification.
5. Bound the influence on auction prices separately. A recycler export can establish its donor economics but cannot, by itself, establish national marginal-bidder influence.

The most useful CCC request is an existing aggregate all-disposition table of repair cost relative to value less expected net salvage, with supplements, age and loss-type definitions. The most useful recycler request is an existing anonymized donor-cohort report linking acquisition costs, projected and realized parts contribution, unsold inventory and purchasing rules. Compatible broad component groups are adequate for an initial test; individual-part forecasts are unnecessary. No new outreach has occurred. [Prepared Bidmate route](../bidmate_adoption_2026-09-29/README.md).

**2. Insurance competition: more observable, less obviously differentiated**

Competition for assignments has direct current support. RB Global's Q2 2026 release reports automotive unit growth of 11%, supported by net market-share gains, and automotive pricing incentives tied to greater transaction volumes. Its consolidated service take-rate decline also includes acquisition/business mix; it is not a clean automotive concession percentage or a Copart fee input. Automotive includes salvage and non-salvage transactions. [RB Global official release](https://investor.rbglobal.com/news/news-details/2026/RB-Global-Reports-Second-Quarter-2026-Results/default.aspx).

That establishes a competitive mechanism. It does not establish an overlooked short. The existing Barclays source screen already found broad carrier repricing consistent with the analyst's published contract economics. In its illustrative win, $118.75m incremental service revenue less $19.15m of concession expense leaves about $99.60m incremental service revenue before operating costs; the corresponding EBITDA estimate remains positive. Winning an account at a discount is not inherently revenue-destructive. The source's combined wins/losses and estimates already incorporate significant adverse effects. [Contract arithmetic and source limitations](../repair_research_2026-09-26/contract_scope_screen/README.md).

The required variant is specific: another exposed account, a longer transition, lower retained-account pricing, less offset from wins, or a less favorable carrier mix than a dated forecast includes. None is validated by repeating the disclosed customer loss or the inherited Progressive allocation scenario; the call's customer reference does not independently identify that carrier.

The carrier model appropriately separates carrier weights from Copart allocation. Its largest shortcomings remain:
- premium share is not vehicle, claim or auctionable-total-loss share;
- the inherited Progressive transition was calibrated to a reported print, not validated out of sample;
- account wins and losses need effective dates and compatible assignment/sale definitions;
- probabilities from the friend's scoring rubric are judgmental, not calibrated frequencies;
- seller concessions affect the affected revenue lines and may raise insurers' net recoveries, supporting assignments or totaling;
- a one-time lost-account drag eventually laps. Continued YoY decline does not prove continued sequential share loss.

Use the simplified Progressive-runoff case as a labeled scenario, and a genuinely flat sequential allocation case as a comparison. Do not extend a one-time loss indefinitely or treat a diagnostic industry-volume residual as measured market share. [Carrier review](../carrier_test_2026-09-28/README.md).

**3. Integration findings that matter before Fable adopts one forecast**

The architecture's shared selection mechanism is a strength: the same repair-versus-value/net-salvage decision changes both total-loss units and selected auction vehicles. Fees follow vehicle prices through brackets; services have separate eligibility and recognition; physical timing has conservation guards. Keep those features.

The remaining implementation and forecast decisions are consequential:

| Finding | Required treatment |
|---|---|
| Two theses are not yet one admitted forecast | The aftermarket adapter loads the price/international reference with same-quarter-neutral carrier settings. The separate core carrier-runoff scenario is not the combined CCC/aftermarket pitch. Build common-base cases: neither thesis, aftermarket only, carrier only, both; calculate interaction. Do not add separate dollar losses from different references. |
| Carrier-specific contract terms are static across periods | In the reviewed engine, carrier_terms are read inside every historical and forecast period with no effective-date selector. Before modeling a new carrier-specific concession, add dated terms that preserve historical economics. A static edit can change inferred historical units while the dollar anchor still reconciles. Existing defaults are not thereby invalidated. |
| National adoption narrative differs from executed scenario | The 5.5-point shift remains a physical eligible-basket change applied for the full FY27. A proposed three-year national ramp is not implemented. Establish one measure and an explicit quarterly path before quoting a next-year effect. |
| Timing is an interface, not measured default behavior | Sale-equivalent cases lack measured adoption/completion/expectation lags. The feedback solver averages quarterly effects to a common price shock. Do not infer a particular quarter's miss from it. |
| FY27 is not the entire proposed holding period | FY27 ends July 2027; twelve months from this review ends September 2027. Extend the common revenue path through that horizon and show the forward estimate investors would be revising at its end, potentially FY28. This does not require building cash flow now. |
| Reference offsets are economically large | Original-family international continuation adds about $89.91m annually versus its flat branch, similar in scale to the aftermarket scenario. +3.7% future insurance ASP is our continuation assumption, not consensus. An incremental thesis effect must coexist with these baseline drivers. |
| Exposure and service composition remain conditional | The 90% US insurance-dollar allocation, fee/buyer mix and ancillary economics are not disclosed disaggregation. Preserve alternative allocations and do not equate a lower average RPU with a fee cut. |
| Scope remains legacy services | Purchased vehicles and ACV acquisition classification need their own perimeter before presenting consolidated revenue. An acquisition-driven headline beat may conceal a legacy miss. |
| Uncertainty is not a probability distribution | Avoid multiplying subjective event probabilities or stacking all adverse settings and calling the result a base case. Report individual drivers and common-case interaction. |

The adoption timing issue is especially important. If, purely illustratively, 5.5 points is reached linearly over 36 months from zero additional adoption, the first-year endpoint is 1.83 points and the continuous first-year average is about 0.92 points, before any sale lag. That is one-sixth of the terminal exposure on average, not the full 5.5 points all year. It does **not** justify mechanically dividing $91m by six: selection, prices, exposures and fee schedules are nonlinear, and the national denominator still differs. It shows why the current output cannot be recycled as a three-year-ramp forecast.

**4. The strongest opposing reading of today's evidence**

Copart's September 10 call reports US insurance sold units down 7.5%, but domestic insurance assignments up 2.3% excluding one customer loss. It also reports US insurance ASP up 3.7% and calendar Q2 TLF of 23.3% versus 22.4%. These are different measures and populations; the assignment adjustment cannot be applied to sold-unit growth. The current picture is consistent with account movement plus resilient salvage economics, not uniquely aftermarket-driven industry weakness. [SEC-filed call transcript](https://www.sec.gov/Archives/edgar/data/1637873/000119312526388383/d138398dex992.htm); matching local licensed transcript lines 94–113.

Management also identifies catastrophe comparisons: global FY26 units fell 5.5%, or 3.1% excluding CAT units. The roughly 2.4-point difference is full-year/global; it is not an available adjustment to Q4 US insurance's 7.5% decline. Hurricanes Helene/Milton benefited FY25. Inventory and cycle-time changes further separate assignments from sales. [Preserved catalyst evidence](../catalyst_assessment_2026-09-29/README.md); local call lines 166–187, 215–218.

A credible bull case uses no heroic new mechanism: known account losses lap, ordinary assignments stabilize, high TLF persists, price/fees stay resilient, and international/services offset domestic weakness. AM may replace OEM while enabling additional repairs and stronger rebuilder demand. These observations can coexist with some long-term aftermarket headwind.

Do not require TLF to fall outright to allow a relative headwind; other forces can offset it. But a small effect visible only against our own unvalidated counterfactual is a weak public catalyst. The short must identify an observable surprise relative to a pre-specified expectation.

**5. What could actually matter within twelve months**

A hard catalyst is a dated event that reveals a forecast-relevant surprise. The date can be known while the disclosure, outcome and stock response remain uncertain.

| Window | Information that would strengthen the short | What does not qualify / opposing result |
|---|---|---|
| LKQ Q3 call, October 29, 2026; date reconfirmed on official IR | Recycled collision contribution/sell-through or donor purchasing weakens while aftermarket/repair activity holds up; explanation links the divergence to substitution | Alternative-parts growth alone; Europe/ERP effects; higher AM and recycled demand together |
| Copart FY27 Q1, expected November 2026; exact date unconfirmed | Underperformance versus an explicit customer-adjusted assignment path plus weaker price-sensitive fees than expected | Repetition of the known customer loss; an unrelated EPS miss; acquisition/perimeter noise |
| RB Global's next quarterly update; exact date not verified | Further competitive wins or concessions beyond the already modeled transition, with compatible scope and timing | Consolidated take-rate mix, equipment-cycle effects, or the same previously announced win |
| CCC/Mitchell public updates; release schedule/content unverified | Compatible adoption and disposition data jointly show a larger effect than the baseline predicts | More AM usage with no evidence on displaced source or claim selection |
| Copart FY27 Q2/Q3/Q4, approximately February/May/September 2027 by historical cadence; dates unconfirmed | Repeated evidence that the expected recovery fails as known distortions lapse, followed by reductions in forward legacy-service assumptions | Repeatedly moving the expected inflection later, or attributing every weak quarter to the thesis |
| New carrier/repair-network sourcing or auction award announcement | A genuinely new, dated rollout with meaningful incremental exposure and known economics | An existing policy, rumor, or hypothetical future award; no such new event was verified here |

[LKQ official IR calendar](https://investor.lkqcorp.com/). The later Copart windows are cadence assumptions, not confirmed events. This review has not found a verified new procurement rollout or incremental account-loss announcement that independently supplies the missing catalyst.

A specific earnings catalyst would cause an analyst to reduce the assumed legacy insurance **unit recovery and/or fee RPU**, rather than merely change tax, interest or acquisition assumptions. Before the event, write down that analyst's unit, ASP, fee and international assumptions and the required miss. Our +3.7% ASP reference cannot stand in for their forecast.

The structural thesis could affect valuation before it materially reduces revenue if investors receive decisive evidence of durable weaker growth. That route is possible, but it requires a strong public signal and a later valuation-duration argument; it cannot rescue an otherwise undated pitch by assertion.

**Proposed time discipline:** use the next two Copart reports as the initial research decision window, not a claim that the thesis must resolve in six months. If no incremental account problem emerges, comparable assignments stabilize, and price/fee strength persists without evidence of recycled impairment, demote the 12-month short. A valid longer-term idea may still be a poor trade for this horizon. Do not keep the same conviction merely by extending the deadline. Numerical cutoffs should be fixed against the named forecast before results, not invented after the print.

**6. Comparison with the previously reviewed successful pitches**

Recovered the August 31 [competition-anatomy review](competition_anatomy_prior_review.md), covering Freshpet, Live Nation, CLEAR and others. The comparison reuses that review; it does not claim a new complete deck audit or subsequent trading-performance study. Direct deck/archives retrieval was unsuccessful in this pass. The BAM sponsor's announcement independently confirms Alabama won its 2024 event, but does not validate every archived participation count. No win probability or percentile is assigned.

| Prior example | Transferable strength documented in the prior review | Current Copart gap |
|---|---|---|
| Freshpet short | Segmented operating opportunity and economics tied to an explicit expectations/valuation hurdle | A novel mechanism is present, but the central adoption/displacement/bidding assumptions do not yet establish the priced-in error |
| Live Nation short | Calendar/deferred-revenue evidence mapped to particular forecast quarters | Our adoption and assignment-to-sale timing remain conditional; no equivalent near-term evidence schedule |
| CLEAR short | A visible deployment/substitution path linked to retention and membership KPIs | No comparably verified AM procurement rollout with measured affected exposure |
| Burlington long | Operational improvements translated into readable, forecastable drivers | Our pitch front end needs fewer decisive operating claims; retain engine detail in the appendix |

[BAM sponsor confirmation](https://www.bamfunds.com/news-and-insights/bam-s-first-stock-pitch-competition).

My judgment is that the current work would demonstrate serious research effort and an interesting mechanism, but would be vulnerable in finalist Q&A on “why now?”, “which assumption drives the miss?”, and “why is this not already in estimates?”. It is not yet as convincing on those dimensions as the strongest reviewed examples. Their success does not prove their assumptions or guarantee investment returns; the comparison is about pitch construction.

**7. Work that would most improve the pitch, in order**

1. **Establish a common expectations sheet.** One or two dated broker operating builds, with account transitions, US insurance units, price/fee assumptions, services, international and ACV scope. Use the held licensed reports first; request a narrow missing-table export only if necessary. An aggregate revenue number cannot identify all drivers. This decides what the pitch is actually contesting.
2. **Choose and implement a consistent national adoption path.** Keep neutral, continuation and faster-adoption cases; justify recycled displacement separately. Retain the present full-year case as a stress. No fine-grained part-by-part forecast is needed.
3. **Complete the dated joint revenue case.** Four common-base cases, carrier-specific effective terms, explicit timing, and a bull offset case. Show own-reference effect separately from the like-for-like benchmark gap.
4. **Obtain the two highest-information empirical checks.** A CCC near-threshold/disposition summary and a recycler donor-contribution/bid-rule report. Use existing exports and broad groups first. They answer more than more model fitting or another general industry article. Escalate collection only after schema and access are known.
5. **Reduce the presentation to one expectations bridge and one catalyst scorecard.** Insurance competition should lead near-term timing if an incremental surprise can be supported; aftermarket should supply differentiated structural risk with explicitly bounded magnitude. If neither yields a measurable twelve-month surprise, keep the project as structural research rather than label it catalyst-ready.

Suggested front-page claim, **conditional on obtaining the evidence**: “Legacy service revenue will recover less than the named forecast assumes because carrier economics remain weaker and repair-parts substitution reduces the volume/price cushion.” Show the numerical miss, reveal quarter, supporting observation and falsifier beside each clause.

Fable can build a transparent scenario workbook now, with the admission status and sources visible. It should not label the larger aftermarket case a validated forecast, stack separate carrier losses, or show the $91m as a measured consensus miss. No model assumptions or source workbooks were changed in this audit.

**Provenance and research limits**

Current workspace was checked at commit 7635484 with later uncommitted research present. Existing provenance/failure records were reviewed selectively. This pass used seven targeted web queries across Copart, competitor, supplier-calendar and competition-example sources, plus direct source retrieval attempts. Official search-returned content supplied RB Global's current disclosure, Copart's SEC-filed call excerpt and LKQ's event date. Direct open requests for those pages and the competition archive/decks failed or were restricted; those failures were not treated as missing facts when preserved or search-returned primary text was available. No exact future RB Global date was established. No investor-positioning survey, current stock valuation, paid data, new account, outreach, bulk collection, agents or model fitting was undertaken.

The new durable result is this pitch-level judgment and the checks file. Earlier source-ledger audits and the Fable package remain separate; this note does not certify every archive or silently update that package.
