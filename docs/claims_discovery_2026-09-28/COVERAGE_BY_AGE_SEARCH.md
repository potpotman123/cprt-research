# Coverage-by-age evidence search

28 September 2026. Fourteen targeted discovery queries and two primary-authored source reads. No paid acquisition, OCR, bulk scraping, outreach or model changes.

## Question and method

We need collision-covered exposure by vehicle age, preferably repeated over time and matched to claim frequency. First search exact coverage/age terms; then broaden to policy-validation businesses, residual-market insurer briefings, surveys and statistical reporting. Inspect original methods before treating a number as usable. This is cheaper and more direct than reconstructing coverage from auction listings, which omit vehicles never assigned to auction.

An insurer's policy records are closer to the desired denominator than selected claims. However, policy counts are not automatically vehicle-years, a portfolio average age is not an age-specific coverage share, and a changing cross-section is not necessarily the same policyholders dropping coverage. These criteria govern acceptance.

## Lead 1: policy-validation data provide a historical precedent

[Quality Planning's March 29, 2011 release](https://www.globenewswire.com/news-release/2011/03/29/1207850/0/en/During-Recession-American-Drivers-Assumed-More-Risk-to-Reduce-Auto-Insurance-Costs.html) describes analysis of 2006–2010 policies, with 59.8 million vehicles across the full period. It reports older vehicles without collision or comprehensive rising from53% to63%. Narrative and example define older as10+; a contradictory “up to10” phrase appears in the methods and is flagged. Annual counts, matched-panel design and separate collision/comprehensive tables are not supplied.

**Use:** historical evidence that policy coverage choices can change within an older-vehicle population, rather than an inference from falling claims. **Do not use:** current coverage levels, a13+ coefficient, annual decline rate, a longitudinal dropout estimate, or national penetration. The sample total must not be described as59.8 million unique vehicles. The combined coverage wording does not justify recovering collision-only coverage by subtraction. No later comparable update was located in this bounded search.

## Lead 2: a recent insurer briefing contains relevant fields, but not their cross-tab

[Maryland Auto's March2025 Howard County delegation briefing](https://chaowu.org/wp-content/uploads/2025/03/Maryland-Automobile-Insurance-Fund-Howard-County-Delegation-Brief-3-5-25.pdf), pp.5,9, gives whole-portfolio average vehicle age12.5 and70% liability-only policies; Howard County average age13.4 and65% liability-only. The remaining35% there includes comprehensive and/or collision. This is a residual-market insurer serving applicants rejected or nonrenewed by private insurers. Figures are portfolio summaries, not age-specific rates or earned vehicle-years; exact snapshot dates are not stated on those slides.

**Use:** confirms a recent insurer publication can expose age and coverage fields outside claims reports. **Do not use:**35% collision penetration for13-year-old vehicles, U.S. fleet coverage, or a change over time. Different geography and risk selection make extrapolation particularly weak. Premium examples in the deck also change liability limits and other coverages, so their differences cannot isolate the price of adding collision.

## Other routes and stopping decision

HLDI search results included insured-exposure appendices but selected newer vehicles, motorcycles or driver-age studies; none was a verified13+ vehicle-age coverage table. A CCC glossary search surfaced a vehicle-age definition, but the page failed to open; no new input was taken. An agent website advertised quote records, but quote requests are not bound policies, and its provenance/sample controls were not verified. Foreign surveys and rating manuals were not substituted for U.S. observed coverage choices.

The historical policy study is a more direct mechanism observation than our prior quotient of mismatched curves. It still does not identify2024–25 behavior. The recent insurer deck shows a promising publication type but fails the cross-tab requirement. Do not continue broad searching indefinitely or insert either source's percentages into the forecast.

## Concrete next evidence request / public-document target

Seek a current policy-data table with calendar period, vehicle model year/age, collision indicator, comprehensive indicator, liability indicator, vehicle count and earned vehicle-years. Require the same insurer panel across years; distinguish renewals from incoming business and deductible changes from coverage removal. Split13–15,16–19,20+ if exact age is unavailable.

For a public-document continuation, prioritize residual-market insurer annual reports and legislative briefings containing the actual cross-tab, plus updated Quality Planning/Verisk policy-coverage research. A narrowly scoped aggregate table would be preferable to individual quote or policy records. No request has been sent; contacting a provider would require user authorization.

The alternative is to keep age coverage as an explicit unmeasured component, use observed compatible claim frequency at the aggregate level, and spend the next research increment on damage selection or service adoption. That may be more efficient than forcing a complete decomposition of a denominator we cannot observe.

## Search log

1. "vehicle age" "collision" "coverage penetration"
2. "vehicle age" "collision coverage" "percent" insurance
3. "HLDI" "exposure" "age" "coverage" older
4. "vehicle age" "comprehensive" "take-up" insurance
5. "vehicle age" "collision" "insured vehicle years" "15"
6. "collision coverage" "older vehicles" "percent" study
7. "automobile" "model year" "earned exposures" statistical plan
8. "vehicle age" "insurance coverage" "survey" United States
9. "Quality Planning" "older vehicles" coverage 2024
10. site.verisk.com "vehicle age" "coverage" collision
11. "collision" "coverage" "vehicle age" "LexisNexis"
12. "collision coverage" "vehicle age" data 2025 2024
13. "older vehicles" "coverage" "Quality Planning" study
14. "insurance" "liability only" "vehicle age" data

Sources accessed September28,2026 via web text extraction. No source PDF was transcribed into a workbook, and no historical/forecast input was overwritten. Above observations are preserved with direct source URLs and page/section locators; whole copyrighted publications are not copied into Git.

## Bounded follow-up: current coverage-mix evidence

28 September 2026. Six queries, two document opens, no OCR, paid collection or forecast changes. The targeted continuation found [Maryland Auto's January 22, 2026 Senate Finance briefing](https://mgaleg.maryland.gov/meeting_material/2026/fin%20-%20134135033962649181%20-%20Briefing%20Materials%20-%20MAIF%20and%20MIA%2001-22-26%202PM.pdf). Printed p.6 / PDF page7 reports liability-only policies at 62.75% of the book in2023 and78.7% in2025. This is a current within-insurer change in coverage composition, stronger temporal evidence than the earlier portfolio snapshot. It remains a residual-market portfolio, without a vehicle-age cross-tab or matched renewal panel.

Interpretation: switching coverage, differential exits and incoming-customer mix can all change the share. The disclosure does not distinguish them. It cannot establish that individual customers dropped collision coverage, quantify collision-only penetration, or identify a national13+ coefficient. Preserve as observed portfolio composition only; do not map it directly into Copart units or TLF.

Architecture implication (inference, not source finding): coverage selection and small-claim nonfiling are distinct filters. Dropping own-damage coverage can remove both repairable and total-loss claims from that coverage channel; omitting small claims selectively removes the repairable denominator. Therefore coverage loss alone does not prove higher TLF. The direction depends on which vehicles/risks leave the observed claims population, and alternative recovery routes must remain separate. Applying a coverage reduction on top of an already calibrated claims-per-fleet-vehicle rate would risk double counting.

Stopping decision: no age-by-coverage time series identified in this pass. Keep the coverage decomposition unmeasured and retain the existing combined claims propensity provisionally; do not multiply in Maryland percentages. Next useful model check is to document exactly which filters the combined rate already contains before further calibration. Reopen empirical coverage estimation only with a concrete compatible dataset lead.

Queries: `site.mymarylandauto.com "vehicle age" coverage`; `site.aipso.com "model year" "collision" exposures`; `site.verisk.com "older vehicles" "coverage" collision`; `"vehicle age" "collision coverage" study policy data`; `"Maryland Auto" "2025" "annual report" coverage`; `"Quality Planning" "coverage" "vehicle" 2024 2025`.

Other opened candidate: [AIPSO Hawaii filing HI13-01](https://cca.hawaii.gov/ins/files/2013/12/AIPSO_Filing_HI_13-01.pdf). Search surfaced a model-year/coverage table, but targeted text lookup did not resolve it; no statistic accepted. Most other hits were prior sources, unrelated coverage studies or irrelevant results. Stop rather than expanding that low-yield branch.
