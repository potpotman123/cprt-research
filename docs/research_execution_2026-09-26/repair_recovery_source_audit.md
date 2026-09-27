# Repair costs and salvage recoveries: bounded source audit

September 26, 2026. Scope: existing local CCC reports and previously extracted HLDI figures, plus ten targeted search queries and six attempted primary-source page/PDF opens. No listing collection, OCR, account access, paid purchase, provider outreach or workbook changes. Search results were screened for primary sources; unrelated maintenance-cost websites and unverified auction-history listings were not used as measurements.

## Result

The audit did not locate an accessible dataset measuring comparable-age, comparable-damage repair estimates and net salvage recovery for cars versus SUVs. It did identify a documented recovery-report structure containing relevant fields, a direct but narrow repair-cost experiment, and evidence that aggregate claims severity can move because the composition of crashes changes. These improve the research design but do not identify the model's decisive ratios.

The negative body-mix result remains a scenario. The correct next decision is between seeking legitimate access to a small, appropriate export and retaining explicit bounds while developing a different near-term earnings mechanism. A large public-listing scrape is not justified by these findings.

## Sources and what each can establish

### A. Mitchell WorkCenter Salvage Recovery documentation

[Official documentation](https://wwwca.mymitchell.com/tchs/helpfiles/WC/1033/Content/82275.htm)

Verified definitions include gross proceeds, ACV completeness, recovery after pool expenses, recovery after additional charges, vehicle-type filters and assignment-to-sale duration. This is an application help page, not an export of observations. Age/damage stratification and export rights were not established. Its financial recovery measures are relevant; its assignment clock is not proof of physical yard occupancy. Access to actual customer reports remains unestablished.

### B. CCC salvage and collision-estimating documentation

[Salvage workflow glossary](https://help.cccis.com/webhelp/insurance_company/thecccportal/Content/Insurance/AnalyticsTableau/CategorizedGlossariesDropdn/SalvageWorkflowGlossary.htm)

[Collision estimating glossary](https://help.cccis.com/webhelp/insurance_company/thecccportal/Content/Insurance/Analytics/Categorized%20Glossaries%20with%20Dropdn/Collision%20Estimating%20Glossary.htm)

Search-indexed documentation identifies repair estimates, vehicle categories and workflow measures. Full-page retrieval failed, including a 403 for the collision glossary; no access restrictions were bypassed. Treat these as leads to report schemas, not independently audited field availability or a public dataset. A cached definition does not establish populated records, permissible export or a join between claims and salvage outcomes.

### C. CCC Q1 2025 Crash Course

[Official report](https://www.cccis.com/reports/crash-course-2025/q1)

The local report and primary search result discuss repairable appraisal costs, vehicle-age composition and fuel-type repair differences. They do not provide the required matched SUV/car repair ratio. The report already attributes moderation in repair costs partly to total losses and age composition. Consequently the general selection argument is not new relative to the source corpus; differentiated work must quantify its effect on a specific forecast. Fuel-type and young-vehicle comparisons cannot be relabeled body-type effects for older vehicles.

### D. IIHS controlled low-speed F-150 comparison, July 2015

[Official article](https://www.iihs.org/news/detail/pricier-repairs-for-aluminum-f-150-than-steel-model-in-fender-benders)

Two low-speed impact configurations produced combined repair costs 26% higher for the aluminum 2015 F-150 than its steel predecessor. This is actual repair-cost evidence under specified test conditions. It compares pickup generations, not SUVs with cars, and does not estimate older vehicles near total-loss thresholds. It cannot be inserted as the model's repair ratio or interpreted as proof that the 18% break-even threshold is crossed.

### E. HLDI F-150 follow-up, December 2018

[Primary bulletin](https://www.iihs.org/media/3d59fbc4-04c5-427e-af4a-d85f93948e7a/PlUPgw/HLDI%20Research/Bulletins/hldi_bulletin_35.46.pdf)

The subsequent insurance analysis found a relative decline in claim severity after accounting for trends in comparison pickups, despite the earlier repair-test result. The bulletin discusses parts pricing, design and repair capability. This illustrates why a narrow experiment cannot simply determine average insurance outcomes. It still does not supply age-matched SUV/car repair costs or salvage recoveries. Old model years in a historical study are not evidence about those vehicles at today's older ages.

### F. IIHS explanation of crash-avoidance effects

[Official explanation](https://www.iihs.org/news/detail/how-crash-avoidance-tech-simultaneously-raises-and-slashes-repair-costs)

IIHS explains that preventing lower-speed crashes can increase average severity among the remaining claims. This supports treating claim composition as a competing explanation for differences in average payments. It does not establish the magnitude of that effect for our vehicle categories. Nor does it imply HLDI severity is useless: it remains evidence about claim costs, but is not an identified repair-cost distribution for our model.

## Separate SUVs from pickups using the local HLDI table

The existing local primary table permits separate descriptive averages. Using the previous report's mini-to-large four-door-car comparator and equal weight for the available size rows gives:

| Category | Paid-claim severity relative to cars | Claim frequency relative to cars |
|---|---:|---:|
| Non-luxury SUVs | 0.997 | 0.682 |
| Pickups | 1.054 | 0.629 |
| Minivans | 0.953 | 0.726 |

Calculated from the class means already audited in `body_sensitivity_results.json`; car comparator severity is 95.5 and frequency 137.75 on the source indices. These are not exposure-weighted estimates of actual Copart cohorts. They refer to the source's recent-model-year population, not matched older vehicles. Luxury SUVs remain separate in the source. Neither the severity ratios nor the frequency ratios should be transplanted directly into the forecast.

The useful result is that category distinctions exist and can be retained without new scraping. It does not validate a single body-specific totaling curve. Since the observed listing change is primarily SUVs/crossovers, pickup experiments should be supporting comparisons, not the central repair-cost calibration.

## Concrete data specification for any future access inquiry

No inquiry has been sent. The user previously stated that no provider access exists outside the repository. Do not ask that same access question again or assume an export is available.

For repair/totaling economics, the minimum useful claims extract would include:

- Anonymous claim identifier and relevant dates, with initial versus final estimate timestamps.
- Model year and a consistent car/SUV/pickup classification, plus mileage if available.
- Coverage/loss type, major damage descriptors and drivable status.
- Repair estimate at the decision stage, distinguishing supplements and paid settlements.
- Pre-accident value, expected salvage recovery if recorded, and repair/total-loss disposition.
- Both repaired and totaled claims; insured exposure only if estimating claim frequency as well.

For recovery and operating economics, seek a linkable salvage extract containing completed-sale status, gross sale proceeds, ACV, pool expenses, advance charges, and actual arrival/sale/pickup dates where available. An assignment date or administrative lot-close date must not automatically substitute for physical arrival or departure.

First inspect an anonymized schema and small illustrative sample. Check essential field coverage, timestamp meanings and linkage before deciding sample size or paying for data. Matched age/body/damage strata and independence should determine the design; a large record count alone is not sufficient.

Define the net-recovery convention before comparison. Different reports subtract different expenses. A ratio of aggregate recovery dollars to aggregate ACV is also not the same as the equally weighted mean of vehicle-level recovery ratios. Missing ACV values must be reported and handled consistently.

## Recommended disposition

1. Keep the body-mix hypothesis active but parameter-bounded. No newly found source justifies replacing the 1.01 repair proxy with another point estimate.
2. Do not escalate public auction scraping to estimate totaling probability: it still excludes repaired claims and lacks the correct denominator.
3. If legitimate report access becomes feasible, request the schema/sample above before commissioning a study. Provider cost, rights and accessibility are unknown, and outreach or purchase requires explicit authorization.
4. Continue inexpensive work on the other mechanisms while this specific evidence gap remains unresolved. The documented workflow fields also clarify what a future capacity dataset would need, but no current utilization estimate follows from them.

This was a bounded search, not proof that suitable public data do not exist. The unresolved issue is access to comparable observations, not a need for more elaborate calculations on the current proxies.
