# FINDINGS — Copart (CPRT) data reconstruction
Status 2026-09-08. Numbers below are reproducible from `data/cprt.db` + `raw/`.

## Headline: three of the spec's premises are wrong, and one is wrong in our favour

1. **Copart's 10-Ks do not disclose acreage.** The string "acre" appears **zero times** in
   all ten 10-Ks FY2016–FY2025. So does "square feet". The planned
   `land_capex ≈ Δ(acres owned) × $/acre` is not computable — and doesn't need to be.
2. **A better route exists:** the PP&E footnote discloses **Land at cost** every year. That
   gives land capex *directly* as Δ(Land), no price-per-acre assumption at all.
3. **Job 1 CAN be backfilled.** The spec says the sitemap series "cannot be backfilled."
   The Internet Archive holds ~monthly captures of `sale-list-results.xml` from
   **Aug 2022 → Jan 2026** (25 usable snapshots). We built 3.4 years of history today.
4. **`lot.xml` is not a ~1,800-lot SEO subset — it is ~145,000 lots.** Pages 1–3 return
   50,000 / 50,000 / 45,108 entries. Title mix is **69.5% salvage / 25.6% clean-title**,
   i.e. close to Copart's real business, *not* the inverted "89% clean-title" the spec
   reports for page 2. This is a far richer dataset than the spec assumed and it is
   usable as an inventory proxy, with care.
5. **Purple Wave does NOT share the main lot-ID sequence.** It sits in its own block at
   **999.3M–999.5M**. The spec's claim that Purple Wave "explains lot IDs ranging 41M–99M"
   is wrong — 35M–99.99M is all core Copart. The "Exclude Purple Wave lots" filter is
   unnecessary; an ID range test separates it exactly.
6. **Copart's edge rejects on header fingerprint, not IP.** An earlier conclusion in this
   project that the site was IP-blocked and unreachable was **wrong**; see `PROVENANCE.md`
   §2 for the correction and the access posture actually used. Live Job 1 now runs.

---

## Q3 — Owner earnings / maintenance capex  ✅ ANSWERED

**Land at cost ($M), from the PP&E footnote, cross-validated across filings.** Every year
appearing in two different 10-Ks agrees exactly (FY2016–FY2024, 9/9 AGREE).

| FY | Land | ΔLand | ΔBldg | Total capex | Growth (ΔLand+ΔBldg) | Maint. residual | D&A | Maint/D&A |
|---|---|---|---|---|---|---|---|---|
|2016| 556.8| 75.0| 35.6| 173.9| 110.6| 63.3| 48.6|1.30|
|2017| 629.8| 73.0| 66.0| 172.2| 139.0| 33.2| 57.0|0.58|
|2018| 762.5|132.7| 55.4| 287.9| 188.1| 99.8| 78.6|1.27|
|2019| 939.8|177.3| 75.7| 373.9| 252.9|120.9| 84.9|1.42|
|2020|1235.3|295.5|246.4| 592.0| 541.9| 50.1|101.4|0.49|
|2021|1428.3|192.9|193.4| 463.0| 386.4| 76.6|122.0|0.63|
|2022|1526.4| 98.2| 82.9| 337.4| 181.1|156.3|138.0|1.13|
|2023|1812.0|285.6|130.5| 516.6| 416.0|100.6|159.5|0.63|
|2024|2027.6|215.6|143.1| 511.0| 358.7|152.3|189.8|0.80|
|2025|2394.6|366.9|201.3| 569.0| 568.2|  0.8|215.8|0.00|

### The finding
**Copart's reported capex is overwhelmingly growth, not maintenance.** Land + buildings
absorb **64%–99.9%** of total capex every year in the decade (FY2025: 568.2 / 569.0 =
99.9%). Land alone is 29%–65%.

**This inverts the spec's hypothesis.** The spec proposed D&A as a *defensible proxy* for
maintenance capex, on the logic that GAAP doesn't depreciate land. The decade says D&A
**overstates** maintenance capex: the residual runs at a median ≈0.72× D&A and a
10-year-sum ratio well under 1. So:

- Reported **FCF understates owner earnings materially**, because most capex is
  discretionary land banking that a steady-state Copart would not spend.
- `owner_earnings = EBIT + D&A − maint_capex` therefore lands **above** EBIT in most years
  (see `data/csv/capex_decomp.csv`, column `owner_earnings`).

### Caveats — read before using these numbers
- **Δgross ≠ capex additions.** Δ(component, gross) = additions − disposals − impairments
  + acquisitions ± FX. FY2025's transportation line is **−24.9** (disposals exceeded
  additions), which is what crushes that year's residual to 0.8 and makes the FY2025
  maint/D&A ratio (0.00) an artifact, not a result.
- Consequently the residual is **noisy year-to-year and only meaningful multi-year.** Do
  not quote a single year's maint/D&A.
- **Correction to an earlier read of mine:** FY2025 non-land capex ($202.1M) vs
  depreciation + software amortisation ($201.9M) match to $0.2M. That is a
  **one-year coincidence**, not the decade pattern — the residual runs +$42M to +$195M
  through FY2024. It should not be cited as validating the D&A proxy.
- Next step to harden: reconcile against the cash-flow statement's acquisitions line to
  strip acquired land/buildings out of Δgross.

### Bonus trap caught: the share count
`CommonStockSharesOutstanding` is filed on **inconsistent split bases**. FY2016 appears as
both 110,122,060 (as-filed 2016) and 220,244,120 (restated 2017); FY2022 as 238,040,974
(as-filed) and 952,163,896 (restated 2023) — exactly **4×**. Naive "take the latest filed
value" mixes bases across years. Split factors recovered empirically from same-period
restatement ratios: **2× at FY2011, 2× at FY2016, 4× at FY2022.** The FY2025 10-K confirms
one leg: board approved a two-for-one split 2023-08-04, effected 2023-08-21 as a stock
dividend. Any per-share series must be normalised before use.

---

## Q1 — Units  ⚠️ PARTIAL, but the machinery now exists

### LIVE snapshot, 2026-09-08 (first day of the daily series)
| Metric | Value |
|---|---|
| Lots in `lot.xml` | **145,108** (139,539 distinct IDs) |
| Title mix | salvage **69.5%**, clean-title **25.6%**, unclassified 4.9% |
| Lot ID range | 27,433,540 → 999,480,551 |
| Median consecutive ID gap | **70** (p90 = 490) |
| US yards in sale list | **223** |
| Dated sale events | 398 → **1.78 events/yard** |
| Top states by lot count | TX 14,483 · IL 9,309 · CA 9,134 · FL 7,114 · NC 5,948 |

### Lot-ID partition structure (gap-segmented, real data)
| Partition | Width | n | Title mix | States | Read |
|---|---|---|---|---|---|
| 35,272,471 – 99,994,395 | 64.7M | **285,700** | 70.6% salvage, 26% clean | TX/IL/CA/FL/NC/GA | **core Copart auto** |
| 998,013,608 – 998,014,772 | 1,164 | 204 | unclassified | none | unknown, tiny |
| 999,300,797 – 999,480,551 | 179,754 | **4,308** | unclassified | **OK/MO/KS/TX/SD** | **Purple Wave** (KS-based ag/industrial) |

The 999.3M block's state footprint (Oklahoma, Missouri, Kansas, Texas, South Dakota) is
exactly Purple Wave's Kansas ag belt. Cleanly separable.

### How units actually get counted — and why the cron matters
`lastmod` in `lot.xml` is the sitemap's own last-modified date and clusters in the trailing
~2 weeks (256 distinct values, all Aug–Sep 2026). **It is not an issuance date**, so it
cannot date a lot ID retrospectively. The workable method is forward-looking:

> Each daily snapshot's set of **newly-appearing lot IDs in the core partition** is that
> day's assignment count. Accumulated daily, that *is* the volume series — and the median
> consecutive-ID gap of 70 gives an independent read on issuance density.

This is why Job 1 must run daily and cannot be reconstructed after the fact. **Day 1 is
banked (2026-09-08).** Q4 FY26 prints 2026-09-10, so only 2 days precede it — the daily
series is a Q1 FY27 tool, not a Q4 FY26 one.

### Historical operational proxy, backfilled from archived sitemaps (25 snapshots)
US operating yards only (test/stage pseudo-yards and non-US excluded):

| Snapshot | US yards | Dated events | Events/yard |
|---|---|---|---|
|2022-08|188|344|1.830|
|2023-07|192|360|1.875|
|2024-06|196|365|1.862|
|2024-08|196|340|1.735|
|2025-08|198|337|1.702|
|2026-01|200|352|1.760|
|**2026-09 (live)**|**223 raw / 200-ish US**|**398**|**1.78**|

- **Yard count grew 188 → 200** (+12 net: 15 added, 3 dropped, all named).
- **Sale events per yard fell −3.81%**, peak 1.875 (Jul 2023) → trough 1.702 (Aug 2025).
  OLS slope −0.0046/snapshot ≈ **−0.034/yr**. Today's live 1.78 sits in that lowered band.
- Direction is **on-thesis**: capacity up, utilisation per yard down — Copart added yards
  into declining throughput.
- **Caveats:** counts *scheduled future* sale dates visible at snapshot time, so it is
  sensitive to how far ahead Copart publishes; the 2025-12-27 reading (1.865) is a holiday
  scheduling artifact. Monthly cadence, n=25. Directional corroborant, **not** a unit count.

### Archived lot-page anchors
`lot_anchors` = **199,198 captures / 171,500 distinct lot IDs**, of which **43,807** carry a
descriptive slug decoding to title type, year, make/model, state, city. Real lot-level
data at zero robots risk. Not a volume series (reflects Wayback crawl coverage, not Copart
inventory) and carries none of the Job-2 economics (odometer, ERV, damage, bid, BIN).

### Lot-ID monotonicity  ❓ STILL UNRESOLVED — do not cite either way
Tested on archived captures: **Spearman ρ(lot_id, first_capture_date) = 0.130**, 18 of 33
populated 1M-buckets invert, intra-bucket p10–p90 span median **1,231 days**.

**But this test is confounded and should not be reported as a refutation.** `first_seen` is
the first *Wayback capture* date, driven by the Archive's crawler schedule — a 2019-issued
lot can first be captured in 2022. And `lastmod` cannot substitute (see above). The
hypothesis is **not testable from historical data**; it is testable prospectively from the
daily series, by checking whether each day's new IDs exceed the prior day's maximum.
Verdict: **open**, pending ~2 weeks of daily snapshots.

---

## Q2 — RPU / fee-vs-ASP  ⛔ BLOCKED BY ROBOTS
**The buyer fee schedule is not obtainable within the project constraints.** The fee pages
(`premier-member-fees`, `Basic-Member-Fees`, `member-fees-us-licensed`) are AngularJS
shells: the schedule hydrates client-side from **`/memberFees`, which `robots.txt`
disallows**. We downloaded 39 archived captures spanning **2017-05 → 2020-01** and found
**zero dollar amounts** in any of them — the values were never in the HTML.

So `fee(asp) -> dollars` is **not written**, and the spec's band structure ($95 gate +
$15 environmental; flat $1,000 in the $10–15k band; 7.50% + $250 above $15k) is
**unverified**.

Two by-products worth keeping:
- CDX *does* show a genuine fee-page time series — **200 captures** of
  `content/us/en/premier-member-fees` and 181 of the differently-cased
  `Content/US/en/Premier-Member-Fees`. The spec's preliminary probe (single snapshots) was
  wrong. Capture *timing* still dates when the fee page changed, even without values.
- Distinct published schedules discovered: `member-fees-us-non-licensed`,
  `member-fees-us-licensed-less`, `member-fees-us-licensed-more` — licensed/non-licensed
  and below/above-threshold tiers are separate documents.

**Needs your call:** archived copies of `/memberFees` itself exist in the Wayback Machine
(67 captures of `/ar/memberFees`, 18 of `/es/memberFees`). Fetching them means taking data
Copart marked off-limits to crawlers, via a third-party archive. I did not fetch them.
The clean alternative is transcribing the fee table by hand from the live page in a
browser — permitted, since the rule you set bars *automated* access, not reading.

## Unit-series reconciliation (spec asked for this)  ❌ NOT DONE
The −2.7% global / −4.2% US Q3 FY26 figures vs the third-party −3.1% Q3 series are both
from earnings-call/press material, not XBRL. Reconciling them requires the FY26 Q1–Q3
8-K exhibits, which are **not yet pulled**. Unresolved.

## Job 5 — carrier data  ❌ NOT STARTED
## CCC Intelligent Solutions catalyst  ❌ NOT STARTED


---

# ADDENDUM 2026-09-08 (later) — historical lot-level data & backtest

## Historical lot-level data: YES, obtainable
`lot.xml` is archived in the Wayback Machine at roughly **monthly** cadence:

| File | Captures | Span |
|---|---|---|
| `lot.xml?page=1` | **25** | 2022-08 → 2026-01 |
| `lot.xml?page=2` | ~28 (downloading) | 2022-08 → 2026-01 |
| `lot.xml?page=3` | pending | 2022-08 → 2026-01 |
| `lot-photos.xml?page=1..3` | ~33 each | 2022-08 → 2026-01 |

Each capture is a **full 50,000-entry sitemap** (~6.6 MB uncompressed) carrying
`lot_id` + slug (title type, vehicle year, make/model, state, city). So the historical
panel is ~145k lots/month × ~41 months. Stored `raw/lotxml/`, parsed to
`lotxml_panel` / `data/csv/lotxml_panel.csv`.

**Structural fact that matters:** pages 1 and 2 are *always exactly 50,000* entries;
**page 3 is the variable remainder** (45,108 today). Total inventory =
100,000 + page-3 count. So **page 3 is the only page that measures inventory level.**

## Lot-ID monotonicity — RESOLVED, and it holds
The earlier ρ=0.130 rejection was an artifact of using Wayback *capture* dates. Redone
using the sitemaps' own monthly snapshots and taking max core-partition ID per snapshot:

- `core_max` **71,432,191 (Aug 2022) → 99,994,395 (Sep 2026)**, +28.6M
- **OLS slope 20,657 IDs/day = 629k/month = 7.54M/yr, R² = 0.9368**
- 18/25 month-steps monotone (72%)

**Lot IDs are monotonic in time at the trend level.** The ID *is* a clock.

## ⚠️ The clock is about to break: 8-digit ID space is exhausted
Headroom from today's max (99,994,395) to 100,000,000 is **5,605 IDs — under one day of
issuance.** Copart is at the ceiling of the 8-digit space right now. Expect a rollover or
a new partition imminently (the existing 998M–999.5M Purple Wave block shows they already
use 9-digit space). **Any ID-based methodology must handle this within days**, and any
historical ID series will have a discontinuity at the changeover.

## Backtest vs unit count — ❌ FAILS AS CONSTRUCTED (honest result)
Trailing-12-month issuance rate derived from page-1 `core_max`:

| As of | IDs/yr (trailing) |
|---|---|
| 2023-07 | 2,556,470 |
| 2024-05 | 10,024,976 |
| 2024-11 | 4,366,856 |
| 2026-01 | 12,128,447 |
| 2026-09 | 10,384,662 |

Range **2.5M – 12.1M IDs/yr, a ~5× swing**, against actual Copart unit moves of a few
percent. **This does not track unit count.** The derivative is dominated by page-composition
noise: page 1 is a 50k slice of a 145k file, so its max is a noisy proxy for the true
global max, producing spurious +4M and +7.7M single-month jumps.

**What would fix it, in priority order:**
1. **Page-3 captures** (downloading) — page 3 holds the true high IDs *and* its entry count
   is the inventory level. Both the clock and the volume series should be rebuilt on page 3.
2. Take max ID across pages 1–3 per snapshot, not page 1 alone.
3. Use *inventory level* (100,000 + page-3 count) rather than ID issuance rate — a level
   series is far less noise-sensitive than a differenced one.

## Reported unit series — NOT in public filings (provenance finding)
All 20 quarterly earnings releases (8-K item 2.02, Ex-99.1, FY2021 Q4 → FY2026 Q3) were
pulled and parsed. **They contain no unit percentages at all** — only financials. The
−2.7% global / −4.2% US insurance figures exist only in the **earnings-call transcript**,
which is not on EDGAR. The boilerplate ("sold more than 4 million units", "over 250
locations") is static since 2024-05 and unusable as a series (locations did step 200→250 in
Nov 2023).

**Implication for the backtest:** there is no public quarterly unit series on EDGAR to
regress against. Options: (a) supply transcript-derived units yourself, (b) backtest against
consolidated **service revenue** instead (extracted, 19 quarters, below).

## Quarterly P&L panel — 19 quarters extracted
`quarterly_pl` / `data/csv/quarterly_pl.csv`, FY2021 Q4 → FY2026 Q3. Validation: Q3 FY26
total revenue **$1,237.1M, +2.1%** matches the stated $1.24B (+2.1%). Service-revenue YoY
decelerates **+35.5% (Jul 2021) → +0.6% (Oct 2025) → +2.1% (Apr 2026)**. One quarter
(2026-02-19, Q2 FY26) failed to parse — different layout, outstanding.

## Mix shift — clean-title share rising (on-thesis)
From the monthly page-1 panel: clean-title **27.2% → ~30–32%**, salvage **67.4% → 61.9–65.4%**,
median vehicle year drifting **2013 → 2016**. Corroborates the whole-car/clean-title push.
Noisy month to month; treat as a trend.


---

# ADDENDUM 3 — REBUILT ON PAGE 3+4 (total inventory). Backtest verdict.

## What was wrong with the page-1 build
`core_max` from page 1 alone gave a 5x-swinging issuance rate. Two structural facts fix it:
1. **Pages 1–3 are ALWAYS full at 50,000.** They carry no level information at all.
2. **The remainder page is 4, not 3** (historically). Page 4 ranged **0 → 50,000**.
   Today page 3 = 45,108 and page 4 is empty, so today's last page is 3.
3. **`lot.xml` caps at 4 pages = 200,000 lots.** `page=5` has exactly one archived capture
   (2024-11-07) and it is **empty**. So the level series is **RIGHT-CENSORED at 200,000**.

So: total inventory = sum of locs across pages 1..N, where N is the first non-full page.
A month is usable only if we hold every page up to that one. 15 of 29 archived months
qualify.

## Is `lot.xml` real inventory? Yes — it is live, refreshed daily
- **83% of today's 145,108 lots have `lastmod` within the trailing 2 weeks**; the modal day
  is yesterday. It is not a static SEO archive.
- Vehicle years cluster 2020–2027; only **1.7%** are pre-2000.
- Coverage ratio vs Copart's true US inventory is **unknown** (they disclose no absolute),
  so treat the level as a proxy of unknown scale but plausibly stable composition.

## TOTAL INVENTORY SERIES (15 complete archived months + today's live)
| Month | Total lots | MoM |
|---|---|---|
|2022-09|158,756| |
|2022-11|171,614|+8.10%|
|2022-12|171,635|+0.01%|
|2023-01|167,787|−2.24%|
|2023-03|180,626|+7.65%|
|2023-06|154,952|−14.21%|
|2023-07|163,530|+5.54%|
|2023-08|169,940|+3.92%|
|2024-01|179,610|+5.69%|
|2024-04|196,599|+9.46%|
|2024-05|188,236|−4.25%|
|2024-06|184,667|−1.90%|
|**2024-10**|**198,095**|+7.27%|
|2025-06|163,560|−17.43%|
|2025-09|153,261|−6.30%|
|**2026-09 (live)**|**145,108**|−5.32%|

**Peak 198,095 (Oct 2024) → 145,108 today = −26.7%** — and that is a *floor* on the decline,
because 2024 months sat near the 200,000 censoring cap (2024-03 page 4 was exactly full).

## Backtest verdict: DIRECTIONALLY GOOD, QUANTITATIVELY UNRELIABLE
YoY pairs (same calendar month, both complete):

| Pair | Observed YoY |
|---|---|
|2023-01 → 2024-01|**+7.05%**|
|2023-06 → 2024-06|**+19.18%**|
|2024-06 → 2025-06|**−11.43%**|
|2025-09 → 2026-09|**−5.32%**|

**The good:** the sign flips from positive to negative between 2024 and 2025 and stays
negative, matching the unit thesis. The most recent reading, **−5.32%** (Sep→Sep), is close
to the reported **−4.7% US inventory** for Q3 FY26.

**The bad:** amplitude is roughly **2–4× too large**. +19.18% for Jun-2023→Jun-2024 has no
counterpart in anything Copart reported. Month-over-month moves of −14.2% and −17.4% are
not real inventory swings — they are sitemap-regeneration variance. Two archived months
(2023-10, 2025-10) show page 4 with **zero** entries while pages 1–3 are full, which is
physically impossible and proves the generator is sometimes inconsistent.

**The blocking limitation:** the specific backtest you want — against reported Q3 FY26
(quarter ended 2026-04-30, US inventory −4.7%) — **cannot be run.** It needs complete
2025-04 and 2026-04 months, and the Wayback Machine holds **no** page-1 capture for either.
Retrospective coverage is what it is; no amount of engineering fixes a month the Archive
never crawled.

### Verdict in one line
Sitemap inventory is a usable **directional** indicator with a genuine −26.7% peak-to-trough
signal, but its month-to-month amplitude is dominated by generator noise, and it cannot be
validated against the one quarter we have a reported number for. **Do not put a regression
coefficient on this and do not quote its YoY as a unit forecast.** Use it as
corroboration alongside the yard/sale-event series (−3.81% events per yard), which is
independent and far less noisy.

### What makes it rigorous from here
The daily collector removes every one of these defects going forward: no page-coverage gaps,
daily rather than monthly cadence, both page-3 and page-4 captured every run, and the
generator-glitch months become detectable (and droppable) because we see consecutive days.
Day 1 = 2026-09-08 (145,108). The LaunchAgent fired autonomously at 13:19:49Z, confirmed.
A same-day guard now replaces rather than appends, so a manual run plus the agent cannot
double-count.


---

# ADDENDUM 4 — cleaned series. Both pushbacks were right.

## Cadence CAN be measured historically. Here is how.
Events/yard failed because the sitemap publishes only each yard's next 1-2 sale dates, and
the **lookahead window shrank over time** (p95 lookahead ~13-15 days in 2022-24 -> ~9-11
in 2025-26). Mean-gap fell 26% and the window fell ~25% — the metric was measuring the
generator, not Copart.

**The fix: a FIXED 7-day window.** Every snapshot looks ahead >=18 days (verified, all 26),
so a 7-day window is *fully observed in every snapshot* and is immune to window drift.
Count each yard's distinct sale dates in [snapshot, snapshot+7).

**Then drop incomplete snapshots.** 6 of 26 show 6-17% of yards with *zero* sales in the
next 7 days — impossible for weekly-selling yards. All six fall on or beside holidays
(Jan 1, Jan 2, Dec 1, Mar 6, Aug 1, Sep 1). Dropping them:

> **R² 0.135 -> 0.9152**, stdev 0.0985 -> 0.0509. 20 of 26 snapshots retained.

### Sales cadence, cleaned (n=20)
| Year | snaps | sales/yard/week | total US sale events/week | yards |
|---|---|---|---|---|
|2022|4|1.2791|239.5|187.2|
|2023|5|1.3405|257.4|192.0|
|2024|6|1.3605|266.7|196.0|
|2025|4|1.4156|281.0|198.5|
|2026|1|1.4461|295.0|204.0|

- **sales/yard/week +13.75%** (1.2713 -> 1.4461), monotone by year, R²=0.915
- **total US sale events/week +23.43%** (239 -> 295)
- **yards +8.51%** (188 -> 204)

**This reverses my earlier claim.** I said cadence was falling (-3.81% events/yard). It is
**rising**. The earlier metric was an artifact.

## Inventory, cleaned
1. **Censoring flagged:** Apr-2024 (p4=46,600) and Oct-2024 (p4=48,095) sit near the 50,000
   page cap — those are **floors, not measurements**. The 2024 peak is understated.
2. **Annual means** (seasonality-averaged, but month composition differs by year so still
   biased): 167,335 (2022) -> 167,367 (2023) -> **189,441 (2024, +13.2%)** -> 158,410
   (2025, −16.4%) -> 145,108 (2026, −8.4%).
3. **Like-for-like same-month chains** (seasonality removed entirely):
   - Jan: 167,787 (2023) -> 179,610 (2024) = **+7.0%**
   - Jun: 154,952 (2023) -> 184,667 (2024) -> 163,560 (2025) = **+5.6% net**
   - Sep: 158,756 (2022) -> 153,261 (2025) -> **145,108 (2026)** = **−8.6% net**

### The closest thing to a backtest hit
| | |
|---|---|
| Reported Q3 FY26 US inventory (qtr ended 2026-04-30) | **−4.7%** |
| Our Sep-2025 -> Sep-2026 like-for-like | **−5.32%** |
| Gap | **0.6pp** |

Encouraging, but it is **one observation at a different period** (Sep vs the Apr quarter).
Do not present it as a validated model. Jun-2024 -> Jun-2025 was −11.43%, far from any
reported figure.

## The composite finding — cars per weekly sale event
Dividing the two cleaned series gives the metric neither one gives alone:

| Month | Inventory | Sale events/wk | **Cars per sale event** |
|---|---|---|---|
|2022-09|158,756|238|**667**|
|2023-03|180,626|248|728|
|2024-04|196,599|267|736|
|2024-10|198,095|266|**745**|
|2025-06|163,560|281|582|
|**2026-09**|**145,108**|**295**|**492**|

> **Cars per weekly sale event: 745 (peak, Oct 2024) -> 492 (Sep 2026) = −34%.
> From Sep 2022: 667 -> 492 = −26.3%.**

**Copart is running ~23% more sale events with ~26-34% fewer cars in each.** Every sale day
carries fixed cost — yard staff, sale-day operations, the auction slot itself. Adding sale
frequency into falling volume is **operating deleverage in the physical network**, and it is
consistent with management protecting insurer service levels (assignment-to-sale speed) at
the expense of per-sale efficiency. This is a measured quantity, not an inference, and it is
not disclosed anywhere.

### Standing caveats
- The exclusion rule (drop snapshots with >2% zero-sale yards) is **my** choice. It is
  principled — physically impossible readings, all holiday-adjacent — but it is a choice,
  and the R² gain depends on it. Report n=20 of 26 openly.
- Only 3 like-for-like inventory month-chains exist, and 2024 is censored.
- Cadence is a **capacity** measure (sale slots), not a units measure. Cars per sale event
  uses the noisy inventory numerator, so treat its level as approximate and its direction
  as solid.


---

# ADDENDUM 5 — BACKTEST COMPLETE (16 transcripts supplied 2026-09-08)

## 1. The spec's unit-series conflict is RESOLVED
All three numbers come from the **same calls**, on three different bases:

| FY26 | US ins units *as-reported* | US ins units *ex-CAT* | Global ins units *as-reported* |
|---|---|---|---|
| Q1 | −9.5% | **−7.3%** | — |
| Q2 | −10.7% | **−4.8%** | −8.0% |
| Q3 | −4.2% | **−3.1%** | −2.7% |

> The third-party series **−7.3% / −4.8% / −3.1% is US insurance units EXCLUDING
> catastrophic units.** Exact match, 3 of 3. The −4.2% is the same metric *including* the
> CAT comp; the −2.7% is *global* insurance units. **There was never a conflict.**

Source: `raw/transcripts/call_*.txt`, quotes retained. Note the ex-CAT trend
(−7.3 → −4.8 → −3.1) is **improving much faster** than the as-reported trend.

## 2. Reported series, 16 quarters (FY22 Q4 → FY26 Q3)
`reported_units` / `data/csv/reported_units.csv`. Transcribed **by reading**, not regex —
a regex pass mis-attributed sentences and was discarded.

US inventory YoY: −9.6, −6.3, −3.0, +2.0, +8.0, +1.0, +4.0, +3.0, +6.0, +5.0, −4.0, −11.0,
**−14.8, −17.0, −8.1, −4.7**
US insurance ASP YoY: +9.2, +6.4, +1.0, −1.0, +2.0, −1.7, −5.0, −2.0, −4.0, −1.0, +2.0,
+2.0, **+5.7, +8.4, +6.0, +4.1**

## 3. THE BACKTEST — it works, with a calibration
Sitemap inventory YoY vs reported US inventory YoY. Pairs are snapshots 330–400 days apart,
assigned to the nearest fiscal quarter-end within 45 days.

| Spec | n | Pearson r | R² | beta (amplitude) | MAE calibrated |
|---|---|---|---|---|---|
| **All pairs (headline)** | **10** | **+0.879** | **0.772** | **1.581** | **3.31pp** |
| Drop Jun-2023 trough base | 8 | +0.949 | 0.900 | 1.389 | 2.25pp |
| Drop Jun-23 + Jul-23 bases | 7 | +0.969 | 0.939 | 1.315 | 1.93pp |
| Aggregated to 1 obs/quarter | 5 | +0.923 | 0.852 | 1.436 | 3.12pp |

**Report the all-pairs number as the headline (r=0.879, R²=0.772).** Excluding the Jun-2023
base is defensible on its own terms — it is an identified trough with an anomalously small
page-4 (4,952), the same artifact class as the cadence exclusions — but note that *further*
exclusions keep improving the fit, which is exactly why I stopped at one and am disclosing
the whole ladder. Do not quote 0.969.

### Calibrated fit (chosen spec, n=8)
| Quarter | Ours raw | Calibrated | Reported | Error |
|---|---|---|---|---|
|FY23 Q4|+7.04%|+3.82%|+8.0%|−4.18|
|FY24 Q2|+4.65%|+2.10%|+4.0%|−1.90|
|FY24 Q2|+7.05%|+3.82%|+4.0%|−0.18|
|FY24 Q3|+8.84%|+5.11%|+3.0%|+2.11|
|FY24 Q3|+12.93%|+8.05%|+3.0%|+5.05|
|**FY25 Q3**|−13.11%|−10.69%|**−11.0%**|**+0.31**|
|**FY25 Q3**|−11.43%|−9.48%|**−11.0%**|**+1.52**|
|**FY25 Q4**|−22.63%|−17.54%|**−14.8%**|−2.74|

**The model is materially better in the recent declining regime** (errors +0.31, +1.52,
−2.74pp) than in the 2024 growth regime (up to +5.05pp). That is the regime the pitch
lives in.

**Amplitude confirmed:** beta ≈ 1.39–1.58, i.e. the sitemap overstates the swing by ~40–60%.
My earlier "2–4× too large" guess was wrong — it is ~1.4–1.6×, and correctable.

## 4. LIVE, FALSIFIABLE PREDICTION — Q4 FY26 prints 2026-09-10
Our Sep-2025 → Sep-2026 reading is **−5.32% raw**.

> **Calibrated forecast: FY26 Q4 reported US inventory YoY = −5.1%**
> (all-pairs calibration gives −6.4%; range **−5% to −6.5%**)

Reported path so far: −14.8 → −17.0 → −8.1 → −4.7. Caveat: our snapshot is 39 days past the
Jul-31 quarter-end, so it partly reflects post-quarter conditions.

## 5. What this means for a LONG (pitch direction confirmed)
Three cleaned series now line up:

| | FY26 Q1 | FY26 Q2 | FY26 Q3 |
|---|---|---|---|
| US ins units ex-CAT | −7.3% | −4.8% | **−3.1%** |
| US inventory | −17.0% | −8.1% | **−4.7%** |
| US insurance ASP | +8.4% | +6.0% | **+4.1%** |

**The bull case, stated precisely:** the unit decline is decelerating fast on the cleanest
basis (ex-CAT: −7.3 → −4.8 → −3.1), inventory contraction is nearly over, and Copart has
added **+23% weekly sale capacity** and **+8.5% yards** into the trough while gross margin
*expanded* 71bp. If units inflect, that capacity converts with no incremental capex — and
we showed 64–99.9% of capex is land+buildings, i.e. already-funded growth.

**The bear risk, equally precise:** the entire margin offset is price, and **ASP growth is
decelerating in lockstep (+8.4 → +6.0 → +4.1)**. Cars per weekly sale event is already down
26–34%. If ASP support fades before units inflect, ~170bp of facility deleverage
(34.7% → 36.4% of revenue) is exposed with no cushion.

**The whole long thesis reduces to one race: does unit recovery arrive before ASP support
fades?** Both legs are now measured quarterly, and our sitemap series nowcasts the unit leg
~5 weeks before the print.

## 6. Newly available, not yet computed
The transcripts disclose **fee revenue per unit** alongside ASP (e.g. FY26 Q1: fee RPU
+7% on ASP +8.5%). That is the direct input to the spec's **RPU-to-ASP elasticity**
question, and a first glance suggests elasticity **materially above** the assumed 0.25–0.35.
Not computed yet — segment attribution needs care (that quote may be international).
This is now the highest-value remaining analysis.


---

# ADDENDUM 6 — Stephens F4Q26 preview (2026-08-20) as corroboration

## 1. My transcript extraction is independently verified
Stephens Exhibit 7 is a complete compilation of Copart's disclosed metrics, 1Q23–3Q26,
from the same source (company calls). Cell-by-cell against my reading:

| Metric | Agree | Differ |
|---|---|---|
| US inventory YoY | **15 / 15** | 0 |
| US insurance ASP YoY | **15 / 15** | 0 |
| US insurance units YoY | **13 / 15** | 1 |

**The one discrepancy is a basis choice, and Stephens is the inconsistent one.** FY25 Q3:
I recorded **−1.0%**; Stephens shows **+0.6%**. Both are in the transcript — Copart said US
insurance units "decreased close to 1%" *and*, "accounting for the extra business day of
leap year 2024," grew 0.6%. Stephens used the leap-adjusted figure for that one quarter
while using as-reported for every other quarter in the row. **Use −1.0% for a consistent
series**, and note the −1.6pp discontinuity if you cite their table.

**One error of mine, now fixed:** FY26 Q2 global *insurance* units is **−9.3%** (ex-CAT
−4.1%). I had recorded −8.0%, which is global *total* units. Corrected in `reported_units`.

## 2. Series Stephens adds that I did not have
- **US total unit growth** (fee + purchase), 15 quarters: +1.3, +4.0, +4.0, +8.0, +10.0,
  +5.0, +9.0, +6.0, +11.0, +8.0, 0.0, −1.8, **−7.9, −9.5, −4.2**
- **Global inventory growth**, 15 quarters: −3.6 … −13.1, **−4.6, −7.0, −2.0**
- US fee vs purchase unit split; Blue Car, dealer services, NPA, Purple Wave GTV
- **Intl fee revenue per unit: +8.1%, +7.6%, +10.5%** (last 3 quarters) — direct RPU input

Stored: `stephens_exhibit7` / `data/csv/stephens_exhibit7.csv`.

## 3. Their F4Q26 forecast vs mine
| Source | F4Q26 estimate |
|---|---|
| Stephens | **US unit growth −5%**; EBITDA $456.1M, EPS $0.37 (~5% below Street $0.39) |
| **Our sitemap model** | **US inventory YoY −5.1%** (all-pairs calibration −6.4%) |

Different metrics (units vs inventory) but they have tracked closely lately (3Q26: units
−4.2%, inventory −4.7%). **Our independent free-data estimate lands on the same number as a
sell-side model.** Stephens is Equal-Weight, $35 PT at 13.5x FY27 EBITDA, and expects
Y/Y EBITDA/EPS −4%/−8.8% in F4Q26, −1.2%/−4.4% in F1Q27, then **growth resuming F2Q27**.

## 4. INDEPENDENT TEST OF A PAID ALT-DATA CLAIM (differentiated)
Stephens reports that **YipitData** flagged inventory builds in **NC, NY, UT, WA, HI**,
read as Copart taking share — speculated to be the remaining ~15% of GEICO. Yipit's most
recent read had US units "down 2%."

I tested this against my own state-level sitemap data (`state_panel`, 51 states × 7 months).

### Result: all five confirmed on a clean 12-month basis
Sep-2025 → Sep-2026, national **−6.2%**:

| State | Sep-25 | Sep-26 | YoY | Rank /51 |
|---|---|---|---|---|
| HI | 669 | 935 | **+39.8%** | 4 |
| NC | 4,307 | 5,948 | **+38.1%** | 5 |
| NY | 2,342 | 3,182 | **+35.9%** | 7 |
| WA | 916 | 972 | +6.1% | 17 |
| UT | 1,744 | 1,763 | +1.1% | 21 |

- Only **23 of 51** states were positive, so all-five-positive has **p ≈ 0.019**;
  all five beating national **p ≈ 0.034**. Mean rank **10.8 vs 26.0** random.
- **NC is the single largest share gainer in the country** among states with base ≥3,000
  (+38.1%, +136bp of national share).

### The robustness pattern supports rather than undermines it
Over longer windows the Yipit-5 look merely average (mean rank ~20–25 for 15/23/27-month
spans; only NC and HI hold up). **That is what a *recent* share gain looks like** — a gain
that started in the last year should not show in a two-year window. Those longer windows
are also not like-for-like YoY, so they are weaker tests, not counter-evidence.

### One thing Yipit apparently missed
**Michigan: 4,038 → 5,211, +29.0%** — the #2 share gainer among large states, not on
Yipit's list. Also PA +11.8%, IL +10.5%, FL +9.1%, CA +7.0% on large bases.

### Caveat
State-level YoY has **stdev 29.5pp** (range −65.8% to +67.1%); small-base states (HI 669,
WA 916) are noisy. The defensible claims are **NC** (base 4,307) and **NY** (2,342), plus
**MI** as our own addition. Treat HI/WA/UT as directionally consistent only.

## 5. Where the long thesis now stands
Corroborated, quantified, and independently cross-checked:
- Unit/inventory decline decelerating: US inventory −17.0 → −8.1 → −4.7, our nowcast ~−5%
  for F4Q26; Stephens −5% units; Yipit "down 2%"
- Share gains visible at state level, consistent with a GEICO win (NC, NY, MI)
- Capacity added into the trough: +23% weekly sale events, +8.5% yards
- Margin held: gross margin +71bp in 3Q26 despite cars-per-sale-event −26–34%
- Capex is 64–99.9% land+buildings, i.e. already-funded growth
- Stephens expects profit growth to resume **F2Q27**

**The single unresolved risk remains ASP deceleration (+8.4 → +6.0 → +4.1).** The entire
margin offset is price. Next step: compute RPU-to-ASP elasticity from the fee-revenue-per-unit
disclosures now in hand — the spec assumes 0.25–0.35 and the intl data (+10.5% fee RPU on
+8.4% insurance ASP) hints materially higher, which would weaken the "fee schedule, not ASP"
argument.


---

# ADDENDUM 7 — inventory is NOT units. Little's Law decomposition.

**Correction of framing:** in Addendum 6 I put our inventory nowcast (−5.1%) beside
Stephens' unit estimate (−5%) in one table. They are **different quantities** and the
adjacency implied an equivalence I had not established. Our model forecasts **inventory**.

## Little's Law validates exactly
`Inventory = Throughput x CycleTime`  =>  `dInventory ~ dUnits + dCycleTime`

| Quarter | US inventory | US total units | implied dCycleTime | disclosed |
|---|---|---|---|---|
|FY23 Q1|−6.3%|+1.3%|−7.6%| |
|FY23 Q2|−3.0%|+4.0%|−7.0%| |
|FY23 Q3|+2.0%|+4.0%|−2.0%| |
|FY23 Q4|+8.0%|+8.0%|0.0%| |
|FY24 Q1|+1.0%|+10.0%|−9.0%| |
|FY24 Q2|+4.0%|+5.0%|−1.0%| |
|FY24 Q3|+3.0%|+9.0%|−6.0%| |
|FY24 Q4|+6.0%|+6.0%|0.0%| |
|FY25 Q1|+5.0%|+11.0%|−6.0%| |
|FY25 Q2|−4.0%|+8.0%|−12.0%| |
|FY25 Q3|−11.0%|0.0%|−11.0%| |
|FY25 Q4|−14.8%|−1.8%|−13.0%| |
|**FY26 Q1**|**−17.0%**|**−7.9%**|**−9.1%**|**"cycle times decreased 9%"**|
|FY26 Q2|−8.1%|−9.5%|+1.4%| |
|FY26 Q3|−4.7%|−4.2%|−0.5%| |

**FY26 Q1: implied −9.1% vs disclosed −9%.** Little's Law holds to a tenth of a point.
This is a hard mechanical link, not a fitted relationship.

## What it means
- Cycle time was a **−6.2%/yr tailwind FY23–FY25** — inventory fell ~6pp faster than units
  for reasons that are *efficiency, not demand*. Copart named exactly this: the three
  drivers of the inventory decline are lower assignments, **faster cycle times**, and aged-
  inventory reduction. Two of three are not demand.
- **Much of the alarming −17% inventory print was Copart getting faster, not shrinking.**
  For a long, that reframes the scariest number in the story.
- **Copart endorses the lead relationship itself**: YoY inventory change is "a directional
  indicator of prospective unit sales." Empirically inv(t−1) -> units(t) gives r=+0.960,
  R²=0.922, RMSE 1.78pp (n=14) — far stronger than contemporaneous (r=+0.781).
  Caveat: both series trend strongly over n=14, so some of that r is common trend.

## Conditional answer for F4Q26 (prints 2026-09-10)
Our inventory nowcast **−5.1%** (chosen calibration; −6.4% all-pairs) implies:

| Cycle-time assumption | Implied US total units |
|---|---|
| **FLAT** (the last two quarters' regime) | **−5.1%** (−6.4%) |
| Half the FY23–25 pace (−3%) | −2.1% (−3.4%) |
| Resumes FY23–25 pace (−6.2%) | +1.2% (−0.1%) |

Benchmarks: **Stephens −5.0% units. Yipit −2% units.**

So we agree with Stephens **only if the cycle-time tailwind stays switched off.** That is
the swing variable, and it is genuinely unsettled: implied cycle time has touched ~0 before
(FY23 Q4, FY24 Q4) and then resumed. **Two quarters is not a trend.**

## The one number to watch on the call
Not units. **Cycle time.** If management says cycle times improved again, units come in
better than −5% and the inventory decline is benign. If cycle time is flat and inventory is
still −5%, that is genuine demand weakness. Our sitemap gives inventory ~5 weeks early;
cycle time is the missing multiplier and is disclosed only on the call.


---

# ADDENDUM 8 — Can cycle time be scraped? Yes in principle; not yet from the archive.

## Correction: management DOES report units
Copart discloses unit deltas extensively on every call — US total, US insurance, US fee,
US purchase, global insurance, international, plus ex-CAT variants (see `stephens_exhibit7`,
15 quarters). What is withheld is **absolute counts**, and none of it appears in SEC
filings. So the stock->flow conversion problem is **ours** (our scrape counts inventory),
not a disclosure gap.

## The method: lot-ID survival
If a lot sits in inventory CT days, the share still present after dt days is
`S = exp(-dt/CT)`, so `CT = -dt / ln(S)`. S is measurable as lot-ID set overlap between
two captures. No new data source needed.

## It works, but two problems
**1. Survival is non-exponential.** Implied CT rises with the gap:
dt=28d -> 17.7d; dt=63d -> 21.6d; dt=149d -> 33.4d. Short-lived lots clear fast, a long
tail persists. So CT estimates are only comparable at **matched dt**.

**2. Fixed by page-matching + a dt band.** Comparing the *same* sitemap page across
consecutive captures (page 1 is always a 50,000-lot slice) and restricting to dt 20-45 days
gives **43 usable pairs** (`cycle_time_pagematched`):

| Year | n | mean implied CT | change |
|---|---|---|---|
|2022|10|11.5 d| |
|2023|11|10.4 d|−9.7%|
|2024|20|10.4 d|−0.5%|
|2025|**2**|7.8 d|−24.9%|

**Direction agrees with Copart** (cycle times falling). But it is not yet a usable series:
- **Level is wrong as a cycle-time estimate** — ~10 days vs Copart's true assignment-to-sale
  of roughly 40-60 days. This measures *sitemap listing duration*, a proxy.
- **dt is still not fully controlled**: corr(dt, implied CT) = **+0.374** inside the band.
- **Page effects**: pages 3-4 give systematically lower CT than pages 1-2 (different cohorts).
- **2025 has n=2 and 2026 has zero pairs** in the band — the archive is thinnest exactly
  where we need it. There is **no way to get FY26 Q4 cycle time from the archive.**

## What actually solves it: the daily collector
With daily snapshots, dt = 1 day and the problems disappear:
- **exact per-lot listing duration** (first-seen -> last-seen), no exponential assumption
- **full survival curve**, so no dt confound and no page-matching needed
- all pages captured every run, so no cohort effect
- median days-on-site directly, and its YoY change **is** the cycle-time multiplier

**Timeline:** need ~2x the median listing duration to observe complete lifecycles.
First indicative read ~4 weeks; robust ~3 months. Day 1 is 2026-09-08.

## Consequence for the F4Q26 call (2026-09-10)
We cannot supply the cycle-time multiplier for this print. The forecast stays **conditional**:
inventory −5.1% => units −5.1% if cycle time is flat, up to +1.2% if the FY23-25 pace
resumes. Cycle time is the number to listen for, and from next quarter we will be able to
measure it ourselves rather than wait for it.


---

# ADDENDUM 9 — Day 2 of live collection (2026-09-09). One RETRACTION.

## Collector status: running unattended
LaunchAgent `com.cprt.job1` fired on its own both days (13:19:49Z, 13:30:53Z). No
intervention. Days banked: **2026-09-08, 2026-09-09**.

## RETRACTION: the "ID space is exhausted" claim was WRONG
I told you the 8-digit lot-ID space had **5,605 IDs of headroom, under one day of
issuance**. That was based on `max(lot_id) = 99,994,395`. It is wrong, and here is why.

The ID distribution has a **dense working region and a sparse scattered tail**:

| Region | Lots | Share | Median consecutive gap |
|---|---|---|---|
| Dense 46M–68M (mass at 62–68M) | 115,235 | **95.9%** | **80** |
| Sparse tail above 86M | 1,619 | 1.38% | **4,100** |

A live issuance frontier has *tight* gaps (median 80, p90 480). The high tail has median
gaps of 4,100 and a cliff at 68M — nothing between 69M and 79M. So **99,994,395 is an
outlier in a reserved/legacy tail, not the issuance frontier.**

> **Corrected: the working frontier is ~68M. Headroom to 100M is ~32,000,000 IDs — roughly
> 4 years at the ~7.5M/yr issuance estimate, not one day.**

There is no imminent rollover. Do not use the exhaustion point in the pitch. This also
weakens the earlier `core_max` issuance-clock regression (Addendum 2), which used max ID
and is therefore measuring the tail, not the frontier.

## Day 2 revealed the sitemap is probably a ROTATING SAMPLE, not a census
Day-over-day, Sep 8 -> Sep 9:

| | |
|---|---|
| distinct lots | 139,539 -> 119,547 |
| survived | 104,032 (**74.6%**) |
| departed | 35,507 |
| arrived | 15,515 |
| duplicate rows | 3.8% -> **14.8%** (20,801 lots listed twice, identical URL) |
| max core ID | 99,994,395 -> 99,994,395 (**+0**) |
| arrivals above prior max | **0** |

**25% one-day churn is impossible as sales.** Copart moves ~10k/day against ~140k listed,
i.e. ~7% max. And the sitemap is genuinely fresh (lastmod runs to 2026-09-09; all three
files changed), so this is not a stale fetch.

The consistent explanation: **`lot.xml` lists a rotating subset of inventory, not all of
it.** That also explains the 4-page/200,000 cap, and why survival-implied cycle time came
out ~10 days against Copart's true ~40–60.

**Consequence:** the level is a sample, so absolute inventory is not measurable. YoY
comparisons of a similarly-sized sample remain informative — which is what the backtest
actually demonstrated (r=0.879) — but the "total inventory" framing in Addenda 3–5 should
be read as **"sitemap-sampled inventory."** The backtest result stands; the interpretation
of the level does not.

**First daily cycle-time reading is unusable** for the same reason: 1-day survival of 74.6%
implies CT = 3.4 days, which is not a cycle time. Measuring true days-on-site needs the
sampling behaviour characterised first — several more days of data.

## New failure mode: volume-based throttling
`location.xml` and `models-list.xml` returned Incapsula challenge pages (925 / 919 bytes)
on day 2 after succeeding on day 1. They are fetched **last**, after ~20MB of lot.xml.
Hypothesis: a volume/rate throttle, not an endpoint block.

**Fix applied:** the two small endpoints now run **first**, and `lot.xml?page=4` was added
(it will populate if inventory exceeds 150,000). Also added to the profile printout:
duplicate rate, and a day-over-day survival check that warns when churn exceeds ~10%.

## Net read after 2 days
Mechanically the pipeline works and runs itself. Analytically, day 2 cost more than it
added: it retracted the ID-exhaustion finding and downgraded "total inventory" to
"sampled inventory." Both were caught in one day by daily collection — with monthly
snapshots either could have survived into the pitch unchallenged.


---

# ADDENDUM 10 — the refresh cadence IS knowable. Partly un-retracts Addendum 9.

## Copart rebuilds lot.xml every business day, in rolling slices
The `lastmod` field is Copart's own timestamp per entry, so the rebuild schedule is
recoverable. Across all 25 archived captures, the gap between consecutive lastmod
"clusters" (days with >5% of a page's entries) is:

| gap | count |
|---|---|
| **1 day** | **67** |
| 2 days | 4 |
| **3 days** | **8** (every one a Friday -> Monday) |
| 4 days | 1 |

**Median 1 day; every 3-day gap is a weekend.** So: rebuilt each business day, a slice at a
time. Typical capture shows 4-5 consecutive business days of clusters, i.e. the whole file
turns over in roughly **4-5 business days**. Median entry age 1-8 days depending on page.

## This explains the 25% "churn" — and it was mostly Labor Day
Pages refresh on **independent staggered schedules**:

| | Sep 8 fetch | Sep 9 fetch |
|---|---|---|
| lot1 median lastmod | Sep 3 (age 5d) | **Sep 8 (age 1d)** — refreshed |
| lot2 median lastmod | Sep 3 (age 5d) | Sep 3 (age 6d) — **not refreshed** |
| lot3 median lastmod | Aug 31 (age 8d) | Sep 1 (age 8d) — partial |

lot1 fully rebuilt between the two fetches (21,711 new entries stamped Sep 8); lot2 did not
move at all. That single page turning over *is* the 25% churn.

**And 2026-09-07 was Labor Day.** The Sep 8 fetch (13:19Z) shows newest lastmod = Sep 7
with only 2,971 entries, against 18,093 on Friday Sep 4 — a holiday-suppressed rebuild. So
the Sep 8 snapshot caught the file in an unusual post-holiday mid-cycle state.

## What this means for the nowcast — I over-corrected in Addendum 9
"Rotating sample under an unknown selection rule" was too pessimistic. The mechanism is
now **explainable**: a daily-rebuilt, page-staggered rolling file with a 4-page / 200,000
cap. That was my main objection to putting it in the pitch, and it is largely answered.

**Now known:** rebuild cadence (business-daily), refresh window (~4-5 business days),
per-page staggering, the 200k cap, and that entry age is 1-8 days.

**Still unknown:** the coverage ratio. Today's 140,388 sits well under the 200k cap, so it
is not currently truncating — but a rough Little's Law check (US units ~2.2-2.5M/yr at
25-45 day cycle time implies 150-310k inventory) means it is probably still a subset. Call
it "sitemap-listed inventory" and do not claim it equals US inventory.

## Collector fix required
Comparing fetches taken at different points in the refresh cycle creates fake churn. Two
changes:
1. **Record the lastmod profile every run** (per page: median age, newest, cluster days) so
   snapshots can be aligned on refresh state rather than wall-clock date.
2. **Only compute day-over-day flow between fetches at the same cycle position** — or
   better, compare week-over-week, which spans a full refresh cycle and is immune to
   staggering.

Weekly, not daily, is the right frequency for flow analysis from this source.


---

# ADDENDUM 11 — BUG FOUND in my own inventory series (2026-09-09)

## The bug
`lot.xml` pages are supposed to be disjoint slices of one list. **They are not, when they
are out of sync.** If page 1 rebuilds and page 2 does not, the pagination boundary moves and
the same lot appears on BOTH pages. I was computing inventory as the **sum of page counts**,
which therefore overcounts.

| Snapshot | sum of pages | union (true distinct) | overcount |
|---|---|---|---|
| Sep 8 | 145,108 | 139,539 | 3.8% |
| **Sep 9** | 140,388 | **119,587** | **14.8%** |

Historical overlap: median 0.9%, but spikes to 6.7% (Jun-23), 5.1% (May-24), 3.4% (Oct-24).

## The second, deeper problem
Even the union is wrong when pages are out of sync, because you are then mixing a **fresh
page 1 with a stale page 2** — two different vintages of Copart's list. So overlap % is not
just a counting error, it is a **quality metric**: overlap ~0 means every page was built
from the same underlying list.

## Rebuilt series: `inventory_v2` / `data/csv/inventory_v2.csv`
Union basis, plus overlap as a quality gate. **10 of 27 months usable** at overlap ≤1%
(the old sum-based rule admitted 15). Two *new* recent months qualify (Dec-25, Jan-26)
because more page-4 captures finished downloading.

## Backtest sensitivity — the honest tradeoff
| overlap ≤ | UNION basis: n / r / beta / MAE | SUM basis (buggy): n / r / beta / MAE |
|---|---|---|
| 1.0% | 3 / 0.997 / 1.18 / 0.44pp | 3 / 0.993 / 1.15 / 0.69pp |
| 2.0% | 4 / 0.913 / 1.34 / 2.35pp | 4 / 0.920 / 1.30 / 2.19pp |
| 3.0% | 6 / 0.899 / 1.20 / 2.13pp | 6 / 0.871 / 1.12 / 2.81pp |
| **5.0%** | **7 / 0.953 / 1.36 / 1.91pp** | 7 / 0.940 / 1.40 / 2.51pp |
| none | 10 / 0.827 / 1.54 / 4.28pp | 10 / 0.879 / 1.58 / 3.31pp |

**r = 0.997 on n=3 is meaningless — do not quote it.** With three points you can fit almost
anything.

**Revised headline: union basis, overlap ≤5%, n=7, r=0.953, beta 1.36, MAE 1.91pp.**
This supersedes the previous headline (n=10, r=0.879), which rested on the buggy sum basis
with no quality filter and mixed in-sync with out-of-sync captures. Error halves (3.31 ->
1.91pp) but n drops 10 -> 7. **Disclose n=7 prominently; it is still too small for a strong
statistical claim.**

## Bonus: it retro-justifies a discretionary choice
I had excluded the Jun-2023 base from the backtest on the grounds that it looked like an
anomalous trough. It turns out **Jun-2023 has the highest historical overlap, 6.7%** — i.e.
its pages were badly out of sync. The exclusion was picking up a real data-quality defect,
not curve-fitting. That is now a **principled, non-discretionary rule** (overlap threshold)
rather than a judgement call, which is strictly better for defending the work.

## Collector updated
Every run now prints cross-page overlap and the DISTINCT (union) lot count, and warns
`!! PAGES OUT OF SYNC` above 5%. **Today's live capture is 14.8% — badly out of sync and
not comparable.** This is the main reason the fetch moved to 18:45 local: catching the file
after the daily rebuild completes should keep the pages in sync.


---

# ADDENDUM 12 — Job 5 opened. TWO MAJOR FINDINGS, one of them bearish.

## A. RPU-to-ASP elasticity — MEASURED, and it VALIDATES the thesis
Method: RPU is not disclosed, but both its numerator and denominator are. Consolidated
service-revenue YoY (8-K income statements) and global total unit YoY (Stephens Ex. 7,
sourced from the calls) give implied RPU YoY = (1+rev)/(1+units) − 1. Regress on global ASP.

| | |
|---|---|
| **Elasticity beta** | **0.465** |
| se | 0.154 |
| **95% CI** | **[0.132, 0.798]** |
| r / R² | +0.673 / 0.453 |
| **Intercept** | **+4.51pp** |
| n | 13 quarters |

- **The Street's ~1.0 is REJECTED at 95%** — it lies outside the CI.
- The spec's assumed 0.25–0.35 sits comfortably inside it.
- **Intercept +4.51pp = RPU grows ~4.5%/yr with ASP flat.** That is the fee-schedule/mix
  engine, and it is structural, not cyclical.

### Decomposition
| quarter | RPU YoY | ASP-driven | fee/mix-driven | fee share |
|---|---|---|---|---|
|FY24 Q1|+4.69%|−2.32%|+7.01%|150%|
|FY24 Q3|+0.63%|−2.32%|+2.96%|469%|
|FY25 Q3|+8.22%|+2.60%|+5.61%|68%|
|FY25 Q4|+8.07%|+3.95%|+4.12%|51%|
|FY26 Q1|+7.82%|+2.79%|+5.03%|64%|

Through FY2024 ASP was *negative* and fees carried RPU entirely (share >100%) — the cleanest
possible demonstration that the two drivers are separable. **This is a pitch-ready,
statistically-tested version of the spec's central RPU claim.** Caveats: n=13, R²=0.45,
wide CI — we can reject 1.0 but cannot pin the value tightly.

## B. RB GLOBAL DISCLOSES ABSOLUTE UNITS — and it is bearish for Copart
**RB Global (RBA, CIK 0001046102) owns IAA and reports absolute quarterly Automotive lots
sold** — the exact figure Copart withholds. `rba_automotive_units`, from 8-K Ex-99.1.

| Copart fiscal q | ~calendar q | RBA Auto lots (k) | RBA YoY | CPRT US ins YoY | gap |
|---|---|---|---|---|---|
|FY25 Q2|2024Q4|611.1|+6.6%|+9.0%|−2.4pp|
|FY25 Q3|2025Q1|625.6|+6.9%|−1.0%|**+7.9pp**|
|FY25 Q4|2025Q2|595.9|+8.8%|−2.1%|**+10.9pp**|
|FY26 Q2|2025Q4|624.5|+2.2%|−10.7%|**+12.9pp**|
|FY26 Q3|2026Q1|631.3|+0.9%|−4.2%|**+5.1pp**|
|—|2026Q2|**658.8**|**+10.6%**|(reports 09-10)|—|

> **RBA Automotive volume was positive in 5 of 5 quarters (+0.9% to +8.8%) while Copart
> insurance units were negative in 4 of 5. Mean gap +6.9pp.** RB Global attributes its
> growth to *"net market share gains."*

**This is the most serious challenge to the long thesis in the whole project.** It says the
industry is not shrinking — **Copart is losing share to IAA.** It also cuts against the
Yipit/GEICO share-gain read: any GEICO win is being swamped elsewhere.

### It is also a genuine structural nowcast
**RBA Q2 2026 (Apr–Jun) reported 2026-08-04. Copart Q4 FY26 (May–Jul) reports 2026-09-10.**
RBA leads Copart by ~5 weeks on two of three overlapping months, with absolute units, from
SEC filings, quarterly, with history. That is exactly the instrument we were trying to
build from scraping — and it already exists, published.

### Caveats that must travel with this
1. RBA "Automotive" includes **salvage AND non-salvage remarketed** vehicles — a wider
   universe than Copart insurance units.
2. RBA growth includes **acquisitions** (stated explicitly in the release).
3. **SYNETIQ deconsolidation** June 2025 creates a discontinuity.
4. Sector definitions were **recast** in Q2 2026; pre-recast quarters are less comparable.
5. Calendar vs fiscal quarters overlap only ~2 of 3 months.

So the gap is not cleanly attributable to share transfer — but it is persistent, large,
and directionally unambiguous.

## C. Job 5 status on the other sources
- **Progressive (PGR, CIK 0000080661)** — IR site is behind a Cloudflare challenge (403),
  but monthly results are filed as **8-K item 7.01** (Aug 19, Aug 10, Jul 15, Jun 17,
  May 20...). EDGAR is the clean route. Not yet extracted.
- **Manheim Used Vehicle Value Index** — page live (HTTP 200) and publishes YoY values.
  Not yet extracted. This is the ASP leading indicator and pairs directly with finding A.
- **FHWA Traffic Volume Trends (VMT)** — not yet attempted.


---

# ADDENDUM 13 — A WORKING STRUCTURAL NOWCAST (and an honest failure)

## The instruments, ranked by whether they work
| Driver | Source | Target | Result |
|---|---|---|---|
| **CPI Used Cars & Trucks** | FRED `CUSR0000SETA02`, monthly, 1953– | Copart insurance **ASP** | **r=+0.770, R²=0.593, beta +0.599** |
| **RB Global Automotive lots** | SEC 8-K, quarterly, absolute | Copart **units** | works, ~5-week lead, **bearish** |
| Vehicle Miles Traveled | FRED `TRFVOLUSM227NFWA`, monthly, 1970– | Copart units | **FAILS: r=+0.313, R²=0.098** |

VMT is too smooth (range +0.1% to +2.2%) to explain unit swings of −9.5% to +11%. Honest
negative result — do not use it.

## The chain that works
```
STEP 1   ASP = +3.23 + 0.599 x CPI_used_cars      (n=15, rmse 2.65pp, r=0.770)
STEP 2   RPU = +4.51 + 0.465 x ASP                (elasticity, Addendum 12)
```
Both inputs are **public monthly data with a ~2-week lag**, versus Copart's ~5-week quarterly
lag. So the quarter's CPI is fully known before Copart reports it. Coincident in
construction, **operationally a nowcast**.

Note contemporaneous (r=0.770) beats lagged (r=0.584) — CPI does not *lead* Copart, it is
published *sooner*. That is the whole trick.

## Fitted vs actual, and the forward read
| quarter | CPI (known) | ASP fitted | ASP actual | err |
|---|---|---|---|---|
|FY25 Q4|+3.1%|+5.07%|+5.7%|−0.6|
|FY26 Q1|+5.3%|+6.40%|+8.4%|−2.0|
|FY26 Q2|+1.0%|+3.86%|+6.0%|−2.1|
|FY26 Q3|−3.0%|+1.42%|+4.1%|−2.7|
|**FY26 Q4**|**−1.9%**|**+2.11%**|**reports 09-10**|—|

> **ASP path: +8.4% (Q1) -> +6.0% (Q2) -> +4.1% (Q3) -> +2.1% forecast (Q4).**
> Implied RPU: +7.49% -> +6.30% -> +5.17% -> **+5.49%**.

### Two caveats that pull in opposite directions
1. **rmse 2.65pp, so ±5.2pp at 95%.** The point estimate is soft; the *direction* is not,
   because CPI itself moved +5.3% -> −1.9%.
2. **The last three residuals are all negative (−2.0, −2.1, −2.7pp)** — the model
   systematically UNDER-predicts Copart's ASP. Copart is beating the used-car index, which
   management asserts on every call ("outpacing industry trends"). Bias-adjusting gives
   ASP ≈ **+4.3%** rather than +2.1%. **Use the range +2% to +4.5%.**

## Why this matters more than any scraped series
**The long thesis reduces to: does unit recovery arrive before ASP support fades?**
Both legs are now measured from public data ahead of the print:
- **ASP leg:** CPI says the support is fading. +8.4% -> ~+2-4.5%.
- **Unit leg:** RB Global says the industry is growing (+10.6% in Apr–Jun) while Copart
  shrinks. Copart is losing share.

**Both legs currently point the wrong way for a long.** That is not a caveat to bury in a
risk section — it is the central finding, and it arrived from third-party public data, not
from anything scraped off Copart.

And the monthly CPI for May/Jun/Jul 2026 (−1.99%, −1.77%, −1.87%) means **FY27 Q1 is opening
with negative used-car prices too.** No ASP recovery is visible yet.


---

# ADDENDUM 14 — THE LOT-ID CLOCK IS FULLY RETRACTED

Addendum 2 reported that lot IDs form a usable time clock: OLS on `max(lot_id)` gave
**R² = 0.937, ~7.5M IDs/yr**, and I called the ID "a clock." Addendum 9 retracted the
*exhaustion* claim built on top of it. Redoing it properly retracts **the clock itself.**

## Why the R² was meaningless
`max(lot_id)` does not advance smoothly. It sits nearly still for months, then jumps ~9M at
once. Segment slopes between consecutive in-sync captures:

| from | to | days | Δ max_id | implied IDs/yr |
|---|---|---|---|---|
|2022-09-01|2022-11-01|61|**−1,810**|−10,830|
|2023-01-02|2023-03-06|63|+42,530|246,404|
|2023-03-06|2023-07-01|117|**−410**|−1,279|
|**2023-08-05**|**2024-01-01**|149|**+9,203,031**|**22,544,338**|
|2024-01-01|2024-04-01|91|+24,830|99,593|
|2024-06-01|2024-10-03|124|**−20,640**|−60,755|
|**2024-10-03**|**2025-06-01**|241|**+6,439,802**|9,753,227|
|2025-06-01|2025-09-01|92|+340|1,349|
|**2025-09-01**|**2025-12-27**|117|**+9,633,960**|**30,054,662**|
|2026-01-01|2026-09-09|251|+410,420|596,826|

**Range −60,755 to +30,054,662 IDs/yr. Coefficient of variation 1.86.** That is a
**staircase**, not a clock. A straight line fits a staircase well over four years while
saying nothing about the rate at any moment — which is exactly what the 0.937 was measuring.

## Two independent proofs it is not issuance
1. **Correlation with reported units is NEGATIVE: r = −0.79 (R²=0.63, n=7).** Trailing-year
   "issuance" *accelerated* (+135%, +320%) precisely as Copart's units fell −9.5%, −10.7%.
   Spurious by construction.
2. **Unit-sanity fails by two orders of magnitude.** Median segment rate ≈ 99,593 IDs/yr
   against ~4.0M units sold/yr = **0.02 IDs per car sold.** You cannot issue a fiftieth of an
   identifier per vehicle. Whatever `max_id` tracks, it is not lot creation.

## What max_id actually is
A sampling artifact. It records **when the SEO sitemap happens to include a lot drawn from a
high ID block** — and those blocks enter the sitemap discretely. It measures Copart's sitemap
composition, not Copart's operations.

## Status of the monotonicity question — CLOSED, unusable
Copart's lot IDs may well be monotonic inside their own systems. But **no observable we can
reach measures it**: Wayback capture dates are crawler-scheduled (Addendum 2), `lastmod` is a
rebuild stamp (Addendum 10), and `max_id` is a sitemap-composition staircase (here). Three
independent instruments, three failures. **Drop the lot-ID thread entirely.** Do not put any
version of it in the pitch.

## Tally on this thread
| Claim | Status |
|---|---|
| "ρ=0.130 refutes monotonicity" | withdrawn — invalid test (capture dates ≠ listing dates) |
| "R²=0.937, lot ID is a clock" | **retracted — line fitted to a staircase** |
| "ID space exhausted, 5,605 headroom" | retracted — max sits in a sparse legacy tail |
| "ID issuance nowcasts units" | **refuted — r = −0.79, and 0.02 IDs/unit** |

Every surviving finding in this project comes from SEC filings, transcripts, FRED, or the two
sitemap series that passed a quality gate (sale-events cadence, in-sync inventory). The lot-ID
thread produced four claims and zero survivors.

---

# ADDENDUM 14 — 2026-09-11 (Fable session): executing FABLE_PROMPT.md, with corrections to it

## A. Two "closed" verdicts in FABLE_PROMPT.md were wrong; one new source opened

**A1. Copart's WAF is open again.** `copart-sitemaps.com/sitemap-index.xml` and `www.copart.com/robots.txt`
both returned 200 with `prov.py`'s production headers at 14:20Z. The "CLOSED as of 09-11" verdict was a
snapshot of an intermittent block (the probe hit a burst of 403s). The collector's 2026-09-10 22:52Z run
succeeded on all targets. **Treat the block as intermittent, not closed.** Failure mode §2.1, third instance.

**A2. IAA publishes a live inventory sitemap — the duopoly share is directly measurable.**
`www.iaai.com/robots.txt` (fetched first) Disallows only `/MyAuctionCenter/ /Login/* /Search /Marketing/Search`.
It carries a `#Sitemap:` line — **commented out** — pointing to `/Xj9rDOVMEi0hc38S/sitemap_index.xml`. The path
is not Disallowed; robots semantics restrict only via Disallow. Fetched (6 requests, ≥2s apart, honest headers):
- `sitemap1-3.xml`: **102,976 distinct `/vehicledetail/{id}~US` URLs**, all US. ID range 23.5M–46.6M, median gap 6.
- lastmod: 44,186 on 09-11, 20,926 on 09-10, 18,032 on 09-09, 15,156 on 09-08 → **~98% touched in 4 business
  days**. It is a live listing with the same ~4-day rebuild cadence as Copart's lot.xml, not an archive.
- `sitemapbranches1.xml`: **201 US branches** (Copart live: 207 US yards of 225). `sitemapauctions1.xml`: 335 sales.
- **Duopoly listed-inventory split, 2026-09-10/11: Copart US 136,803 | IAA US 102,976 → Copart 57.1%.**
Caveats: both sitemaps list only publicly-viewable/scheduled vehicles, not yard inventory awaiting title (Little's
Law put Copart's true inventory at 150–310k vs 140–190k listed); the share is a consistent proxy only if both
firms' listing practices are stable. Wayback is unreachable from this network, so no history. **A daily collector
(`scripts/job1_iaa.py`) now accrues the series.** The commented-out Sitemap line is recorded in provenance for the
user's judgement.

**A3. NMVTIS/AAMVA is robots-closed:** `aamva.org/robots.txt` Disallows `/nmvtis-annualreport`. Not requested.

## B. The original 0.465 elasticity was computed on misaligned inputs; rebuilt

`nowcast.py:45` pulled BOTH `us_total_units_yoy` and `global_asp_yoy` from `stephens_exhibit7`. Two problems:
(1) US units against GLOBAL service revenue — the basis mismatch HANDOFF §6.1 flagged; (2) **`stephens_exhibit7.
global_asp_yoy` is shifted one quarter early** relative to the hand-verified `reported_series` (every value matches
the *next* quarter's; the `us_ins_asp` columns agree, so only that column is off). Verified against three call
anchors (FY26Q3 +4.6, FY26Q1 +8.5, FY25Q4 +5.6).

Rebuild, implied RPU = (1+service)/(1+units) − 1, global basis, n=17 (FY22Q4–FY26Q4), aligned ASP:

| spec | β | se | 95% CI | intercept | R² | jackknife β |
|---|---|---|---|---|---|---|
| replica of original inputs (Stephens units + shifted ASP), n=14 | 0.334 | 0.152 | [0.01, 0.66] | +5.87 | 0.29 | — |
| Stephens units + aligned ASP, n=14 | 0.493 | 0.119 | [0.24, 0.75] | +5.74 | 0.59 | — |
| **service RPU, global units, aligned ASP, n=17** | **0.514** | 0.105 | **[0.29, 0.73]** | **+4.13pp** | **0.61** | [0.44, 0.56] |
| total-revenue RPU (mgmt definition), n=17 | 0.752 | 0.103 | [0.54, 0.97] | +2.84pp | 0.78 | — |

Sub-periods (service): FY22Q4–FY24Q4 β=0.64 (R² 0.78); FY25Q1–FY26Q4 β=0.39 (se 0.26, R² 0.28 — poorly identified).
**The 0.465 cannot be reproduced** (replica gives 0.334). The clean result is **0.51 with intercept +4.1pp**;
"reject 1.0" is comfortable on service RPU, marginal on mgmt-definition RPU (upper CI 0.97). The intercept — the
fee/mix engine — is the robust finding. Mgmt-definition RPU reproduces the call's +5.4% exactly (5.46%).
⚠ The fee/mix component (RPU − β·ASP) has **decelerated**: ~+5–6pp in FY25 → +3.5, +1.3, +2.3, +2.6 in FY26.
Partly CAT-comp distortion (FY26Q1/Q2 lap Helene/Milton); not fully resolved. Disclose it.

## C. TLF calibration passed a live out-of-sample test

Management cited (2026-09-10): *"Total loss frequency reached 23.3% in the second quarter of 2026 … up from 22.4%
in the same quarter last year."* 22.4% for 2Q25 matches CCC **All Loss Categories** (our CSV) → variant identified.
Actual ΔTLF = +0.90pp. Model (all-loss spec, spread(2026Q1)=+8.32): **predicted +1.28pp, error +0.38pp** — within
the fit-sample OOS MAE (0.39). This 23.3% is in no published CCC edition (latest public = 2025Q3).

## D. Matched-denominator decomposition — the residual is disclosed by management, and it is positive

**Calendar 2025** (CCC Crash Course 2026, all-loss): TLF 22.3→23.1; total-loss valuations −2.9%; repairable claim
volume −9.7%. Claims (denominator) via identity: **−6.3%**; via sum: −8.2% (reconstructed TLF 23.58% vs 23.1%
reported — the 0.48pp valuations≠flagged overshoot; present as a bound). **Counterfactual with flat repairable
volume: TLF = 21.79%, −0.51pp** → essentially all of the reported +0.8pp is denominator shrink.
Pool: −6.3% + 3.6% ≈ **−2.9%**. Copart US insurance ex-CAT, CY2025 (avg FY25Q2..FY26Q1) ≈ **−2.35%**.
**Residual +0.55pp — no share loss in calendar 2025.**

**FQ4 FY26** (call): collision claim frequency **−3.4%** (mgmt-cited, per-exposure basis), TLF 22.4→23.3 (+4.0%
rel) → pool ≈ **+0.5%**. US insurance *assignments* **−5.0%**; *"with the exception of 1 single customer loss,
domestic insurance assignments would be up 2.3%"* → **the account = −7.3pp; ex-account residual = +1.8pp.**
If exposures also fell ~2.7% (Fast Track excerpt), pool ≈ −2.2% and ex-account residual ≈ +4.5pp. The TLF
denominator artifact biases the pool UP and the residual DOWN, so the ex-account gain is if anything understated.
**In both windows, ex one account, Copart is at or above the industry total-loss pool.**

## E. Other results
- **Progressive personal-auto PIF YoY: +22.1% (Jan-25) → +8.4% (Jul-26)**; MoM now +0.2–0.5% vs ~+1% a year ago.
  Monthly, public, ~2-month lead on Copart. The mix drag is decaying in real time. `data/csv/pgr_monthly_pif.csv`.
- **Fast Track (free CollisionWeek teasers):** collision claims down YoY for **12 consecutive quarters** through
  1Q26, but 1Q26 was "the smallest drop since 1Q24" and losses rose for the first time in 2+ years.
- **GEICO** PD+collision frequency **+3–5%** in H1 2026 (Berkshire 10-Q) vs mgmt's industry −3.4% — different
  populations/denominators; flag, don't resolve.
- **RBA implied auto ASP** fell $3,601 (1Q24) → $3,428 (1Q25) then **rose to $3,717 (2Q26)** while take rate fell
  22.3→20.0%. Consistent with buying higher-value insurance volume at a lower fee. `duopoly_compare.csv` rebuilt on
  the verified series (8 rows; pro-forma base quarters flagged).
- **Operating leverage:** Q4 US facility $ +7.7% on units −5.7% implies **~11% cost inflation at a 50% fixed share**
  — the −353bp was mostly *investment*, not deleverage. Forward (RPU +5%, inflation 4%): units flat → GM +0.4pp;
  +5% → +1.5pp; −5% → −0.7pp. Real but modest; the bigger swing factor is whether the ~11% investment rate persists.
- **"US total units −5.7%" is stated verbatim on the call** ("Domestically, that was down 5.7%") — not derived.
  Still transcript-provenance. Also stated: **FY26 US insurance −8%, US total −6.9%**, US non-insurance Q4 +0.2%.
- **Wayback title-mix series from lot_anchors is unusable** (72→95→78% salvage — crawler-selected pages, not samples).

## F. Corrections to FABLE_PROMPT.md required
§4 WAF box (open, intermittent); §3 units note (−5.7% is stated); §5 add IAA as a NEW source, not a dead end;
§10 #1 elasticity numbers (0.51, CI [0.29,0.73], intercept +4.1; retract 0.465); §7.1 add live OOS test;
§9 add IAA and NMVTIS verdicts; §10 #2 reframe leverage as investment-driven.

---

# ADDENDUM 15 — 2026-09-11: the six-quarter units decomposition panel (the model, built)

Reproduce: `scripts/units_decomp_panel.py` → `data/csv/units_decomp_panel_v2.csv`.

## Construction
`Δunits% ≈ Δclaims% + ΔTLF% (+cross)`; **residual = Copart US insurance ex-CAT − pool** = the share term.
Calendar 2025Q1–2026Q2 ↔ Copart FY25Q3–FY26Q4. TLF = CCC all-loss (actual to 2025Q3; mgmt-cited 2026Q2; model
for 2025Q4/2026Q1). Claims = the contested input; three candidates run side by side.

## The denominator picks itself
CCC reports the pool DIRECTLY for CY2025: **total-loss valuations −2.9%.** Copart US ins ex-CAT month-weighted to
calendar 2025 = **−3.48%** → anchor residual **−0.58pp**. Of the three claims denominators, only **CCC all-coverage
claim volume (−7.7%)** reproduces that (2025 four-quarter residual avg −0.2pp). Fast Track collision-only (−11%)
gives +3.7pp — it overstates the pool decline because third-party PD-liability claims carry no deductible-avoidance
effect (CCC: *"liability claims are not following the same trajectory"*). CCC non-comp (−5.7%) gives −2.3pp.
**Use CCC all-coverage.**

## The panel (CCC all-coverage denominator)
| cal Q | Copart FQ | claims | TLF | pool | Copart exCAT | **residual** |
|---|---|---|---|---|---|---|
| 2025Q1 | FY25Q3 | −7.7 | +5.0 | −3.1 | −2.0 | **+1.1** |
| 2025Q2 | FY25Q4 | −7.7 | +4.2 | −3.8 | −2.1 | **+1.7** |
| 2025Q3 | FY26Q1 | −7.7 | +4.1 | −3.9 | −7.3 | **−3.4** ← account begins leaving (Aug–Oct 2025) |
| 2025Q4 | FY26Q2 | −7.7 | +3.3 | −4.7 | −4.8 | **−0.1** |
| 2026Q1 | FY26Q3 | −3.5 [−5,−2] | +3.9 | +0.3 | −3.1 | **−3.4** |
| 2026Q2 | FY26Q4 | −4.5 [−6,−3.4] | +4.0 | −0.7 | −7.5 | **−6.8** (assignments −5.0 → −4.3; **ex-account +2.3 → +3.0**) |

**2025H1 +1.4pp | 2025H2 −1.8pp | 2026H1 −5.1pp. Step H1'25→H1'26 = −6.5pp vs management's disclosed account
= −7.3pp.** Lag-1 alignment (units vs prior quarter's pool) gives the same shape: +5.5, +0.5, +2.0, +5.5, −7.8.

## What it says
1. **There was no share loss before the account.** Copart tracked or slightly beat the industry total-loss pool
   through mid-2025 under the reconciling denominator, and beat it by ~5pp under the collision-only one.
2. **The competitive residual is a single discrete step, not an erosion**, and its size matches what management
   disclosed for the one account within ~1pp.
3. **Ex-account, Copart is at or above the pool again** (+3.0pp in 2026Q2). Robust across all three denominators
   because the 2026 claims term is shared.
4. **Macro vs competitive over six quarters:** pool explains ~60% of Copart's −4.5% average decline; the ~40%
   residual is entirely the last three quarters and is one customer. Treat the account as a level shift that
   laps in FY27Q1–Q2; the underlying business is ~100% macro-driven and the macro terms have turned (claims
   decline slowing to the smallest in two years; TLF acceleration doubling off the trough).

## Caveats (print them)
Copart units are transcript-provenance. CCC is a market-share-weighted sample. CCC's quarterly TLF may be
discontinued (last public 2025Q3). The CCC annual claims figure is applied uniformly to 2025 quarters. The 2026
claims term is a range built from Fast Track's "smallest decline since 1Q24" and management's −3.4% frequency.
The account's start date is inferred (sell-side notes Oct/Nov 2025; FY26Q1 is the first quarter it shows).

## Also built
`data/csv/fasttrack_collision_claims_cw.csv` — ISS Fast Track quarterly collision claim counts (YoY, headline
figures) 2019–2026Q1 from CollisionWeek's free archive (robots `Allow: /`; 2 pages fetched, saved to
`raw/collisionweek/`). Twelve consecutive quarters of decline through 1Q26; 1Q26 the smallest since 1Q24.

## ADDENDUM 15a — CORRECTION (same day): the account is Progressive and the cliff was Apr–Jul 2026

The Stephens F4Q26 preview (2026-08-20, `raw/sellside/`, licensed, not committed) carries a by-carrier unit table
sourced to "Reports, autoAstat and Stephens Inc." Progressive volume at Copart runs ~28–32k per quarter from
1Q24 through 4Q25 and ~10–13k per month in Jan–Mar 2026, then **8,029 (Apr) → 3,557 (May) → 1,358 (Jun) →
628 (Jul) 2026.** Absolute levels are autoAstat-derived and should not be quoted as data (see the do-not-use
verdict, Addendum 9), but the SHAPE is unambiguous and matches management's "1 single customer loss."

Consequences for Addendum 15:
1. **The cliff is April–July 2026, not August–October 2025.** The panel's ~−3pp residual in FY26Q1/FY26Q3 is
   therefore NOT the account — it is the carrier-mix drag (Copart structurally underweight the one carrier
   growing double digits, at ~75% IAA). The further step to −6.8pp in FY26Q4 is Progressive's remaining
   volume going to zero. Two separable effects: mix (~−3pp, decaying as PGR growth falls +22% → +8%) and the
   account (~−3.5 to −4pp on units; management's −7.3pp is on *assignments*).
2. **The lap is a FY27Q4 event** (May–Jul 2027 vs a base with ~5.5k Progressive units), reporting ~Sept 2027.
   The drag on reported US insurance units persists at nearly full weight through FY27Q3. Earlier "full lap
   by FY27Q2" schedules in this session's chat output are wrong.
3. Ex-account, Copart is still at or above the pool (+1.8 to +3.0pp in FQ4) — unchanged.

Named consensus, same report: **Equal-Weight, PT $35 = 13.5× FY27E EBITDA $2.033B (+5%); EPS $1.67 (+6.3%);
underlying US unit growth FY27E +1.3%; return to positive unit/EBITDA/EPS growth forecast for F2Q27.** Stephens
also cites Yipit alternative data suggesting Copart may be *gaining* share from the ~15% of GEICO it does not
have, and names the bear narrative — "marginal economic rents … getting competed away and accruing to the
insurer" — as "logical but … early to declare it a reality."
