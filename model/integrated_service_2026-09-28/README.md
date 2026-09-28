# Integrated quarterly service-revenue research model

**Current presentation baseline:** [HISTORY_REPAIR.md](HISTORY_REPAIR.md). Use `reconciled_quarterly_service.csv` for reported history and provisional same-quarter forecast bridges, plus `historical_operating_bridge.csv` for unit/RPU attribution. `quarterly_results.csv` is retained as the original absolute reconstruction and diagnostic. Its historical errors remain unresolved; its forecast dollars are superseded for presentation. The original integration description below documents that diagnostic engine.

After running the engine, run `history_repair.py` and `check_history_repair.py` from this directory using the same Python runtime shown below. The new adapter does not identify absolute operating units; see its explicit base-transfer assumption and manifest.

28 September 2026. First integrated revision after the architecture audit. No Excel authoring, paid access, OCR, scraping or external outreach. Runs locally with Python standard library in seconds.

## Delivered

One runnable eight-quarter legacy-service model connecting the revised age-constrained economics, evolving cohort composition, simplified carrier allocation, selected-price fees, title/delivery assumptions, other-US activity and international activity/fee/FX schedules. Financial controls, missing-data gates, historical residuals, source hashes and Fable field mappings are included. This supersedes the old prototype as the **integration reference**, not as an adopted investment forecast.

The model is structurally complete for the chosen legacy-service scope. Absolute quantities are normalized, multiple operational inputs remain assumed, and historical predictive validation has not passed. Optional post-close consolidated-service output is deliberately unavailable while acquired revenue classification/eliminations are missing. This is not described as a complete consolidated acquisition forecast.

## Run

From repository root:

```sh
/Users/kwu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 model/integrated_service_2026-09-28/engine.py
/Users/kwu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 model/integrated_service_2026-09-28/checks.py
```

Inputs: prior linked inputs.json (reported history, fleet, fee grid, friend allocations); age_constrained_engine_results.json (latest cohort parameters); assumptions.json (all integration choices); acquisition management projection CSV (optional gated branch). No local workbook, browser session or original licensed PDF is needed to execute these calculations with the repo input snapshots.

## Equations and interfaces

**Claims.** Use CY2025 calibration claim weights by age/body. For quarter q, multiply each weight by the ratio of its fleet claim-weighted stock in q to CY2025; normalize all weights to one. Separately multiply total fleet-stock growth by the FY25 US service-dollar seasonal proxy and an assumed reported-claim-frequency multiplier. This does not identify physical-damage coverage; fleet is a proxy for covered exposure. No separate filing multiplier is applied. The model preserves cohort composition changes without multiplying fleet growth twice.

**Damage and capture.** For each age/body cell use the new car ACV, repair median and age-group dispersion with existing body ratios. Solve repair bill > pre-loss value − assumed net salvage over continuous damage rank. Weight the selected states by claims, routing, effective carrier capture and insurance-consignment fraction. Carrier weights are treated as total-loss-weight proxies, with common cohort economics across carriers. Forecast weights and non-PGR allocations freeze at FY26Q4. PGR retains its inherited path. No duplicate aggregate share haircut.

**Timing.** Output is sale-equivalent captured fee vehicles, not physical assignments. No additional lag is imposed. Physical opening and closing inventory fields are null. Attempting to activate an unsupported physical-inventory mode raises an error; it does not silently operate with invented opening stock. A real inventory revision must supply origin cohorts, opening balances and non-sale exits and change the carrier-path interpretation.

**Fees.** Integrate buyer fees on the selected auction-price distribution, using the existing standard/preferred mix, prebid fee and fixed fee. Seller revenue equals assumed seller rate × hammer price. Gross salvage recovery changes with damage rank and also enters the totaling threshold after seller fee. Buyer fees do not reduce insurer proceeds in this framework. Other seller net costs are not independently modeled.

**Services.** Insurance sale-equivalent units × title adoption × incremental title price, plus units × delivery adoption × external delivery fee less explicit waived fees. Same-quarter attachment is an assumption, not verified service recognition. A bundled-title switch prevents adding title revenue already counted in seller fees. Noninsurance service activity remains in other-US, avoiding a second application of all-US service dollars to insurance units.

**Base scale.** One FY26Q4 normalization sets modeled insurance service revenue to 90% of reported US services. It does not establish absolute claims, auction units or true company market share. The unit scale is computed once per input snapshot; forecast-only driver changes cannot change it. Other-US starts at the remaining10%; international at reported Q4 international dollars. Base assumptions determine normalization and remain visible.

**Other US and international.** Activity-equivalent counts × assumed fees, with FY25 geography revenue shape as an explicit seasonal activity proxy and separate quarterly activity/fee/FX drivers. This replaces the old flat-Q4 seasonal convention; it is still not independently identified physical-unit seasonality. No residual balancing plug is forecast, and no total-service-growth input exists.

**Acquisition.** Existing annual management total-revenue projections are mapped to fiscal months using an assumed January2027 inclusion date. Pre-close service contribution is zero. After that, acquired-service dollars and consolidated-service output remain null unless a service-classification fraction AND eliminations are specified. Management total revenue is shown separately and never automatically relabeled service revenue.

## Outputs

| File | Use |
|---|---|
| historical_controls.csv | FY25/FY26 reported service dollars, source files and excluded purchased-vehicle dollars |
| quarterly_results.csv | Eight quarterly modeled branch dollars, reported comparators, residuals, normalized activity, fees and acquisition gate |
| cohort_engine.csv | 192 quarter/age/body rows with claim weights, probabilities, selected values, prices and fees |
| carrier_allocation.csv | Carrier weights, allocation and contribution, applying capture once |
| acquisition_gate.csv | Assumed month mapping and total-versus-service classification status |
| INPUT_REGISTER.md | Evidence status, populations, conventions and ownership of every consequential input |
| assumptions.json | Editable integration inputs; missing drivers are rejected rather than filled with zero |
| checks.json / manifest.json | Structural checks, source hashes, normalization and unresolved evidence |
| FABLE_HANDOFF.md | Four-view design contract, field mapping, display rules and unsupported interpretations |

`*_raw` fields are relative calculation intermediates. `normalized_*` quantities are calibrated activity, NOT reported units. `activity_equivalent` counts are bookkeeping scales, NOT auction-unit estimates. Every revenue `_musd` field is USD millions. Historical model values are reconstruction; reported history remains separate and immutable.

## Verification and historical limitation

Follow-up: [historical error explanation](HISTORICAL_ERROR_EXPLANATION.md) quantifies percentage misses and an exact mechanical bridge. The Q2 US miss is 10.90%; its principal arithmetic contributions are the prior-year revenue seasonal proxy and inherited capture relative to Q4, not the small modeled intra-year cohort changes. This is not causal identification, and no inputs were changed to erase errors.

74 structural checks passed: cohort/claim normalization, carrier aggregation, six TLF targets, four selected age-value targets, two repaired means, fee integration, revenue addition, units × RPU, missing-driver rejection, invalid adoption rejection, unsupported physical-timing rejection, acquisition classification gating, forecast-only propagation preserving history/scale, and title-bundling treatment. Increasing fee integration from1,024 to4,096 changes core RPU by less than0.001% in checked quarters.

Historical US modeled minus reported revenue is +$46.986m, +$89.298m, +$18.920m, $0m. International: +$9.580m, +$9.618m, −$3.334m, $0m. Q4 ties by construction. These are reconstruction diagnostics using later calibration evidence/current schedules, not out-of-sample backtests. Do not publish FY27 totals as validated forecasts. Revised constraints can worsen historical fit; neither hide this nor select an older calibration solely for a better-looking error.

## Audit closure and remaining work

- Stage A complete provisionally: periods, controls, perimeter, normalized levels and assumption register defined. Unknown inputs are explicitly assumed or gated.
- Stage B complete for sale-equivalent convention: claims/cohort adapter, latest repair/value engine, routing and simplified allocation connected. Physical inventory is not built and not claimed.
- Stage C complete for legacy provisional branches: buyer/seller fees, title/delivery, other-US and international executable. Acquisition overlay has an explicit missing-classification gate.
- Stage D complete: reproducible runner, structural checks, historical residual output and Fable package.
- Stage E not presented as completed: predictive validation, evidence-supported driver forecasts, thesis attribution, consensus comparisons and valuation remain separate follow-up work. No thesis-materiality sweep was run to choose assumptions.

Highest-priority remaining validation is the historical claims/seasonality/allocation convention, service normalization, and population compatibility. Resolve these on the connected model before interpreting fine repair sensitivities. Expensive experiments remain subject to user review; ordinary local source checks and integration are authorized.
