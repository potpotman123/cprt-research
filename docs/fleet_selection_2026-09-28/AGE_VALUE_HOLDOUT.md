# Age-value holdout — 2026-09-28

## Verdict

Reject the flatter-curve candidate for adoption. It matches an aggregate value through offsetting age-group errors. The prior suggestion that the original age curve was too steep was a possible explanation from aggregate calibration, not an established finding. This check does not support it. The original curve also misses young-vehicle values and is not validated.

## New evidence, held fixed during the test

CCC Q4 2025 report, Figure 6, national non-comprehensive total-loss valuations through October 2025. Source URL: https://www.cccis.com/reports/crash-course-2025/q4. Image URL, hash and transcribed labels in `age_value_holdout_results.json`; retained image `ccc_2025q4_age_values.webp`.

Extracted image link from saved report HTML; downloaded one 44KB image and visually read printed labels. No OCR, bulk scrape or fit to these dollar values. Bottom chart title ends at 2024 but legend and bars explicitly include through-October 2025; use those labels with the inconsistency disclosed.

| Age | CCC AAVV | Original curve model | Flatter candidate | Candidate difference |
|---|---:|---:|---:|---:|
| Current year | $40,187 | $31,236 | $30,125 | -25.0% |
| 1–3 | $30,259 | $25,423 | $25,272 | -16.5% |
| 4–6 | $20,328 | $18,681 | $19,438 | -4.4% |
| 7+ | $9,122 | $8,971 | $10,288 | +12.8% |

Both models calculate ACV among selected total losses. The original uses continuous recalibration to the old TLF targets; candidate parameters are taken unchanged from the previous fitted case. No parameters use the new age-dollar labels. Both retain assumed body weights and representative ages.

Observed age shares: 2.1%, 10.7%, 14.9%, 72.3%. Multiplying them by the printed values gives $13,706, close to the chart's $13,700 aggregate (rounding). Applying the same four weights to modeled values gives original $12,645 versus candidate $13,671. Thus candidate aggregate agreement conceals substantial within-age errors. Its overvaluation of the large 7+ group offsets its undervaluation of younger groups.

The current-year / 7+ selected-value ratio is 4.41 in CCC, 3.48 under the original and 2.93 under the candidate. Flattening moves the modeled age profile away from this observed contrast. This contrast is not a longitudinal depreciation estimate: it also includes vehicle/body/trim mix, cohort differences and selection. Do not infer a mechanically steeper depreciation slope from this ratio alone.

## Comparability limits

- CCC values and broad mix are non-comprehensive, through October; calibration uses all-loss annual age rates and conditional age weights. Current-year-or-newer model bucket is not strictly the same label as current-year chart bucket.
- The observed chart aggregates 7+; model aggregation within it uses annual all-loss shares of ages 7–9, 10–12 and 13+. That finer distribution is not independently matched here.
- CCC valuations are not established unique Copart sales. They describe pre-loss adjusted values, not auction proceeds.
- These age dollars were withheld from fitting, but are from the same provider and overlapping year as earlier targets. This is a held-out target check, not independent-provider confirmation or a statistical significance test.

## Consequence

Neither the original +4% unit response nor candidate +6.09% response to a 5% repair shock is empirically validated. Do not select the response favorable to a long or short. Keep the candidate archived as a failed validation case; no production inputs changed.

The next model revision should constrain selected values by age instead of only an aggregate, then test whether repair-cost dispersion can reconcile repair bills without distorting those values. Start with the four observed value groups, preserve the unknown 7+ internal slope explicitly, and retain coverage caveats. Do not set unconditional cohort ACV equal to selected total-loss AAVV without accounting for selection. This is a concrete modeling restriction learned from the failed candidate, not a reason to keep fitting unconstrained global curves.

Reproduction: `age_value_holdout.py`; calculation output and image retained. Small local run, no workbook edits.
