# Joint units and RPU research: bounded execution plan

2026-09-28. This plan follows a targeted read of existing transcript text and existing valuation audits. No new scraping, OCR, simulation, workbook changes, or paid acquisition was performed. Hypotheses are not adopted forecasts. Large collection or computational work requires a separate proposal and user approval.

## Question and perimeter

Which mechanisms jointly explain claim supply, Copart allocation, completed insurance sales, and service revenue per unit? Do their next-two-quarter effects differ materially from dated analyst forecasts? Start with US insurance; retain an explicit US non-insurance and acquisition perimeter when comparing to aggregate US revenue/RPU. Do not multiply an insurance unit series by all-US RPU.

## New source observations

- raw/transcripts/call_2025-02-20.txt, around lines 280–295: management describes Title Express pilots expanding across carrier accounts; mature clients generally use it for nearly all titles. This supports an account-rollout model, not proof of industry saturation.
- raw/transcripts/call_2026-05-21.txt, around lines 395–406: analyst question describes prior pricing actions as fully lapped. Management identifies service penetration, selling prices and non-insurance mix as RPU drivers. The anniversary claim is the analyst's premise, not independently verified implementation history.
- Same May call, around lines 471–480: management discusses expanded long-haul delivery and approximately $15m incremental facility operating costs associated with it. Costs do not identify revenue without scope and margin assumptions.
- raw/transcripts/call_2026-09-10.txt, around lines 569–579: management explicitly attributes RPU increases to products including Title Express but declines to disclose fee mix; points to additional product opportunities.
- raw/transcripts/call_2026-02-19.txt, around lines 115–124: management describes faster title-related cycle times. Any fee saturation analysis must also consider potential assignment-to-sale timing benefits.
- docs/repair_research_2026-09-26/value_recovery_audit/README.md: small older-vehicle retail proxy panel gives crossover/sedan ratio about 1.128, versus the unvalidated legacy 1.50 assumption. Neither ratio is an adopted insurer-ACV estimate. Existing database lacks paired pre-loss values and completed sale proceeds.

## Track A: service adoption and prospective RPU deceleration

1. Build a compact historical source ledger from existing transcript text, filings and supplied analyst models. Record date, page/line, speaker, geography, vehicle population, units/assignments distinction, reported versus estimated values and accounting scope. Search existing text first; inspect only specific ambiguous source pages. No bulk OCR.
2. Reconcile same-population service revenue and unit growth to implied RPU growth. Separate domestic/international, insurance/non-insurance and acquisitions. Treat unexplained differences as unidentified; do not label residual growth as ancillary services.
3. Represent Title Express activity as eligible carrier title volume times account adoption/rollout, and recognized revenue per title where supported. Track carrier wins and within-account rollout separately. Distinguish title-service allocation from auction allocation; verify whether volumes extend beyond Copart auction assignments.
4. Represent delivery as eligible jobs times uptake times recognized revenue per job, including route/service mix. Check gross/net revenue presentation. Do not convert cost increases into exact revenue without justified margin and scope.
5. Bound contribution with available disclosures. Competing explanations: continuing new-account wins, new products, price changes, sale-price effects and non-insurance mix. Account saturation is not market saturation. Model cycle-time effects once in the sales conversion stage.
6. Use latest available dated analyst forecasts as comparators, retaining older forecasts as historical references. Calculate how much additional service revenue each RPU forecast requires after independently supported price/mix effects. Test whether required adoption is feasible before fitting any adoption curve.
7. Continue only if a material two-quarter gap survives plausible bounds and has a dated observable test. Otherwise retain as an uncertainty, not a headline short. Fee-anniversary work is secondary until timing is independently established.

## Track B: crossovers, fleet aging, damage selection and fees

1. Start with the same-age RAV4/Camry and CR-V/Accord economic comparison as an illustration. Use pickups separately. A vehicle is not assumed to be allocated to Copart merely because its carrier is specified.
2. Audit existing model-year/body classifications, birth cohorts, survival and claim weights. Use national source cohorts to forecast exposure; auction listings are a selected sample and cannot estimate the insured fleet directly. Preserve age, body and within-cohort economic changes separately.
3. First calculate break-even combinations of pre-loss value, repair costs and recovery using existing inputs. This ranks which missing measurements could change sign or six-month magnitude before new collection.
4. Only if material, propose a small matched valuation panel: same model year, geography, mileage, condition, drivetrain and transparent trim treatment. Use accessible structured valuation tables. These remain retail proxies unless insurer valuations are obtained. Do not replace 1.50 with 1.128 mechanically.
5. Audit existing repair weights and transfer assumptions. CRSS impact shares are police-reported crash involvements, not insured repair-operation frequencies. AAA cases are narrow repair scenarios, not complete older-vehicle claims. Seek aligned CCC/Mitchell/HLDI tables already held before collecting more records.
6. Apply explicit damage-state costs and net-salvage assumptions to the economic totaling threshold. Derive both total-loss frequency and the condition distribution of selected vehicles. Record statutory/operational limitations. Differentiate gross auction proceeds from seller net salvage.
7. Apply carrier auction routing and allocation, then assignment-to-sale timing. Price only vehicles that reach the sale stage. Apply stored buyer fee schedules, transparent seller-fee scenarios and separately recognized services. Higher salvage recovery can both raise fees and make totaling more attractive; include both effects.
8. Reconcile to history and hold out a later period where possible. Fitting total-loss rates does not independently validate repair/value assumptions. Compare observations and predictions on the same denominator and calendar.
9. Aggregate actual projected cohort changes over two fiscal quarters. Report units, conditional auction prices, core fees, other services and total revenue. Stop promoting the mechanism if only extreme parameters or large invented mix shifts create material downside.

## Integration and decision rule

Revenue is summed over sold cohorts and service events; RPU is a derived summary on a compatible unit denominator. Do not independently add crossover, fleet-aging and damage-selection sensitivities that describe overlapping effects. Show interactions separately. Separate all-in US RPU from insurance-specific RPU. Compare with analyst forecasts on matched dates and business scope.

Immediate authorized work: existing-source ledger, historical comparability checks, and bounded deterministic break-even arithmetic. No large scrape, OCR, paid data, provider outreach or major simulation. Before escalation, present exact source/method, sample and coverage, cost and runtime where knowable, cheaper alternatives, failure conditions, and the decision the result could change. Do not claim an exact token cost in advance.

Deliverables: a sourced quarterly RPU bridge with unidentified portions visible; a joint cohort units/fees bridge; and a decision note selecting, weakening or rejecting each hypothesis. No workbook design work in this phase.
