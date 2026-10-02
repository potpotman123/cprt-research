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
    # ---------------- Reverse DCF (Barclays)
    rd = wb.create_sheet('Reverse DCF (Barclays)'); tab_color(rd, NAVY); setup(rd, label_w=58, ncols=8, notes_col='K')
    title(rd, 'Copart, Inc. — Reverse DCF on Barclays\' model (Via-style): Street operating path, one lever solved to today\'s price', "Explicit period = Barclays' three forecast years; cash flow = margin on revenue; terminal = exit multiple on FY2029E EBITDA. Lever: the exit multiple the market pays (solved); alternative lever: uniform growth uplift at Barclays' own 10x. Valuation date 30 Sep 2026, mid-year discounting, FY ends 31 Jul.")
    section(rd, 4, 'A. Market data and capital structure (links to the DCF tab)', ['Value', 'Source'])
    A = [(5, 'Current share price (26 Sep 2026)', '=DCF!H118', F_USD + '.00', 'DCF tab'), (6, 'Shares outstanding, mn (31 Jul 2026)', '=DCF!H112', '0.0', 'DCF tab; Barclays 925.81 (line 57)'),
         (7, 'Market capitalisation', '=D5*D6', F_INT, ''), (8, '(−) Cash & HTM securities, 31 Jul 2026', '=-DCF!H107', F_INT, 'DCF tab'), (9, '(+) Total debt', '=-DCF!H108', F_INT, 'DCF tab'), (10, '(+) Non-controlling interest', '=-DCF!H109', F_INT, 'DCF tab'),
         (11, 'Enterprise value today', '=D7+D8+D9+D10', F_INT, ''), (12, 'WACC (cost of equity; no net debt)', '=DCF!H88', F_PCT2, 'DCF tab: 4.21% risk-free + 1.05 beta × 4.30% ERP')]
    for r, lab, f, fmt, note in A: label(rd, r, lab, note=note, b=(r in (7, 11))); put(rd, f'D{r}', f, 'link' if 'DCF' in f else 'formula', fmt, b=(r in (7, 11)))
    section(rd, 14, "B. Barclays' operating path (green = D Barclays)", YEARS)
    br = ctx['barclays_rows']; col = {y: L(4 + j) for j, y in enumerate(YEARS)}
    def row(r, lab, key=None, fmt=F_INT, b=False, formula=None, i=False, note=''):
        label(rd, r, lab, b=b, i=i, note=note)
        for j, y in enumerate(YEARS):
            c = col[y]
            if key: put(rd, f'{c}{r}', f"='D Barclays'!{c}{br[key]}", 'link', fmt, b=b)
            elif formula: put(rd, f'{c}{r}', formula(c, j), fmt=fmt, b=b, i=i)
    row(15, 'Revenue', 'Revenue', b=True); row(16, '   y/y growth', fmt=F_PCT, i=True, formula=lambda c, j: f'={c}15/{col[YEARS[j-1]]}15-1' if j else None)
    row(17, 'EBITDA (adj)', 'EBITDA (adj)'); row(18, '   margin', fmt=F_PCT, i=True, formula=lambda c, j: f'={c}17/{c}15')
    row(19, 'EBIT (adj)', 'EBIT (adj)'); row(20, 'Net income (adj)', 'Net income (adj)'); row(21, 'EPS (adj), $', 'EPS (adj), $', fmt='0.00')
    row(22, 'Cash flow from operations', 'Cash flow from operations'); row(23, 'Capital expenditure', 'Capital expenditure')
    row(24, 'Unlevered cash flow, base = CFO − capex', fmt=F_INT, b=True, formula=lambda c, j: f'={c}22+{c}23', note='Standard definition from two published lines; Barclays\' own FCF line is far higher and undefined, so it is the alternative (row 26)')
    row(25, '   cash-flow margin on revenue', fmt=F_PCT, i=True, formula=lambda c, j: f'={c}24/{c}15')
    row(26, "Barclays' free cash flow line (alternative)", 'Free cash flow (Barclays line; definition not stated)', note='Exceeds CFO − capex by ~$1bn a year; not used unless the selector in D40 is 2')
    row(27, 'Cash flow used', fmt=F_INT, b=True, formula=lambda c, j: f'=IF($D$40=2,{c}26,{c}24)')
    row(28, 'Discount period, years from 30 Sep 2026 (mid-year)', fmt='0.00', formula=lambda c, j: f'=DCF!{L(9+j-1)}66' if j else None)
    row(29, 'Discount factor', fmt='0.0000', formula=lambda c, j: f'=1/(1+$D$12)^{c}28' if j else None)
    row(30, 'PV of cash flow', fmt=F_INT, b=True, formula=lambda c, j: f'={c}27*{c}29' if j else None)
    for r in (16, 28, 29, 30): rd[f'D{r}'].value = None
    section(rd, 32, 'C. Valuation and the lever', ['Value', 'Note'])
    V = [(33, 'PV of explicit cash flows, FY27–FY29', '=SUM(E30:G30)', F_INT, ''), (34, 'Exit EV/EBITDA multiple on FY2029E (the lever; solved so that row 43 = 0)', None, '0.00', 'Solved at build by bisection; re-solve with Goal Seek (set D43 to 0 by changing D34) after any input change'),
         (35, 'Terminal value = multiple × FY2029E EBITDA', '=D34*G17', F_INT, ''), (36, 'Discount period to end FY2029 (31 Jul 2029)', '=G28+0.42', '0.00', 'Mid-year period plus half a year'), (37, 'PV of terminal value', '=D35/(1+D12)^D36', F_INT, ''),
         (38, 'Enterprise value', '=D33+D37', F_INT, ''), (39, 'Equity value = EV + cash − debt − NCI', '=D38-D8-D9-D10', F_INT, ''), (40, 'Cash-flow definition selector: 1 = CFO − capex (base); 2 = Barclays FCF line', 1, '0', 'TOGGLE'),
         (41, 'Implied share price', '=D39/D6', F_USD + '.00', ''), (42, 'Current share price', '=D5', F_USD + '.00', ''), (43, 'Implied − current (Goal Seek target 0)', '=D41-D42', F_USD + '.00', ''), (44, 'Premium / (discount) to current', '=D41/D42-1', F_PCT, '')]
    for r, lab, f, fmt, note in V:
        label(rd, r, lab, note=note, b=(r in (34, 38, 41, 43)))
        if f is not None: put(rd, f'D{r}', f, 'toggle' if r == 40 else 'formula', fmt, b=(r in (38, 41, 43)))
    section(rd, 46, 'D. What the price implies, read two ways', ['Value', 'Note'])
    W = [(47, 'Market-implied exit multiple on FY2029E EBITDA (Barclays path, CFO − capex)', '=D34', '0.0', 'Lever 1'),
         (48, "Barclays' own multiple (PT $25 = 10x FY2026E EBITDA)", 10, '0.0', 'Report line 468'),
         (49, 'Barclays EV/EBITDA at $30.75, FY2026A / FY2029E', "='D Barclays'!D21", '0.0', "Barclays' own table (line 183); FY2029E in G21"),
         (50, "Lever 2: uniform revenue-growth uplift on Barclays' path needed to reach today's price at Barclays' 10x (FY29E EBITDA margin held)", None, F_PCT, 'Solved at build; points of extra growth a year on top of Barclays\' 1.5% / 3.8% / 3.6%'),
         (51, 'Implied FY2029E revenue under lever 2', None, F_INT, ''), (52, "Our model's known-facts FY27 total revenue (Scenarios case 1)", f"=Scenarios!{ACOL[2027]}{ctx['case_rows'][2]+2}", F_INT, 'For comparison with Barclays FY2027E 4,768'),
         (53, 'Reading: the market pays a higher terminal multiple than the Underweight, on the same operating path; the revenue and margin path itself is not in dispute between the Street\'s bear and the price', None, None, '')]
    for r, lab, f, fmt, note in W:
        label(rd, r, lab, note=note, b=(r in (47, 50)))
        if f is not None: put(rd, f'D{r}', f, 'link' if isinstance(f, str) and ("'" in f or '!' in f) else ('input' if isinstance(f, (int, float)) else 'formula'), fmt, b=(r in (47, 50)))
    rd.freeze_panes = 'D5'
    # ---------------- solve the two levers in Python with the same arithmetic as the sheet
    price, shares, cash, debt, nci, wacc = 29.95, 925.811482, 4489.802, 88.367, 16.585, 0.08725
    ev_today = price * shares - cash + debt + nci
    rev = B['Revenue'][1]; ebitda = B['EBITDA (adj)'][1]; cfo = B['Cash flow from operations'][1]; capex = B['Capital expenditure'][1]
    per = [0.42, 1.42, 2.42]; cf = [cfo[j] + capex[j] for j in (1, 2, 3)]
    pv = sum(c / (1 + wacc) ** p for c, p in zip(cf, per)); tv_pv_needed = ev_today - pv; mult = tv_pv_needed * (1 + wacc) ** (per[-1] + 0.42) / ebitda[3]
    put(rd, 'D34', round(mult, 4), 'toggle', '0.00', b=True)
    # lever 2: uplift u to growth so that EV at 10x FY29 EBITDA (margin held at Barclays FY29) + PV of CF (cf margin held) equals EV today
    g = [rev[j] / rev[j - 1] - 1 for j in (1, 2, 3)]; m_cf = [cf[k] / rev[k + 1] for k in range(3)]; m_eb = ebitda[3] / rev[3]
    def ev_at(u):
        r = rev[0]; tot = 0.0; rs = []
        for k in range(3): r = r * (1 + g[k] + u); rs.append(r); tot += r * m_cf[k] / (1 + wacc) ** per[k]
        return tot + 10 * rs[-1] * m_eb / (1 + wacc) ** (per[-1] + 0.42), rs[-1]
    lo, hi = -0.5, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2; lo, hi = (mid, hi) if ev_at(mid)[0] < ev_today else (lo, mid)
    put(rd, 'D50', round((lo + hi) / 2, 5), 'toggle', F_PCT, b=True); put(rd, 'D51', round(ev_at((lo + hi) / 2)[1], 1), 'formula', F_INT)
    ctx['rdcf'] = dict(ev_today=ev_today, implied_multiple=mult, uplift=(lo + hi) / 2)
