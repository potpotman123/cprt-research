# Common-reference thesis scenarios

1 October 2026. **Conditional audit scenarios, not an adopted forecast.** Economic findings and evidence status are in the [full audit](../../docs/thesis_architecture_audit_2026-10-01/README.md). This package joins the existing CCC/premium/aftermarket/carrier/fleet modules without changing their saved reference or fitting coefficients to the preferred conclusion.

Run from the repository root:

```text
python3 model/thesis_audit_2026-10-01/run.py
python3 model/thesis_audit_2026-10-01/test_audit.py
```

Standard library only; no network, raw workbook, new calibration or external account needed. Input dependencies and their current fingerprints are in `runtime_manifest.json`. The older audit ZIP is not this version.

## Read the two comparisons separately

- **Saved model:** $4,093.077730m → $3,904.623888m service revenue. Interaction-aware contributions: carrier allocation −$132.820456m, aftermarket −$55.633386m. No further premium relief and the fleet roll already exist in this reference, so contribute **zero incremental dollars**.
- **Diagnostic recovery comparator:** $4,132.662422m → the same $3,904.623888m. Freezes same-quarter fleet mass/mix and assumes 5% additional premium relief, alongside the prior-year allocation convention. Four-driver contributions are allocation −$133.611677m, aftermarket −$55.966965m, no relief −$22.973733m, and fleet roll −$15.486159m. This comparator is illustrative, not a surveyed bull or consensus forecast.

`assumptions.json` gives the exact driver definitions. The comparator's recovery magnitude and the premium response parameters are assumed. A frozen cohort comparison isolates the existing roll; it is not a forecast that vehicles stop aging. Neither comparison establishes a forecast miss or a catalyst.

## How the joint calculation works

1. Start with the saved CCC reference. Historical quarterly service dollars, the assumed insurance revenue split, calibration and fee schedule are held common across every combination.
2. Toggle four channels: PGR-only runoff with other carrier weights/allocations frozen at Q4; no further premium relief versus 5% relief; incremental aftermarket sourcing; existing fleet roll versus frozen same-quarter mass. Premium and age signals are not applied again as unexplained claim haircuts.
3. For sourcing, transfer cumulative basket quantities each quarter: OEM 1/2/3/4pp and recycled 0.375/0.75/1.125/1.5pp into aftermarket. This reaches the previous 5.5pp stress endpoint in Q4 rather than applying it all year. It is not the earlier suggested three-year national adoption narrative.
4. Use delivered source prices and eligible-bill exposure to calculate repair savings. Each quarter solves the inherited recycler contribution, rebuilder benefit and scarcity equation with that quarter's selected loss population. Expected salvage updates according to its explicit pass-through. Other drivers are shared with the no-sourcing counterfactual. The feedback measures incremental sourcing effects only; it does not claim full industry equilibrium after a macro coverage shock.
5. The threshold-responsive and locked claim fractions are disjoint identical starting populations. Add their units, revenues and claim counts; recompute TLF, ASP and RPU from those totals. Do not average ratios. Default sale-equivalent timing is required; assignment-flow timing is explicitly rejected here.
6. Price selected vehicles using the current model fee bands, seller terms and ancillary services. Retain the reference's other US and international assumptions. Quarterly outputs, source-price feedback and component identities remain inspectable.
7. Evaluate all 16 subsets. Shapley attribution averages each marginal effect over all 24 orderings, sharing interactions once. A separate two-driver attribution matches the unchanged saved reference. Neither attribution is a causal estimate.

## Output map and reviewer checks

| File | Purpose |
|---|---|
| `assumptions.json` | Exact scenario paths, population definitions and evidence labels |
| `endpoint_configs.json` | Recovery comparator and combined configuration before sourcing; apply the path in assumptions through `run_aftermarket` |
| `scenario_summary.csv`, `quarterly_results.csv` | All subsets; common reference and period |
| `factor_attribution.csv` | Four-driver diagnostic attribution and standalone deltas |
| `results.json` | Both comparisons, sequential bridge, unit/RPU identity and opposing sensitivities |
| `aftermarket_feedback.json` | Quarterly repair, bid, scarcity and convergence checks |
| `checks.json` | New economic invariants, distinct from evidence validation |
| `runtime_manifest.json` | Reproduction dependencies; no source refresh implied |

Workbook/Fable acceptance: preserve the two reference labels, units in millions of service dollars, source/admission status and zero additional premium/age loss against the saved reference. Match annual service endpoints within $0.1m before interpreting small differences. Keep price expectations separate from realized prices, and reported TLF separate from total-loss counts. Do not use the current dollar ranking as evidence that one causal mechanism is empirically stronger.
