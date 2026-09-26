# E4 — Off-lease / used-supply mechanism for used-car CPI: the value side of the totaling spread

*2026-09-26. Script `scripts/experiments/e4_offlease_used_values.py`; data `data/csv/used_car_cpi_drivers.csv`. No network: FRED
TOTALNSA (light-vehicle sales, monthly NSA, 1976–2026-08), BLS CPI used cars & trucks and new vehicles (`raw/bls/`), FRED VMT.
Requests: 0. Usage: ~35k tokens.*

## The explanation tested

Used-vehicle values are set largely by the supply of 2–4-year-old vehicles, which is new sales two to four years earlier —
a quantity already known through mid-2028. New sales fell to 13.8–15.0M in 2020–2022 and recovered to 15.5–16.1M in
2023–2025, so the 2–4-year-old stock is now growing and should soften used values, widening the spread from the value side.

## What was done

- `SUP(m)` = sales in months m−48 … m−24 (the 2–4-year-old cohort). Two specifications, both fitted on **1995Q1–2019Q4 only**
  and tested on 2020–2026, so the 2021–22 spike is never learned:
  1. **Growth form:** used-car CPI YoY on SUP YoY, new-vehicle CPI YoY, VMT YoY.
  2. **Level form:** log(used CPI ÷ new CPI) on log(SUP ÷ trailing 10-year sales) plus a trend.
- The raw lag profile corr(used YoY, sales YoY lagged k quarters) for k = 0…20 was printed first, so the lead is seen rather
  than assumed.

## Result

**Growth form: no supply effect.** The lag profile peaks at only −0.36 around 7–9 quarters, not at the 30–42 months the
plan expected; in the regression the supply term is insignificant (coefficient −0.06, t −0.8) and new-vehicle CPI does all
the work (coefficient +2.3, t +6.9, R² 0.39, effective n ≈ 12). Out of sample the frozen fit misses 2021–22 by 15–25pp,
which is the point: that episode was a new-car supply shock, not an off-lease story. **On the plan's own kill rule ("no lag
structure at 30–42 months") the growth-form version is killed.**

**Level form: the mechanism is there, pre-2020.** log(used/new) on log(2–4-year-old stock ÷ 10-year sales):

| Fit window | Elasticity b | se | t | R² | resid ρ1 |
|---|---|---|---|---|---|
| 1995Q1–2019Q4 | **−0.175** | 0.034 | −5.1 | 0.60 | 0.76 |
| 1995Q1–2026Q2 | −0.149 | 0.056 | −2.6 | 0.09 | 0.87 |

A 10% rise in the 2–4-year-old stock relative to the fleet lowers used values relative to new by about 1.8% (FITTED,
pre-COVID; the full-sample fit collapses because 2021–22 dominates the variance). Residual autocorrelation is high; the
standard errors overstate precision.

**The forward path is data, not a forecast.** With sales through August 2026, the 2–4-year-old stock is known to mid-2028:

| Quarter | 2–4-yr stock ÷ scale, vs 2026Q2 | Implied Δ log(used/new), % | Spread value-side, pp | ΔTLF, pp (× 0.0815) |
|---|---|---|---|---|
| 2026Q4 | +6.6% | −1.1 | +1.1 | +0.09 |
| 2027Q2 | +15.6% | −2.6 | +2.6 | +0.21 |
| 2027Q4 | +23.4% | −3.7 | +3.7 | +0.30 |
| 2028Q2 | +31.9% | −4.9 | +4.9 | +0.40 |

Everything else held constant (new-vehicle prices, miles, the trend). Label: MEASURED stock path × FITTED elasticity.

## What it means

1. **The used-value side of the spread turns from headwind to tailwind on a known schedule.** Used values rose through
   2025 (the spread's collapse to +2.3pp, what hurt Copart); the cohort arithmetic says they soften by ~2.5% relative to
   new by mid-2027 and ~5% by mid-2028. On the TLF calibration that is worth about **+0.2pp of total-loss frequency in
   FY27 and +0.4pp in FY28**, before any change in repair inflation.
2. **It is small relative to the repair side.** The spread moved 13pp peak-to-trough in 2024–25; the value side
   contributes low single digits over two years. The spread's action is in repair costs (E3) and in used-car shocks the
   cohort model does not contain (2021–22). Say this plainly; it is a bound, not a catalyst.
3. **It is the kind of driver a pod does not have in its model:** a calendar, from public sales history, with a direction
   that is not a regression on Copart's own data.

## Caveats (print them)

- The elasticity is pre-2020. The 2021–22 shock (chip shortage, rental-fleet liquidation, stimulus) is outside the
  mechanism and the full-sample fit shows it. Do not present the level fit's R² on the full sample.
- Lease penetration is not in the variable; off-lease returns are leases × sales, and lease share fell sharply in
  2021–22. Adding an Experian lease-share series (robots allows `/blogs/`; not fetched) would sharpen the 2025–27 path,
  most likely *lowering* near-term off-lease supply and therefore the tailwind. Direction of the correction: smaller.
- Scale for the last 24 months of the stock path reuses the last 120 sales months (ASSUMED; negligible).
- Used-car CPI is quality-adjusted retail; Copart's ASP is salvage. The ASP-on-CPI slope (0.60) and the vintage effect
  (`ASP_Drivers`) sit between this series and Copart's revenue.

## For the model

`Inputs`: a "used-value cohort effect" row by fiscal quarter, −0.4 / −1.1 / −1.8 / −2.6 / −3.1 / −3.7 / −4.2 / −4.9 % on
used values relative to new (2026Q3 → 2028Q2), feeding the spread's value side; sensitivity ±50% on the elasticity. The
CSV's `forecast` rows carry the stock path.
