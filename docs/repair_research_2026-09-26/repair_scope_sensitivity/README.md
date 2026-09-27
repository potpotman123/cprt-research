# Repair-scope frequency gate and sensitivity specification

26 September 2026 ET. Follow-up authorized to test measured scope shares first and use explicit sensitivity cases where evidence fails. No paid access, outreach, OCR, photo analysis or broader sample collection. This is a research component for the future model, not a calibrated revenue/valuation build.

## Result
The bounded search did not identify scope frequencies for 7–9-year-old cars versus SUVs. CISS provides damage descriptions, not insurer-required repair bundles. Public CCC evidence is more granular than previously located but mismatched to the target cohort. Proceed with explicit uncalibrated sensitivities; do not assign a best-estimate q.

## Data inspection actually performed
Downloaded official 2024 CISS structured archive (18,497,017 bytes). Read GV, CRASH and CDC; checked unique (CASEID, VEHNO) vehicle keys and unique crash IDs. Joined vehicle age from CRASHYEAR minus MODELYR; selected ages 7–9 and BODYTYPE car codes 1–9,17 versus SUV codes 14,15,16,19. Selected any CDC record with CDCPLANE=F. Kept all case categories and inspection statuses for field-availability auditing. This is NOT an initial-front-impact cohort or a weighted population-frequency calculation.

| Field-availability count | Cars | SUVs |
|---|---:|---:|
| Age/body vehicle records | 840 | 490 |
| Vehicles with any recorded front CDC | 473 | 278 |
| Front CDC records | 582 | 342 |
| Vehicles with multiple front CDC records | 73 | 42 |
| Front records with unknown depth code 99 | 64 | 38 |
| Front records with A-pillar code 8 (not applicable) | 582 | 342 |

Inspection completeness also varies; see ciss_completeness.json. Counts are unweighted diagnostics, not q estimates. No binomial confidence intervals or national extrapolation applied.

The depth code records deformation extent, not a parts-replacement schedule. Pillar data are collected conditionally: code 8 cannot be recoded to zero damage. Front-impact records therefore cannot be classified as exterior-only simply because A-pillar damage is not recorded. Repeated impacts mean treating CDC rows as independent claims would also overcount some vehicles. No engineering validation links the nine depth categories to our three provisional repair bundles. We did not impose arbitrary depth thresholds to fabricate that link.

Source definitions: CISS2024 Analytical User Manual printed pp. 50–52 (body type), p. 64 (inspection), pp. 113–118 (CDC and depth), pp. 123–124 (pillar fields). Exact pages can also be located by column names in the retained extracted text. Original manual: https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813771 ; data: https://static.nhtsa.gov/nhtsa/downloads/CISS/2024/CISS_2024_CSV_files.zip

## Provider search and source disposition
Five targeted web queries covered CCC front bumper/headlamp claim frequencies, Mitchell front components/frequency, Mitchell parts occurring together, Mitchell's 2024 impact release, and CCC co-occurrence. Relevant original materials inspected:

- CCC Crash Course 2018, PDF pp. 23–25 (printed 44–49), figures 32–34: CY2017 front-primary-impact repairable appraisals for two anonymous sedans. Contains repair-dollar distributions and differences in individual component appearance across ADAS groups. Not joint component frequencies, not older SUV/car calibration. Do not interpret difference percentages as absolute occurrence rates. Source https://preview.thenewsmarket.com/Previews/3CIS/DocumentAssets/577096.pdf . Direct Python download failed certificate validation; system curl succeeded without disabling certificate verification. Original file retained with hash.
- Mitchell Q3 2024 release: ICE front/rear primary-impact shares 31.59%/27.57% among its described repairable-claims comparison. Population, impact coding, powertrain and age aggregation differ from CRSS. This reinforces that CRSS shares must not silently become claim-frequency weights. Not target-cohort q. https://www.mitchell.com/insights/news-release/auto-physical-damage/primary-point-impact-contributing-differences-claims
- CCC Parts Dashboard and audit-guideline documentation surfaced again; examples and rules are not observed joint distributions. No evidence of absence across all possible provider products is claimed.

## Sensitivity component built
scope_grid.csv contains every three-scope probability vector on a 10-percentage-point grid: 66 distributions. Cross car and SUV distributions independently: 4,356 paired cases. Fractions are nonnegative and sum to one separately for each vehicle group. The grid is a mathematical stress range, not a plausible-confidence region, Monte Carlo draw or empirical distribution. No likelihoods, favored case, averaging across cases or assumed independence of damaged parts. Endpoints deliberately include extreme possibilities. Its 10-point spacing is an analyst choice for inspection, not measurement accuracy; a break-even root would later be solved continuously.

The provisional scopes are mutually exclusive COMPLETE repair bundles: exterior, intermediate, extensive. Final component/operation specifications and six matched full-bundle costs remain missing. Names alone do not establish an exhaustive real-world taxonomy. scope_inputs.json makes those costs null, not zero. evaluate.py refuses to emit dollar estimates until all six costs are provided. With inputs present, it calculates cost = sum(share × complete-bundle cost), then SUV minus car and ratio. Retain source/status for each future input. No frontend/rear/glass pooling or use of new-car AAA values as older-car costs.

For each group, extensive share is an editable sensitivity and exterior share can absorb a specified shift, holding intermediate fixed. Changing which scope supplies the shifted cases changes the cost effect and must be explicit.

Illustration of the arithmetic ONLY: shifting 10 percentage points from exterior to extensive increases average front-case cost by 0.10 × (extensive cost − exterior cost). A $1,000/$3,000/$5,000 assumed cost gap means +$100/+$300/+$500 per front case. These dollar gaps are unit sensitivities, NOT sourced repair prices or model assumptions. A shift is only valid when exterior share is at least 10% and extensive remains at most 100%.

Once costs exist, unrestricted scenario bounds are convex: each group's average lies between its cheapest and most expensive bundle. For a common distribution across groups, difference bounds are min/max of the three matched bundle cost differences. For independently varying distributions, difference bounds are min(SUV costs)−max(car costs) through max(SUV costs)−min(car costs). These are mathematical bounds conditional on the bundle specification, not statistical confidence intervals.

## Important modeling distinction
Joint repair scopes are needed for a distribution of whole bills and total-loss threshold crossings. They are not always necessary for the mean of an additive component-cost model: valid marginal operation frequencies can weight individual operation costs by linearity, without assuming components are independent. That shortcut still needs proper quantities, shared-labor treatment, sourcing and compatible populations. Current pooled historical part frequencies do not satisfy the target cohort requirement. Do not infer a bill distribution or TLF from marginal frequencies alone.

## QA, reproducibility and decision
build.py recreates the availability audit and sensitivity grid in under a second locally. Checks: vehicle/crash key uniqueness; 66 distributions/4,356 combinations; shares sum to one and nonnegative; arithmetic identity checks. evaluate.py was run with missing costs and correctly stopped without output. This verifies the missing-input guard, not empirical validity. No forecast inputs changed.

The next productive step is to price six consistently specified front-repair bundles (three per body type) and evaluate the sensitivity surface. Avoid extending the q search without a concrete new source. For total-loss analysis, additional compatible ACV/salvage and unrepaired-total-loss evidence is required; a repairable-only sample cannot identify that distribution.

Provenance: prior pass sources.jsonl includes the official CISS download and failed CCC request. This folder's sources.jsonl records the retained curl result, Mitchell capture, and references to existing manuals. Raw bytes remain in the adjacent feasibility raw folder. The local repository contains mirrored scripts, outputs and this research rationale; it does not imply a GitHub push or a raw-data upload.
