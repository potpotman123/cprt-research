# Claim counts versus TLF: compatibility check

28 September 2026. Four queries, two primary-source page opens and targeted lookups, plus a small identity calculation. No forecast edits. Existing valuation/repairable figures were already recorded in `model/integrated_service_2026-09-28/WITHIN_AGE_ECONOMICS.md` and `JOINT_CLAIM_SELECTION.md`; they are not new discoveries. The new addition is the CCC May2026 recap and explicit cross-series reconciliation.

## Sources and observations

[CCC annual report](https://www.cccis.com/reports/crash-course-2026), text preceding Figures17 and31: CY2025 all-coverage repairable volume -9.7%, total-loss valuations -2.9%, flagged TLF23.1%, up0.8pp. Non-comprehensive: -8%, -0.2%, and23.9%, up1pp, respectively. Baseline TLF22.3% and22.9% are derived by subtraction, not separately extracted chart observations. These are valuations versus flagged claims versus repairable appraisals; do not assume a common exhaustive count population.

[CCC webinar recap, May20,2026](https://www.cccis.com/news-and-insights/posts/crash-course-2026-webinar-recap), “What's happening with claim volumes in early2026?”: total volume2025 -7.7%, Q1CY2026 -3.3%; non-comprehensive -5.7% and-1.6%; collision -8.5% and-3.6%. The comprehensive discussion identifies weather and theft as competing explanations. The recap supplies no stable-panel/revision reconciliation to the earlier annual report. These are count changes, not claims per insured vehicle-year, and calendar quarters, not Copart fiscal quarters.

## Arithmetic diagnostic

If C=T+R with identical population and timing, T1/T0=(C1/C0)×(p1/p0), and R1/R0=(C1/C0)×((1-p1)/(1-p0)).

| CY2025 comparison | All coverage | Non-comprehensive |
|---|---:|---:|
| Totals growth implied by recap claims and annual TLF | -4.39% | -1.58% |
| Published valuation growth | -2.90% | -0.20% |
| Repairables growth implied by recap claims and annual TLF | -8.65% | -6.92% |
| Published repairables growth | -9.70% | -8.00% |

Conversely, treating valuations and repairables as an exhaustive pair yields TLF23.58%/24.37%, about0.48/0.47pp above published23.1%/23.9%. The discrepancy requires a definition, panel, timing or revision explanation; no cause is established. Do not fit a nonfiling coefficient to close it. Code/results: `count_compatibility.py` and `count_compatibility_results.json`.

## Decision

Directionally, reported TLF strength coexists with lower valuation volumes and weaker repairable activity. That supports separating numerator from denominator. It does not identify small-claim nonfiling versus fewer accidents, weather/theft, coverage removal, customer/panel mix or repair-to-total conversion. CCC's first-party concentration narrative is not a measured fraction of missing small claims.

The easing2026 volume declines are a counterpoint to mechanically extending2025 weakness. They are YoY rate improvements, not proof of sequential growth or a durable recovery. Preserve that counterevidence in the pitch.

Keep incremental nonfiling at zero pending identification. A useful next source must disclose compatible counts of flagged total-loss and repairable claims, coverage, matched calendar periods, stable panel and revision policy. Age-specific counts would be required to assign this effect to13+ vehicles. Avoid another broad search until a concrete dataset lead exists; this branch has supplied a diagnostic, not an adopted forecast driver.

Queries: `site.cccis.com 2026 "2025" "total loss" "volume"`; `site.cccis.com "2025" "22.8" "2024"`; `site.mitchell.com 2025 total loss frequency repairable claims volume 2026`; `site.cccis.com "2025" "9.7%"`. Mitchell results were screened but not used to combine different vendor panels. Sources accessed2026-09-28; no bulk collection or OCR.
