# Quarterly repairable / total-loss pair search

Date: 2026-09-28. Result: no compatible Q1/Q2 2026 pair located in the bounded sources checked. This is a search limitation, not proof the data do not exist.

## Scope and provenance

- Searched saved CCC quarterly reports for 2025 and annual Crash Course 2026 for valuation counts, repairable volumes and total-loss counts.
- Checked saved chart descriptions for apparent volume exhibits. Q1 2025 Figure 2 and Q4 2025 Figure 3 describe shares of claims, not absolute count series. Public Q1 2025 page also identifies its figure as a share chart: https://www.cccis.com/reports/crash-course-2025/q1. Did not digitize these charts: shares alone cannot establish counts.
- Ran five targeted public searches for CCC 2026 quarterly valuations/repairable counts and updates. Results surfaced the annual report, older quarterly reports and the May webinar recap, not a matched current-quarter pair.
- Attempted likely report URLs `/reports/crash-course-2026/q2` and `/q3`; browser retrieval failed. These guessed URLs and failures establish neither publication nor nonexistence.
- Re-read https://www.cccis.com/news-and-insights/posts/crash-course-2026-webinar-recap (May 20, 2026). Q1 aggregate claim-volume declines: all categories 3.3%, non-comprehensive 1.6%. No corresponding quarterly repairable/valuation split or matching quarterly TLF was supplied in the recap.

## Compatibility inventory

| Evidence | Period | Population / measurement | Permitted use |
|---|---|---|---|
| CCC annual total-loss valuations and repairable volumes | CY2025 YoY | All categories and non-comprehensive; valuations versus repairable claims | Directional annual evidence; previous reconciliation fails |
| CCC share charts in 2025 quarterly reports | Historical monthly/quarterly periods through 2025 | Claims flagged total loss / claims | Rates only; not counts |
| CCC webinar volume update | Q1 2026 YoY | Coverage-specific volume, full counting methodology unspecified | Observed claim-volume trend; not auction units |
| ISS Fast Track via CCC | Earlier reported periods | Paid counts / earned exposure | Exposure-frequency accounting; do not merge into CCC appraisal population |

CCC's report caveat distinguishes electronic appraisals transmitted through its network from total-loss valuations processed by CCC. Same provider does not guarantee common population, unique vehicles, or identical timing. See saved Q4 2025 report line 239 and annual 2026 line 390.

## A useful conditional threshold

With compatible populations, total-loss count growth factor equals claim-count growth factor times the relative TLF factor. Thus Q1 non-comprehensive claims down 1.6% would require TLF to rise 1.626% relatively for total-loss counts to stay flat. All-category claims down 3.3% would require a 3.413% relative TLF increase. These are accounting thresholds, not measured total-loss outcomes.

For illustration only, start non-comprehensive TLF at 24%. With claims down 1.6%:

| Assumed ending TLF | Implied total-loss count change |
|---:|---:|
| 24.0% | -1.60% |
| 24.5% | +0.45% |
| 25.0% | +2.50% |

Flat total losses would require approximately 24.390% ending TLF. The starting 24% is explicitly hypothetical, not an observed Q1 baseline, and these cases are not a probability distribution. Arithmetic is reproducible in `quarterly_pair_check.py` / `quarterly_pair_results.json`.

## Decision for the build

Do not adopt claims stabilization as a quantified Copart unit rebound. Equally, do not infer continuing total-loss decline from slightly negative overall claim growth. The distinction can turn on less than half a percentage point of TLF, making period/population mismatches consequential.

Keep this as an unresolved validation target while continuing the cohort repair/value engine. That engine should compute total losses and the corresponding observed TLF together; the headline TLF should not be an independent additional tailwind. Copart allocation, inventory-to-sale timing and selected-vehicle RPU still follow downstream.

Potential future document request, if convenient: CCC's Q1 and Q2 2026 tables with total-loss valuations and repairable appraisals, current and prior-year counts, separately all coverages and non-comprehensive, and the denominator/methodology footnotes. No contact was sent and no paid access, video transcription, OCR or bulk scrape was attempted. Do not spend heavily extracting percentage-only charts to solve a missing-count problem.
