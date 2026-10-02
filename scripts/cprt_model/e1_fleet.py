"""E1 Fleet (summary) and E1a Fleet (roll): births x stretched EPA survival, by calendar year 2019-2028."""
from .common import *
BODIES = [('Car', 'Car', 'C', 'J', 4), ('SUV', 'Utility vehicle (SUV)', 'D', 'K', 5), ('Pickup', 'Pickup', 'E', 'K', 5), ('Van', 'Van / minivan', 'F', 'K', 5)]  # key, label, births col on D Fleet, survival col, k row on E1a
BANDS = ['0 (current or newer)', '1–3 years', '4–6 years', '7+ years']
AGES = range(0, 46)
def band(a): return 0 if a == 0 else 1 if a <= 3 else 2 if a <= 6 else 3
def build(wb, ctx):
    b0, b1 = ctx['births']; s0, s1 = ctx['surv']
    BY = f"'D Fleet'!$B${b0}:$B${b1}"; SR = lambda col: f"'D Fleet'!${col}${s0}:${col}${s1}"
    # ---------------- derived columns on D CCC: claim share implied by the cells
    dc = wb['D CCC']; r0, r1 = ctx['ccc_r0'], ctx['ccc_r1']
    dc.cell(4, 10, 'TL mix / TLF').font = font(b=True); dc.cell(4, 11, 'Implied claim share').font = font(b=True)
    for r in range(r0, r1 + 1):
        put(dc, f'J{r}', f'=G{r}/F{r}', fmt='0.0000'); put(dc, f'K{r}', f'=J{r}/SUMIFS($J${r0}:$J${r1},$B${r0}:$B${r1},B{r})', fmt='0.0000')
    dc.cell(3, 10, 'Derived (black): share of claims in each cell = (TL mix ÷ TLF), normalised within the year').font = font(C_NOTE, i=True, sz=10)
    # ---------------- E1 Fleet summary
    ws = wb.create_sheet('E1 Fleet'); tab_color(ws, '7030A0'); setup(ws, ncols=10, notes_col='P')
    title(ws, 'E1 Fleet — vehicles on the road by age and body (thousands)', 'Fleet(a, b, Y) = Births(Y−a, b) × S_b(a ÷ k_b(Y));  k_b(Y) = k_b(2013) × m(Y).  Calendar years; feeds E2 by fiscal-quarter weights.  Appendix A, Eq. 1–3.')
    for y in CYEARS: put(ws, f'{CYCOL[y]}3', y, 'note').alignment = Alignment(horizontal='right')
    ws['C3'] = 'CY'; ws['C3'].font = font(C_NOTE, i=True, sz=10)
    header(ws, 4, None, hist_span=(4, 10), proj_span=(11, 13), notes_col='P')
    section(ws, 5, 'A. Births by body (new light vehicles sold in the calendar year)', [f'CY{y}' for y in CYEARS])
    r = 6
    for key, lab, bc, _, _ in BODIES:
        label(ws, r, lab, '000s', note='D Fleet; Ward\'s/ORNL to 2021, FRED 2022–25 (VERIFIED); SUV/pickup/van split is an EPA composition proxy (ASSUMED)' if key == 'Car' else '')
        for y in CYEARS: put(ws, f'{CYCOL[y]}{r}', f"=INDEX('D Fleet'!${bc}${b0}:${bc}${b1},MATCH({CYCOL[y]}$3,{BY},0))", 'link', F_INT)
        r += 1
    label(ws, r, 'Total light vehicles', '000s', b=True)
    for y in CYEARS: put(ws, f'{CYCOL[y]}{r}', f'=SUM({CYCOL[y]}6:{CYCOL[y]}9)', fmt=F_INT, b=True).border = TOP
    r += 1; label(ws, r, '   y/y growth', '%', i=True)
    for i, y in enumerate(CYEARS):
        if i: put(ws, f'{CYCOL[y]}{r}', f'={CYCOL[y]}10/{CYCOL[CYEARS[i-1]]}10-1', fmt=F_PCT, i=True)
    group(ws, 13, 'B. Survival stretch  (k = 1 is the raw EPA schedule; k > 1 means vehicles last longer)')
    label(ws, 14, 'm(Y): drift multiplier, linear 2013 → 2024, flat after', 'x', note='FITTED to two 2024 count anchors (Inputs rows); AGE_CURVES.md §2.4')
    label(ws, 15, 'k_cars(Y)', 'x'); label(ws, 16, 'k_light trucks(Y)', 'x')
    for y in CYEARS:
        c = CYCOL[y]
        put(ws, f'{c}14', f'=1+($D$92-1)*MIN(MAX({c}$3-2013,0),11)/11', fmt=F_X); put(ws, f'{c}15', f'=$D$90*{c}14', fmt=F_X); put(ws, f'{c}16', f'=$D$91*{c}14', fmt=F_X)
    group(ws, 18, 'C. Vehicles on the road by age band × body (thousands; from E1a roll)')
    r = 19; cell_rows = {}
    for key, lab, *_ in BODIES:
        for bi, bl in enumerate(BANDS):
            label(ws, r, f'{lab} — {bl}', '000s', indent=1 if bi else 0)
            for y in CYEARS:
                c = CYCOL[y]; put(ws, f'{c}{r}', f"=SUMIFS('E1a Fleet (roll)'!{L(5+CYEARS.index(y))}$7:{L(5+CYEARS.index(y))}$190,'E1a Fleet (roll)'!$A$7:$A$190,\"{key}\",'E1a Fleet (roll)'!$C$7:$C$190,{bi})", fmt=F_INT)
            cell_rows[(key, bi)] = r; r += 1
    label(ws, r, 'Total vehicles on the road', '000s', b=True)
    for y in CYEARS: put(ws, f'{CYCOL[y]}{r}', f'=SUM({CYCOL[y]}19:{CYCOL[y]}34)', fmt=F_INT, b=True).border = TOP
    tot_row = r; r += 1
    label(ws, r, '   share aged 7+', '%', i=True)
    for y in CYEARS: put(ws, f'{CYCOL[y]}{r}', f"=SUMIFS('E1a Fleet (roll)'!{CYCOL[y]}$7:{CYCOL[y]}$190,'E1a Fleet (roll)'!$C$7:$C$190,3)/{CYCOL[y]}{tot_row}", fmt=F_PCT, i=True)
    s7_row = r
    group(ws, 39, 'D. Claims-weighted composition: share of claims by body × age band  (model = fleet × R(age) × body factor; CCC-implied = TL mix ÷ TLF, normalised)')
    r = 40; mrows = {}
    for key, lab, *_ in BODIES:
        for bi, bl in enumerate(BANDS):
            label(ws, r, f'Model: {lab} — {bl}', '%', indent=1 if bi else 0)
            for y in CYEARS:
                c = CYCOL[y]; cc = L(4 + 12 + CYEARS.index(y))   # claims-mass block on E1a starts at column P (16)
                put(ws, f'{c}{r}', f"=SUMIFS('E1a Fleet (roll)'!{cc}$7:{cc}$190,'E1a Fleet (roll)'!$A$7:$A$190,\"{key}\",'E1a Fleet (roll)'!$C$7:$C$190,{bi})/SUM('E1a Fleet (roll)'!{cc}$7:{cc}$190)", fmt=F_PCT)
            mrows[(key, bi)] = r; r += 1
    crows = {}; cccname = {'Car': 'Car', 'SUV': 'Utility Vehicle', 'Pickup': 'Pickup', 'Van': 'Van'}
    for key, lab, *_ in BODIES:
        for bi, bl in enumerate(BANDS):
            label(ws, r, f'CCC-implied: {lab} — {bl}', '%', indent=1 if bi else 0, note='D CCC column K (VERIFIED cells, derived ratio); 2020–2025 only' if (key == 'Car' and bi == 0) else '')
            for y in CYEARS:
                if 2020 <= y <= 2025:
                    c = CYCOL[y]; put(ws, f'{c}{r}', f"=SUMIFS('D CCC'!$K${ctx['ccc_r0']}:$K${ctx['ccc_r1']},'D CCC'!$B${ctx['ccc_r0']}:$B${ctx['ccc_r1']},{c}$3,'D CCC'!$C${ctx['ccc_r0']}:$C${ctx['ccc_r1']},\"{cccname[key]}\",'D CCC'!$D${ctx['ccc_r0']}:$D${ctx['ccc_r1']},{bi})", 'link', F_PCT)
            crows[(key, bi)] = r; r += 1
    r += 1
    for key, lab, *_ in BODIES:
        label(ws, r, f'Gap, body total: {lab} (model − CCC)', 'pp', i=True)
        for y in range(2020, 2026):
            c = CYCOL[y]; put(ws, f'{c}{r}', f"=SUM({c}{mrows[(key,0)]}:{c}{mrows[(key,3)]})-SUM({c}{crows[(key,0)]}:{c}{crows[(key,3)]})", fmt=F_PCT, i=True)
        r += 1
    label(ws, r, 'Largest single-cell gap, |model − CCC|', 'pp', b=True)
    for y in range(2020, 2026):
        c = CYCOL[y]; terms = ','.join(f'ABS({c}{mrows[k]}-{c}{crows[k]})' for k in mrows); put(ws, f'{c}{r}', f'=MAX({terms})', fmt=F_PCT, b=True)
    gap_row = r; ctx['e1'] = dict(cell_rows=cell_rows, mrows=mrows, crows=crows, tot_row=tot_row, s7_row=s7_row, gap_row=gap_row)
    group(ws, 80, 'E. Checks')
    label(ws, 81, 'Total vehicles on the road, 2024 vs Experian anchor', '000s', note='Anchor in Inputs; the roll is fitted to it via m(2024), so this is a reproduction check, not validation')
    put(ws, 'D81', f'={CYCOL[2024]}{tot_row}', fmt=F_INT); put(ws, 'E81', '=$D$95', 'link', F_INT); put(ws, 'F81', '=D81/E81-1', fmt=F_PCT); put(ws, 'G81', '=IF(ABS(F81)<0.02,"PASS","FAIL")', b=True)
    label(ws, 82, 'Share aged 7+, 2024 vs S&P anchor', '%'); put(ws, 'D82', f'={CYCOL[2024]}{s7_row}', fmt=F_PCT); put(ws, 'E82', '=$D$96', 'link', F_PCT); put(ws, 'F82', '=D82-E82', fmt=F_PCT); put(ws, 'G82', '=IF(ABS(F82)<0.02,"PASS","FAIL")', b=True)
    label(ws, 83, 'Largest cell gap vs CCC claim mix, 2020–2025 (out of sample except body factors at 2025)', 'pp', note='PASS if every cell within 3.5 points and 2025 within 2.5; see docs/source_trace_2026-10-01/FLEET_VS_CCC.md')
    put(ws, 'D83', f'=MAX({CYCOL[2020]}{gap_row}:{CYCOL[2025]}{gap_row})', fmt=F_PCT); put(ws, 'G83', '=IF(D83<0.035,"PASS","FAIL")', b=True)
    label(ws, 84, 'Largest body-total gap, 2020–2024 (body factors fitted on 2025 only)', 'pp')
    terms = ','.join(f'ABS({CYCOL[y]}{rr})' for y in range(2020, 2025) for rr in range(gap_row - 4, gap_row)); put(ws, 'D84', f'=MAX({terms})', fmt=F_PCT); put(ws, 'G84', '=IF(D84<0.015,"PASS","FAIL")', b=True)
    put(ws, 'B86', 'Feeds →  E2 Claims & Totals (vehicles by band × body, rows 19–34, mapped to fiscal quarters)', 'note')
    section(ws, 88, 'Inputs  (blue = typed value; every number here carries a label and a source)', ['Value', 'Label'])
    inputs = [(89, 'k_cars(2013): survival stretch, cars', 1.064, 'FITTED', 'docs/AGE_CURVES.md §2.3 — reproduces IHS 2013 census of cars by age (ORNL Table 3.11)'),
              (90, 'k_cars(2013)', 1.064, 'FITTED', 'same (duplicate row kept for formula anchoring)'),
              (91, 'k_light trucks(2013)', 0.921, 'FITTED', 'docs/AGE_CURVES.md §2.3 — IHS 2013 census of trucks (ORNL Table 3.12)'),
              (92, 'm(2024): drift multiplier', 1.194, 'FITTED', 'docs/AGE_CURVES.md §2.4 — fitted to the two 2024 anchors below; anchors themselves need sourcing'),
              (93, 'exposure(age 0): fraction of a claim-year for current-year vehicles', 0.5, 'ASSUMED', 'data/csv/age_curves.csv header; looks low versus CCC age-0 claim share (5.5% vs 4.0%)'),
              (94, 'Claims decay per year beyond age 6 (R(a) = exposure × e^(−decay·max(a−6,0)))', 0.09027, 'FITTED', 'scripts/age_curves.py — fitted jointly with P(a) to eight CCC 2024 statistics'),
              (95, 'Vehicles in operation, 2024 (thousands)', 292000, 'UNVERIFIED', 'Experian figure on disk per PROVENANCE (file to be cited); the recalled S&P 289M is retired'),
              (96, 'Share aged 7+, 2024', 0.66, 'UNVERIFIED', 'recalled S&P Global Mobility release; not on disk'),
              (97, 'Body factor: Car (claims per vehicle vs common curve)', 1.110, 'CALIBRATED', 'scripts/fleet_vs_ccc_backtest.py — fitted to 2025 CCC cells only; 2020–24 are the test'),
              (98, 'Body factor: Utility vehicle (SUV)', 0.917, 'CALIBRATED', 'same'), (99, 'Body factor: Pickup', 1.028, 'CALIBRATED', 'same'), (100, 'Body factor: Van / minivan', 0.923, 'CALIBRATED', 'same')]
    for row, lab, val, kind, src in inputs:
        label(ws, row, lab, note=src); put(ws, f'D{row}', val, 'input', F_X if isinstance(val, float) and val < 10 else F_INT); put(ws, f'E{row}', kind, 'note')
    ws.freeze_panes = 'D6'
    # ---------------- E1a roll
    wr = wb.create_sheet('E1a Fleet (roll)'); tab_color(wr, '7030A0'); wr.sheet_view.showGridLines = False; wr.sheet_view.zoomScale = 85
    title(wr, 'E1a Fleet (roll) — single-age roll behind E1, by body (thousands) and claims mass', 'Fleet cell = Births(CY − age, body) × S_body(age ÷ k_body(CY)), linear interpolation of the EPA schedule, zero beyond its last age. Claims mass = fleet × R(age) × body factor. Formulas only; collapse this tab in normal use.')
    for c, w in (('A', 9), ('B', 6), ('C', 6), ('D', 9)): wr.column_dimensions[c].width = w
    for i in range(5, 27): wr.column_dimensions[L(i)].width = 11
    put(wr, 'D3', 'CY →', 'note'); put(wr, 'D4', 'k cars', 'note'); put(wr, 'D5', 'k light trucks', 'note'); put(wr, 'O3', 'claims mass →', 'note')
    for i, y in enumerate(CYEARS):
        c = L(5 + i); put(wr, f'{c}3', y, 'note'); put(wr, f'{c}4', f"='E1 Fleet'!{CYCOL[y]}15", 'link', F_X); put(wr, f'{c}5', f"='E1 Fleet'!{CYCOL[y]}16", 'link', F_X)
        put(wr, f'{c}6', f'Fleet CY{y}', 'label', b=True); put(wr, f'{L(16 + i)}6', f'Claims CY{y}', 'label', b=True); put(wr, f'{L(16+i)}3', y, 'note')
    for c, h in (('A', 'Body'), ('B', 'Age'), ('C', 'Band'), ('D', 'R(age)')): put(wr, f'{c}6', h, 'label', b=True)
    r = 7; factor_row = {'Car': 97, 'SUV': 98, 'Pickup': 99, 'Van': 100}
    for key, lab, bc, scol, krow in BODIES:
        for a in AGES:
            wr[f'A{r}'] = key; wr[f'B{r}'] = a; wr[f'C{r}'] = band(a)
            put(wr, f'D{r}', f"=IF($B{r}=0,'E1 Fleet'!$D$93,1)*EXP(-'E1 Fleet'!$D$94*MAX($B{r}-6,0))", fmt='0.000')
            for i, y in enumerate(CYEARS):
                c = L(5 + i); x = f'($B{r}/{c}${krow})'; S = SR(scol)
                f = (f"=IFERROR(INDEX('D Fleet'!${bc}${b0}:${bc}${b1},MATCH({c}$3-$B{r},{BY},0)),0)"
                     f"*IFERROR(INDEX({S},INT({x})+1)+({x}-INT({x}))*(INDEX({S},INT({x})+2)-INDEX({S},INT({x})+1)),0)")
                put(wr, f'{c}{r}', f, fmt=F_INT)
                put(wr, f'{L(16+i)}{r}', f"={c}{r}*$D{r}*'E1 Fleet'!$D${factor_row[key]}", fmt=F_INT)
            r += 1
    wr.freeze_panes = 'E7'
