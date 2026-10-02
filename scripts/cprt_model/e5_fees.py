"""E5 Prices & Fees: historical ledger -> implied insurance units; ASP path; fee mapping -> all-in RPU."""
from .common import *
def build(wb, ctx):
    ws = wb.create_sheet('E5 Prices & Fees'); tab_color(ws, '7030A0'); setup(ws)
    std_header(ws, 'All-in RPU = buyer fee(ASP) + seller rate × ASP + fixed fees + attached services;  buyer fee(ASP) = β × (ASP ÷ ASP₀)^ε.  Ledger: FY26 US service $ × insurance share ÷ all-in RPU = implied units.  Appendix A, Eq. 5.', 'E5 Prices & Fees — vehicle prices, fee economics and the historical ledger')
    section(ws, 5, 'A. Historical ledger, FY26 (reported dollars; the split and the units are inferred, not disclosed)', quarter_labels())
    g = ctx['geo_rows']
    label(ws, 6, 'US service revenue (8-K)', '$M', note='VERIFIED: D Reported geography table (raw/sec/8k)')
    label(ws, 7, 'Insurance share of US service dollars', '%', note='ASSUMED 90% (80% alternative); 10-K FY26: insurers supplied 79% of vehicles processed globally — different denominator')
    label(ws, 8, 'US insurance service revenue', '$M', b=True); label(ws, 9, 'Attached services per sale (title + delivery)', '$', note='ASSUMED 50% × $50 + 10% × $300 = $55; undisclosed products')
    label(ws, 10, 'Core RPU at the FY26 price level', '$'); label(ws, 11, 'Implied US insurance units', '000s', b=True, note='Inferred by identity; labelled MODELED, not disclosed'); label(ws, 12, '   y/y (diagnostic; FY27+ comes from Scenarios)', '%', i=True)
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        if fy == 2026:
            put(ws, f'{c}6', f"='D Reported'!$D${g[(2026,q)]}", 'link', F_MONEY); put(ws, f'{c}7', '=$D$39', 'link', F_PCT); put(ws, f'{c}8', f'={c}6*{c}7', fmt=F_MONEY, b=True)
            put(ws, f'{c}9', '=$D$40*$D$41+$D$42*$D$43', fmt=F_USD); put(ws, f'{c}10', f'={c}23', 'link', F_USD); put(ws, f'{c}11', f'={c}8*1000/({c}10+{c}9)', fmt=F_INT, b=True)
    for r, fmt in ((6, F_MONEY), (8, F_MONEY), (11, F_INT)): put(ws, f'{ACOL[2026]}{r}', f'=SUM({QCOL[(2026,1)]}{r}:{QCOL[(2026,4)]}{r})', fmt=fmt, b=(r != 6))
    group(ws, 14, 'B. Vehicle prices: US insurance ASP, base path (continuation; thesis B price change applied in Scenarios)')
    label(ws, 15, 'US insurance ASP, base path', '$', b=True, note='FY26 level is the engine\'s modeled selected-vehicle price (ENGINE, $3,041), held flat within FY26; FY27+ grows at the input rate')
    label(ws, 16, '   y/y', '%', i=True); label(ws, 17, 'Reference: disclosed US insurance ASP y/y (FQ4 FY26 +3.7%; Manheim +2.8%)', '%', i=True, note='VERIFIED, call 10 Sep 2026')
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        if fy == 2026: put(ws, f'{c}15', '=$D$45', 'link', F_USD)
        else: put(ws, f'{c}15', f'={QCOL[(fy-1,q)]}15*(1+$D$44)', fmt=F_USD, b=True); put(ws, f'{c}16', f'={c}15/{QCOL[(fy-1,q)]}15-1', fmt=F_PCT, i=True)
    put(ws, f'{QCOL[(2026,4)]}17', ctx['F']('cprt_us_ins_asp_yoy_fq4fy26'), 'link', F_PCT); put(ws, f'{QCOL[(2026,3)]}17', ctx['F']('manheim_yoy_fq4fy26'), 'link', F_PCT); put(ws, f'{QCOL[(2026,2)]}17', 'Manheim →', 'note')
    group(ws, 19, 'C. Fee economics per sold insurance vehicle (posted grid summarised by an elasticity; grid itself on D Fees)')
    label(ws, 20, 'Buyer variable fee  β × (ASP ÷ ASP₀)^ε_b', '$', note='β and ε_b derived from the engine\'s 1,024-node fee integration (Inputs rows 46–51)')
    label(ws, 21, 'Seller commission  (rate from E3, base)', '$'); label(ws, 22, 'Fixed buyer fees (gate, environmental)', '$', note='ASSUMED $110 inherited; posted fixed fees on D Fees show gate $79/$95 — to be reconciled')
    label(ws, 23, 'Core RPU', '$', b=True); label(ws, 24, 'Attached services per sale', '$'); label(ws, 25, 'All-in insurance RPU, base', '$', b=True); label(ws, 26, '   y/y', '%', i=True)
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        put(ws, f'{c}20', f'=$D$50*({c}15/$D$45)^$D$51', fmt=F_USD); put(ws, f'{c}21', f"='E3 Carriers'!{c}${E3_SELLER_BASE_ROW}*{c}15", 'link', F_USD); put(ws, f'{c}22', '=$D$48', 'link', F_USD)
        put(ws, f'{c}23', f'={c}20+{c}21+{c}22', fmt=F_USD, b=True); put(ws, f'{c}24', '=$D$40*$D$41+$D$42*$D$43', fmt=F_USD); put(ws, f'{c}25', f'={c}23+{c}24', fmt=F_USD, b=True)
        if fy > 2026: put(ws, f'{c}26', f'={c}25/{QCOL[(fy-1,q)]}25-1', fmt=F_PCT, i=True)
    put(ws, 'B28', 'Feeds →  Scenarios (FY26 units row 11; ASP path row 15; fee parameters Inputs rows 45–51; attached services row 24)', 'note')
    section(ws, 38, 'Inputs', ['Value', 'Label'])
    items = [(39, 'Insurance share of US service dollars', 0.90, 'toggle', 'ASSUMED', '0.80 alternative; carry both'),
             (40, 'Title service: adoption (share of sales)', 0.50, 'input', 'ASSUMED', 'Undisclosed'), (41, 'Title service: charge per job', 50, 'input', 'ASSUMED', 'Inherited with the adoption rate above; product price undisclosed'),
             (42, 'Delivery service: adoption', 0.10, 'input', 'ASSUMED', 'Undisclosed; gross/net unknown'), (43, 'Delivery service: charge per job', 300, 'input', 'ASSUMED', 'Inherited; gross charge per delivered vehicle, product price undisclosed'),
             (44, 'US insurance ASP growth, FY27+ (continuation)', 0.037, 'input', 'ASSUMED', 'FQ4 FY26 disclosed +3.7% continued; not guidance (6% alternative)'),
             (45, 'ASP₀: modeled selected-vehicle price at the FY26 anchor', ctx['F']('engine_asp0'), 'link', 'ENGINE', 'age_constrained_engine_results.json baseline_core.ASP'),
             (46, 'Core RPU at the anchor (buyer fees + seller commission + fixed fees)', ctx['F']('engine_core_rpu0'), 'link', 'ENGINE', 'baseline_core.core_RPU'),
             (47, 'Seller commission rate embedded in the anchor', 0.04, 'input', 'ASSUMED', 'driver_register buyer_and_seller_fees'), (48, 'Fixed buyer fees embedded in the anchor', 110, 'input', 'ASSUMED', 'Inherited; contradicts posted $79/$95 gate fee — flagged in source trace'),
             (49, 'Core-RPU elasticity to ASP from the engine\'s +5% value test  (ln(1 + ΔRPU) ÷ ln(1 + ΔASP))', '=LN(1+' + ctx['F']('engine_value_plus5_rpu')[1:] + ')/LN(1+' + ctx['F']('engine_value_plus5_asp')[1:] + ')', 'formula', 'ENGINE', 'age_constrained_engine_results.json scenario_changes value_plus_5pct'),
             (50, 'β: buyer variable fee at the anchor  (core − seller − fixed)', '=D46-D47*D45-D48', 'formula', 'ENGINE', 'Identity'),
             (51, 'ε_b: buyer-fee elasticity to ASP  ((ε_core × core − seller$) ÷ β)', '=(D49*D46-D47*D45)/D50', 'formula', 'ENGINE', 'Identity; the stepwise grid is summarised by one elasticity between ±5% of the anchor')]
    for row, lab, val, kind, lbl, src in items:
        label(ws, row, lab, note=src); put(ws, f'D{row}', val, kind, '0.000' if (isinstance(val, float) and val < 10) or kind == 'formula' else F_USD if isinstance(val, (int, float)) and val > 10 else '0'); put(ws, f'E{row}', lbl, 'note')
    ws.freeze_panes = 'D6'
