"""Reverse DCF on Barclays' published model (11 Sep 2026, UW, PT $25 = 10x FY2026E EBITDA): Via-style, one lever solved to today's price."""
from .common import *
SRC = "Barclays, Copart Inc. F4Q26 Review (11 Sep 2026), financial summary; licensed report held locally; txt lines 147–190"
B = {  # FY2026A, FY2027E, FY2028E, FY2029E  (Barclays table; $mn unless stated)
 'Revenue': (147, [4666, 4768, 4948, 5128]), 'EBITDA (adj)': (148, [1882, 1916, 2018, 2116]), 'EBIT (adj)': (149, [1653, 1690, 1784, 1873]),
 'Pre-tax income (adj)': (150, [1835, 1830, 1924, 2013]), 'Net income (adj)': (151, [1484, 1458, 1533, 1604]), 'EPS (adj), $': (152, [1.55, 1.56, 1.64, 1.72]),
 'Diluted shares, mn': (153, [957, 933, 933, 934]), 'Cash and equivalents': (167, [4490, 5656, 6907, 8240]), 'Total assets': (168, [10028, 11602, 13252, 14976]),
 'Short and long-term debt': (169, [88, 88, 88, 88]), 'Net debt / (funds)': (173, [-1820, -2986, -4237, -5570]), "Shareholders' equity": (174, [9097, 10612, 12202, 13865]),
 'Change in working capital': (175, [-208, -83, -83, -83]), 'Cash flow from operations': (176, [1604, 1646, 1731, 1813]), 'Capital expenditure': (177, [-337, -500, -500, -500]),
 'Free cash flow (Barclays line; definition not stated)': (178, [1942, 2146, 2231, 2313]), 'EV/EBITDA (adj), x, at $30.75': (183, [15.0, 14.1, 12.8, 11.5]), 'P/E (adj), x': (181, [19.8, 19.7, 18.7, 17.9])}
YEARS = ['FY2026A', 'FY2027E', 'FY2028E', 'FY2029E']
def build(wb, ctx):
    # ---------------- D Barclays
    ws = wb.create_sheet('D Barclays'); tab_color(ws, 'BFBFBF'); setup(ws, label_w=46, ncols=8)
    title(ws, 'D Barclays — published model, Copart F4Q26 Review, 11 September 2026 (Underweight, PT $25)', 'Numeric extraction only from a licensed report held locally; no text reproduced. PT = 10x EV/EBITDA on FY2026E (report line 468). Price in the report $30.75 (10 Sep 2026). Shares outstanding 925.81mn (line 57).')
    for j, h in enumerate(['Line'] + YEARS + ['Report line']): put(ws, f'{L(3+j)}4', h, 'label', b=True)
    rows = {}
    for i, (lab, (line, vals)) in enumerate(B.items()):
        r = 5 + i; rows[lab] = r; put(ws, f'B{r}', lab, 'label')
        for j, v in enumerate(vals): put(ws, f'{L(4+j)}{r}', v, 'input', '0.00' if 'EPS' in lab or ', x' in lab else F_INT)
        put(ws, f'H{r}', f'line {line}', 'note')
    put(ws, f'B{5+len(B)+1}', SRC, 'note'); ctx['barclays_rows'] = rows
    # ---------------- Rebuild the owner's 'Reverse DCF' tab in place (owner's 2 Oct shape: two-year explicit period, FY28E exit multiple)
    rd = wb['Reverse DCF']
    for rng in list(rd.merged_cells.ranges): rd.unmerge_cells(str(rng))
    for row in rd.iter_rows(min_row=3, max_row=max(rd.max_row, 80)):
        for c in row: c.value = None; c.font = font(); c.fill = PatternFill(); c.border = Border()
    NOTES_COL['Reverse DCF'] = 'P'
    put(rd, 'B2', "Reverse DCF on Barclays' published model (11 Sep 2026, Underweight, PT $25 = 10x FY2026E EBITDA). Explicit period FY27E–FY28E, cash flow = CFO − capex margin, terminal = exit multiple on FY2028E EBITDA. One lever solved to today's price; Goal Seek H41 to 0 after any change.", 'note')
    section(rd, 4, 'A. Market data and capital structure (links to the DCF tab)', ['Value', 'Source'])
    A = [(5, 'Current share price (26 Sep 2026)', '=DCF!H118', F_USD + '.00', 'DCF tab'), (6, 'Shares outstanding, mn (31 Jul 2026)', '=DCF!H112', '0.0', 'DCF tab; Barclays 925.81 (line 57)'),
         (7, 'Market capitalisation', '=D5*D6', F_INT, ''), (8, '(−) Cash & HTM securities', '=-DCF!H107', F_INT, 'DCF tab'), (9, '(+) Total debt', '=-DCF!H108', F_INT, 'DCF tab'), (10, '(+) Non-controlling interest', '=-DCF!H109', F_INT, 'DCF tab'),
         (11, 'Enterprise value today', '=D7+D8+D9+D10', F_INT, ''), (12, 'WACC (cost of equity; no net debt)', '=DCF!H88', F_PCT2, 'DCF tab')]
    for r, lab, f, fmt, note in A: label(rd, r, lab, note=note, b=(r in (7, 11))); put(rd, f'D{r}', f, 'link' if 'DCF' in f else 'formula', fmt, b=(r in (7, 11)))
    section(rd, 14, "B. Barclays' operating path (green = D Barclays, 11 Sep 2026)", ['FY2026A', 'FY2027E', 'FY2028E', '', 'FY2029E (shown, not discounted)'])
    br = ctx['barclays_rows']; cols = {'FY2026A': 'D', 'FY2027E': 'E', 'FY2028E': 'F', 'FY2029E': 'H'}; src = {'FY2026A': 'D', 'FY2027E': 'E', 'FY2028E': 'F', 'FY2029E': 'G'}
    def row(r, lab, key=None, fmt=F_INT, b=False, formula=None, i=False, note='', years=('FY2026A', 'FY2027E', 'FY2028E', 'FY2029E')):
        label(rd, r, lab, b=b, i=i, note=note)
        for y in years:
            c = cols[y]
            if key: put(rd, f'{c}{r}', f"='D Barclays'!{src[y]}{br[key]}", 'link', fmt, b=b)
            elif formula:
                f = formula(c, y)
                if f: put(rd, f'{c}{r}', f, fmt=fmt, b=b, i=i)
    prev = {'FY2027E': 'D', 'FY2028E': 'E', 'FY2029E': 'F'}
    row(15, 'Revenue', 'Revenue', b=True); row(16, '   y/y growth', fmt=F_PCT, i=True, formula=lambda c, y: f'={c}15/{prev[y]}15-1' if y in prev else None)
    row(17, 'EBITDA (adj)', 'EBITDA (adj)'); row(18, '   margin', fmt=F_PCT, i=True, formula=lambda c, y: f'={c}17/{c}15')
    row(19, 'EBIT (adj)', 'EBIT (adj)'); row(20, 'Net income (adj)', 'Net income (adj)'); row(21, 'EPS (adj), $', 'EPS (adj), $', fmt='0.00')
    row(22, 'Cash flow from operations', 'Cash flow from operations'); row(23, 'Capital expenditure', 'Capital expenditure')
    row(24, 'Unlevered cash flow = CFO − capex', fmt=F_INT, b=True, formula=lambda c, y: f'={c}22+{c}23', note="Two published lines. Barclays' own 'free cash flow' line (row 26) is ~$1bn a year higher and undefined in the text; selector D37")
    row(25, '   cash-flow margin on revenue', fmt=F_PCT, i=True, formula=lambda c, y: f'={c}24/{c}15')
    row(26, "Barclays' free cash flow line (alternative)", 'Free cash flow (Barclays line; definition not stated)')
    row(27, 'Cash flow used', fmt=F_INT, b=True, formula=lambda c, y: f'=IF($D$37=2,{c}26,{c}24)', years=('FY2027E', 'FY2028E'))
    row(28, 'Discount period, years from 30 Sep 2026 (mid-year; DCF convention)', fmt='0.00', formula=lambda c, y: f"=DCF!{'I' if y == 'FY2027E' else 'J'}66", years=('FY2027E', 'FY2028E'))
    row(29, 'Discount factor', fmt='0.0000', formula=lambda c, y: f'=1/(1+$D$12)^{c}28', years=('FY2027E', 'FY2028E'))
    row(30, 'PV of cash flow', fmt=F_INT, b=True, formula=lambda c, y: f'={c}27*{c}29', years=('FY2027E', 'FY2028E'))
    section(rd, 32, 'C. Valuation and the lever', ['Value', 'Note'])
    V = [(33, 'PV of explicit cash flows, FY27E–FY28E', '=SUM(E30:F30)', F_INT, ''), (34, 'Exit EV/EBITDA multiple on FY2028E EBITDA (the lever; solved so that H41 = 0)', None, '0.00', 'Solved at build by bisection; Goal Seek: set H41 to 0 by changing D34'),
         (35, 'Terminal value = multiple × FY2028E EBITDA', '=D34*F17', F_INT, ''), (36, 'Discount period to end FY2028 (31 Jul 2028)', '=F28+0.42', '0.00', 'Mid-year period plus half a year'), (37, 'Cash-flow definition: 1 = CFO − capex (base); 2 = Barclays FCF line', 1, '0', 'TOGGLE'),
         (38, 'PV of terminal value', '=D35/(1+D12)^D36', F_INT, ''), (39, 'Enterprise value', '=D33+D38', F_INT, ''), (40, 'Equity value = EV + cash − debt − NCI', '=D39-D8-D9-D10', F_INT, '')]
    for r, lab, f, fmt, note in V:
        label(rd, r, lab, note=note, b=(r in (34, 39)))
        if f is not None: put(rd, f'D{r}', f, 'toggle' if r == 37 else 'formula', fmt, b=(r == 39))
    label(rd, 41, 'Implied share price  |  current  |  implied − current (Goal Seek to 0)  |  premium / (discount)', b=True)
    put(rd, 'D41', '=D40/D6', fmt=F_USD + '.00', b=True); put(rd, 'F41', '=D5', fmt=F_USD + '.00'); put(rd, 'H41', '=D41-F41', fmt=F_USD + '.00', b=True); put(rd, 'J41', '=D41/F41-1', fmt=F_PCT)
    section(rd, 43, 'D. What the price implies, read two ways', ['Value', 'Note'])
    W = [(44, 'Lever 1: market-implied exit multiple on FY2028E EBITDA, Barclays path, CFO − capex', '=D34', '0.0', 'Barclays trades the stock at 12.8x FY2028E in its own table (D Barclays line 183)'),
         (45, "Barclays' own multiple behind the $25 target (10x FY2026E EBITDA)", 10, '0.0', 'Report line 468; 20-year range 7x–25x per Barclays'),
         (46, "Lever 2: uniform revenue-growth uplift on Barclays' path needed to reach today's price at Barclays' 10x on FY2028E (EBITDA and cash-flow margins held)", None, F_PCT, 'Solved at build; points of extra growth a year on top of Barclays\' 2.2% / 3.8%'),
         (47, 'Implied FY2028E revenue under lever 2', None, F_INT, 'Barclays FY2028E 4,948'), (48, "Our known-facts FY27E total revenue (Scenarios case 1), for comparison with Barclays FY2027E 4,768", f"=Scenarios!{ACOL[2027]}{ctx['case_rows'][2]+2}", F_INT, '')]
    for r, lab, f, fmt, note in W:
        label(rd, r, lab, note=note, b=(r in (44, 46)))
        if f is not None: put(rd, f'D{r}', f, 'link' if isinstance(f, str) and '!' in f else ('input' if isinstance(f, (int, float)) else 'formula'), fmt, b=(r in (44, 46)))
    put(rd, 'B50', "Reading: the Street's bear and the market share the same operating path; the price is a terminal-multiple disagreement of about two turns on FY2028E EBITDA. A revenue shortfall against Barclays' path is therefore a shortfall against a path the market already pays a premium multiple for.", 'note')
    section(rd, 52, 'E. Sensitivity: implied share price by exit multiple (FY2028E EBITDA) and WACC', ['8x', '10x', '12x', '14x', '16x'])
    for j, m in enumerate((8, 10, 12, 14, 16)): put(rd, f'{L(4+j)}52', m, 'input', '0')
    for k, w in enumerate((0.0775, 0.08725, 0.0975)):
        r = 53 + k; label(rd, r, f'WACC {w:.3%}'.replace('.000%', '%'), i=True); put(rd, f'C{r}', w, 'input', F_PCT2)
        for j in range(5): c = L(4 + j); put(rd, f'{c}{r}', f'=((E27/(1+$C{r})^E28+F27/(1+$C{r})^F28+{c}$52*$F$17/(1+$C{r})^$D$36)-$D$8-$D$9-$D$10)/$D$6', fmt=F_USD + '.00')
    rd.freeze_panes = 'D5'
    # ---------------- solve the two levers in Python with the same arithmetic
    price, shares, cash, debt, nci, wacc = 29.95, 925.811482, 4489.802, 88.367, 16.585, 0.08725
    ev_today = price * shares - cash + debt + nci
    rev = B['Revenue'][1]; ebitda = B['EBITDA (adj)'][1]; cfo = B['Cash flow from operations'][1]; capex = B['Capital expenditure'][1]
    per = [0.42, 1.42]; cf = [cfo[1] + capex[1], cfo[2] + capex[2]]
    pv = sum(c / (1 + wacc) ** p for c, p in zip(cf, per)); mult = (ev_today - pv) * (1 + wacc) ** (per[-1] + 0.42) / ebitda[2]
    put(rd, 'D34', round(mult, 4), 'toggle', '0.00', b=True)
    g = [rev[1] / rev[0] - 1, rev[2] / rev[1] - 1]; m_cf = [cf[0] / rev[1], cf[1] / rev[2]]; m_eb = ebitda[2] / rev[2]
    def ev_at(u):
        r = rev[0]; tot = 0.0; rs = []
        for k in range(2): r = r * (1 + g[k] + u); rs.append(r); tot += r * m_cf[k] / (1 + wacc) ** per[k]
        return tot + 10 * rs[-1] * m_eb / (1 + wacc) ** (per[-1] + 0.42), rs[-1]
    lo, hi = -0.5, 1.5
    for _ in range(80):
        mid = (lo + hi) / 2; lo, hi = (mid, hi) if ev_at(mid)[0] < ev_today else (lo, mid)
    put(rd, 'D46', round((lo + hi) / 2, 5), 'toggle', F_PCT, b=True); put(rd, 'D47', round(ev_at((lo + hi) / 2)[1], 1), 'formula', F_INT)
    ctx['rdcf'] = dict(ev_today=ev_today, implied_multiple=mult, uplift=(lo + hi) / 2)
    # ---------------- owner edits captured from the 2 Oct saved copy (so they survive rebuilds)
    wb['DCF']['H92'].value = 8   # owner set the DCF exit EV/EBITDA multiple to 8 (was 12.5 in v1)
    put(wb['DCF'], 'P92', 'Owner edit, 2 Oct 2026: exit multiple set to 8x (v1 had 12.5x); captured in build so it persists', 'note')
