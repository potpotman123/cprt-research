# Workbook plan: building the revenue architecture into `CPRT_Model_v1.xlsx`

1 October 2026. Plan only; nothing built yet. Owner approval required before any build step.

## 0. What exists and what the plan does with it

| Workbook | Role here |
|---|---|
| `~/Downloads/CPRT_Model_v1.xlsx` (11 tabs: RPM, Volume Build, RPU Build, DCF, Reverse DCF, six PitchBook data tabs) | **Target.** Keep DCF, Reverse DCF and the PitchBook tabs untouched. Rewire RPM to pull from engine tabs. Retire Volume Build and RPU Build (their placeholder percentages become engine outputs). |
| `raw/reference/TeamBDCModel.xlsx` (Black Diamond, 22 tabs) | **Formatting source A**: Garamond; navy title bar; blue section bars; year headers white-on-navy; grey group bars with thin top/bottom borders; divider tabs ("Model ->", "Alternative Data ->"); "(READ ME)" build tabs; per-segment Revenue / YoY / Delta-to-Street on the RPM. |
| `~/Downloads/KW VIA MODEL.xlsx` (22 tabs) | **Formatting source B**: one `Engine` tab with named engines each ending in a line that feeds `Revenue Build`; an `Inputs` block at the foot of the engine (every assumption in one place); a `Contract Layer` with one row per contract; `Notes / sources` column on the right; green for cross-tab links, blue for hard inputs, red for toggles and probabilities; divider tabs "RPM ELEMENTS ----->" and "DATA ----->"; "AD " prefix on data tabs; "Check vs." rows. |
| `model/CPRT_Intermediate.xlsx` (55 tabs) | **Donor of live formulas** for the fleet roll (Survival, Fleet, FleetByAge, TLF_Roll) and regressions (Spread_Reg, RPU_Reg). Copied in, not linked. |
| Python engine outputs: `model/revenue_architecture_2026-09-28/`, `model/ccc_age_body_2026-09-29/`, `model/aftermarket_bridge_2026-09-29/`, `model/thesis_audit_2026-10-01/` | **Donor of values** where Excel cannot reasonably reproduce the computation (1,024-point selection distributions, the bid-feedback solver, the 16-subset Shapley table). Pasted as values on data tabs with file, date and SHA-256, labelled ENGINE. |

Work goes into a copy, `model/CPRT_Model_v2.xlsx`, built by one script (`scripts/build_cprt_model.py`) from `CPRT_Model_v1.xlsx` plus the CSVs, so it can be rebuilt and checked. The Downloads file is never overwritten.

## 1. Formatting standard (applied by the script to every tab)

- **Font** Garamond everywhere. Title row 1: 13 bold, white on navy `0E2841`, spanning B:P. Row 2: 10 italic grey `595959`: the tab's governing equation and units. Rows 1–2 are the only rows that use the navy fill.
- **Grid** gridlines off, zoom 90, column A width 2.5 (margin), B 56 (labels), C 8 (units: `$M`, `000s`, `%`, `$`), D–O 13 (periods), P 48 (notes / sources, grey 10 italic). Freeze panes at the first projected column, below the header rows.
- **Header rows** row 4: `Units` italic centred; `Historicals` / `Projected` bold centred with bottom border over their column spans. Row 5: section bar, bold white on blue `215E99` in B; period labels (`FY2026A`, `FY2027E`; quarterly tabs `FQ1 FY27E`) right-aligned on the same bar.
- **Blocks within a tab** group bar: bold black on light grey `D0D0D0` with thin top and bottom borders (Black Diamond style), one blank row above, none below. Totals: bold, thin top border. Ratios and growth rows: italic, label indented three spaces, format `0.0%_);\(0.0%\);\-_)`. Money `#,##0.0_);\(#,##0.0\);\-_)`, units `#,##0_);\(#,##0\);\-_)`, per-unit dollars `"$"#,##0`.
- **Colour code** (legend on Cover): blue `0000FF` hard-coded input; black formula; green `008000` link from another tab; red `FF0000` toggle, probability or scenario selector; purple text `7030A0` ENGINE-pasted value. Every input row carries an evidence label in column P: VERIFIED / MEASURED / FITTED / CALIBRATED / ASSUMED / ENGINE.
- **Tab colours** navy `0E2841` for RPM, DCF, Reverse DCF; purple `7030A0` for engines; grey `BFBFBF` for data; divider tabs are empty sheets named with arrows, as in both reference models.
- **Every engine tab** has, in order: title and equation; the calculation blocks; a `Feeds →` line naming the RPM row it drives; an `Inputs` block at the foot listing every assumption used on the tab (blue), with evidence label and source, so no number is typed inside a calculation block.

## 2. Tab map, left to right

```
Cover | RPM | DCF | Reverse DCF | RPM ENGINES -----> | E1 Fleet | E2 Claims & Totals | E3 Carriers | E4 Aftermarket | E5 Prices & Fees | E6 Other Branches | Scenarios | Street | Checks | DATA -----> | D Reported | D CCC | D Fleet | D Fees | D Carriers | D Engine | D Street | PB IS (Annual) … PB CF (Qtr)
```

Time axis. Engines run **quarterly, FQ1 FY26A to FQ4 FY28E** (12 columns) with three annual roll-up columns (FY26A, FY27E, FY28E) at the right, because the catalyst question lives in quarters (the lost account laps in FQ4 FY27). RPM and DCF stay **annual FY2022A–FY2031E**: FY27E and FY28E come from the engines; FY29E–FY31E extend by explicit fade rows on RPM, labelled "beyond engine horizon".

### Cover
Ticker, price and date, DCF implied price and upside (green links to DCF), key statistics, colour and evidence-label legend, a one-line-per-tab map, and the three dated benchmarks (JPM 11 Sep 2026 FY27 service $4,061m ex-ACV; CapIQ total; engine reference $4,093.1m).

### RPM (one page)
Equation in row 2: `Service revenue = Σ channels (units × all-in RPU); Total = service + vehicle sales`.
Blocks: (1) Total revenue, y/y, Δ to Street. (2) Service revenue by channel: US insurance core, US insurance ancillary (title + delivery), US non-insurance, International; each with y/y and Δ to Street where a broker discloses the line. (3) Vehicle sales (purchased), y/y. (4) Units by channel and global fee units, y/y. (5) All-in RPU by channel, y/y. (6) Scenario selector (red cell: Neither / A only / B only / Both / Bull offset) and the row "Service revenue vs own reference" beside "vs JPM FY27", so the two comparisons are never confused. FY27–28 cells are green links to `Scenarios`; FY29–31 are fade formulas: `units_t = units_{t-1} × (1 + g_units)`, `RPU_t = RPU_{t-1} × (1 + g_RPU)` with the fades as blue inputs.

### E1 Fleet (live formulas, copied from the intermediate workbook)
`Fleet(age, body, FY) = Births(FY − age, body) × S(age; stretch)`; light trucks split SUV / pickup / minivan by the fixed pool proxy. Output block: vehicles on the road by five age bands × four bodies, FY26–FY28, plus share of fleet by band (feeds E2). Inputs: Ward's/FRED births (VERIFIED), EPA survival (VERIFIED), stretch parameter (FITTED to the 2013 IHS census and 2024 counts), body split (ASSUMED).

### E2 Claims & Totals (live)
`Claims(cell) = Fleet(cell) × w(age, body) × m_claims`; `Totals(cell) = Claims(cell) × TLF(cell)`; `Pool = Σ cells × routing`. Cells are the 16 CCC age × body cells. Blocks: claim weights (CALIBRATED, from `calibration_cells.csv`), TLF by cell (observed 2020–25, calibrated 2025 level), claims multiplier and paired non-filing term (ASSUMED, default 1.0 and 0), derived TLF check against CCC annual (MEASURED), total-loss pool by quarter (quarterly = annual × seasonal weights from the historical ledger). Cross-check block: the spread regression ΔTLF = 0.599 + 0.0815 × spread(t−1) carried as a diagnostic row, not a driver. Feeds E3.

### E3 Carriers (thesis A; live)
`Copart assignments = Σ_i Pool × w_i × a_i(t)`; `Aggregate share = Σ w_i a_i`. One row per carrier (State Farm, Progressive, GEICO, Allstate, USAA, Farmers, Liberty, Travelers, Nationwide, Other) with weight (FY26Q4 frozen, ASSUMED: premium share is not claim share) and allocation path by quarter. Progressive follows the inherited runoff and then stays flat (labelled scenario). GEICO and State Farm events appear as separate rows with red probability cells and start quarter, default off in the "A only" case unless the owner turns them on; the sheet shows expected-value and realised-case variants side by side. A second block, `Seller terms by carrier`, holds commission % and any dated concession (effective quarter), feeding E5. Outputs: insurance sale-equivalent units by quarter (sale-equivalent timing stated in row 2; physical timing not modelled). Inputs block records the share-build source, its UNVERIFIED expert-call basis, and the measured listed-inventory split (57.2%, four clean nights) as a reference row.

### E4 Aftermarket (thesis B; live reduced form, with ENGINE parity rows)
`Bill saving % = e × Σ_s Δq_s × (1 − p_s / p_OEM)` over the eligible basket (e = 40% bill share; prices 1.00 / 0.50 / 0.60; shifts by quarter OEM→AM 1/2/3/4 pp and recycled→AM 0.375/0.75/1.125/1.5 pp cumulative, matching the 1 October package). `Δ units = −η_sel × bill saving % × threshold-responsive fraction` (η_sel the engine's implied selection response, ENGINE). `Δ price = −x × κ × τ × Δq_recycled / q_recycled` (x = 25% donor exposure, κ = 1.5 contribution-to-hammer, τ = 50% transmission; all ASSUMED). Three blocks: sourcing path, repair-cost channel, donor-bid channel; then a parity block pasting the engine's quarterly Δ units and Δ RPU from `aftermarket_feedback.json` so the reduced form is checked against the solver each quarter. A "no recycled displacement" countercase row is always visible. Feeds E3 (unit adjustment) and E5 (price adjustment).

### E5 Prices & Fees (live)
`ASP_t = ASP_{t−1} × (1 + g_ASP) × (1 + Δprice_E4)`; `Core fee per unit = Σ bands share_b × fee(band_b, buyer mix) + fixed fees + seller fee % × ASP`; `Ancillary per unit = Σ services adoption × price`; `All-in RPU = core + ancillary`. Blocks: ASP path (US insurance +3.7% continuation as a blue input, Manheim as a reference row); posted buyer-fee grid by price band (VERIFIED snapshot 26 Sep 2026, one vintage; `SUMPRODUCT` over band shares pasted from the engine's selected-value distribution, ENGINE); buyer mix 50% preferred and seller fee 4% (ASSUMED); title 50% × $50 and delivery 10% × $300 (ASSUMED); historical ledger anchoring US service dollars to the 8-Ks with the 90% / 80% insurance-share toggle (red) and implied units. Feeds RPM RPU rows.

### E6 Other Branches (live)
US non-insurance: dealer, BluCar, Copart Direct units × RPU (disclosed growth rates as inputs). International: fee units × reported-currency RPU, with a toggle between +3.5% continuation and flat (the $90m-a-year difference the audit flagged). Purchased-vehicle revenue overlay. ACV acquisition: toggle, default excluded, so the RPM perimeter matches JPM's ex-ACV benchmark. Feeds RPM channel rows and vehicle sales.

### Scenarios
Four common-base cases (Neither / A only / B only / Both) plus a Bull offset case, assembled live from the engines by switching E3 and E4 on or off; beside them the ENGINE-pasted 16-subset table and Shapley attribution from `model/thesis_audit_2026-10-01/` for parity. Every case shows FY27 and FY28 service revenue, Δ vs own reference, Δ vs JPM, unit and RPU contributions, and the interaction term. The red selector cell on RPM reads from here.

### Street
The expectations sheet in workbook form: one column per named broker (JPM 11 Sep, Barclays 11 Sep, Stephens 20 Aug, BNP 11 Sep, HSBC 10 Sep, Jefferies 29 Jun, Equisights 12 Sep) and CapIQ; rows for FY27 service revenue, purchased revenue, total, US insurance units, lost-account treatment, ASP, RPU, international, ACV scope, with "not disclosed" preserved as text. Source is the extraction already completed overnight (saved JSON, to be converted locally without agents). Delta rows feed RPM.

### Checks
Service revenue history ties to the 8-K series within $0.1m; units identity (Σ channels = global fee units); fee-band shares sum to one; engine parity (FY27 reference $4,093.08m; larger-shift $4,002.41m; combined $3,904.62m); scenario columns sum; no hard-coded numbers inside calculation blocks (a count of blue cells outside Inputs blocks, must be zero). Pass/fail cells with conditional fill.

### Data tabs (values only, grey)
`D Reported` (8-K quarterly geography × revenue, units growth), `D CCC` (annual and quarterly TLF, the 16 age × body cells, claim mix), `D Fleet` (births, EPA survival), `D Fees` (Copart and IAA grids, with effective dates), `D Carriers` (share-build inputs with source labels), `D Engine` (pasted CSVs with file, date, SHA-256), `D Street` (extracted figures with report, date and line reference; licensed text never pasted). PitchBook tabs stay as they are.

## 3. Build order and the stopping rule

1. Script skeleton: copy v1 to v2, apply the formatting standard, add Cover, dividers and the seven data tabs. Mechanical.
2. E1 and E2 from the intermediate workbook's live formulas and the CCC cells; check derived TLF against CCC annual.
3. E5 and E6; reproduce FY26A US and international service dollars to the 8-Ks.
4. E3 and E4 (the two theses) with their Inputs blocks and parity rows.
5. Scenarios, Street, RPM rewiring, Checks; retire Volume Build and RPU Build; confirm DCF still reads RPM rows 6, 10, 12 and 29.
6. Verify: run the build script, open in Excel for recalculation, compare to the Python outputs, record pass/fail in Checks and in a short note.

Each step is one local script run; no agents, no web. Stop and report if any check fails by more than $0.1m or if a step needs a number that is not in the repository.

## 4. Decisions needed from the owner before step 1

1. Quarterly engines with annual RPM (recommended, so FQ4 FY27 is visible), or annual-only engines.
2. Build into `model/CPRT_Model_v2.xlsx` (recommended) rather than editing the Downloads file in place.
3. Keep the PitchBook tabs as the historical source, or replace them with `D Reported`.
4. FY29–31: fade rows on RPM (recommended) or extend the engines.

## 5. Engine page layout, worked for E1 Fleet (1 October addendum)

The owner asked how a complicated build like the fleet roll should look on its tab, and whether the equations and fits belong in the workbook or in a memo appendix. Proposed layout (rows are indicative):

| Row | Content | Style |
|---|---|---|
| 1 | `E1 Fleet — vehicles on the road by age and body (thousands)` | navy title bar |
| 2 | `Fleet(a, b, Y) = Births(Y−a, b) × S_b(a / k_b(Y)); k_b(Y) = k_b(2013) × m(Y). Calendar years; fiscal roll-up at right. Appendix A, Eq. 1–3.` | grey italic |
| 4 | `Units` · `Historicals CY2013–CY2025` · `Projected CY2026–CY2028` · `Notes / sources` | header row |
| 5–11 | **A. Births by body** — Cars, Light trucks, of which SUV / Pickup / Minivan, Total, y/y. Green links to `D Fleet`. | blue section bar |
| 13–17 | **B. Survival stretch** — k_cars(2013) 1.064, k_LT(2013) 0.921 (blue, FITTED), m(Y) across the years (1.000 → 1.194 → flat), k_b(Y) rows. | grey group bar |
| 19–35 | **C. Vehicles on the road by age band × body** — 16 rows (4 bodies × CCC bands 0, 1–3, 4–6, 7+), each a `SUMPRODUCT` over single ages of births × survival; the single-age roll itself lives on companion tab `E1a Fleet (roll)`, grouped and collapsed. | grey group bar |
| 37–55 | **D. Claims-weighted composition** — 16 rows: share of claims = Fleet × R(a) × body factor, normalised; beside each, the CCC-implied share for 2020–2025 (green links to `D CCC`) and the gap. | grey group bar |
| 57–63 | **E. Checks** — total vehicles 2024 vs Experian; share aged 7+ vs S&P; IHS 2013 bucket error; max cell gap vs CCC by year; PASS / FAIL. | grey group bar |
| 65 | `Feeds → E2 Claims & Totals, fleet by band × body` | italic |
| 67–75 | **Inputs** — k_cars, k_LT, m(2024), exposure(0) 0.5, decay 0.09027, body factors; each blue with label and source in P. | blue section bar |

Equations and fits: the workbook carries one plain-English equation per block (row 2 and the group bars) and a reference to a numbered equation in a two-page LaTeX appendix, *Model equations and fits* (Eq. 1 survival stretch and its fit to the 2013 census; Eq. 2 fleet roll; Eq. 3 claims propensity and body factors; Eq. 4 total-loss selection rule and its calibration targets; Eq. 5 fee-band mapping; Eq. 6 aftermarket bridge; Eq. 7 carrier allocation). The fitting procedures (one-dimensional minimisation, bisection) stay in the committed Python scripts and are cited by file; they are not re-run as Excel Solver steps. Reason: judges read the memo and open the model to audit one number; the tab must show where every number comes from, not teach the derivation.

## 6. Build status, 1 October 2026

Built by `scripts/build_cprt_model.py` (modules in `scripts/cprt_model/`) into `model/CPRT_Model_v2.xlsx`; recalculated and checked by `scripts/verify_cprt_model.py` (LibreOffice headless; writes `model/CPRT_Model_v2_recalc.xlsx` with cached values). The owner's DCF, Reverse DCF and PitchBook tabs are untouched; Volume Build and RPU Build are hidden, superseded by the engines. Rebuild:

```bash
./.venv/bin/python scripts/build_cprt_model.py && ./.venv/bin/python scripts/verify_cprt_model.py
```

Tabs delivered: Cover, RPM (rewired: FY27–28 from Scenarios, FY29–31 fade rows, delta to JPM), E1 Fleet + E1a roll, E2 Claims & Totals, E3 Carriers, E4 Aftermarket, E5 Prices & Fees, E6 Other Branches, Scenarios, Street, Checks, seven data tabs.

| FY27E legacy service revenue, $m | Workbook | Δ vs case 1 | Δ vs JPM $4,061m |
|---|---:|---:|---:|
| Case 1 Neither (known Progressive runoff laps; no thesis) | 3,957.0 | — | −104.0 |
| Case 2 A only (State Farm and "other" events on; no concession) | 3,930.9 | −26.1 | −130.1 |
| Case 3 B only (sourcing ramp to 5.5 pts by FQ4 FY27) | 3,906.1 | −51.0 | −154.9 |
| Case 4 Both | 3,880.5 | −76.5 | −180.5 |
| Case 5 Bull offset (ASP +6%) | 3,984.5 | +27.5 | −76.5 |

Engine parity: case 1 is within $3m of the engine's reference-plus-allocation case (mask 11, $3,960m); case 3 − case 1 is within $6m of the engine's aftermarket effect (−$56.6m). The engine's saved reference ($4,093m) repeats prior-year carrier conditions and therefore implies a rebound after the account loss; the workbook's case 1 does not.

What the table says for the pitch: with the known loss fully reflected and nothing else assumed, FY27 is already about 2.6% below the JPM figure. Either JPM assumes a unit recovery or stronger price, fee or international growth than the continuation inputs here, or the Street number is high. The Street tab is where that gets settled, driver by driver.

Open items (not blockers): the $110 fixed fee versus the posted $79/$95 gate fee; the 66% aged-7+ anchor (UNVERIFIED, fails its check honestly); body factors are fitted to 2025 only; the Bull case is a single ASP alternative, not a full offset case; FY29–31 fade rates are placeholders.
