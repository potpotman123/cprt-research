"""Summary (Solstice-style): headline financials from the 3SM, Barclays and consensus with % Δ, the component delta to Street for FY2027E, valuation links."""
from .common import *
YEARS = list(range(2024, 2030)); SC = {y: L(4 + i) for i, y in enumerate(YEARS)}; TC = {y: L(4 + y - 2022) for y in YEARS}   # Summary cols D–I; 3SM/DCF cols F–K
BC = {2026: 'D', 2027: 'E', 2028: 'F', 2029: 'G'}; NOTES = 'L'
def build(wb, ctx):
    ws = wb.create_sheet('Summary'); tab_color(ws, NAVY); setup(ws, label_w=70, ncols=6, notes_col=NOTES); NOTES_COL['Summary'] = NOTES
    title(ws, 'Copart, Inc. — Summary: headline financials, Street comparison and the component delta to Street',
          'Every cell links to the 3SM, DCF, Scenarios, Street or D Barclays tab (green). Fiscal years end 31 July. $M except per share. Barclays = 11 Sep 2026 model (Underweight, $25).')
    header(ws, 4, None, hist_span=(4, 6), proj_span=(7, 9), notes_col=NOTES)
    T = ctx['tsm_rows']; b = ctx['barclays_rows']; bk = lambda pre: next(k for k in b if k.startswith(pre)); s0 = ctx['summary_row0']
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
    nxt(); section(ws, nxt(), 'Street — Barclays model (11 Sep 2026) and consensus EPS; % Δ = 3SM ÷ Street − 1', per)
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
    nxt(); section(ws, nxt(), 'Component delta to Street — FY2027E legacy service revenue ($M) and the EBITDA bridge to Barclays', ['FY2027E'])
    def one(text, f, units='$M', fmt=F_MONEY, kind='link', bold=False, ital=False, indent=0, note=''):
        rr = nxt(); label(ws, rr, text, units, b=bold, i=ital, indent=indent, note=note); put(ws, f'D{rr}', f, kind, fmt, b=bold); return rr
    S = lambda c, k: f'=Scenarios!{c}{s0 + k}'
    c0 = one('Street-implied (case 0): known runoff, coverage recovering to the Street path', S('D', 1), note=f'Scenarios D{s0 + 1}; the recovery rate is reverse-solved so case 0 equals JPMorgan')
    one('JPMorgan FY27E legacy service revenue, 11 Sep 2026 (ex-ACV)', '=Scenarios!$D$108', note='Scenarios D108 ← D Facts (licensed report held locally)')
    t1 = one('Thesis 1 — coverage persistence: case 1 (known facts, sticky coverage) − case 0', S('F', 2), bold=True, note=f'Scenarios F{s0 + 2}')
    t2 = one('Thesis 2 — aftermarket substitution: thesis 2 case − case 1', S('E', 4), bold=True, note=f'Scenarios E{s0 + 4}')
    t3 = one('Thesis 3 — carrier reallocation (probability-weighted): thesis 3 case − case 1', S('E', 5), bold=True, note=f'Scenarios E{s0 + 5}')
    one('Interaction (all three − case 0 − sum of the three parts; exact on the common base)', f'=Scenarios!F{s0 + 6}-D{t1}-D{t2}-D{t3}', kind='formula', ital=True, indent=1)
    one('All three vs Street-implied', S('F', 6), bold=True, note=f'Scenarios F{s0 + 6}')
    one('All three vs JPMorgan, %', S('H', 6), '%', F_PCT, note=f'Scenarios H{s0 + 6}')
    sel = one('Selected case on the RPM (D3): FY27E service revenue', '=RPM!I10', note='RPM I10 → 3SM')
    one('Δ selected case vs Street-implied', f'=D{sel}-D{c0}', kind='formula', bold=True)
    one('Vehicle sales FY27E (RPM)', '=RPM!I12', note='RPM I12; JPMorgan purchased-vehicle revenue 710 on Street F8')
    one('Δ vs JPMorgan purchased-vehicle revenue', '=RPM!I12-Street!F8', kind='formula', ital=True, indent=1)
    nxt(); label(ws, nxt(), 'EBITDA bridge to Barclays, FY2027E', b=True)
    drev = one('Δ revenue (3SM − Barclays)', f"='3SM'!I{T['d_rev']}", note=f"3SM row {T['d_rev']}")
    reff = one("of which revenue effect at Barclays' EBITDA margin", f"=D{drev}*'3SM'!I{T['b_ebitda']}/'3SM'!I{T['b_rev']}", kind='formula', ital=True, indent=1)
    deb = one('Δ adjusted EBITDA (3SM − Barclays)', f"='3SM'!I{T['d_ebitda']}", bold=True, note=f"3SM row {T['d_ebitda']}")
    one('of which margin effect (facility cost per unit on fewer units; Barclays-implied G&A ratio)', f'=D{deb}-D{reff}', kind='formula', ital=True, indent=1)
    one('Δ diluted EPS ($)', f"='3SM'!I{T['eps']}-'3SM'!I{T['b_eps']}", '$', F_USD + '0', kind='formula', bold=True)
    one('Δ diluted EPS (%)', f"='3SM'!I{T['d_eps']}", '%', F_PCT)
    nxt(); label(ws, nxt(), 'Valuation (links)', b=True)
    one('Current share price (DCF H118)', '=DCF!H118', '$', F_USD)
    one('DCF implied share price, selected case (DCF H113)', '=DCF!H113', '$', F_USD, bold=True)
    one('Upside / (downside) vs current (DCF H114)', '=DCF!H114', '%', F_PCT)
    one('WACC (Reverse DCF S25, bottom-up build)', "='Reverse DCF'!S25", '%', F_PCT2)
    one('Exit EV/EBITDA multiple (DCF H92; Barclays uses 10×)', '=DCF!H92', 'x', F_X)
    one('Structural effective tax rate (Reverse DCF S33)', "='Reverse DCF'!S33", '%', F_PCT2)
    ws.freeze_panes = 'D5'
