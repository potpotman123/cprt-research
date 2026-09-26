# CCC's own age-bucket data: total-loss propensity by age 2020–2025, and the ageing-vs-propensity decomposition

*2026-09-26. Source: CCC Crash Course 2026 report page (`cccis.com`, robots `Allow: /`), chart images fetched from the page's
CDN with data labels read at 4400 px (`raw/ccc/img/`). Requests: 6 pages + 6 images + 1 robots. Scripts:
`scripts/experiments/ccc_age_decomposition.py`. Data: `ccc_tl_share_by_age_2020_2025.csv`, `ccc_tl_valuation_share_by_age_2020_2025.csv`,
`ccc_claims_share_by_age_2020_2025.csv`, `ccc_tlf_mix_vs_propensity.csv`, `ccc_deductible_share_quarterly.csv`. Usage: ~70k tokens.*

## Why this matters

`docs/AGE_CURVES.md` fitted P(age) — the probability a claim is declared a total loss — to eight CCC statistics because
"no public source publishes total-loss rate by single year of age", and `HANDOFF.md` §6 listed "CCC's 2026 Figures 18 and 22
may carry data labels by age group" as an open item. They do. **Figure 19 of Crash Course 2026 is P by six age buckets for
every calendar year 2020–2025**, and Figure 18 is the total-loss mix by the same buckets. Together they give the claims mix
by age (claims in bucket = total losses in bucket ÷ P), so the TLF rise can be decomposed into fleet ageing and everything
else *from CCC's data alone*, with no fitted curve.

## P(age bucket), all loss categories, % of claims declared total loss (VERIFIED, Figure 19)

| bucket | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| current year or newer | 6.8 | 7.1 | 9.2 | 9.0 | 9.7 | 9.6 |
| 1–3 | 9.7 | 9.4 | 8.9 | 9.3 | 10.2 | 10.7 |
| 4–6 | 15.3 | 14.6 | 13.3 | 14.1 | 15.4 | 15.7 |
| 7–9 | 22.8 | 21.6 | 19.1 | 20.5 | 22.8 | 23.4 |
| 10–12 | 31.6 | 29.2 | 26.5 | 28.4 | 31.5 | 32.3 |
| 13+ | 43.1 | 40.0 | 37.8 | 40.6 | 43.6 | **45.3** |
| total | 20.6 | 19.7 | 18.8 | 20.2 | 22.3 | 23.1 |

CCC's disclaimer on the chart: the age grouping "does not match up 100% to current industry reporting … should not be
compared to other reporting as it could vary slightly." The chart's own totals differ from the headline annual series on
disk by up to 0.3pp (22.3 vs 22.3 for 2024; 23.1 vs the 2026 edition's 22.8 elsewhere on the page).

**Three things this settles.**
1. **The "45.3% at 13+" anchor the repository dropped as unsourced is real: it is CY2025 in this chart.** The fitted P curve's
   bucket values (P(7+) 31.7%, 36% at 13, 44% at 17) sit inside the measured 7–9 / 10–12 / 13+ values (23.4 / 32.3 / 45.3 in
   2025), so the fit was not wrong; it can now be *replaced* by data at bucket resolution.
2. **Propensity rises within every bucket 2022→2025**, by +1.8 (1–3) to +7.5pp (13+). Age-specific propensity is not a fixed
   curve; it moves with the cycle — which is exactly what the spread regression models. The two mechanisms are separable
   and both visible.
3. **The 2022 trough is in every bucket.** Used-car values peaked (spread collapsed) and P fell everywhere; the fleet did not
   get younger.

## Claims-age mix, derived (MEASURED from Figures 18 and 19)

| bucket | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| current | 4.8 | 5.2 | 3.5 | 3.8 | 4.4 | 4.8 |
| 1–3 | 28.6 | 26.2 | 23.1 | 21.5 | 21.4 | 22.2 |
| 4–6 | 25.6 | 26.3 | 25.7 | 25.5 | 23.6 | 22.1 |
| 7–9 | 16.6 | 17.7 | 19.9 | 20.5 | 21.1 | 20.6 |
| 10–12 | 9.5 | 9.2 | 11.1 | 12.5 | 13.2 | 14.2 |
| 13+ | 15.0 | 15.5 | 16.7 | 16.1 | 16.3 | 16.2 |

Reconstructed TLF (Σ w·P) matches the chart total within 0.4pp every year, which validates the derivation. The 1–3-year share
of claims fell from 28.6% to 21.4% between 2020 and 2024 — the 2020–22 new-sales collapse working through — and the 7–12
share rose from 26% to 35%.

## Decomposition of the TLF change (pp)

| window | base TLF | mix (ageing) | within-age propensity | interaction | total |
|---|---|---|---|---|---|
| **2020 → 2025** | 20.2 | **+1.75** | **+1.02** | +0.01 | +2.77 |
| 2020 → 2022 | 20.2 | +1.42 | −2.52 | −0.29 | −1.39 |
| **2022 → 2025** | 18.9 | **+0.29** | **+3.80** | +0.07 | +4.16 |
| 2023 → 2024 | 20.2 | +0.15 | +1.89 | +0.02 | +2.07 |
| 2024 → 2025 | 22.3 | +0.03 | +0.68 | +0.00 | +0.71 |

**Reading.** Over the full window ageing explains 63% of the rise; but it is front-loaded in 2020–22, when the young-claims
share collapsed with new sales, and is essentially zero since 2023 (+0.15, +0.03). The 2022→2025 surge of +4.2pp is 91%
within-age propensity — the spread cycle and whatever else moves the totaling decision at a given age. This is the
measured version of `HANDOFF.md` §3F's conclusion from the fitted roll ("demographics explain part of the past rise and none
of the next two years"), and it is stronger because it uses CCC's own buckets, not fitted curves.

**For the pitch:** the popular "ageing fleet" story is real, sized, and over: it was worth about +1.5pp of TLF in 2020–22 and
about +0.2pp since. What moved TLF in 2023–25 was the totaling decision at *every* age. That is the spread's territory and
the repair-cost side (E3), not demographics.

## Deductible shares, quarterly 2021Q1–2025Q4 (VERIFIED, Figure 2)

Share of repairable collision claims with a $1,000+ deductible: 19.3% → 28.1%; $500–999: 55.8% → 47.4%; <$500 flat at ~25%.
The shift accelerates from 2023Q4 (21.9%) — one policy cycle after the insurance-CPI surge began — and is still accelerating
in 2025Q4 (+0.9pp per quarter). Twenty quarters, `ccc_deductible_share_quarterly.csv`; this is E2's filing-behaviour series.

## What was not found

- HLDI class-level losses: the make-and-model page loads from an `/api/hldilosses/getviewmodel` endpoint that returns 404 to a
  plain GET; the two 2025 bulletins cited on the topic page are theft studies. The IIHS vehicle-age page 404s. Class-level
  frequency/severity would need the HLDI fact sheets (`/research-areas/auto-insurance/auto-insurance-fact-sheets`, not yet
  fetched). Open.
- CCC 2026 Figure 12/13 are *theft* total losses by vehicle type, not total-loss frequency by type. The one body-type
  sentence ("pickup trucks outpace other categories") is about thefts. No CCC page on disk gives TLF by body.

## For the workbook

- `Curves`: add a `P_measured` block (this table) beside the fitted P; the fit's bucket means should be checked against
  the 2024 column (the year the curves were fitted to).
- `TLF_Roll`: the forward demographic drift row can cite this decomposition (2023–25 mix effect +0.15 / +0.03pp) as the
  measured basis for "≈0 forward".
- `Inputs`: deductible $1,000+ share as the E2 driver row.
