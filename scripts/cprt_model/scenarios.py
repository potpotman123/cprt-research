"""Scenarios: Neither / A only / B only / Both / Bull, assembled live from the engines; engine parity; selected-case outputs for RPM."""
from .common import *
CASES = [(1, 'Neither (known Progressive runoff only; no thesis)', 0, 0, "='E5 Prices & Fees'!$D$44"), (2, 'A only (contestable allocation: events, drift, concessions)', 1, 0, "='E5 Prices & Fees'!$D$44"),
         (3, 'B only (aftermarket substitution)', 0, 1, "='E5 Prices & Fees'!$D$44"), (4, 'Both (A and B)', 1, 1, "='E5 Prices & Fees'!$D$44"), (5, 'Bull offset (no thesis; ASP +6%)', 0, 0, 0.06)]
ROWS = ['Insurance units', 'y/y', 'US insurance ASP', 'Core RPU', 'All-in insurance RPU', 'US insurance service revenue', 'US non-insurance service revenue', 'International service revenue', 'Legacy service revenue', 'Purchased-vehicle revenue', 'Total revenue (legacy + purchased + ACV)']
def block_row(k, i): return 7 + (k - 1) * 13 + 1 + i   # row of item i in case k's block
def build(wb, ctx):
    ws = wb.create_sheet('Scenarios'); tab_color(ws, NAVY); setup(ws)
    std_header(ws, 'Units_q = Units_{q−4} × pool ratio (E2) × share ratio (E3, base or A) × (1 + b·Δunits (E4));  ASP_q = ASP₀ (1+g)^t × (1 + b·Δprice);  RPU from E5 parameters with the case\'s seller rate.  Four common-base cases with exact interaction; never quote the own-reference delta as a Street miss.', 'Scenarios — the two theses on one common base')
    put(ws, 'B3', 'Selected case (set on RPM, cell D3)', 'label', b=True); put(ws, 'D3', '=RPM!$D$3', 'link', '0')
    section(ws, 5, 'Cases (each block is a complete quarterly path)', quarter_labels())
    P0 = 75
    for k, name, a, b, g in CASES:
        r0 = 7 + (k - 1) * 13; group(ws, r0, f'Case {k} — {name}')
        pr = P0 + k   # parameter row for this case
        for i, lab in enumerate(ROWS):
            r = r0 + 1 + i; units = ['000s', '%', '$', '$', '$', '$M', '$M', '$M', '$M', '$M', '$M'][i]
            label(ws, r, lab, units, b=(i in (0, 8, 10)), i=(i == 1), indent=1 if i == 1 else 0)
        R = {lab: r0 + 1 + i for i, lab in enumerate(ROWS)}
        for fy, q in QUARTERS:
            c = QCOL[(fy, q)]; p = QCOL[(fy - 1, q)] if fy > 2026 else None; t = fy - 2026
            if fy == 2026:
                put(ws, f"{c}{R['Insurance units']}", f"='E5 Prices & Fees'!{c}11", 'link', F_INT, b=True); put(ws, f"{c}{R['US insurance ASP']}", "='E5 Prices & Fees'!$D$45", 'link', F_USD)
            else:
                put(ws, f"{c}{R['Insurance units']}", f"={p}{R['Insurance units']}*'E2 Claims & Totals'!{c}${E2_POOL_RATIO_ROW}*IF($D${pr}=1,'E3 Carriers'!{c}${E3_SR_A_ROW},'E3 Carriers'!{c}${E3_SR_BASE_ROW})*(1+$E${pr}*'E4 Aftermarket'!{c}${E4_DU_ROW})", fmt=F_INT, b=True)
                put(ws, f"{c}{R['y/y']}", f"={c}{R['Insurance units']}/{p}{R['Insurance units']}-1", fmt=F_PCT, i=True)
                put(ws, f"{c}{R['US insurance ASP']}", f"='E5 Prices & Fees'!$D$45*(1+$F${pr})^{t}*(1+$E${pr}*'E4 Aftermarket'!{c}${E4_DP_ROW})", fmt=F_USD)
            asp = f"{c}{R['US insurance ASP']}"; seller = f"IF($D${pr}=1,'E3 Carriers'!{c}${E3_SELLER_A_ROW},'E3 Carriers'!{c}${E3_SELLER_BASE_ROW})"
            put(ws, f"{c}{R['Core RPU']}", f"='E5 Prices & Fees'!$D$50*({asp}/'E5 Prices & Fees'!$D$45)^'E5 Prices & Fees'!$D$51+{seller}*{asp}+'E5 Prices & Fees'!$D$48", fmt=F_USD)
            put(ws, f"{c}{R['All-in insurance RPU']}", f"={c}{R['Core RPU']}+'E5 Prices & Fees'!{c}24", fmt=F_USD)
            put(ws, f"{c}{R['US insurance service revenue']}", f"={c}{R['Insurance units']}*{c}{R['All-in insurance RPU']}/1000", fmt=F_MONEY)
            put(ws, f"{c}{R['US non-insurance service revenue']}", f"='E6 Other Branches'!{c}8", 'link', F_MONEY); put(ws, f"{c}{R['International service revenue']}", f"='E6 Other Branches'!{c}12", 'link', F_MONEY)
            put(ws, f"{c}{R['Legacy service revenue']}", f"={c}{R['US insurance service revenue']}+{c}{R['US non-insurance service revenue']}+{c}{R['International service revenue']}", fmt=F_MONEY, b=True).border = TOP
            put(ws, f"{c}{R['Purchased-vehicle revenue']}", f"='E6 Other Branches'!{c}16", 'link', F_MONEY)
            put(ws, f"{c}{R['Total revenue (legacy + purchased + ACV)']}", f"={c}{R['Legacy service revenue']}+{c}{R['Purchased-vehicle revenue']}+'E6 Other Branches'!{c}19", fmt=F_MONEY, b=True)
        for lab in ('Insurance units', 'US insurance service revenue', 'US non-insurance service revenue', 'International service revenue', 'Legacy service revenue', 'Purchased-vehicle revenue', 'Total revenue (legacy + purchased + ACV)'):
            annual_sum(ws, R[lab], F_INT if lab == 'Insurance units' else F_MONEY, b=lab in ('Insurance units', 'Legacy service revenue', 'Total revenue (legacy + purchased + ACV)'))
        for fy in (2027, 2028): put(ws, f"{ACOL[fy]}{R['y/y']}", f"={ACOL[fy]}{R['Insurance units']}/{ACOL[fy-1]}{R['Insurance units']}-1", fmt=F_PCT, i=True)
        for fy, col in ACOL.items():
            put(ws, f"{col}{R['All-in insurance RPU']}", f"={col}{R['US insurance service revenue']}*1000/{col}{R['Insurance units']}", fmt=F_USD)
            put(ws, f"{col}{R['US insurance ASP']}", f"=AVERAGE({QCOL[(fy,1)]}{R['US insurance ASP']}:{QCOL[(fy,4)]}{R['US insurance ASP']})", fmt=F_USD)
    section(ws, P0, 'Case parameters', ['a (thesis A)', 'b (thesis B)', 'ASP growth', 'Label'])
    for k, name, a, b, g in CASES:
        r = P0 + k; label(ws, r, f'Case {k}: {name}'); put(ws, f'D{r}', a, 'toggle', '0'); put(ws, f'E{r}', b, 'toggle', '0'); put(ws, f'F{r}', g, 'link' if isinstance(g, str) else 'input', F_PCT); put(ws, f'G{r}', 'TOGGLE / ASSUMED', 'note')
    label(ws, P0 + 6, 'JPMorgan FY27 service revenue, 11 Sep 2026 (ex-ACV)', '$M', note='VERIFIED, licensed report held locally, Table 3 lines 275–278'); put(ws, f'D{P0+6}', 4061, 'input', F_MONEY)
    S0 = P0 + 9; group(ws, S0, 'Summary — FY27 legacy service revenue by case; quote both deltas, never only the larger one')
    for j, h in enumerate(['FY27E', 'Δ vs Neither (own reference)', 'Δ vs JPM $4,061m', 'Δ vs JPM %', 'FY28E']): put(ws, f'{L(4+j)}{S0}', h, 'label', b=True)
    for k, name, *_ in CASES:
        r = S0 + k; label(ws, r, f'Case {k}: {name}'); lr = block_row(k, 8)
        put(ws, f'D{r}', f'={ACOL[2027]}{lr}', fmt=F_MONEY, b=True); put(ws, f'E{r}', f'=D{r}-$D${S0+1}', fmt=F_MONEY); put(ws, f'F{r}', f'=D{r}-$D${P0+6}', fmt=F_MONEY); put(ws, f'G{r}', f'=F{r}/$D${P0+6}', fmt=F_PCT); put(ws, f'H{r}', f'={ACOL[2028]}{lr}', fmt=F_MONEY)
    e0, e1 = ctx['eng_ss']; r = S0 + 7
    label(ws, r, 'Engine parity — saved reference (mask 10) FY27 service revenue', '$M', note='ENGINE: D Engine; the engine reference repeats prior-year carrier conditions (implies a rebound after the account loss), so it sits above case 1 by design')
    put(ws, f'D{r}', f"=SUMIFS('D Engine'!$D${e0}:$D${e1},'D Engine'!$B${e0}:$B${e1},10)", 'engine', F_MONEY)
    label(ws, r + 1, 'Engine parity — reference + allocation (mask 11): the like-for-like comparator for case 1', '$M', b=True); put(ws, f'D{r+1}', f"=SUMIFS('D Engine'!$D${e0}:$D${e1},'D Engine'!$B${e0}:$B${e1},11)", 'engine', F_MONEY, b=True); put(ws, f'E{r+1}', f'=D{S0+1}', fmt=F_MONEY, b=True); put(ws, f'F{r+1}', '← workbook case 1', 'note')
    label(ws, r + 2, 'Engine parity — aftermarket effect (mask 14 − mask 10): the comparator for case 3 − case 1', '$M', b=True); put(ws, f'D{r+2}', f"=SUMIFS('D Engine'!$D${e0}:$D${e1},'D Engine'!$B${e0}:$B${e1},14)-D{r}", 'engine', F_MONEY, b=True); put(ws, f'E{r+2}', f'=E{S0+3}', fmt=F_MONEY, b=True); put(ws, f'F{r+2}', '← workbook case 3 − case 1', 'note')
    label(ws, r + 3, 'Engine all four drivers (mask 15), for reference only: its allocation term is measured against a rebound reference, so it is not comparable with case 4 − case 1', '$M', i=True); put(ws, f'D{r+3}', f"=SUMIFS('D Engine'!$D${e0}:$D${e1},'D Engine'!$B${e0}:$B${e1},15)", 'engine', F_MONEY)
    O0 = S0 + 12; group(ws, O0, 'Selected case → RPM')
    for i, (lab, item, fmt) in enumerate([('Selected: legacy service revenue', 8, F_MONEY), ('Selected: purchased-vehicle revenue', 9, F_MONEY), ('Selected: insurance units', 0, F_INT), ('Selected: total revenue', 10, F_MONEY), ('Selected: all-in insurance RPU', 4, F_USD)]):
        r = O0 + 1 + i; label(ws, r, lab, b=True)
        for col in list(QCOL.values()) + list(ACOL.values()):
            put(ws, f'{col}{r}', '=CHOOSE($D$3,' + ','.join(f'{col}{block_row(k, item)}' for k in range(1, 6)) + ')', fmt=fmt, b=True)
    ctx['sel_rows'] = {'legacy': O0 + 1, 'purchased': O0 + 2, 'units': O0 + 3, 'total': O0 + 4, 'rpu': O0 + 5}; ctx['summary_row0'] = S0; ctx['jpm_cell'] = f"'Scenarios'!$D${P0+6}"
    ws.freeze_panes = 'D6'
