"""E2 Claims & Totals: claims mass by cell (from E1a via fiscal-quarter weights) x total-loss frequency (CCC 2025 calibrated) -> pool."""
from .common import *
from .e1_fleet import BODIES, BANDS
CYW = list(range(2023, 2029))   # calendar years carrying weight for FQ1 FY26 .. FQ4 FY28
CLAIM_COL = {y: L(16 + CYEARS.index(y)) for y in CYEARS}   # E1a claims-mass columns P..Y
def build(wb, ctx):
    ws = wb.create_sheet('E2 Claims & Totals'); tab_color(ws, '7030A0'); setup(ws)
    std_header(ws, 'Claims(cell, q) = Σ_CY w(q, CY) × Fleet(cell, CY) × R(age) × body factor;  Totals(cell, q) = Claims × TLF(cell);  Pool = Σ cells × routing.  Appendix A, Eq. 3–4.', 'E2 Claims & Totals — insured claims and total losses by body × age band, by fiscal quarter')
    section(ws, 5, 'A. Fiscal-quarter fleet interpolation weights by calendar year', quarter_labels())
    label(ws, 6, 'Rule: average over the quarter\'s three month-midpoints of a linear interpolation between year-end fleets', note='MEASURED by rule (scripts/cprt_model/common.py cy_weights); reproduces linked_service_revenue inputs.json periods[].weights', i=True)
    wrow = {}
    for i, y in enumerate(CYW):
        r = 7 + i; wrow[y] = r; label(ws, r, f'   weight on CY{y} year-end fleet', 'share', indent=1)
        for fy, q in QUARTERS: put(ws, f'{QCOL[(fy,q)]}{r}', round(cy_weights(fy, q).get(y, 0.0), 6), 'formula', '0.0000')
    label(ws, 13, '   check: weights sum to one', '', i=True)
    for fy, q in QUARTERS: put(ws, f'{QCOL[(fy,q)]}13', f'=SUM({QCOL[(fy,q)]}7:{QCOL[(fy,q)]}12)', fmt='0.0000', i=True)
    # helper block: claims mass by cell and calendar year (from E1a)
    H0 = 86; group(ws, H0 - 1, 'Helper: claims mass by cell and calendar year (fleet × R(age) × body factor, from E1a; thousands-equivalent)')
    for j, y in enumerate(CYW): put(ws, f'{L(4+j)}{H0-1}', f'CY{y}', 'label', b=True)
    hrow = {}; r = H0
    for key, lab, *_ in BODIES:
        for bi, bl in enumerate(BANDS):
            label(ws, r, f'{lab} — {bl}', indent=1 if bi else 0)
            for j, y in enumerate(CYW):
                put(ws, f'{L(4+j)}{r}', f"=SUMIFS('E1a Fleet (roll)'!{CLAIM_COL[y]}$7:{CLAIM_COL[y]}$190,'E1a Fleet (roll)'!$A$7:$A$190,\"{key}\",'E1a Fleet (roll)'!$C$7:$C$190,{bi})", 'link', F_INT)
            hrow[(key, bi)] = r; r += 1
    # B. claims mass by cell by quarter
    group(ws, 15, 'B. Claims mass by body × age band (relative claims; thousands-equivalent) — composition from E1, level is an index')
    r = 16; crow = {}
    for key, lab, *_ in BODIES:
        for bi, bl in enumerate(BANDS):
            label(ws, r, f'{lab} — {bl}', 'index', indent=1 if bi else 0)
            for fy, q in QUARTERS:
                c = QCOL[(fy, q)]; terms = '+'.join(f'{c}${wrow[y]}*${L(4+j)}${hrow[(key,bi)]}' for j, y in enumerate(CYW))
                put(ws, f'{c}{r}', f'=({terms})*$D$80', fmt=F_INT)
            annual_sum(ws, r, F_INT); crow[(key, bi)] = r; r += 1
    label(ws, 32, 'Total claims mass (× claims multiplier)', 'index', b=True)
    for fy, q in QUARTERS: put(ws, f'{QCOL[(fy,q)]}32', f'=SUM({QCOL[(fy,q)]}16:{QCOL[(fy,q)]}31)', fmt=F_INT, b=True).border = TOP
    annual_sum(ws, 32, F_INT, b=True)
    label(ws, 33, '   y/y', '%', i=True)
    for fy, q in QUARTERS:
        if fy > 2026: put(ws, f'{QCOL[(fy,q)]}33', f'={QCOL[(fy,q)]}32/{QCOL[(fy-1,q)]}32-1', fmt=F_PCT, i=True)
    for fy in (2027, 2028): put(ws, f'{ACOL[fy]}33', f'={ACOL[fy]}32/{ACOL[fy-1]}32-1', fmt=F_PCT, i=True)
    # C. TLF by cell
    group(ws, 35, 'C. Total-loss frequency by cell: CCC 2025 calibrated level (D Engine), held flat; the thesis-B shift is applied in Scenarios so it is never counted twice')
    c0, c1 = ctx['cal_rows']; cccname = {'Car': 'Car', 'SUV': 'Utility Vehicle', 'Pickup': 'Pickup', 'Van': 'Van'}
    r = 36; trow = {}
    for key, lab, *_ in BODIES:
        for bi, bl in enumerate(BANDS):
            label(ws, r, f'{lab} — {bl}', '%', indent=1 if bi else 0, note='D Engine calibration cells: calibrated_tlf (CALIBRATED to the 2025 CCC cell, VERIFIED source)' if (key == 'Car' and bi == 0) else '')
            for fy, q in QUARTERS:
                c = QCOL[(fy, q)]
                put(ws, f'{c}{r}', f"=SUMIFS('D Engine'!$F${c0}:$F${c1},'D Engine'!$B${c0}:$B${c1},\"{cccname[key]}\",'D Engine'!$C${c0}:$C${c1},{bi})", fmt=F_PCT)
            trow[(key, bi)] = r; r += 1
    # D. total losses
    group(ws, 54, 'D. Total losses by cell = claims mass × TLF')
    r = 55
    for key, lab, *_ in BODIES:
        for bi, bl in enumerate(BANDS):
            label(ws, r, f'{lab} — {bl}', 'index', indent=1 if bi else 0)
            for fy, q in QUARTERS:
                c = QCOL[(fy, q)]; put(ws, f'{c}{r}', f'={c}{crow[(key,bi)]}*{c}{trow[(key,bi)]}', fmt=F_INT)
            annual_sum(ws, r, F_INT); r += 1
    label(ws, 71, 'Total-loss pool reaching the insurance auction channel (× routing × (1 + extra CAT))', 'index', b=True)
    for fy, q in QUARTERS: put(ws, f'{QCOL[(fy,q)]}71', f'=SUM({QCOL[(fy,q)]}55:{QCOL[(fy,q)]}70)*$D$82*(1+$D$83)', fmt=F_INT, b=True).border = TOP
    annual_sum(ws, 71, F_INT, b=True)
    label(ws, 72, '   y/y', '%', i=True)
    for fy, q in QUARTERS:
        if fy > 2026: put(ws, f'{QCOL[(fy,q)]}72', f'={QCOL[(fy,q)]}71/{QCOL[(fy-1,q)]}71-1', fmt=F_PCT, i=True)
    for fy in (2027, 2028): put(ws, f'{ACOL[fy]}72', f'={ACOL[fy]}71/{ACOL[fy-1]}71-1', fmt=F_PCT, i=True)
    label(ws, 73, '   aggregate total-loss frequency (pool ÷ claims)', '%', i=True, note='Check: CCC-cell-weighted 2025 level is 23.1% (model/ccc_age_body annual_derived.csv); CCC headline all-loss TLF 2025 is 23.9% (different population)')
    for fy, q in QUARTERS: put(ws, f'{QCOL[(fy,q)]}73', f'={QCOL[(fy,q)]}71/{QCOL[(fy,q)]}32/$D$82/(1+$D$83)', fmt=F_PCT, i=True)
    for fy in ACOL: put(ws, f'{ACOL[fy]}73', f'={ACOL[fy]}71/{ACOL[fy]}32/$D$82/(1+$D$83)', fmt=F_PCT, i=True)
    label(ws, E2_POOL_RATIO_ROW, 'Pool ratio to the same quarter a year earlier  (→ Scenarios: units chain)', 'x', b=True)
    for fy, q in QUARTERS:
        if fy > 2026: put(ws, f'{QCOL[(fy,q)]}{E2_POOL_RATIO_ROW}', f'={QCOL[(fy,q)]}71/{QCOL[(fy-1,q)]}71', fmt='0.0000', b=True)
    put(ws, 'B77', 'Feeds →  Scenarios (pool ratio, row 75); E5 (aggregate TLF, diagnostic only)', 'note')
    section(ws, 79, 'Inputs', ['Value', 'Label'])
    for row, lab, val, kind, src in [(80, 'Claims multiplier (relative combined claims propensity)', 1.0, 'ASSUMED', 'Neutral default; the 0.98 stress has no empirical anchor (driver_register.json)'),
                                      (81, 'Paired repairable non-filing term (deductible shift)', 0.0, 'ASSUMED', 'Placeholder; CCC deductible-share series could bound it. Not yet wired'),
                                      (82, 'Routing fraction of total losses to the insurance auction channel', 1.0, 'ASSUMED', 'Convention; dismantlers may buy directly from insurers (10-K)'),
                                      (83, 'Extra catastrophe unit fraction', 0.0, 'ASSUMED', 'Convention; FY25 hurricane units handled in history')]:
        label(ws, row, lab, note=src); put(ws, f'D{row}', val, 'input', '0.000'); put(ws, f'E{row}', kind, 'note')
    ws.freeze_panes = 'D6'
