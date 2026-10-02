"""Key Drivers: the thesis-critical numbers in one place, every cell a link to its source cell."""
from .common import *
def build(wb, ctx):
    ws = wb.create_sheet('Key Drivers'); tab_color(ws, NAVY); setup(ws, label_w=70, ncols=4, notes_col='H')
    title(ws, 'Key Drivers — the numbers the three theses turn on (all cells link to the engines; labels and sources travel with them)', 'Green = link. Change an input on its engine tab, not here. FQ4 FY26 is the last reported quarter; FQ1 FY27 is the first forecast quarter.')
    for j, h in enumerate(['Value', 'Unit', 'Label']): put(ws, f'{L(4+j)}4', h, 'label', b=True); put(ws, 'H4', 'Source / where it lives', 'note')
    s0 = ctx['summary_row0']; P0 = 100
    blocks = [
     ('Thesis 1 — coverage persistence (E2 block F, D Coverage)', [
      ('Motor-vehicle-insurance CPI, latest month y/y (Aug 2026)', "='D Coverage'!Q17", '%', 'VERIFIED', 'BLS CUUR0000SETE, raw/bls; the premium index is falling'),
      ('Premium growth used for FY27 (selected path; E2 row 127 selects BLS trend or S&P-consistent)', "='E2 Claims & Totals'!D123", '%', 'selected', 'E2 D123'),
      ('Average hourly earnings growth, latest year', "='E2 Claims & Totals'!D124", '%', 'VERIFIED', 'BLS CES0500000003'),
      ('Premium burden 2023 (level at which households left) / 2026 to date (2025 = 1)', "='E2 Claims & Totals'!J108", 'x', 'MEASURED', 'E2 row 108; 2026 value in M108 (0.956): still 10% above 2023 after the 2026 premium decline'),
      ('First quarter the burden falls below its 2023 level, selected path', "='E2 Claims & Totals'!D131", '', 'MEASURED', 'E2 D131; "beyond FQ4 FY28" on the S&P-consistent path'),
      ('S&P auto combined ratio path 2025P / 2026P / 2027P', "='D Coverage'!D20", 'ratio', 'VERIFIED (republication)', 'D Coverage rows 20–22: 94.5 / 97.1 / 98.9, breaching 100 in 2028 (Carrier Management, 6 Jan 2026)'),
      ('Uninsured-motorist rate 2017 / 2023', "='D Coverage'!D8", '%', 'VERIFIED endpoints', 'IRC release 20 Feb 2025; 2023 = 15.4% (D Coverage J8)'),
      ('Physical-damage coverage index 2017 (2025 = 1.000; the 2017–23 change is the measured coverage decline)', "='E2 Claims & Totals'!D107", 'x', 'MEASURED', 'E2 row 107; collision share 76–77% flat 2021–23, so the decline is the uninsured leg'),
      ('Share of insured drivers with collision coverage, 2021 / 2022 / 2023', "='D Coverage'!H9", '%', 'VERIFIED (republication)', 'III via Wayback snapshots 2024 and 2025 plus the live page: 76% / 77% / 77%'),
      ('Two-point coverage response to premium burden (ε)', "='E2 Claims & Totals'!D110", 'x', 'UNVERIFIED', 'E2 D110; n = 2'),
      ('Street-implied FY27 coverage recovery r (reverse-solved to JPM)', "='E2 Claims & Totals'!D126", '%', 'MEASURED', 'E2 D124: what the Street number needs'),
      ('Coverage ratio FQ1 FY27: sticky / premium-response / recovery', "='E2 Claims & Totals'!H116", 'x', 'paths', 'E2 rows 116–118 (H117, H118 for the other paths)'),
      ('CCC total claim volume y/y, 2024 / 2025', "='D Coverage'!K10", '%', 'VERIFIED', 'D Coverage K10 / L10 (2025 = −3.3%)')]),
     ('Thesis 2 — aftermarket substitution (E4)', [
      ('Aftermarket share of replacement-part dollars, 2025', "='E4 Aftermarket'!D47", '%', 'VERIFIED', 'CCC Crash Course 2026 (21.0% in 2024)'),
      ('Recycled share of replacement-part dollars, 2025', "='E4 Aftermarket'!D48", '%', 'VERIFIED', 'CCC (10.7% in 2024)'),
      ('Aftermarket price relative to OEM at the anchor', "='E4 Aftermarket'!D50", 'x', 'VERIFIED (historical)', 'Mitchell 2016 discounts, mean 27%; recycled set equal at the anchor'),
      ('Aftermarket relative-price drift per year (PartsTrader: OEM +4.3%, aftermarket <1%)', "='E4 Aftermarket'!D68", '%', 'VERIFIED (trend, one year)', 'E4 D68'),
      ('Aftermarket price relative to OEM by FQ4 FY28 (recycled stays at 0.73)', "='E4 Aftermarket'!O9", 'x', 'derived', 'E4 row 9'),
      ('Sourcing path selector (1 observed trend, 2 memo stress)', "='E4 Aftermarket'!D64", '', 'TOGGLE', 'E4 D64'),
      ('Cumulative aftermarket share shift at FQ4 FY27 (selected path)', "='E4 Aftermarket'!K7", 'pts', 'path', 'E4 row 7'),
      ('Complete repair-bill change at FQ4 FY27', "='E4 Aftermarket'!K14", '%', 'derived', 'E4 row 14'),
      ('Change in total-loss units at FQ4 FY27', "='E4 Aftermarket'!K40", '%', 'ENGINE-derived η × bill change', 'E4 row 40'),
      ('Change in auction price at FQ4 FY27', "='E4 Aftermarket'!K41", '%', 'ASSUMED scaling', 'E4 row 41'),
      ('Memo stress case (5.5 pts) at sourced prices: bill change / units', "='E4 Aftermarket'!D31", '%', 'derived', 'E4 D31 / E31; engine basket reproduces 1.03% in D30')]),
     ('Thesis 3 — carrier allocation (E3)', [
      ('Copart share of the insured total-loss pool, FQ4 FY26', "='E3 Carriers'!G43", '%', 'reconstructed', 'E3 row 43 (frozen weights × inherited allocation)'),
      ('Share FQ4 FY27, base (known runoff only)', "='E3 Carriers'!K43", '%', 'scenario', 'E3 row 43'),
      ('Share FQ4 FY27, thesis 3 (probability-weighted moves)', "='E3 Carriers'!K44", '%', 'scenario', 'E3 row 44; memo: 56.6% → 55.3%'),
      ('Progressive allocation to Copart, FQ4 FY26 / FQ4 FY27', "='E3 Carriers'!G20", 'share', 'UNVERIFIED path', 'E3 row 20 (K20 for FY27)'),
      ('Expected move: State Farm / Other (pts)', "='E3 Carriers'!F77", 'pts', 'UNVERIFIED', 'E3 rows 77–78: −5 pts × 45% each'),
      ('Progressive move: effect on FQ4 FY26 service revenue', "='E3 Carriers'!D83", '%', 'MEASURED chain', 'E3 row 83 (E83 = % of total revenue)'),
      ('Listed-inventory split, Copart share of duopoly (4 nights)', "='E3 Carriers'!G45", '%', 'MEASURED', 'data/csv/duopoly_daily.csv'),
      ('IAA acreage (owned + leased)', "='E3 Carriers'!E86", 'acres', 'VERIFIED', 'RB Global FY2025 10-K'),
      ('RB Global automotive lots, Q2 2026 y/y', "='E3 Carriers'!E94", '%', 'VERIFIED', 'RB Global 10-Q'),
      ('Effective seller commission, thesis 3, FQ4 FY27', "='E3 Carriers'!K56", '%', 'UNVERIFIED (Barclays 4% base)', 'E3 row 56')]),
     ('Prices, fees and the ledger (E5)', [
      ('US insurance ASP growth, FY27+ (input)', "='E5 Prices & Fees'!D44", '%', 'ASSUMED continuation', 'E5 D44; FQ4 FY26 disclosed +3.7%'),
      ('All-in insurance RPU y/y, FQ1 FY27 (base)', "='E5 Prices & Fees'!H26", '%', 'derived', 'E5 row 26'),
      ('Buyer-fee elasticity to ASP', "='E5 Prices & Fees'!D51", 'x', 'ENGINE-derived', 'E5 D51'),
      ('Insurance share of US service dollars', "='E5 Prices & Fees'!D39", '%', 'ASSUMED', 'E5 D39 (0.80 alternative)'),
      ('Implied US insurance units, FY26', "='E5 Prices & Fees'!P11", '000s', 'MODELED', 'E5 row 11')]),
     ('Outputs (Scenarios, RPM)', [
      ('JPMorgan FY27 legacy service revenue (ex-ACV), 11 Sep 2026', f"=Scenarios!D{P0+8}", '$M', 'VERIFIED (licensed)', 'Scenarios D108'),
      ('Case 0 Street-implied FY27', f"=Scenarios!D{s0+1}", '$M', 'by construction', 'Scenarios summary'),
      ('Case 1 Known facts FY27 / Δ vs JPM', f"=Scenarios!D{s0+2}", '$M', 'model', f'Scenarios D{s0+2}; Δ vs JPM in G{s0+2}'),
      ('Thesis 2 FY27 / Δ vs case 1', f"=Scenarios!D{s0+4}", '$M', 'model', f'Scenarios E{s0+4}'),
      ('Thesis 3 FY27 / Δ vs case 1', f"=Scenarios!D{s0+5}", '$M', 'model', f'Scenarios E{s0+5}'),
      ('All three FY27 / Δ vs JPM', f"=Scenarios!D{s0+6}", '$M', 'model', f'Scenarios G{s0+6}'),
      ('Selected case on the RPM (cell D3) and its FY27 service revenue', "=RPM!D3", 'case', 'selector', 'RPM D3; I10 holds the revenue'),
      ('Selected case Δ to JPM', "=RPM!D50", '$M', 'model', 'RPM D50 (E50 in %)')])]
    r = 5
    for name, items in blocks:
        group(ws, r, name); r += 1
        for lab, f, unit, lbl, note in items:
            label(ws, r, lab, note=note); fmt = F_PCT if unit == '%' else F_MONEY if unit == '$M' else F_INT if unit in ('000s', 'acres') else '0.000' if unit in ('x', 'share', 'pts') else '0'
            put(ws, f'D{r}', f, 'link', fmt); put(ws, f'E{r}', unit, 'label', i=True); put(ws, f'F{r}', lbl, 'note'); r += 1
        r += 1
    ws.freeze_panes = 'D5'
