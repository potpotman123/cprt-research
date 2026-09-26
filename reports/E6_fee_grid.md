# E6 — The buyer fee grid: Copart and IAA, read live 2026-09-26

*Owner-driven browser session (the owner navigated in their own Chrome; the agent read the rendered pages through the Claude in
Chrome extension). No fetcher touched a robots-disallowed Copart path. IAA's tables are SVG images on a Contentful CDN embedded
in public pages; those files were fetched (host has no robots.txt), rendered, and read by local OCR (macOS Vision) with a
programmatic cross-check. Records: `raw/fees/live_2026-09/` (page dumps, SVGs), `data/csv/copart_fee_grid_2026-09.csv` (996 rows),
`copart_fixed_fees_2026-09.csv`, `iaa_fee_grid_2026-09.csv` (285 rows), `iaa_fixed_fees_2026-09.csv`. Scripts:
`scripts/experiments/e6_parse_fee_page.py`, `e6_ocr_iaa_table.py`, `e6_iaa_ocr_to_csv.py`, `ocr_image.swift`,
`e6_fee_grid_simulation.py`. Usage: ~120k tokens, ~2 hours of the owner's clicking. All VERIFIED.*

## 1. What Copart's schedule actually is

Copart publishes three member pages (non-licensed; licensed low-volume; licensed high-volume) but only **two schedules**:

| schedule | who | clean-title top rate | non-clean top rate | gate fee |
|---|---|---|---|---|
| **Standard Pricing** | non-licensed buyers, and licensed buyers with < 25 units or < $75K/yr or ≥ 5 bidder accounts | 7.25% above $15,000 | 7.50% | $79 clean / $95 non-clean |
| **Preferred Pricing** | licensed, ≥ 25 units AND ≥ $75K/yr AND < 5 bidder accounts | 5.75% | 6.00% | $79 / $95 |

The low-volume licensed page was verified band-for-band identical to the non-licensed page (clean and non-clean standard
grids; heavy assumed). Within each schedule: 45 fixed-dollar bands from $0 to $14,999.99, then a percentage; a separate
"unsecured payment" column ~+10–40% higher; **non-clean title is a distinct, higher grid at every band above $200** (e.g.
$375 vs $325 at $1,000–1,199) with a $16 higher gate fee and $1–11 higher virtual-bid fees; **heavy vehicles** share the
bands to $5,499 (Standard) or $7,999 (Preferred) then go flat 15%/20% or 10%/15% (secured/unsecured). Per-unit fixed
charges on top: $15 environmental, virtual-bid fee by high bid ($39–149 clean, $40–160 non-clean), $50 late payment, $20
title handling; relist 10% (min $600); $69 third-party finance fee.

## 2. IAA's schedule is Copart's schedule

| IAA page | IAA tier | equals Copart… | test |
|---|---|---|---|
| Licensed | Standard Volume (7.5% > $15k) | Standard Pricing, non-clean, secured | 0 mismatches at 45 prices |
| Licensed | High Volume (6.0% > $15k) | Preferred, non-clean, secured | 0 mismatches at 45 prices |
| Non-Licensed | single grid | IAA Standard Volume (hence Copart Standard non-clean) | 39/39 bands identical |
| Heavy | Standard / High Volume | Copart Standard / Preferred non-clean **heavy** (15% from $5,500 / 10% from $8,000) | band-for-band |
| Internet bid fees (all pages) | proxy / live | Copart non-clean virtual-bid pre-bid / live-bid ($40–140 / $50–160) | identical |
| Rec Rides (powersports) | single grid | no Copart analogue (CrashedToys not read) | — |

Differences: IAA does not split by title (its one grid is Copart's *non-clean* grid, so a clean-title car is cheaper to buy
at Copart by $30–80 per unit and ~0.25pp at the top); IAA charges a **$105 service fee "effective October 1, 2026"** plus $20
title handling and an unstated EH&S/fuel surcharge where Copart charges $79/$95 gate + $15 environmental; IAA's tables carry
the date **"Effective November 4, 2024"**. The Rec Rides SVG is versioned `0926` — revised this month.

**For the pitch:** the duopoly's buyer fee schedules are identical to the dollar, and IAA dated its current grid to Nov-2024.
That is the clearest public evidence that buyer fees are set with reference to each other, not competed away — the
"marginal rents accrue to the insurer" bear case (Stephens' framing) has to run through *seller* fees, which neither
company publishes.

## 3. The mechanism (C): convexity → elasticity ≈ 0.5, by construction

Buyer-side fee (band + gate + environmental + live virtual bid) as % of price, Standard non-clean: 99% at $300, 57% at $1,000,
29% at $3,000, 20% at $5,000, 15% at $8,000, 9.3% at $15,000, 8.4% at $30,000. Fixed dollars dominate below ~$5,000; above
$15,000 the fee is a flat percentage plus ~$300 of fixed charges.

Simulated elasticity of the mean buyer fee per unit to a uniform price shift (lognormal price distribution, **median and
sigma ASSUMED** — Copart discloses no ASP level or distribution):

| assumed median | σ | elasticity, Standard non-clean | Preferred | Standard clean |
|---|---|---|---|---|
| $2,500 | 0.8–1.0 | 0.39–0.41 | 0.42–0.44 | 0.41–0.44 |
| $3,500 | 0.8–1.0 | 0.38–0.42 | 0.41–0.44 | 0.40–0.45 |
| $5,000 | 0.8–1.0 | 0.41–0.47 | 0.43–0.47 | 0.43–0.49 |
| $7,000 | 0.8–1.0 | 0.47–0.52 | 0.46–0.51 | 0.49–0.55 |

**The grid produces 0.4–0.5 for any plausible salvage price distribution; the measured service-RPU elasticity is 0.514
(CI 0.29–0.73).** That is the mechanism-then-number structure the blueprint asked for: the fee function predicts β ≈ 0.5,
reported financials say 0.514. Caveats: buyer fees are one component of service revenue (seller fees, transport, storage,
title and other services are the rest and are not public); the simulation holds the grid fixed, so it says nothing about the
+4pp intercept, which is dated fee-schedule changes and mix.

## 4. History — what we could and could not establish

- Wayback copies of Copart's fee page (40 captures 2017–2020 on disk) are client-rendered stubs with no numbers. Dead.
- Management refuses to discuss fee schedules on calls ("we don't talk about fee schedules", 2022-11 and 2024-09).
- Dated evidence on disk: IAA's grids are "Effective November 4, 2024" (so IAA's last schedule change was Nov-2024); IAA's
  $105 service fee is "Effective October 1, 2026"; IAA's Rec Rides grid was revised 09-2026. Copart's pages carry no dates.
- Copart's quarterly "fee revenue per unit" disclosures (transcripts): +7.6% (FY26Q2), +10.5% (FY26Q3), +7.5% (FY26Q1
  US), +3.5% (FY26Q4). Those are the intercept's realised path, not its cause.

Kill rule from the scoping doc ("simulated fee steps explain < ⅓ of the intercept → mix is the story") cannot be run
without dated Copart grids; that remains open and needs the FY26 10-K's revenue disaggregation.

## 5. For the model (tab `C_FeeGrid`)

`Data_copart_fee_grid_2026-09` and `Data_iaa_fee_grid_2026-09` are in the workbook on rebuild. Build `fee(price, title,
schedule)` as a lookup on the band table; the ASP distribution median is the one ASSUMED input (blue); the elasticity output
should read 0.4–0.5 and be compared with `RPU_Reg!K12` (0.514) on the Checks tab.
