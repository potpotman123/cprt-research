# E2 — Insurance affordability → filing behaviour → the claims term

**2026-09-28 interpretation update:** the claims that the industry decline is ending and that deductible effects reverse specifically in mid-2027 are not established by the descriptive carrier series/correlations below. Progressive frequency is not an industry claim count, and a selected lag is not a causal forecast. See [CCC count/population check](../docs/fleet_selection_2026-09-28/CLAIMS_COUNTS_AND_DENOMINATOR.md). Preserve these historical results as exploratory evidence rather than adopting the stated forward timing.

*2026-09-26. Requests: 48 to sec.gov (Progressive CIK 80661: older filings index + 47 10-Q/10-K primary documents 2015–2026, ~150 MB,
descriptive UA). Data: `data/csv/pgr_frequency_quarterly.csv` (every number with its source sentence), `claims_term_drivers.csv`.
Scripts: `scripts/experiments/e2_pgr_frequency.py`, `e2_affordability_claims.py`. Usage: ~90k tokens.*

## Why Progressive instead of Fast Track

Fast Track's CollisionWeek headlines give 12 numeric quarters out of 25, half of them the COVID swing (scoping doc §1.3). Progressive's
10-Q MD&A states its personal-auto incurred accident frequency change every quarter (four wordings over the decade, a table since
2023), so the series is quarterly, numeric and continuous for Q1–Q3 of every year 2015–2026 (Q4 is not in the 10-K primary document).
Caveat Progressive itself states: its frequency reflects its own mix (a shift to "preferred" customers in 2024–26) as well as the industry.

## The series (MEASURED, YoY %)

| year | Q1 | Q2 | Q3 | severity (Q2) |
|---|---|---|---|---|
| 2019 | −3 | −4 | −2 | +8 |
| 2020 | −18 | −39 | −19 | +8 |
| 2021 | −3 | +47 | +10 | +8 |
| 2022 | +2 | −8 | −9 | +16 |
| 2023 | 0 | +2 | +4 | +12 |
| 2024 | −9 | −8 | −5 | +12 |
| 2025 | −3 | −4 | −2 | — |
| 2026 | **0** | **−2** | | — |

Collision-only frequency: −11 / −7 (2024 Q1/Q3), −6 / −6 / −5 (2025), **0 / −3** (2026 Q1/Q2).

## Regressions (freq = a + b·VMT YoY + c·insurance-CPI YoY lagged k)

| sample | n | VMT coefficient | best insurance-CPI lag | c | t | R² |
|---|---|---|---|---|---|---|
| 2015Q1–2026Q2, COVID quarters excluded | 29 | +1.56 (t 3.0) | 8 (positive, wrong sign) | +0.15 | +0.9 | 0.32 |
| full sample incl. 2020–21 | 35 | +1.69 (t 15.8) | 3 | −0.26 | −2.3 | 0.91 |
| collision only, ex-COVID | 23 | +3.30 (t 2.9) | 0 | −0.38 | — | 0.51 (ρ1 0.51) |

**Reading.** Miles driven explain frequency; the insurance-price channel is identified only when the 2021–23 episode is in the
sample (premiums surged as frequency fell), and disappears ex-COVID. **The scoping doc's kill rule ("no lag structure after
controlling for VMT") is met for the frequency channel.** The mechanism's clean footprint is elsewhere: CCC's $1,000+ deductible
share tracks insurance CPI with a **4–6 quarter lag (corr 0.79–0.88, n = 16 overlapping YoY changes)**. Dearer insurance moves
deductibles, which suppress *small filed claims* and the repairable denominator — exactly what CCC said (repairables −9.7% in
2025) — not accident frequency per se.

## What it means for the claims term (both directions)

- **The claims decline is ending, in the data.** Progressive's frequency went from −9/−8/−5 (2024) to −3/−4/−2 (2025) to 0/−2
  (2026 H1). Fast Track said the same ("smallest decline since 1Q24"). The model's hand input for the 2026 claims term is
  −3 to −5%; the observable now says **0 to −2% and flattening**. That is modestly *bullish* for FY27 units: the industry pool
  term stops subtracting.
- **The deductible channel reverses with a lag, not immediately.** Insurance CPI peaked at +22.6% (Apr-2024) and is now −4.5%;
  at a 4–6-quarter lag the $1,000+ deductible share should stop rising around **mid-2027**, so suppressed small claims return in
  FY28, not FY27. The recovery in *repairable* volume that E (the TLF-denominator exhibit) needs is a 2027H2 event.
- **Not a catalyst on the pitch horizon.** A claims term going from −4% to 0% over four quarters is worth ~+4pp on Copart's US
  insurance units versus a −4% run-rate — real, but it is the consensus "return to growth from F2Q27" already in Stephens'
  numbers, not a variant view.
- **Bearish angle:** the improvement is partly Progressive's mix (its own words), and Progressive's volume no longer reaches
  Copart (E — the account left Apr–Jul 2026). The industry claims term matters for Copart only through the carriers it still
  has; Progressive is the wrong carrier to weight.

## Caveats

- Q4 is missing every year (10-K primary documents carry no MD&A; the annual report is Exhibit 13 — 11 more fetches if wanted).
- Overlapping YoY observations; effective n is smaller than shown. No causal claim.
- Insurance CPI Oct/Nov-2025 interpolated (BLS source gap).
- Progressive's severity series is extracted only where the sentence pattern matched (about two-thirds of quarters).
