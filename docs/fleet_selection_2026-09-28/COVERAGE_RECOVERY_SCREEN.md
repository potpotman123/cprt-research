# Coverage recovery screen — 2026-09-28

Purpose: distinguish restoration of minor filed claims from restoration of insurer salvage supply. Work consisted of existing-file inspection, two targeted web queries, one primary-page read and small accounting calculations. No OCR, mass acquisition, regression fitting or workbook creation. Reproducible arithmetic: `coverage_screen.py`; output: `coverage_screen_results.json`.

## 1. Historical exposure/count bridge

CCC Q4 2024 report, through Q2 2024, saved in `raw/ccc/crash-course-2024-q4.txt`, line 105. Source: https://www.cccis.com/reports/crash-course-2024/q4. CCC attributes underlying figures to ISS Fast Track. Exposure is annualized earned car years, not policy counts. Arithmetic assumes the reported count and exposure changes have compatible bases; this was not independently audited against the underlying subscription dataset.

| Coverage | Exposure YoY | Paid claims YoY | Implied paid frequency YoY |
|---|---:|---:|---:|
| Collision | -2.0% | -5.7% | -3.78% |
| Property damage liability | -2.7% | -3.6% | -0.92% |
| Comprehensive | -2.4% | -2.8% | -0.41% |

Frequency factor = paid-count factor / exposure factor. Collision contraction cannot be explained by exposure contraction alone. Its residual includes accident incidence, filing, mix and payment timing, not just deductibles.

Collision exposure relative to liability exposure actually increased 0.72%. Thus this particular aggregate period does not demonstrate an industry shift from collision to liability-only. It does not refute survey evidence or later developments: different reporting panels, coverage mix and timing remain possible. Do not infer nationwide coverage penetration without a compatible fleet/exposure population. No numeric primary-source match was located in this bounded search for the Substack's Q4 2025 exposure decline of 4.0%; leave it unverified.

## 2. The deductible series cannot independently identify adoption

Existing chart transcription `data/csv/ccc_deductible_share_quarterly.csv` gives $1,000+ deductibles in 24.5% of repairable collision claims in Q4 2024 and 28.1% in Q4 2025. This is NOT the fraction of policies with those deductibles.

Let E_H and E_L be high/lower-deductible covered exposure; r_H and r_L be recorded repairable-claim incidence per exposure. Observed high-deductible claim share is E_H*r_H/(E_H*r_H + E_L*r_L). Consequently, claim-share odds equal exposure odds multiplied by relative recorded incidence.

The observed claim-share odds increased 20.44%. Holding relative incidence fixed would imply exposure odds increased 20.44%; a 10% reduction in relative high-deductible incidence would require exposure odds to increase 33.82% to produce the same observation. Alternatively, unchanged exposure odds plus a 20.44% increase in relative incidence also fits. These are identification examples, not forecasts. Vehicle age, damage and repair/total selection also affect incidence.

Therefore, retire any interpretation of the old CPI-to-deductible-claim-share correlation as a calibrated adoption or filing elasticity. It is descriptive evidence only. Chart share growth is compatible with affordability pressure but does not measure the missing claims.

## 3. New primary-source observation

CCC, May 20, 2026 webinar recap, accessed September 28: https://www.cccis.com/news-and-insights/posts/crash-course-2026-webinar-recap, section on early-2026 volumes. Non-comprehensive claim volume: -1.6% YoY in Q1 2026 versus -5.7% for CY2025. Collision: -3.6% versus -8.5%; comprehensive: -12.6% versus -16%. This supports moderation in CCC's broader population, independently of Progressive. Quarter versus full-year comparisons are not sequential growth. The recap does not provide the repairable/total-loss split needed here or fully define its volume denominator. Do not join it directly to paid Fast Track counts.

The webpage was read successfully; no underlying webinar transcript or subscription tables were acquired. These are attributed analyst disclosures, not independently replicated counts.

## 4. What this means for the model

- Broad claims stabilization now has some primary evidence beyond one carrier. It is a competing bullish explanation to retain, not dismiss.
- Whether that stabilization raises auction supply remains unidentified. Seek matched quarterly total-loss valuation and repairable counts within the same CCC coverage population. A matched TLF plus claim count could substitute only after checking scope and timing.
- Do not mechanically roll a -5.7% claim trend into -1.6% and then separately add denominator-driven TLF gains: returning repairables can offset the TLF movement without changing total losses.
- Keep filed-claim frequency as the provisional observed input. Do not independently multiply an estimated filing rate onto it. Coverage and filing are separately reasoned mechanisms, but unavailable components should not masquerade as measured model parameters.
- Preserve cohort economics as the source of changes in the total-loss population and RPU. Pure return of small repairables contributes zero auction revenue in that limiting case. Restoration of coverage can contribute units, with RPU dependent on which age/body/value cohorts return.

## 5. Next bounded test and stopping rule

Search existing CCC quarterly reports, then a few public CCC updates, for Q1/Q2 2026 total-loss valuation counts and repairable counts on matching bases. Record reporting vintage, period, coverage and whether counts are valuations, appraisals or unique claims. If the paired data are absent, retain the observable claims trend as a validation target and an explicit uncertainty in total-loss conversion. Do not expand into scraping listings, fitting a precise premium-cycle recovery date, or purchasing data without discussing the cost and expected benefit with the user.
