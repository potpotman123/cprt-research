# CPRT research — Copart, Inc. (NASDAQ: CPRT)

Research pipeline behind a **pitch on Copart — long or short, decided by the analyses** (direction opened 2026-09-26; see `HANDOFF.md` §1): public, robots-compliant data with a logged provenance trail,
calibrated mechanisms, and one workbook the model is built from. **Licensed content (transcripts, sell-side, the
reference model) is gitignored and never committed.**

## Start here

**Current research state, published 30 September 2026:** start with [RESEARCH_STATE.md](RESEARCH_STATE.md), the [latest pitch audit](docs/pitch_audit_2026-09-29/README.md), and the [current revenue architecture](model/revenue_architecture_2026-09-28/README.md). The pitch remains intellectually interesting but lacks an established measurable forecast error tied to an observable near-term catalyst. The index below and earlier headline results retain historical context; the current audits govern interpretation. [Publication inventory and local-only exclusions](docs/repository_snapshot_2026-09-30/README.md) specify what a GitHub clone contains.

**Standing research instructions:** read [RESEARCH_PRINCIPLES.md](RESEARCH_PRINCIPLES.md) for end-to-end method explanations, explicit alternatives, broader discovery and cost gates.


| Read | For |
|---|---|
| **`PROMPT_HIGH_REASONING_FABLE_2026-09-30.md`** | **Paste into a fresh high-reasoning session:** the full context, the claim-to-sale engine in 14 steps, the ten unsourced load-bearing assumptions, and a phased assignment — expectations sheet, catalyst scorecard for both theses, decision, model integration. |
| **`NEXT_STEPS_FOR_OTHER_CLAUDE_FABLE.md`** | **For a second Fable session with a fresh budget:** the expensive experiments, each specified end to end (goal, the explanation being tested, steps and why, cost, cheaper alternatives, kill criteria, deliverable). Start here if you were sent this repo to run them. |
| **`HANDOFF.md`** | **The whole project by research thread: what was tried, why, what was found, where it led, what is still open.** Confidence labelled on every result. Read §0–§3 first. |
| **`MODEL_BLUEPRINT.md`** | The model architecture — mechanisms A–E, the units identity, the RPU chain, tab map, build order, checks. |
| **`model/CPRT_Intermediate.xlsx`** | The workbook to copy from: every dataset as a tab plus live formulas (fleet roll, age curves, Solver calibration, TLF drift, spread and RPU regressions, checks). Rebuild with `scripts/build_intermediate_xlsx.py`. |
| `docs/AGE_CURVES.md` | How S(age), R(age), P(age) are derived and validated, and what is fitted versus measured. |
| `findings.md` | The lab notebook — every result in chronological addenda, **including every retraction**. Addendum 22 = the 2026-09-26 experiment session. |
| `reports/` | One report per experiment from the second session (E1, E4, E8, E10, CCC age buckets) and the scoping doc. |
| `PROVENANCE.md` | Every host touched, its robots.txt status, what was fetched, where it is saved. |
| `ARCHITECTURE.md` | How the collector and the sitemap data physically work, and the bugs found the hard way. |
| `scripts/README.md`, `data/csv/README.md` | One line per script and per dataset: what it is and whether it is live, analysis, dead-end or legacy. |
| `docs/archive/` | Superseded documents, each with a header saying why. |

## Earlier results — historical snapshot, subject to the current audits

1. **Revenue per unit is a fee-and-mix engine, not a price pass-through.** Service-RPU elasticity to ASP 0.514
   (95% CI 0.29–0.73) with a +4.1pp intercept, n = 17; effective n ≈ 6. Used-car CPI → ASP → RPU is the nowcast chain; its FY26Q4 miss is ~0.8pp on service RPU,
   mostly at the ASP step (findings Addendum 19).
2. **Total-loss frequency follows the totaling spread** (repair CPI − used-car CPI), calibrated on 27 CCC industry
   quarters, not Copart's: ΔTLF = 0.599 + 0.0815 × spread(t−1), R² 0.81, one live out-of-sample hit. The spread went
   +15.7pp → +2.3pp → +8.3pp.
3. **The FY26 unit decline is one account, not share erosion.** Industry claims × total-loss rate × residual shows no
   share loss before the Progressive cliff (Apr–Jul 2026), which laps in FY27Q4. Management: *"with the exception of
   1 single customer loss, domestic insurance assignments would be up 2.3%."*
4. **Fleet ageing adds about +0.16pp a year to total-loss frequency** — a quarter of the 2019–25 rise, from an EPA
   survival schedule calibrated to the vehicle census and claim curves fitted to eight CCC statistics and tested
   out of sample. Smaller than the popular version, and defensible.
5. **Two datasets nobody else has:** a daily Copart-versus-IAA listed-inventory split (Copart ≈ 57% on clean nights)
   and cars per weekly sale event (~700 → 492), both from public sitemaps.

## Running things

```bash
cd /Users/kwu/cprt
./.venv/bin/python scripts/job1_snapshot.py             # Copart daily sitemap snapshot (nightly via LaunchAgent)
./.venv/bin/python scripts/job1_iaa.py                  # IAA daily snapshot — once per day only
./.venv/bin/python scripts/analysis_20260911.py         # TLF calibration, elasticity, decomposition CSVs
./.venv/bin/python scripts/age_curves.py                # age curves: extract, calibrate, fit, validate
./.venv/bin/python scripts/build_intermediate_xlsx.py   # rebuild the workbook from data/csv
./.venv/bin/python scripts/verify_intermediate_xlsx.py  # check its key formulas against the scripts
```

Both collectors run nightly via LaunchAgent `com.cprt.job1` (`scripts/run_job1.sh`, log `logs/job1_cron.log`).
Database `data/cprt.db` (gitignored); exported series in `data/csv/` (committed, indexed).

## Research-ethics rules (non-negotiable; `HANDOFF.md` §1)

robots.txt first on every host, and obey it · ≥2 s between requests to a host · honest identification per host ·
no authentication · no paywall or challenge circumvention · report blockers rather than work around them · every
dataset's source, method and date logged.

## Trust hierarchy

| Tier | Source | Reliability |
|---|---|---|
| 1 | SEC filings (10-K/10-Q/8-K, XBRL) | very high |
| 2 | Earnings-call transcripts, hand-transcribed | high — cross-checked 15/15 against a sell-side exhibit |
| 3 | Copart / IAA sitemaps (scraped) | medium — listed inventory, not yard inventory; gate on cross-page overlap |
| 4 | Derived series, regressions, fitted curves | lowest — compounds every upstream error; confidence intervals printed |

Tiers 1–2 produced every result that survived. Tiers 3–4 produced every claim that was retracted.
