"""E4 Aftermarket (thesis B): sourcing shift -> repair-bill saving -> fewer total losses; recycled displacement -> lower bids -> prices."""
from .common import *
def build(wb, ctx):
    ws = wb.create_sheet('E4 Aftermarket'); tab_color(ws, '7030A0'); setup(ws)
    std_header(ws, 'Bill saving = e × [Σ_s (q_s + Δq_s) p_s ÷ Σ_s q_s p_s − 1];  Δ total-loss units = η × bill saving;  Δ price scaled from the engine\'s endpoint.  Every coefficient here is ASSUMED or ENGINE-derived.  Appendix A, Eq. 6.', 'E4 Aftermarket — repair-parts substitution to units and prices (thesis B)')
    section(ws, 5, 'A. Sourcing path: cumulative shift of eligible-basket quantity into aftermarket (points of the basket)', quarter_labels())
    label(ws, 7, 'OEM → aftermarket', 'pts', note='Path selector (Inputs row 64): 1 = observed CCC trend, aftermarket dollar share +1.7 pts a year (21.0% → 22.7%, 2024→25, VERIFIED) continued; 2 = memo stress, 1 pt a quarter to a 4-pt endpoint (ASSUMED)')
    label(ws, 8, 'Recycled → aftermarket', 'pts', note='Observed: recycled dollar share fell 0.2 pt a year (10.7% → 10.5%, CCC, VERIFIED) continued; stress: 0.375 pt a quarter (ASSUMED). LKQ FY2025 10-K: most recycled inventory comes from third-party salvage auctions and limited salvage supply could raise its costs over time (VERIFIED counter-evidence)')
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]; nq = 0 if fy == 2026 else (q if fy == 2027 else 4 + q)
        hold = '*$D$56' if fy == 2028 else ''
        put(ws, f'{c}7', f'=IF($D$64=1,$D$65*{nq},$D$54*MIN({nq},4){hold})', fmt='0.0000'); put(ws, f'{c}8', f'=IF($D$64=1,$D$66*{nq},$D$55*MIN({nq},4){hold})', fmt='0.0000')
    label(ws, 9, 'Aftermarket price relative to OEM, drifting: p_AM × (1 + drift)^(years since FQ4 FY26)', 'x', note='Drift = −(OEM inflation − aftermarket inflation) from PartsTrader (Inputs row 68); recycled stays at its anchor because it is priced off the OE list')
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]; nq = 0 if fy == 2026 else (q if fy == 2027 else 4 + q)
        put(ws, f'{c}9', f'=$D$50*(1+$D$68)^({nq}/4)', fmt='0.000')
    group(ws, 10, 'B. Repair-cost channel')
    label(ws, 11, 'Eligible-basket cost index, before the shift  (Σ q_s p_s)', 'x'); label(ws, 12, 'Eligible-basket cost index, after the shift', 'x')
    label(ws, 13, '   basket relative cost change', '%', i=True); label(ws, 14, 'Complete repair-bill change  (× eligible share e)', '%', b=True)
    label(ws, 15, 'Change in total-loss units, relative  (η × bill change)', '%', b=True, note='η is the engine\'s implied selection response per 1% of bill: FY unit delta ÷ repair change in the larger-shift case (ENGINE-derived, Inputs row 61)')
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        put(ws, f'{c}11', '=$D$46*$D$49+$D$47*$D$50+$D$48*$D$51', fmt='0.0000')
        put(ws, f'{c}12', f'=($D$46-{c}7)*$D$49+($D$47+{c}7+{c}8)*{c}9+($D$48-{c}8)*$D$51', fmt='0.0000')
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
    label(ws, 30, 'Parity: the engine\'s assumed basket (65/25/10; prices 1/0.50/0.60; e 40%) at the 5.5-pt endpoint reproduces its documented 1.03% bill saving', '%', note='ENGINE identity check of the formula structure with the engine\'s own inputs (model/aftermarket_bridge README)')
    put(ws, 'D30', '=0.40*(((0.65-0.04)*1+(0.25+0.04+0.015)*0.5+(0.10-0.015)*0.6)/(0.65*1+0.25*0.5+0.10*0.6)-1)', 'engine', F_PCT2, b=True); put(ws, 'E30', '=D30*$D$61', 'engine', F_PCT2); put(ws, 'F30', '← bill change; unit change (η × bill change) vs engine −2.06%', 'note')
    label(ws, 31, 'Sourced basket at the same 5.5-pt stress endpoint (CCC dollar shares, Mitchell price, no drift)', '%', note='The memo\'s stress case at anchor prices; with recycled equal to aftermarket the recycled→aftermarket slice is cost-neutral, so the saving is the OEM→aftermarket slice only')
    put(ws, 'D31', '=$D$45*((($D$46-4*$D$54)*$D$49+($D$47+4*$D$54+4*$D$55)*$D$50+($D$48-4*$D$55)*$D$51)/($D$46*$D$49+$D$47*$D$50+$D$48*$D$51)-1)', fmt=F_PCT2, b=True); put(ws, 'E31', '=D31*$D$61', fmt=F_PCT2)
    label(ws, 28, 'Countercase to keep visible: zero recycled displacement (set Inputs row 55 to 0) removes the price channel and most of the paired downside; OEM-only displacement raised RPU slightly in the engine', i=True)
    group(ws, 38, 'Outputs → other tabs (thesis B effects, always computed; Scenarios switches them on or off)')
    label(ws, E4_DU_ROW, 'Δ total-loss units, relative  (→ E2 TLF cells, → Scenarios)', '%', b=True); label(ws, E4_DP_ROW, 'Δ auction price, relative  (→ Scenarios ASP)', '%', b=True)
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]; put(ws, f'{c}{E4_DU_ROW}', f'={c}15', fmt=F_PCT2, b=True); put(ws, f'{c}{E4_DP_ROW}', f'={c}21', fmt=F_PCT2, b=True)
    section(ws, 44, 'Inputs', ['Value', 'Label'])
    F = ctx['F']
    items = [(45, 'e: parts share of the complete repair bill (all replacement parts)', '=(' + F('ccc_parts_share_of_bill_low')[1:] + '+' + F('ccc_parts_share_of_bill_high')[1:] + ')/2', 'VERIFIED range', 'CCC Crash Course: parts 36–44% of the bill by vehicle age (docs/aftermarket_parameter_audit); 40% is the midpoint. Treats all replacement-part dollars as the basket'),
             (46, 'q_OEM: OEM share of replacement-part dollars, 2025', F('ccc_oem_dollar_share_2025'), 'VERIFIED', 'CCC Crash Course 2026: 1 − 22.7% − 10.5% (dollar shares; counts differ slightly, see docs/bidmate_adoption)'), (47, 'q_AM: aftermarket share of replacement-part dollars, 2025', F('ccc_am_dollar_share_2025'), 'VERIFIED', 'CCC Crash Course 2026, 22.7% (21.0% in 2024)'), (48, 'q_rec: recycled share of replacement-part dollars, 2025', F('ccc_rec_dollar_share_2025'), 'VERIFIED', 'CCC Crash Course 2026, 10.5% (10.7% in 2024)'),
             (49, 'p_OEM: relative price', 1.00, 'ASSUMED', 'Numeraire'), (50, 'p_AM: aftermarket price relative to OEM', '=1-' + F('mitchell_am_discount_2016_mean')[1:], 'VERIFIED (historical)', 'Mitchell Q2 2017 Industry Trends Report pp. 8–10: 2016 six-component discounts 23.3% domestic, 29.9% Asian, 27.7% European; mean 27% (raw cache; docs/aftermarket_transition_evidence). Current catalogue ~0.50 is a stress (MapleV 2026, vendor-selected)'), (51, 'p_rec: recycled price relative to OEM at the anchor (set equal to aftermarket)', '=D50', 'ASSUMED (neutral)', 'No matched national dataset: trade sources put recycled 25–50% below OEM and aftermarket 20–50% below; equal at the anchor is the neutral choice. Recycled is priced off the OE list (PartsTrader), so it does not drift'),
             (52, 'x: donor contribution exposed to collision-part substitution', 0.25, 'ASSUMED', 'No supporting record (FORWARD_ASSUMPTIONS.md)'), (53, 'κ: contribution-to-hammer bid ratio', 1.5, 'ASSUMED', 'Sturgeon 2018 margins make the scale interpretable, not the value'),
             (54, 'Stress path: OEM → aftermarket shift per quarter through FY27 (points)', 0.01, 'ASSUMED', 'model/thesis_audit_2026-10-01/assumptions.json (memo stress; 5.5-pt endpoint)'), (55, 'Stress path: recycled → aftermarket shift per quarter (points)', 0.00375, 'ASSUMED', 'same'), (56, 'Stress path: hold FY27 endpoint through FY28 (1) or revert (0)', 1, 'toggle', 'Convention for the stress path only'),
             (57, 'τ: recycler bid transmission to the marginal price', 0.5, 'ASSUMED', 'The 10% case removes most of the price effect (AUDIT.md)'), (58, 'Endpoint recycled displacement used by the engine (points)', 0.015, 'ASSUMED', 'ccc_larger_shift case')]
    items += [(64, 'Sourcing path selector: 1 = observed CCC trend continued; 2 = memo stress (5.5 pts by FQ4 FY27)', 1, 'toggle', 'Default is the evidence; the stress is shown for the memo\'s larger case'),
              (65, 'Observed path: aftermarket dollar-share gain per quarter (points)', '=(' + F('ccc_am_dollar_share_2025')[1:] + '-' + F('ccc_am_dollar_share_2024')[1:] + ')/4', 'VERIFIED (trend)', 'CCC 2024→25 +1.7 pts a year ÷ 4; a one-year trend, so a continuation assumption'),
              (66, 'Observed path: recycled dollar-share loss per quarter (points)', '=(' + F('ccc_rec_dollar_share_2024')[1:] + '-' + F('ccc_rec_dollar_share_2025')[1:] + ')/4', 'VERIFIED (trend)', 'CCC 2024→25 −0.2 pt a year ÷ 4'),
              (68, 'Aftermarket relative-price drift per year  (−(OEM inflation − aftermarket inflation), PartsTrader Apr 2025–Mar 2026)', '=-(' + F('partstrader_oem_inflation')[1:] + '-' + F('partstrader_am_inflation')[1:] + ')', 'VERIFIED (trend, one year)', 'Aftermarket flat under tariffs while OEM and recycled (priced off OE) rose 4.3%; continued through FY28 as an assumption. Incremental to a reference that holds general repair cost neutral'),
              (67, 'Tariff effect: additional aftermarket share suppressed by the Taiwan parts tariff (points, FY27 endpoint)', 0.0, 'ASSUMED', 'Memo: 0.84–1.69 pts with a price-response coefficient of 2; coefficient unsourced, so 0 by default. The other session verified a 1 May 2025 implementation for qualifying categories only')]
    for row, lab, val, lbl, src in items:
        kind = 'toggle' if lbl == 'toggle' else ('link' if isinstance(val, str) else 'input'); label(ws, row, lab, note=src); put(ws, f'D{row}', val, kind, '0.0000' if (isinstance(val, float) or kind == 'link') else '0'); put(ws, f'E{row}', lbl if lbl != 'toggle' else 'TOGGLE', 'note')
    label(ws, 61, 'η: selection response, Δ units per unit of bill change (ENGINE-derived: ccc_larger_shift unit delta ÷ repair change)', note='D Engine CCC scenario summary; the engine\'s derivative is calibrated to levels only (AUDIT.md priority 1)')
    put(ws, 'D61', f"=SUMIFS('D Engine'!$F${e0}:$F${e1},'D Engine'!$B${e0}:$B${e1},\"ccc_larger_shift\")/SUMIFS('D Engine'!$C${e0}:$C${e1},'D Engine'!$B${e0}:$B${e1},\"ccc_larger_shift\")", 'engine', '0.000'); put(ws, 'E61', 'ENGINE', 'note')
    ws.freeze_panes = 'D6'
