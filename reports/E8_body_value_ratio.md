# E8 — Light-truck vs car value ratio at the same age (the body-mix input on `ASP_Drivers!B4`)

*2026-09-26. Requests: 3 (coxautoinc.com robots, August-2026 ATP report page, its data-table PDF; iseecars.com robots and the
2026 retained-value study were fetched under E1). Files: `raw/cox/`, `raw/iseecars/`. Data: `data/csv/kbb_atp_by_segment_2026-08.csv`.
Script: `scripts/experiments/e8_body_value_ratio.py`. Usage: ~25k tokens.*

## Construction

`ratio = (new-price ratio, LT ÷ car) × (retained-value ratio at the same age, LT ÷ car)`

- **New prices (VERIFIED):** Kelley Blue Book average transaction prices by segment, August 2026 (Cox Automotive data tables).
  Compact car $27,997 · mid-size car $33,909 · subcompact SUV $31,149 · compact SUV $37,722 · mid-size SUV $50,315 ·
  full-size SUV $79,710 · small/mid pickup $43,806 · full-size pickup $67,446 · minivan $49,151 · van $64,645.
- **Segment mix within each body (ASSUMED, mass-market):** cars 55/45 compact/mid-size (the August subcompact-car print,
  +50% YoY, is anomalous and excluded); SUVs 10/45/35/10 subcompact/compact/mid/full; pickups 75/25 full/small; vans 70/30.
- **Body weights (MEASURED, E1 step 1):** pickups 10.9%, SUVs 40.9%, vans 4.7% of the listed light pool.
- **Retained value at 5 years (VERIFIED, iSeeCars 2026, 950k five-year-old vehicles sold Mar-2025–Feb-2026):** trucks
  retain 65.8% (34.2% depreciation), SUVs 55.1%, overall 58.2%. iSeeCars publishes no car-only average; the overall figure is
  used as the car proxy (ASSUMED).

## Result

| step | LT | car | ratio |
|---|---|---|---|
| new price, blended | $49,408 | $30,657 | **1.61** |
| 5-yr retained value | 57.2% | 58.2% | 0.98 |
| **value at age 5** | | | **1.58** |

Sensitivity to the assumed mixes and the car-retention proxy: 1.28–1.71. **`ASP_Drivers!B4` is set to 1.50** — below the age-5
point because the salvage pool averages ~10 years and retention convergence beyond year 5 is not measured (pickups are known
to hold value unusually well, SUVs less so; the two pull in opposite directions and the pool is 80% SUV). Label: MEASURED
direction, ASSUMED level. The workbook was rebuilt and `verify_intermediate_xlsx.py` reports ALL CHECKS: OK (55 sheets,
5,369 formulas, 0 problems).

## What it does to the ASP decomposition

With B4 = 1.50 and the light-truck share of the total-loss pool rising ~1.7pp/yr (roll) — or ~2.7pp/yr on the listed pool
(E1 step 1) — the body-mix effect on Copart's average price is roughly +0.5 to +0.8pp/yr. Together with the vintage effect
(~1.0pp/yr, Addendum 21) that accounts for about half of the 3.3pp ASP-over-CPI intercept; the residual falls to ~1.5pp/yr.
Read the `ASP_Drivers` tab for the year-by-year split.

## Caveats

- Salvage value is a fraction of pre-loss value that itself varies by body (export demand for pickups); no public source gives
  it by body. The ratio here is a pre-loss value ratio applied to salvage.
- The segment mixes are assumptions; the listed pool's make/model slugs could refine them (a second pass on E1's
  classifier with size classes), which would make the sticker ratio MEASURED.
- iSeeCars' "SUVs" bucket blends mass-market and luxury; the luxury tail depreciates faster, so the mass-market SUV retention
  is probably a little above 55%, which would raise the ratio slightly.
