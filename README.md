# CPRT research — Copart, Inc. (NASDAQ: CPRT)

Equity research pipeline for a **long pitch on Copart.** Everything here is built from public,
robots-compliant sources with a logged provenance trail. **Licensed content (transcripts, sell-side)
is gitignored and never committed.**

## Start here

| Read | For |
|---|---|
| **`MODEL_BLUEPRINT.md`** | **The model architecture** — mechanisms A–E, the units identity, the RPU chain, tab map, build order, checks. Open this every time you touch the model. |
| `docs/AGE_CURVES.md` | How the fleet-survival, claim-frequency and total-loss-propensity curves are calculated and what evidence backs each; the manual-pull list. |
| **`HANDOFF.md`** | The current state of the project: what is verified, what was retracted, the thesis, the data sources, the failure modes to avoid. Read §0a and §2 first. |
| `findings.md` | The lab notebook — every result in chronological addenda, **including every retraction**. |
| `PROVENANCE.md` | Every host touched, its robots.txt status, what was fetched, where it is saved. |
| `ARCHITECTURE.md` | How the collector and the sitemap data actually work, and the bugs found the hard way. |
| `scripts/README.md` | One line per script: what it does and whether it is live, analysis, one-off, dead-end, or legacy. |
| `docs/archive/` | Superseded documents, each with a header saying why. |

## The three results that carry the pitch (details and caveats in `HANDOFF.md`)

1. **Total-loss frequency is driven by the totaling spread** (repair CPI − used-car CPI). Calibrated
   on 27 quarters of CCC industry data, not Copart's: β = 0.083 pp of TLF per pp of spread, one-quarter
   lag, R² 0.79, out-of-sample MAE 0.16 pp, and a live hit against a management-cited figure.
   The spread collapsed from +15.7 pp to +2.3 pp through 2025 and has recovered to +8.3 pp.
2. **Revenue per unit is a fee-and-mix engine, not a price pass-through.** Service-RPU elasticity to
   ASP = 0.514 (95% CI 0.29–0.73) with a +4.1 pp intercept, n = 17.
3. **The unit decline is one account, not share erosion.** A six-quarter decomposition of Copart's US
   insurance units into industry claims × total-loss rate × residual shows no share loss before the
   account, a discrete step equal to management's disclosed account impact, and at-or-above-industry
   volume after it, ex-account. Management: *"with the exception of 1 single customer loss, domestic
   insurance assignments would be up 2.3%."*

Plus one dataset nobody else has: **IAA's live inventory sitemap**, giving the duopoly's US
listed-inventory split daily (Copart 57.1% on 2026-09-11).

## Running things

```bash
cd /Users/kwu/cprt
./.venv/bin/python scripts/job1_snapshot.py        # Copart daily sitemap snapshot (Job 1)
./.venv/bin/python scripts/job1_iaa.py             # IAA daily sitemap snapshot (Job 1b) - once per day only
./.venv/bin/python scripts/analysis_20260911.py    # rebuilds TLF calibration, elasticity, decomposition CSVs
./.venv/bin/python scripts/units_decomp_panel.py   # rebuilds the six-quarter units panel
```

Both collectors run nightly via LaunchAgent `com.cprt.job1` (18:45 local, `scripts/com.cprt.job1.plist`
→ `scripts/run_job1.sh`). Logs in `logs/`. Database: `data/cprt.db` (gitignored); exported series in
`data/csv/` (committed).

## Research-ethics rules (non-negotiable; see `HANDOFF.md` §1)

robots.txt first on every host, and obey it · ≥2 s between requests to a host · honest identification
with a contact email on every request · no authentication · no paywall or challenge circumvention ·
report blockers rather than work around them · every dataset's source, method and date logged.

## Trust hierarchy

| Tier | Source | Reliability |
|---|---|---|
| 1 | SEC filings (10-K/10-Q/8-K, XBRL) | very high |
| 2 | Earnings-call transcripts, hand-transcribed | high — cross-checked 15/15 against a sell-side exhibit |
| 3 | Copart / IAA sitemaps (scraped) | medium — listed inventory, not yard inventory |
| 4 | Derived series and regressions | lowest — compounds every upstream error |

Tiers 1–2 produced every result that survived. Tiers 3–4 produced every claim that was retracted.
