# Selected total-loss value check — 2026-09-28

## Result

The joint repair-bill/TLF fits fail a provisional external-value cross-check. Do not adopt their higher ACV scales. This is a material warning, not a perfectly matched statistical rejection: available CCC value data exclude comprehensive while the age-rate calibration and conditional age mix use all-loss data.

| Case | Mean modeled pre-loss value among selected total losses |
|---|---:|
| Original dispersion/value scale, CY2025 model age mix | $12,386 |
| Original dispersion/value scale, conditional CCC age mix | $12,577 |
| Joint fit, conditional CCC age mix | $21,316 |
| Joint fit, CY2025 model age mix | $21,846 |
| CCC CY2025 non-comprehensive valuation benchmark | $13,610 |

Original-dispersion rows refit age medians continuously to the same TLF targets; they are not a verbatim nine-state workbook output. The joint fits exceed the provisional benchmark by 56.6–60.5%. The original values are closer, but that does not validate the original repair distribution or age/body value structure.

## Source and acquisition

Saved report `raw/ccc/crash-course-2026.html` identifies Figure 22's image URL. One 56KB chart image was downloaded and visually read; no OCR or video processing. Retained as `ccc_2026_figure22.webp` with SHA256 in `selected_value_results.json`. Live report retrieval returned 403; the CDN image succeeded. No claim of a successful live report refresh.

Report: https://www.cccis.com/reports/crash-course-2026

Image: https://cdn.prod.website-files.com/677e7ecbb3dbbe98615cde30/69cada2ee6e49394a5609441_Picture22-p-1600.webp

The image specifies CCC national non-comprehensive total-loss valuations, CY2025 through December, average adjusted vehicle value $13,610. Despite wording in the chart title referencing age groups, this displayed chart has one aggregate bar per year, not separate age-group dollar levels. Do not invent age-specific benchmarks from it. CCC's report text describes valuations for potential total losses; valuations are not confirmed unique auction sales.

## Calculation

Within each age/body cohort, weight assumed pre-accident ACV by modeled total-loss probability and the historical claim weight. Divide summed value-weighted total losses by summed total losses. This compares selected values, not the $10,000 age-ten car input or auction hammer prices. The model has one ACV per age/body cohort, so within-cohort value heterogeneity remains absent.

The value target was not used in the preceding joint fits. This is an additional diagnostic beyond the eight in-sample calibration targets. Inputs/output hashes and reproducible code are retained in `selected_value_check.py` and its result JSON. The shared joint-calibration script now exports selected values; its original fitted parameters are unchanged.

## Reverse check

Hold each joint fit's dispersion fixed but scale ACV and repair bills together so selected ACV equals $13,610. TLF remains unchanged by this common scaling. The implied repaired-vehicle mean bills fall to:

| Weights | Ages 0–6 | Ages 7+ |
|---|---:|---:|
| Conditional CCC | $3,653 | $2,351 |
| Model CY2025 | $3,564 | $2,294 |
| CCC repair benchmarks | $5,721 | $3,682 |

This is a conditional reverse check, not a newly optimized constrained fit. It demonstrates that the earlier mathematical reconciliation depended on the large common value scale. It does not prove no more flexible distribution can match the data.

## Model decision

Keep all joint fits as rejected-for-adoption diagnostics. Neither select the original base as correct nor add an arbitrary revenue adjustment. Unknowns include the within-cohort ACV distribution, age depreciation slope, broad lognormal damage distribution, deterministic damage/recovery link, body ratios, and coverage/population compatibility. This test cannot isolate which is responsible.

Next cheap useful step: hold an explicitly provisional value anchor near the observed selected value and test whether younger/older repair-cost dispersion or a more realistic age-value curve can reconcile the two repaired means without moving the aggregate selected value. Compare the minimum parameter changes required and the resulting unit sensitivities. First reuse any age-value charts already saved to constrain the curve; do not add parameters simply to force a perfect fit. Any resulting fit remains conditional until coverage and age/body selection are aligned.
