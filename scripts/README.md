# scripts/ — what each file does

**Status key:** LIVE = runs nightly · ANALYSIS = reproduces a result in `findings.md` · ONE-OFF = ran once
to build a table in `data/cprt.db` / `data/csv` · DEAD-END = investigated, retracted, kept as the record ·
LEGACY = superseded but historically important.

Every network request goes through `prov.py`. Nothing here authenticates, solves a challenge, or touches a
robots-disallowed path.

## Core

| Script | Status | Purpose |
|---|---|---|
| `prov.py` | LIVE | Provenance-logged, rate-limited fetcher. Per-host headers (SEC wants a descriptive UA; Copart/IAA want a conventional browser set). Retries WAF challenges with backoff; refuses disallowed URLs. |
| `job1_snapshot.py` | LIVE | **Job 1.** Copart daily sitemap snapshot: `sale-list-results.xml` + `lot.xml` pages 1–4. Robots parsed from the saved live file; cross-page overlap as a quality gate; same-day guard v3. |
| `job1_iaa.py` | LIVE | **Job 1b.** IAA daily sitemap snapshot → `duopoly_daily` (Copart vs IAA listed US inventory). Small files first, then the three ~6.8 MB vehicle sitemaps 90 s apart (IAA volume-throttles bursts); never parses a challenge page; records `iaa_complete` / `copart_overlap_pct` / `usable` and publishes a share only when both sides are clean. `--from-dir` loads saved XML. |
| `run_job1.sh` | LIVE | Nightly runner invoked by LaunchAgent `com.cprt.job1` (`com.cprt.job1.plist`, 18:45 local). |
| `reported_series.py` | ONE-OFF | **Hand-transcribed** quarterly unit / inventory / ASP series from 16 earnings calls (authoritative; the regex parser was discarded — see dead-ends). |

## Analysis (reproduce the pitch numbers)

| Script | Status | Purpose |
|---|---|---|
| `analysis_20260911.py` | ANALYSIS | TLF calibration (ΔTLF ~ totaling spread, CCC 2018Q1–2025Q3), the rebuilt RPU/ASP elasticity (n=17, aligned inputs), and the matched-denominator decomposition. Writes `tlf_calibration`, `totaling_spread_quarterly`, `elasticity_rebuild`, `decomposition` CSVs. |
| `backtest_inventory_v2.py` | ANALYSIS | Sitemap inventory YoY vs Copart reported US inventory YoY using UNION counts and the cross-page-overlap quality gate → `backtest_inventory_v2.csv`. Honest summary: r 0.99 on the 4 gated pairs, 0.83 ungated — the gate is the finding, not the r. |
| `recovery_divergence_check.py` | ANALYSIS | Cheap test of the external note's salvage-recovery hypothesis: ASP − used-car CPI divergence by quarter, and whether it adds to the ΔTLF spread regression (it does not on n=11; wrong sign) → `recovery_divergence_quarterly.csv`. findings.md Addendum 18. |
| `units_decomp_panel.py` | ANALYSIS | Six-quarter units decomposition panel under three claims denominators with the CCC direct anchor → `units_decomp_panel_v2.csv`. |
| `build_intermediate_xlsx.py` | LIVE | Builds `model/CPRT_Intermediate.xlsx`: every committed CSV as a Data_* tab (provenance in row 2) plus the formula tabs — Inputs, Survival, Fleet, FleetByAge, Curves, Calibration (Solver), TLF_Roll, Spread_Reg, RPU_Reg, Checks. Parameters are read from the `age_curves.csv` header so the workbook always matches the script. Rebuild after any data update. |
| `verify_intermediate_xlsx.py` | ANALYSIS | Evaluates the workbook’s key formulas with pycel (no LibreOffice here) and compares with the script outputs; RSQ/CORREL recomputed in Python. |
| `blueprint_cohort_tab.py` | LEGACY | Built `model/legacy/blueprint_A_CohortRoll.xlsx`, the first worked example of a model tab. Superseded by `build_intermediate_xlsx.py`; its survival calibration to S&P average age is the artefact explained in `docs/AGE_CURVES.md` §2.3 and its 45.3%-at-13+ anchor is unsourced. Kept as a record. |
| `age_curves.py` | ANALYSIS | Mechanism A age curves. Extracts ORNL TEDB Ed.40 tables (EPA survival, miles by age, IHS fleet census, Ward's sales), calibrates survival to the 2013 census and S&P 2024 counts, fits R(age) and P(age) jointly to eight CCC 2024 claim-mix statistics, tests them out of sample on 2019/2020/2025, and runs the survival sensitivity → `age_curves.csv`, `age_curves_validation.csv`, `light_vehicle_sales_by_year.csv`, `ornl_tedb40_*.csv`. Method: `docs/AGE_CURVES.md`. |
| `nowcast.py` | ANALYSIS | The CPI-used-cars → Copart ASP chain (still valid, r=0.77). ⚠ Its RPU-elasticity section used a misaligned Stephens ASP column and is **superseded** by `analysis_20260911.py`. |
| `rba_units.py` | ONE-OFF | RB Global (IAA parent) absolute quarterly Automotive lots and take rate from 8-K Ex-99.1. |
| `corroborate_stephens.py` | ONE-OFF | Cross-check of the transcript series against the Stephens exhibit (15/15). ⚠ Found later: the exhibit's `global_asp_yoy` column is shifted one quarter; `us_ins_asp` is fine. |
| `backtest_final.py` | ANALYSIS | Sitemap-derived inventory YoY vs reported US inventory YoY, lead-aligned (R² 0.83 lead vs 0.52 same-quarter). |
| `inventory_v2.py` | ANALYSIS | Listed-inventory level with the two fixes: union-not-sum across pages, overlap as a quality filter. |
| `inventory_panel.py` / `lotxml_panel.py` | ONE-OFF | Earlier inventory panels from the Wayback backfill. Superseded by `inventory_v2.py` for levels. |
| `cadence_fixed_window.py` | ANALYSIS | Sale events per week in a fixed 7-day window → cars-per-sale-event (745 → 492). The scraper's one durable pitch metric. |
| `state_panel.py` | ONE-OFF | State-level listed inventory from lot slugs, per complete month. |
| `yard_analysis.py` / `parse_salelist_sitemaps.py` | ONE-OFF | Yard / sale-event panel Aug-2022 → Jan-2026 from archived sale-list sitemaps. |

## SEC extraction

| Script | Status | Purpose |
|---|---|---|
| `sec_extract.py` | ONE-OFF | XBRL companyfacts → annual P&L / capex / D&A series FY2016–FY2025. |
| `ppe_land.py` / `ppe_components.py` | ONE-OFF | **Land at cost** and PP&E components regex-parsed from the 10-K HTML footnote (Land is absent from XBRL). Feeds the owner-earnings / maintenance-capex split. |
| `fetch_10k.py` / `fetch_8k_units.py` | ONE-OFF | Download 10-Ks and 8-K earnings exhibits to `raw/sec/`. |

## Internet Archive backfill

| Script | Status | Purpose |
|---|---|---|
| `cdx.py` | ONE-OFF | CDX index queries for archived Copart sitemaps. |
| `wayback_sitemaps.py` / `wayback_lotxml.py` | ONE-OFF | Fetch archived sale-list and lot.xml captures → the 3.5-year backfill. |
| `lot_anchors.py` | ONE-OFF | (lot_id, capture date) anchor pairs from archived lot pages. |

## `deadends/` — investigated and retracted (kept so nobody re-runs them)

| Script | What it tried | Why it died |
|---|---|---|
| `id_clock_v2.py` | Lot-ID issuance as a unit clock | R²=0.937 was a line fitted to a staircase; correlation with actual units **r = −0.79**; implied 0.02 IDs per car. Four claims, zero survivors. |
| `monotonicity.py` | Test whether lot IDs are monotonic in time | Unmeasurable with any available instrument (Wayback dates are crawler-scheduled; `lastmod` is a rebuild stamp; `max_id` is a composition staircase). |
| `cycle_time.py` / `cycle_time2.py` | Cycle time from lot survival between snapshots | Confounded by page rebuild cadence; Tier-4 derived. |
| `parse_transcripts.py` | Regex extraction of call metrics | 133/176 cells missing, sentences mis-attributed across speakers. Replaced by hand transcription (`reported_series.py`). |
| `wayback_fees.py` / `wayback_lotxml_p45.py` | Archived fee schedule; lot.xml pages 4–5 | Fee pages are robots-disallowed and archived copies are single snapshots; pages 4–5 never existed. |
| `backtest_inventory.py` | First inventory backtest (same-quarter alignment) | Superseded by `backtest_final.py` (lead alignment). |
| `cadence.py` / `cadence_weekday.py` | Earlier cadence definitions | Superseded by `cadence_fixed_window.py`. |

## `legacy/`

| File | Note |
|---|---|
| `copart_snapshot.py` | The **original** standalone collector (2026-09-08). Historically important: it proved Copart's WAF rejected on header shape, not IP or TLS — a fact two later sessions each independently got wrong while this file sat on disk. Disabled; `job1_snapshot.py` replaces it. |
| `com.kendall.cprt-snapshot.plist` | Its LaunchAgent, disabled. The live one is `../com.cprt.job1.plist`. |
