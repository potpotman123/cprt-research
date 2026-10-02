"""Cover (Via-style): price, target, implied upside, key statistics, fully diluted shares, legend, tab map."""
from .common import *
def build(wb, ctx):
    ws = wb.create_sheet('Cover'); tab_color(ws, NAVY); setup(ws, label_w=48, ncols=4, notes_col='H'); ws.column_dimensions['D'].width = 16; ws.column_dimensions['E'].width = 3; ws.column_dimensions['F'].width = 40; ws.column_dimensions['G'].width = 70
    d = ctx['d10k_rows']
    put(ws, 'B2', 'Copart, Inc. (NASDAQ: CPRT)', 'label', b=True); ws['B2'].font = font(NAVY, b=True, sz=18, u='single')
    put(ws, 'B3', 'Revenue architecture, three-statement model, DCF and reverse DCF — Harvard pitch team, October 2026', 'note'); ws['B3'].font = font(C_NOTE, i=True, sz=12)
    section(ws, 5, 'Ticker', ['NASDAQ: $CPRT'])
    rows = [(6, 'Current price (26 Sep 2026)', '=DCF!H118', F_USD + '.00', 'input'), (7, 'Price target (DCF implied share price, selected case)', '=DCF!H113', F_USD + '.00', 'link'), (8, 'Implied upside / (downside)', '=D7/D6-1', F_PCT, 'formula'),
            (10, 'Market capitalisation ($m)', '=D6*D15', F_INT, 'formula'), (11, 'Enterprise value ($m)', '=D10-DCF!H107-DCF!H108-DCF!H109', F_INT, 'formula'), (12, 'Cash & held-to-maturity securities, 31 Jul 2026 ($m)', '=DCF!H107', F_INT, 'link'), (13, 'Total debt (finance leases), 31 Jul 2026 ($m)', '=-DCF!H108', F_INT, 'link'),
            (15, 'Fully diluted shares (mn) = basic + treasury-method options + RSUs', '=D16+D17+D18', '0.0', 'formula'), (16, 'Basic shares outstanding, 31 Jul 2026 (mn)', f"='D 10-K FY26'!C{d['Common shares issued and outstanding, 31 Jul 2026']}", '0.0', 'link'),
            (17, 'Net shares from options, treasury method (mn): N × max(0, 1 − K/P)', f"='D 10-K FY26'!C{d['Stock options outstanding, 31 Jul 2026 (thousands) / weighted-average exercise price ($) / remaining term (yrs) / intrinsic value ($000)']}/1000*MAX(0,1-'D 10-K FY26'!D{d['Stock options outstanding, 31 Jul 2026 (thousands) / weighted-average exercise price ($) / remaining term (yrs) / intrinsic value ($000)']}/D6)", '0.00', 'formula'),
            (18, 'Unvested RSUs (mn)', f"=IF(ISNUMBER('D 10-K FY26'!C{d['Restricted stock units unvested, 31 Jul 2026 (thousands) / weighted-average grant-date fair value ($)']}),'D 10-K FY26'!C{d['Restricted stock units unvested, 31 Jul 2026 (thousands) / weighted-average grant-date fair value ($)']}/1000,0)", '0.00', 'formula'),
            (20, 'FY2026A revenue ($m)', '=RPM!H6', F_INT, 'link'), (21, 'FY2026A adjusted EBITDA ($m)', '=DCF!H31', F_INT, 'link'), (22, 'FY2027E legacy service revenue, selected case ($m)', '=RPM!I10', F_INT, 'link'), (23, 'Δ to JPMorgan FY27E service revenue ($m)', '=RPM!D50', F_INT, 'link'),
            (25, 'WACC (bottom-up build, Reverse DCF R–X)', "='Reverse DCF'!S25", F_PCT2, 'link'), (26, 'Structural effective tax rate', "='Reverse DCF'!S33", F_PCT2, 'link')]
    for r, lab, f, fmt, kind in rows:
        label(ws, r, lab, b=(r in (6, 7, 8, 15))); put(ws, f'D{r}', f, kind, fmt, b=(r in (6, 7, 8, 15)))
    put(ws, 'H6', 'DCF tab; price as of 26 Sep 2026', 'note'); put(ws, 'H17', '10-K Note 12: 12.759m options at a $24.19 weighted-average exercise price', 'note'); put(ws, 'H18', 'RSU count not parsed from the filing text; enter from Note 12 on D 10-K FY26', 'note'); put(ws, 'H16', '10-K Note 12: 926,298,293 shares at 31 Jul 2026', 'note')
    put(ws, 'B9', 'Key statistics', 'label', b=True); ws['B9'].font = font(NAVY, b=True, sz=14)
    put(ws, 'F5', 'Colour and label legend', 'label', b=True)
    for r, (k, t) in enumerate([('input', 'Blue: typed input, with label and source'), ('formula', 'Black: formula'), ('link', 'Green: link from another tab'), ('toggle', 'Red: toggle, probability or scenario selector'), ('engine', 'Purple: value pasted from the Python engine'), ('note', 'Grey italic: notes and sources')], start=6): put(ws, f'F{r}', t, k)
    put(ws, 'F12', 'Labels: VERIFIED · MEASURED · FITTED · CALIBRATED · ASSUMED · UNVERIFIED · ENGINE', 'note')
    put(ws, 'F14', 'Tab map', 'label', b=True)
    tabs = [('Key Drivers', 'the numbers the theses turn on'), ('Summary', 'headline financials, Street Δ, component delta to Street'), ('RPM', 'one-page revenue build; scenario selector in D3'), ('3SM', 'three statements FY22A–FY31E with schedules; feeds the DCF'), ('DCF / Reverse DCF', 'valuation; WACC and tax build in Reverse DCF columns R–X'), ('E1–E6', 'engines: fleet, claims, carriers, aftermarket, fees, branches'), ('Scenarios / Street', 'seven cases on one base; broker assumptions'), ('Sources / Checks', 'every input with its source; live checks'), ('D …', 'data tabs with sources and dates')]
    for r, (t, dsc) in enumerate(tabs, start=15): put(ws, f'F{r}', t, 'label', b=True); put(ws, f'G{r}', dsc, 'note')
    ws.freeze_panes = None
