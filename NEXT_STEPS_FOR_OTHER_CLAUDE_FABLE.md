# Next steps for another Claude Fable — the expensive experiments, specified

*Written 2026-09-25 by the Fable session that built this repository, for a second Fable session running with a fresh
usage budget. The owner will carry your reports back here. Read `HANDOFF.md` §0–§3 first (twenty minutes); it tells you
what exists, what was retracted, and how this project fails.*

---

## 0. The standard you are working to

*Owner's instruction 2026-09-26: the pitch is long OR short, decided by the analyses. Do not write toward a direction; report what each result implies for both.*

**The problem with the repository as it stands.** It forecasts Copart's KPIs through an identity — US insurance
units = industry claims × total-loss rate × Copart share; revenue per unit = f(realised price, fees) — and each term is
either measured or fitted on public history. That is honest, and it is not a pitch. A multi-manager pod has the same
CCC series, the same BLS series, the same transcripts, and thirty analysts. "Our regression is better than theirs" is
false and everyone in the room knows it. The owner's words: *"The total-loss frequency is a price ratio and the ratio
re-widened — that is an observation, not an explanation."*

**What counts as an explanation here.** A mechanism with (i) a named driver you can measure, (ii) a reason it moved
when it did, (iii) a reason it will move next, on a 3–12-month horizon, and (iv) a consequence for a Copart KPI that the
consensus model does not contain. The test: could a judge accept every number and still keep their prior causal story?
If yes, it is an observation.

**Every fitted number must be decomposed into drivers.** The repository's fitted constants are: the total-loss-rate
regression's intercept (~0.6pp/yr, unexplained), Copart's price-over-used-car-CPI intercept (~3.3pp/yr, ~1pp now
explained by vehicle vintage), the fee-and-mix intercept in revenue per unit (~4pp/yr, unexplained), and the two age
curves R(age), P(age) (fitted, not measured). Each experiment below attacks one of these.

**Rules that do not bend** (the owner's; a judge may ask about them):
- `robots.txt` first on every host, obeyed literally. Use `scripts/prov.py` for every request so it is logged with its
  robots status; ≥2 s between requests to a host; no concurrency against one host.
- No authentication, no paywall or CAPTCHA circumvention, no proxies. A challenge page is a stop.
- Identify honestly. BLS and SEC require a descriptive User-Agent with a contact email (`prov.get(..., ua=...)`);
  Copart and IAA refuse descriptive UAs and want a browser set. `prov.headers_for(url)` picks per host.
- Do not buy data, contact a vendor, or submit a form without the owner's explicit approval. Say so in the report.
- Licensed content (`raw/transcripts/`, `raw/sellside/`, `raw/reference/`, the IHS-sourced ORNL tables) is read locally
  and never committed or quoted at length.
- **Report blockers rather than working around them.** Three separate agents on this project declared things
  unavailable that were on disk, and declared hosts "closed" during a temporary burst. Paste the status code.

**How to hand results back.** For each experiment, one markdown report at `reports/<experiment-id>.md` with: what was
done (exact URLs, dates, request counts), what data was produced (CSV in `data/csv/` with a `#` provenance header, indexed
in `data/csv/README.md`), the result with its uncertainty, what would change the conclusion, and the usage actually
spent. New code goes under `scripts/experiments/`; do not modify existing analysis scripts or the collectors. If you touch
the workbook, run `scripts/verify_intermediate_xlsx.py` and report its output. Label every number MEASURED / FITTED /
ASSUMED / UNVERIFIED. Prefer "we did not find" to "does not exist."

**Before spending anything, check in with the owner** with the end-to-end steps, why each step, the cost estimate, and
the cheaper alternatives. The owner approves scope; a material expansion needs another check-in. Cost figures below are
rough ranges in tokens of your own usage (input + output, including the reading you will do); they are estimates, not
quotes.

---

## 1. The experiments, in the order I would run them

Ordering criteria: explanatory power for a KPI on the pitch horizon, then cheapness, then whether the data is
reachable within the rules. E4 and E2 have cheap first steps on data already in `data/csv/`; run those before anything
that fetches.

### E1 — The truck cohort wave: does body type change the totaling decision, and by how much?

**Goal.** Replace the single fitted P(age) with body-specific curves P_car(age), P_truck(age), and quantify what the
light-truck share of the total-loss pool rising from 57% (2024) to 62% (2027) does to (a) total-loss frequency and
(b) Copart's realised price.

**The explanation being tested.** Light trucks were half of new sales for the 2010–2013 model years and 83% in 2025.
Those cohorts reach the 7–12-year totaling ages from now through 2030 (`docs/AGE_CURVES.md`, `findings.md` Addendum 20).
Trucks differ from cars in every input to the totaling decision: higher value at the same age (pushes *against*
totaling), higher repair cost per claim — aluminium bodies (F-150 from MY2015), larger panels, more ADAS sensors
(pushes *for*), and higher salvage recovery, partly from export demand for pickups (pushes *for*, and lifts price). The
net sign for the total-loss rate is genuinely unknown; the sign for realised price is positive. If trucks total at a
higher rate than cars at the same age, the cohort wave is a supply driver nobody in the consensus models, with a
known schedule. If they total at a lower rate, the repository's demographic result is overstated and we need to know.

**Why it matters for the pitch.** It is the one demographic driver with a calendar: sales mix by model year is public
history, so the wave's timing is not a forecast. It ties supply (units) and price (ASP) to one cause.

**What exists.** Fleet roll by body (`scripts/age_curves.py` computes cars and light trucks separately; combined for the
fit). Light-truck share of sales, fleet and modelled total losses by year. Copart listed-inventory make/model slugs in
`data/cprt.db` (`lot_snapshots`, 1.3M rows) — body type can be inferred from make/model for the listed pool.

**Steps.**
1. *Body-level claim severity and frequency.* HLDI (the Highway Loss Data Institute, iihs.org/hldi) publishes insurance
   loss results by vehicle class — collision claim frequency, claim severity, overall losses — for large pickups,
   midsize SUVs, small cars, etc. Our earlier URL guesses returned 404; find the current index page (check
   `iihs.org/robots.txt` first) and pull the class-level tables for the latest three model-year groups. *Why:* claim
   severity by class is the numerator of the totaling ratio by body.
2. *Body-level value by age.* A public retained-value or depreciation table by segment (Cox Automotive, Edmunds,
   iSeeCars publish these as articles; check robots). *Why:* the denominator of the ratio by body.
3. *Body-level total-loss share, if published anywhere.* CCC Crash Course pages (on disk in the scratch of the earlier
   session; re-fetch the report pages — cccis.com robots allows) and Mitchell's quarterly *Industry Trends* reports
   sometimes split total-loss share or repair cost by vehicle type. *Why:* a direct measurement beats a derived one.
4. *Derive P_body(age).* With severity/value by body from 1–2, compute the share of claims whose repair cost exceeds the
   totaling threshold by age and body under the CCC repair-cost distribution (TCOR ≤6 yrs $5,721; 7+ $3,682), and
   re-fit the age-curve model with two P curves against the same eight CCC 2024 statistics (`scripts/age_curves.py`
   is the template; add a body dimension). *Why:* this is the quantitative core.
5. *Translate to KPIs.* Run the roll to 2030 with body-specific P; report the change in baseline total-loss frequency
   per year attributable to body mix, and the realised-price mix effect given a truck-vs-car salvage value ratio
   (E8). *Why:* the pitch needs pp of TLF and pp of ASP, not a curve.
6. *Cross-check against Copart's own listings.* From `lot_snapshots`, classify listed lots by body from the make/model
   slug and compute the truck share of the listed salvage pool by month, 2022–2026. If the modelled truck share of
   total losses (57% in 2024) is far from the listed share, one of the two is wrong. *Why:* a free reality check on
   the roll.

**Cost.** 150–300k tokens; 40–120 HTTP requests; 4–8 hours of your time. No paid data unless the depreciation table
turns out paywalled, in which case stop and report.

**Cheaper or more precise alternatives.** Step 6 alone (listed truck share by month) is ~20k tokens on data on disk and
would confirm or refute the roll's body split before any fetching. If HLDI's class tables are not reachable, Copart's
listed make/model mix by age is a partial substitute for the frequency side only. Do not scrape Copart lot pages for
values — robots-disallowed hydration path; a human reading a handful of public pages is not automated access, and the
owner can do that (E8).

**Kill criteria.** If P_truck(age) ≈ P_car(age) within the fit's tolerance, body mix is a price story only; drop the
supply half. If the listed truck share diverges from the roll by more than 10 points, stop and reconcile the roll first.

**Deliverable.** `reports/E1_truck_cohort.md`; `data/csv/hldi_class_losses.csv`, `data/csv/value_by_age_body.csv`,
`data/csv/age_curves_by_body.csv`; a table of ΔTLF and ΔASP by year 2025–2030 attributable to body mix.

### E2 — Insurance affordability → coverage and filing → the claims term

**Goal.** Explain the industry claims term (−7.7% in 2025; −3 to −5% in 2026) with a driver that has a lag structure,
and forecast it: the auto-insurance price cycle.

**The explanation being tested.** Motor-vehicle insurance CPI rose 22.6% year over year at its April 2024 peak and is
now falling (−4.5%). Households responded with higher deductibles ($1,000+ share up 6 points in two years, CCC),
coverage downgrades to liability-only, and non-renewal (JD Power: 5.7% of vehicle households uninsured). Each response
removes filed first-party claims from the system with a lag of one policy cycle (6–12 months). So the 2024–25 claims
decline is the affordability shock working through, and falling premiums in 2026 should reverse it with the same lag.
This is a *reason* the claims term recovers, with a date, not an assumption that it does.

**Why it matters.** The claims term is the largest swing factor in FY27 units and currently a hand input in the model.
A forecastable driver with a lag is exactly what the identity lacks.

**What exists.** Insurance CPI monthly (`data/csv/cprt_cpi_three_series.csv`, SETE), Fast Track collision-claim
headlines (`fasttrack_collision_claims_cw.csv`), CCC deductible statements (quoted in `HANDOFF.md`, Addendum 15),
Progressive policies in force monthly (`pgr_monthly_pif.csv`), GEICO frequency sentences.

**Steps.**
1. *Cheap first (data on disk, ~20k tokens):* regress Fast Track collision-claim growth on insurance-CPI growth lagged
   0–8 quarters; report the lag profile. *Why:* if there is no lag structure the mechanism is not there.
2. *Coverage penetration.* Pull Insurance Information Institute / Triple-I public pages on the share of insured
   drivers carrying collision and comprehensive, and the Insurance Research Council uninsured-motorist rate by year
   (check robots). *Why:* the coverage channel needs a level series.
3. *Deductible mix.* CCC report pages give the $1,000+ share; J.D. Power's Auto Claims Satisfaction press release gives
   the 26% figure. Assemble the time series that exists (likely 4–6 annual points). *Why:* the filing channel.
4. *A filing-propensity model.* Filed collision claims = accidents (proxy: VMT × frequency trend) × insured share ×
   filing rate; fit the two behavioural terms to insurance CPI with the lag from step 1; forecast the claims term for
   FY27 quarters from the insurance CPI path already in the data. *Why:* turns the mechanism into a number the model
   can use.
5. *Cross-check* against Progressive PIF growth (policies rising while claims fall = coverage downgrade, not fewer
   drivers).

**Cost.** 80–150k tokens; 20–40 requests. **Alternatives.** If the coverage series is unreachable, run step 1 and 4 with
the deductible share alone and state the missing channel. **Kill.** No lag structure in step 1, or a filing elasticity
with the wrong sign. **Deliverable.** `reports/E2_affordability_claims.md`; `data/csv/claims_term_drivers.csv`; a
forecast row for the claims term by fiscal quarter with the lag stated.

### E3 — Collision-repair labour scarcity → repair CPI → the spread's repair side

**Goal.** Decompose repair-cost inflation, the numerator of the totaling spread, into wages, parts and ADAS content, and
forecast it from labour-market series rather than extrapolating the CPI.

**The explanation being tested.** Repair CPI sits at an all-time high (+6.6% YoY) while used-car values are flat to
down. The consensus treats repair inflation as post-COVID residue that fades. The alternative: the collision repair
labour market is structurally short of technicians (an ageing workforce, few entrants), and the vehicles arriving at
shops need more calibrated labour (ADAS sensors standard from ~MY2018, now aged 7–8 and entering the modal repair
population). If so, the spread stays wide even after used-car prices normalise, and the total-loss rate keeps
rising for a labour-market reason that is measurable and slow-moving.

**What exists.** Repair CPI monthly (SETD, on disk); CCC statements on labour hours and parts per claim (scratch copies
of the report pages; re-fetch); the fleet roll gives the share of the claim pool by model year, hence ADAS-era share.

**Steps.**
1. Fetch BLS Current Employment Statistics for NAICS 8111 (automotive repair and maintenance): employment and average
   hourly earnings, monthly, from `download.bls.gov/pub/time.series/ce/` (allowed; descriptive UA). Fetch Occupational
   Employment and Wage Statistics for SOC 49-3021 (automotive body and related repairers): employment and wages,
   annual. *Why:* the labour driver, measured.
2. Fetch JOLTS if the sector is available at that granularity (likely not; report). *Why:* vacancies would sharpen it.
3. Build the ADAS-content series: share of the modelled claim pool with model year ≥ 2018, by year, from the fleet roll.
   *Why:* the complexity driver, from data we already have.
4. Regress repair CPI YoY on body-shop wage growth, parts PPI (BLS PPI for motor vehicle parts, `pc` files) and the
   ADAS share; forecast 2026–27 repair CPI from the wage trend and the known ADAS path; feed the spread. *Why:* the
   spread's repair side becomes a driver model.
5. Sanity check against CCC's published labour-rate and hours-per-claim statements.

**Cost.** 100–200k tokens; 10–20 large file fetches. **Alternatives.** Steps 1, 3, 4 alone give most of the value; skip
JOLTS. **Kill.** Wage growth explains none of repair CPI beyond parts, or the ADAS share has the wrong sign.
**Deliverable.** `reports/E3_repair_labour.md`; `data/csv/bls_ces_8111.csv`, `data/csv/repair_cpi_drivers.csv`.

### E4 — New-vehicle supply and the off-lease cliff → used-car values → the spread's value side

**Goal.** Forecast used-car CPI, the denominator of the totaling spread, from supply that is already known: new-vehicle
sales three years earlier (lease returns) and new-vehicle prices.

**The explanation being tested.** Used-car values are set largely by the supply of 2–4-year-old vehicles, which is
determined by new sales and lease penetration three years earlier. New sales collapsed in 2020–2022 (14.1–15.4M vs 17M+)
and lease penetration fell with them, so 2023–2025 saw a shortage of 3-year-old cars that supported used values;
2023–2025 sales recovered to 15.6–16.5M, so 2026–2028 off-lease supply rises and used values should soften, widening the
spread from the value side. This is a driver with a three-year lead that a pod knows about in general terms; the
contribution here is putting it on the totaling spread with a number.

**What exists.** New light-vehicle sales by calendar year 1976–2026 (FRED, on disk), used-car CPI monthly 1953–2026 (on
disk), new-vehicle CPI (fetched 2026-09-25, `raw/bls/`).

**Steps.**
1. *Cheap first (~30k tokens, data on disk):* regress used-car CPI YoY on new-sales YoY lagged 30–42 months and on
   new-vehicle CPI YoY; report the lag profile and fit. *Why:* if the lag is there, the rest is worth doing.
2. Add lease penetration if a public series exists (Experian Automotive Finance press releases give quarterly lease
   share; check robots). *Why:* off-lease supply is leases × sales, not sales alone.
3. Forecast used-car CPI 2026–2028 from known sales and the lease share; run it through the spread regression to get
   the value-side contribution to ΔTLF by quarter. *Why:* closes the loop to the KPI.

**Cost.** 30–80k tokens. **Kill.** No lag structure at 30–42 months. **Deliverable.** `reports/E4_offlease_values.md`;
`data/csv/used_car_cpi_drivers.csv`; a forecast row for used-car CPI by quarter with the lag stated.

### E5 — Title processing speed → inventory velocity → why listed inventory falls faster than units

**Goal.** Test whether the decline in Copart's listed inventory (−6% YoY on gated nights) is partly faster turnover from
electronic titling rather than fewer cars, which would change how the sitemap series and facility cost per unit are
read.

**The explanation being tested.** A salvage vehicle sits in a yard until the title is processed; state DMVs are
moving to electronic salvage titles, cutting days-to-title. Faster titles mean lower inventory at the same throughput,
lower storage days, and more sale events per car — which is what the scrape shows (events up, lots per event down).
Management has cited cycle-time improvement. If true, inventory is a velocity KPI, not a volume KPI, and the "lots per
event" decline is partly good news.

**What exists.** Listed lots by state by month 2022–2026 (`data/csv/state_panel.csv`), sale events by yard nightly,
management cycle-time remarks in transcripts (local).

**Steps.**
1. Screen: which states' listed inventory fell most relative to the national series, 2023–2026? (~20k tokens, on disk.)
2. Find state e-title / electronic salvage title adoption dates from state DMV pages or AAMVA public news (AAMVA's
   NMVTIS report is robots-closed — do not request it; DMV pages vary, check each robots file). *Why:* the treatment
   dates.
3. Difference-in-differences: inventory change in early-adopting states vs others around adoption, controlling for
   each state's share of national claims (proxy: registrations). *Why:* the causal test.
4. If it holds, re-express the sitemap inventory series as volume × days-on-site and re-read the facility-cost-per-unit
   argument.

**Cost.** 100–200k tokens; 20–60 requests to state sites. **Alternatives.** Steps 1 and 4 with management's cycle-time
statements as the only "treatment" evidence is a weaker but cheap version. **Kill.** No cross-state dispersion in step 1.
**Deliverable.** `reports/E5_title_velocity.md`; `data/csv/state_inventory_vs_etitle.csv`.

### E6 — The fee grid and fee-schedule history → the revenue-per-unit intercept

**Goal.** Replace the fitted +4pp fee-and-mix intercept with dated fee increases and the convexity of Copart's buyer-fee
schedule.

**The explanation being tested.** Copart's buyer fees are a schedule of fixed dollars by price band plus percentage
tiers, gate fees, environmental and virtual-bid fees. Fixed dollars dominate at low prices, so revenue per unit
mechanically moves about half as much as price (the measured 0.51), and every dated schedule increase is a step in the
intercept. If the +4pp is mostly dated fee increases, it is a pricing-power fact with a history and a cadence, not a
regression constant.

**What exists.** `MODEL_BLUEPRINT.md` §3C (the mechanism); earlier fee figures in old prompt files are **unsourced —
do not use**. Copart's fee pages are robots-disallowed to crawlers.

**Steps.**
1. **A human reads the fee pages** (Copart member fee schedule, IAA buyer fees) and screenshots them; a human reading a
   public page is not automated access. Transcribe the current grid. *Why:* the only compliant route.
2. History: the Wayback Machine was unreachable from the original network; from yours, try `web.archive.org` for the
   fee page at yearly intervals 2019–2026 (robots allows). Transcribe changes and dates. *Why:* the dated steps.
3. Simulate: apply each year's grid to the ASP distribution (lognormal, median ~$5k, shifted by the year's ASP) and
   compute implied service revenue per unit; compare the simulated year-over-year changes with the measured intercept.
4. Cross-check with third-party fee calculators and the Substack's fee discussion (local file).

**Cost.** 1–2 hours of human reading; 40–80k tokens. **Kill.** Simulated fee steps explain less than a third of the
intercept — then mix (services, transport) is the story and needs the FY26 10-K's revenue disaggregation.
**Deliverable.** `reports/E6_fee_grid.md`; `data/csv/copart_fee_grid_by_year.csv` (transcribed, with capture dates).

### E7 — Export demand and the dollar → the unexplained price residual

**Goal.** Test the external note's hypothesis that overseas buyers drive Copart's realised price above domestic values.

**The explanation being tested.** A weaker dollar and rising demand in destination markets (Mexico, Nigeria, UAE,
Central America) raise what foreign buyers can bid for US salvage, lifting Copart's price without any change in
domestic used-car values. The residual in `ASP_Drivers` (about 2.2pp/yr after CPI pass-through and vintage, and it
co-moves with CPI) is where this would live.

**Steps.**
1. FRED trade-weighted dollar index (allowed host): regress the ASP residual on it, contemporaneous and lagged one
   quarter (~20k tokens).
2. US Census used-vehicle exports (HS 8703 used, by destination, monthly) via the USA Trade Online / Census API —
   check robots and terms; if gated, stop. Regress the residual on export volumes and values.
3. Copart's own statements: 10-K language on international buyers' share of units (read locally from filings on disk
   in `raw/sec/`).

**Cost.** 40–100k tokens. **Kill.** No relationship with the dollar or exports on 14–17 quarters — then report it as a
negative and stop. **Deliverable.** `reports/E7_export_fx.md`; `data/csv/asp_residual_drivers.csv`.

### E8 — Truck-versus-car salvage value ratio (prerequisite for E1's price half; small)

**Goal.** One number: the ratio of salvage value for a light truck to a car at the same age and damage class.

**Steps.** A human reads a public source of sale results by vehicle type (e.g. a public auction-results summary, a KBB
or Edmunds article on retained value by segment) and records the ratio with its URL and date. Enter it in
`model/CPRT_Intermediate.xlsx` on `ASP_Drivers!B4`; the body-mix column then fills. **Cost.** Minutes for a human; ~5k
tokens to wire and document. **Deliverable.** the number, its source, in `reports/E8_body_value_ratio.md`.

### E9 — Progressive's IAA volume and local congestion (only if paid alternative data exists)

**Goal.** Test whether Progressive's move to IAA (April–July 2026) degraded IAA service at specific yards and pushed other
carriers toward Copart.

**Status.** The external note (owner's `~/Documents/ChatGPT/HFAC x Citadel/research/cprt_feasibility_2026-09-25/`)
concluded, and we confirmed (`findings.md` Addendum 18), that this cannot be tested from public sitemaps: IAA vehicle
entries carry no branch. It needs carrier-by-yard volumes and cycle times, which exist only in autoAstat/Yipit-type
data. **Do not** build anything here unless the owner has that access. If they do: yard × carrier × week panel;
exposed yards (large Progressive inflow) vs comparison yards; other-carrier cycle time and later allocation changes;
pre-trends and placebo periods. Cost unknown until the data is seen.

### E10 — Two documents to read the day they exist (cheap; do first if filed)

- **ACV's SC 14D-9** (reportedly filed 2026-09-17): management's standalone projections (2027 adjusted EBITDA $123M, EBIT
  after stock comp $20M, unlevered FCF −$97M are UNVERIFIED second-hand figures). One EDGAR fetch (`data.sec.gov`,
  descriptive UA). Report the projections, the fairness-opinion assumptions, and any staging/yard-usage language that
  would connect ACV volume to Copart's facility cost per unit. ~30k tokens.
- **Copart's FY26 10-K** (expected late September–early October 2026): tie the workbook's FY26 base year to it
  (`MODEL_BLUEPRINT.md` §7), and read the revenue disaggregation and cost notes for E6. ~40k tokens.

---

## 2. What not to do

- Do not re-derive the units identity, the spread regression, the elasticity or the age curves; they are built and
  documented. Extend them.
- Do not touch `scripts/job1_snapshot.py`, `scripts/job1_iaa.py` or the LaunchAgent; the collectors run nightly on the
  owner's machine.
- Do not fetch Copart pages beyond the sitemaps the collector already reads; lot pages hydrate from a robots-disallowed
  path.
- Do not treat a challenge page, a 403 burst or a missing file as proof of anything. Paste the evidence.
- Do not present a fitted coefficient as a finding. Present the driver behind it or say it is unexplained.

## 3. Where the existing pieces are

| Need | File |
|---|---|
| project state by research thread | `HANDOFF.md` |
| model architecture, mechanisms A–E, build order | `MODEL_BLUEPRINT.md` |
| age curves: method, evidence, validation | `docs/AGE_CURVES.md` |
| the workbook (every dataset + live formulas) | `model/CPRT_Intermediate.xlsx`, rebuilt by `scripts/build_intermediate_xlsx.py`, verified by `scripts/verify_intermediate_xlsx.py` |
| the walk-through page with charts | `docs/walkthrough.html` (`scripts/build_walkthrough_page.py`) |
| every result and retraction, chronological | `findings.md` (Addenda 14–21 are this month) |
| every host, robots status, what was saved | `PROVENANCE.md` |
| every script / dataset, with status | `scripts/README.md`, `data/csv/README.md` |
| the fetcher you must use | `scripts/prov.py` (`prov.get(url, robots_status, basis, note=, save_to=, ua=)`) |
