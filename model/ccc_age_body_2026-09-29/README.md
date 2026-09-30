# CCC direct age/body data incorporated into revenue selection

**Parameter audit (29 September):** the hypothetical source mix, 40% eligible repair-bill exposure, 25% donor exposure and 1.5× contribution multiplier are not measured CCC inputs. New primary evidence constrains total parts spending but does not validate these parameters. See [parameter provenance and offset tests](../../docs/aftermarket_parameter_audit_2026-09-29/README.md) and the linked CCC interview brief.

Received 29 September 2026 from the user as CCC contact data. Source: `Data for Harvard Research (Daniella Biblin)_9.29.2026.xlsx`, sheet **Vehicle Type, Age**. The unchanged workbook is archived in gitignored `raw/ccc_direct_2026-09-29/`; its hash is in `source_manifest.json`.

**This is a runnable CCC-based reference and aftermarket scenario family using the existing revenue engine.** It updates claim composition and total-loss frequencies. It does not measure sourcing, repair savings, near-threshold density or bids. The earlier reference remains reproducible. Pending population clarification, this is a labeled CCC-sample/body-mapping case rather than a silent replacement of national assumptions.

## Source and checks

The workbook supplies 2020–2025 frequencies and total-loss mix for four body types × four age groups: **96 cohort-year records, each with two source metrics**, plus body controls. Frequencies are in `A1:H23`, age/body total-loss mix in `K1:R21`, body mix in `L24:R31`. Extracted records retain precision and source cell addresses.

All six total-loss mixes sum to one and all 24 body-mix controls match their age-cell sums. Body-frequency controls reconcile closely but not exactly: maximum residual **0.005354 percentage points**, or 0.5354 basis points. Its cause is not established; raw values are preserved. There is one visible sheet and no formulas, comments or explanatory footnotes.

Unspecified definitions: geography, coverage/loss exclusions, estimate maturity, annual completeness and commercial vans. Headers refer to estimate years, not Copart fiscal quarters or sale dates. Car→Car and Pickup→Pickup are direct label mappings; Utility Vehicle→SUV and Van→existing Van/minivan economics are proxies. The workbook's 7+ category cannot identify the model's 7–9, 10–12 and 13+ split.

## Integration method

1. For total-loss share `m_i` and frequency `p_i`, derive `claim_weight_i = (m_i/p_i) / Σ(m_j/p_j)` and `aggregate_TLF = 1 / Σ(m_j/p_j)`. These identities require common source populations/partitions. They do not recover absolute claims.
2. Use the **2025** cross-section to anchor 16 age/body cells. Allocate each 7+ group's claims over the engine's older buckets using the inherited within-body conditional claim weights. That finer split remains a proxy.
3. Calibrate **one repair-distribution level multiplier per observed cell**, holding inherited values, dispersions and salvage-rank relationships fixed. A small bounded scalar bisection reproduces the observed frequency. Each 7+ group uses one common multiplier. These multipliers absorb model misspecification; they are not observed repair-price differences or aftermarket savings.
4. Apply the multiplier **before** the selection cutoff in `cell_economics`. The same cutoff then determines selected vehicle/damage ranks and auction fees. Overwriting frequency after price selection would disconnect the volume and price populations; that alternative was rejected.
5. Roll claim weights using relative fleet changes from the **active vintage/body fleet at 2025**. Reusing the predecessor fixed-body denominator would distort the already observed body mix again. Annual-to-quarter mapping remains a proxy; the historical time trend is not extrapolated automatically.
6. Pass the same `cohort_anchor_path` through the aftermarket adapter's reference, feedback loop and revenue attribution. Each sourcing case is compared with its **own CCC-based reference**. Source transfer, donor exposure, bid transmission and timing assumptions are unchanged.

`reference_config.json` is the directly runnable configuration; `aftermarket_inputs.json` points to `cohort_anchor.json`. This family should be used when discussing the supplied cross-section, alongside the prior family as a comparison. Historical reported dollars remain reconciled, while inferred insurance units and internal fee/service splits change with composition.

## Results

| FY27 legacy service revenue | Previous composition | CCC composition/level case |
|---|---:|---:|
| Reference | $4,105.80m | **$4,093.08m** |
| Larger aftermarket shift | $4,015.15m | **$4,002.41m** |
| Aftermarket effect against own reference | −$90.66m | **−$90.66m** |

CCC larger-shift insurance units fall **2.045%** and all-in insurance RPU **0.914%** versus reference. The baseline revision of **−$12.73m** is a changed model decomposition, not an observed revenue decline. Half-switching gives **−$62.99m** versus −$90.66m. The workbook does not independently validate the response derivative.

The full panel implies aggregate TLF rising **22.238%→23.124%** in 2024–2025. A symmetric decomposition gives **+1.0043 pp** from within-cell rates and **−0.1189 pp** from composition, totaling **+0.8854 pp**. Within-cell changes include severity and aging inside 7+; this is not an aftermarket causal estimate.

## Calibration tradeoff

The new case reproduces all 16 frequencies and TL-mix cells at its 2025 fleet anchor. The predecessor's exact repair/value targets are no longer jointly imposed:

| Cross-check | Previous target | New implied |
|---|---:|---:|
| Mean repaired cost, age 0–6 | $5,721 | $5,644.70 |
| Mean repaired cost, age 7+ | $3,682 | $3,735.82 |
| Selected value, current/newer | $40,187 | $38,989.23 |
| Selected value, age 1–3 | $30,259 | $29,689.54 |
| Selected value, age 4–6 | $20,328 | $19,907.61 |
| Selected value, age 7+ | $9,122 | $9,157.55 |

The source populations/periods are not confirmed identical. Residuals are preserved in `economic_crosschecks.csv`; no extra parameters were fitted to hide them. The earlier audit's twelve-target exact fit applies to the **original family only**. Response shapes, finer old-age mix, body values, absolute insurance units, carrier allocation and service economics remain partly assumed.

## Files and reproduction

- `source_cells.csv`, `source_body_controls.csv`, `annual_derived.csv`, `source_manifest.json`: complete source panel, derived claims, controls and provenance.
- `cohort_anchor.json`, `calibration_cells.csv`: 24 engine inputs and 16 scalar level fits.
- `reference_config.json`, `aftermarket_inputs.json`: wired reference and scenarios.
- `scenario_summary.csv`, `quarterly_results.csv`, `base_component_ledger.csv`: revenue outputs.
- `economic_crosschecks.csv`, `checks.json`: disclosed target residuals and ten integration checks.

Run `python3 model/ccc_age_body_2026-09-29/integrate.py` using the saved source CSV; standard library only, no workbook or network required. To import the original again, run `extract.py` with its path. It refuses to overwrite a different archived source under the same filename and never edits the original workbook. Fable receives extracted inputs/results, not the raw workbook.

Source definitions were requested from the user without blocking this labeled case. No agents, outreach, paid collection, broad discovery or extensive fitting occurred.
