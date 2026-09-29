# Cohort identification test — bounded result, 2026-09-28

## Status
Partial test only. Published age-direction evidence rejects a pure BETWEEN-age-group explanation for falling replacement counts. The proposed age × damage/component matched test cannot be completed from the public tables located. No causal sourcing coefficient or revenue forecast changed.

## Existing work checked
MIX_SEGMENTATION.md; repair_pilot/modern_frequency_source_audit.md and alternative_parts_findings.md; local CCC 2025 Q1–Q4 text and 2026 HTML/text. Earlier retail component baskets identify prices, not operation/sourcing frequencies. CRSS accident populations cannot fill estimate-line decisions. No repeat of bulk listing or inaccessible PDF collection.

## Test 1: can changing age weights alone explain replacement-count decline?
CCC 2026 report, Figure 37 and adjacent prose: non-comprehensive repairable appraisals average replacement count 13.6 in 2024, 13.0 in 2025. Prose explicitly says decline consistent across vehicle age groups. Figure 37 itself has only annual aggregate counts; no numeric age cells were recovered. Original chart retrieved and visually checked at raw/ccc_figure37.webp.
Source: https://www.cccis.com/reports/crash-course-2026
Image: https://cdn.prod.website-files.com/677e7ecbb3dbbe98615cde30/69caddd7c1f87ed17a7f6a69_Picture37.webp

Identity: overall change = sum_a w_2024,a*(n_2025,a-n_2024,a) + sum_a (w_2025,a-w_2024,a)*n_2025,a.
Here w is appraisal share and n is replacements per repairable appraisal. First term holds age weights constant; second is between-age mix. If counts decrease in every group with positive weight, the first term must be negative. This sign test uses the source's within-age statement; it is not an independently recomputed age standardization. We cannot assign a fraction of the -0.6 decline without age-cell counts. Age bins themselves allow changing exact ages, models and damage severity.

Result: between-age mix alone is insufficient. Does NOT reject total-loss selection within age bins. Does NOT show increased aftermarket sourcing within each bin: replacement count and replacement source are different outcomes.

## Test 2: age × impact × component standardization
Needed: both years' counts/exposure of eligible damaged components, repair/replace decisions, OEM/aftermarket/recycled counts, stable vehicle-age/model and damage definitions, comparable estimate maturity. For each joint cell compute operation and sourcing rates; reweight both years to a common distribution. Repairable-only data still condition on survival past total-loss decision. To identify total-loss selection additionally need pre-disposition estimates/damage information for totalled candidates, or a defensible external severity measure for all claims. Matching on final repair cost alone is invalid: it is affected by the repair/source choices being tested. Point of impact alone does not hold damage severity constant.

Result: no public joint table found in bounded pass. No pseudo-matched dataset constructed from unrelated marginals. Zero empirical matched cells admitted; no test statistic or effect size manufactured.

## Competing operational explanation found
Mitchell primary transcript, Ryan Mandell, March 12 2026, pp3–4:
https://www.mitchell.com/print/pdf/node/30026

Reports rising repaired-part share and proposes fewer repair jobs → shops seek better margins → favor labor-intensive repairs over purchasing replacement parts; also less parts-related cash outlay/waiting. His margin estimates and causal explanation are commentary, not controlled evidence. Transcript is same vendor/author as June Enlyte report, not independent replication. Earlier March preliminary numbers should not replace June 14.8%→15.5% history. It mentions stronger alternative utilization collectively; not a clean recycled-only measure comparable to CCC.

This expands the prior technician-shortage explanation: repair/replacement choices may respond to shop utilization. With spare capacity, repairing an eligible bumper may make economic sense despite a long-run shortage of technicians. Candidate mechanism can affect repair cost and donor demand, but cheaper total invoice is not guaranteed: additional labor offsets avoided parts expense. Must measure both.

## Bounded discovery (six queries)
1. collision repair parts replacement utilization vehicle age point of impact 2025 2024 repair replace CCC
2. site.mitchell.com 2025 "repair" "bumper" "2024"
3. site.solera.com repair replace parts age 2025 report
4. site.thatcham.org repair replace 2025 parts data age
5. Boyd 2025 repair replace ratio parts labour repair percentage same store
6. Caliber collision 2025 repair replace percentage parts repair data

Routes: estimator histories first (closest outcome); repair-chain operating disclosures (different incentives); Solera/Thatcham (alternative claims systems, repairability engineering). Search results outside primary shortlist offered European consumer preferences, product/API capabilities, ADAS calibration material and broad shop severity commentary, not the required US joint operation-frequency panel. Did not promote these into substitutes or exhaustively read them. Mitchell transcript followed because it directly explained the operational choice. No paid access, outreach, OCR, bulk scrape or agents.

## Decision and next step
Evidence admission: source-reported within-age replacement-count direction; qualitative shop-utilization mechanism. Not admitted: within-cohort substitution, numerical repair savings, salvage bid elasticity, revenue delta.

Best next route is a small existing estimator/repair-chain disclosure of repair-vs-replace by component over time, with age and claim scope. Stronger identification needs an extract; no such access is currently established. Do not repeat generic searches for this exact panel. In the model preserve separate assumption switches for within-cohort repair choice, source mix and selection; evaluate their implications conditionally. The evidence does not justify choosing a numerical causal effect merely to finish the bridge.
