# Incremental repairable-claim nonfiling

28 September 2026. Implemented in `engine.py`; `history_repair.build` consumes the paired claims/TLF automatically. No empirical rate adopted. No Excel work or external collection.

## Input contract

`assumptions.json` now contains `incremental_repairable_nonfiling`: eight quarterly fractions, default zero. Each fraction is the share of otherwise reportable **repairable claims** removed within each economic cell after the existing repair/value selection. It is not a fraction of all claims, a coverage penetration rate, or an absolute historical filing probability. Values must be finite and in [0,1). Uniform fractions across cells are a scenario simplification.

The explicit `claims_frequency_convention` requires the combined baseline frequency multiplier to exclude this incremental removal. This documents and gates the accounting convention; software cannot establish whether a real source already contains the effect. Review denominator and cohort-mix compatibility before entering evidence. Existing baseline propensity remains combined and calibrated.

## Cell arithmetic

For baseline-reportable claims C, economic total-loss probability p, and incremental repairable nonfiling fraction f:

- Total losses T = C × p.
- Removed claims = f × (C − T).
- Reported claims C' = C − f × (C − T).
- Reported TLF = T / C'.

Total-loss assignment/capture, sale-equivalent units, selected ACV, ASP, fees and ancillary jobs continue to use T and the existing economic selection. No total-loss vehicles are removed by this scenario. It does not model removing coverage, not filing a total loss, lower accident frequency or altered sale timing.

## Output semantics

Quarterly `claims_raw`, `TLF` and `normalized_claims` now describe the post-filter reported population. New `baseline_claims_raw`, `baseline_TLF`, `removed_repairable_claims_raw` and the scenario fraction expose the bridge. Cohort equivalents include baseline and reported claims/TLF, removed claims, and `reported_claim_weight`; legacy `claim_weight` remains the pre-filter weight for compatibility. Aggregate TLF uses reported weights, not those legacy baseline weights. These quantities remain model-relative or revenue-normalized, not measured absolute claims.

Same-quarter forecast activity ratios fall and TLF ratios rise by offsetting amounts when only repairable filing changes. Thus the existing revenue bridge stays neutral. The separate fleet/vintage research candidates remain their zero-incremental-nonfiling comparisons; they have not been given new scenario inputs. Previously saved baseline exports were not regenerated merely to add columns; rerunning the engine produces the expanded schema.

## Validation and limits

69 new integration checks passed: unchanged history for forecast-only inputs, paired counts, reported weights, constant total-loss units/ASP/RPU/revenue, same-quarter bridge neutrality, interaction with a repair-cost change, and invalid-input rejection. All74 existing structural checks passed. Comparison with the prior engine confirmed352 existing quarterly fields unchanged at default settings within numerical tolerance.

Synthetic FY27Q1 example: removing10% of repairables changes TLF from22.8745% to24.7861%. This is not market evidence. The module does not specify which repair types disappear or calculate a new average repairable severity; those require a severity-selective filing rule. It also cannot identify accident, coverage and filing effects from one observed claim-frequency change.

Forecast assumptions remain zero. Next empirical task should distinguish a falling repairable denominator from a changing total-loss numerator using compatible claim counts and populations; a TLF increase alone cannot identify the nonfiling fraction.
