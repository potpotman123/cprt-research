# Repair-frequency feasibility pass — 26 September 2026 ET

## Decision and scope
Completed provider-documentation audit, CRSS/CISS dictionary screening and one-year CRSS cohort table. Public crash data support damage-pattern proxies, not measured repair-operation or paid-claim frequencies. No revenue/TLF/valuation assumptions changed. No outreach, paid access, bulk OCR, photo classification or multi-year expansion. This is exploratory descriptive research; outcomes and comparisons were not preregistered.

## What was actually done and why
1. Read CCC's 12-page Parts Dashboard guide and Mitchell's 2018 KPI article. Purpose: verify an actual route to component operations instead of assuming product marketing implies an accessible national dataset. CCC describes repaired records and part-count/spend views, with age, repair/replace, loss-category and sourcing filters. The guide does not establish body-type cross-tabs or distinct-claim incidence denominators. Mitchell documents age-conditioned bumper repair analysis and custom other-part analysis, but no underlying public cohort counts. These products remain access leads, not acquired datasets.
2. Located official 2024 CRSS/CISS documentation and CRSS download. Selected 2024 because it is the latest year listed in the inspected CRSS directory. Dictionary screening preceded data download. CRSS is broader than CISS for an initial impact-mix table; CISS selection requires a qualifying tow-away crash and cannot stand in for all claims.
3. Downloaded one 50,891,020-byte CRSS ZIP. Used only accident and vehicle tables. This is a small local structured-data calculation, not token-by-token processing. Downloaded original manuals and kept response bytes/hashes. The NHTSA publication endpoint returned PDF bytes wrapped in multipart content despite HTTP 200: extraction strips through the PDF signature/end marker into a separate file, retaining the original. CISS ROSA mirror and web CCC fetch failed; official publication endpoint and direct CCC download succeeded. Failures are retained in sources.jsonl.
4. Parsed existing PDF text locally, then inspected targeted field definitions. No OCR. CRSS manual printed pp. 13–14: survey design/variance; 106–108: NCSA body types; 136–138: impact and damage. CISS manual printed pp. 113 onward: event-level CDC damage measurements; pp. 123–124: pillar damage fields, conditionally collected. No complete repair-operation/payment frequency schema was established in this screen. CISS was not downloaded or analyzed beyond the manual.
5. Built cohort ratios and design-aware standard errors. Original data, executable scripts, QA and exact outputs are retained. A probability sample is preferable to public estimate uploads for frequencies because the selection and weights are documented. CRSS still samples police-reported crashes, not insurance claims.

## Exact estimand and coding
Unit: an in-transport vehicle involvement in a sampled 2024 police-reported crash, as represented in VEHICLE. Not unique owners, annual insured vehicles, repairs, claims or auction vehicles. Multiple vehicles in one crash remain separate vehicle observations; dependence is retained in PSU-level variance totals.

Join VEHICLE to ACCIDENT on CASENUM, many-to-one. Check unique vehicle keys (CASENUM, VEH_NO), unique crash keys, and identical weight/design fields across the join. No joins to person or repeated-event tables, avoiding row multiplication.

Analyst-defined NCSA BODY_TYP groups: Car={1,2,3,4,5,6,7,8,9,17}; SUV={14,15,16,19}; Pickup={32,33,34,39}; Minivan={20}. Exclude other and unresolved types. These are explicitly NCSA-code groups, not the agency's newer vPIC-based standard analytical classification. Classification robustness against vPIC has not been tested. Do not silently compare with published vPIC cohort totals.

Age=max(0, crash YEAR−MOD_YEAR), with raw valid model years 1900 through crash year+1. Next-year models assigned age zero and counted separately. Unknown/model-year sentinel codes excluded; no imputed model year used. Bins 0–3, 4–6, 7–9, 10–12, 13+. This is model-year age, not exact time since manufacture or registration.

Front initial impact={11,12,1}; rear={5,6,7}; unknown initial impact={98,99}. Side-specific codes, noncollision, top, undercarriage and remaining categories are retained in the denominator, not silently reclassified. Thus front+rear need not equal 100%. Initial impact is not all damaged areas or maximum-damage location.

Disabling damage: DEFORMED=6. Unknown damage severity={7,8,9}; code 7 means damage reported but extent unknown. All retained cohort vehicles, including unknown and no-damage records, form each ratio denominator. Police operational damage is not structural repair scope or an insurer total-loss determination.

## Formulas and uncertainty
For a cohort D and outcome y, p=sum_D(weight*y)/sum_D(weight). Use WEIGHT; never treat survey-weighted totals as raw sample counts. Output sample_n separately.

Taylor ratio linearization: for each record in D, u_i=w_i*(y_i−p)/sum_D(w). Sum u_i within (PSUSTRAT, PSU_VAR), using zero for every out-of-domain PSU. Variance=sum_h[m_h/(m_h−1)*sum_j(U_hj−mean_h(U))^2]. Standard error=sqrt(variance). With-replacement first-stage approximation, no finite-population correction, consistent with the manual's first-stage guidance. All 25 design strata and 67 variance PSUs retained; no singleton strata. These are not simple-binomial standard errors. SEs exclude coding error, missingness bias and other nonsampling errors. No pairwise significance or causal tests performed. Do not infer difference SEs by assuming cohort independence.

## QA and results
51,658 crash rows; 90,641 vehicle rows; 73,875 retained. Excluded 15,024 outside selected/known body groups, then 1,742 missing/invalid model years. Included 263 next-model-year vehicles at age zero. Unique keys and all join weight/design checks passed. cohort_table.csv contains 20 cohort rows, weighted ratios and SEs. Raw counts are sufficient to attempt descriptive tables; this does not establish representativeness for insurance claims.

| Age 7–9 | Sample n | Front % (SE pp) | Rear % (SE pp) | Disabling % (SE pp) | Unknown damage % (SE pp) |
|---|---:|---:|---:|---:|---:|
| Car | 6,921 | 56.0 (0.7) | 24.5 (0.6) | 30.7 (1.5) | 22.1 (4.6) |
| SUV | 3,655 | 54.9 (1.0) | 28.0 (1.1) | 26.8 (1.2) | 16.0 (4.4) |
| Pickup | 1,366 | 57.3 (1.7) | 21.3 (1.5) | 20.7 (1.5) | 16.2 (3.6) |

This creates a testable hypothesis: cohort impact mix may change weighted repair economics. Competing explanations include driving conditions, driver selection, vehicle use, model composition, reporting and coding differences. Unknown damage shares differ materially. An observed lower disabling share is not proof of cheaper repairs or lower TLF. Conditioning only on known severity could add selection bias; no missing-at-random assumption is made.

## Stop/go decision
GO for a cheap classification/missingness sensitivity before further inference. Provider data requirement remains distinct claims by age/body/loss category, component involvement, repair/replace and joint scope counts, including estimate version and disposition. CISS may refine damage mechanisms after its conditional collection rules are checked; pillar damage is not a repair decision. STOP before interpreting crash proxies as operation weights, or acquiring paid data/large case collections without user approval. This pass does not solve the missing component-operation incidence.

## Reproduction and sources
Run extract_manuals.py for saved manual text; run analyze.py for cohort_table.csv and qa.json using bundled Python. fetch.py logs URL, actual retrieval UTC, HTTP result, byte count and SHA-256; rerunning fetches current remote bytes, whereas reproducing this result uses saved bytes. output_manifest.json hashes this run's scripts and derived outputs. No software-package dependencies needed for analysis beyond Python standard library; PDF extraction uses pypdf.

Official data: https://static.nhtsa.gov/nhtsa/downloads/CRSS/2024/CRSS2024CSV.zip
CRSS manual: https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813796
CISS manual: https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813771
CCC: https://help.cccis.com/training/insurance_company/analytics/visual/PartsDashboard.pdf
Mitchell: https://www.mitchell.com/insights/article/auto-physical-damage/kpi-spotlight-percentage-repair-individual-part-types
Directory discovery: https://www.nhtsa.gov/file-downloads?p=nhtsa/downloads/CRSS/2024/ and corresponding CISS directory. Web discovery requests are described here, not retroactively represented as raw HTTP downloads in sources.jsonl.
