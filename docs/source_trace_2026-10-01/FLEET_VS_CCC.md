# Fleet roll versus the CCC age-and-type constraints, 1 October 2026

Source: owner-supplied CCC workbook *Data for Harvard Research (Daniella Biblin) 9.29.2026* (SHA-256 2a127900…, identical to the file integrated 29 Sep). Script: `scripts/fleet_vs_ccc_backtest.py` (MEASURED). The CCC cells give, per body and age group, the share of claims declared a total loss and each cell's share of all total losses; dividing the second by the first gives the share of **claims** in each cell, which is what a fleet roll times a claims-propensity curve must reproduce.

The Python engine already matches all 16 cells in 2025 by construction (claim weights are backed out of them). The test below is of the fleet roll itself: births × stretched EPA survival × the age-exposure curve, with nothing fitted to these cells except, in the second table, four body factors fitted to 2025 alone.

## 1. Roll with one claims curve for all bodies (nothing fitted to CCC)

| Year | Car CCC / model | Pickup | Utility | Van | Age 0 | 1–3 | 4–6 | 7+ | Max cell gap |
|---|---|---|---|---|---|---|---|---|---|
| 2020 | 48.5 / 44.2 | 14.7 / 13.3 | 33.0 / 37.6 | 3.9 / 4.8 | 4.2 / 3.7 | 27.6 / 26.0 | 25.3 / 25.4 | 42.8 / 44.9 | 3.0 pp |
| 2021 | 46.6 / 42.4 | 14.3 / 13.5 | 35.3 / 39.5 | 3.8 / 4.6 | 4.8 / 3.8 | 25.3 / 24.5 | 25.9 / 25.6 | 44.0 / 46.2 | 2.6 pp |
| 2022 | 44.9 / 40.5 | 14.2 / 13.8 | 37.2 / 41.3 | 3.7 / 4.4 | 4.6 / 3.5 | 23.3 / 23.2 | 25.3 / 25.4 | 46.9 / 47.8 | 2.0 pp |
| 2023 | 43.0 / 38.7 | 14.4 / 14.0 | 39.1 / 43.1 | 3.6 / 4.2 | 4.7 / 3.9 | 21.7 / 21.6 | 25.0 / 25.1 | 48.5 / 49.4 | 1.8 pp |
| 2024 | 40.8 / 36.7 | 14.4 / 14.2 | 41.2 / 45.1 | 3.5 / 4.0 | 5.0 / 4.0 | 21.6 / 22.0 | 23.1 / 23.6 | 50.3 / 50.4 | 1.6 pp |
| 2025 | 38.5 / 34.7 | 14.7 / 14.3 | 43.4 / 47.3 | 3.4 / 3.7 | 5.5 / 4.1 | 22.2 / 22.5 | 21.6 / 22.4 | 50.8 / 51.0 | 1.6 pp |

Shares of claims, per cent. The roll puts cars about four points too low and utility vehicles about four points too high in every year, so cars claim more per vehicle on the road than SUVs; the age-group shares are within about 1.5 points except the newest group, where the half-year exposure assumption for age 0 looks too low.

## 2. Same roll with body factors fitted to 2025 only (2020–2024 out of sample)

Body factors (claims per vehicle relative to the common curve): Car 1.110, Pickup 1.028, Utility Vehicle 0.917, Van 0.923.

| Year | Car CCC / model | Pickup | Utility | Van | Age 0 | 1–3 | 4–6 | 7+ | Max cell gap |
|---|---|---|---|---|---|---|---|---|---|
| 2020 | 48.5 / 48.2 | 14.7 / 13.5 | 33.0 / 33.9 | 3.9 / 4.4 | 4.2 / 3.6 | 27.6 / 25.5 | 25.3 / 25.4 | 42.8 / 45.6 | 3.3 pp |
| 2021 | 46.6 / 46.4 | 14.3 / 13.7 | 35.3 / 35.7 | 3.8 / 4.2 | 4.8 / 3.7 | 25.3 / 23.9 | 25.9 / 25.4 | 44.0 / 47.0 | 3.4 pp |
| 2022 | 44.9 / 44.5 | 14.2 / 14.0 | 37.2 / 37.5 | 3.7 / 4.0 | 4.6 / 3.4 | 23.3 / 22.6 | 25.3 / 25.2 | 46.9 / 48.7 | 2.6 pp |
| 2023 | 43.0 / 42.6 | 14.4 / 14.3 | 39.1 / 39.3 | 3.6 / 3.8 | 4.7 / 3.8 | 21.7 / 21.0 | 25.0 / 24.8 | 48.5 / 50.3 | 2.5 pp |
| 2024 | 40.8 / 40.6 | 14.4 / 14.5 | 41.2 / 41.2 | 3.5 / 3.6 | 5.0 / 3.9 | 21.6 / 21.4 | 23.1 / 23.3 | 50.3 / 51.4 | 2.1 pp |
| 2025 | 38.5 / 38.5 | 14.7 / 14.7 | 43.4 / 43.4 | 3.4 / 3.4 | 5.5 / 4.0 | 22.2 / 21.9 | 21.6 / 22.1 | 50.8 / 52.1 | 2.1 pp |

## 3. Does the roll reproduce the 2020→2025 shift?

| Shift 2020→2025, points of claim share | CCC | Roll |
|---|---|---|
| Car | -10.0 | -9.5 |
| Pickup | +0.0 | +0.9 |
| Utility Vehicle | +10.4 | +9.7 |
| Van | -0.4 | -1.1 |
| Age 0 (current/newer) | +1.3 | +0.4 |
| Age 1-3 | -5.5 | -3.5 |
| Age 4-6 | -3.7 | -3.0 |
| Age 7+ | +8.0 | +6.1 |

## 4. Conclusion for the build

- The fleet roll reproduces the direction and most of the size of the five-year shift in the claim mix (cars down ten points, utility vehicles up ten; the 7+ group up) without being fitted to it. That is a genuine out-of-sample check and it passes at the body level.
- It understates the ageing shift (7+ up 6 points against 8; the 1–3 group down 3.5 against 5.5), so the roll is slightly too slow to age the claiming fleet. The births for 2021–2023 or the young-vehicle survival are the likely cause; this is the one place more precision would change a number.
- Levels need body-specific claims factors (cars ≈ 1.11×, SUVs ≈ 0.92×). The engine's 2025 cell weights already embed these implicitly; the workbook should make them explicit inputs on E2, labelled CALIBRATED to the 2025 CCC cells, with the 2020–2024 comparison shown as the test.
- E1 Fleet therefore gets a Checks block with this table live: model claim share minus CCC-implied share per cell and year, PASS if every cell is within 2 points and every body total within 1 point.
