# Does changing composition within ages 13+ explain higher TLF?

28 September 2026. Cheap existing-data check, no new data collection or forecast changes. Annual CY2024 and CY2025 cohort snapshots; not observed CCC claim microdata.

## Finding

The existing fleet-cohort assumptions do not support a simple story that the 13+ claim population got older and therefore had higher TLF. Its modeled claims-weighted average age falls from 17.542 to 17.442 years. The fraction aged exactly 13 rises from 15.33% to 17.42%. The unweighted surviving fleet's average age is nearly flat, 19.359 to 19.347.

The recorded CCC 13+ TLF nevertheless rises from 43.6% to 45.3%, or 1.70 percentage points. A smooth legacy age curve applied to the modeled composition produces a small decline, approximately −0.192 pp. This curve is an inherited fitted interpolation, not observed single-year probabilities or an adopted replacement for the damage engine.

## Mechanism

The model defines age as calendar year minus sales cohort year. In 2024, 2011 sales enter the bucket at age 13; in 2025, 2012 sales enter. Existing sales inputs contain 12.5419 million vehicles in 2011 and 14.2200 million in 2012, a 13.38% larger incoming birth cohort. These are sales counts before survival and claim weighting, not measured entering claims. Incoming younger vehicles, aging incumbents and modeled attrition together determine the within-bucket distribution.

Holding survival and age-dependent claim propensity schedules fixed, the larger younger cohort more than offsets incumbent aging in the claims-weighted average. A 13+ bucket need not age on average just because each surviving individual car becomes a year older.

## Method and evidence status

1. Reuse annual car/light-truck sales, survival schedules, and relative claim propensities from the integrated input snapshot. Reconstruct every age 13–45 in 2024 and 2025. No new interpolation of unknown sales is introduced.
2. Repeat with inherited fixed light-truck subtype shares and the previously collected EPA vintage-specific shares. The latter preserve car/total light-truck births; their subtype splits transfer model-year production shares to calendar-year sales and remain proxies.
3. Compare three weighting conventions: surviving fleet only, fleet times relative claim propensity, and that claim proxy times the existing body/age-cell calibration correction. The two claim-weighted versions coincide here; they are not independent confirmation. Aggregate exact-age distributions also coincide across subtype mappings because existing subtype survival and propensity assumptions are shared and aggregate births are preserved.
4. Save every body/single-age contribution and four descriptive bands (13–15, 16–19, 20–24, 25–45). Do not present model-imputed claims as observations.
5. Apply the inherited smooth age curve as a sensitivity only, then calculate curve-independent bounds under a fixed nondecreasing TLF-with-age assumption.

The CCC annual source was checked: its published split stops at 13+, and its discussion of finer segmentation refers to splitting the old 7+ category into 7–9, 10–12 and 13+. It does not supply actual single-year claim weights within 13+. The existing age-curve documentation explicitly labels relative claim propensity and within-bucket total-loss probability as fitted. The underlying survival shape has external provenance but its scaling is calibrated. Calendar snapshot timing and sales-year mapping are not an exact match to CCC age definitions or annual claim flows.

## Bound without inventing exact-age TLF

Suppose there is one fixed age-specific TLF curve, between 0% and 100%, that never falls as age increases. For any age threshold, calculate how the share of the modeled 13+ population at or above that threshold changes. The largest positive tail-share change is an upper bound on the TLF increase attributable solely to age composition.

Reason: any nondecreasing bounded curve can be represented as a weighted sum of upward threshold steps, with total step height at most one. Its change in weighted mean cannot exceed the largest tail-share increase. A 0%-to-100% step at the maximizing threshold attains the unrestricted bound. We do not require that extreme curve to reproduce baseline TLF, making this a deliberately generous ceiling.

| Weighting | Maximum age-only increase with a common monotone curve | Threshold producing ceiling | Legacy smooth-curve change |
|---|---:|---:|---:|
| Surviving fleet | +0.718 pp | Age 20 | −0.103 pp |
| Modeled claims | +0.265 pp | Age 25 | −0.192 pp |

The observed +1.70 pp exceeds these ceilings. The common-age-curve ceiling also falls short of the prior combined scenario's approximately +0.52 pp residual, but the experiments use different constructions and should not be mechanically added. This is a composition plausibility check, not a recomputed joint fit.

The bound depends on a common fixed monotone age curve and the modeled age distributions. It is not a bound on every possible damage, coverage, value, or reporting change. If arbitrary nonmonotone age probabilities are allowed, the modeled-claim upper bound is +4.60 pp; hence monotonicity is a substantive restriction, not a mathematical inevitability.

## Allowing different body-specific age curves

For a broader check, allow each body type its own arbitrary fixed nondecreasing 0–100% age curve and allow body shares to change. Summing each body's maximum positive joint tail-share change gives an upper ceiling of +0.637 pp under fixed subtype mapping and +1.053 pp under vintage subtype mapping, using modeled claims. These still fall short of the full +1.70 pp increase but are large enough that we cannot rule out body/age composition contributing to the prior smaller residual.

These extreme curves are not calibrated to observed starting rates and are not estimates. With the actual frozen body-specific 13+ TLF values already in the damage engine, body-share changes produce only +0.011 pp with fixed subtype mapping and +0.003 pp with vintage mapping. The production damage engine assigns one probability to all exact ages within each body/13+ cell; it currently has no internal exact-age TLF slope. The separate legacy smooth-curve calculation is an explicit diagnostic, not functionality silently added to production.

## Interpretation and next step

Under current cohort assumptions, ordinary within-bucket aging is a weak explanation and has the wrong sign under the inherited smooth curve. Do not claim this proves actual older claims became younger: age-specific insurance coverage, filing propensity, survival, mileage and damage mix may differ from our fitted, time-invariant schedules.

The remaining task is evidence on the claim population, particularly age-dependent coverage/reporting or finer age claim counts, not an increasingly flexible curve fitted to the same +1.70 pp target. If those data are unavailable, retain the oldest-bucket residual openly. This result does not establish a bearish or bullish Copart revenue forecast; it narrows one proposed historical explanation.

## Reproduction and provenance

Outputs: within_13plus_single_age.csv, within_13plus_segments.csv, within_13plus_comparison.csv, and within_13plus_results.json. The JSON records input/source hashes and 24 checks of normalization, monotone bounds, constant-curve invariance and the smooth diagnostic's membership in the bounds. Runtime was about 0.1 second. No source data or production assumptions changed.

Sources: integrated inputs.json; age_constrained_engine_results.json; existing historical candidate_body_births.csv; docs/AGE_CURVES.md; raw/ccc/crash-course-2026.txt, Figures 18–19 discussion; existing CCC age-rate CSV. Underlying EPA cohort-source methodology is documented in docs/historical_body_births_2026-09-28/README.md. No new empirical status is assigned to inherited fitted curves.
