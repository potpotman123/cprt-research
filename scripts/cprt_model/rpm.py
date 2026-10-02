"""Rewire the owner's RPM: FY27-28 from the selected scenario, FY29-31 by fade rows, implied RPU, delta to Street."""
from .common import *
def build(wb, ctx):
    ws = wb['RPM']; S = ctx['sel_rows']; NOTES_COL['RPM'] = 'P'
    put(ws, 'B3', 'Scenario selector — click D3 and choose a case (drives rows 10, 12, 21 for FY27–28; case index in I3)', 'label', b=True)
    for m in [str(m) for m in ws.merged_cells.ranges]:
        if m.startswith('D3:'): ws.unmerge_cells(m)
    ws.merge_cells('D3:H3'); dropdown(ws, 'D3', ctx['case_names'], index_cell='I3', default_index=2, list_col='U', list_row=4, title='Scenario options (list source for the D3 dropdown; do not edit)')
    for fy, col in (('FY27', 'I'), ('FY28', 'J')):
        a = ACOL[2027 if fy == 'FY27' else 2028]
        put(ws, f'{col}10', f"=Scenarios!{a}{S['legacy']}", 'link', F_MONEY); put(ws, f'{col}12', f"=Scenarios!{a}{S['purchased']}", 'link', F_MONEY)
        put(ws, f'{col}21', f"=Scenarios!{a}{S['units']}/Scenarios!{ACOL[2026 if fy=='FY27' else 2027]}{S['units']}-1", 'link', F_PCT)
    for col, prev in (('K', 'J'), ('L', 'K'), ('M', 'L')):
        put(ws, f'{col}10', f'={prev}10*(1+$D$43)', fmt=F_MONEY); put(ws, f'{col}12', f'={prev}12*(1+$D$44)', fmt=F_MONEY); put(ws, f'{col}21', '=$D$45', 'link', F_PCT)
    for col, prev in (('I', 'H'), ('J', 'I'), ('K', 'J'), ('L', 'K'), ('M', 'L')):
        put(ws, f'{col}33', f'={col}10*1000/{col}29', fmt=F_USD); put(ws, f'{col}34', f'={col}33/{prev}33-1', fmt=F_PCT)
    put(ws, 'P10', 'FY27–28 from Scenarios (selected case); FY29–31 fade at row 43', 'note'); put(ws, 'P12', 'FY27–28 from Scenarios (E6 purchased overlay); FY29–31 fade at row 44', 'note')
    put(ws, 'P21', 'FY27–28 from Scenarios (E2 pool × E3 share × E4); FY29–31 fade at row 45', 'note'); put(ws, 'P33', 'Implied: service revenue ÷ global fee units (no longer a driver)', 'note'); put(ws, 'P34', 'Implied from row 33', 'note')
    for r, note in ((21, 'FY25–26 history: owner-entered from Copart calls (US insurance units y/y); see D Reported'), (22, 'Owner-entered from Copart calls (US non-insurance units y/y, VERIFIED FQ4 FY26 +0.2%)'), (23, 'Owner-entered from Copart calls (international units y/y)'), (36, 'Disclosed by Copart (calls, 8-Ks); owner-entered in v1'), (37, 'Disclosed by Copart (calls); owner-entered in v1'), (38, 'Disclosed by Copart (calls); owner-entered in v1'), (39, '8-K segment revenue; owner-entered in v1 (see D Reported geography table)'), (40, '8-K segment revenue; owner-entered in v1 (see D Reported geography table)')):
        if not ws[f'P{r}'].value: put(ws, f'P{r}', note, 'note')
    group(ws, 42, 'Beyond the engine horizon (FY29–31): fade inputs')
    for r, lab, val, note in ((43, 'Service revenue growth, FY29–31', 0.03, 'ASSUMED: roughly the FY28 engine growth; the engines stop at FY28'), (44, 'Vehicle-sales revenue growth, FY29–31', 0.0, 'ASSUMED flat'), (45, 'US insurance unit growth, FY29–31', 0.01, 'ASSUMED')):
        label(ws, r, lab, '%', note=note); put(ws, f'D{r}', val, 'input', F_PCT)
    group(ws, 47, 'Delta Δ to Street and to the engine (FY27E service revenue, legacy, ex-ACV)')
    label(ws, 48, 'JPMorgan 11 Sep 2026', '$M', note='VERIFIED, licensed report held locally'); put(ws, 'D48', f"={ctx['jpm_cell']}", 'link', F_MONEY)
    label(ws, 49, 'Model, selected case', '$M'); put(ws, 'D49', '=I10', fmt=F_MONEY)
    label(ws, 50, 'Δ model − JPM', '$M', b=True); put(ws, 'D50', '=D49-D48', fmt=F_MONEY, b=True); put(ws, 'E50', '=D50/D48', fmt=F_PCT, b=True)
    label(ws, 51, 'Engine saved reference (mask 10) / reference + allocation (mask 11, comparable with case 1)', '$M', note='ENGINE; see Scenarios summary')
    s0 = ctx['summary_row0']; n = ctx['ncases']; put(ws, 'D51', f'=Scenarios!D{s0+n+2}', 'engine', F_MONEY); put(ws, 'E51', f'=Scenarios!D{s0+n+3}', 'engine', F_MONEY)
    for r in range(42, 52):
        for c in range(2, 20):
            if ws.cell(r, c).value is None: ws.cell(r, c).font = font()
