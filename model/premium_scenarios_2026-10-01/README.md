# Explicit premium channels in the revenue model

1 October2026. Audit result: the prior engine had no premium-rate input. Coverage, driving and baseline filing were combined in `claims`; incremental small-repair nonfiling was separate. Effects could be represented but not explained by premium scenarios. The loan-payoff sidecar also imposed an assumed unit loss without deriving it from premiums.

The main engine now accepts an optional `premium_assumptions` block. Its `run()` function compiles this through `premium_channels.py`, then runs the existing cohort, carrier, fee and service calculations. Existing configurations omit the block and retain their baseline. No historical source, CCC calibration or presentation workbook was changed. Previously recorded source hashes remain historical snapshots, not hashes of this new implementation.

## Inputs and mechanism

Four quarterly actual/scenario paths and explicit reference paths are required for premiums, income, vehicle value and deductibles. A matched physical-damage premium is preferable; broad motor-insurance CPI is only a proxy. Compare like populations, coverages and price definitions. Loan input is an excess lien-free fraction relative to reference, not originations blindly shifted70 months. The supplied cohort-average vehicle-value path is separate from the main engine's vehicle-value multiplier and must be reconciled before calibration.

Coverage pressure uses deviations in premium/income and premium/vehicle-value ratios, plus the loan-payoff deviation. Repairable filing pressure uses premium/income and deductible/income deviations. Separate assumed slopes act on coverage and filing log odds. A quarterly adjustment fraction gradually moves behavior toward the new target, allowing delayed cancellation and restoration. Initial incremental pressure is zero; the historical price increase is already in the baseline, not a new backlog automatically applied again.

A baseline coverage probability and repairable filing probability anchor the hypothetical affected population. The affected fraction weights **baseline covered claims**, not all cars. Coverage probabilities produce a relative claim-exposure multiplier. Filing probabilities are weighted conditional on the surviving coverage pool. This is a uniform pooled approximation: actual response likely varies by age, loan status, income, loss type and insurer. The eligible fraction must exclude unaffected third-party claims and other coverage routes. Non-insurance recapture and different route fees are not separately estimated here.

Core identities:

- Covered claim exposure = reference combined exposure × residual claims driver × incremental coverage multiplier.
- Total losses = covered claim exposure × cohort economic TLF.
- Reported claims = total losses + otherwise filed repairables × incremental filing multiplier.
- Assignments and sales follow the existing carrier/routing/timing logic; revenue follows existing fee and service logic.

Thus changes in small-repair filing alone cannot create or destroy modeled total-loss vehicles. Premium changes can affect volume through coverage, while premiums, income and deductibles affect the observed claims denominator through filing. Falling premiums can restore exposure; the adapter does not impose a permanently bearish effect. Premiums do not directly alter repair costs, ACV, salvage values or auction fees.

## Double counting and admission

The adapter rejects a simultaneous incremental nonfiling shock or preexisting coverage/filing multiplier. A non-neutral claims forecast requires explicit acknowledgement that its residual excludes the premium channels. This acknowledgement is a user modeling convention, not statistical identification. Age effects already in baseline must not be applied again. Measured loss counts already reflect premium effects; use them as targets or a reduced-form alternative, not an additional independent haircut. Premiums are also endogenous to claim costs: a historical CPI/TLF correlation is not a causal elasticity.

All behavioral slopes, probabilities, affected fraction and lag in `assumptions.json` are **ASSUMED**. CPI evidence does not calibrate them. `forecast_admission=false`; the saved reference is unchanged. The meaningful missing evidence is policy exposure/coverage and claim incidence by matched renewal cohort, with premium, deductible, vehicle value and lien status. Loan vintage/term survival is required before an excess payoff path can be estimated.

## Runnable checks and examples

Run `python3 model/premium_scenarios_2026-10-01/run.py`. It passes complete configs through the main engine and saves quarterly diagnostics and annual results. Indices normalize to100 in the reference; hypothetical premium paths are not a current-rate forecast.

Checks cover neutral baseline reproduction, historical-ledger preservation, filing-only revenue invariance, premium increases/decreases, proportional scaling of all burden inputs, payoff-only effects, gradual recovery after a shock, zero exposure, zero adjustment speed, invalid prices, and prevention of overlapping claims/nonfiling effects. The original43 engine checks also pass.

The illustrative+10% premium case lowers annual service revenue by about$47m under the chosen assumptions; the−5% case raises it about$24m. These are demonstration outputs, not estimated premium sensitivities. Do not cite them as a Copart forecast or combine them mechanically with the earlier loan-payoff sidecar.
