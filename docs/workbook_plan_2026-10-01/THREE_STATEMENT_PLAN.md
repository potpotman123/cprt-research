# Plan: WACC build, three-statement model, Via-style cover and Solstice-style summary — 2 October 2026

Plan only; nothing changes until approved. Standing rules for the build: the current look and tab structure stay as they are; the owner's Reverse DCF numbers are not touched (the WACC build goes beside them); only top-line revenue (from the RPM) and gross margin deviate from Barclays' 11 September model; every other line follows Barclays where it publishes one and Copart's FY2026 actual ratio, held flat and labelled, where it does not; every number has a source on D Facts, D Barclays or the new D 10-K tab.

## 0. Build mechanics change (needed first)

The build script currently regenerates the workbook from the v1 skeleton, which would wipe the owner's reorganisation (the MODEL divider, Sheet1, the unhidden Volume/RPU Build tabs, the Reverse DCF rework). From this step on the script takes the **current workbook as its base** and regenerates only the generated tabs (engines, Scenarios, Street, Key Drivers, Sources, Checks, data tabs, and the new tabs below). Owner-authored tabs (RPM layout, DCF, Reverse DCF, Sheet1) are left alone except for explicitly listed one-cell links.

## 1. Tab map after the change (new or changed tabs in bold)

| Position | Tab | Content | Sources | Feeds |
|---|---|---|---|---|
| 1 | **Cover** (rebuilt, Via-style) | Ticker; current price and date; price target (from DCF); implied upside; key statistics: market cap, EV, cash & HTM, debt (finance leases), NCI, 52-week range; fully diluted shares: basic shares + treasury-method options + unvested RSUs; FY26A revenue and adjusted EBITDA; colour and label legend; one-line tab map | D 10-K FY26 (shares, options, RSUs, cash, leases), DCF (target), D Facts (price) | — |
| 2 | Key Drivers (kept) | Add: 3SM EPS, FCF and their Δ to Barclays | 3SM | — |
| 3 | **Summary** (new, Solstice-style) | Headline financials FY26A–FY29E (revenue, adj. EBITDA, GAAP EPS, UFCF, margins); Barclays and consensus estimates with % Δ; component delta to Street: US insurance units, RPU, international, gross margin, each in $m of FY27E revenue or EBITDA | 3SM, Scenarios, Street, D Barclays | memo front page |
| 4 | MODEL divider, RPM (kept) | Unchanged | | 3SM revenue |
| 5 | **3SM** (new) | Income statement, balance sheet, cash flow, FY2022A–FY2031E, with supporting schedules beneath (see §2) | PB tabs (history), RPM, D Barclays, D 10-K FY26 | DCF (optional links), Summary, Cover |
| 6 | DCF (kept) | Unchanged structure. Optional one-cell links on approval: WACC ← Reverse DCF build; EBIT, D&A, SBC, capex, ΔNWC ← 3SM | | |
| 7 | Reverse DCF (kept) + **WACC and tax build** in columns R–X beside the owner's block | Capital structure; cost of debt; cost of equity (CAPM with dated risk-free, ERP and a peer-beta table); WACC; effective-tax-rate build (statutory, state, FDII, option benefit; cash-tax series; Barclays-implied) | D Facts (rates, betas, dates), D 10-K FY26 (tax note), D Barclays | DCF WACC and tax rows (on approval) |
| 8–15 | Engines, Scenarios, Street, Sources, Checks (kept) | Checks gains: balance sheet balances, cash ties, Barclays parity rows (EBITDA, EPS, CFO, cash) | | |
| 16+ | DATA: D Reported, D Facts, **D Barclays** (re-added, data only), **D 10-K FY26** (new), D Coverage, D CCC, D Fleet, D Fees, D Carriers, D Engine, PB tabs | D 10-K FY26 holds the balance-sheet detail, share and option counts, SBC, interest income, lease and tax-note figures with page anchors | | |

## 2. The 3SM and its schedules (Via layout: statements first, schedules beneath, one row per driver, `% of revenue` or days convention stated)

**Income statement.** Service revenue and vehicle sales from the RPM (selected case). Yard and fleet operations cost = units × facility cost per unit (the owner's DCF convention, so gross margin moves with volume: operating leverage is the one margin effect our theses carry). Cost of vehicle sales at Copart's FY26 ratio to vehicle sales. Gross profit and margin. G&A at the ratio Barclays' EBITDA margin implies (40.2%, 40.8%, 41.3%), held at FY29 after; D&A = Barclays EBITDA − EBIT (226, 234, 243); operating income; interest income = yield on average cash (Barclays pre-tax − EBIT ≈ 140 a year, cross-checked to the 10-K yield); pre-tax; tax at the built rate; NCI; net income; diluted EPS on the share schedule; adjusted-EBITDA reconciliation with a parity row to Barclays.

**Balance sheet** (history from the PitchBook tabs FY22A–FY26A): cash & HTM securities (plug from the cash flow), receivables, vehicle pooling costs, prepaid and other; PP&E (schedule), operating-lease ROU assets, goodwill and intangibles (flat; ACV only if toggled), other non-current; AP and accrued, deferred revenue, lease liabilities, finance leases/debt (88), other long-term; equity rolled with net income, SBC and buybacks. Balance check row.

**Cash flow.** Net income + D&A + SBC + other non-cash − ΔNWC = CFO (Barclays 1,646 / 1,731 / 1,813 as parity rows); capex (Barclays −500 a year, or % of revenue after FY29); acquisitions (ACV gate, default excluded); buybacks (schedule); ending cash with a tie to the balance sheet and a parity row to Barclays' cash (5,656 / 6,907 / 8,240).

**Schedules beneath the statements:**
1. Working capital: receivables and vehicle pooling costs in days of revenue; prepaid in days; AP/accrued in days of cost; deferred revenue in days of revenue; NWC and ΔNWC, with Barclays' −83 a year as the parity row.
2. PP&E and capex: opening, capex, depreciation rate on opening balance, closing; D&A tied to the income statement.
3. Leases: ROU assets and lease liabilities at FY26 ratios to revenue (10-K).
4. Cash and interest income: yield on average cash and HTM from the 10-K; interest income to the income statement.
5. SBC: % of revenue from the 10-K cash flow statement.
6. Shares and buybacks: basic shares, net issuance, treasury-method options, RSUs; buyback dollars as the input (Barclays' flat 933m share count implies none after FY27); diluted shares to EPS.
7. Tax: structural rate from the Reverse DCF tax build (statutory 21%, state +1.2, FDII −2.5, option benefit −0.4 → 19.7%; Barclays-implied 20.3%; cash taxes 21.6–21.7% of pre-tax in FY25–26), applied as a single rate with the components visible.
8. ACV acquisition: toggle; consideration $1.9bn (DCF), contribution gated until classified.

## 3. WACC build (Reverse DCF tab, columns R–X)

Capital structure: market cap, debt including finance leases, cash. Cost of debt: Copart carries no funded debt; show the revolver pricing from the 10-K for completeness and weight it at the actual debt (≈0). Cost of equity: 10-year Treasury (dated, sourced), equity risk premium (Damodaran, dated), peer betas (RB Global, OPENLANE, ACV Auctions, Carvana, Copart's own 5-year monthly; source and date each), selected beta, no size premium; CAPM. WACC with weights. Output cell offered to the DCF's WACC row as a one-cell link.

## 4. Order of work, cost, stopping rule

1. Switch the build base to the current workbook; re-add D Barclays as data only. 2. D 10-K FY26 extracts (local reads of the filing on disk). 3. WACC and tax build. 4. 3SM and schedules with checks. 5. Cover and Summary. 6. Optional DCF links on approval. 7. Verify, commit. All local; no agents; a handful of fetches at most (Treasury yield, ERP, peer betas) through the logged fetcher. Stop and ask if a line Barclays does not publish has no FY26 actual to hold.

## 5. Questions for the owner

1. **Sheet1**: what is it, and should the build leave it alone (default: yes)?
2. **Volume Build and RPU Build** are visible again; keep visible or hide?
3. **DCF links**: may the DCF's WACC row and UFCF lines point at the new builds (one cell each), or keep the DCF fully as is?
4. **Horizon**: 3SM to FY2031E (DCF horizon), with FY30–31 at Barclays' FY29 ratios, or stop at FY29?
5. **Gross margin**: volume-driven via facility cost per unit (recommended) or Barclays' implied margin held?
6. **Peer set for beta**: RB Global, OPENLANE, ACV, Carvana, plus Copart's own, or your list?
