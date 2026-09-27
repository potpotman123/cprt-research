# Vehicle mix: repair-cost audit and sign-reversal tests

September 26, 2026. Local analysis only. No network requests, OCR, new listing collection, paid data or changes to the source workbook/repository. The sensitivity calculations completed in under one second. That is computation time, not total assistant effort or a usage-credit estimate.

## Finding

The prior model's negative body-mix effect is reproducible, but its sign is not established by the evidence used to calibrate it. The base produces approximately a 0.24% calendar-2027 revenue headwind in the existing US-insurance/service-revenue approximation. It changes sign at a light-truck/car repair-cost ratio of approximately 1.18 under the other base assumptions. A coherent change in relative salvage recoveries can also remove or reverse it.

These are conditional sensitivities of the previous model, not new estimates of actual repair costs, recoveries, group revenue, EPS or share value. The model combines SUVs, pickups and minivans/light trucks; it is not an independently estimated SUV-only model.

## 1. What the 1.01 input actually measures

The existing E1 report averages HLDI collision paid-claim severity indices for recent model years and uses the light-truck/car ratio as a proxy for relative repair costs. The saved HLDI source defines severity as the size of claim payments. It does not provide a repair-only estimate for otherwise comparable damaged vehicles, or the cost of repairing vehicles that were instead totaled.

That distinction matters because a claim payment reflects the disposition of a claim as well as damage. The totaling model needs the repair-cost distribution that enters the insurer's decision. Using payments after that decision as if they measure repair costs before it can make the assumed relationship depend on the outcome we are trying to explain.

Further limitations:

- HLDI's table covers 2022–2024 model years. It does not directly measure body-specific repair-cost ratios at the older ages central to the salvage model.
- The ratio is constructed from averages of class/size indices, not an exposure-weighted sample of Copart's potential supply.
- Vehicles in the different categories are not matched here on damage and age.
- The prior value ratio of 1.50 is itself a proxy built from new prices, assumed segment weights and retention data. Applying it to salvage auction prices is an additional assumption.
- Higher expected salvage recovery changes both the totaling decision and auction proceeds. The original model uses a common threshold fraction rather than explicitly estimating that recovery difference.

### Apparent arithmetic discrepancy resolved

An initial comparison appeared to contradict the reported class averages because it included micro four-door cars. The earlier report explicitly used mini-to-large four-door cars, excluding microcars.

With that stated exclusion, the car paid-severity mean is 95.5 and the light-truck mean over the selected size rows is approximately 96.56. Their ratio is 1.0111, reproducing the rounded 1.01 assumption. There is no demonstrated arithmetic error in that ratio.

Including microcars changes the comparator mean to 92 and the ratio to approximately 1.0495. Under that alternative comparator the modeled revenue effect becomes approximately -0.18%. This is a population sensitivity, not a correction and not a more accurate estimate of repair costs. Neither comparator resolves the conceptual limitation above.

## 2. Replication before sensitivity

I read the prior research-branch model and executed only its local setup and calculation functions, excluding its original file-writing sections. The same fleet, survival, claim-frequency and totaling inputs reproduce its calendar-2027 result:

| Component | Reproduced effect |
|---|---:|
| Units | -0.620% |
| Service RPU | +0.384% |
| Revenue, original additive approximation | -0.236% |
| Revenue, compounding those two effects | -0.239% |

The compounded figure is used below. This minor arithmetic refinement does not alter the interpretation. These are effects attributed by the old approximation to changing body mix, not a complete forecast of Copart revenue growth. Calendar years have not been translated into fiscal quarters.

For each scenario, the model still preserves the aggregate 2024 age-specific totaling curve by construction. Thus its good aggregate fit cannot independently validate the chosen body split. Claim frequency is held equal between bodies, as in the original base case.

## 3. Repair-cost sensitivity

Hold the effective totaling-threshold ratio and auction-price ratio at 1.50, the original dispersion at approximately 1.57, and the service-RPU/ASP elasticity at 0.514. Vary only the assumed light-truck/car repair-cost ratio.

| Repair-cost ratio | Unit effect | RPU effect | Combined revenue effect |
|---|---:|---:|---:|
| 1.00 | -0.636% | +0.384% | -0.254% |
| 1.01, original assumption | -0.620% | +0.384% | -0.239% |
| 1.05 | -0.558% | +0.381% | -0.179% |
| 1.10 | -0.484% | +0.378% | -0.108% |
| 1.15 | -0.413% | +0.374% | -0.041% |
| 1.20 | -0.346% | +0.371% | +0.023% |
| 1.30 | -0.221% | +0.364% | +0.142% |
| 1.50 | approximately zero | +0.350% | +0.350% |

The break-even repair-cost ratio is approximately 1.182. This is about 17% higher than the original 1.01 ratio, or repair costs about 18% above cars. It is not a claim that actual repair costs have that relationship.

Mechanism: increasing light-truck repair costs reduces the extent to which higher vehicle values favor repairing them. The modeled unit disadvantage shrinks. The surviving positive fee/price contribution then offsets it. Therefore 'light trucks total less often' and 'light trucks reduce revenue' are different thresholds: the revenue effect becomes positive before the unit effect reaches zero.

### Other assumptions move the threshold

If value and auction-price ratios both equal 1.30, the repair-cost break-even is approximately 1.113. At 1.70, it is approximately 1.246. These linked value/price cases replicate the prior model's convention; value and sale price need not actually move together.

At the base value/price ratio, varying the distributional dispersion from 1.05 to 2.00 changes the repair-cost break-even from approximately 1.279 to 1.107. This parameter describes how widely repair costs relative to values differ among same-age vehicles. The same average shift can move different numbers of claims across the totaling boundary depending on that distribution.

These dispersion cases are stress assumptions, not statistically estimated confidence bounds. The earlier claim that repair-cost dispersion alone is necessarily a lower bound on dispersion of repair-cost/value is not generally valid: covariance between costs and values also matters. No new dispersion estimate was established here.

## 4. Explicit recovery sensitivity

The original simplified rule totals when repair cost exceeds a common fraction of vehicle value. To inspect the missing recovery mechanism, replace the relative threshold with:

**Relative net totaling cost = relative pre-accident value × (1 − light-truck net recovery fraction) / (1 − car net recovery fraction).**

For illustration, hold the car's net recovery at 30% of its pre-accident value, the light truck's pre-accident value at 1.50 times the car's, and relative repair costs at 1.01. Vary the light-truck recovery fraction. These recovery fractions are assumed, not measured.

Keep the price and recovery assumptions coherent: the auction-price ratio follows the net recovery ratio under an explicit assumption of equal proportional deductions between gross auction proceeds and net recovery. This relationship may not hold with different seller charges and disposal costs; it is a scenario convention.

| Light-truck recovery / its ACV | Effective totaling-cost ratio | Implied auction-price ratio | Modeled revenue effect |
|---|---:|---:|---:|
| 20% | 1.714 | 1.00 | -0.835% |
| 25% | 1.607 | 1.25 | -0.516% |
| 30%, equal percentage to car | 1.500 | 1.50 | -0.239% |
| 35% | 1.393 | 1.75 | approximately zero (+0.008%) |
| 40% | 1.286 | 2.00 | +0.233% |

Better salvage recovery works through two channels: it lowers the insurer's net cost of totaling, reducing the modeled unit disadvantage, and it raises auction proceeds and modeled fee revenue. This scenario therefore identifies recovery as another decisive missing input. It does not establish which recovery case is likely, and expected recoveries at claim disposition are not automatically identical to eventual realized proceeds.

## 5. What changes in our research judgment

The observed SUV/crossover composition shift remains a useful finding. The fee schedule also supports the possibility that higher sale prices fail to offset fewer transactions. However, the current evidence does not establish the required totaling difference or its net revenue sign.

The existing -0.24% estimate should be retained as a scenario, not promoted to a measured demographic drag. Even under its original assumptions, it is a relatively small revenue contribution whose group earnings and valuation implications have not been established. The results here should not be mechanically extrapolated into a stock-price target.

The next data priority is a comparable-age, comparable-damage repair-cost measure and expected net recovery by body type. More sitemap records will not supply either field. An inexpensive next action is a bounded source/access inventory for those exact fields. Separate SUVs/crossovers from pickups wherever possible, and verify the denominator before treating paid claims or sold salvage as representative of potential claims.

## Scope and validation

- Reproduced the committed 2027 additive result within the stored rounding tolerance.
- Checked that equal repair and threshold ratios eliminate the modeled body-specific unit effect.
- Checked monotonicity of the repair-cost sensitivity and bracketed each zero crossing.
- Parsed the relevant HLDI class table from embedded PDF text; no OCR or individual vehicle inspection.
- Preserved all existing source data and workbooks. No forecast changes were written back.

The adjacent `body_sensitivity_results.json` records the exact results, assumptions and model-source hash. `body_sensitivity.py` reproduces the calculations locally. The original HLDI PDF remains in the local repository's raw-data directory and was not uploaded or reproduced as a full table in this report.
