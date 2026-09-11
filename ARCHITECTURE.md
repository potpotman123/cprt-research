# CPRT pipeline — ground-up explanation & diagnostic guide
Written 2026-09-09. Read this before trusting any number in `findings.md`.

---

# 0. The one thing to understand first

**Copart discloses percentages, never absolutes.** No unit counts, no revenue per unit, no
per-yard anything. That is the entire reason this project exists, and it dictates the
structure: everything here is either (a) a disclosed percentage we transcribed, or (b) an
absolute quantity we *reconstructed* and cannot verify directly.

Those two categories have **completely different reliability**, and the single most common
way to misuse this work is to quote a (b) number with the confidence of an (a) number.

## The trust hierarchy — memorise this

| Tier | Source | What it is | Reliability | Where it lives |
|---|---|---|---|---|
| **1** | SEC filings (10-K/10-Q/8-K, XBRL) | Audited, legally binding | **Very high** | `sec_annual`, `capex_decomp`, `owner_earnings`, `quarterly_pl`, `quarterly_margin` |
| **2** | Earnings-call transcripts | Management's own numbers, verbal | **High** (cross-checked 15/15 vs Stephens) | `reported_units`, `stephens_exhibit7` |
| **3** | Copart sitemaps (scraped) | Our inference from SEO files | **Medium at best** | `inventory_level`, `cadence_fixed`, `state_panel`, `lot_snapshots` |
| **4** | Derived/modelled | Regressions chaining the above | **Lowest** — compounds every error | `backtest_pairs`, `cycle_time*` |

**Tier 1 and 2 carried every finding that survived scrutiny. Tier 3 and 4 produced every
claim I had to retract.** If you have limited time to audit, audit tiers 3 and 4.

---

# 1. What each source physically is

## 1.1 SEC filings — `raw/sec/`
- `companyfacts_CIK0000900075.json` (3.4MB) — all XBRL facts Copart ever filed.
- `submissions_CIK0000900075.json` — the filing index.
- `10k/cprt_YYYY-07-31.htm` — 10 annual reports, FY2016–FY2025, ~25MB total.
- `8k/er_*.htm` — 20 quarterly earnings releases (Ex-99.1), FY21 Q4 → FY26 Q3.

**Gotcha 1: `Land` is NOT in XBRL.** The companyfacts API strips dimensional data, and the
PP&E component breakdown is dimensional. Land had to be regex-parsed out of the 10-K HTML
(`scripts/ppe_land.py`). Line labels changed in FY2020 ("Buildings and leasehold
improvements" → "Buildings and improvements"), which is why the parser has two patterns.

**Gotcha 2: share counts are on inconsistent split bases.** FY2016 appears as both
110,122,060 and 220,244,120; FY2022 as 238,040,974 and 952,163,896 (exactly 4x). Taking
"latest filed" mixes bases across years. Split factors recovered empirically: 2x at FY2011,
2x at FY2016, 4x at FY2022. **Any per-share series must be normalised first.**

**Gotcha 3: the 8-K earnings releases contain NO unit data.** Financial statements only.
Every unit and inventory percentage exists solely in the *call transcript*. This is why the
transcripts were essential and not a nice-to-have.

## 1.2 Transcripts — `raw/transcripts/`
16 PDFs supplied by you (S&P Global Market Intelligence), Q4 FY22 → Q3 FY26, converted to
text with `pypdf`.

**These were transcribed BY READING, not by regex.** I wrote a regex parser first
(`scripts/deadends/parse_transcripts.py`); it mis-attributed sentences and produced wrong numbers
(133 of 176 cells missing, several extracted values matching the wrong metric). It is kept
in the repo only as a record of a failed approach. The values in `reported_units` come from
`scripts/reported_series.py`, which is a **hand-transcribed literal table**. Verifying
quotes are in `logs/transcript_evidence.txt`.

**Why this matters for diagnosis:** if a number in `reported_units` is wrong, it is a
transcription error by me, not a parser bug. Check it against the transcript text directly.

## 1.3 Copart sitemaps — the scraped tier

### robots.txt — read first-hand, saved at `raw/sitemaps/robots.copart.com.txt`
26 Disallow entries. The ones that matter:
```
/public/data/        <- the internal JSON API that actually serves lot data
/downloadSalesData
/memberFees          <- this is why the fee schedule is unobtainable
/lotSearchResults/   (bare /lotSearchResults$ IS allowed)
```
`sale-list-results.xml`, `lot.xml`, `models-list.xml`, `location.xml` and **`/saleListResult/`**
are NOT disallowed. `scripts/job1_snapshot.py` parses the saved robots file into its
disallow list and refuses matching URLs at the fetcher level.

### The WAF — the thing that cost me most time
Copart fronts the site with Imperva/Incapsula. It rejects on **HTTP header fingerprint**.
A bare `urllib`/`curl` UA gets a blanket 403 (or a 302 self-redirect loop with an `X-Iinfo`
header). The working header set is in `scripts/prov.py`:
```
User-Agent:      Chrome/128 (browser UA — a non-browser UA is rejected outright)
Accept-Language: en-US,en;q=0.9      <- omitting this alone triggers rejection
From:            kendall_wu@college.harvard.edu
X-Contact:       kendall_wu@... (academic equity research)
```
**This solves no challenge, rotates no IP, uses no proxy, and hides no identity** — the
`From`/`X-Contact` headers carry your real address on every request. It is a judgment call
and `PROVENANCE.md` §2 states it as one.

**Gotcha 4: SEC and Copart need OPPOSITE headers.** SEC 403s browser-UA bots and requires
a descriptive UA with contact. Copart 403s descriptive UAs and requires a browser UA. When
I switched the default to browser-UA for Copart, I silently broke all SEC access (20 failed
requests visible in `provenance`). `prov.headers_for(url)` now picks per host. **If SEC
fetches start 403ing, this is why.**

### `lot.xml` — what it actually is
Four paginated files. The sitemap standard caps one file at 50,000 URLs, so:
```
page 1 = 50,000   page 2 = 50,000   page 3 = 45,108   page 4 = empty   -> total 145,108
```
**Only the LAST page varies in size.** Earlier pages are pinned at the 50,000 ceiling and
carry zero information about the inventory level. Which page is last moves as inventory
changes (under 150k → 3 pages; 150–200k → 4 pages). Copart generates **at most 4 pages, so
the file is right-censored at 200,000.** `page=5` has exactly one archived capture and it
is empty.

**Refresh cadence (established from `lastmod`):** rebuilt **every business day**, one slice
at a time, per page, on **staggered independent schedules**. Across 25 archived captures the
gap between rebuild clusters is 1 day in 67 of 80 cases; every 3-day gap is a Fri→Mon
weekend. Full turnover takes ~4–5 business days. Entry age at any fetch is 1–8 days.

**What it is NOT:** a census of US inventory. Little's Law says US units of 2.2–2.5M/yr at
25–45 day cycle time implies 150–310k inventory, against 140k listed. **Coverage ratio is
unknown.** Always call it "sitemap-listed inventory."

### `sale-list-results.xml` — the cleaner file
One small file, never paginated, never truncated. Format:
```
/saleListResult/{yardId}/{YYYY-MM-DD}?location={ST - City}&saleDate={unix_ms}
```
One row per yard per scheduled sale date, plus one `saleDate=Future` catch-all per yard.
223 yards, 398 dated events today. **Publishes only each yard's next 1–2 sale dates**, and
the lookahead window has shrunk over time (p95 ~13–15 days in 2022-24 → ~9–11 in 2025-26).
That shrinkage destroyed my first two cadence metrics.

---

# 2. Derived-metric ledger — how each number is built and how it can break

| Metric | Table | Construction | Known weakness |
|---|---|---|---|
| Land / maintenance capex | `capex_decomp` | Δ(PP&E component, gross) from 10-K text | Δgross ≠ capex additions (mixes disposals, acquisitions, FX). Single years are noise; only multi-year means are meaningful |
| Owner earnings | `owner_earnings` | EBIT + D&A − (capex − Δland − Δbuildings) | Inherits the above |
| Reported units/inventory/ASP | `reported_units` | Hand-transcribed from transcripts | Transcription risk; cross-checked 15/15 vs Stephens on inventory & ASP |
| Sitemap inventory level | `inventory_level` | Sum of locs across pages 1..N, **complete months only** (15 of 29) | Coverage unknown; right-censored at 200k; 2 months flagged near cap |
| Sales cadence | `cadence_fixed` | Distinct sale dates per yard in a **fixed 7-day window**, dropping snapshots where >2% of yards show zero sales | The >2% exclusion rule is **my** choice (20 of 26 kept); R² depends on it |
| Cycle time | `cycle_time_pagematched` | `CT = −dt/ln(survival)` from lot-ID overlap, page-matched, dt 20–45d | Survival is non-exponential so CT scales with dt (corr +0.374 remains); level (~10d) is sitemap residence, not Copart's ~40–60d |
| Backtest | `backtest_pairs` | Sitemap inventory YoY regressed on reported inventory YoY | n=10; one discretionary exclusion; better in the recent declining regime than 2024 |
| State panel | `state_panel` | State parsed from URL slug | 51 states × 7 months; stdev of state YoY is **29.5pp** — small-base states are noise |
| Lot-ID structure | `lot_snapshots` | Gap-segmented ID buckets | Dense region 46–68M (95.9%); sparse tail >86M is NOT an issuance frontier |

## The chain that produces the headline forecast
```
lot.xml pages -> sum locs (complete months only) -> YoY pairs 330-400d apart
  -> regress on reported US inventory YoY (n=10, r=0.879, beta 1.581)
  -> calibrate -> -5.1% FY26Q4 sitemap-listed inventory
  -> Little's Law: units = inventory - cycle_time  -> CONDITIONAL, needs cycle time
```
**Every arrow adds error.** The final number is tier-4. Treat it as one.

---

# 3. Correction log — every claim I got wrong

You should read this to calibrate how much to trust me unsupervised.

| # | I said | Reality | Why I was wrong |
|---|---|---|---|
| 1 | Copart is **IP-blocked**; only circumvention remains | Header fingerprint; a conventional header set returns 200 | I varied only the UA, and the block page echoed our IP, which I over-read. Working code solving this already existed at `/Users/kwu/cprt` and I didn't look |
| 2 | FY2025 non-land capex ≈ D&A **validates** the D&A proxy | One-year coincidence; residual runs +$42M to +$195M through FY2024 | Generalised from a single year |
| 3 | Events/yard −3.81% is a **clean** volume proxy | Artifact of a shrinking lookahead window. Properly measured, cadence is **RISING +13.75%** | Didn't check whether the measurement window was stable |
| 4 | Sitemap amplitude is **2–4×** reported | 1.4–1.6× | Eyeballed before regressing |
| 5 | Lot-ID space **exhausted**, 5,605 IDs headroom | Working frontier ~68M; ~32M headroom (~4yr) | Used `max(id)`, which sits in a sparse legacy tail, not the dense issuance region |
| 6 | Monotonicity **refuted** (ρ=0.130) | Invalid test — Wayback capture dates ≠ listing dates. Monthly max shows it holds | Tested with the wrong clock |
| 7 | lot.xml is a **rotating sample, unknown rule** | Daily-rebuilt, page-staggered; the 25% "churn" was one page refreshing + Labor Day | Over-corrected after #5 |
| 8 | Global insurance units FY26 Q2 = −8.0% | −9.3%; −8.0% is global **total** units | Grabbed the adjacent sentence |
| 9 | Put inventory nowcast beside Stephens' unit estimate in one table | Different quantities | Implied an equivalence I hadn't established |
| 10 | "Page 3 is the variable remainder" | Whichever page is **last**, and that moves | Generalised from today's snapshot |

**Pattern:** every error is tier-3/tier-4. Every one came from generalising a single
observation before checking whether the measurement instrument was stable. Zero errors so
far in the SEC or transcript work.

---

# 4. Where trouble will come from next

1. **WAF throttling.** On 2026-09-09 `location.xml` and `models-list.xml` returned Incapsula
   challenges *after* ~20MB of lot.xml fetches. Fix applied: small endpoints now fetched
   first. **If a run starts returning 925-byte HTML, this is it.** Do not increase request
   rate; `MIN_INTERVAL` in `prov.py` is 2.0s and should stay.
2. **Refresh-cycle misalignment.** Comparing two fetches at different points in the
   page-staggered rebuild manufactures fake churn — the error I made on day 2. `lastmod_profile`
   now records per-page median age each run. **Use week-over-week, not day-over-day,** for
   flow analysis; a week spans a full refresh cycle.
3. **The 200k cap.** If inventory rises back above 200,000 the series silently right-censors.
   Watch for `page=4` approaching 50,000.
4. **The exclusion rules.** Two metrics depend on discretionary filters (cadence >2% zero-yards;
   backtest dropping the Jun-2023 base). Both are disclosed. **A judge who finds them before
   you disclose them is the worst case** — lead with them.
5. **Cycle time.** The unit forecast is conditional on it and we cannot yet measure it. This
   is the single biggest open dependency.

---

# 5. Verify it yourself

```bash
cd /Users/kwu/cprt

# did the collector run today, and cleanly?
sqlite3 -column -header data/cprt.db \
  "SELECT snapshot_utc,target,http,rows,note FROM run_log ORDER BY snapshot_utc DESC LIMIT 8"

# is the sitemap fresh, and which pages refreshed?
sqlite3 -column -header data/cprt.db \
  "SELECT * FROM lastmod_profile ORDER BY snapshot_utc DESC LIMIT 8"

# every HTTP request ever made, with robots status
sqlite3 -column -header data/cprt.db \
  "SELECT fetched_utc,url,http_status,bytes,robots_status FROM provenance ORDER BY fetched_utc DESC LIMIT 20"

# prove no robots-disallowed URL was ever fetched (must return 0)
sqlite3 data/cprt.db \
  "SELECT count(*) FROM provenance WHERE robots_status='disallowed' AND http_status IS NOT NULL"

# the backtest, pair by pair
sqlite3 -column -header data/cprt.db "SELECT * FROM backtest_pairs"

# my transcript numbers vs Stephens, cell by cell
./.venv/bin/python scripts/corroborate_stephens.py

# re-run any derived metric from raw bytes on disk
./.venv/bin/python scripts/inventory_panel.py
./.venv/bin/python scripts/cadence_fixed_window.py
./.venv/bin/python scripts/ppe_components.py
```

Every derived number is reproducible from `raw/` without re-fetching anything. If a script
output disagrees with `findings.md`, **the script is right and the doc is stale.**

---

# 6. Current state

- **Collector:** LaunchAgent `com.cprt.job1`, daily 09:17 local. Ran unattended 2026-09-08
  and 2026-09-09. The prior `com.kendall.cprt-snapshot` is disabled (`.plist.disabled`).
- **Data:** 859MB. 28 tables. 123 logged HTTP requests, 0 to disallowed paths.
- **Days of live collection banked:** 2.
- **Next hard event:** Q4 FY26 prints 2026-09-10 — tests the −5.1% nowcast out of sample and
  supplies the cycle-time number the unit forecast depends on.
