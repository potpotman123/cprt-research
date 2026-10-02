"""Summary (Solstice-style, compact): headline financials from the 3SM, Barclays and consensus with % Δ, component delta to Street by year, EBITDA bridge, valuation strip."""
from .common import *
YEARS = list(range(2024, 2030)); SC = {y: L(4 + i) for i, y in enumerate(YEARS)}; TC = {y: L(4 + y - 2022) for y in YEARS}   # Summary cols D–I; 3SM/DCF cols F–K
BC = {2026: 'D', 2027: 'E', 2028: 'F', 2029: 'G'}; SQ = {2027: 'Q', 2028: 'R'}; NOTES = 'L'
def build(wb, ctx):
    ws = wb.create_sheet('Summary'); tab_color(ws, NAVY); setup(ws, label_w=70, ncols=6, notes_col=NOTES); NOTES_COL['Summary'] = NOTES
    title(ws, 'Copart, Inc. — Summary: headline financials, Street comparison and the component delta to Street',
          'Every cell links to the 3SM, DCF, Scenarios, Street, Cover or D Barclays tab (green). Fiscal years end 31 July. $M except per share. Barclays = 11 Sep 2026 model (Underweight, $25). – = no line for that year.')
    header(ws, 4, None, hist_span=(4, 6), proj_span=(7, 9), notes_col=NOTES)
    T = ctx['tsm_rows']; b = ctx['barclays_rows']; bk = lambda pre: next(k for k in b if k.startswith(pre)); s0 = ctx['summary_row0']
    br = lambda k: 7 + (k - 1) * 13 + 1 + 8          # Scenarios row holding case k's FY27 (col Q) and FY28 (col R) legacy service revenue
    case = lambda k, fy: f'Scenarios!{SQ[fy]}{br(k)}'
    per = [f'FY{y}{"A" if y <= 2026 else "E"}' for y in YEARS]; r = [4]
    def nxt(n=1): r[0] += n; return r[0]
    def row(text, units, fn, fmt=F_MONEY, kind='link', bold=False, ital=False, indent=0, note='', years=YEARS):
        rr = nxt(); label(ws, rr, text, units, b=bold, i=ital, indent=indent, note=note)
        for fy in years:
            v = fn(fy, SC[fy], SC.get(fy - 1))
            if v is not None: put(ws, f'{SC[fy]}{rr}', v, kind, fmt, b=bold)
        return rr
    g = lambda rr: (lambda fy, c, p: f'=IF({p}{rr}=0,0,{c}{rr}/{p}{rr}-1)' if p else None)
    m = lambda num, den: (lambda fy, c, p: f'=IF({c}{den}=0,0,{c}{num}/{c}{den})')
    dl = lambda ours, theirs: (lambda fy, c, p: f'=IF({c}{theirs}=0,0,{c}{ours}/{c}{theirs}-1)' if fy in BC else None)
    tsm = lambda key: (lambda fy, c, p: f"='3SM'!{TC[fy]}{T[key]}")
    bar = lambda pre: (lambda fy, c, p: f"='D Barclays'!{BC[fy]}{b[bk(pre)]}" if fy in BC else None)
    units_of = lambda fmt: '$M' if fmt == F_MONEY else '%' if fmt in (F_PCT, F_PCT2) else '$'
    # ---- headline financials
    section(ws, nxt(), 'Headline financials — 3SM, selected case (RPM D3)', per)
    rev = row('Revenue', '$M', tsm('rev'), bold=True, note=f"3SM row {T['rev']} (RPM)")
    row('y/y growth', '%', g(rev), F_PCT, 'formula', ital=True, indent=1, years=YEARS[1:])
    ebitda = row('Adjusted EBITDA', '$M', tsm('ebitda'), bold=True, note=f"3SM row {T['ebitda']} (EBIT + D&A, Barclays definition)")
    row('margin', '%', m(ebitda, rev), F_PCT, 'formula', ital=True, indent=1)
    eps = row('GAAP diluted EPS', '$', tsm('eps'), F_USD + '0', bold=True, note=f"3SM row {T['eps']}")
    row('y/y growth', '%', g(eps), F_PCT, 'formula', ital=True, indent=1, years=YEARS[1:])
    fcf = row('Free cash flow (CFO + capex)', '$M', tsm('fcf'), bold=True, note=f"3SM row {T['fcf']}")
    row('margin', '%', m(fcf, rev), F_PCT, 'formula', ital=True, indent=1)
    ufcf = row('Unlevered free cash flow (DCF)', '$M', lambda fy, c, p: f'=DCF!{TC[fy]}63', note='DCF row 63: NOPAT + D&A + SBC − capex − ΔNWC; D&A, SBC, capex and ΔNWC read the 3SM')
    row('margin', '%', m(ufcf, rev), F_PCT, 'formula', ital=True, indent=1)
    # ---- Street
    section(ws, nxt(), 'Street — Barclays model (11 Sep 2026) and consensus EPS; % Δ = 3SM ÷ Street − 1', per)
    brev = row('Barclays revenue', '$M', bar('Revenue'), note='D Barclays (numeric extraction from the licensed report held locally; FY2026A = reported)')
    row('y/y growth', '%', g(brev), F_PCT, 'formula', ital=True, indent=1, years=[2027, 2028, 2029])
    row('% Δ 3SM vs Barclays', '%', dl(rev, brev), F_PCT, 'formula', bold=True, indent=1)
    beb = row('Barclays adjusted EBITDA', '$M', bar('EBITDA (adj)'))
    row('margin', '%', lambda fy, c, p: f'=IF({c}{brev}=0,0,{c}{beb}/{c}{brev})' if fy in BC else None, F_PCT, 'formula', ital=True, indent=1)
    row('% Δ 3SM vs Barclays', '%', dl(ebitda, beb), F_PCT, 'formula', bold=True, indent=1)
    beps = row('Barclays diluted EPS', '$', bar('EPS (adj)'), F_USD + '0')
    row('% Δ 3SM vs Barclays', '%', dl(eps, beps), F_PCT, 'formula', bold=True, indent=1)
    ceps = row("Consensus EPS, post-print (owner's DCF row 49)", '$', lambda fy, c, p: f'=DCF!{TC[fy]}49' if fy in (2026, 2027) else None, F_USD + '0', note='DCF rows 45–49 hold Barclays, JPMorgan, BNP, Stephens and the consensus (owner-entered, dated)')
    row('% Δ 3SM vs consensus', '%', lambda fy, c, p: f'=IF({c}{ceps}=0,0,{c}{eps}/{c}{ceps}-1)' if fy in (2026, 2027) else None, F_PCT, 'formula', bold=True, indent=1)
    for lab, col in (('BNP Paribas (Outperform, $40)', 'E'), ('J.P. Morgan', 'F'), ('BofA Global Research', 'G'), ('Barclays, 25 Aug 2026 note', 'I')):
        row(f'Broker total revenue — {lab}', '$M', lambda fy, c, p, col=col: f'=Street!{col}{9 if fy == 2027 else 10}' if fy in (2027, 2028) else None, note='Street tab rows 9–10 (named-broker extractions; report dates in Street row 5)')
    # ---- component delta to Street, by year
    section(ws, nxt(), 'Component delta to Street — legacy service revenue by case ($M; engines run FY27–28) and the EBITDA bridge to Barclays', per)
    def comp(text, f27, f28=None, fmt=F_MONEY, kind='link', bold=False, ital=False, indent=0, note=''):
        rr = nxt(); label(ws, rr, text, units_of(fmt), b=bold, i=ital, indent=indent, note=note); put(ws, f'G{rr}', f27, kind, fmt, b=bold)
        if f28 is not None: put(ws, f'H{rr}', f28, kind, fmt, b=bold)
        return rr
    c0 = comp('Street-implied (case 0): known runoff, coverage recovering to the Street path', f'={case(1, 2027)}', f'={case(1, 2028)}', note=f'Scenarios Q/R{br(1)}; the recovery rate is reverse-solved so FY27 equals JPMorgan')
    comp('JPMorgan FY27E legacy service revenue, 11 Sep 2026 (ex-ACV)', '=Scenarios!$D$108', note='Scenarios D108 ← D Facts (licensed report held locally); JPMorgan publishes no FY28 service line')
    t1 = comp('Thesis 1 — coverage persistence: case 1 (known facts, sticky coverage) − case 0', f'={case(2, 2027)}-{case(1, 2027)}', f'={case(2, 2028)}-{case(1, 2028)}', bold=True, note=f'Scenarios rows {br(2)} − {br(1)}')
    t2 = comp('Thesis 2 — aftermarket substitution: thesis 2 case − case 1', f'={case(4, 2027)}-{case(2, 2027)}', f'={case(4, 2028)}-{case(2, 2028)}', bold=True, note=f'Scenarios rows {br(4)} − {br(2)}')
    t3 = comp('Thesis 3 — carrier reallocation (probability-weighted): thesis 3 case − case 1', f'={case(5, 2027)}-{case(2, 2027)}', f'={case(5, 2028)}-{case(2, 2028)}', bold=True, note=f'Scenarios rows {br(5)} − {br(2)}')
    comp('Interaction (all three − case 0 − sum of the three parts; exact on the common base)', f'={case(6, 2027)}-{case(1, 2027)}-G{t1}-G{t2}-G{t3}', f'={case(6, 2028)}-{case(1, 2028)}-H{t1}-H{t2}-H{t3}', kind='formula', ital=True, indent=1)
    comp('All three vs Street-implied', f'={case(6, 2027)}-{case(1, 2027)}', f'={case(6, 2028)}-{case(1, 2028)}', bold=True, note=f'Scenarios rows {br(6)} − {br(1)}')
    comp('All three vs JPMorgan, %', f'=Scenarios!H{s0 + 6}', fmt=F_PCT, note=f'Scenarios H{s0 + 6}')
    sel = comp('Selected case on the RPM (D3): service revenue', '=RPM!I10', '=RPM!J10', note='RPM I10 / J10 → 3SM')
    comp('Δ selected case vs Street-implied', f'=G{sel}-G{c0}', f'=H{sel}-H{c0}', kind='formula', bold=True)
    comp('Vehicle sales (RPM)', '=RPM!I12', '=RPM!J12', note='RPM I12 / J12; JPMorgan FY27E purchased-vehicle revenue 710 on Street F8')
    comp('Δ vs JPMorgan FY27E purchased-vehicle revenue', '=RPM!I12-Street!F8', kind='formula', ital=True, indent=1)
    group(ws, nxt(), 'EBITDA bridge to Barclays (3SM − Barclays; Barclays publishes FY27–29)')
    def bridge(text, fn, fmt=F_MONEY, kind='link', bold=False, ital=False, indent=0, note=''):
        rr = nxt(); label(ws, rr, text, units_of(fmt), b=bold, i=ital, indent=indent, note=note)
        for fy in (2027, 2028, 2029): put(ws, f'{SC[fy]}{rr}', fn(fy, SC[fy], TC[fy]), kind, fmt, b=bold)
        return rr
    drev = bridge('Δ revenue', lambda fy, c, tc: f"='3SM'!{tc}{T['d_rev']}", note=f"3SM row {T['d_rev']}")
    reff = bridge("of which revenue effect at Barclays' EBITDA margin", lambda fy, c, tc: f"={c}{drev}*'3SM'!{tc}{T['b_ebitda']}/'3SM'!{tc}{T['b_rev']}", kind='formula', ital=True, indent=1)
    deb = bridge('Δ adjusted EBITDA', lambda fy, c, tc: f"='3SM'!{tc}{T['d_ebitda']}", bold=True, note=f"3SM row {T['d_ebitda']}")
    bridge('of which margin effect (facility cost per unit on fewer units; Barclays-implied G&A ratio)', lambda fy, c, tc: f'={c}{deb}-{c}{reff}', kind='formula', ital=True, indent=1)
    bridge('Δ diluted EPS ($)', lambda fy, c, tc: f"='3SM'!{tc}{T['eps']}-'3SM'!{tc}{T['b_eps']}", F_USD + '0', kind='formula', bold=True)
    bridge('Δ diluted EPS (%)', lambda fy, c, tc: f"='3SM'!{tc}{T['d_eps']}", F_PCT)
    # ---- valuation strip (one row, six links)
    section(ws, nxt(), 'Valuation (links)', ['Price (Cover)', 'DCF implied', 'Upside', 'WACC', 'Exit multiple', 'Tax rate'])
    rr = nxt(); label(ws, rr, 'Current price (Cover D6) · DCF implied share price (H113) · upside (H114) · WACC (Reverse DCF S25) · exit EV/EBITDA (DCF H92; Barclays 10×) · structural tax rate (S33)')
    for c, f, fmt in (('D', '=Cover!D6', F_USD), ('E', '=DCF!H113', F_USD), ('F', '=DCF!H114', F_PCT), ('G', "='Reverse DCF'!S25", F_PCT2), ('H', '=DCF!H92', F_X), ('I', "='Reverse DCF'!S33", F_PCT2)): put(ws, f'{c}{rr}', f, 'link', fmt, b=(c == 'E'))
    ws.freeze_panes = 'D5'
