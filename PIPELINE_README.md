# CPRT research data pipeline

`./.venv/bin/python scripts/job1_snapshot.py`  — daily snapshot (Job 1). Exit 2 = all
targets failed; exit 1 = partial. Scheduled via LaunchAgent `com.cprt.job1` at 09:17 daily.

| Script | Does |
|---|---|
| `prov.py` | provenance-logged, rate-limited fetcher; refuses robots-disallowed URLs |
| `job1_snapshot.py` | **Job 1** daily sitemap snapshot + profile printout |
| `sec_extract.py` | **Job 4** XBRL annual series FY2016–FY2025 |
| `ppe_land.py` / `ppe_components.py` | **Job 4** Land-at-cost + capex decomposition from 10-K text |
| `cdx.py` / `wayback_sitemaps.py` / `wayback_fees.py` | **Job 3** Internet Archive backfill |
| `lot_anchors.py` / `monotonicity.py` | archived lot-ID anchors + monotonicity test |
| `parse_salelist_sitemaps.py` / `yard_analysis.py` | yard/sale-event panel Aug 2022 → Jan 2026 |

Read `PROVENANCE.md` first — it documents the access posture and the one open robots
question (`/memberFees`). `findings.md` has the results and the caveats.

**Collector:** `com.cprt.job1` (daily 09:17) is the live one. The prior `com.kendall.cprt-snapshot` is disabled (`.plist.disabled`, reversible).
snapshots Copart daily at 06:15. Two collectors are running. Pick one.
