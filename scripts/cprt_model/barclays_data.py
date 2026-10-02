"""D Barclays: Barclays' published model (11 Sep 2026) as a data tab. Reverse DCF itself is owner-authored and not rebuilt."""
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
