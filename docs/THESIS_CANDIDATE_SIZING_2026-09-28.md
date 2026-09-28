# Candidate thesis sizing, not adopted forecasts

28 September 2026. User requested granular, quantifiable short candidates. Bounded arithmetic using existing results; no new data collection or workbook changes. None of these conditional cases is a probability-weighted forecast or established consensus gap.

## SUV selection and fee offset

Existing CRSS age-7–9 initial rear-impact shares are car 24.45%, SUV 28.00%, pickup 21.30%. These are conditional shares among sampled police-reported involvements, not claim incidence per insured vehicle or repair-operation frequencies. The pickup does not have the higher rear-impact share. Current assumption-driven repair means: car $3,682; SUV $3,706.98; pickup $4,822.91. Body-specific frequencies change SUV/car repair premium from 1.91% under common impact weights to 0.68%; not an empirical causal repair-premium estimate.

Use existing deterministic age-10 severity scenarios in model_tests_2026-09-27/results.json, nodes=8001, recovery slope=0.4. Define a synthetic two-body claims mix with SUV share changing 40% to 42%, fixed total claims and allocation. This is NOT a measured six-month mix change and excludes pickups/vans, other ages, carrier differences and their interactions. Units = weighted TLF. Revenue per claim = weighted TLF times conditional service RPU. Blended RPU = revenue divided by units.

| Assumed SUV/car ACV | Unit change | RPU change | Revenue change | Illustrative H1 dollar change |
|---|---:|---:|---:|---:|
| 1.20x | -0.2774% | +0.1256% | -0.1522% | -$2.274m |
| 1.50x | -0.6407% | +0.2627% | -0.3796% | -$5.672m |

Dollar scaling uses legacy H1 US service forecast $1,660.1203m times the UNVALIDATED 90% insurance-service assumption = $1,494.1083m. It is materiality arithmetic, not the future bottom-up revenue estimate. The strong recovery/severity slope is also unvalidated. Do not apply these age-10 toy coefficients to the full book in a production forecast without cohort aggregation. 1.5x scenario probabilities/RPU: car 34.3332%/$710.392; SUV 24.5844%/$817.069. The per-claim revenue ratio is 0.82358. Constant-recovery counterpart is 0.88218.

## Within-age TLF change, rather than aging alone

Existing CCC reconstruction attributes ~0.027pp of 2024–25 aggregate TLF change to age mix and ~0.683pp to within-age changes, with population compatibility limitations. This does not establish future reversal. Prior forecast-only diagnostic: a uniform -1pp shift in body/age TLF moves H1 services -$74.4719m under fixed fee and exposure conventions. A -0.3pp shift therefore produces -$22.3416m. This is a sensitivity threshold, not a forecast. The selected fees of marginal losses would also change in a joint damage engine, so do not independently add this shock to the SUV-selection case. Evidence needed: observed same-cohort repair/value/recovery movements and an earlier-date calibration predicting later outcomes.

## Contract-wide seller fee concessions

Existing Barclays illustration assumes 621,900 carrier vehicles, 125,000 incremental vehicles, $3,850 auction price, 4% seller commission and 20% commission discount. The discount is $30.80 per affected vehicle: $19.15452m annually across the carrier base versus $3.85m if applied only to 125,000 incremental units; difference $15.30452m. The original analyst illustration ALREADY accounts for the broader concession. This arithmetic is not a newly identified Street miss.

A further 20 percentage points of discount off the original commission (40% total discount instead of 20%, not 20% off the already-discounted fee) would reduce annual service fees another $19.15452m, or $9.57726m under an illustrative half-year/full-run-rate convention. No evidence establishes that extra concession or its timing. The contract still adds revenue in the original example. Research requires affected retained-unit scope, negotiated fee evidence, timing and comparison with the actual analyst baseline. No EBITDA forecast is added here.

## Do not pitch yet

- Structural SUV disadvantage is not automatically a large six-month company revenue decline. The legacy attribution actually gives body-within-age +$0.082m and age composition -$0.885m over H1 against its embedded baseline.
- A broad fleet-aging cliff is not established; the current demographic result is small.
- Rear impacts are not more frequent for all light trucks, and initial-impact shares do not identify required parts.
- Precision of arithmetic is not precision of economic estimates. These candidates require empirical validation before being combined into a short memo. The objective is a dated revenue difference versus a comparable external forecast, not a large downside number manufactured from assumptions.
