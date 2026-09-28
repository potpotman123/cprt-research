# Joint repair economics and claim-reporting check

28 September 2026. Existing local evidence; 2,873 elementary scenarios, 221 distinct economic evaluations, and fee integration only for the baseline and three representative cases. Completed locally in under a second. No network, OCR, paid data, workbook changes, production-input changes or forward forecast adoption.

## Question and finding

Can repair/value changes, disappearance of small repair claims, or both explain older vehicles' higher reported total-loss frequency (TLF), roughly 1% repairable-cost growth and declining selected vehicle values simultaneously?

The combined specification fits the diagnostic targets better than either isolated mechanism, but none passes the tighter analyst-defined screen. The oldest group is particularly difficult. This is a failure of a deliberately restrictive specification against imperfectly aligned observations, not statistical rejection of the economic mechanisms. Four combinations pass a looser screen. We do not have an identified historical decomposition or a validated forecast.

## Evidence contract

| Observation | Target | Population and use |
|---|---|---|
| Age 7–9 TLF | 22.8% to 23.4% | CCC Figure 19, CY2024–25, all loss categories |
| Age 10–12 TLF | 31.5% to 32.3% | Same |
| Age 13+ TLF | 43.6% to 45.3% | Same; age methodology warning retained in source CSV |
| Repairable mean, ages 7+ | Approximately +1% | CCC annual text, Figure 34 discussion, line 277; aggregate selected repaired vehicles, not each age bucket |
| Total-loss vehicle valuation, ages 7+ | −0.5% | Saved Figure 22 footnote; non-comprehensive selected valuations, not unconditional vehicle values |
| Total-loss valuation counts | All losses −2.9%; non-comprehensive −0.2% | All ages; cannot be treated as older-cohort counts |
| Repairable counts | All losses −9.7%; non-comprehensive −8% | All ages; incompatible with an exact reconciliation of reported TLF and valuation counts |

Original publisher: https://www.cccis.com/reports/crash-course-2026. Sources are preserved locally; no fresh retrieval claimed. Machine-readable results record source hashes. The older valuation target is a cross-coverage plausibility check, not a population-matched validation target. Missing older-cohort counts are left missing.

## Constructing the reference population

Use only the three older age buckets and four existing vehicle body categories. Normalize the existing CY2025 calibration claim weights within ages 7+. Retain their damage-distribution shapes, vehicle-value levels, repair/body ratios, salvage curve and seller-fee assumptions. For each age bucket, adjust only its log repair-cost location until modeled TLF equals its reported CY2024 rate. Save these three adjustments explicitly.

This is a synthetic 2024 reference, not a measured 2024 fleet or an independent backtest. It uses later calibration information and hybrid-period levels. Matching starting TLF by construction must not be counted as predictive evidence. Unlike the preceding test, which worked backward from a fully recorded 2025 endpoint, this construction permits forward removal of small claims without silently anchoring a post-removal TLF to a pre-removal denominator. Production calibration is untouched.

Starting repairable mean is $3,649; starting selected total-loss ACV is $9,141. These are synthetic levels, not newly observed CCC statistics. This test compares growth rather than validating their historical levels.

## Mechanism and scenario grid

For each age/body cell, underlying damage rank runs from zero to one. The existing lognormal distribution maps rank to repair cost. A total loss occurs when repair cost exceeds vehicle value less assumed net salvage. Salvage remains a function of the original damage rank; removing claims does not relabel physical damage or improve salvage.

A filing parameter removes the lowest fraction of ranks in every cell. These ranks are checked to remain below the repair/total-loss boundary. This is a relative, cell-specific severity filter, NOT a measured deductible or one common dollar cutoff. It models additional disappearance of claims relative to the reference recorded population, not the probability that every real-world incident was originally reported.

For a cell with repair/total-loss cutoff u and removed fraction f:

- Total-loss mass remains 1 − u.
- Recorded repairable mass becomes u − f.
- Recorded claim mass becomes 1 − f.
- Recorded TLF is (1 − u) / (1 − f).
- Repairable mean uses the truncated repair-cost distribution between ranks f and u.
- Selected total-loss ACV, auction price and fees are averaged over the unchanged ranks above u unless the economic threshold itself moves.

Three common parameters apply across older age/body cells: same-damage repair-cost change −2% to +6%; unconditional vehicle-value change −3% to +3%; removed low-rank claim fraction 0% to 6%. All use 0.5-percentage-point steps. These are diagnostic search bounds, not evidence-based uncertainty ranges. Economics-only fixes removal to zero; filing-only fixes repair and value changes to zero; combined allows all three. Uniform parameters intentionally test a simple common explanation before adding more degrees of freedom.

Existing economic shapes and claim composition are frozen. No claim-volume/exposure adjustment, carrier change, service adoption change, or fee-schedule change enters the comparison. The same current fee schedule is applied to both endpoints solely to show conditional transmission, not actual historical fee growth.

## Results

Representative cases minimize the same descriptive score: sum of squared TLF errors divided by 0.25 pp, plus squared repair-mean and selected-value growth errors divided by 0.5 pp. These are analyst weights, not standard errors. The score is a ranking convenience, not likelihood or evidence of causality.

| Result | Economics only | Small-claim removal only | Combined |
|---|---:|---:|---:|
| Assumed same-damage repair growth | +2.0% | 0% | +0.5% |
| Assumed underlying vehicle-value growth | −0.5% | 0% | −1.0% |
| Original low-rank claim population removed | 0% | 2.0% | 1.0% |
| Predicted TLF increase, age 7–9 | +0.90 pp | +0.47 pp | +0.78 pp |
| Predicted TLF increase, age 10–12 | +1.08 pp | +0.64 pp | +0.97 pp |
| Predicted TLF increase, age 13+ | +1.21 pp | +0.89 pp | +1.18 pp |
| Repairable mean growth | +0.45% | +2.59% | +0.90% |
| Selected total-loss ACV growth | −0.30% | 0% | −0.88% |
| Total-loss count growth per fixed reference exposure | +3.29% | 0% | +1.99% |
| Recorded repairable count growth | −1.54% | −2.93% | −2.39% |
| Core auction RPU growth | +0.08% | 0% | −0.27% |
| Core auction revenue growth per fixed reference exposure | +3.37% | 0% | +1.71% |

These revenue figures apply only to this synthetic older population with fixed routing/capture. They exclude ancillary revenue and cannot be applied directly to Copart's consolidated revenue or FY27. In particular, the combined case's +1.71% is NOT an adopted forecast.

### Why the cases behave differently

Economics-only moves expensive repair candidates into the total-loss population. Removing those candidates suppresses the repaired average, so a +2% increase in the cost of identical repairs produces only +0.45% growth in the observed repaired average. Changes in which body/age cells contribute totals also mean underlying value change and selected total-loss ACV change differ.

Removing only the smallest claims leaves auction supply and fees unchanged, but removes low-cost observations from repair statistics. The representative 2% removal raises repaired average costs 2.59%, substantially above the roughly 1% target, while still not generating enough TLF increase for ages 13+.

The combined case balances these opposing selection effects and gets closer on repaired costs. But its 13+ TLF increase remains about 0.52 pp below the observed 1.70 pp increase. That residual can reflect within-bucket composition, age-specific reporting behavior, economic changes, model shape, or source differences. This test does not choose among those explanations.

## Robustness and count limitations

The tight screen allows at most 0.25 pp error in each age TLF and 0.5 pp error in each conditional-growth observation. No scenario passes. Relax only age TLF tolerance to 0.5 pp and four scenarios pass, with conditional total-loss growth from +2.65% to +3.94%. This is a coarse-grid descriptive set, NOT a confidence interval or proof that actual total losses grew. A finer grid could change boundaries and representative choices; no optimizer or extra refinement is warranted on these mismatched data.

The published all-age count changes cannot independently validate older-only results. They also fail the exact count/TLF identity documented in CLAIMS_COUNTS_AND_DENOMINATOR.md. We therefore do not fit them or multiply an invented activity adjustment to force a reconciliation. In real data, accident/coverage exposure may decline enough to offset increasing total-loss probability. Fixed-exposure results cannot establish absolute industry volume growth.

## Architecture and next evidence

Keep recorded claims and total-loss numerator separate. If reported claim frequency is already an input, do not apply this removal factor a second time. A production adapter must either start from incident exposure and generate both counts, or reconcile its filing adjustment to the reported claim population explicitly.

This experiment supports retaining that interface, not adopting its fitted parameters. Do not add age-specific fitting knobs merely to erase the oldest-group residual. The highest-value next check is whether existing source charts provide finer ages/composition or compatible older-cohort counts and conditional means. In their absence, document the parameter ambiguity and proceed with explicit scenarios rather than calling any one mechanism proven. Auction listings alone would not reveal missing repairable claims.

## Reproduction and checks

Run joint_claim_selection.py using the repository Python environment. Outputs: full grid, three-case comparison, JSON with baseline/rebase details, tolerance counts, checks and source hashes. Ten checks cover three starting TLF anchors; three units × RPU identities; filing invariance of totals and selected ACV; the increase in conditional TLF/repair mean under minor removal; equal repair/value scaling; and count reconciliation for every grid point. These validate arithmetic, not economic identification.
