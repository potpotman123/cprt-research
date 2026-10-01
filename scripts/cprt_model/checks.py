"""Checks: ties to 8-Ks, identities, engine parity, typed numbers outside Inputs blocks."""
from .common import *
INPUT_START = {'E1 Fleet': 88, 'E2 Claims & Totals': 79, 'E3 Carriers': 63, 'E4 Aftermarket': 44, 'E5 Prices & Fees': 38, 'E6 Other Branches': 29, 'Scenarios': 75}
def build(wb, ctx):
    ws = wb.create_sheet('Checks'); tab_color(ws, NAVY); setup(ws, ncols=6, notes_col='H')
    title(ws, 'Checks — ties, identities, engine parity, discipline', 'PASS/FAIL cells recalculate with the workbook. Tolerances are spreadsheet acceptance tolerances, not economic confidence intervals.')
    section(ws, 4, 'Check', ['Model', 'Target', 'Difference', 'Result'])
    S = ctx['sel_rows']; g = ctx['geo_rows']; rows = []
    fy26_service = '+'.join(f"'D Reported'!$D${g[(2026,q)]}+'D Reported'!$E${g[(2026,q)]}" for q in (1, 2, 3, 4))
    rows.append(('FY26 legacy service revenue (case 1) ties to the 8-K quarterly service total', f"=Scenarios!{ACOL[2026]}{7+1+8}", f'={fy26_service}', 0.1, F_MONEY))
    rows.append(('FY26 US insurance + non-insurance service = reported US service', f"=Scenarios!{ACOL[2026]}{7+1+5}+Scenarios!{ACOL[2026]}{7+1+6}", '=' + '+'.join(f"'D Reported'!$D${g[(2026,q)]}" for q in (1, 2, 3, 4)), 0.1, F_MONEY))
    rows.append(('E1: 2024 vehicles on the road vs anchor (within 2%)', "='E1 Fleet'!D81", "='E1 Fleet'!E81", "=0.02*'E1 Fleet'!E81", F_INT))
    rows.append(('E1: largest claim-mix cell gap vs CCC 2020–2025 (within 3.5 pts)', "='E1 Fleet'!D83", 0, 0.035, F_PCT))
    rows.append(('E2: fiscal-quarter weights sum to one (FQ4 FY28)', "='E2 Claims & Totals'!O13", 1, 1e-6, '0.0000'))
    rows.append(('E3: carrier weights sum to one', "='E3 Carriers'!D16", 1, 1e-6, '0.0000'))
    rows.append(('E4: complete-bill saving at the FQ4 FY27 endpoint reproduces the documented 1.03%', "='E4 Aftermarket'!K14", -0.0103, 0.0003, F_PCT2))
    rows.append(('E5: core RPU at the anchor reproduces the engine ($851.51)', "='E5 Prices & Fees'!D23", "='E5 Prices & Fees'!D46", 0.05, F_USD))
    e0, e1 = ctx['eng_ss']; eng = lambda m: f"SUMIFS('D Engine'!$D${e0}:$D${e1},'D Engine'!$B${e0}:$B${e1},{m})"
    rows.append(('Engine parity: case 1 (known runoff, no thesis) vs engine reference + allocation (mask 11), within $25m', f"=Scenarios!D{ctx['summary_row0']+1}", f"={eng(11)}", 25, F_MONEY))
    rows.append(('Engine parity: case 3 − case 1 (thesis B) vs engine aftermarket effect (mask 14 − mask 10), within $15m', f"=Scenarios!E{ctx['summary_row0']+3}", f"={eng(14)}-{eng(10)}", 15, F_MONEY))
    rows.append(('DCF still reads RPM: DCF revenue FY27E equals RPM total revenue FY27E', '=DCF!I6', '=RPM!I6', 0.001, F_MONEY))
    r = 5
    for lab, model, target, tol, fmt in rows:
        label(ws, r, lab); put(ws, f'D{r}', model, 'link', fmt); put(ws, f'E{r}', target, 'link' if isinstance(target, str) else 'input', fmt); put(ws, f'F{r}', f'=D{r}-E{r}', fmt=fmt)
        tolf = tol if isinstance(tol, str) else str(tol); put(ws, f'G{r}', f'=IF(ABS(F{r})<={tolf.lstrip("=")},"PASS","FAIL")', b=True); r += 1
    # discipline: typed numbers inside calculation blocks (above each tab's Inputs section)
    typed = []
    for name, start in INPUT_START.items():
        if name not in wb.sheetnames: continue
        t = wb[name]
        for row in t.iter_rows(min_row=6, max_row=start - 1):
            for c in row:
                if isinstance(c.value, (int, float)) and not isinstance(c.value, bool) and c.font and c.font.color is not None and c.font.color.rgb in (f'00{C_INPUT}', f'FF{C_INPUT}', C_INPUT):
                    typed.append(f'{name}!{c.coordinate}={c.value}')
    r += 1; label(ws, r, 'Typed numbers inside calculation blocks (should be reference rows only)', b=True); put(ws, f'D{r}', len(typed), 'formula', '0'); put(ws, f'E{r}', '; '.join(typed)[:400], 'note')
    r += 2; put(ws, f'B{r}', 'Not checked here: the economic coefficients (every ASSUMED input). See docs/source_trace_2026-10-01/README.md for the 21 numbers with no source.', 'note')
    ws.freeze_panes = 'D5'
