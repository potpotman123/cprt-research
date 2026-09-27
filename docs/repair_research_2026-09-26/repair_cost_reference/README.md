# Historical front-repair distributions benchmarked to recent repair statistics

26 September 2026 ET. User authorized historical reference distributions plus current benchmarks. This is the first executable approximation, not a measured distribution for older SUVs or all front-impact crashes.

## What was built
Preserved four CCC series: two anonymous sedans, each split ADAS/no ADAS, CY2017 repairable collision appraisals with front primary impact. Figure 32A/B labels MY15–MY16. Do not pool the vehicles or equipment variants without composition weights. historical_bins.csv retains 11 printed cost brackets and all original percentages. Two series sum to 99.9%, two to 100%; normalized calculation weights divide by their own sum. No missing total-loss tail is invented.

historical_summary.csv contains midpoint-based means and bin-endpoint mean bounds. These are calculations from binned data, not reported exact sample means, standard errors or confidence intervals. They condition on the displayed bins representing the normalized reference distribution. Within-bin locations are unknown.

| Historical reference | Printed share above $6,000 | Approximate mean using bracket midpoints |
|---|---:|---:|
| Sedan 1, no ADAS | 14.4% | $3,265 |
| Sedan 1, ADAS | 13.7% | $3,193 |
| Sedan 2, no ADAS | 30.9% | $5,012 |
| Sedan 2, ADAS | 29.3% | $4,958 |

These differences justify keeping multiple distribution shapes. They do not establish an ADAS treatment effect or body-type premium. No sample counts are published in the extracted table, so sampling precision is unknown.

## Recent benchmarks
CCC 2026 report, 2025 observations, figure 34 and adjoining text: age six or newer mean $5,721, exceeding age seven-plus by $2,039. Derived older mean=$3,682, approximate because source dollars are rounded. Retain the broader age seven-plus and report's all-loss repairable context; this is not a 7–9-year-old sedan/SUV front-impact statistic. Source: https://www.cccis.com/reports/crash-course-2026

Mitchell Q2 2026 US repairable ICE average=$4,955, all model years, not restricted to front impact. Use as a separate cross-provider broad level check, not a substitute older-vehicle mean. Source: https://www.mitchell.com/insights/article/auto-physical-damage/plugged-in-ev-collision-insights-q2-2026

The benchmarks are not a low/high confidence interval. Differences can reflect age, provider, period, coverage, impact and reporting/repairability selection. No ratio between them is interpreted as an age effect.

## Explicit approximation
For each of the four historical shapes, separately align its modeled mean to each benchmark. This gives eight PROVISIONAL reference distributions:
1. Original probability for each bracket stays unchanged.
2. Represent each historical bracket by its midpoint for mean calculation.
3. Scale factor = selected benchmark mean / historical midpoint-based mean.
4. Multiply all bracket endpoints and midpoints by that factor.
5. Confirm sum(probability × scaled midpoint) equals selected benchmark.

benchmark_aligned_bins.csv contains those eight series and all coefficients. Equaling a benchmark is imposed by construction, not out-of-sample validation. The factors are NOT inflation estimates: they combine a different price period and different populations. Some factors are below one, which does not imply repair-price deflation. Both the distribution-shape transfer and assigning an all-impact mean to a front-impact reference are assumptions. No scenario is designated a measured or preferred base case.

This is a working dollar-scale reference that can be replaced by better matched evidence. It does not extrapolate the observed repairable histogram to totaled vehicles. CRSS impact weights were not multiplied into these distributions because their population/impact definitions differ. Windshield, side and rear estimates are not mixed into this front-reference shape.

## Next model parameters, currently unresolved
A front-impact versus all-impact mean adjustment remains needed, as do age 7–9 versus seven-plus and car/SUV/pickup relative-cost adjustments. Do not infer those factors from the two benchmark means. A model can expose these as separate sensitivities on the chosen reference; use documented matched-bundle evidence to constrain them. A component-based parts/labor bridge remains preferable for explaining any chosen adjustment but is not fabricated here.

For mean repair costs, marginal operation frequencies may suffice for an additive model. For total-loss thresholds, the distribution and its missing-total-loss portion matter. Neither benchmark identifies the omitted tail or its relationship with ACV and salvage. No TLF, earnings or valuation outputs have been recalibrated.

## Source and numerical audit
Historical source: CCC Crash Course 2018, PDF p.23 / printed pp.44–45, Figure 32A/B. https://preview.thenewsmarket.com/Previews/3CIS/DocumentAssets/577096.pdf . Original PDF remains in ../repair_frequency_feasibility/raw/ccc_front_2018.pdf; exact extracted table page is retained in raw/ccc2018_figure32.txt. build.py parses the four printed rows, rather than maintaining a second manual transcription.

An adjacent Figure 33A reports a $4,037 no-ADAS sedan-1 mean, whereas the normalized Figure 32A bracket-midpoint estimate is $3,265 and its displayed-bin upper-endpoint mean is $3,954. This apparent inconsistency/comparability issue is unresolved. Do not claim our midpoint number reproduces that reported mean or use both interchangeably. Keep Figure 32 as the explicitly selected histogram reference; sensitivity to historical shape remains essential. Figure 33B also uses different model-year labels from Figure 32B. Neither adjacent mean is used for the scale factor.

Checks: four series, 11 bins each, positive valid percentages, sums within rounding tolerance, normalized probabilities total one, all eight imposed means reconcile. Midpoint approximation does not preserve actual within-bin variation; percentile locations are only identified to brackets without extra assumptions. No fitted lognormal or synthetic claim records used.

This pass used two targeted search queries, primary pages and an existing PDF text layer. No OCR, paid acquisition, outreach or large collection. Raw current pages retained; source log records URL, timestamp, bytes and hash. sources.jsonl also records the local historical PDF hash. output_manifest.json fingerprints inputs, code and outputs. Reproduce with bundled Python: run build.py beside raw/ccc2018_figure32.txt. No external libraries needed for the calculation itself.
