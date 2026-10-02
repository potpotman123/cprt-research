# Encoding the three memo theses into the RPM, with a source behind every number — plan, 2 October 2026

Plan only. Nothing in the workbook changes until the owner approves. Rule for the build: no numeric input may sit in a cell without a Notes entry that names its source (file path, URL, report and line, or the explicit assumption and why) and its label (VERIFIED / MEASURED / FITTED / CALIBRATED / ASSUMED / UNVERIFIED / ENGINE).

## 0. Where the current workbook stands against the memo

| Memo thesis | What the workbook already encodes | Gap |
|---|---|---|
| T1 Once burned, twice shy (coverage lost to the 2023 premium shock does not come back) | Nothing. E2 has a claims multiplier (1.0) and a non-filing term (0) as placeholders. The overnight Python work added a premium channel, but every slope in it is ASSUMED (1.0) | A coverage layer with measured history, a fitted response, and two explicit forward paths (recovery vs sticky) |
| T2 The seesaw breaks (aftermarket parts cut repairs and dismantler bids) | E4, reduced form. Adoption path, basket, prices and the whole donor-bid chain are ASSUMED | Re-base on CCC's measured source shares; make recycled displacement the observed trend, not a 1.5-point stress; bound the dismantler chain with LKQ data; add the tariff argument with its source |
| T3 Progressive is structural; IAA at parity; more carriers move | E3, realised-case toggles. The workbook's thesis-A share path already equals the memo's base case exactly (56.6% FQ4 FY26 → 55.3% FQ4 FY27) because the inherited carrier paths are the probability-weighted expected moves | Show the probabilities and shift sizes explicitly, sourced row by row to the dated quotes and the historical precedents; add the parity evidence (acreage, cycle time, margin, board seat) with sources; derive the "5.2% revenue loss" inside the model |
| Street comparator | JPM FY27 $4,061m; Reverse DCF implies 4.0% revenue CAGR | A "Street-implied" case that states what unit recovery JPM's number requires, so each thesis is a miss against something specific |

Two facts from the inventory shape the plan. The memo's T3 base case (−130 bp) is already the workbook's thesis-A path, so T3 is a documentation job, not a modelling job. The memo's T1 evidence (IRC uninsured rate 15.4% vs 12.6%; 24% "considered" liability-only; 22.4% lapse penalty) is about liability coverage and surveys; the model needs physical-damage coverage (collision and comprehensive), which is what feeds total losses. That data exists publicly and we do not hold it yet.

## 1. Thesis 1 — coverage persistence

**Mechanism in the model.** Insured total losses = fleet claims (E1/E2) × physical-damage coverage index × filing index. Units chain gains a coverage ratio alongside the pool and share ratios.

**Evidence to obtain (bounded, public, robots-checked, through `scripts/fetch_logged.py`):**
1. NAIC *Auto Insurance Database Report* (annual PDF): earned car-years by coverage (liability, collision, comprehensive) by year, 2017–2023. Collision car-years ÷ liability car-years is the share of insured vehicles carrying collision; its path through the 2021–23 premium shock is the measured coverage drop. 1–2 fetches. Label VERIFIED.
2. FRED CPI motor vehicle insurance (CUSR0000SETE), monthly to 2026: the premium index. 1 fetch. VERIFIED.
3. CCC Crash Course claim-volume series already in the repository (total, ex-comprehensive and repairable claim volume y/y, 2020–2025): the observed outcome against which the coverage layer is checked. VERIFIED, on disk.
4. Progressive monthly policies-in-force (8-Ks on disk, `raw/sec/pgr`): a high-frequency check that the industry's insured base is growing again or not. VERIFIED, on disk.
5. The memo's secondary figures: IRC uninsured-motorist 2023 release (1 fetch), the 22.4% lapse penalty (1 search, 1 fetch to find the primary; likely a rate-comparison study, labelled accordingly), S&P premium forecast (owner holds; licensed, paraphrase with date).

**Quantification.** Fit one slope of coverage share to the premium-to-income ratio on 2017–2023 (FITTED, public data), with the stickiness shown as the 2024–25 residual (coverage not returning as premium growth slowed). Forward paths: *Sticky* (T1) = coverage index flat at the 2025 level, with an alternative that continues eroding at the S&P-forecast premium rise; *Recovery* (Street-implied) = coverage index reverse-solved so that case 0 reaches JPM's $4,061m given our ASP, fee and international inputs. The T1 dollar value is Recovery minus Sticky, quoted against JPM. If NAIC data cannot be obtained, the layer is built with the slope labelled ASSUMED and the memo must say so.

**Kill condition for T1.** NAIC 2024 collision car-years recover toward 2019 penetration, or CCC claim volume turns positive while frequency is flat.

## 2. Thesis 2 — aftermarket substitution

**Re-base E4 on measured quantities.** Replace the hypothetical 65/25/10 basket with CCC's national source shares by count and by dollars, 2020–2025 (on disk; VERIFIED), keeping the eligible-share conversion explicit. Adoption path = continuation of the CCC trend (+1.7 points of dollar share 2024→25, VERIFIED base rate), with the memo's tariff-suppression estimate (0.84–1.69 points) shown as a labelled upside only if its price-response coefficient of 2 can be sourced; otherwise ASSUMED and shown as a sensitivity. Price discounts: Mitchell 2016 matched discounts 23–30% (VERIFIED) as the default; the current catalogue's ~50% as the stress.

**Recycled displacement.** Default to the observed trend: recycled dollar share fell 0.2 points 2024→25 (CCC, VERIFIED), not the 1.5-point stress. This is the honest number and it makes the price channel small. The memo's "both sides move together" then rests mainly on the repair-cost (units) channel, with the price channel a conditional extension. Say so.

**Dismantler chain (donor exposure, bid ratio, transmission).** One bounded fetch: LKQ 2025 10-K (SEC) for North America revenue by product type (recycled vs aftermarket) and its language on salvage-vehicle procurement cost; plus the LKQ Q2 2026 release already on disk. These bound how much of a dismantler's revenue is collision parts exposed to substitution; the bid ratio and transmission stay ASSUMED and visible, with the no-displacement countercase always shown.

**Kill condition for T2.** CCC 2026 mid-year shows recycled share flat or up with aftermarket up, or LKQ reports recycled collision demand holding while salvage procurement costs rise.

## 3. Thesis 3 — structural carrier shift

**Documentation, not re-modelling.** E3 gets a probability table: carrier, move size (points), probability, start quarter, ramp length, evidence rows (dated quote-bank entries and the historical precedents of 10–20 point moves over four quarters, from the share build), each labelled UNVERIFIED second-hand with the date and source type. Expected-value path = Σ pᵢ × shiftᵢ (this reproduces 55.3%); realised-case path shown beside it. A *Parity evidence* block: IAA ~14.8k acres (RB Global FY2025 10-K properties table, on disk, VERIFIED once read), Copart 19.1k acres (to be located in the FQ1 FY25 call; the first grep found no "acres" there, so the citation must be found or dropped), cycle time 50 vs 52 days (expert calls, UNVERIFIED), gross margin 45.3% → 41.8% (8-K exhibits, on disk, VERIFIED), Progressive-affiliated director at RB Global (2026 proxy statement, 1 fetch, VERIFIED). The "~5.2% revenue loss in FQ4 FY26" is derived in the model from the ledger (Progressive weight × allocation change × insurance share of US service × US share of global service) rather than asserted.

**Kill condition for T3.** No further carrier move by FQ2 FY27 and Copart assignments ex-Progressive growing, or RB Global automotive growth decelerating to Copart's.

## 4. Scenario architecture after the change

| Case | Definition |
|---|---|
| 0 Street-implied | Known Progressive runoff; coverage recovery reverse-solved to JPM FY27 $4,061m; continuation inputs elsewhere. States what the Street needs |
| 1 Known facts | Current case 1: runoff laps, coverage flat, no thesis |
| T1 | Case 1 with the sticky-coverage path and the premium-rise alternative |
| T2 | Case 1 with the re-based aftermarket path (observed displacement; stress shown) |
| T3 | Case 1 with the probability-weighted carrier moves (−130 bp) |
| All three | T1 + T2 + T3 on one base; interaction reported |
| Bull | Case 0 plus ASP +6% and international continuation |

Every thesis effect is quoted three ways: against case 1, against case 0, and against JPM. The RPM selector gains the new cases; nothing else on the RPM or DCF changes.

## 5. Source discipline

A new `Sources` tab lists every numeric input in the workbook: tab, cell, value, label, source (path / URL / report and line), date, rationale. It is generated by the build script from the same list that writes the inputs, so a cell cannot exist without a row. `Checks` gains two rows: inputs without a source row (must be 0) and ASSUMED inputs inside each thesis case (listed, so the memo can disclose them). `docs/source_trace_2026-10-01/trace_register.csv` is regenerated from the same list.

## 6. Order of work, cost and stopping rule

1. Fetch the public sources listed above (about eight requests, all robots-checked; no paid, OCR, bulk or outreach). If NAIC blocks or the PDF needs OCR, stop and report.
2. Extract the figures into data tabs with citations; fit the coverage slope; locate the Copart acreage citation; derive the 5.2%.
3. Model changes: E2 coverage block, E3 probability and parity blocks, E4 re-base, Scenarios recut, Sources tab, Checks rows. Three or four local build-and-verify iterations; no agents.
4. Update the source-trace register and this plan's status; produce a one-table appendix for the memo: thesis → mechanism → input → source → FY27 effect vs case 1 / case 0 / JPM.

Stop and ask before: any paid or licensed acquisition; any step that needs more than a handful of fetches; or if a thesis number cannot be sourced at all, in which case the memo wording, not the model, has to change.

## 7. Points the owner should decide

1. Base case for quoting thesis effects: both case 0 (Street-implied) and case 1 (known facts), or only one.
2. T2 default: observed recycled displacement (small price effect) with the 1.5-point case as a labelled stress, or the memo's larger case as default. I recommend the former.
3. Expert-call material (95:5 allocation, 50 vs 52 days, probabilities) enters the workbook as dated paraphrases labelled UNVERIFIED. Acceptable, or keep such figures out of the model and in the memo appendix only.
4. Approve the fetch list in §1–§3 (NAIC, FRED, IRC, one rate-study source, LKQ 10-K, RB Global proxy).
5. Whether to fit the coverage slope from NAIC history (FITTED) or hold it ASSUMED until a published elasticity is found.

## 8. Memo statements to tighten (evidence check)

- "IRC uninsured rate 15.4% vs 12.6%" is liability-uninsured; the model needs collision/comprehensive penetration. Use NAIC coverage counts for the volume claim and keep IRC as context.
- "22.7% (up from 21%)" matches CCC (21.0 → 22.7). "Recycled and OEM both decreased" is true but recycled fell only 10.7 → 10.5; the memo should give the size.
- "0.84–1.69 points suppressed by a 15% Taiwan tariff with a price-response coefficient of 2": the coefficient needs a source; the other session verified a 1 May implementation for qualifying categories, not national exposure.
- "~5.2% revenue loss in Q4'26": derive in-model; the ledger arithmetic gives roughly 4.7–6.1% depending on the denominator.
- "56.6% → 55.3%": matches the workbook exactly; cite E3.
- "14.8k vs 19.1k acres": RB Global figure checkable on disk; the Copart figure needs a located citation.
- Stephens quote: the held note says it is "possible" a cyclical issue is being confused with a secular one; attribute precisely.

## 9. Findings from the 2 October source pass (before any model change)

**Thesis 2 number origins.** The repository's own parameter audit (29 Sep, `docs/aftermarket_parameter_audit_2026-09-29/README.md`, "What the original numbers actually were") records that the bridge inputs were "illustrative scenario choices, not extracted estimates": basket 65/25/10, eligible share 40%, prices 1.00/0.50/0.60, donor exposure 25%, contribution-to-bid 1.5×, transmission 50% are all marked Assumed with "no dataset establishes it". The numbers that do have sources are the CCC national shares (dollar and count, 2020–2025), the Mitchell 2016 matched discounts (23–30%), CCC all-parts spend (36–44% of the bill by age) and Sturgeon's 2018 recycler margins. The re-base in §2 therefore replaces, not re-labels, the six assumed inputs.

**Thesis 3 documentation now on disk (VERIFIED unless stated).** RB Global FY2025 10-K: 333 locations, 6,143 owned + 8,660 leased = 14,803 acres (US: 250 locations, 4,431 owned, 7,769 leased), plus >1,800 option acres for catastrophes; insurance-supplier agreements cancellable on 30–90 days' notice; top three vehicle suppliers ≈ 23% of FY2025 consolidated revenue; FY2025 automotive lots 2,447.7k (+7%), Q2 2026 automotive lots 658.8k (+11%) with GTV per lot ≈ $3,717 (+2.5%); seller revenue −1% from automotive price incentives; take rate 20.0% vs 21.1%. RB Global 2026 proxy: director Michael Sieger, appointed 2023, three decades at Progressive (a former Progressive executive, not a Progressive representative; the memo should say so). Copart FY2026 10-K: new sentence that certain seller arrangements are non-exclusive and terminable on limited notice; 286 facilities; insurers 79% of vehicles processed (81%, 81% prior). Dated expert items (UNVERIFIED, second-hand) exist in the owner's `~/Downloads/CPRT_share_loss_build.xlsx` Contract_Calendar tab: State Farm RFP out since ~2025 and an Illinois pilot to IAA; Progressive IAA agreement in principle Feb 2026, executed May 2026, all 50 states; GEICO RFP 1–2 years out (Jul 2025); Liberty Mutual 3-year master agreements; Erie/regionals shifting with IAA additions in Pennsylvania. The Messages-attachment share build could not be opened by any process in this environment (EPERM); its quote bank and precedents tabs are not yet extracted. Copart's "19.1k acres" is not in any of the 17 call transcripts or the FY25/FY26 10-Ks; the citation must be supplied or the claim replaced by facility counts.

**Thesis 1 sources fetched.** FRED CPI motor vehicle insurance (`raw/fred/CUSR0000SETE.csv`, VERIFIED). IRC press release, Uninsured and Underinsured Motorists 2017–2023 (`raw/irc/`, VERIFIED): 15.4% uninsured in 2023, 18.0% underinsured, 33.4% combined, up 10 points since 2017. MoneyGeek lapse study (`raw/discovery_2026-10-02/moneygeek_lapse.html`): the 22.4% figure is a nine-insurer quote comparison, so it is a rate-comparison estimate, not a filing. NAIC Auto Insurance Database Report: HTTP 403 behind bot protection; not retried, no workaround. Alternative: the Insurance Information Institute republishes the NAIC collision and comprehensive coverage shares by year (one fetch, labelled as a republication).

**LKQ FY2025 10-K** fetched (`raw/sec/lkq/10k_latest.htm`) for the thesis-2 dismantler bound; not yet read.

## 10. Build status, 2 October 2026 — done

Implemented in `model/CPRT_Model_v2.xlsx` (rebuild: `./.venv/bin/python scripts/build_cprt_model.py && ./.venv/bin/python scripts/verify_cprt_model.py`): D Coverage data tab; E2 block F (coverage index, premium burden, three forward paths; r reverse-solved live); E3 blocks F (probability-weighted moves, path check, derived Progressive effect) and G (parity evidence); E4 re-based on CCC dollar shares and the Mitchell price with a path selector (observed trend default, memo stress alternative, engine-basket parity row); Scenarios recut to seven cases with Δ vs case 1, case 0 and JPM; RPM selector 1–7 (default 2, known facts); Sources tab generated from the inputs (142 inputs, 0 without a source note); Checks 13 live rows, all PASS. Results and the thesis table are in `MEMO_APPENDIX_THESES.md`. Open: Copart acreage citation; NAIC coverage history (site refused); the share build's quote bank and precedents (file not openable here); recycled/OEM price (ASSUMED); donor-bid coefficients (ASSUMED, visible).

## 11. Data-and-source audit, 2 October 2026 (later)

New `D Facts` tab: 42 verified, measured, engine or second-hand data points the engines use, each with value, unit, evidence label, source, date and file or URL. Engine tabs now link to it (E1 anchors; E3 parity block, move sizes and probabilities, listed-inventory split, share y/y, Barclays commission and concession; E4 CCC shares, parts share, Mitchell price, observed-trend steps; E5 engine anchors, ASP and Manheim references; Scenarios JPM benchmark). Typed inputs fell from 144 to 107, all of them parameters, toggles or labelled assumptions, every one with a source note. New Checks rows: verified/measured/engine data typed on engine tabs instead of linked (0); inputs without a source note (0). All case results unchanged by the relinking.
