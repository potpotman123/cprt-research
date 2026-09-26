# E3 — The repair side of the totaling spread: is it labour scarcity, parts, or neither?

*2026-09-26. Requests: 8 to download.bls.gov (descriptive UA; robots re-checked): CES directory and series index, `ce.data.80a/80b`
(Other Services employment, hours & earnings), `ce.data.05b` (total private comparator), PPI directory, `pc.series`,
`pc.data.22.TransportationEquipment`. Data: `data/csv/ppi_motor_vehicle_parts.csv`, `data/csv/repair_cost_drivers.csv`. Script:
`scripts/experiments/e3_repair_cost_drivers.py`. Usage: ~40k tokens. No regression was run; this is an accounting read.*

## The explanation tested

That repair-cost inflation — the numerator of the totaling spread, +6.6% YoY in July 2026 on BLS's motor-vehicle maintenance
and repair CPI — is structural: a collision-repair labour market short of technicians, plus ADAS content, so the spread stays
wide even as used-car prices normalise, and total-loss frequency keeps rising for a slow-moving, measurable reason.

## What the measured drivers say (annual averages, YoY %, MEASURED)

| year | repair CPI (SETD) | used-car CPI | spread | parts PPI (NAICS 3363) | body-shop wages (CES 8111 AHE) | all-private wages | body-shop jobs |
|---|---|---|---|---|---|---|---|
| 2019 | 3.4 | 1.0 | 2.4 | 0.3 | 2.3 | 3.3 | 1.4 |
| 2021 | 3.9 | 26.6 | −22.7 | 3.4 | 5.9 | 4.3 | 4.5 |
| 2022 | 8.2 | 12.7 | −4.5 | 5.1 | 5.0 | 5.4 | 4.2 |
| 2023 | 11.5 | −7.1 | 18.7 | 2.4 | 6.0 | 4.5 | 4.2 |
| 2024 | 6.1 | −6.0 | 12.1 | 1.0 | 6.2 | 4.0 | 1.4 |
| 2025 | 5.9 | 2.8 | 3.1 | 1.4 | 4.4 | 4.0 | 0.4 |
| 2026 YTD | 4.4 | −3.0 | 7.4 | 2.0 | 2.8 | 2.8 | −0.2 |

Monthly, the latest prints (July 2026): repair CPI **+6.6%**, body-shop hourly earnings **+3.6%**, all-private earnings **+3.2%**,
parts PPI **+2.4%** (+3.3% in August), body-shop employment **0.0%** (1.035M, off a February peak). Body-shop wages ran 1.5–2.2pp
above the all-private rate in 2023–24; that premium is **gone** in 2026. Employment in the sector is flat, not falling.

## Reading

1. **The labour-scarcity story is not in the labour data.** A structurally short market would show wages rising faster than the
   economy's and employment unable to grow. In 2023–24 it looked that way; by 2026 body-shop wage growth equals the all-private
   rate and headcount is flat. Whatever kept wages elevated in 2023–24 has passed through.
2. **Repair CPI is running ~3pp above its measurable inputs.** With wages +3.6%, parts +2.4% and (per CCC) labour hours and
   parts counts per claim slightly *down*, a cost-weighted input index grows ~3%; the CPI prints +6.6%. CCC's own average
   collision repair cost (TCOR) grew **+1.7% in 2025**, the lowest since 2017, and +1.4% through Q3 2025. The gap between the
   constant-quality CPI and the input costs is shop pricing (labour *rates* billed, not wages *paid*), ADAS calibration and
   diagnostic line items (CCC: calibration share of claims 26.9% → 35.6% in a year, average calibration fee ~$550), and the
   CPI's own basket, which includes routine maintenance. None of those is a scarcity mechanism with a forecastable driver.
3. **What it means for the spread.** The spread regression's numerator is the CPI, and the CPI is the part of the spread that
   is currently *unexplained* by inputs. If repair CPI mean-reverts toward input growth (~3%), the spread narrows by ~3pp and,
   at 0.0815 pp of ΔTLF per pp of spread, the total-loss tailwind shrinks by ~0.25pp of TLF per year. If shop pricing power
   holds (insurers keep paying billed rates above wage growth), the spread stays where it is. Nothing in the public data
   settles which; the prior should be reversion, because a 3pp wedge between a service price and its input costs is not
   usually stable.

## For the two directions

- **Bearish reading:** the two legs that carried TLF up in 2023–25 — the repair leg and the ageing-mix leg — are both fading in
  the measured data. Wages have normalised, parts inflation is 2–3%, the cohort mix effect is ≈0 since 2023
  (`reports/CCC_age_buckets_2026.md`). The remaining spread (+7.4pp in 2026) rests on repair-CPI pricing that inputs do not
  explain, plus the used-car side turning (E4: −2.6% relative by 2027Q2 helps the spread, but only ~+0.2pp of TLF).
- **Bullish reading:** ADAS content is a genuine, rising, per-claim cost that the input series miss (calibration share +9pp in
  a year), and CCC's total-loss share was still rising in 2025 across every age bucket. The spread need not close; the
  question is the pace of ADAS-driven severity versus the deflation elsewhere.

## Caveats

- Cost shares (labour 45 / parts 40 / misc 15) are ASSUMED; CCC publishes contributions as charts only. The decomposition
  is illustrative; the wage and parts series are the finding.
- CES 8111 is "automotive repair and maintenance" (includes mechanical shops), not collision only; no finer public series exists.
- PPI 3363 is manufacturers' selling prices for parts, not shop-billed parts prices; the CCC "+6.6% per part" (June 2025)
  statement sits between them, and OEM part-price inflation is one candidate for the wedge in point 2.
- One data gap: BLS repair CPI is blank for Oct-2025 (the source gap noted in the CPI file).

## For the model

`Inputs`: repair-CPI path scenarios for FY27 — hold (+6.5%), revert to inputs (+3%), midpoint (+4.75%) — with the spread and
ΔTLF consequences computed on `Spread_Reg`. The wage, parts and jobs rows are in `repair_cost_drivers.csv` for the exhibit.
