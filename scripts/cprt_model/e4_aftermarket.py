"""E4 Aftermarket (thesis B): sourcing shift -> repair-bill saving -> fewer total losses; recycled displacement -> lower bids -> prices."""
from .common import *
def build(wb, ctx):
    ws = wb.create_sheet('E4 Aftermarket'); tab_color(ws, '7030A0'); setup(ws)
    std_header(ws, 'Bill saving = e × [Σ_s (q_s + Δq_s) p_s ÷ Σ_s q_s p_s − 1];  Δ total-loss units = η × bill saving;  Δ price scaled from the engine\'s endpoint.  Every coefficient here is ASSUMED or ENGINE-derived.  Appendix A, Eq. 6.', 'E4 Aftermarket — repair-parts substitution to units and prices (thesis B)')
    section(ws, 5, 'A. Sourcing path: cumulative shift of eligible-basket quantity into aftermarket (points of the basket)', quarter_labels())
    label(ws, 7, 'OEM → aftermarket', 'pts', note='ASSUMED: 1 pt per quarter through FY27 (1 Oct audit path), held in FY28; CCC aftermarket dollar share rose 1.7 pts over 2024–25 on a whole-bill denominator')
    label(ws, 8, 'Recycled → aftermarket', 'pts', note='ASSUMED: 0.375 pt per quarter; recycled dollar share actually fell only 0.2 pt 2024–25 (CCC)')
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]; nq = 0 if fy == 2026 else (q if fy == 2027 else 4)
        hold = '*$D$56' if fy == 2028 else ''
        put(ws, f'{c}7', f'=$D$54*{nq}{hold}', fmt='0.000'); put(ws, f'{c}8', f'=$D$55*{nq}{hold}', fmt='0.0000')
    group(ws, 10, 'B. Repair-cost channel')
    label(ws, 11, 'Eligible-basket cost index, before the shift  (Σ q_s p_s)', 'x'); label(ws, 12, 'Eligible-basket cost index, after the shift', 'x')
    label(ws, 13, '   basket relative cost change', '%', i=True); label(ws, 14, 'Complete repair-bill change  (× eligible share e)', '%', b=True)
    label(ws, 15, 'Change in total-loss units, relative  (η × bill change)', '%', b=True, note='η is the engine\'s implied selection response per 1% of bill: FY unit delta ÷ repair change in the larger-shift case (ENGINE-derived, Inputs row 61)')
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        put(ws, f'{c}11', '=$D$46*$D$49+$D$47*$D$50+$D$48*$D$51', fmt='0.0000')
        put(ws, f'{c}12', f'=($D$46-{c}7)*$D$49+($D$47+{c}7+{c}8)*$D$50+($D$48-{c}8)*$D$51', fmt='0.0000')
        put(ws, f'{c}13', f'={c}12/{c}11-1', fmt=F_PCT2, i=True); put(ws, f'{c}14', f'=$D$45*{c}13', fmt=F_PCT2, b=True); put(ws, f'{c}15', f'=$D$61*{c}14', fmt=F_PCT2, b=True)
    group(ws, 17, 'C. Donor-bid channel (recycled displacement → dismantler bids → marginal auction price)')
    label(ws, 18, 'Recycled quantity displaced, relative to the recycled share', '%'); label(ws, 19, 'Recycler-only bid change  (−τ × κ × x × displacement; reduced form)', '%', i=True, note='Intuition row only; the engine also includes rebuilder benefit and donor scarcity')
    label(ws, 20, 'Engine net auction-price change at the 5.5-point endpoint (fixed selection)', '%', note='ENGINE: D Engine CCC scenario summary, ccc_larger_shift auction_price_change_at_fixed_selection')
    label(ws, 21, 'Auction-price change, scaled to the quarter\'s displacement', '%', b=True, note='ASSUMED linear scaling from the endpoint')
    e0, e1 = ctx['eng_ccc_ss']
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        put(ws, f'{c}18', f'={c}8/$D$48', fmt=F_PCT2); put(ws, f'{c}19', f'=-$D$52*$D$53*$D$57*{c}18', fmt=F_PCT2, i=True)
        put(ws, f'{c}20', f"=SUMIFS('D Engine'!$D${e0}:$D${e1},'D Engine'!$B${e0}:$B${e1},\"ccc_larger_shift\")", 'engine', F_PCT2)
        put(ws, f'{c}21', f'={c}20*{c}18/($D$58/$D$48)', fmt=F_PCT2, b=True)
    group(ws, 23, 'D. Parity with the Python engine (1 Oct package): aftermarket added to the saved reference, FY27 quarters')
    q0, q1 = ctx['eng_q']
    label(ws, 24, 'Engine service revenue, reference (mask 10 = premium recovery + fleet mix)', '$M'); label(ws, 25, 'Engine service revenue, reference + aftermarket (mask 14)', '$M'); label(ws, 26, 'Engine Δ service revenue from aftermarket', '$M', b=True)
    for fy, q in QUARTERS:
        if fy == 2027:
            c = QCOL[(fy, q)]; per = f'FY{fy}Q{q}'
            put(ws, f'{c}24', f"=SUMIFS('D Engine'!$E${q0}:$E${q1},'D Engine'!$B${q0}:$B${q1},10,'D Engine'!$D${q0}:$D${q1},\"{per}\")", 'engine', F_MONEY)
            put(ws, f'{c}25', f"=SUMIFS('D Engine'!$E${q0}:$E${q1},'D Engine'!$B${q0}:$B${q1},14,'D Engine'!$D${q0}:$D${q1},\"{per}\")", 'engine', F_MONEY)
            put(ws, f'{c}26', f'={c}25-{c}24', fmt=F_MONEY, b=True)
    put(ws, f'{ACOL[2027]}26', f'=SUM({QCOL[(2027,1)]}26:{QCOL[(2027,4)]}26)', fmt=F_MONEY, b=True)
    label(ws, 28, 'Countercase to keep visible: zero recycled displacement (set Inputs row 55 to 0) removes the price channel and most of the paired downside; OEM-only displacement raised RPU slightly in the engine', i=True)
    group(ws, 38, 'Outputs → other tabs (thesis B effects, always computed; Scenarios switches them on or off)')
    label(ws, E4_DU_ROW, 'Δ total-loss units, relative  (→ E2 TLF cells, → Scenarios)', '%', b=True); label(ws, E4_DP_ROW, 'Δ auction price, relative  (→ Scenarios ASP)', '%', b=True)
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]; put(ws, f'{c}{E4_DU_ROW}', f'={c}15', fmt=F_PCT2, b=True); put(ws, f'{c}{E4_DP_ROW}', f'={c}21', fmt=F_PCT2, b=True)
    section(ws, 44, 'Inputs', ['Value', 'Label'])
    items = [(45, 'e: eligible-parts share of the repair bill', 0.40, 'ASSUMED', 'CCC all-parts spend 36–44% by age is the nearest anchor; not the substitutable share'),
             (46, 'q_OEM: OEM share of the eligible basket', 0.65, 'ASSUMED', 'CCC 2025 whole-bill dollar shares: AM 22.7%, recycled 10.5% (different denominator)'), (47, 'q_AM: aftermarket share', 0.25, 'ASSUMED', ''), (48, 'q_rec: recycled share', 0.10, 'ASSUMED', ''),
             (49, 'p_OEM: relative price', 1.00, 'ASSUMED', ''), (50, 'p_AM: relative price', 0.50, 'ASSUMED', 'Mitchell 2016 matched discounts were 23–30% (0.70–0.77); 0.50 is the stress'), (51, 'p_rec: relative price', 0.60, 'ASSUMED', 'No matched national dataset'),
             (52, 'x: donor contribution exposed to collision-part substitution', 0.25, 'ASSUMED', 'No supporting record (FORWARD_ASSUMPTIONS.md)'), (53, 'κ: contribution-to-hammer bid ratio', 1.5, 'ASSUMED', 'Sturgeon 2018 margins make the scale interpretable, not the value'),
             (54, 'OEM → aftermarket shift per quarter through FY27 (points)', 0.01, 'ASSUMED', 'model/thesis_audit_2026-10-01/assumptions.json'), (55, 'Recycled → aftermarket shift per quarter (points)', 0.00375, 'ASSUMED', 'same'), (56, 'Hold FY27 endpoint through FY28 (1) or revert to zero (0)', 1, 'toggle', ''),
             (57, 'τ: recycler bid transmission to the marginal price', 0.5, 'ASSUMED', 'The 10% case removes most of the price effect (AUDIT.md)'), (58, 'Endpoint recycled displacement used by the engine (points)', 0.015, 'ASSUMED', 'ccc_larger_shift case')]
    for row, lab, val, lbl, src in items:
        kind = 'toggle' if lbl == 'toggle' else 'input'; label(ws, row, lab, note=src); put(ws, f'D{row}', val, kind, '0.000' if isinstance(val, float) else '0'); put(ws, f'E{row}', lbl if lbl != 'toggle' else 'TOGGLE', 'note')
    label(ws, 61, 'η: selection response, Δ units per unit of bill change (ENGINE-derived: ccc_larger_shift unit delta ÷ repair change)', note='D Engine CCC scenario summary; the engine\'s derivative is calibrated to levels only (AUDIT.md priority 1)')
    put(ws, 'D61', f"=SUMIFS('D Engine'!$F${e0}:$F${e1},'D Engine'!$B${e0}:$B${e1},\"ccc_larger_shift\")/SUMIFS('D Engine'!$C${e0}:$C${e1},'D Engine'!$B${e0}:$B${e1},\"ccc_larger_shift\")", 'engine', '0.000'); put(ws, 'E61', 'ENGINE', 'note')
    ws.freeze_panes = 'D6'
