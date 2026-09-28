# Claims, coverage and filing: denominator audit

28 September 2026. Existing-file inspection and six small identity checks; no web searches, fitting, spreadsheet work or forecast changes. Results: `claims_filter_audit_results.json`.

## What is actually implemented

| Component | Source / implementation | Interpretation and limitation |
|---|---|---|
| Exact-age R(a) | `docs/AGE_CURVES.md` §3; `scripts/age_curves.py`; `model/linked_service_revenue_2026-09-28/prepare.py` | Half weight at age0; exp(-0.09027 × max(age-6,0)) thereafter. Fitted relative claims per surviving vehicle, bundling mileage, risk, coverage and filing. Not a measured coverage rate or pure accident probability. |
| Base claim shares | `docs/fleet_selection_2026-09-28/age_constrained_engine.py` | Relative age claims inferred as total-loss age mix divided by target age TLF; body weights supplied by the fleet proxy. Older age split and population/period compatibility remain assumptions. This is not an independent claim-count dataset. |
| Cell corrections | `fleet_cohort_build.py`; `vintage_body_integration.py` | Each target claim share divided by raw CY2025 fleet-times-R mass. Therefore the baseline age/body share is calibrated; the inherited R slope supplies within-cell age structure and subsequent cohort evolution. Its broad age gradient is not independently revalidated by the corrected shares. |
| Aggregate claim activity | `engine.py` versus cohort candidates | Original engine uses total fleet growth for aggregate activity and R for composition. Cohort candidates use corrected fleet-times-R for both activity and composition. Do not confuse the candidates with an adopted production rewrite. |
| Quarterly frequency change | `assumptions.json`, `engine.py` | All eight multipliers equal1. No explicit new coverage or filing trend is presently supplied. The name reported_claim_frequency does not specify whether the denominator is insured exposure or surviving fleet; it needs a contract before using outside data. |
| TLF / damage selection | `age_constrained_engine.py`; `engine.py` | Repair distributions are calibrated to reported age TLF. Baseline claim selection is absorbed into that calibration; the distributions are not independently observed pre-filing crash severity. |
| Minor-claim filter | `joint_claim_selection.py` | Separate retrospective diagnostic, not wired into the forecast. Removes low-ranked repairables and changes reported denominator and TLF together. Its hypothetical baseline/rebasing must not be interpreted as observed unfiled claims. |
| Dollar scale | `engine.py`; `history_repair.py` | Revenue normalization and same-quarter anchors do not establish physical claims, coverage or absolute units. |

## Rules for adding drivers

1. **Keep the combined R baseline for now.** Do not multiply it by a new absolute coverage percentage or another age mileage curve. Those mechanisms are already conceptually bundled, although not separately identified. Refitting cell corrections after adding coverage can simply absorb the change, producing the same fit without new evidence.
2. **A future change needs one accounting location.** A matched claims-per-surviving-vehicle change can serve as a combined multiplier only after separating cohort mix already modeled. Do not also add component coverage/filing changes embedded in it. Conditional claims per insured vehicle-year need compatible covered exposure; they cannot replace the combined rate directly. A measured total claim count already includes exposure growth, so multiplying it by fleet growth again is also unsafe.
3. **Selective nonfiling requires a paired TLF adjustment.** For reported baseline claims C and totals T, removing x repairables gives C'=C-x and TLF'=T/(C-x). Their product still equals T. Applying C'/C while holding baseline TLF fixed invents lost total losses; raising TLF without reducing claims invents extra total losses. If losses themselves stop being filed, this simple preservation result no longer applies.
4. **Coverage removal is a separate channel problem.** Uniform loss of otherwise identical covered exposure reduces both types of claims proportionately and leaves TLF unchanged; selective removal can change TLF either way. First-party coverage loss does not eliminate every third-party recovery route. Do not treat a collision coverage rate as a filter on all insured physical-damage claims.
5. **Do not add an absolute filing cutoff to the calibrated damage curve.** A future explicit filing engine needs a stated baseline selection process and joint recalibration, or a clearly labeled incremental removal from the baseline reported population. Preserve the revenue anchor and test both claim and total-loss identities.

## Checks and implications

Using existing model cells, baseline TLF is22.8838%. In a hypothetical removal of10% of repairable claims, reported claims fall7.7116% and TLF rises to24.7960%, while total losses remain unchanged. Keeping TLF fixed instead would incorrectly reduce total losses7.7116%. These are identity demonstrations, not estimated market changes. A separate synthetic10% uniform exposure shock applied twice produces a19% decline instead of10%.

Six checks passed, including baseline calibration absorption and the flat quarterly frequency configuration. Arithmetic checks do not validate the calibrated probabilities.

Corrected two statements in `docs/AGE_CURVES.md`: the mileage-adjusted residual is not identified coverage/filing, and HLDI insured-exposure frequency is not directly R per registered vehicle. The legacy generating script still contains those historical interpretations in its printed narrative; do not treat rerunning it as updated evidence.

Next integration requirement: choose an explicit reported-claims denominator convention, retain combined baseline propensity, and pair any incremental repairable-nonfiling scenario with its conditional TLF and selected-value calculations. Until compatible time-series evidence exists, leave its magnitude assumed/unknown rather than adding a Maryland-derived forecast shock.
