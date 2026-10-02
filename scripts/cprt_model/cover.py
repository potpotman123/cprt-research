"""Cover (Via-style): price, target, implied upside, key statistics (the hub every valuation tab reads), fully diluted shares, legend, tab map."""
from .common import *
def build(wb, ctx):
    ws = wb.create_sheet('Cover'); tab_color(ws, NAVY); setup(ws, label_w=66, ncols=2, notes_col='H'); NOTES_COL['Cover'] = 'H'
    ws.column_dimensions['E'].width = 3; ws.column_dimensions['F'].width = 22; ws.column_dimensions['G'].width = 58; ws.column_dimensions['H'].width = 70
    d = ctx['d10k_rows']; T = ctx['tsm_rows']; dk = lambda pre: next(k for k in d if k.startswith(pre)); D10 = lambda pre, col='C': f"'D 10-K FY26'!{col}{d[dk(pre)]}"
    pres = ctx.get('preserve', {}); price = pres.get('price', 29.95); plabel = pres.get('price_label') or 'Current price (26 Sep 2026)'
    put(ws, 'B2', 'Copart, Inc. (NASDAQ: CPRT)', 'label', b=True); ws['B2'].font = font(NAVY, b=True, sz=18, u='single')
    put(ws, 'B3', 'Revenue architecture, three-statement model, DCF and reverse DCF — Harvard pitch team, October 2026', 'note'); ws['B3'].font = font(C_NOTE, i=True, sz=12)
    section(ws, 5, 'Ticker', ['NASDAQ: $CPRT'])
    rows = [(6, plabel, price, F_USD + '.00', 'input', 'Owner-entered close — the one typed price in the workbook. DCF H118, the WACC build (Reverse DCF S5) and the Summary read this cell; a rebuild keeps whatever is typed here'),
            (7, 'Price target (DCF implied share price, selected case)', '=DCF!H113', F_USD + '.00', 'link', 'DCF equity bridge on the Cover statistics and fully diluted shares'),
            (8, 'Implied upside / (downside)', '=D7/D6-1', F_PCT, 'formula', ''),
            (10, 'Market capitalisation ($m)', '=D6*D15', F_INT, 'formula', 'Price × fully diluted shares; feeds the WACC build (Reverse DCF S7)'),
            (11, 'Enterprise value ($m)', '=D10-D12+D13+D14', F_INT, 'formula', 'Market cap − cash & HTM + lease debt + non-controlling interest'),
            (12, 'Cash & held-to-maturity securities, 31 Jul 2026 ($m)', f"={D10('Cash, cash equivalents')}+{D10('Investment in held to maturity')}", F_INT, 'link', '10-K balance sheet (D 10-K FY26: 1,907.9 + 2,581.9); feeds DCF H107'),
            (13, 'Debt: lease liabilities, 31 Jul 2026 ($m)', f"='3SM'!H{T['debt']}", F_INT, 'link', '3SM balance sheet (PitchBook / 10-K): 15.2 current + 73.2 non-current; no funded debt. Feeds DCF H108 and the WACC build (S8)'),
            (14, 'Non-controlling interest, 31 Jul 2026 ($m)', f"='3SM'!H{T['ncieq']}", F_INT, 'link', '3SM balance sheet; feeds DCF H109'),
            (15, 'Fully diluted shares (mn) = basic + treasury-method options + RSUs', '=D16+D17+D18', '0.0', 'formula', 'Feeds DCF H112 and the WACC build (Reverse DCF S6)'),
            (16, 'Basic shares outstanding, 31 Jul 2026 (mn)', f"={D10('Common shares issued')}", '0.0', 'link', '10-K Note 12: 926,298,293 shares at 31 Jul 2026'),
            (17, 'Net shares from options, treasury method (mn): N × max(0, 1 − K/P)', f"={D10('Stock options outstanding')}/1000*MAX(0,1-{D10('Stock options outstanding', 'D')}/D6)", '0.00', 'formula', '10-K Note 12: 12.759m options at a $24.19 weighted-average exercise price; P = the price in D6'),
            (18, 'Unvested RSUs (mn)', f"=IF(ISNUMBER({D10('Restricted stock units unvested')}),{D10('Restricted stock units unvested')}/1000,0)", '0.00', 'formula', 'RSU count not parsed from the filing text; enter it from Note 12 on D 10-K FY26'),
            (19, 'EV / FY2026A adjusted EBITDA (x)', '=D11/D22', F_X, 'formula', ''),
            (20, 'Price / FY2026A diluted EPS (x)', f"=D6/'3SM'!H{T['eps']}", F_X, 'formula', '3SM FY2026A diluted EPS'),
            (21, 'FY2026A revenue ($m)', '=RPM!H6', F_INT, 'link', ''),
            (22, 'FY2026A adjusted EBITDA ($m)', f"='3SM'!H{T['ebitda']}", F_INT, 'link', '3SM: EBIT + D&A (Barclays definition)'),
            (23, 'FY2027E legacy service revenue, selected case ($m)', '=RPM!I10', F_INT, 'link', ''),
            (24, 'Δ to JPMorgan FY27E service revenue ($m)', '=RPM!D50', F_INT, 'link', ''),
            (25, 'Selected scenario (dropdown on RPM D3)', '=RPM!D3', '@', 'link', ''),
            (26, 'WACC (bottom-up build, Reverse DCF R–X)', "='Reverse DCF'!S25", F_PCT2, 'link', ''),
            (27, 'Structural effective tax rate', "='Reverse DCF'!S33", F_PCT2, 'link', '')]
    for r, lab, f, fmt, kind, note in rows:
        bold = r in (6, 7, 8, 11, 15); label(ws, r, lab, b=bold); put(ws, f'D{r}', f, kind, fmt, b=bold)
        if note: put(ws, f'H{r}', note, 'note')
    put(ws, 'B9', 'Key statistics — the hub: the DCF bridge, the WACC build and the Summary read these cells', 'label', b=True); ws['B9'].font = font(NAVY, b=True, sz=13)
    put(ws, 'F5', 'Colour and label legend', 'label', b=True)
    for r, (k, t) in enumerate([('input', 'Blue: typed input, with label and source'), ('formula', 'Black: formula'), ('link', 'Green: link from another tab'), ('toggle', 'Red: toggle, probability or scenario selector'), ('note', 'Grey italic: notes and sources')], start=6): put(ws, f'F{r}', t, k)
    put(ws, 'F11', 'Labels: VERIFIED · MEASURED · FITTED · CALIBRATED · ASSUMED · UNVERIFIED · ENGINE', 'note')
    put(ws, 'F12', 'Tab map', 'label', b=True)
    tabs = [('Key Drivers', 'the numbers the theses turn on'), ('Summary', 'headline financials, Street Δ, component delta to Street'), ('RPM', 'one-page revenue build; scenario dropdown in D3'), ('3SM', 'three statements FY22A–FY31E with schedules; feeds the DCF'),
            ('DCF / Reverse DCF', 'valuation; WACC and tax build in Reverse DCF columns R–X'), ('E1–E6', 'engines: fleet, claims, carriers, aftermarket, fees, branches'), ('Scenarios / Street', 'seven cases on one base; broker assumptions'), ('Sources / Checks', 'every input with its source; live checks'), ('D …', 'data tabs with sources and dates')]
    for r, (t, dsc) in enumerate(tabs, start=13): put(ws, f'F{r}', t, 'label', b=True); put(ws, f'G{r}', dsc, 'note')
    ws.freeze_panes = None
    # ---- the DCF equity bridge and current price read the Cover (one cell each)
    dcf = wb['DCF']
    put(dcf, 'H107', '=Cover!D12', 'link'); put(dcf, 'H108', '=-Cover!D13', 'link'); put(dcf, 'H109', '=-Cover!D14', 'link')
    put(dcf, 'B112', 'Fully diluted shares (M) — Cover key statistics', 'label'); put(dcf, 'H112', '=Cover!D15', 'link'); put(dcf, 'H118', '=Cover!D6', 'link')
    put(dcf, 'P107', 'Rows 107–109, 112 and 118 read the Cover key statistics (cash & HTM, lease debt, NCI, fully diluted shares, price)', 'note')
    put(dcf, 'P118', 'Type the price on the Cover (D6), not here', 'note')
    if dcf['H76'].value == "='PB BS (Annual)'!M18/1000": put(dcf, 'H76', '=Cover!D12', 'link'); put(dcf, 'P76', 'Opening cash & HTM from the Cover key statistics', 'note')
