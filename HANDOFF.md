# CPRT research — handoff for the next agent

**Current model/research update (27 September 2026):** Start with [MODEL_AND_RESEARCH_HANDOFF_2026-09-27.md](docs/MODEL_AND_RESEARCH_HANDOFF_2026-09-27.md). It records the repair and value audits, quarterly service-revenue build, corrections, current four-main-tab presentation, and the latest scope. The service-revenue-only scope there supersedes this file's older three-statement/DCF build sequence.

*Written 2026-09-25 for whoever (or whatever) picks this up. Organised by research thread: what we tried, why,
what we found, and where it led. Confidence is labelled on every result. Where we are not sure, it says so.*

---

## 0. How to read this repository

**Start here, then go where the question takes you.**

| If you need… | Read |
|---|---|
| the shape of the whole project in ten minutes | this file, §1–§3 |
| the model architecture the user is building (mechanisms A–E, tab map, build order) | `MODEL_BLUEPRINT.md` |
| how the age curves S(age), R(age), P(age) were derived and validated | `docs/AGE_CURVES.md` |
| the numbers, formulas and data in one workbook to copy from | `model/CPRT_Intermediate.xlsx` (built by `scripts/build_intermediate_xlsx.py`) |
| every result in the order it happened, **including every retraction** | `findings.md` (Addenda 1–17) |
| every host touched, its robots.txt status, what was saved where | `PROVENANCE.md` |
| how the collector and the sitemap data physically work | `ARCHITECTURE.md` |
| what each script / CSV is and whether it is live, analysis, dead-end or legacy | `scripts/README.md`, `data/csv/README.md` |
| the previous handoff with its detailed sections on competitors, theses, feasibility | `docs/archive/HANDOFF_2026-09-11_updated-to-09-25.md` |
| the expensive experiments a second session should run, specified end to end | `NEXT_STEPS_FOR_OTHER_CLAUDE_FABLE.md` |
| the model walk-through page with charts | `docs/walkthrough.html` (published as an artifact; `scripts/build_walkthrough_page.py`) |

**Confidence labels used throughout:**
- **VERIFIED** — in a filing, a transcript, or a fetched page on disk; you can re-read the source.
- **MEASURED** — computed from verified data by a committed script; you can re-run it.
- **FITTED** — a parameter chosen so a model reproduces measured statistics; the statistics are the evidence, the
  parameter is not.
- **ASSUMED** — our judgement, stated as such.
- **UNVERIFIED** — recalled or inferred, not yet found in a source on disk. Treat as a lead, not a fact.
- **RETRACTED** — was claimed earlier and is wrong. Kept so nobody re-derives it.

**Three habits this project learned the hard way** (the full list is §5):
1. Before saying something is unavailable, blocked or absent, show the request and the status code, or the `ls`
   output. Three separate agents on this project each declared something missing that was on disk.
2. State the mechanism before you regress, then do a units check on the result.
3. When the user pushes back, ask what new evidence arrived before conceding or digging in. The user caught more
   substantive errors here than the model did.

---

## 1. The task and the constraints

**Goal.** A pitch on Copart (NASDAQ: CPRT) — **long or short, whichever the data support** — for a student stock-pitch competition judged by hedge-fund
practitioners: a two-page PDF plus a model. Horizon 3–12 months. The user builds the Excel model themself; this
repository supplies the data, the mechanisms, the calibrations and the reasoning.

**Dates (UNVERIFIED — taken from a parallel session's brief with no cited source; confirm with the user):**
interest form Sept 18, preliminary submission Oct 2, finals Oct 22–24. Copart's FQ1 FY27 reports in late November,
after the finals, so no forward call can be validated before presenting.

**Research-ethics rules — the user's own, non-negotiable, and a judge may ask about them.**
- `robots.txt` first on every host, obeyed literally. Disallowed paths are never requested.
- At least 2 s between requests to a host; single-threaded; `prov.py` enforces it and logs every request.
- No authentication, ever. No paywall or CAPTCHA circumvention, no proxies, no IP rotation. A challenge page is a
  stop, not a puzzle: `job1_iaa.py` and `prov.py` detect "Pardon Our Interruption" / Incapsula pages and never parse
  them as data.
- Honest identification. SEC gets a descriptive User-Agent with a contact email; Copart and IAA get a conventional
  browser header set (they reject descriptive UAs). `prov.headers_for(url)` chooses per host — changing one broke
  the other once.
- Report blockers rather than work around them.

**Licensed content never committed** (`.gitignore` covers `raw/`, `data/cprt.db`, lot-level CSVs): 17 S&P earnings
transcripts, one Stephens sell-side preview, the Black Diamond SOLS model used as a formatting reference, and the
IHS-sourced ORNL tables 3.11/3.12/3.13 (marked "further reproduction prohibited"; extracts live in
`raw/ornl/tedb40/extracts/`). Numeric facts extracted from licensed sources are committed with provenance headers;
the sources are not. The GitHub remote is private.

---

## 2. The story in one page

1. **We started by scraping Copart's public sitemaps** to nowcast unit volumes, because Copart discloses no absolute
   unit count. It half-worked: listed inventory tracks reported inventory when the capture is clean, and fails when it
   is not, and we can tell which is which before looking at the answer (§3A). Several derived claims from the scrape
   did not survive: the lot-ID "clock", daily inflow as an assignments proxy, and every unit forecast built on it.
2. **The scrape's durable contribution turned out to be physical, not statistical:** cars per weekly sale event fell
   about 30% while sale events rose — operating deleverage you can see (§3H) — and, later, a daily Copart-versus-IAA
   inventory split nobody else publishes (§3G).
3. **Transcripts became the dependent variable.** Regex parsing of natural language failed badly; the quarterly series
   was hand-transcribed and cross-checked 15 of 15 against a sell-side exhibit (§3B).
4. **Revenue per unit turned out to be the strongest result.** Service RPU moves about half as much as vehicle prices
   and carries a +4pp intercept: fee and mix growth that compounds with prices flat. A first estimate (0.465) was
   retracted for an alignment error and rebuilt at 0.514 (§3C).
5. **Total-loss frequency was calibrated on industry data rather than Copart's six quarters:** the repair-versus-used-car
   price spread explains the cycle (β 0.0815 per pp, one-quarter lag, R² 0.81 on 27 CCC quarters) and passed a live
   out-of-sample test against a management-cited figure (§3D). The intercept, about 0.6pp a year, is drift the
   regression does not explain.
6. **The units decomposition then showed the FY26 unit decline was one account, not share loss** — and management said
   so in their own words on the FQ4 call. The Progressive volume left between April and July 2026, so it laps in
   FY27Q4, not earlier (§3E).
7. **To explain the unexplained TLF drift we built a fleet-ageing engine** (§3F). It says demographics add about
   0.16pp a year — a quarter of the 2019–2025 rise — and that the popular "ageing fleet" story is real but smaller
   than told. Along the way we found that S&P's average vehicle age is the wrong thing to calibrate a survival curve
   to, that the claim-frequency and totaling curves can only be *fitted* to published claim-mix statistics, not
   measured, and that one anchor we used (289M vehicles) is from memory and still unverified.
8. **Everything was assembled into one styled workbook** the user copies from (§4), verified cell by cell against the
   scripts, and the collectors were audited after two weeks, which found and fixed a bug in the IAA share (§3G).

**Direction is open (owner's instruction, 2026-09-26).** Everything before this date was written toward a long. Two
findings from the second session cut the other way and must be weighed without a thumb on the scale: (1) the ageing-fleet
contribution to total-loss frequency is measured from CCC's own buckets as ≈0 since 2023 (`reports/CCC_age_buckets_2026.md`),
so the demographic tailwind has already passed through; (2) the truck-heavy cohorts file fewer collision claims at higher
value, which lowers age-specific totaling propensity (`reports/E1_step3_hldi_class_losses.md`) — a supply headwind with a
calendar. Every report from here states what it implies for both directions.

**Where it leads next:** the user's model (DCF + three statements) with three build tabs — units, RPU, facility cost —
each handing one row to a revenue tab; manual pulls that would turn fitted curves into measured ones (§6); and the
two documents that do not exist yet but would change things: the FY26 10-K and the ACV acquisition's SC 14D-9.

---

## 3. Thread-by-thread ledger

Each thread: why we tried it, what we did, what we found, confidence, where it led, what is still open.

### A. Copart sitemap scraping — listed inventory as a nowcast

**Why.** Copart discloses unit *growth* only on calls, never levels; the public `lot.xml` sitemap lists every
lot with a URL slug carrying title type, year, make/model, state and yard. If listed inventory tracked reported
inventory, we would have a two-week read on a five-week disclosure.

**What we did.** Archived ~25 Wayback captures (2022–2026) and built a nightly collector (`scripts/job1_snapshot.py`,
LaunchAgent `com.cprt.job1`, ~23:00Z) that saves the sale list and the four `lot.xml` pages, parses slugs, and stores
snapshots in `data/cprt.db`. Back-tested union counts against reported US inventory YoY
(`scripts/backtest_inventory_v2.py`).

**What we found.**
- Pages rebuild on their own schedules and **overlap when out of sync** — up to 14.8% double-count if you sum pages.
  Union, never sum; and the overlap percentage is a free quality gate (MEASURED).
- **Gated (overlap ≤ 1%) captures track reported inventory well; ungated ones do not.** r 0.99 on the 4 gated pairs
  versus 0.83 on all 11 — but 4 pairs is not evidence of skill. The defensible claim is "the method works when the
  capture is clean, and we know when it is clean before looking" (MEASURED, small n).
- As of September 2026 the listing has shrunk to **three pages**; the fourth is empty and the third is partial and
  varies nightly. Union counts swing 128–149k; 8 of 16 nights pass the gate. Gated mean ≈ 143.6k vs 153.1k on the
  usable 2025-09-01 capture, about **−6% YoY** (MEASURED; single base capture; listed ≠ yard inventory).
- **Daily inflow/outflow between snapshots is not an assignments proxy.** Churn is 15–30% on out-of-sync nights and
  under 1% on the one synced pair: it is page rotation, not vehicles (MEASURED, negative result).
- **The lot-ID "issuance clock" is RETRACTED in full:** a line fitted to a staircase, an implied 0.02 IDs per car
  sold, and a negative correlation with units. Four claims, zero survivors (`findings.md` Addendum 14).
- Coverage is unknown: Little's-Law arithmetic implies 150–310k true US inventory against ~140–150k listed. Say
  "sitemap-listed inventory," never "US inventory."

**Where it led.** Keep the collector for the appendix and the physical series (§3H, §3G); do not build a unit
thesis on it. The negative results are worth publishing — no competing deck we reviewed showed a graveyard.

**Open.** Whether the shrink to three pages is a Copart-side change in what `lot.xml` lists (we have not found a
statement either way); whether the gate threshold should tighten now that page 3 is partial.

### B. The dependent variable — hand-transcribed transcript series

**Why.** No filing discloses Copart's unit growth, inventory growth or ASP growth by quarter; the calls do.

**What we did.** A regex transcript parser was tried first and **discarded** (133 of 176 cells missing, sentences
attributed to the wrong speaker; kept in `scripts/deadends/parse_transcripts.py` as the record). The series was
hand-transcribed (`scripts/reported_series.py` → `data/csv/reported_units.csv`) and cross-checked against a
Stephens exhibit: 15 of 15 cells match.

**What we found.** Three unit bases are disclosed on the same calls (US insurance ex-CAT, US insurance including the
CAT comp, global insurance); an apparent conflict between two earlier documents was three bases, not a disagreement
(VERIFIED). The Stephens exhibit's global-ASP column is **shifted one quarter** relative to the transcripts — do not
regress on it (`stephens_exhibit7.csv` is kept for corroboration only).

**Where it led.** Every regression in §3C–E uses this series. Its provenance is Tier 2 (transcript), and the
appendix must say so.

### C. Revenue per unit — a fee-and-mix engine, not a price pass-through

**Why.** Consensus models RPU as tracking used-vehicle prices roughly one for one. If it does not, the Street's
revenue line is wrong in a way that is cheap to show.

**What we did.** Implied RPU growth = (1 + service-revenue growth) ÷ (1 + unit growth) − 1, regressed on global ASP
growth, all three on the same basis, n = 17 quarters (`scripts/analysis_20260911.py` → `elasticity_rebuild.csv`).
A first estimate (0.465, intercept +4.51) was **RETRACTED**: it had used a misaligned ASP column and US units against
global revenue.

**What we found.** Service-RPU elasticity **0.514** (95% CI 0.29–0.73), **intercept +4.13pp**, R² 0.61 (MEASURED).
Management's total-RPU definition gives 0.752, intercept +2.84. Residual autocorrelation makes the effective n about
6 — disclose it. The intercept is the robust finding; it decelerated in FY26 (+5–6pp → +1.3 to +3.5pp), partly
CAT-comp distortion. Upstream, used-car CPI explains Copart's insurance ASP (β 0.599, r 0.77, n 15), and CPI
publishes two weeks after month-end against Copart's five, so the chain nowcasts: used-car CPI → ASP → RPU. The "0.1pp FY26Q4 back-test" quoted in earlier documents used the RETRACTED coefficients on management's total-RPU
  definition; with the rebuilt coefficients the chain misses FY26Q4 service RPU by ~0.8pp (predicted +5.2%, actual +4.4%),
  mostly at the ASP step (+2.1% predicted, +3.5% actual), and FY26Q4 sits inside the fitting sample (Addendum 19).

**Where it led.** Thesis #1 in the archived handoff; the RPU_Reg tab in the workbook; the user's RPU Build tab.
The forward RPU floor (+4.5–5.5% vs a Street implied ~3%) rests on the intercept holding — the FY26 deceleration
is the risk to state.

### D. Total-loss frequency — calibrated on industry data, not Copart's

**Why.** Copart's supply is total losses. CCC publishes total-loss frequency (TLF) quarterly for the industry; a
model of TLF calibrated on 27 industry quarters borrows far more strength than Copart's own six.

**What we did.** ΔTLF (pp, YoY) regressed on the **totaling spread** = repair-CPI YoY − used-car-CPI YoY, lagged one
quarter (`analysis_20260911.py` → `tlf_calibration.csv`, `totaling_spread_quarterly.csv`). Two TLF variants
(all-loss, non-comprehensive).

**What we found.** All-loss: **ΔTLF = 0.599 + 0.0815 × spread(t−1)**, R² 0.81, n 27, out-of-sample MAE 0.39pp;
non-comp: 0.609 + 0.0834, R² 0.79, OOS MAE 0.16pp but effective n ≈ 6 (MEASURED). A **live test**: management
cited a CCC figure not in any public edition (23.3% vs 22.4% in 2Q26); the model had predicted +1.28pp against the
actual +0.90pp. The spread collapsed from +15.7pp (2Q24) to +2.3pp (3Q25) — that is what hurt Copart — and recovered
to +8.3pp (2Q26). Separately, **most of the 2025 headline TLF rise is denominator shrink**: repairable claim volume
fell 9.7% as $1,000+ deductibles rose, so the ratio climbed while total-loss counts fell 2.9%. That cuts against
"structural TLF uptrend" while supporting a cyclical recovery — in CCC's own words.

**Where it led.** The Spread_Reg tab; the TLF term of the units identity (§3E). **The intercept (~0.6pp/yr) is
unexplained drift**, which is what motivated §3F. Use the spread term for 12 months, not the decade.

**Open.** CCC's quarterly series may be discontinued (last public point 2025Q3). The effective-n caveat is real;
the CI on β is honest but the drift term is not modelled by this regression.

### E. The units identity — one account, not share loss

**Why.** To say anything about units you have to separate the industry from Copart's share.

**What we did.** `(1 + Δunits) = (1 + Δclaims) × (1 + ΔTLF) × (1 + Δshare)`, with claims and TLF from industry data
and share solved as the residual, on a matched claim denominator so the deductible shock cancels
(`scripts/units_decomp_panel.py` → `units_decomp_panel_v2.csv`; `decomposition.csv`). Three claim denominators were
tried; the one that reproduces CCC's directly reported total-loss count (−2.9% CY2025) was kept.

**What we found.** Calendar 2025: industry pool −2.9%, Copart US insurance ex-CAT −2.35% → **residual +0.55pp, no
share loss** (MEASURED). FQ4 FY26: assignments −5.0%, but *"with the exception of 1 single customer loss, domestic
insurance assignments would be up 2.3%"* — management's words (VERIFIED). The account is **Progressive**, whose
volume fell from ~10–13k/month to ~600/month between **April and July 2026** (sell-side carrier table, licensed,
read locally). So the comp **laps in FY27Q4** (May–Jul 2027), not earlier — an earlier "Aug–Oct 2025" inference
was **RETRACTED**. Lapping takes the drag to zero, never positive; growth needs a new driver.

**Where it led.** FY27 units ≈ consensus; the variant view moved to RPU, margin normalisation, and FY28. The
Units Build tab in the user's model is this identity with three input rows and one output row.

**Open.** The claims term for 2026 is a range (Fast Track headlines and management's frequency comment), not a
level series; no free quarterly claim-count level exists.

### F. Fleet ageing — the age curves behind baseline TLF

**Why.** The spread regression leaves ~0.6pp/yr of TLF drift unexplained, and the popular explanation is an ageing
fleet. We wanted to know how much of the drift demographics can actually produce.

**What we did.** A cohort roll: fleet by age = sales by model year × survival; claims = fleet × R(age); total
losses = claims × P(age); baseline TLF = total losses ÷ claims (`scripts/age_curves.py`; full write-up
`docs/AGE_CURVES.md`).
- **S(age)** is EPA's published survival schedule (ORNL TEDB Ed.40 T3.15) stretched along the age axis by one
  parameter, fitted to the IHS/Polk 2013 census by single year of age and drifted to hit 2024 fleet counts.
- **R(age) and P(age) are FITTED, not measured.** No public source publishes claims per vehicle or total-loss
  rate by single year of age. Five parameters were chosen (minimum-distance / GMM-style, Nelder–Mead in Python,
  Solver in Excel) so the model reproduces eight CCC 2024 claim-mix statistics, then frozen and tested on 2019,
  2020 and 2025 statistics never used in the fit.

**What we found.**
- **S&P's average vehicle age is the wrong calibration target.** The IHS census itself implies ~2 years less than
  S&P's figure unless the 15+ bucket averages ~27 years. Calibrating to 12.8 forces 90% survival at age 17 and 341M
  vehicles — the artefact in the first worked example (`model/legacy/`). Calibrate to counts (MEASURED).
- The count-calibrated roll gives fleet growth 2020→2025 of +5.4% vs Experian's +5.1% — an independent check that
  passed (MEASURED). Experian's "12M fewer vehicles aged ≤6" is **not reproducible from sales under any survival
  curve** (sales alone give −9.7M with zero scrappage); we recorded it and did not fit to it.
- Fitted R: flat through age 6, then −8.6%/yr; a free 0–6 slope returned +1.6%/yr with no better fit, so it was
  fixed flat. Fitted P: 8% at age 0, 10% for ≤3 yrs, 20% at 7, 34% at 12, 43% at 17. Bucket values P(7+) 31.7% /
  P(0–6) 12.7% are stable under every survival assumption tried; the single-year interior is interpolation (FITTED).
- Out of sample: 2020 average claim / repairable / total-loss ages within 0.3 years; 2025 shares within 1pp; 2019
  repairable mix misses by ~3pp (claims were younger in 2019 — EV share and pre-AEB fleet are plausible reasons,
  UNVERIFIED).
- **Demographics add +0.16pp/yr to TLF (0.04–0.18 across survival assumptions), about a quarter of the 2019–2025
  rise.** The rest is level: the spread cycle, technology, filing behaviour (MEASURED given the fitted curves).
- **Forward, the same roll gives about zero:** +0.035pp (2025), +0.019 (2026), +0.006 (2027), slightly negative
  2028–30 with sales held at the 2025 level. The +0.16 is a 2019–2025 average, **not a near-term catalyst** (Addendum 19).

**Corrections made while building it** (all in `findings.md` Addendum 16): the "45.3% total-loss propensity at 13+"
anchor had no source and was dropped; the fit originally summed ages to 31 while the stretched curve is non-zero
to ~39 (now 45); the 289M VIO anchor is **from memory, UNVERIFIED** — swapping in Experian's on-disk 292.1M moves the
stretch by 1% and nothing downstream.

**Where it led.** The engine tabs in the workbook (Inputs, Curves, Calibration, Survival, Fleet, FleetByAge,
TLF_Roll) and one number for the Units Build: demographic drift. Honest version of the ageing-fleet story.

**Open.** HLDI publishes measured claim frequency by vehicle age — it would replace fitted R with data (user pull).
CCC 2026 Figures 18/22 data labels would pin P's interior. The k-drift path between 2013 and 2024 is linear by
assumption; only its endpoints are anchored.

### F2. Decomposing the fitted price intercept into drivers (2026-09-25, Addenda 20–21)

**Why.** The owner's standard: a fitted constant is not a finding until its drivers are named. Copart's realised price
grows ~3.3pp/yr faster than used-car CPI (the ASP-on-CPI intercept); a pod shop has the same fit.

**What we found.** (a) **Vintage drift, MEASURED:** the median model year of Copart's listed inventory advances one year
per year (2013 in 2022 → 2016 in 2025), so the typical totaled car is constant in age but newer in sticker; weighted
through the fleet roll with BLS new-vehicle CPI (fetched 2026-09-25, `raw/bls/`), this adds **~1.0pp/yr in 2022–26,
rising to ~1.4 by 2028** — about 29% of the intercept. (b) **Body mix:** light-truck share of the total-loss pool rises
57% → 62% (2024 → 2027) → 68% (2030); its price effect needs a truck-vs-car salvage value ratio (UNSOURCED, `ASP_Drivers!B4`).
(c) The totaling spread does **not** explain the residual (corr +0.07). (d) The remaining residual (~2.2pp/yr) co-moves
with CPI and is unexplained — export demand and fee tiers are candidates (`NEXT_STEPS_FOR_OTHER_CLAUDE_FABLE.md` E6, E7).
The `ASP_Drivers` tab in the workbook lays this out by calendar year.

**Corrections in the same pass (Addendum 19):** the "FY26Q4 back-test to 0.1pp" on RPU is retracted (retracted
coefficients, in-sample; the current chain misses by 0.8pp at the ASP step); the blueprint's facility-cost line had mixed
bases (comparable +0.6%/+1.1%, not −9.7%); forward demographic drift is ≈0 for 2026–27.

**Where it led.** The owner's critique that the theses are observations, not explanations. The expensive experiments
that would supply explanations are specified in `NEXT_STEPS_FOR_OTHER_CLAUDE_FABLE.md`.

### G. IAA — the duopoly inventory split

**Why.** IAA (RB Global) is Copart's only real competitor; a daily Copart-versus-IAA listed-inventory split is a
share tracker nobody publishes.

**What we did.** `www.iaai.com/robots.txt` disallows four paths and carries a *commented-out* `#Sitemap:` line pointing
to an obfuscated path that is **not** disallowed. We recorded that judgement call in `PROVENANCE.md` for the user
and built `scripts/job1_iaa.py` (nightly after the Copart job): three ~6.8MB vehicle sitemaps plus branch and auction
files → `duopoly_daily`.

**What we found.** IAA lists ~103–106k US vehicles; Copart holds **≈57%** of listed duopoly inventory on clean nights
(MEASURED, 3 clean nights so far). IAA throttles by download volume: the third sitemap was challenged on 11 of the
first 15 nights, and the stored share was **wrong (60–62%)** on those nights because it used a partial count. Fixed
2026-09-25: 90 s pauses between big files, `iaa_complete` / `copart_overlap_pct` / `usable` flags, share published
only when both sides are clean; history re-flagged (`findings.md` Addendum 17).

**Where it led.** The pitch's kill condition — share < 55% by mid-October — now measured only on `usable = 1` nights.

**Open.** Whether the pacing fix holds (first test is the 2026-09-25 run). Coverage of each sitemap versus each
firm's true inventory is unknown; the split is of *listings*.

### H. Operating leverage — the physical series

**Why.** Facility costs are Copart's largest cost line and are fixed-ish; the FY26 margin damage is unit deleverage.

**What we found.** US facility costs fell in dollars in FY26 (segment table, −$11.8M / −0.7%) yet rose +6.6% per unit;
consolidated facility operations were +0.6% on the 8-K's exclusive-of-D&A basis and +1.1% inclusive — an earlier
blueprint line that mixed those bases and showed −9.7% is corrected (Addendum 19); international grew costs 11.4%
and per-unit +1.2% because its units grew (VERIFIED, 8-K). **Cars per weekly sale event ~700 → 492**, with weekly US
sale events up while units fell (MEASURED from two scraped series; an earlier 745 peak **fails the overlap gate** and
is retracted in favour of ~700). Sale events have been stable at 620–630 across 223–225 US yards every night since
collection began.

**Where it led.** Thesis #2 (asymmetric leverage) and the Facility Cost Build tab.

### I. Capex and owner earnings

**What we found.** Land plus buildings were 64–99.9% of capex every year FY2016–FY2025; land at cost is absent from
XBRL and was parsed from the 10-K footnote (`scripts/ppe_land.py`). Maintenance capex sits below D&A, so reported FCF
understates owner earnings (MEASURED, multi-year only). **Both signs matter:** the best public bull argues current
FCF is *flattered* because post-COVID land spend has already slowed. Do not pitch "land capex is about to free up
cash."

### J. Competitive landscape, the field, and the theses

Detailed in the archived handoff §6, §8, §10. In brief: the best public bull published his model, which makes him a
nameable opponent for the RPU line; ten competing decks were reviewed and none printed an error bar, a graveyard,
or a downside price below spot — those are cheap differentiators. Theses ranked: (1) RPU fee-and-mix engine,
(2) asymmetric operating leverage, (3) the units decomposition with the calibrated TLF leg, (4) owner earnings as the
valuation frame, (5) reverse DCF as a physical claim. **ACV is genuinely ambiguous** — first ranked on novelty (wrong
reason), then called clearly bearish (too strong); the SC 14D-9 with management's projections would resolve it.

### K. Sources tried and dead — do not re-tread

Auction aggregators (0.47% coverage, pre-auction proxy bids, filters silently ignored); a 51-state auto-insurance
rate series (all BLS sub-national insurance CPI ends 2021; SERFF 403; Texas is the lone exception,
`tx_auto_rate_filings.csv`); per-lot detail beyond the slug (hydrates from a robots-disallowed path); Wayback copies of
sale-list pages (empty stubs); HLDI URLs (404 from here); NHTSA and spglobal.com (robots 403); AAMVA NMVTIS report
(robots-closed); web.archive.org unreachable from this network (an open lead from another network, not a dead end).
"Dead" here means "we did not find a way within the rules" — not that none exists.

---

## 4. What is built and where

| Artefact | Path | Status |
|---|---|---|
| The workbook to copy from — every dataset as a tab plus live formulas for the fleet roll, curves, Solver calibration, TLF drift, spread and RPU regressions, checks | `model/CPRT_Intermediate.xlsx` | rebuilt by `scripts/build_intermediate_xlsx.py`; verified by `scripts/verify_intermediate_xlsx.py` (pycel; RSQ/CORREL recomputed in Python) — all checks OK |
| Nightly collectors | `scripts/job1_snapshot.py`, `scripts/job1_iaa.py`, `scripts/run_job1.sh`, LaunchAgent `com.cprt.job1` | running; log `logs/job1_cron.log` |
| Provenance-logged fetcher | `scripts/prov.py` | every request in `data/cprt.db` `provenance` |
| Analyses that reproduce the pitch numbers | `scripts/analysis_20260911.py`, `units_decomp_panel.py`, `age_curves.py`, `backtest_inventory_v2.py` | re-runnable |
| Data | `data/csv/*.csv` (committed, indexed in `data/csv/README.md`); `data/cprt.db` (gitignored, 1.3M lot rows) | |
| Documents | `MODEL_BLUEPRINT.md`, `docs/AGE_CURVES.md`, `findings.md`, `PROVENANCE.md`, `ARCHITECTURE.md` | current |
| Archive | `docs/archive/` — earlier handoffs, the parallel session's brief, the first build spec, a retired dashboard; `model/legacy/` — the first worked tab | superseded, kept as record |

The workbook follows the formatting conventions of the Black Diamond SOLS model the user pointed at (Garamond,
gridlines off, navy section bars, A/E year headers, blue inputs, green links, pink key outputs, Cover with table of
contents). Formula cell addresses are stable; the verify script is the contract.

---

## 5. How the agent doing this work fails — observed, not hypothetical

Condensed from the archived handoff §2 plus this fortnight. Each is a real error from this project.

1. **Confident false negatives.** Copart "IP-blocked" (it was header fingerprinting; working code was on disk).
   The IAA and Copart WAFs declared "closed" during a burst that cleared hours later. An adversarial reviewer refuted a
   file that existed. *Countermeasure:* status codes and `ls` output before any claim of absence.
2. **Manufacturing structure from thin data.** The lot-ID clock, R² 0.94 on a staircase. *Countermeasure:* mechanism
   first, residual plot, units check.
3. **Convenient anchors from memory.** The 289M VIO figure; "Progressive insures an older fleet." *Countermeasure:*
   anything that helps the thesis needs a source on disk before it gets a sentence.
4. **Calibrating to the wrong target.** Survival fitted to S&P average age produced a fleet that cannot exist.
   *Countermeasure:* check a calibration against a second, independent statistic (here, counts).
5. **Fitting noise.** A free 0–6 slope in R returned +1.6%/yr that the data could not distinguish from flat.
   *Countermeasure:* when a parameter barely moves the loss, remove it.
6. **Silent truncation.** Summing ages to 31 while the curve ran to 39. *Countermeasure:* the workbook and the
   script must agree; the verify script exists for this.
7. **Alignment and basis errors.** The 0.465 elasticity; same-quarter alignment of a leading stock (the user caught
   it: "shouldn't the curves be a little to the left?").
8. **Aggregation on paginated sources.** Summing overlapping pages. Union, never sum.
9. **Destroying data defensively.** A same-day guard that deleted before writing; 2026-09-09 is lost.
10. **Sign-picking.** Arguing only the land-capex direction that helped. Compute both signs.
11. **"Lapping turns growth positive."** It does not; it takes the drag to zero.
12. **Reversing under pushback rather than evidence,** in both directions. Ask what changed.
13. **Licensed data leaking into the repo.** IHS tables were committed as CSV extracts until the source line was read.
    *Countermeasure:* read the footer of every table before committing an extract.
14. **Novelty mistaken for edge.** ACV ranked first because nobody had modelled it, before checking the direction.

**The meta-observation:** the user caught more substantive errors than the model did. Show reasoning, not
conclusions, and expect correction.

---

## 6. Open questions and uncertainties — stated plainly

- **289M light vehicles in operation (S&P 2025)** is recalled, not sourced. Experian's 292.1M is on disk and gives
  the same answer within 1%. Confirm or replace.
- **R(age) is fitted, not measured.** HLDI's insurance loss statistics by vehicle age would make it measured. We
  could not reach iihs.org from this environment; the user offered to pull manually.
- **P(age)'s interior — now MEASURED at bucket level.** CCC 2026 Figure 19 gives P for six age buckets, every year 2020–2025
  (`data/csv/ccc_tl_share_by_age_2020_2025.csv`, `reports/CCC_age_buckets_2026.md`); "45.3% at 13+" is CY2025 in it. The
  fitted single-year curve is still the interpolation between those buckets.
- **The survival drift path** 2013→2024 is linear by assumption; only its endpoints are anchored. Forward, k is held
  flat, which is a choice.
- **Experian's "12M fewer ≤6-year vehicles"** cannot be reproduced from sales; we suspect a definitional difference
  and have not confirmed it.
- **The 2019 repairable mix** misses by ~3pp with frozen curves; we attribute it to EV share and AEB penetration
  without proof.
- **The spread regression's intercept** (~0.6pp/yr) is not explained by the spread; demographics explain about a
  quarter of it; the remainder is attributed to technology and filing behaviour without a model.
- **Effective sample sizes** are small everywhere (≈6 for the RPU slope and the non-comp TLF variant). The
  confidence intervals are honest; the point estimates are not precise.
- **Listed inventory versus yard inventory** — coverage of the sitemap is unknown and may have changed with the
  shrink to three pages.
- **Competition dates and the two-page limit** are from an uncited brief.
- **ACV's SC 14D-9 is read** (`reports/E10_filings.md`, Addendum 22): projections verified, FCF-negative through 2029,
  a rival bid at $11–12 that withdrew. **The FY26 10-K is still not filed** (checked 2026-09-26).
- **The IAA pacing fix** worked on 2026-09-25 (all three sitemaps clean) but the Copart side was ungated that night, so no
  usable duopoly share yet.
- **Second-session experiments (2026-09-26):** scope in `reports/00_scoping_2026-09-26.md`; results so far in Addendum 22 and
  `reports/E1_step1_*.md`, `E4_*.md`, `E8_*.md`, `E10_*.md`, `CCC_age_buckets_2026.md`. E2, E3, E6 (human step) and E1 steps 3–6 are
  open.

---

## 7. Suggested next steps, in order of value per hour

1. Read the FY26 10-K the day it files; tie the FY26 base year in the workbook to it (`MODEL_BLUEPRINT.md` §7).
2. Confirm or replace the 289M anchor from S&P's release; re-run `age_curves.py` and rebuild the workbook (two
   commands; the verify script tells you if anything moved).
3. If the user pulls HLDI claim frequency by vehicle age, replace the fitted R slope with the measured curve on
   `Inputs` and re-run the out-of-sample checks on `TLF_Roll` — this is the single biggest upgrade to §3F.
4. Watch `duopoly_daily.usable` for a week; if sitemap3 keeps failing, try a second, later fetch of only the missing
   file rather than shorter pauses.
5. Re-pull ACVA's EDGAR submissions for the SC 14D-9; if management projections appear before Oct 2, ACV becomes
   quantifiable.
6. Build the user's model in this order: three statements and DCF on Street drivers first, then replace one driver
   row at a time with the Units, RPU and Facility builds, then plug in the engine tabs by Move or Copy.

---

## 8. Operational notes

```bash
cd /Users/kwu/cprt
./.venv/bin/python scripts/job1_snapshot.py            # Copart nightly snapshot (also run by LaunchAgent)
./.venv/bin/python scripts/job1_iaa.py                 # IAA nightly snapshot — ONCE per day; IAA throttles bursts
./.venv/bin/python scripts/analysis_20260911.py        # TLF calibration, elasticity, decomposition CSVs
./.venv/bin/python scripts/units_decomp_panel.py       # six-quarter units panel
./.venv/bin/python scripts/age_curves.py               # age curves: extract, calibrate, fit, validate
./.venv/bin/python scripts/build_intermediate_xlsx.py  # rebuild the workbook from data/csv
./.venv/bin/python scripts/verify_intermediate_xlsx.py # evaluate its key formulas (pycel); exit 1 on any mismatch
```

- Python is 3.9 in `.venv`; no numpy/scipy/LibreOffice on this machine. `pycel` is installed for verification.
  Excel recalculates the workbook on open.
- Copart's WAF is **intermittent**, not closed: `prov.get` retries with backoff; do not fight a burst and do not
  declare it closed. SEC and Copart need opposite headers (`prov.headers_for`).
- The nightly log is `logs/job1_cron.log`. `2026-09-09` is missing permanently; other gaps are the machine asleep.
- Rebuild the workbook after any CSV change; commit the CSV, the workbook and the verify output together.
- Keep `PROVENANCE.md` and `findings.md` current. When a judge asks "how do you know that," the answer cannot be
  "a model told me."
