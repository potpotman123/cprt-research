"""E3 Carriers (thesis A): carrier weights x Copart allocation paths -> aggregate share; seller terms."""
from .common import *
def build(wb, ctx):
    ws = wb.create_sheet('E3 Carriers'); tab_color(ws, '7030A0'); setup(ws)
    std_header(ws, 'Copart share S(q) = Σ_i w_i × a_i(q);  units chain uses S(q) ÷ S(q−4).  Known Progressive runoff is always on; thesis A adds events and drift via toggles.  Appendix A, Eq. 7.', 'E3 Carriers — carrier weights, Copart allocation paths and seller terms (thesis A)')
    section(ws, 5, 'A. Carrier weights: share of the insured total-loss pool (frozen at FQ4 FY26)', quarter_labels())
    names = ctx['carriers']; w0, w1 = ctx['carrier_w']; a0, a1 = ctx['carrier_a']
    PCOL = {(2026, 1): 'C', (2026, 2): 'D', (2026, 3): 'E', (2026, 4): 'F', (2027, 1): 'G', (2027, 2): 'H', (2027, 3): 'I', (2027, 4): 'J'}   # D Carriers period columns
    for i, n in enumerate(names):
        r = 6 + i; label(ws, r, n, 'share', note='D Carriers (UNVERIFIED premium-share proxy; frozen per carrier test 28 Sep)' if i == 0 else '')
        for fy, q in QUARTERS: put(ws, f'{QCOL[(fy,q)]}{r}', f"='D Carriers'!$F${w0+i}", 'link', '0.0000')
    label(ws, 16, '   check: weights sum to one', '', i=True)
    for fy, q in QUARTERS: put(ws, f'{QCOL[(fy,q)]}16', f'=SUM({QCOL[(fy,q)]}6:{QCOL[(fy,q)]}15)', fmt='0.0000', i=True)
    group(ws, 18, 'B. Copart allocation by carrier — base: FY26 inherited reconstruction; from FQ1 FY27 Progressive follows its runoff path and every other carrier is frozen at FQ4 FY26')
    toggle_row = {'GEICO': 66, 'State Farm': 67, 'Other (Erie, AAA, AmFam, regionals)': 68}
    for i, n in enumerate(names):
        r = 19 + i; label(ws, r, n, 'share', note='Progressive: inherited runoff (FITTED to the FQ4 FY26 print), then flat' if n == 'Progressive' else '')
        for fy, q in QUARTERS:
            c = QCOL[(fy, q)]; src = PCOL.get((fy, q), 'J'); inherited = f"'D Carriers'!${src}${a0+i}"; frozen = f"'D Carriers'!$F${a0+i}"
            if fy == 2026 or n == 'Progressive': f = f'={inherited}'
            else: f = f'={frozen}'
            put(ws, f'{c}{r}', f, 'link', '0.000')
    group(ws, 30, 'C. Allocation with thesis-A additions — events switch a carrier to its inherited event path; drift subtracts points per quarter from FQ1 FY27')
    for i, n in enumerate(names):
        r = 31 + i; label(ws, r, n, 'share')
        for fy, q in QUARTERS:
            c = QCOL[(fy, q)]; src = PCOL.get((fy, q), 'J'); inherited = f"'D Carriers'!${src}${a0+i}"; base = f'{c}{19+i}'
            nq = max(0, (fy - 2027) * 4 + q) if fy >= 2027 else 0
            if fy == 2026: f = f'={base}'
            elif n == 'Progressive': f = f'=MAX(0,{base}-$D$70*{nq}*$D$64)'
            elif n in toggle_row: f = f'=MAX(0,IF($D${toggle_row[n]}*$D$64=1,{inherited},{base})-$D$69*{nq}*$D$64)'
            else: f = f'=MAX(0,{base}-$D$69*{nq}*$D$64)'
            put(ws, f'{c}{r}', f, fmt='0.000')
    group(ws, 42, 'D. Aggregate Copart share of the insured total-loss pool')
    label(ws, 43, 'Share, base (known runoff only)', '%', b=True); label(ws, 44, 'Share, with thesis-A additions', '%', b=True)
    label(ws, 45, 'Reference: Copart share of duopoly listed US inventory, 4 clean nights 11–27 Sep 2026', '%', i=True, note='MEASURED, data/csv/duopoly_daily.csv usable=1; listed inventory, not assignments. Mean 57.2%, range 56.8–57.6%')
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        put(ws, f'{c}43', f'=SUMPRODUCT({c}6:{c}15,{c}19:{c}28)', fmt=F_PCT, b=True); put(ws, f'{c}44', f'=SUMPRODUCT({c}6:{c}15,{c}31:{c}40)', fmt=F_PCT, b=True)
    put(ws, f'{QCOL[(2026,4)]}45', 0.572, 'input', F_PCT)
    annual_avg(ws, 43); annual_avg(ws, 44)
    label(ws, E3_SR_BASE_ROW, 'Share ratio to same quarter a year earlier, base  (→ Scenarios)', 'x', b=True)
    label(ws, E3_SR_A_ROW, 'Share ratio to same quarter a year earlier, thesis A  (→ Scenarios)', 'x', b=True)
    for fy, q in QUARTERS:
        if fy > 2026:
            c, p = QCOL[(fy, q)], QCOL[(fy - 1, q)]
            put(ws, f'{c}{E3_SR_BASE_ROW}', f'={c}43/{p}43', fmt='0.0000', b=True); put(ws, f'{c}{E3_SR_A_ROW}', f'={c}44/{p}43', fmt='0.0000', b=True)
    group(ws, 51, 'E. Seller terms (commission as a share of the vehicle\'s sale price)')
    label(ws, 52, 'Base seller commission rate', '%', note='UNVERIFIED analyst assumption (Barclays 25 Aug 2026 Figure 1 uses 4%); not a contract term')
    label(ws, 53, 'Concession on a contested account (share of the commission)', '%', note='UNVERIFIED (Barclays illustration, 20%)')
    label(ws, 54, 'Share of Copart insurance volume on concession terms (thesis A)', '%', note='ASSUMED; 0 in base')
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        put(ws, f'{c}52', '=$D$71', 'link', F_PCT); put(ws, f'{c}53', '=$D$72', 'link', F_PCT); put(ws, f'{c}54', f'=IF({fy}>=2027,$D$73*$D$64,0)', fmt=F_PCT)
    label(ws, E3_SELLER_BASE_ROW, 'Effective seller commission rate, base  (→ E5)', '%', b=True); label(ws, E3_SELLER_A_ROW, 'Effective seller commission rate, thesis A  (→ E5)', '%', b=True)
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]; put(ws, f'{c}{E3_SELLER_BASE_ROW}', f'={c}52', fmt=F_PCT2, b=True); put(ws, f'{c}{E3_SELLER_A_ROW}', f'={c}52*(1-{c}53*{c}54)', fmt=F_PCT2, b=True)
    put(ws, 'B58', 'Feeds →  Scenarios (share ratios rows 48–49); E5 Prices & Fees (seller rates rows 55–56)', 'note')
    section(ws, 63, 'Inputs and toggles', ['Value', 'Label'])
    items = [(64, 'Thesis A master toggle (1 = additions on; Scenarios reads both states, so leave at 1)', 1, 'toggle', 'TOGGLE', ''),
             (66, 'GEICO allocation event (inherited: allocation 0.83 → 0.90, a gain for Copart)', 0, 'toggle', 'ASSUMED', 'Share build U5: 60% judgmental probability; off by default in the bear variant'),
             (67, 'State Farm adverse event (inherited: 0.50 → 0.4775 by FQ4 FY27)', 1, 'toggle', 'ASSUMED', 'Share build U7: 45% judgmental; shown as realised case, not probability-weighted'),
             (68, 'Other-carrier drift event (inherited: 0.50 → 0.4775)', 1, 'toggle', 'ASSUMED', 'Share build Events row 15; regional anecdote on a 24% bucket'),
             (69, 'Additional allocation drift, non-Progressive carriers (points per quarter from FQ1 FY27)', 0.0, 'input', 'ASSUMED', 'No evidence; 0 by default. Use only as a labelled stress'),
             (70, 'Additional Progressive decline (points per quarter from FQ1 FY27)', 0.0, 'input', 'ASSUMED', 'The inherited path already reaches 5%'),
             (71, 'Base seller commission rate', 0.04, 'input', 'UNVERIFIED', 'Barclays 25 Aug 2026 Figure 1 (licensed, local)'),
             (72, 'Concession, share of commission', 0.20, 'input', 'UNVERIFIED', 'Barclays 25 Aug 2026 Figure 1'),
             (73, 'Share of volume on concession terms when thesis A is on', 0.0, 'input', 'ASSUMED', 'Set in Scenarios; 0 means no retained-account repricing')]
    for row, lab, val, kind, lbl, src in items:
        label(ws, row, lab, note=src); put(ws, f'D{row}', val, kind, '0.000' if isinstance(val, float) else '0'); put(ws, f'E{row}', lbl, 'note')
    ws.freeze_panes = 'D6'
