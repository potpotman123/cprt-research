# Copart (CPRT) research data pipeline — build spec

You are building a local data pipeline for an equity research pitch on **Copart, Inc. (NASDAQ: CPRT)** for the HFAC x Citadel Intercollegiate Stock Pitch Competition. Submission is **October 2, 2026**. Work fast, prefer working code over elegant code, and report what you find rather than what you assume.

## The point of all this

Copart discloses **percentages, never absolutes**. No absolute unit counts, no revenue per unit, no consignment-vs-purchase contract mix, no per-yard anything, no maintenance capex. The thesis rests on reconstructing those undisclosed quantities from public sources. Three specific questions we are trying to settle, each of which is currently argued in public with adjectives rather than data:

1. **Units.** Can we count Copart's quarterly volume from public data before the company reports it?
2. **RPU.** How much of Copart's revenue-per-unit growth is fee-schedule hikes vs. rising average selling prices? (Elasticity of RPU to ASP is believed to be ~0.25–0.35, not ~1.0. The Street models it closer to 1.0.)
3. **Owner earnings.** What is maintenance capex, separated from discretionary land banking?

---

## HARD CONSTRAINTS — read before writing any fetching code

`https://www.copart.com/robots.txt` disallows:

```
/public/data/        <-- the site's internal JSON API. DO NOT hit this directly.
/downloadSalesData
/memberFees
/lotSearchResults/   (bare /lotSearchResults$ IS allowed)
```

Rules:

- **Respect robots.txt.** This work goes in front of hedge fund judges; a provenance question we can't answer cleanly is worse than missing data.
- **Do not authenticate and then scrape.** Copart's member agreement prohibits automated access. Unauthenticated public browsing is a much cleaner posture than logged-in scraping. If a Copart account exists, use it by hand only.
- Rate limit everything. 1–2s between requests minimum. Identify with a real User-Agent including a contact email.
- Do not defeat bot protection, CAPTCHAs, or paywalls.
- **Log the exact provenance of every dataset** — URL, method, date, and whether robots permitted it. We need an appendix that survives scrutiny.

---

## JOB 1 — Daily sitemap snapshot (START TODAY, cannot be backfilled)

Copart's own sitemap index lists these. All are static XML, all sanctioned.

```
https://www.copart-sitemaps.com/sitemap-index.xml     (index; note the separate domain)
https://www.copart.com/sale-list-results.xml          (~1,144 entries)
https://www.copart.com/lot.xml?page=1                 (~700 entries)
https://www.copart.com/lot.xml?page=2                 (~700 entries)
https://www.copart.com/lot.xml?page=3                 (~400 entries)
https://www.copart.com/CMS/en/content/location.xml    (yard list)
https://www.copart.com/models-list.xml
```

Note: `copart-sitemaps.com` had an SSL chain issue from one client — if verification fails, diagnose rather than blanket-disabling verification.

**`sale-list-results.xml` is the valuable one.** Format:

```
/saleListResult/{yardId}/{YYYY-MM-DD}?location={ST - City}&saleDate={unix_ms}
```

That is Copart's **complete US yard roster with numeric IDs plus every scheduled auction date**. Examples: 309 = CA Adelanto, 308 = WI Madison South, 336 = UT Salt Lake City, 335 = FL Tampa North, 338 = NC Lumberton, 337 = WA Spanaway.

Derived series we want from it: **sale events per yard per week over time.** Yards add sale days when throughput rises and drop them when it falls. That is a clean operational volume proxy nobody tracks, and it needs no gated data at all.

**`lot.xml` is an SEO-curated subset** — only ~1,800 lots total, and page 2 profiled at 89% clean-title / 11% salvage, the inverse of Copart's real business. Do **not** treat it as inventory. It is useful for two things: (a) tracking Copart's clean-title / whole-car SEO push over time, which is on-thesis, and (b) harvesting `(lot_id, date)` pairs.

Slug format encodes real fields: `/lot/{id}/{title-type}-{year}-{make}-{model}-{st}-{city}`

Schema — append one row per lot per snapshot, with a UTC snapshot timestamp:

```
snapshot_utc, lot_id, title_type, year, make_model, state, yard_slug, lastmod, loc
```

Put it on cron immediately (daily, early morning). SQLite preferred, CSV mirror fine.

---

## JOB 2 — Sale-list lot enumeration (the real volume data)

Each `saleListResult` page lists the lots in that yard's sale. Verified by hand on yard 309 (CA Adelanto): **591 entries**, paginated 20 at a time, with facet counts shown (Clean Title 50, Non Repairable 12, Salvage Title 100+).

Per-lot fields visible **without logging in**:

```
lot_id, year, make, model, odometer, odometer_flag (ACTUAL / NOT ACTUAL),
estimated_retail_value, title_type + title_state e.g. "Salvage Title (SC - CA)",
damage_type (Front End / Rear End / Side / Undercarriage / Mechanical /
             All Over / Minor Dent-Scratches ...),
keys_available, yard, sale_date / countdown, current_bid, buy_it_now_price,
sale_status (Upcoming lot vs live)
```

**Investigate the "Export" button first.** The sale list page has a native Export control. If it produces a CSV/XLSX of the result set, that is by far the best path — it is a first-party feature, not scraping. Find out what it emits and whether it works logged out.

**Important caveat:** these pages render client-side from `/public/data/`, which robots disallows. So: prefer Export; failing that, render the page as a browser would and rate-limit hard; document the choice and the reasoning either way. **Do not** enumerate `/public/data/` endpoints directly.

Two filters on the page matter:
- **"Exclude Purple Wave lots"** — Purple Wave (Copart's industrial/ag auction arm) shares the lot-ID sequence. This explains lot IDs ranging 41M–99M. Segment it out; current Copart issuance is ~99M+.
- **"Exclude upcoming auction vehicles"** — separates live from scheduled.

Even if per-lot capture proves hard, **capture the total-entries count and the title-type facet counts per yard per day.** Those alone give volume and mix.

---

## JOB 3 — Historical anchors from the Internet Archive

Needed for the backtest. The CDX API returns one row per capture:

```bash
# archived Copart URLs containing "fee", collapsed so only content CHANGES appear
curl -s 'https://web.archive.org/cdx/search/cdx?url=copart.com*&fl=original,timestamp&filter=original:.*[Ff]ee.*&collapse=digest&limit=1000'

# sitemap history
curl -s 'https://web.archive.org/cdx/search/cdx?url=copart-sitemaps.com*&fl=original,timestamp&limit=500'

# THE important one: archived lot pages = free (lot_id, date) anchor pairs
curl -s 'https://web.archive.org/cdx/search/cdx?url=copart.com/lot/*&fl=original,timestamp&limit=5000'

# sale list pages
curl -s 'https://web.archive.org/cdx/search/cdx?url=copart.com/saleListResult/*&fl=original,timestamp&limit=5000'
```

Preliminary probing via the availability API suggested **single snapshots, not time series**, for the fee pages (Basic-Member-Fees: one capture ~Jul 2025; premier-member-fees: one ~Mar 2026; sitemap-index: one ~Jan 2026). Those probes used guessed URLs, and Copart has restructured its site over the years — CDX with wildcards is the authoritative check. Please settle it.

**Why lot-page anchors matter:** if lot IDs are monotonic in time within a partition, the ID *is* a clock. Enough `(lot_id, date)` pairs reconstructs Copart's historical assignment rate without ever having had a crawler running. Test the monotonicity hypothesis explicitly — bucket IDs, look for partition boundaries (Purple Wave, international, business line), and report whether it holds.

---

## JOB 4 — SEC filings (fully self-contained, do this while other jobs run)

Copart CIK **0000900075**. Fiscal year ends **July 31**.

```
https://data.sec.gov/submissions/CIK0000900075.json
https://data.sec.gov/api/xbrl/companyfacts/CIK0000900075.json
```

SEC requires a descriptive User-Agent with a contact email or it 403s.

Extract per fiscal year, **FY2016 through FY2025**:

```
total revenue, service revenue, purchased-vehicle revenue,
operating income, D&A, capex (purchases of PP&E),
cash & equivalents, shares outstanding,
acres owned, acres leased, facility/yard count
```

The acreage and yard-count figures are in the Item 2 Properties narrative, not XBRL — parse the 10-K text.

**Then compute the thing nobody has:**

```
land_capex      ≈ Δ(acres owned) × regional industrial land $/acre
maintenance_capex ≈ total_capex − land_capex − new-yard construction
owner_earnings  =  EBIT + D&A − maintenance_capex
```

Compare `maintenance_capex` to reported D&A. Note that GAAP does not depreciate land, so D&A already excludes the growth asset — meaning D&A may be a defensible proxy for maintenance capex at Copart specifically. **If the residual tracks D&A, that validates the proxy and we can build a clean 10-year EV/owner-earnings series.** If it diverges, the size and sign of the divergence is itself the finding.

Also pull the buyer fee schedule and structure it into bands:

```
https://www.copart.com/Content/US/EN/Basic-Member-Fees
https://www.copart.com/content/us/en/premier-member-fees
https://www.copart.com/content/us/en/member-fees-us-licensed
```

Known structure to verify: **$95 gate fee + $15 environmental fee** fixed per car regardless of price; **flat $1,000 buyer fee** in the $10,000–15,000 band; **7.50% + $250** above $15,000. Encode as a function `fee(asp) -> dollars` so an ASP distribution can be run through it.

---

## JOB 5 — Carrier data for mix attribution

- **Progressive publishes monthly results including policies in force** — investors.progressive.com. Monthly public feed on the single most contested carrier. Pull the full history.
- **GEICO** — Berkshire Hathaway 10-Q/10-K segment disclosure.
- **State Farm** — mutual; NAIC statutory filings.
- **NAIC state-level private passenger auto market share by carrier** — annual reports.

Goal: pair NAIC carrier share *by state* with Copart lot volume *by state* (from Jobs 1–2), regress over time, and estimate Copart's implied carrier exposure. Then weight by each carrier's disclosed PIF growth to build a bottom-up unit forecast.

Context: Progressive routes roughly **75% of salvage to IAA, 25% to Copart** — inverted versus other top-10 carriers. Progressive passed State Farm as the **#1 US auto insurer in May 2026** and adds ~3M policies a year, so this mix drag compounds through growth rather than annualizing away.

---

## Facts already established — do not re-derive, but DO reconcile

- **Q4 FY26 earnings: September 10, 2026.**
- Q3 FY26 actuals: global insurance units **−2.7%**, US insurance units **−4.2%**, US inventory **−4.7%**, US assignments down low-single-digit, Copart Direct units **−26.3%**; ASP **+4.6%**, US insurance ASP **+4.1%** (record); revenue **$1.24B (+2.1%)**; international revenue **$234.2M (+14.1%)**, international operating margin **31.5%**; gross margin **46.3% (+71bp)**; cash **$4.2B**, zero debt, **$5.5B** liquidity; buybacks **43.4M shares / $1.6B** fiscal YTD; FCF +12% YTD.
- A third-party analysis reports FY26 insurance unit YoY of **−7.3% / −4.8% / −3.1%** for Q1/Q2/Q3. That Q3 figure conflicts with the −4.2% US / −2.7% global above. **Reconcile which basis is which and document it** — the whole unit thesis depends on getting this series right.
- CEO transition: **Jeff Liaw out effective July 31, 2026**; **Jay Adair** resumed as CEO (announced June 29, 2026).
- **Copart is reportedly among the suitors for CCC Intelligent Solutions** (Bloomberg, Aug 18 2026), alongside GTCR and Veritas. CCC market cap ~$4.2B; valued ~$8B in 2023; Elliott activist stake drove the process. Pull everything public on this — it is likely the central catalyst.

---

## Deliverables

1. `cprt.db` (SQLite) + CSV mirrors, in a `data/` directory, with a cron job running Job 1 daily.
2. `PROVENANCE.md` — every source, URL, method, date, robots status.
3. `findings.md` — what the data says, with the reconciliation of the unit series, the lot-ID monotonicity test result, and the maintenance-capex-vs-D&A comparison.
4. A short profile printout after each run: lot-ID min/max and gap structure, title-type mix, state distribution, yard count, sale-event count.

Report blockers immediately rather than working around them — especially anything that would require authenticating, hitting `/public/data/`, or otherwise crossing the constraints above.
