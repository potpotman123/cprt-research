# Prompt for a high-reasoning Fable session — Copart (CPRT): turn two structural theses into a catalyst-backed pitch, or prove it cannot be done

*Prepared 2026-09-30 by the Fable session that has worked in this repository since 2026-09-08. You are starting a new chat with no memory of that work. Everything you need is in the repository at `potpotman123/cprt-research` (GitHub) or the owner's local clone at `/Users/kwu/cprt`. Read this whole prompt before opening any file.*

---

## 1. Who you are working for and what the job is

The owner is preparing a stock pitch on Copart for a competition judged by multi-manager pod-shop practitioners (two-page PDF plus a model; finals late October 2026; horizon 3–12 months). Over three weeks, two agents (this session and another called Astra) built a granular revenue architecture: a claim-to-sale engine that starts with the US vehicle fleet and ends with Copart's quarterly legacy service revenue, plus two structural theses. The owner's own audit, and the repository's, agree on the current state:

> We have an intellectually interesting structural pitch, but have not established one measurable forecast error supported by evidence and tied to an observable near-term catalyst. (`RESEARCH_STATE.md`, 2026-09-30)

**Your job is to close that gap or to show rigorously that it cannot be closed on this horizon.** Concretely: for each of the two theses below, identify the specific adoption or allocation path that a named forecast assumes, show where the evidence says that path is wrong, name the dated public observation that would reveal the error, and quantify the revision it forces. If after a bounded search no such catalyst exists, say so plainly and recommend the pitch be reframed. A pitch whose edge is "our model is more granular than a pod's" is not acceptable; the owner has said so and is right.

## 2. The two theses, as the owner frames them

**Thesis A — competitive convergence in the salvage duopoly.** Copart's historical advantage over IAA (land, yard density, buyer base, service quality) has narrowed to the point where insurers have no reason to allocate exclusively to Copart. Progressive's move of most of its volume to IAA between April and July 2026 is, on this view, not a one-off but the first visible instance of allocation becoming contestable. The market becomes a genuine duopoly with pricing pressure on seller terms. The owner believes Copart holds roughly 60% of the market to IAA's roughly 30%, and cites IAA's land position, IAA's acquisition by RB Global, and leadership change as reasons the two offerings are now indistinguishable. **Treat every one of those factual claims as UNVERIFIED until you source it**: verify the acquisition date and terms (RB Global closed the IAA acquisition in March 2023, so "just acquired" needs a precise date), the leadership changes at RB Global and IAA with dates, IAA's owned versus leased acreage from RB Global filings, and the share figures against RB Global's disclosed automotive volumes and this repository's daily listed-inventory split (Copart ≈57% of the duopoly's listed US inventory on clean nights; `data/csv/duopoly_daily.csv`, use `usable = 1` rows only). Note that "no competitive advantage" and "more of a duopoly than ever" are not the same claim; the precise version is convergence of allocation toward a contestable equilibrium, and you should state what equilibrium share the evidence supports.

**Thesis B — aftermarket parts substitution as a unidirectional lever on both units and price.** Copart's KPIs are normally hedged against each other (fewer total losses come with higher prices, and so on). Aftermarket parts adoption may be the rare driver that moves both the same way: on the seller side, cheaper repairs mean fewer marginal total losses (fewer units); on the buyer side, less demand for recycled parts means dismantlers bid less for donor cars (lower prices and fees). The repository contains an explicit bridge for this mechanism (`model/aftermarket_bridge_2026-09-29/`). Its coefficients are assumed, not measured; its own countercases show the RPU sign can flip if recycled displacement is small. The owner knows this.

**The shared problem.** Neither thesis yet has a Street misforecast attached to it. The repository has a dated named benchmark (JPMorgan, 2026-09-11: FY27 legacy service revenue $4,061M, ex-ACV, about +2.3%) and CapIQ consolidated totals with an unresolved acquisition perimeter. It does not have the analysts' unit, price, fee, allocation or adoption assumptions behind those totals. Without them nothing can be called a miss.

## 3. Read in this order, and no more than this to start

1. `AGENTS.md` and `RESEARCH_PRINCIPLES.md` — the standing research rules. They bind you. Section 4 is the default assignment template.
2. `RESEARCH_STATE.md` — the recovery index and the agreed conclusion.
3. `docs/pitch_audit_2026-09-29/README.md` — the PM audit of both theses. Its sections 5 and 7 are the closest thing to your task list; do not redo its work, extend it.
4. `model/revenue_architecture_2026-09-28/README.md`, then `docs/model_audit_2026-09-29/AUDIT.md` and `FABLE_HANDOFF.md` — the engine, its checks, its unresolved inputs, and the workbook contract.
5. `docs/catalyst_assessment_2026-09-29/README.md`, `docs/carrier_test_2026-09-28/README.md`, `docs/FABLE_SHARE_BUILD_REVIEW_2026-09-27.md`, `docs/aftermarket_parameter_audit_2026-09-29/FORWARD_ASSUMPTIONS.md`.
6. `HANDOFF.md` (the earlier project by research thread, including what was retracted) and `findings.md` Addenda 14–22 only if you need the history of a specific number.

Do not read `scripts/`, `data/csv/`, or the model code beyond what a specific question requires. Filter large outputs. The repository is the analytical archive; `raw/` (licensed transcripts, sell-side PDFs, the source CCC workbook, collection caches) is local to the owner's machine and absent from a clone. If a step needs a licensed file, say exactly which one and ask the owner to run that step or supply the extract.

## 4. How the engine builds units and RPU, so you can reason about it without rebuilding it

The chain from a crash to a Copart sale, as implemented (`model/revenue_architecture_2026-09-28/model.py` plus the CCC integration and the aftermarket bridge):

1. **Fleet births.** New light-vehicle sales by calendar year, split into cars and light trucks (Ward's via ORNL; FRED 2022–25), with light trucks split into SUV/pickup/minivan by a fixed pool proxy (`docs/historical_body_births_2026-09-28/`).
2. **Survival.** EPA survival schedules stretched along the age axis by a parameter fitted to the 2013 IHS census and to 2024 fleet counts (`docs/AGE_CURVES.md`). Output: vehicles on the road by age and body.
3. **Claims propensity.** Relative claims per vehicle by age (flat to age 6, then declining) and body, calibrated to CCC claim-mix statistics; a combined claims multiplier (default 1.0) and a paired repairable non-filing term for the deductible shift.
4. **Carrier layer.** Carrier weights (premium share × salvage intensity) and Copart allocation per carrier from a quote/event model (Progressive runoff calibrated to the FQ4 FY26 print; GEICO and other-carrier events with judgmental probabilities). Default is allocation held flat year over year; runoff is a separate labelled case.
5. **Damage selection.** For each age × body × carrier cell, a damage severity distribution (nine states) at six representative ages, a pre-loss value scale, a repair-cost function, and an expected net salvage recovery (an inherited curve of roughly 40% of value falling to 20% with age, less seller charges). A claim becomes a total loss when repair cost exceeds value minus expected net salvage. Levels are calibrated to CCC targets (originally twelve: six age TLFs, four selected values, two repaired means; then sixteen age × body TLF cells and total-loss mix from the owner's CCC workbook). **The derivative of this decision, how many claims sit near the threshold, is not measured by anything.** This is the "damage selection engine" the owner refers to.
6. **Aftermarket bridge (thesis B).** A source mix inside an "eligible basket" of the repair bill (assumed 65% OEM / 25% aftermarket / 10% recycled, at assumed price ratios 1.00 / 0.50 / 0.60, the basket assumed to be 40% of the bill) shifts toward aftermarket; that lowers the complete repair cost (fewer total losses through step 5) and lowers recyclers' expected donor contribution (assumed 25% of contribution exposed, 1.5× contribution-to-hammer), which lowers their bids with an assumed 50% transmission to marginal auction prices; a solver iterates selection and prices to consistency.
7. **Totals × routing × allocation.** Total losses × routing fraction to the insurance auction channel (default 1) × extra CAT fraction (default 0) × Copart allocation = Copart assignments.
8. **Timing.** Sale-equivalent by default (assignments sell in the same quarter). A physical mode with opening backlog, title/no-title delay kernels and withdrawals exists but is gated off because its inputs are unmeasured.
9. **Prices.** The selected vehicles' value distribution gives a realized auction price at fixed rank, moved by a forward price path (+3.7% continuation of FQ4 FY26 US insurance ASP growth in the reference; +6% alternative). Neither is guidance.
10. **Fees.** Copart's posted buyer-fee grids (transcribed 2026-09-26: non-licensed and licensed tiers, clean/non-clean, standard/heavy, virtual-bid, gate and fixed fees) applied per sale by price band, with an assumed buyer mix (50% preferred) and seller fee (4%). Only one dated schedule snapshot exists; its application to history is a proxy.
11. **Service events.** Title processing and delivery as separate jobs with assumed adoption and price (50% × $50; 10% × $300), eligibility, waivers, bundling and recognition delays.
12. **Other branches.** Other-US fee activity (a 10% residual), international (fee units × reported-currency RPU, +3.5% continuation), purchased-vehicle revenue as an overlay, and the ACV acquisition gated as unknown.
13. **Ledger and level problem.** Historical US service dollars are anchored to the 8-Ks each quarter; 90% is assigned to insurance (80% alternative) and units are inferred from the assumed fees. Nothing here is observed disaggregation.
14. **Benchmarks and hurdles.** The JPM FY27 ex-ACV service forecast and CapIQ totals; `hurdles.csv` gives the all-in insurance RPU growth required to meet each benchmark for a given unit growth. 15 core, 11 aftermarket and 5 CCC scenarios with exact interaction accounting.

Two properties of this chain matter for your task. First, the same selection decision drives both units and selected prices, so thesis B is expressible in it. Second, almost every response coefficient is assumed or calibrated to levels; the engine can represent a mechanism but cannot by itself validate one.

## 5. The assumptions that are unsourced and load-bearing

Treat these as the list a hostile judge would read out. Each is labelled in the repository as assumed; none has an evidence-backed central value. Ranked by how much of the output they move:

1. Insurance share of US service dollars, 90% (alt 80%) — sets implied unit levels and every per-unit figure (`driver_register.json`).
2. The damage-selection derivative: near-threshold mass, the imposed damage/recovery rank relationship, six representative ages × nine severity states — calibrated to levels only.
3. Expected salvage recovery, 40% → 20% of value by age, and its response and timing to price changes — inherited.
4. Aftermarket bridge coefficients: 40% eligible bill share; 65/25/10 basket; 1.00/0.50/0.60 prices; a 5.5-point shift applied for all of FY27; 25% donor exposure; 1.5× contribution/hammer; 50% recycler transmission; 1.0× rebuilder ratio. Public evidence supports adoption growth (CCC aftermarket dollar share 18.0% in 2022 to 22.7% in 2025) and a historical 23–30% aftermarket discount (Mitchell 2016), and nothing else in that list.
5. Carrier model: carrier weights from mixed-year premium shares (premium share is not salvage-volume share); event probabilities of 60% (GEICO) and 45% (State Farm) are judgmental; the Progressive ramp was fitted to the print it is compared with; a 5-point loss applied to a 24% "Other" bucket rests on regional anecdote.
6. Fee application: buyer mix 50% preferred, seller fee 4%, fixed fees $110, one September-2026 schedule applied to all history.
7. Service adoption and price: title 50% × $50, delivery 10% × $300 — undisclosed products.
8. Reference continuation: +3.7% US insurance ASP and international Q4 economics (+3.5% RPU) carried forward; international alone is worth about $90M a year, the size of the larger aftermarket case.
9. Neutral stresses with no empirical anchor: claims multiplier 0.98, repair cost 0.97, other-US ±5%.
10. Structural conventions: routing 1, extra CAT 0, sale-equivalent timing, SUV/pickup/minivan split fixed across vintages, fleet composition used as claims composition.

Also inherited from the earlier work: the 289M vehicles-in-operation anchor was recalled rather than sourced (Experian's 292M on disk gives the same survival stretch); the CCC quarterly TLF series may be discontinued after 2025Q3; effective sample sizes in the price and fee regressions are about six.

You are not asked to source all of these. You are asked to (a) identify which two or three actually determine whether either thesis produces a measurable Street miss, and (b) say which of those can be sourced within the rules and which must remain labelled sensitivities in the pitch.

## 6. What to produce

Work in phases. Each phase ends with a short written checkpoint to the owner. Before any phase that involves more than a handful of fetches, OCR, large extraction, extensive fitting or anything paid, stop and send the owner the complete proposed workflow: every step, why it is necessary, the cheaper or more precise alternative and why it is or is not sufficient, an honest cost range without invented precision, the expected information gain, the stopping rule, and the deliverable. Wait for approval. Routine cheap continuation does not need approval.

**Phase 0 — Recover state (bounded, read-only).** Read §3's files. Write a one-page statement of the unresolved question in your own words, the competing explanations for Copart's FY26 unit decline and price resilience (account movement plus resilient salvage economics is the strongest opposing reading), and what you will not redo. If anything in this prompt conflicts with the repository, the repository wins and you note the conflict.

**Phase 1 — The expectations sheet.** The pitch contests a forecast, so establish what is being contested. Assemble, from the licensed reports the owner holds locally (JPM 2026-09-11, Stephens 2026-08-20, any Barclays material) and from public transcripts, the assumptions a named analyst makes for FY27 by quarter where available: US insurance units or assignments, the treatment of the lost account and its lap (FY27Q4), US insurance ASP, fee or service RPU, international growth, purchased revenue, and ACV scope. Where a figure is not disclosed, record it as not disclosed rather than inferring it from a total. Ask the owner to extract any licensed table you cannot open. Deliverable: `reports/expectations_sheet_2026-10.md` with a table of named-source assumptions, dates, and the gaps.

**Phase 2 — For each thesis, find the misforecast and its reveal.**

For thesis A: the variant must be worse than what the expectations sheet already contains. Candidate forms: another exposed account (identify which carriers' contracts renew in the window and what the RB Global disclosures say about wins), lower retained-account pricing (seller concessions), a longer or deeper Progressive transition than the ramp assumes, or less offset from wins. For each candidate: the observable (a filing line, a call statement, a reported unit or take-rate figure, the daily listed-inventory split), the date it is next observed, the pre-specified threshold that would count as a surprise, and what result would kill it. Verify the owner's factual claims about IAA and RB Global with sources. Use the carrier model's Progressive-runoff case and a flat-allocation case as the two comparisons; do not extend a one-time loss indefinitely.

For thesis B: the misforecast must be about adoption or displacement, not about the mechanism existing. Candidate forms: insurer procurement or direct-repair-program rules that expand aftermarket eligibility with an effective date; CCC or Mitchell releases showing a change in source shares or total-loss rates in 2026 rather than 2024–25; LKQ's Q3 call (October 29, 2026, confirmed) showing recycled collision demand weakening while aftermarket and repair activity hold; the next Copart print showing weaker price-sensitive fees than the expectations sheet implies. Broaden discovery per `RESEARCH_PRINCIPLES.md` §2: who observes the repair-parts decision (estimating vendors, DRP shops, parts distributors, insurer payment surveys, recyclers' purchasing software) and what ordinary records they publish. One bounded pass of four to six queries across those source families, then open the strongest leads only.

Deliverable: `reports/catalyst_scorecard_2026-10.md` with, per candidate, the mechanism, the named assumption it contradicts, the observable, the date, the pre-specified threshold, the kill result, and your confidence label (VERIFIED / MEASURED / FITTED / ASSUMED / UNVERIFIED).

**Phase 3 — Decide.** Rank the candidates. If one thesis has a defensible dated surprise and the other does not, say which leads and which supplies structural context. If neither does, write that conclusion first in the report and recommend how the pitch should be reframed (for example, the earlier long-leaning variant view on RPU floor and the Progressive lap, or a structural research piece rather than a catalyst pitch). Do not keep conviction by extending the deadline.

**Phase 4 — Model integration, only for what survives.** Implement one dated combined forecast in the existing engine: four common-base cases (neither thesis, A only, B only, both) with exact interaction, carrier-specific effective-dated terms, an explicit quarterly adoption path for B rather than a full-year shift, and a horizon that runs to September 2027 so the forward estimate investors would revise at the end is visible. Quote every thesis effect both against the model's own reference and against the named benchmark; never present the own-reference delta as a consensus miss. Do not stack adverse settings and call the result a base case. Run the existing tests and `scripts/verify_intermediate_xlsx.py` if you touch the workbook.

**Phase 5 — Report.** Update `RESEARCH_STATE.md` with the new conclusion and a one-line change log; add a compact provenance entry to `PROVENANCE.md` for every host touched; leave the failure record of anything that did not work. The owner will carry your reports back to the original session for the reasoning discussion.

## 7. Standards that apply throughout

- Distinguish observation from explanation. "The total-loss rate follows the repair-versus-value spread" is an observation; an explanation names what moves the spread and why it moves next. Every claim in the scorecard must be of the second kind.
- Every number carries a label: VERIFIED (in a filing or fetched page on disk), MEASURED (computed from verified data by a committed script), FITTED, ASSUMED, UNVERIFIED (recalled or second-hand), RETRACTED. Preserve uncertainty and evidence against the preferred direction.
- Inventory prior work before searching; preserve failed searches; distinguish independent sources from republications of one dataset.
- Rules that do not bend: `robots.txt` first and obeyed; `scripts/prov.py` for every request (it logs and rate-limits; BLS and SEC want a descriptive User-Agent with a contact email, Copart and IAA refuse one — `prov.headers_for(url)`); no authentication, paywall or challenge circumvention; no vendor contact, purchases, form submissions or agents without the owner; licensed material never committed or quoted at length. Paste status codes before calling anything blocked; three separate agents on this project declared things unavailable that were on disk.
- The owner caught more substantive errors than the models did. Show reasoning, not conclusions, and expect correction.

## 8. What a good final answer looks like

One page a pod PM could read: the contested forecast and its source; the mechanism; the specific assumption that is wrong and by how much; the date and observable that reveals it; the kill condition; the valuation consequence left for the owner's DCF. Beneath it, the scorecard and the expectations sheet. Beneath those, the model cases. If the honest answer is that no twelve-month catalyst exists, the one page says that, says why, and says what the research is worth instead.
