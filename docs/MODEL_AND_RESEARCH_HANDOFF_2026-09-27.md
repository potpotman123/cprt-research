# CPRT: current research and model handoff

Updated 27 September 2026. Read this before the older `HANDOFF.md` and `MODEL_BLUEPRINT.md` for the current scope. This records research rationale, executed work, definitions, findings, corrections and remaining decisions. It does not elevate assumptions into evidence.

## 1. What the user wants now

**Architecture approved:** the user subsequently approved the organization of the 14-tab workbook with four main reading tabs and will continue visual design with Fable. Preserve the [approved architecture](../model/service_revenue_2026-09-27/APPROVED_ARCHITECTURE.md). Analytical development continues here; the approval is not validation of the inputs or final styling.

- A differentiated Copart pitch with an approximately six-month catalyst horizon. The user is currently pursuing a short, but the calculation must retain contrary evidence and must not be adjusted to manufacture downside.
- **The present model deliverable is quarterly TOTAL SERVICE REVENUE: US service revenue plus international service revenue.** Do not build EPS, margins, a DCF or vehicle-sales revenue as part of this task. A separate valuation model may exist elsewhere.
- Preserve the detailed research: repair-cost weighting, age/body cohorts, economic total-loss thresholds, probability calibration, auction pricing and nonlinear fees. The user values granular equations and visible calculations.
- Four main reading tabs, not four total tabs. Supporting calculations and source records follow behind them. Do not replace live research calculations with fixed output values merely to reduce tab count.
- Main reading path: **RPM Summary → Volume Build → Vehicle Economics → Revenue Bridge**. Main tabs should be compact, tabular financial schedules. Supporting schedules must remain traceable and editable.
- Formatting references are the supplied KW VIA and TeamBDC/KWBM workbooks. Garamond, aligned periods, clear horizontal rules, compact rows, restrained shading, subtotal/total lines. No large gaps or explanatory paragraphs occupying the main schedules. Color only section markers; ordinary tabs stay uncolored.
- Use cheap structured-data exploration first. Ask before expensive OCR, bulk listing collection, paid data or large exploratory analysis. Explain the full pipeline, purpose, cost and alternatives before requesting approval. Existing local calculations and bounded checks do not require another approval.
- Fable may take over design. This handoff and the repository artifacts are intended to make that possible without relying on chat history.

## 2. Read these files in order

1. This handoff: current objectives, evidence and modeling decisions.
2. [Repair research index](repair_research_2026-09-26/README.md): links to all repair investigations, outputs, source logs and limitations.
3. [Working repair-cost build](repair_research_2026-09-26/body_mix_working_case/README.md), its `results.json`, `repair_cost_build.csv` and `build.py`.
4. [Age-curve derivation](AGE_CURVES.md): sources, survival interpolation, claim weights, earlier calibration and validation limits.
5. [Value/recovery audit](repair_research_2026-09-26/value_recovery_audit/README.md) and [auction pilot](repair_research_2026-09-26/auction_recovery_pilot/README.md): why the 1.50 ratios remain uncertain.
6. [Contract arithmetic](repair_research_2026-09-26/contract_scope_screen/README.md): source reconstruction and the distinction between novelty and a risk already in an analyst forecast.
7. Older `HANDOFF.md`, `findings.md`, `reports/` and `MODEL_BLUEPRINT.md`: broader research history, market-share work, alternate mechanisms and retractions. Their old three-statement/DCF instructions do not expand the current service-revenue-only scope.

The reproducible [workbook package](../model/service_revenue_2026-09-27/README.md) specifies commands, dependencies, calculation ownership and completed validation. The [execution plan v2](research_execution_2026-09-26/research_execution_plan_v2.md) and other files in that directory preserve the broader cheap-test research program and local first-pass findings. Full licensed source documents, browser captures and large raw datasets remain local; source URLs/paths and hashes identify them. Do not claim the Git clone includes those raw sources.

## 3. Research findings and evidence strength

### Repair costs: scope and population matter

The initial approximately 1% repair premium was not a tightly identified industry estimate. Matching parts or individual operations does not establish the mean complete repair bill. Labor overlap, repair versus replace, sourcing, ADAS work and the extent of damage can dominate a parts-price comparison. AAA deliberately specified repair scenarios; their total bills are not average front/rear insurance claims.

Public repairer estimates and OEM baskets were examined, together with CCC/Mitchell documentation and targeted AlphaSense leads. No matched national insurer-allowed-cost dataset by body, age and complete repair scope was acquired. Do not describe a failed or narrow search as proof no such dataset exists. Source acquisition notes and earlier findings are in `repair_pilot/`.

### CRSS frequencies are useful proxies, not repair-operation frequencies

The 2024 NHTSA CRSS pass used 51,658 crash rows and 90,641 vehicle rows, retaining 73,875 car/SUV/pickup/minivan vehicle involvements after explicit exclusions. It created 20 body-by-age cells, with survey-weighted ratios and design-aware standard errors. Age-7–9 sample counts include 6,921 cars, 3,655 SUVs and 1,366 pickups.

Front/rear initial-impact shares at ages 7–9: cars 56.0%/24.5%, SUVs 54.9%/28.0%, pickups 57.3%/21.3%. The exact weights and coding are in `repair_frequency_feasibility/cohort_table.csv` and its README. Unit of analysis is a vehicle involvement in a police-reported crash, not an insured exposure, claim, paid repair or auction vehicle. Transferring these weights to insurance repair economics is an assumption. Disabling damage is not structural repair severity or an insurer total-loss decision.

CISS manual screening did not establish a validated mapping to our proposed complete repair bundles. A 66-vector probability grid and 4,356 paired combinations were built as mathematical sensitivity ranges. Missing bundle costs remain null; the evaluator refuses to manufacture cost estimates. These are not estimated probability distributions or confidence intervals. See `repair_scope_sensitivity/`.

### Current working repair premium

The user authorized a single assumption-driven working case instead of further sensitivity research. It produces:

| Body | Mean modeled repair cost | Relative to car |
|---|---:|---:|
| Car | $3,682.00 | 1.0000× |
| SUV | $3,706.98 | 1.0068× |
| Pickup | $4,822.91 | 1.3099× |
| Minivan | $3,612.70 | 0.9812× |

Mechanism: anchor car repair mean to the CCC older-vehicle reference; assume car front/rear/other relative scope costs of 1/.6/.8; normalize these to the car mean; transfer AAA new-model front/rear body cost ratios; assume other-impact SUV/pickup premiums of 10%/15%; apply each body's CRSS impact weights. Minivan uses SUV cost ratios and its own impact shares.

Blend light trucks using listing-based weights of 72.39% SUV, 19.29% pickup and 8.32% van/minivan. The result is approximately **6.31% higher repair cost for LT**. Neither the source-population transfer nor the complete-scope mean is independently validated. The AAA pickup detail/summary discrepancy remains disclosed. Large CRSS N does not validate the cost-transfer assumptions.

Historical CCC front-impact distributions were retained and aligned to newer mean benchmarks. They are repairable-only reference statistics, not a measured latent distribution including total losses. Do not threshold a repaired-only histogram and call that the probability of totaling. See `repair_cost_reference/`.

### ACV and salvage ratios are unresolved

The original 1.50 value and auction-price ratios descend from the same E8 new-price/depreciation proxy. They are not independent measurements. The auction ratio means **LT price 50% above car price**, not **50% salvage recovery of ACV**.

A five-model 2016 KBB retail-value convenience panel found roughly 1.128× for selected crossovers and 1.493× for F150 relative to selected sedans. A historical Mitchell table reproduced by Manheim showed different body ratios again. Those populations are not a current age/condition-matched insurer-ACV panel. Neither check was adopted as a fleet-wide replacement. The findings specifically warn against equating pickups with all light trucks when the observed mix shift is concentrated in crossovers/SUVs.

A bounded seven-VIN auction pilot produced two descriptive secondary-corroborated ACV/proceeds pairs: Camry gross recovery 21.69%, F150 41.60%. They are not matched comparables, and neither was primary settlement-verified. Several archive records confused failed bids and completed sales. No body-specific recovery coefficient was estimated.

### Contract concessions: much of the arithmetic is already in the analyst case

Barclays' 25-Aug-2026 illustration is consistent with a concession applied to 621.9k carrier units rather than only the 125k midpoint incremental units: 125k × $950 less $40m cost and $19.1545m concessions = **$59.5955m**, matching the rounded $60m gain. This does not verify the real contract or settle whether the carrier base is pre/post award.

The contract win remains positive in the reconstructed example. A broad-base concession is therefore not a newly discovered hidden loss in that analyst case. Avoid adding the same contract loss/concession twice to a forecast that already contains it. The table image is licensed source material and is not included in the Git commit; our numerical reconstruction and provenance are included.

## 4. How the mechanism connects to revenue

For age a, body b and period t:

- Fleet stock = cohort births × survival. Historical car/LT annual sales proxy vintage births; actual historical LT subtype splits remain unavailable.
- Relative claiming exposure = stock × age claim weight × relative body claim frequency. The age weight is a fitted driving/coverage/claiming composite, not an observed absolute accident probability. Do not add a redundant coverage multiplier.
- Economic total if repair cost > ACV − net salvage. Gross auction proceeds and seller net recovery are different quantities.
- Relative threshold H_b = [ACV_b × (1 − net recovery_b)] / [ACV_car × (1 − net recovery_car)].
- Body offset = ln(H_b / relative repair cost_b) / sigma. Probability within age bucket k is Φ(z_k − offset_b).
- Solve z_k so base-year modeled claim weights reproduce the CCC bucket mean. This is calibration by construction, not external validation of body probabilities. The CCC buckets are step functions; a smooth single-year curve is not directly observed.
- Weighted auction supply = claiming exposure × total-loss probability. Absolute claims and company allocation levels are not inferred from this normalization.
- Auction price = ACV × gross recovery. Apply buyer fee schedules at price-distribution nodes, then weight the fees; applying a nonlinear fee schedule only to mean price is generally different. Add the assumed seller fee separately.
- Revenue potential = sum of weighted auction supply × service RPU. Its period growth rate feeds an actual-dollar US service revenue base. International services are forecast separately and added.

The latest model uses same-quarter prior-year reported service dollars for seasonality and monthly-midpoint interpolation of calendar-year-end demographic cohorts for fiscal-quarter timing. It does not divide annual revenue by four or claim measured quarterly cohort data.

The revenue bridge removes the fleet effect already embedded in a latest-quarter growth baseline before adding the new period's effect:

**US service forecast = B × (1 + s×g_forecast) / (1 + s×g_reference)**,

where B is prior-year same-quarter US services grown at the chosen baseline rate, s is assumed insured-service exposure (currently 90%, not disclosed), and g is the modeled demographic revenue-growth contribution. International service forecast = prior-year same quarter × (1 + assumed growth).

US/international baseline growth currently carries forward the latest reported Q4 FY26 rates. This is a mechanical starting case, not consensus, and does not separately model contract laps, insurer mix, fee changes, catastrophes or FX. The pending ACV acquisition is excluded explicitly.

## 5. Distinguish the three modeling stages

1. **Earlier two-body research bridge:** blended repair ratio 1.0631, assumed value/auction ratio 1.50 and fee elasticity .514 yielded a calendar-2027 exposed-service contribution around -0.160pp. This is a conditional, small contribution, not a six-month consolidated forecast.
2. **First granular annual workbook:** four bodies, CCC bucket calibration and explicit fee schedules. Showed approximate offset between lower units and higher RPU. The user rejected its 25-tab presentation and arbitrary index/$1bn outputs. Its mathematical results are not directly comparable to the earlier approximation.
3. **Quarterly dollar bridge:** clean service revenue, actuals through FY26, fiscal-quarter demographic timing and incremental adjustment versus embedded baseline effects. Starting Q1/Q2 FY27 estimates were approximately $1,005.4m/$965.2m. Incremental fleet adjustments were approximately -$0.23m/-$0.45m. The user rejected stripping out live research equations to reach four total tabs. The current redesign restores live calculations behind four main reading tabs.

Do not describe these numbers as contradictions without checking denominator, horizon, counterfactual, fee method, calibration and aggregation. None establishes a large standalone short or a reliably negative sign under all plausible inputs.

## 6. What remains worth investigating

**Subsequent cheap tests:** [27 September model diagnostics](model_tests_2026-09-27/README.md) quantify existing-input sensitivity, exact age/body counterfactual attribution, forecast-only versus permanent parameter changes and an illustrative damage/recovery selection model. In the current bridge, H1's -$0.684m fleet adjustment comprises -$0.885m age composition, +$0.082m body-within-age, +$0.061m fleet size and +$0.058m interaction. A +/-1pp US baseline growth change moves H1 services +/-$16.743m. Permanent economic-input changes mostly cancel through the relative growth bridge and calibration; newly introduced forecast-only changes can have much larger effects. Those scenarios are not empirical predictions and were not adopted into the workbook. Do not pitch the current negative incremental adjustment as demonstrated negative body-mix attribution.

- Historical crossover/SUV/pickup/van birth cohorts and age-matched pre-loss values, particularly crossovers versus sedans.
- Claim-population age weights and cohort transitions; an older average fleet does not itself prove a near-term total-loss supply cliff.
- Carrier exposure/claim growth × Copart allocation, distinct from one-time contract losses and wins. Premium share is not insured-vehicle share. Market-share work can proceed independently using the older handoff and experiments.
- Actual usable yard capacity: occupied area, throughput, dwell time and vehicle footprint. No CapEx/capacity dollar forecast has been validated here.
- Scope selection versus true repair-cost relief, and complete bill composition versus individual operation prices. Missing operation frequencies remain missing.

Rank further work by whether a feasible measurement can materially change the six-month revenue estimate relative to a dated comparable forecast. Novelty alone is insufficient. Do not expand collection merely to tighten an immaterial coefficient.

## 7. Reproduction, Git boundaries and quality checks

The research directories preserve scripts, numerical outputs, source logs, failed acquisitions, exclusions and hashes. Some scripts require large raw inputs retained locally; those dependencies are declared rather than silently refetched. Earlier incomplete acquisition logs were not retroactively fabricated.

The workbook package includes compact input snapshots and the live-formula builder, so Fable can inspect both the formulas and the precise inputs without reconstructing the chat. Check annual reported service totals, quarter mappings, survival roll, repair mean reconstruction, CCC bucket calibration, nonlinear fee bands, actual-dollar scaling and input-response restoration. Arithmetic checks do not validate empirical assumptions.

Only this research/model work is committed in this update. Concurrent nightly data collector modifications are left untouched. Licensed PDFs/table images, raw browser captures, dependencies, caches and credentials are excluded. No agent messages or external outreach were sent.
