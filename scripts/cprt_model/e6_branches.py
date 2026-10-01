"""E6 Other Branches: US non-insurance service, international service, purchased vehicles, ACV gate."""
from .common import *
def build(wb, ctx):
    ws = wb.create_sheet('E6 Other Branches'); tab_color(ws, '7030A0'); setup(ws)
    std_header(ws, 'Each branch = FY26 reported dollars × explicit growth inputs. International RPU +3.5% is the FQ4 FY26 disclosure continued; everything else is flat unless an input says otherwise.', 'E6 Other Branches — US non-insurance, international, purchased vehicles, ACV')
    g = ctx['geo_rows']; section(ws, 5, 'A. US non-insurance service revenue (dealer, BluCar, Copart Direct consignment fees)', quarter_labels())
    label(ws, 6, 'US service revenue (8-K)', '$M'); label(ws, 7, 'Non-insurance share of US service dollars  (1 − insurance share)', '%'); label(ws, 8, 'US non-insurance service revenue', '$M', b=True, note='FY26 = residual of the ledger split (ASSUMED 10%); FY27+ grows at the input rate'); label(ws, 9, '   y/y', '%', i=True)
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        if fy == 2026:
            put(ws, f'{c}6', f"='D Reported'!$D${g[(2026,q)]}", 'link', F_MONEY); put(ws, f'{c}7', "=1-'E5 Prices & Fees'!$D$39", 'link', F_PCT); put(ws, f'{c}8', f'={c}6*{c}7', fmt=F_MONEY, b=True)
        else: put(ws, f'{c}8', f'={QCOL[(fy-1,q)]}8*(1+$D$30)', fmt=F_MONEY, b=True); put(ws, f'{c}9', f'={c}8/{QCOL[(fy-1,q)]}8-1', fmt=F_PCT, i=True)
    annual_sum(ws, 8, b=True)
    group(ws, 11, 'B. International service revenue')
    label(ws, 12, 'International service revenue', '$M', b=True, note='FY26 VERIFIED (8-K); FY27+ = prior year × (1 + unit growth) × (1 + RPU growth)'); label(ws, 13, '   y/y', '%', i=True)
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        if fy == 2026: put(ws, f'{c}12', f"='D Reported'!$E${g[(2026,q)]}", 'link', F_MONEY, b=True)
        else: put(ws, f'{c}12', f'={QCOL[(fy-1,q)]}12*(1+$D$31*$D$33)*(1+$D$32*$D$33)', fmt=F_MONEY, b=True); put(ws, f'{c}13', f'={c}12/{QCOL[(fy-1,q)]}12-1', fmt=F_PCT, i=True)
    annual_sum(ws, 12, b=True)
    group(ws, 15, 'C. Purchased-vehicle revenue (Copart owns the car; comparison overlay, not legacy service)')
    label(ws, 16, 'Purchased-vehicle revenue, US + international', '$M', b=True, note='FY26 VERIFIED (8-K); forward flat by default; JPM FY27 expects $721m (licensed benchmark)')
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        if fy == 2026: put(ws, f'{c}16', f"='D Reported'!$F${g[(2026,q)]}+'D Reported'!$G${g[(2026,q)]}", 'link', F_MONEY, b=True)
        else: put(ws, f'{c}16', f'={QCOL[(fy-1,q)]}16*(1+$D$34)', fmt=F_MONEY, b=True)
    annual_sum(ws, 16, b=True)
    group(ws, 18, 'D. ACV Auctions acquisition (gated; excluded by default so the perimeter matches the JPM ex-ACV benchmark)')
    label(ws, 19, 'Acquired service revenue recognised', '$M', b=True, note='UNKNOWN; tender documents on disk (raw/sec/acv) give timing, not revenue. Keep 0 unless classified')
    for fy, q in QUARTERS: put(ws, f'{QCOL[(fy,q)]}19', '=0*$D$35', fmt=F_MONEY, b=True)
    put(ws, 'B22', 'Feeds →  Scenarios (rows 8, 12, 16, 19)', 'note')
    section(ws, 29, 'Inputs', ['Value', 'Label'])
    items = [(30, 'US non-insurance service growth, y/y', 0.0, 'ASSUMED', 'Flat convention; FQ4 FY26 non-insurance units +0.2% with dealer +5.8%, BluCar +20%, Direct −11.7% (call)'),
             (31, 'International fee-unit growth, y/y', 0.116, 'ASSUMED', 'Derived FQ4 FY26: service +15.5% ÷ 1.035 − 1 (MEASURED by identity), continued as an assumption'),
             (32, 'International fee RPU growth, y/y', 0.035, 'ASSUMED', 'FQ4 FY26 disclosed +3.5% (VERIFIED), continued'), (33, 'International continuation toggle (1 = continue; 0 = flat)', 1, 'TOGGLE', 'Worth about $90m a year'),
             (34, 'Purchased-vehicle revenue growth, y/y', 0.0, 'ASSUMED', 'Flat convention'), (35, 'ACV included (1) or excluded (0)', 0, 'TOGGLE', 'Perimeter gate')]
    for row, lab, val, lbl, src in items:
        label(ws, row, lab, note=src); put(ws, f'D{row}', val, 'toggle' if lbl == 'TOGGLE' else 'input', '0.000' if isinstance(val, float) else '0'); put(ws, f'E{row}', lbl, 'note')
    ws.freeze_panes = 'D6'
