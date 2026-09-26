# E5 step 1 — the cross-state screen: listed inventory disperses, but not the way a titling-speed story needs

*2026-09-26, third session. Script `scripts/experiments/e5_state_dispersion.py`; data `data/csv/state_share_dispersion.csv`.
Input `data/csv/state_panel.csv` (51 states × 16 captures: 2022-09 → 2025-09 from archived `lot.xml`, Sep-2026 live). No
network. Usage: ~15k tokens. The transcripts' cycle-time remarks are local-only (`raw/transcripts/`, not in this container)
and were not re-read.*

## What the screen asks

If electronic salvage titling shortens days-to-title state by state, states adopting it should show **large, persistent,
one-directional** declines in their share of Copart's listed inventory relative to the national series, on different dates,
clustered by adoption rather than by hurricane. The kill rule from the scoping doc: "no cross-state structure → stop."

Shares of the national listed total are used, never levels (captures are page-out-of-sync; `ARCHITECTURE.md`). The noise
benchmark is each state's within-year wobble: the coefficient of variation of its share across the five captures of 2023 and
the five of 2024.

## Result (43 states with ≥ 0.5% of listings; 98% of the pool)

| statistic | value |
|---|---|
| relative change in share, 2023 → Sep-2026: mean / stdev / IQR | +0.7% / **30.1%** / −22% … +19% |
| within-year wobble (CV of share across a year's captures): mean / max | 11.9% / 30.1% |
| between-year stdev ÷ within-year wobble | **2.5×** |
| persistence: corr(change 2023→24, change 2024→26) | **−0.37** |
| size dependence: corr(\|change\|, log share) | −0.07 |
| regional means, 2023→26 (unweighted) | Northeast **+25%** (7) · Midwest +9% (10) · South **−9%** (17) · West **−9%** (9) |
| Helene/Milton-2024 states (FL GA NC SC TN VA) vs others, 2023→24 / 2024→26 | −2.1% vs +3.1% / −1.5% vs +1.3% |

Largest moves: CO −47%, MS −44%, SC −42%, WV −42%, NV −37%, TN −35% down; CT +104%, MI +63%, NC +37%, VA +33%, AZ +32%,
MN +31%, OH +30% up. Texas, the largest state, went 8.4% → 10.3% of listings (+23%).

## Reading

1. **There is dispersion**: between-year moves are 2.5× the within-year wobble, and they do not depend on state size, so
   they are not just sampling noise on small states.
2. **It is not persistent** — the sign of a state's move from 2023 to 2024 predicts the *opposite* sign for 2024 to 2026
   (corr −0.37). MO +48% then −47%; NM +74% then −43%; AZ +78% then −26%; FL −30% then +45%; DE −37% then +13%. A titling
   regime change would show as a level shift that holds; mean reversion is what capture artefacts and lumpy CAT
   inventory look like.
3. **It is not CAT-structured**: the 2024 hurricane footprint states do not stand out in either window (Helene inventory
   sat in the 202410 capture and left by 2025).
4. **The one structure that survives is regional**: Northeast and Midwest shares up, South and West down. That is
   consistent with Copart's own mix moving (yard openings, carrier assignment patterns, the Progressive account's
   geography leaving between April and July 2026), and with the live capture's partial third page rotating yards in and
   out. Nothing in it points at title processing, and the biggest single declines (CO, SC, TN, NV) are in states with no
   obvious common e-title date.

## Verdict on the kill rule

**Weak structure, wrong shape.** The screen does not justify the 20–60 DMV-site requests of steps 2–3 before the finals. E5
stops here unless the owner supplies state e-title adoption dates from a single source, in which case the test is a
difference-in-differences on `state_share_dispersion.csv` with the regional trend as a control — one script, no fetches.

## What it implies for both directions

- **Long:** the −6% YoY in gated listed inventory (§3A) cannot be re-read as "faster titles, same throughput" on this
  evidence; velocity is not shown to have changed. The listed-inventory decline stays a volume signal, with the account
  loss as its named cause.
- **Short:** no support here either — the regional shifts are not a demand signal, and the Northeast/Midwest gains offset
  the South/West losses. The screen is a negative for E5, not a finding about Copart.

## Caveats

- 2025 has two captures and 2026 one (live, three pages, the third partial), so the 2024→26 column is the noisiest.
- State is parsed from the lot slug; ~90% of lots carry a state token. DC is over-represented (1% of listings) because the
  Washington-area yards carry a DC token; it is left in.
- Vermont is absent from the 2023 captures and is skipped.
