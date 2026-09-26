# data/csv — every committed dataset, what it is, and whether to trust it

**Status key:** LIVE = written by the nightly collectors · RAW = extracted or hand-transcribed from a source, provenance
in `PROVENANCE.md` or the file's `#` header · ANALYSIS = produced by a script in `scripts/`, re-runnable · DEAD-END =
kept as the record of something that did not work · LEGACY = superseded, kept for traceability.

Trust tiers (from `README.md`): SEC filings > transcripts (hand-transcribed) > sitemap-derived > regressions on any of them.
Every file with a `#` header carries its own provenance; the ones without are described here.

## Mechanism A — fleet ageing and the age curves (`scripts/age_curves.py`, `docs/AGE_CURVES.md`)

| File | Status | What it is | Caveat |
|---|---|---|---|
| `ornl_tedb40_survival_by_age.csv` | RAW | EPA survival rates by age, cars and light trucks (EPA-420-D-16-900, 2016) via ORNL TEDB Ed.40 Table 3.15 | verbatim |
| `ornl_tedb40_miles_by_age.csv` | RAW | EPA annual miles per vehicle by age, ORNL Table 3.14 | used only to decompose R after the fit |
| `ornl_tedb40_new_sales.csv` | RAW | Ward's new retail vehicle sales 1970–2021, ORNL Table 3.6 | thousands; Ward's reports to the unit, hence decimals |
| `fred_TOTALNSA.csv`, `fred_LTRUCKNSA.csv`, `fred_HTRUCKSNSA.csv` | RAW | BEA light-vehicle, light-truck and heavy-truck sales, monthly NSA (FRED) | BEA definitions differ from Ward's; spliced on the 2021 overlap |
| `light_vehicle_sales_by_year.csv` | ANALYSIS | Cohort sizes 1970–2025 on Ward's basis (2022–25 from FRED, rescaled) | heavy trucks are outside the light-vehicle roll |
| `age_curves.csv` | ANALYSIS | S, miles, R, P by age; 2024 fleet, claims and total-loss shares. The header carries the fitted parameters the workbook reads | R and P are FITTED, not measured |
| `age_curves_validation.csv` | ANALYSIS | Every fit target, out-of-sample check, survival check and sensitivity row | targets are CCC statements, quoted |

The IHS-sourced ORNL tables (3.11, 3.12, 3.13 — census by age, average age) are **not committed**: the sheets say
"further reproduction prohibited." Extracts live in `raw/ornl/tedb40/extracts/` (gitignored) and are cited by table number.

## Total-loss frequency and the totaling spread (`scripts/analysis_20260911.py`)

| File | Status | What it is | Caveat |
|---|---|---|---|
| `ccc_tlf_annual.csv` | RAW | CCC total-loss share of claims, CY2013–2025, two variants; data labels read off the published chart | edition-year ≠ data-year; revises ~0.1pp between editions |
| `ccc_tlf_quarterly.csv` | RAW | Same, quarterly 2018Q1–2025Q3 | series may be discontinued after 2025Q3 |
| `cprt_cpi_three_series.csv` | RAW | BLS CPI used cars, vehicle repair, vehicle insurance; SA and NSA; YoY; footnote codes | Oct-2025 (repair) and Oct+Nov-2025 (insurance) are BLS gaps, left blank |
| `totaling_spread_quarterly.csv` | ANALYSIS | repair-CPI YoY − used-car-CPI YoY, quarterly mean | `months < 3` rows are partial quarters |
| `tlf_calibration.csv` | ANALYSIS | ΔTLF = a + b·spread(t−1): a, b, se, R², residual autocorrelation, effective n, OOS MAE | effective n ≈ 6 on the non-comp variant |
| `recovery_divergence_quarterly.csv` | ANALYSIS | Copart insurance ASP YoY − used-car CPI YoY by quarter with ΔTLF and spread; the salvage-recovery check (`scripts/recovery_divergence_check.py`) | n = 11 overlap; negative result, see Addendum 18 |
| `cpi_insurance_repair_yoy.csv` | LEGACY | Earlier two-series CPI extract (2021–2026) | superseded by `cprt_cpi_three_series.csv` |

## Copart reported series and the units decomposition

| File | Status | What it is | Caveat |
|---|---|---|---|
| `reported_units.csv` | RAW | Quarterly US inventory, US insurance units (incl./ex-CAT), US insurance ASP, global ASP, global insurance units YoY — **hand-transcribed from earnings calls** (`scripts/reported_series.py`) | Tier 2; no filing discloses these |
| `stephens_exhibit7.csv` | RAW | Numeric exhibit from a sell-side preview, transcribed for corroboration (15/15 match) | its global-ASP column is shifted one quarter — **never regress on it** |
| `quarterly_pl.csv`, `quarterly_margin.csv`, `quarterly_segments.csv`, `segment_service_rev_8k.csv`, `facility_ops_quarterly.csv` | RAW | 8-K Ex-99.1 press-release lines | Tier 1 |
| `sec_annual.csv` | RAW | 10-K XBRL annual figures (`scripts/sec_extract.py`) | Tier 1 |
| `elasticity_rebuild.csv` | ANALYSIS | 17 quarters: service and total revenue YoY, global units and ASP YoY, implied RPU YoY, fee/mix component | the basis-matched inputs behind β = 0.514 |
| `units_decomp_panel_v2.csv` | ANALYSIS | Six-quarter decomposition under three claims denominators; residual = share term | claims term for 2026 is a range |
| `decomposition.csv` | ANALYSIS | CY2025 and FQ4 FY26 matched-denominator windows | |
| `fasttrack_collision_claims_cw.csv` | RAW | ISS Fast Track collision-claim-count headlines via CollisionWeek | headline figures with qualifiers, not levels |
| `pgr_monthly_pif.csv` | RAW | Progressive personal-auto policies in force, monthly 8-K | definition change Dec-2024 noted in file |
| `geico_frequency_series.csv` | RAW | Berkshire filing sentences on GEICO claim frequency | text, banded |
| `rba_automotive_series.csv` | RAW | RB Global automotive lots, GTV, take rate from 8-Ks | 5 of 18 quarters pro forma; includes non-salvage |
| `rba_automotive_units.csv` | LEGACY | First RBA extract (`scripts/rba_units.py`) | superseded by `rba_automotive_series.csv` |
| `duopoly_compare.csv` | ANALYSIS | RBA lots YoY vs Copart US insurance units YoY by matched quarter | industry signal contaminated by share and acquisitions |
| `capex_decomp.csv`, `owner_earnings.csv` | ANALYSIS | Capex by PP&E component; owner-earnings bridge (`scripts/ppe_components.py`, `ppe_land.py`) | land at cost parsed from footnote HTML; use multi-year ratios only |
| `er_boilerplate.csv` | RAW | Units, locations, countries as stated in 10-K boilerplate by filing date | round numbers |

## Scraped series — Copart and IAA sitemaps (Tier 3: listed inventory, not yard inventory)

| File | Status | What it is | Caveat |
|---|---|---|---|
| `duopoly_daily.csv` | LIVE | Nightly Copart US lots vs IAA US vehicles, share, with `iaa_complete`, `copart_overlap_pct`, `usable` | **use `usable = 1` rows only**; share is NULL where IAA was partial |
| `sale_events_live.csv` | LIVE | Every dated sale event per yard per nightly snapshot | the facility-cost series |
| `inventory_v2.csv` | ANALYSIS | Monthly union lot counts from archived captures with overlap % and gates (`scripts/inventory_v2.py`) | only `usable = 1` months are comparable |
| `backtest_inventory_v2.csv` | ANALYSIS | Gated sitemap YoY vs reported US inventory YoY (`scripts/backtest_inventory_v2.py`) | n = 4 gated pairs |
| `lots_per_sale_event.csv` | ANALYSIS | Listed lots ÷ weekly sale events (~700 → 492) | the 745 peak fails the gate |
| `yard_panel_us.csv`, `yard_panel.csv` | ANALYSIS | US yards and dated events per capture (`scripts/yard_analysis.py`, `parse_salelist_sitemaps.py`) | |
| `cadence_fixed.csv` | ANALYSIS | Sale-event cadence per yard (`scripts/cadence_fixed_window.py`) | |
| `sale_events.csv` | ANALYSIS | Historical sale events from archived captures | Wayback capture dates ≠ listing dates |
| `state_panel.csv` | ANALYSIS | Listed lots by state by capture | |
| `inventory_panel.csv`, `lotxml_panel.csv` | ANALYSIS | Per-capture page counts, ID ranges, title mix | inputs to the union/overlap work |
| `lot_snapshots.csv`, `lot_anchors.csv` | gitignored | 2.7M lot-level snapshot rows; 199k archive anchors | in `data/cprt.db`; too large for GitHub |

## Dead ends — kept as the record, do not rebuild a thesis on them

| File | Why it is here |
|---|---|
| `backtest_pairs.csv` | the first back-test, on **summed** page counts (up to 14.8% double-count); superseded by `backtest_inventory_v2.csv` |
| `inventory_level.csv` | the summed series behind that bug |
| `id_clock_v2.csv`, `lotid_monotonicity.csv` | the lot-ID "clock" — four claims, all retracted (`findings.md` Addendum 14) |
| `cycle_time.csv`, `cycle_time_pagematched.csv` | cycle-time from lot survival between captures; page sync makes it unusable at daily frequency |
| `cadence_panel.csv`, `cadence_weekday.csv` | earlier cadence attempts superseded by `cadence_fixed.csv` |
| `tx_auto_rate_filings.csv` | 7,613 Texas auto rate filings — real data, but the state-level rate-vs-inventory test it was for cannot be run (no other state has a free series) |
| `state_yoy_for_rates.csv` | the proxy attempt at that test (r = −0.115) |

If a file is missing from this index it is new; add it here with its status when you commit it.
