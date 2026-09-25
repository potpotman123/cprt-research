# CPRT model — blueprint

**The reference for building the model. Open this first, every time.** Written 2026-09-14 from the model
design conversation. Every number here is either sourced in `findings.md` or flagged ASSUMED.

---

## 0. The architecture

```
A  cohort roll ──────► baseline TLF ─┐
   spread cycle ─────► ΔTLF around it ┼─► TLF_t
B  carrier book (PIF × share) ───────┼─► Copart share_t, mix_t
   claims scenario ──────────────────┘
                                      └─► US insurance units_t   (identity, multiplicative)
C  fee grid × ASP distribution ──────► service RPU_t  (produces the elasticity; regression validates it)
D  yards × cars/event ───────────────► facility cost_t → gross margin_t
E  repairable-claim recovery ────────► headline TLF vs TL count (exhibit)
                                       ▼
                     Revenue_PxQ → Costs → Bridge to Stephens → Valuation
```

**What makes this interesting rather than a growth-rate model:** the mechanisms *produce* the numbers the
regressions merely measured. A produces the TLF baseline; the spread produces the cycle; C produces the
~0.5 RPU elasticity from the fee grid's convexity. The regressions stay in the workbook as **validation tabs**
("the fee function predicts β≈0.5; reported financials say 0.514"). That is the SOLS structure: mechanism →
number → the Street's number that has no such mechanism.

---

## 1. Five rules before any cell

1. **Units are an identity, not a regression.** `(1+Δunits) = (1+Δclaims)(1+ΔTLF)(1+Δshare)`. Only TLF is
   estimated, on CCC's 27 external quarters — never on Copart's own ~6 effective observations.
2. **Chain revenue off reported FY26 revenue in growth rates.** Copart discloses no unit or RPU levels.
   `Rev_t = Rev_{t−4} × (1+Δunits) × (1+ΔRPU)`. Absolute units appear once, labeled RECONSTRUCTED.
3. **Granularity = disclosure.** US service / US purchased-vehicle / Intl service / Intl purchased-vehicle;
   US units split 80/20 insurance/non-insurance by an input. Nothing deeper except where a mechanism (A–E)
   earns it.
4. **Every tab exists to feed the Bridge tab.** Build backward from the line-by-line delta to Stephens.
5. **Colour:** blue = input · black = formula · green = link to another tab · yellow = calibrated to a stated
   anchor. One assumption per labeled cell, source beside it. No numbers inside formulas.

**Depth allocation (19 days, 2 pages):** one deep mechanism (A), one medium (C), the identity chain, the
bridge. B and D as appendix exhibits unless A and C are green by day 10. E is one chart. Everything else
(§6) is a single labeled input.

---

## 2. Tab map

| Tab | Purpose | Status of inputs |
|---|---|---|
| `README` | legend, tab map, sources, the five rules, effective-n warnings | — |
| `Inputs` | scenario switch (1/2/3) + every driver, Bear/Base/Bull + Live column | — |
| `Hist_Reported` | Copart quarterly series FY22Q4–FY26Q4 | `reported_units.csv`, `quarterly_pl.csv`, `quarterly_margin.csv`, `segment_service_rev_8k.csv`, `facility_ops_quarterly.csv` |
| `Hist_Industry` | CCC, BLS, Fast Track, PGR, GEICO, RBA, duopoly, FRED sales | see §10 |
| `Calib_TLF` | ΔTLF ~ spread(t−1), live SLOPE/INTERCEPT/RSQ | `ccc_tlf_quarterly.csv`, `totaling_spread_quarterly.csv` |
| `Calib_RPU` | ASP ~ used-car CPI; service RPU ~ ASP | `elasticity_rebuild.csv`, `reported_units.csv` |
| `A_CohortRoll` | fleet cohort roll → baseline TLF | **built as live formulas in `model/CPRT_Intermediate.xlsx`** (Survival, Fleet, FleetByAge, Curves, TLF_Roll). The earlier worked example `model/legacy/blueprint_A_CohortRoll.xlsx` is kept only as a record — its survival curve was calibrated to S&P average age, which `docs/AGE_CURVES.md` §2.3 shows is the wrong target |
| `B_CarrierBook` | named carriers + "all other" → share and mix | Stephens carrier table (shares only), PGR PIF, Berkshire, NAIC republishers |
| `C_FeeGrid` | fee schedule × ASP distribution → service RPU | **needs a hand read of the fee pages in a browser** |
| `D_Yards` | yards × lots/event → facility cost | `yard_panel_us.csv`, `lots_per_sale_event.csv`, `facility_ops_quarterly.csv` |
| `E_TLFInversion` | repairable-claim recovery → headline TLF falls while TL count rises | CCC 2025 disclosures |
| `Units_Decomp` | historical six-quarter panel + forward identity | `units_decomp_panel_v2.csv` |
| `RPU_Build` | CPI → ASP → RPU by segment | — |
| `Revenue_PxQ` | four lines, quarterly FY27Q1–FY28Q4, annual roll-ups | — |
| `Costs_Margin` | vehicle cost, facility (fixed/variable), G&A, D&A → GP, EBITDA, EBIT, EPS | — |
| `Bridge` | ours vs Stephens FY27, line by line, % delta; FY28 | — |
| `Valuation` | EV/EBITDA, P/E, reverse DCF as a physical claim, Bear/Base/Bull PT, downside below spot | — |
| `Duopoly_Tracker` | daily Copart vs IAA listed inventory; kill condition | `duopoly_daily.csv` |

---

## 3. The mechanisms

### A — Fleet cohort roll → baseline TLF   (the SOLS contract-waterfall analog)

```
baseline TLF_t  =  Σ_MY [ share(MY,t) × P(age) ]          age = t − MY
share(MY,t)     =  sales(MY) × S(age) × R(age)  ÷  Σ_MY′ [ same ]
```
- `sales(MY)` = Ward's new retail sales 1970–2021 (ORNL TEDB Ed.40 T3.6) + FRED TOTALNSA/LTRUCKNSA 2022–25 rescaled
  to Ward's basis → `data/csv/light_vehicle_sales_by_year.csv`, cars and light trucks separately.
- `S(age)` survival — **EPA schedule (ORNL T3.15), stretched:** `S(a/k)`. k fitted to the IHS/Polk 2013 census by
  single year of age (cars 1.064, trucks 0.921; bucket MAE 0.4pp), drifted ×1.194 by 2024 to hit S&P's counts (VIO
  ~289M, 66% aged 7+); independent check: fleet growth 2020→25 +5.4% vs Experian +5.1%. **Never calibrate to S&P
  average age** — the census itself implies ~2 yrs less (a 27-yr-old registered tail); see `docs/AGE_CURVES.md` §2.3.
- `R(age)` relative insured-claim frequency — `e(a)·exp(−0.0903·max(a−6,0))`: flat through age 6, then −8.6%/yr;
  e(0)=0.5 (half-year exposure for the current model year). Fitted jointly with P to eight CCC 2024 claim-mix
  statistics; a free 0–6 slope is not identified (fits +1.6%/yr with no gain), so it is fixed flat.
  R(7+)/R(0–6) = 0.57 = miles-by-age 0.65 (EPA T3.14) × coverage/filing 0.87.
- `P(age)` total-loss propensity — logistic `0.048 + 0.432/(1+exp(−(a−9.22)/3.73))`: 8% new, 10% for ≤3 yrs (CCC
  "1 in 10"), 20% at 7, 34% at 12, 43% at 17. Buckets P(7+) 31.7% / P(0–6) 12.7%, unchanged under every survival
  assumption. The old "45.3% at 13+" anchor is **unsourced — dropped.** Shape fixed; the LEVEL moves with the spread.
- Per-age values `data/csv/age_curves.csv`; every fit target, out-of-sample check and sensitivity row
  `data/csv/age_curves_validation.csv`. Method and evidence, in full: **`docs/AGE_CURVES.md`**.
- **Output and finding:** demographics move baseline TLF **+0.16pp/yr** (0.04–0.18 across survival assumptions) —
  about a quarter of the +3.9pp rise 2019→2025 — vs the **+0.60pp/yr** intercept in the spread regression. Out of
  sample, the frozen curves reproduce 2020's average claim / repairable / total-loss ages within 0.3 yrs and 2025's
  7+ shares within 1pp. The 7–12-yr cohort peaks in 2026 (~88M, +14% vs 2022) and rolls off to 2028. Demographics
  are a quarter of the secular rise; the rest is the repair-cost cycle, technology and filing behaviour. **Say so** —
  smaller than the popular version, and more credible.

### Spread cycle → ΔTLF around the baseline

```
totaling spread  =  repair-CPI YoY − used-car-CPI YoY
ΔTLF (pp, YoY)   =  0.599 + 0.0815 × spread(t−1)        CCC all-loss, n=27, R² 0.81, OOS MAE 0.39pp
                 (non-comp variant: 0.609 + 0.0834×, R² 0.79, OOS MAE 0.16pp, but effective n≈6)
```
A car is totaled when repair cost exceeds ~70–80% of its value; repair inflation outrunning car values
pushes more cars across. 2Q24 spread **+15.7pp** → 3Q25 **+2.3pp** (what hurt Copart) → 2Q26 **+8.3pp**.
Live OOS: predicted 2Q26 +1.28pp, management-cited actual +0.90pp. **The spread explains the cycle; the
intercept is drift the model does not explain** — use for 12 months, not for the decade.

### B — Carrier book → share and mix   (the contract-book analog)

```
Copart US insurance units  =  Σ named carriers  +  "All other carriers"
```
- **Named** (weight × public growth series): Progressive (~5% → **0**; monthly PIF +22% → +8%; cliff Apr–Jul
  2026, laps FY27Q4 — a *dated schedule*), GEICO (~15%; Berkshire; Yipit/Stephens say Copart may be gaining
  the remaining ~15%), State Farm (~15%; annual), USAA / Allstate / Farmers (~5% each; NAIC premium growth
  minus rate as PIF proxy).
- **"All other" (~30%): do NOT impute per carrier.** Weight = 1 − Σ named. Historically *solve* its growth
  as the residual to Copart's reported total (that implied series is a check). Forward: grow at the
  industry pool with Copart's share held constant — one stated assumption.
- Weights from the Stephens carrier table as *shares only* — its absolutes are autoAstat-derived
  (do-not-use for levels). Put NAIC 2024 shares beside Copart's weights: the gap is the underweight-
  Progressive exhibit (SF 18.9 / PGR 16.7 / GEICO 11.6 / Allstate 10.2 / USAA 6.2).
- **Tie-out:** the book's forward Δshare must equal the identity's Δshare term. Two views of one number.

### C — Fee grid × ASP distribution → service RPU   (the physical-intensity analog)

```
service RPU  =  Σ_bands [ share of units in band × (buyer fee(band) + gate + environmental + virtual-bid) ]
             +  seller fee (~1–2% × ASP under PIP)
```
Fixed dollars dominate at low prices, percentages above ~$15k → the grid is convex → RPU elasticity to ASP
is ~0.5 *by construction*. Assume a lognormal ASP distribution (median ~$5k), shift it by the ASP scenario,
run it through the grid. **Output:** the elasticity falls out; compare to the measured 0.514. A dated fee
increase becomes a step in the grid, not a regression constant.
**Data:** fee pages are robots-disallowed to crawlers — **read them in a browser and screenshot** (a human
reading a public page is not automated access). Build as `fee(price, title_type)`: the gate fee may differ
clean vs non-clean. Corroborate with third-party fee calculators and the Substack §2.10–2.11.

### D — Yards × lots-per-event → facility cost   (the COGS breakout)

```
facility cost_t  =  fixed cost per yard-week × yards_t  +  variable cost per lot × lots_t
```
Calibrate the two parameters to the annual line (FY23 $1,518M · FY24 $1,710M · FY25 $1,944M · FY26
$1,756M) and check against FQ4 FY26's disclosed +7.7% dollars on −5.7% units (+14.2% per unit). Exhibit:
International, same quarter, +11.4% dollars / **+1.2%** per unit — opposite leverage sign. US yards 187 →
204 (2022 → 2026); sale events/week 204 → 295; **lots per event ~700 → 492 (−30%)** on quality-gated months.
Not available: acreage (not in any 10-K), per-yard cost, US/intl facility split before FQ4 FY26.

### E — TLF denominator inversion   (one chart; the contrarian exhibit)

CCC 2025: repairable claims −9.7%, total-loss valuations −2.9%; $1,000+ deductibles up 6pp in two years.
Hold repairable volume flat and 2025 TLF would have been ~21.8% (−0.5pp), not the reported +0.8pp "record."
If suppressed claims return as rates fall: repairable +10%, TL +3% → **headline TLF 22.4% (−1.2pp) while the
total-loss count (Copart's supply) +3%.** Bears will read the headline as the structural story breaking.
Precedent: 2021–22 TLF fell 1.8pp while Fast Track collision claims surged +46/+21/+17%. Dated moment:
Crash Course 2027, ~March.

---

## 4. The identity (US insurance units)

```
Copart US insurance units  =  Claims  ×  Total-loss rate  ×  Copart share       (three sequential gates)
(1 + Δunits)  =  (1 + Δclaims) × (1 + ΔTLF) × (1 + Δshare)                       (exact; ≈ sum when small)
```
Measure two terms from industry data, know Copart's number → **the third term falls out.** FQ4 FY26:
claims −3.4%, TLF +4.0% → pool +0.5%; assignments −5.0% → Δshare **−5.5pp**; ex-one-account +2.3% →
Δshare **+1.8pp**. Historical panel (six quarters, CCC all-coverage denominator, chosen because it
reconciles to CCC's directly-reported −2.9% pool): 2025H1 **+1.4pp** | 2025H2 −1.8pp | 2026H1 −5.1pp; step
−6.5pp vs management's disclosed account −7.3pp. **No share loss before the account; one discrete step; at
or above the pool after, ex-account.** Forward: schedule the share term (account drag ~−5pp through FY27Q3,
0 from FY27Q4; mix drag decaying; underlying +1.8 to +3pp). Do not solve for it forward — state it.

---

## 5. RPU chain (validation tabs for C)

```
ASP_yoy           =  3.23 + 0.599 × used-car CPI_yoy            r = 0.77, n = 15
service RPU_yoy   =  4.13 + 0.514 × ASP_yoy                     n = 17, CI [0.29, 0.73], R² 0.61
mgmt-def RPU_yoy  =  2.84 + 0.752 × ASP_yoy                     total revenue ÷ units; reproduces the +5.4% print
```
Used-car CPI −8% → +10% moves service RPU only +3.3% → +8.9%. **RPU is low-variance; the intercept floors
it.** Stephens' FY27 implies ~+3%. ⚠ Fee/mix component decelerated in FY26 (+5–6pp → +1.3 to +3.5pp) — partly
CAT comps, possibly fee-hike lapping; date the fee-schedule changes (C) before a judge asks.

---

## 6. Simple builds — one labeled input each, no mechanism

| Line | Treatment | Anchor |
|---|---|---|
| Purchased-vehicle revenue (US, intl) | `prior × (1+Δpurchased units) × (1+ASP)` | FQ4 US +10.9%, intl +4.4%; Copart Direct −26% units FY26 |
| Purchased-vehicle margin | flat % | FY26 US 6.7% |
| International service | `prior × (1+Δunits) × (1+ΔRPU)`, two inputs | FQ4 units +10%, fee RPU +3.5% |
| US non-insurance units | one growth input | FQ4 +0.2%, dealer +5.8% |
| G&A | one growth rate off FY26 ~$431M | FY23→25 +60%; "restructuring" |
| D&A | flat per quarter | FY26 ~$235M |
| SBC add-back | flat | reconcile FY26 adj. EBITDA to Stephens $1,937M |
| Interest income | net cash × yield ÷ 4 | ~$2.6B post-ACV × ~4% |
| Tax | flat | 22–23% |
| Shares | buyback $ ÷ price, quarterly | $1.63B bought Jan–Mar 26; ~940M exiting FY26 |

---

## 7. FY26 base year ($M) — what the projection chains off

| | Q1 | Q2 | Q3 | Q4 | FY26 |
|---|---|---|---|---|---|
| US service | 855.5 | 819.5 | 895.5 | 817.8 | 3,388.3 |
| Intl service | 136.3 | 132.6 | 160.6 | 151.7 | 581.2 |
| US purchased-vehicle | 97.1 | 102.2 | 107.4 | ~113.0† | ~419.7 |
| Intl purchased-vehicle | 66.1 | 67.5 | 73.6 | ~69.9† | ~277.1 |
| **Total revenue** | 1,155.0 | 1,121.7 | 1,237.1 | 1,152.4 | **4,666.2** |
| Gross profit | 537.0 | 492.8 | 572.6 | 481.0 | 2,083.4 |
| Facility operations | 427.2 | 427.5 | 450.3 | 450.7 | 1,755.7 |
| Operating income | | | | 368.9 | ~1,652.6 |

†Q4 vehicle split derived from the call; sum ties to 182.9. Net income $1,480M, EPS $1.55, D&A ~$235M,
cash+HTM $4.5B pre-ACV (ACV = $1.9B equity value, $10.50/sh), zero debt.

**Named consensus (Stephens 2026-08-20, stock $26.81):** EW, PT **$35 = 13.5× FY27E EBITDA $2,033.2M**
(Q: 488.2 / 478.2 / 573.3 / 493.5), EPS **$1.67** (0.39 / 0.39 / 0.48 / 0.41), GP $2,186.1M, GM 45.1%,
EBITDA margin 42.0%, US units **+1.3%**, positive growth from F2Q27. FY26E for reconciliation: EBITDA $1,937.2M.

---

## 8. Build order and the checks that catch the usual errors

1. `Hist_*` — paste the CSVs, don't retype.
2. `Calib_*` — **stop until you reproduce 0.0815 / 0.599 (TLF) and 0.514 / 4.13 (RPU) exactly.** A mismatch
   means misaligned columns — exactly how the retracted 0.465 happened.
3. `Inputs` with the switch; confirm all three scenarios propagate.
4. `A_CohortRoll` — checks: 2019 = 19.2 ±0.3; avg age 2025 within 1 yr of 12.7; TL share from 7+ within
   10pp of 70%. Use the gentler propensity curve.
5. `Units_Decomp` historical — residuals must match `units_decomp_panel_v2.csv` to the decimal.
6. Forward units → RPU → Revenue. **FY27 Base revenue should land within ~2% of Stephens' implied ~$4.85B**,
   above on RPU not units. FY27 US insurance units ≈ −3 / −1 / 0 / **+5** by quarter (lap is Q4).
7. Costs — reconcile FY26 EBITDA to $1,937M via the SBC cell; FY26 EPS to $1.55.
8. Bridge, then Valuation. Bear PT **below spot**.
9. **Back-test the whole chain on FY26Q4:** actual used-car CPI −1.9% → service RPU ≈ +4.4%, mgmt-def RPU
   ≈ +5.4%; actual claims/TLF → US insurance units ≈ −7.5%. If yes, the plumbing is right.

**Every tab:** title + two-sentence description + sources / INPUTS / CALCULATION / OUTPUT / CHECKS. Guess the
three headline outputs *before* building (FY27 RPU ~+5%, FY28 units ~+6%, FY28 EBITDA ~$2.35B) so a
nonsense result reads as a bug, not a discovery.

---

## 9. Corrections to carry (things earlier in the project got wrong)

- **Lapping takes the drag to zero, never positive.** The sign flip comes from the underlying.
- **The account is Progressive; the cliff was Apr–Jul 2026, not Aug–Oct 2025.** Full lap FY27Q4. The pre-cliff
  ~−3pp residual is carrier mix.
- **FY27 units ≈ consensus.** The variant view is RPU (floor +4.5–5.5% vs ~3%), margin (the ~11% investment
  inflation normalizing), and FY28 (units +5–7%, revenue +10–12%, EBITDA +15–20%).
- **Lots per sale event is ~700 → 492**, not 745 → 492; the 745 capture fails the overlap gate.
- **0.465 is retracted**; 0.514 on aligned inputs. Effective n ≈ 6 — print it.
- **Fee-grid numbers in the old prompt files are unsourced** ($95 gate / flat $1,000 / 7.5%+$250). Read the
  grid yourself.
- Copart unit growth is **transcript-provenance**; no filing discloses it.
- **The blueprint tab's survival curve was calibrated to S&P average age — wrong target.** It forces a 27-year
  registered tail and 90% survival at 17. Calibrate survival to vehicle counts (`docs/AGE_CURVES.md` §2.3).
- **"45.3% total-loss propensity at 13+" is unsourced.** Use the fitted P curve (36% at 13, 44% at 17).

---

## 10. Where every input lives (`data/csv/`)

| File | Contents |
|---|---|
| `reported_units.csv` | transcript series FY22Q4–FY26Q3 (add FY26Q4: US inv −3.4, US ins −7.5, US ins ASP +3.7, global ASP +3.5, global ins −4.2, US total −5.7, non-ins +0.2, intl +10) |
| `quarterly_pl.csv`, `quarterly_margin.csv`, `segment_service_rev_8k.csv` | 8-K income statements; US/intl service split FY26 |
| `facility_ops_quarterly.csv` | Facility operations line, FY25Q1–FY26Q4 |
| `elasticity_rebuild.csv` | the 17 quarters behind 0.514 |
| `ccc_tlf_quarterly.csv`, `ccc_tlf_annual.csv` | CCC total-loss frequency, both variants |
| `cprt_cpi_three_series.csv`, `totaling_spread_quarterly.csv` | BLS used-car / repair / insurance CPI; the spread |
| `tlf_calibration.csv` | the regression outputs |
| `units_decomp_panel_v2.csv`, `decomposition.csv` | the six-quarter panel |
| `fasttrack_collision_claims_cw.csv` | ISS Fast Track collision claim headlines 2019–2025 |
| `pgr_monthly_pif.csv` | Progressive personal-auto PIF, Jan-2003+ |
| `geico_frequency_series.csv` | Berkshire frequency bands |
| `rba_automotive_series.csv`, `duopoly_compare.csv` | RB Global lots / GTV / take rate |
| `duopoly_daily.csv` | Copart vs IAA listed US inventory, daily |
| `fred_TOTALNSA.csv`, `fred_LTRUCKNSA.csv`, `light_vehicle_sales_by_year.csv` | US light-vehicle sales; cohort sizes 1970–2025 by body type (Ward's basis) |
| `ornl_tedb40_*.csv` | EPA survival by age, miles by age, Ward's sales (ORNL TEDB Ed.40). The IHS census and avg-age extracts are local-only (`raw/ornl/tedb40/extracts/`, licence line on the sheet) |
| `age_curves.csv`, `age_curves_validation.csv` | S, R, P by age with 2024 fleet/claims/TL shares; every target, OOS check and sensitivity |
| **`model/CPRT_Intermediate.xlsx`** | **the workbook to copy from** — every Data_* tab plus live formulas: Survival, Fleet, FleetByAge, Curves, Calibration (Solver), TLF_Roll, Spread_Reg, RPU_Reg, Checks (`scripts/build_intermediate_xlsx.py`; verified by `verify_intermediate_xlsx.py`) |
| `yard_panel_us.csv`, `cadence_fixed.csv`, `lots_per_sale_event.csv` | yards, sale events, utilization |
| `backtest_inventory_v2.csv` | sitemap inventory vs reported (appendix exhibit) |

Licensed, gitignored, read locally only: `raw/transcripts/` (17 S&P transcripts), `raw/sellside/` (Stephens
F4Q26 preview — the carrier table and consensus numbers).
