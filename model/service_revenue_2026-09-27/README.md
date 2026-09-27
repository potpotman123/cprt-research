# Quarterly service revenue model

Current design as of 27 September 2026. Start with [the research handoff](../../docs/MODEL_AND_RESEARCH_HANDOFF_2026-09-27.md) for the investment question, prior findings and unresolved assumptions.

## Reading order

| Main tab | Purpose |
|---|---|
| RPM Summary | FY26 reported and FY27 projected quarterly US, international and total service revenue, in $m; H1 FY27 total |
| Volume Build | Fleet, claiming exposure, total-loss frequency and resulting unit/RPU contributions; fitted age inputs |
| Vehicle Economics | Editable body-specific value, recovery and frequency assumptions, repair costs, calibrated TLF and fee examples |
| Revenue Bridge | Prior-year dollars, baseline growth, removal of embedded fleet growth, incremental fleet adjustment and reconciliation |

After these four tabs, CALCULATIONS introduces Cohort Roll, Repair Costs, Loss Calibration and Fee Calculation. DATA introduces four values-only source tabs. There are 14 tabs including the two section dividers. Only RPM Summary and the two dividers have colored tabs. Main schedules use compact rows, aligned periods, horizontal rules and Garamond. Red/yellow inputs are assumptions; blue numbers are source records; green formulas link across sheets.

## Calculation ownership and trace

1. AD Fleet supplies annual car/LT births and survival records. Cohort Roll computes stock for four bodies, ages 0–45, calendar 2023–27. The historical LT split uses the same listing-weight proxy across vintages; this is a limitation, not measured historic subtype data. Future births and LT share default to flat 2025 levels and are editable in Cohort Roll G26:H27.
2. Volume Build D22:D25 holds the inherited survival stretches, declining claim weight and newborn-cohort exposure fraction. Claims are relative exposure, not absolute company counts. Survival is linearly interpolated in scaled age and zero at scaled age 31 or higher. This tail convention is inherited.
3. Repair Costs rebuilds the working mean from age-7–9 CRSS front/rear impact shares, AAA within-scope body/car ratios and explicit other-scope assumptions. CCC's $3,682 older-vehicle repairable mean is assigned to cars by assumption. The ratios are transferred across ages; the workbook does not claim observed age-specific repair bills.
4. Vehicle Economics converts value less net salvage into a relative threshold. Log threshold/repair differences, divided by dispersion, provide body offsets. Loss Calibration uses 32 visible bisection iterations per age bucket to match CCC2025 bucket means using CY2025 modeled claim weights. The calibration is live, without macros or Solver. Matching buckets does not validate the assumed body split. Overall modeled TLF need not equal CCC's aggregate because the populations/age weights differ.
5. Fee Calculation prices each body/age at three bid nodes and applies the captured non-licensed, secured-payment, non-clean-title buyer/prebid fee tier, gate/environmental charges and an assumed seller fee. It is an illustrative fee schedule, not realized customer mix. Current fees are also used for the modeled historical comparison to isolate composition effects.
6. Cohort Roll multiplies stock, relative claim frequency, calibrated TLF and fees. Monthly-midpoint interpolation of calendar-year-end totals creates fiscal-quarter demographic exposures. This is an interpolation assumption, not a quarterly auction sample.
7. Revenue Bridge projects US services as B*(1+s*g_new)/(1+s*g_reference), with B equal to same-quarter prior-year services times baseline growth, and s=90% assumed insured-service exposure. The baseline carries forward Q4 FY26 growth. International services carry forward their separate Q4 growth. Add the two for total services. This is not a Street forecast, and the pending ACV acquisition is excluded.

The active workbook restores the live research equations behind the four main reading views. It supersedes the earlier four-tab compact version and the earlier 25-tab annual presentation. It forecasts services only; no EPS, vehicle sales or CapEx projection is included.

## Reproduction

Included files: workbook; `build.mjs`; self-contained `model_inputs.json`; independent read-only validator; validation outputs and live-input test results. Source provenance is in the data tabs, input snapshot and linked research directories. No raw archive or original reference workbook is required to rebuild this snapshot.

Use the Codex bundled Node runtime with `@oai/artifact-tool` available through a local `node_modules` symlink. The bundle was located at `/Users/kwu/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/` for this run. Dependencies are not committed. Use the bundled Python runtime with openpyxl for read-only verification.

From this directory, with those runtimes on PATH:

```sh
node build.mjs
python3 validate_live.py
```

Default output is this directory (or its parent when the script is in a directory named `work`). Optional `CPRT_OUTPUT_DIR` overrides the workbook output directory for both commands. The builder writes local previews and live-input test records. Rebuilding overwrites the packaged workbook; review the Git diff afterward. No network collection or OCR is performed.

## Validation performed

Independent Python reconstruction checked 920 annual stock cells, repair means, 60-iteration probability calibration, every cohort's nonlinear fees, fiscal-quarter weighting and dollar forecasts. The workbook's 32-iteration solver differs only within numerical tolerance. All checks passed; no cached Excel error values or external workbook links were found. Data tabs contain values only. ACV, repair-cost and insured-exposure mutation tests propagated to forecasts and restored exactly. Rendered views of all tabs were reviewed.

Recalculation was tested in artifact-tool, not desktop Microsoft Excel. Numerical agreement validates implementation, not the underlying empirical assumptions. The current incremental fleet effect is small and does not establish a large standalone short.
