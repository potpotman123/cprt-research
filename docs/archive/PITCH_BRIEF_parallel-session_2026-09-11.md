> **ARCHIVED 2026-09-11 — superseded. Do not build on this document.**
> A brief written by a parallel session without access to the working scraper. Good on competition mechanics and the SOLS deck teardown (absorbed into `HANDOFF.md` §1 and §8). **Wrong on six factual points** — TLS-fingerprint diagnosis, the ~1,800-row lot.xml claim, 'CDX never run', the lot-ID clock recommendation, the unit-basis 'conflict', and the acres × $/acre capex method — each resolved in `HANDOFF.md` §4. Its fee-schedule numbers (line ~188) are unsourced and were the origin of a circular-provenance trap.
> Current handoff: `HANDOFF.md`. Results and every retraction: `findings.md`.

---

# CPRT pitch — full handoff brief

You are taking over research for a stock pitch on **Copart, Inc. (NASDAQ: CPRT)** for the HFAC × Citadel Intercollegiate Stock Pitch Competition. This document is written by the Claude session that did the prior work. It contains what was established, what was not, what I got wrong, and how to avoid repeating it.

Read the whole thing before starting. The most important sections are **§4 (my failure modes)** and **§6 (what actually wins)** — the research is recoverable, bad judgment about what to research is not, given the clock.

---

## 1. Constraints and clock

- **Today: September 11, 2026.**
- **Interest form closes September 18** — 7 days. Team of 2–4 must be named.
- **Preliminary submission due October 2** — 21 days. **2-page PDF maximum, including appendix**, plus a model.
- Finalists notified Oct 12; event Oct 22–24.
- Universe is exactly one of: ABNB, ADBE, CPRT, GEV, NCLH, NKE, SBUX, SPOT. CPRT is chosen.
- Long or short permitted. **Horizon 3–12 months** — so roughly January through October 2027.
- Citadel is a multi-manager pod shop. They think in catalysts, estimate revisions, and dated events. A thesis whose payoff is "in five years the fleet gets more expensive to repair" is correct and useless here.

**Two pages is brutally short.** Every paragraph has to survive a "does this change the conclusion" test. See §6 for the measured space allocation of decks that actually won.

---

## 2. FIRST TASK, before anything else

**Copart reported FY26 Q4 and full year on September 10, 2026 — yesterday.** Nobody in the prior session has seen it. It is Jay Adair's first call back as CEO and the first live opportunity for anyone to ask about the CCC situation.

Pull, in this order:
1. The FY26 Q4 press release and full-year financials (businesswire / Copart IR).
2. The Q4 earnings call transcript — **read the Q&A section closely**, especially anything on CCC, capital allocation, buybacks, unit trends, and the whole-car business.
3. The FY26 10-K when it files (historically early-to-mid October — check whether it is out; if it is, it supersedes several items below).
4. Analyst reactions and any estimate revisions since.

Everything in §3 below is pre-Q4. Treat it as the state of knowledge on Sept 8, not today. **Reconcile it against the actual print and flag anything that changed.**

---

## 3. What was established, with confidence levels

### VERIFIED — sourced this session

**The CCC situation (this is probably the pitch).**
Bloomberg reported August 18, 2026 that **Copart is among the suitors for CCC Intelligent Solutions Holdings (NASDAQ: CCCS)**, alongside private equity firms GTCR and Veritas Capital. CCC's market cap was ~$4.2B at $7.14/share; the stock was down 27% over the prior year; it was valued near $8B when it last explored a sale in 2023. **Elliott Investment Management** took a stake and drove the sale process. Copart's market cap ~$29B. Deliberations ongoing, no agreement certain, all parties declined comment.
*Why this matters more than it looks:* **CCC's software is what determines whether a vehicle is declared a total loss.** Total loss frequency is the single variable that creates Copart's entire supply. A salvage auctioneer acquiring the total-loss decision engine is either the most important strategic move in the company's history or a catastrophic conflict with its own customers — the insurance carriers. Note also that Copart's cash balance is **$4.2B**, matching CCC's market cap almost exactly; it could pay cash.

**CEO transition.** Announced June 29, 2026: **Jeff Liaw stepped down as CEO effective July 31, 2026** — the literal last day of the fiscal year — with **Jay Adair** (Executive Chairman, prior CEO, ~3.14% holder) resuming the role. No stated reason, no successor search, Liaw retained as Special Advisor. Seven weeks later the company is reported bidding $4B+ for CCC.

**Q3 FY26 actuals** (quarter ended April 30, 2026):
- Global insurance units **−2.7%** YoY; US insurance units **−4.2%**; US inventory **−4.7%**; US assignments down low-single-digit
- Copart Direct units **−26.3%** (stated as a deliberate shift of lower-value units to the direct buy channel)
- ASP **+4.6%**; US insurance ASP **+4.1%**, a seasonally adjusted record
- Revenue **$1.24B (+2.1%)**; international revenue **$234.2M (+14.1%)**; international operating margin **31.5%**
- Global gross margin **46.3% (+71bp)**; operating income $464.3M (+2.8%)
- **Cash $4.2B, zero debt, $5.5B liquidity**
- **Buybacks: 43.4M shares for $1.6B fiscal YTD** — a scale Copart has never run before. This is a capital allocation regime change and almost nobody is writing about it.
- Management: "claims activity remains softer as consumers adjust insurance purchasing behavior" in response to rising premiums

**Progressive.** Routes roughly **75% of salvage volume to IAA, 25% to Copart** — inverted versus other top-10 carriers. Progressive **passed State Farm as the #1 US auto insurer in May 2026**, first change since WWII, and adds ~3M policies annually. Source: In Practise expert interviews.
*Correction to a widespread claim:* Progressive has **not** "almost entirely shifted to IAA." It is 75/25, and it appears to be an established allocation rather than a recent cliff. But the growth dynamic is arguably worse than a one-time shift: the fastest-growing large carrier is IAA-weighted, so the drag compounds rather than annualizing away.

**Scraping reconnaissance** (see §7 for the full picture): `robots.txt` disallows `/public/data/`, `/downloadSalesData`, `/memberFees`, `/lotSearchResults/`. Sitemaps are published at `copart-sitemaps.com`. `lot.xml` pages 1–3 total only ~1,800 entries and are ~89% clean-title — an SEO subset, not inventory. `sale-list-results.xml` has ~1,144 entries giving the complete yard roster with numeric IDs plus every scheduled auction date. Yard 309 (CA Adelanto) showed 591 lots with full per-lot detail visible logged out. Purple Wave shares Copart's lot-ID sequence (IDs observed 41M–99M). **`www.copart.com` returns 403 to non-browser HTTP clients** — TLS fingerprinting, not header discrimination.

### UNVERIFIED — do not build on these without checking

- **The FY26 quarterly unit series.** A third-party analysis reports insurance unit YoY of **−7.3% / −4.8% / −3.1%** for FY26 Q1/Q2/Q3. That Q3 figure conflicts with the −4.2% US / −2.7% global above. Different bases, probably, but **the entire unit thesis depends on getting this series right.** Reconcile it from primary sources and document which basis is which.
- **The whole-car overhaul and its "spring–summer 2027" timing** — that is one writer's characterization of CEO commentary, never checked against a transcript. If real, it lands inside the pitch horizon, which would matter. Verify or discard.
- Whether the Internet Archive CDX has any Copart lot-page or fee-schedule history (see §7).
- Whether lot IDs are monotonic in time within a partition.
- Whether Copart's maintenance capex residual tracks D&A.
- Copart's actual carrier mix — nobody discloses it, and both the leading public bull and the leading public bear assert things about it without sources.

---

## 4. How I failed, and what to do differently

This section exists because the prior session wasted a lot of the available clock. Read it as a list of specific, observed failure modes in the model you are also running on — not as ritual humility.

**I generated architecture faster than I verified premises.** I produced a scoring rubric, a two-gate mechanism test, a memo space budget, and a seven-tab model spec before I had confirmed a single load-bearing fact about the company. The CCC acquisition — almost certainly the most important thing on the tape, reported three weeks earlier — I did not find until the user told me to stop talking and go do things. **Verify the tape before you build a framework.** A ten-minute search for recent news beats a day of structure.

**I proposed data sources without feasibility-testing them.** Copart UK Companies House filings, a Wayback fee-schedule time series, sitemap-based inventory enumeration — each was described confidently and each died on first contact with reality. **Before recommending a dataset, spend five minutes establishing it exists and is reachable.** Say "I haven't checked whether this is available" when you haven't.

**I made a specific arithmetic error about mean reversion.** I wrote that a YoY decline "turns positive mechanically" once it laps. It does not — **lapping takes the drag to zero, not to positive.** Growth requires a new driver. This error is easy to make and very easy for a judge to catch.

**I asserted an unverifiable fact as support.** I claimed Progressive insures an older fleet, which would have supported a total-loss argument. No public source publishes vehicle age by carrier. I retracted it, but only after being asked for a citation. **Anything that conveniently supports the thesis deserves a source before it deserves a sentence.**

**I gave a one-sided directional conclusion.** On land capex I argued that separating maintenance from growth capex makes Copart look cheaper. The source I was critiquing had already made the opposite and better point — that current FCF is *flattered* because post-COVID land spend has been low. Both adjustments are real and they pull in opposite directions. **When an adjustment has two signs, compute it; don't pick the one that helps.**

**I over-corrected whenever pushed.** Across this project I reversed position on NCLH, on the Copart short, on Nike, and on the land-capex direction, every time in response to pushback rather than new evidence. Sometimes the reversal was right. The point is that **my agreement is weak evidence** — if I concede a point immediately, re-derive it yourself rather than banking it.

**Practical instructions that follow:**
- Tag every number you produce as VERIFIED (with a URL), DERIVED (with the calculation shown), or ASSUMED.
- When the user proposes a framing, check it before adopting it. The "Progressive left for IAA" premise was wrong and went unchallenged for a long time.
- Prefer killing a thesis early to nursing it. Four separate signals said the scraping path was expensive before anyone admitted it.
- My knowledge cutoff is May 2026. Everything in §3 after that date came from searching, and anything else post-cutoff I would simply invent. **Search rather than recall for anything current.**

---

## 5. The two best public analyses, and where each breaks

Knowing these is worth more than reading twenty sell-side notes, because they define what is already priced into informed opinion.

**The bull: "Undiscovered Compounders," a ~55,000-word Copart deep dive (Substack, Aug 2026).** Core claim: the insurers in Copart's mix have passed their cyclical trough, and **PIF growth — not market share — drives the unit recovery.** Builds an EBIT sensitivity model: coefficients for service units (a), variable site costs on total units (b), and purchased units (c), weighted US/international, yielding **~$30.7M of EBIT per point of unit growth** ($26.5M US, $4.2M international). Values on EV/unlevered FCF at the 35th percentile of a ten-year distribution.

Where it breaks:
- Coefficients are fit on a single Q3-26 TTM window — measured while volume was *falling*. Cost behavior on the way down may not describe cost behavior on the way up. His robustness check (FY25, 2yr, 3yr averages) uses four heavily overlapping windows *all inside the same downturn*, so it demonstrates arithmetic consistency, not robustness.
- He conflates two things inside one coefficient: **per-car economics** (stable across the cycle, best estimated on long history) and **scale** (how many cars equal one point — must be current). Separating them is a real methodological improvement.
- On RPU he quotes management's *attribution language* ("driven by higher ASPs") against a *quantitative* claim. Q1-26: fee RPU +7.5% on ASP +8.4%. But RPU growth = fee-schedule hikes + ASP effect + mix. If the fee cadence is 5–7%, ASP's contribution is ~1–2.5pp on ASP of +8.4% — **implied elasticity ~0.15–0.30**, which is the bear's number, not his.
- He states that **EV/owner-earnings (EBIT + D&A − maintenance capex) is the correct metric**, that EV/unlevered FCF is distorted by the land cycle and currently *flatters* FCF — and then, unable to estimate maintenance capex ("management doesn't produce it. Not once"), percentile-ranks the distorted series anyway. **He identifies the gap and abandons it. That gap is an opening.**

**The bear (a comment thread on that piece, and it is the sharpest bear case available).** Claims: unit share shifts within the big three carriers are net negative and continuing; the regressive fee schedule is well known and RPU growth is mostly fee hikes at 5–7% ASP-adjusted, so units + RPU together give LSD service revenue at best; governance is mediocre (insiders sold from peak through a 50% drawdown while denying share loss; the CCC pursuit will alarm carriers who think Copart wants to influence total-loss rates; track record outside the core — International, Purple Wave, NPA — is weak); 38x exit multiple is indefensible for LSD growth, and **GAAP margin is flattered by land capex running through cash flow rather than income.**

Scoring it honestly: the bear wins on RPU, wins the second half of the multiple argument (and finds exactly the seam the bull conceded), and has the better *question* on carrier mix though no sources. The bull wins on epistemics and on the multiple percentile (the bear misread EV/unlevered FCF as EV/FCF). **Net: informed opinion tilts bearish on fundamentals, and the bear's conclusion is roughly consensus.** A long has to beat this specific argument, not a strawman.

---

## 6. What actually wins these competitions

The prior session measured the space allocation in eight Culverhouse/CIMG competition decks and read the user's own second-place Citadel deck. The patterns are consistent and specific.

**Measured space allocation.**

| Section | Winners (median) | Non-winners (median) |
|---|---|---|
| Business description | **13%** | 35% |
| Evidence | **40%** | 16% |
| Valuation | **10%** | 23% |

Winners spend roughly a third as much explaining what the company does and two and a half times as much on evidence. Judges know what the company does, or can be told in three sentences. **In a two-page memo this means: no more than a short paragraph of business description, and the valuation section is a small table, not a DCF walkthrough.**

**The discriminator between winners and finalists: mechanism inversion vs. magnitude re-sizing.**
- *Re-sizing*: "the market says units fall 5%, we think 9%." Same causal model, different number. This is what most good pitches do, and it reliably places second.
- *Inverting*: "the market believes X causes Y; in fact X causes not-Y," or the causal arrow runs the other way, or the variable everyone is watching is downstream of one nobody is watching. This is what wins.
- Test your thesis against this explicitly. If a judge could accept your whole analysis and still hold their prior causal model, you have re-sized.

**From the user's own SOLS deck (Solstice Advanced Materials, 2nd at Citadel) — the structure to copy:**
- **An explicit alpha statement on the second slide**, naming the source of edge in one sentence: *"Information asymmetry vs. Street informed by KOL calls and data-scraping gives us differentiation on UF6 Conversion & Refrigerants segments."* Say where your edge comes from; don't make the judge infer it.
- **"No Mgmt. Disclosure of Unit Economics = Opportunity."** The organizing principle. Find the segment management refuses to break out, then *construct* its economics bottom-up. They built a $/kgU contract price waterfall (pre-2017 $6.00 → 2023 $28.50 → 2024 $35.00 → 2025 $50.00 → 2026E $55.00) against COGS+OpEx ($15 → $17), landing **52% segment EBITDA margin vs. the Street's 33% — a 67% delta worth $81mm.**
- **One hard physical ratio computed from primary sources.** In refrigerants: 9.97 lbs/ton for liquid chilled water vs 3.52 for DX air-cooled, so **2.86x** — against a Street belief that liquid cooling is *more* efficient. A single checkable number that inverts a widely held assumption is worth more than ten pages of qualitative argument.
- **An explicit per-segment bridge to Street**, with a percentage delta on each, summing to a total ($1.18B vs $1.04B 2026 EBITDA, 13.6%).
- **A competitor-model annotation slide**: side-by-side screenshots of the UBS model marked up — *"NO PxQ analysis," "NO segment COGS breakout," "Key values are hardcoded," "NO new contract waterfall"* — against their own build. This is the single most persuasive slide in the deck. It shows, rather than asserts, that the Street hasn't done the work.
- **A named KOL roster with credentials**: ex-President of Nuclear Fuel Operations at BWXT, a 40-year uranium fuel expert, the Standard Nuclear CEO, an ex-Centrus contact.

**The user's own hypothesis** — that you need a creative thesis *plus* either novel data or a novel re-analysis — is right, and I'd add two refinements:

1. **The evidence must be checkable by the judge.** A proprietary dataset the judge cannot audit gets discounted. A derivation from public primary sources that the judge could in principle reproduce gets full credit. This is why the $/kgU waterfall works: every input is defensible.
2. **A dated, falsifiable catalyst is the third leg, not optional** — at least for Citadel. The pitch needs a sentence of the form: "on [date], [specific observable] will happen, and it will move the stock because [mechanism]." And a stated kill condition: what observation would prove you wrong. Pods respect that; it reads as a real position rather than an essay.

**A useful negative pattern:** "reading a public document nobody bothered to open" is *diligence*, not edge. Statutory filings, obscure disclosures, a buried footnote — valuable, but a lower grade of contribution than deriving a quantity that exists nowhere. Aim for derivation.

---

## 7. The data situation — what works and what is closed

**Closed, do not re-litigate:**
- `www.copart.com` returns **403 to non-browser HTTP clients** (urllib, requests, curl). This is TLS fingerprinting; headers do not fix it. Getting past it means impersonating a browser's TLS stack, which is **out of bounds** — this work goes in front of hedge fund judges and a provenance question you cannot answer cleanly is worse than missing data.
- `robots.txt` disallows `/public/data/` (the internal JSON API), `/downloadSalesData`, `/memberFees`, `/lotSearchResults/`. Respect it.
- Do not authenticate and then scrape. Copart's member agreement prohibits automated access; unauthenticated public browsing is a far cleaner posture. If an account is used, use it by hand.
- `lot.xml` is a ~1,800-row SEO subset, ~89% clean-title. It is not inventory and cannot nowcast insurance units.
- Internet Archive coverage of Copart fee pages and sitemaps appears to be **single snapshots, not time series** (probed via the availability API with guessed URLs — CDX would confirm).

**Open and worth an hour each, in priority order:**

1. **CDX queries.** These were never run; the prior session's fetcher was blocked from `web.archive.org/cdx` but a normal client is not.
   ```bash
   curl -s 'https://web.archive.org/cdx/search/cdx?url=copart.com/lot/*&fl=original,timestamp&limit=5000'
   curl -s 'https://web.archive.org/cdx/search/cdx?url=copart.com*&fl=original,timestamp&filter=original:.*[Ff]ee.*&collapse=digest&limit=1000'
   curl -s 'https://web.archive.org/cdx/search/cdx?url=copart.com/saleListResult/*&fl=original,timestamp&limit=5000'
   ```
   The first matters most: archived lot pages are free `(lot_id, date)` anchor pairs, and if lot IDs are monotonic within a partition, the ID is a clock — you can reconstruct historical assignment volume without ever having run a crawler. `collapse=digest` on the second returns only captures where content *changed*, so the output is the fee-change timeline if one exists.

2. **The Export button** on the sale-list page. It is a first-party feature. If it emits a CSV logged out, the whole per-lot data problem collapses into a download. Check this before writing any crawler.

3. **A real browser.** Playwright driving actual Chrome works where urllib does not, and a browser loading public pages is a browser, not circumvention. Rate-limit hard, log provenance. Treat any output as a supporting exhibit, **not load-bearing** — the prior session burned hours here.

4. **Third-party salvage-auction history services.** An ecosystem of sites retains past Copart/IAA records with sale prices, searchable by VIN, some with years of depth. Cleanest route to historical ASP distributions. Check their terms.

**Completely unblocked, high value, nobody has done it:**

- **SEC EDGAR.** Copart CIK **0000900075**, FY ends July 31. `https://data.sec.gov/submissions/CIK0000900075.json` and `https://data.sec.gov/api/xbrl/companyfacts/CIK0000900075.json` (SEC requires a descriptive User-Agent with a contact email). Pull FY2016–FY2026: revenue, service vs purchased-vehicle revenue, operating income, D&A, capex, cash, shares, and — from the Item 2 Properties narrative, not XBRL — **acres owned, acres leased, facility count.**

  Then compute the thing the best public bull said he could not:
  ```
  land_capex        ≈ Δ(acres owned) × regional industrial land $/acre
  maintenance_capex ≈ total_capex − land_capex − new-yard construction
  owner_earnings    =  EBIT + D&A − maintenance_capex
  ```
  Compare the residual to reported D&A. **GAAP does not depreciate land**, so D&A already excludes the growth asset — which makes D&A an unusually defensible maintenance-capex proxy *at Copart specifically*. If the residual tracks D&A, the proxy is validated and you can build a clean ten-year EV/owner-earnings series. If it diverges, the size and sign of that divergence is itself the finding. **Either outcome is publishable. This is the highest-certainty original contribution available.**

- **The fee schedule**, structured as a function `fee(asp) → dollars`. Pages: `/Content/US/EN/Basic-Member-Fees`, `/content/us/en/premier-member-fees`, `/content/us/en/member-fees-us-licensed`. Known structure to verify: **$95 gate + $15 environmental fixed per car**; **flat $1,000 buyer fee in the $10,000–15,000 band**; **7.50% + $250 above $15,000**. Run any ASP distribution through it and you can decompose RPU growth into fee-hike vs. ASP contribution — settling the central quantitative dispute between the bull and the bear.

- **Carrier data.** Progressive publishes **monthly** results including policies in force (investors.progressive.com) — a monthly public feed on the most contested carrier. GEICO via Berkshire filings; State Farm via NAIC statutory; **NAIC state-level private passenger auto market share by carrier.** Pair NAIC carrier share *by state* with Copart volume *by state* and you can estimate implied carrier exposure econometrically, then weight by disclosed PIF growth for a bottom-up unit forecast. Neither the bull nor the bear has this.

- **Everything on CCC.** CCCS filings, the Elliott 13D/13G, proxy materials, any merger agreement or 8-K, sell-side on CCCS, and the antitrust/vertical-integration commentary. Plus CCC's own disclosures on total-loss valuation products and market share among carriers.

- **KOL calls.** The user's mother owns a Farmers insurance agency. She cannot supply carrier data — that is policyholder PII under GLBA, prohibited by her agency agreement, statistically useless at n=1 agency, and a disqualifying provenance problem if a judge traced it. **But her introductions are gold**: Farmers total-loss adjusters, claims managers, a body shop owner, a licensed salvage buyer. Legitimate expert conversations about industry practice, which is exactly what the SOLS deck ran on.

  **The single highest-value question to ask them:** *would carriers accept their salvage vendor owning the software that decides whether a car is a total loss?* That question determines whether the CCC deal is strategic genius or self-immolation, and no public analyst has asked it.

---

## 8. Candidate theses, honestly scored

**A — The CCC / capital-allocation regime change. Strongest, and it is what I would build.**
In ten weeks Copart changed CEOs with no succession warning (founder-era Adair returning), ran $1.6B of first-ever-scale buybacks, and entered talks to spend its entire $4.2B cash pile on the company whose software decides whether a car is a total loss. Meanwhile the entire public debate — both the best bull and the sharpest bear — is arguing about unit percentages and exit multiples.
- *Inversion, not re-size:* the market is modeling Copart as a volume story; it has become a capital-allocation and vertical-integration story. Total loss frequency is Copart's supply, and it is trying to buy the thing that sets it.
- *Catalysts inside horizon:* deal announced or abandoned; the Q1 FY27 print (~late Nov 2026); Q2 FY27 (~late Feb 2027); Q3 FY27 (~late May 2027).
- *Evidence path:* filings, transcripts, CCC disclosures, and carrier KOL calls on the conflict question. Needs no scraping.
- *Direction is genuinely open.* Long: buying the funnel at a distressed price with 5%-yielding cash, defensively, as Progressive uses IAA to erode Copart's scale advantage. Short: burning the balance sheet and $170M of interest income on an asset Copart's own customers cannot accept, while carrier relationships are already fraying. **Let the KOL calls pick the side.**

**B — Owner earnings / maintenance capex. Best supporting leg.** Resolves a dispute both public analysts got tangled in, using only 10-Ks. Not a catalyst; it is your valuation section. High certainty of producing *something*.

**C — RPU decomposition.** Settles the bull/bear fight quantitatively. Supporting exhibit, one exhibit's worth of space.

**D — The unit nowcast ("we counted the cars").** Was the headline; is now doubtful. Requires the browser route to work and a backtest that may have no historical data. Pursue in background only.

**E — The secular total-loss story** (vehicle technology → repair cost → TLF). True, well understood, **no catalyst in twelve months.** One sentence in the memo, positioned as "why terminal value isn't impaired." Never the thesis.

**F — Weather/CAT.** A lottery ticket, not a view. Risk section only, as two-sided skew.

---

## 9. Suggested sequence

**Days 1–2 (by Sept 13):** FY26 Q4 print and transcript. Everything public on CCC. Reconcile the unit series. Verify or discard the whole-car 2027 timing. Run the CDX queries. *Then* decide long or short.

**Days 3–7 (by Sept 18):** EDGAR pull and the owner-earnings build. Fee schedule as a function. Progressive PIF and NAIC series. Book the KOL calls — they have the longest lead time and the most upside. **File the interest form and name the team.**

**Days 8–16:** The model. Carrier-mix attribution. Run the KOL calls. Browser-based collection in the background if someone else can own it.

**Days 17–21 (by Oct 2):** Write. Two pages, to the measured allocation: ~13% business description, ~40% evidence, ~10% valuation, remainder thesis/catalysts/risks. Build the model to support the memo, not the reverse.

---

## 10. Deliverable standard

The memo needs, in order of importance:

1. **An alpha statement in the first three sentences** — what the variant view is and where the edge comes from.
2. **A causal mechanism**, stated as a mechanism, that inverts rather than re-sizes.
3. **Evidence occupying ~40% of the space**, at least one piece of which is derived from primary sources rather than cited.
4. **A dated catalyst** and a **stated kill condition**.
5. **A bridge to consensus** — where your numbers differ from the Street, line by line, with the delta in percent.
6. **A valuation table**, small.
7. **Provenance you can defend** — every dataset's source, method, and date, in the appendix.

And keep a running `PROVENANCE.md` and `findings.md` from day one. When a judge asks "how do you know that," the answer cannot be "a model told me."
