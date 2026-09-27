# Working base: light-truck repair premium and Copart body-mix revenue

26 September 2026 ET. User explicitly requested a single assumption-driven model case, rather than more sensitivity research. This build supplies that case, with empirical inputs and judgment separated. It is a standalone research-model component; the existing intermediate workbook is not overwritten.

## Result
Modeled average repair costs: car $3,682; SUV $3,707 (+0.7%); pickup $4,823 (+31.0%); minivan $3,613 (−1.9%). Blending 72.4% SUV, 19.3% pickup and 8.3% van/minivan yields $3,914, or a **6.3% light-truck premium**. These are model outputs, not observed group means.

Inserted into the existing E1 calendar-2027 bridge, replacing its 1.01 repair ratio with 1.0631:

| Growth contribution from changing body mix | Updated working base | Prior base |
|---|---:|---:|
| Unit effect | −0.538 pp | −0.620 pp |
| ASP mix effect | +0.740% | +0.746% |
| Service RPU effect | +0.380 pp | +0.384 pp |
| Compounded service revenue effect | **−0.160 pp** | **−0.239 pp** |

Equivalent to about −$1.60m per $1bn of exposed service revenue, holding other factors fixed. This is the existing US-insurance/service-revenue approximation, not a consolidated revenue forecast. Consolidated effect requires the affected business's revenue weight; no unsupported company-wide dollar impact supplied. Calendar years, not a precise next-four-quarter catalyst. Buy-sell, international, share changes, catastrophe and noninsurance effects are outside this experiment.

## Cost construction and rationale
1. Start with $3,682 as the CAR repair mean. The number is derived from CCC2025 seven-plus-year all-loss repairable mean; assigning it specifically to cars aged 7–9 is an assumption. Absolute scale cancels in the repair ratio used in E1, so it does not determine the sign here.
2. Set car front/rear/other severity proportions to 1.00/0.60/0.80. These are judgment assumptions: front cases receive the largest average bill; rear cases less; other/side between them. All unmodeled impact categories, including unknown/noncollision, are folded into other for this working case. Scale these three means so their car impact-weighted mean equals $3,682. Do not infer these proportions from AAA's deliberately different full-repair scopes.
3. Use the CRSS2024 age7–9 front/rear/other shares already calculated, separately for each body. Transferring police-crash mix to insurance repair mix is explicitly assumed. Minivan shares remain separate. This allows both price differences and impact-mix differences to affect costs.
4. Front/rear repair ratios come from AAA2023 published hypothetical complete estimates: Rogue/Camry 0.9940/1.0285; F150/Camry 1.4260/0.9107. Transfer those relative differences to the older cohort without an attenuation factor. This is a strong proxy assumption, not an age-matched observation. Treating a specific high-cost front scope as representative of average front repairs is also assumed.
5. Set other-impact SUV premium to 10%, pickup to 15%: explicit modest positive judgment allowances for unpriced components/operations, not measured premiums. Use SUV operation ratios for minivans; their separate impact mix explains a different total mean. No use of windshield-only costs or mirror-only premiums as full side-collision prices.
6. Blend using prior E8 listed-body shares: SUVs40.9, pickups10.9, vans4.7 divided by their sum. Using the selected salvage/listed mix as a fixed proxy for the source exposure mix is approximate and potentially endogenous. Treat the van bucket as minivan for costing. No assumption that these are population registration weights.

At identical CAR impact weights, SUV repair costs are +1.9% and pickups +28.8%. After their own impact weights, +0.7% and +31.0%. This decomposition is part of the one working case, not another sensitivity grid.

## Historical-distribution connection
Use CCC2017 sedan1/noADAS as the selected historical FRONT shape, scaled to the modeled car front mean; other body front distributions use their relative front costs. Save front_reference_distribution.csv. This choice carries the previously identified Figure32/33 discrepancy; it is a historical histogram reference, not a measured latent repair distribution. Other historical shapes remain archived but are not additional cases here.

The E1 total-loss calculation does NOT directly threshold this repairable-only histogram. It retains the existing age-specific totaling curve and log-cost/value dispersion, and applies the modeled relative cost as a multiplicative shift. This avoids pretending that missing total losses are present in CCC's repaired population. Thus distribution shape is a recorded price reference; the relative cost ratio is the current connector to TLF. Explicitly note this architecture rather than suggesting CCC has estimated the latent loss tail.

## Unit and fee mechanism
Inherited assumptions: relative effective totaling threshold=1.50; relative auction ASP=1.50; equal claim frequency per exposure across bodies; fee/ASP elasticity=.514; effective log(cost/value) dispersion≈1.5702. Equal net salvage-recovery percentages are consistent with using the same value/auction ratio, but neither recovery percentage nor that equality is measured here. Claim frequency is not set to the old HLDI0.67 proxy.

Model log threshold/repair shift=ln(1.50/1.0631)/1.5702. The existing aggregate2024 totaling curve is preserved when splitting car/LT curves. The fleet roll then changes cohort composition through2027. This is a two-body approximation: weighted average repair ratios are fed into the nonlinear totaling model rather than separately estimating SUV and pickup totaling curves. Seven-to-nine-year relative repair costs are applied at other ages as a simplifying assumption.

Compute unit contribution using the prior E1 differential of TLF changes relative to its one-body roll; compute ASP change from the change in LT share of total losses; RPU contribution=.514×ASP change; compound unit/RPU contributions. That inherited decomposition is an attribution approximation, not an independently identified causal frozen-mix counterfactual. The earlier report's circa18.2% repair break-even remains a reference under these fixed assumptions; no new sensitivity sweep was run.

Interpretation: the 6.3% repair premium partly offsets LT's assumed50% higher effective totaling threshold, but does not eliminate its repairability advantage. The modeled loss of units exceeds fee growth, giving a small negative mix effect. Do not call this alone a large short thesis.

## Evidence, assumptions and known issues
- AAA source/ratios: ../repair_pilot/aaa_scenario_results.json and findings; https://newsroom.aaa.com/wp-content/uploads/2023/11/Report_Cost-of-ADAS-Repairs-FINAL-23.pdf . F150 radar detail conflicts with summary by$594.28. For this authorized working case, retain the published full bill and flag it as provisional; do not invent a correction or claim component reconciliation. New-model and equipment differences remain embedded.
- CRSS source/output: ../repair_frequency_feasibility/cohort_table.csv and methodology; https://static.nhtsa.gov/nhtsa/downloads/CRSS/2024/CRSS2024CSV.zip . Large samples improve those population shares, not validity of transferring them to claims.
- CCC benchmark/histogram: ../repair_cost_reference/README.md and historical_bins.csv; https://www.cccis.com/reports/crash-course-2026 ; https://preview.thenewsmarket.com/Previews/3CIS/DocumentAssets/577096.pdf . The benchmark assignment and distribution transfer remain assumptions.
- LT blend/value assumptions: /Users/kwu/cprt/reports/E8_body_value_ratio.md. Listed weights are measured within their selected pool, then transferred by assumption.
- E1 model source: commit71803fc87727332171c5b682ea9853d6281a4a11, scripts/experiments/e1_body_propensity.py. Source snapshot retained; only inspected setup and split/roll functions executed, excluding write sections. Source comments asserting paid severity measures repair costs, claiming causal HLDI identification, or a guaranteed dispersion lower bound are not adopted.

## Reproduction and QA
build.py produces repair_cost_build.csv, results.json and front_reference_distribution.csv. Inherited compact inputs are snapshotted under inherited_inputs. Source/result hashes appear in manifest.json. All listed local upstream files are hashed there. No new web acquisition was necessary; inputs reuse saved research. No OCR, paid access, outreach or expensive analysis. Runtime under one second.

Checked impact weights and LT weights sum to1, car costs reconcile, equal repair/threshold ratios remove the old model's unit difference, old 1.01 case reproduces prior outputs, and updated calculation is traceable to component contributions. This is arithmetic/model verification, not evidence that assumptions are true. Recommended label in the pitch: 'Working model estimate: LT repair premium ~6%; mix effect ~−0.16pp on exposed service growth.'
