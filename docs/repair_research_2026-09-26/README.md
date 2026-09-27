# Repair research audit index

Local copy created 26 September 2026 ET; consolidated for the 27 September repository update. Start with the [current research and model handoff](../MODEL_AND_RESEARCH_HANDOFF_2026-09-27.md).

Start with [frequency feasibility methodology and results](repair_frequency_feasibility/README.md). It records decisions, alternatives, executed steps, definitions, formulas, exclusions, checks and limitations. [Source log](repair_frequency_feasibility/sources.jsonl) records this pass’s downloads and failures. [Output manifest](repair_frequency_feasibility/output_manifest.json) fingerprints scripts and outputs.

Earlier work is preserved as a snapshot in repair_pilot/: findings.md (original estimates), matched_parts_findings.md (older-model OEM baskets), alternative_parts_findings.md (sourcing sensitivity), weighted_repair_architecture.md and repair_frequency_seed.json (historical component weights), aaa_scenario_findings.md (controlled scenarios and discrepancies), older_scenario_frequency_audit.md (older-at-estimate cases), and source/AlphaSense feasibility notes. These earlier files contain sources and methodological caveats, but are not retroactively certified as complete request-level logs. Missing earlier timestamps/raw captures remain missing; the copied files do not create evidence that was never retained.

Raw downloaded data/manuals and original response bytes for the current pass remain at:
/Users/kwu/Documents/ChatGPT/HFAC x Citadel/research/cprt_discovery_plan_2026-09-26/local_pass/repair_frequency_feasibility/raw/

Reproduction: copy that raw folder beside the mirrored scripts, or run the scripts from the original workspace. Avoid refetching to reproduce an old result; use the hashed source versions. Repository snapshot contains code/results, not the large raw archive.

For subsequent material analyses, retain: question and estimand; source population/period/version; acquisition method and failures; classification and join rules; alternative methods and choice rationale; exact executed transformations; numerical checks; interpretation and competing explanations; limitations; decision to proceed/stop. Decision summaries document the research rationale, not a claim to preserve private internal reasoning.

## Repair-scope follow-up

[Scope-frequency gate and explicit sensitivity component](repair_scope_sensitivity/README.md): CISS field completeness, additional provider evidence, uncalibrated probability grid and missing-cost guard. This has its own source log and manifest. Earlier repository snapshots remain unchanged.

## Historical distribution benchmarking

[Historical CCC reference shapes and current benchmark alignment](repair_cost_reference/README.md): four original distributions, two recent benchmarks, eight explicit mean-aligned approximations, source discrepancies and reproducible inputs/calculations.

## Single working base: repair premium to revenue

[Assumption-driven body-mix model](body_mix_working_case/README.md) estimates a6.3% LT repair premium and a−0.16pp calendar2027 exposed-service revenue contribution. See its assumptions and exact calculation; prior sensitivities are retained as history, not current base-case inputs.

- [Value and recovery assumption audit](value_recovery_audit/README.md): traces both 1.50 inputs to E8; older-vehicle KBB checks and historical Mitchell ACVs; auction recovery remains unmeasured. Prior revenue result remains an assumption-conditional scenario.

- [Paired auction recovery pilot](auction_recovery_pilot/README.md): seven candidate VINs; two secondary-corroborated ACV/sale pairs, no matched body comparison or primary settlement validation. Identifies unsold bids mislabeled as sales and preserves exclusions.

- [Contract-scope source and arithmetic screen](contract_scope_screen/README.md): Barclays Figure 1 implies broad carrier-base discounting already; reconstructed contract gain +$59.6m; actual scope remains unverified. Carrier composition and fleet-cohort framing distinguished from assumptions.
