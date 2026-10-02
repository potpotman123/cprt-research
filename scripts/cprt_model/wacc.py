"""WACC and effective-tax build in the owner's Reverse DCF tab (columns R-X); the DCF's WACC and tax cells link here; the DCF's old WACC rows are retired."""
from .common import *
def build(wb, ctx):
    rd = wb['Reverse DCF']; d = ctx['d10k_rows']; F = ctx['F']
    for c in 'RSTUVWX': rd.column_dimensions[c].width = 14
    rd.column_dimensions['R'].width = 58
    def lab(r, text, b=False, i=False, note=''):
        put(rd, f'R{r}', text, 'label', b=b, i=i)
        if note: put(rd, f'X{r}', note, 'note')
    def bar(r, text):
        put(rd, f'R{r}', text, 'label', b=True)
        for c in 'RSTUVWX': rd[f'{c}{r}'].fill = fill(BLUE); rd[f'{c}{r}'].font = font(C_WHITE, b=True)
    bar(4, 'WACC build (bottom-up; feeds DCF!H88)'); put(rd, 'S4', 'Value', 'label', b=True); put(rd, 'T4', 'Label', 'label', b=True)
    lab(5, 'Current share price (Cover key statistics, D6)', note='Cover D6 — the one typed price in the workbook'); put(rd, 'S5', '=Cover!$D$6', 'link', F_USD + '.00')
    lab(6, 'Fully diluted shares, mn (Cover key statistics, D15)', note='Cover D15: basic + treasury-method options + RSUs (10-K Note 12)'); put(rd, 'S6', '=Cover!$D$15', 'link', '0.0')
    lab(7, 'Market value of equity ($m) (Cover D10)', b=True); put(rd, 'S7', '=Cover!$D$10', 'link', F_INT, b=True)
    lab(8, 'Debt: lease liabilities ($m), no funded debt (Cover D13)', note='Cover D13 ← 3SM balance sheet; revolver undrawn'); put(rd, 'S8', '=Cover!$D$13', 'link', F_INT)
    lab(9, 'Weight of equity / weight of debt'); put(rd, 'S9', '=S7/(S7+S8)', fmt=F_PCT2); put(rd, 'T9', '=S8/(S7+S8)', fmt=F_PCT2)
    lab(11, 'Risk-free rate: 10-year US Treasury par yield, 1 Oct 2026', note='VERIFIED — US Treasury daily par yield curve, raw/discovery_2026-10-02/ust_yield_curve_2026.csv (row 10/01/2026, 10 Yr)'); put(rd, 'S11', 0.0524, 'input', F_PCT2); put(rd, 'T11', 'VERIFIED', 'note')
    lab(12, 'Equity risk premium: United States, Damodaran, January 2026', note='VERIFIED — Damodaran country risk premiums table (Aa1; mature-market 4.23% + 0.23% CRP), raw/discovery_2026-10-02/damodaran_ctryprem.html'); put(rd, 'S12', 0.0446, 'input', F_PCT2); put(rd, 'T12', 'VERIFIED', 'note')
    lab(13, 'Beta — industry evidence (Damodaran, data as of January 2026): levered / unlevered / cash-corrected unlevered', b=True, note='VERIFIED — raw/discovery_2026-10-02/damodaran_betas.html')
    for j, h in enumerate(['Levered', 'Unlevered', 'Cash-corrected']): put(rd, f'{L(19+j)}13', h, 'label', b=True)
    betas = [('Business & Consumer Services (155 firms)', 0.89, 0.77, 0.81), ('Retail (Automotive) (34 firms)', 0.94, 0.70, 0.71), ('Auto Parts (35 firms)', 1.34, 1.02, 1.13), ('Transportation (19 firms)', 0.86, 0.68, 0.71), ('Total market (5,994 firms)', 0.91, 0.72, 0.76)]
    for i, (n, lv, ul, cc) in enumerate(betas):
        r = 14 + i; lab(r, n); put(rd, f'S{r}', lv, 'input', '0.00'); put(rd, f'T{r}', ul, 'input', '0.00'); put(rd, f'U{r}', cc, 'input', '0.00')
    lab(19, 'Peer company betas (5-year monthly): RB Global, OPENLANE, ACV Auctions, Carvana, Copart', note='NOT OBTAINED — price downloads refused by the only permitted free source\'s robots file; paste CapIQ or Bloomberg values here (dated) to override the industry beta')
    for j, n in enumerate(['RBA', 'KAR', 'ACVA', 'CVNA', 'CPRT']): put(rd, f'{L(19+j)}19', n, 'label', i=True)
    lab(20, 'Selected unlevered beta (default: average of the two closest industries, cash-corrected)', b=True, note='ASSUMED choice of industries; Copart is an auction-services business with retail-automotive exposure'); put(rd, 'S20', '=AVERAGE(U14,U15)', fmt='0.00', b=True); put(rd, 'T20', 'ASSUMED', 'note')
    lab(21, 'Relevered beta = βu × (1 + (1 − t) × D/E)'); put(rd, 'S21', '=S20*(1+(1-S33)*S8/S7)', fmt='0.00')
    lab(22, 'Cost of equity (CAPM) = Rf + β × ERP', b=True); put(rd, 'S22', '=S11+S21*S12', fmt=F_PCT2, b=True)
    lab(23, 'Pre-tax cost of debt (revolver pricing proxy; weight ≈ 0)', note='ASSUMED: 10-K describes the $1,250m unsecured revolver maturing 23 Jan 2031 without the margin; SOFR + 1.0–1.5% proxy'); put(rd, 'S23', 0.0575, 'input', F_PCT2); put(rd, 'T23', 'ASSUMED', 'note')
    lab(24, 'After-tax cost of debt'); put(rd, 'S24', '=S23*(1-S33)', fmt=F_PCT2)
    lab(25, 'WACC = E/V × Ke + D/V × Kd(1 − t)   → DCF!H88', b=True); put(rd, 'S25', '=S9*S22+T9*S24', fmt=F_PCT2, b=True)
    lab(26, 'Memo: DCF\'s previous inputs — risk-free 4.21%, beta 1.05, ERP 4.30% → 8.725%', i=True)
    bar(28, 'Effective tax rate build (feeds the DCF tax-rate row)'); put(rd, 'S28', 'Value', 'label', b=True); put(rd, 'T28', 'Label', 'label', b=True)
    lab(29, 'US federal statutory rate', note='10-K MD&A'); put(rd, 'S29', 0.21, 'input', F_PCT2); put(rd, 'T29', 'VERIFIED', 'note')
    lab(30, '(+) State income taxes: $21.5m ÷ pre-tax income $1,835m', note='10-K MD&A Income Taxes; pre-tax income from the income statement'); put(rd, 'S30', f"='D 10-K FY26'!E{d['Tax reconciliation FY2026 ($m): FDII benefit / excess stock-option benefit / state taxes']}/1834.977", fmt=F_PCT2); put(rd, 'T30', 'VERIFIED', 'note')
    lab(31, '(−) FDII deduction: $46.7m ÷ pre-tax income', note='10-K MD&A; set by federal tax law, check the FY27 deduction rate'); put(rd, 'S31', f"='D 10-K FY26'!C{d['Tax reconciliation FY2026 ($m): FDII benefit / excess stock-option benefit / state taxes']}/1834.977", fmt=F_PCT2); put(rd, 'T31', 'VERIFIED', 'note')
    lab(32, '(−) Excess tax benefit on option exercises: $6.6m (FY25: $36.7m); excluded from the forward rate because it depends on the share price', note='10-K MD&A'); put(rd, 'S32', f"='D 10-K FY26'!D{d['Tax reconciliation FY2026 ($m): FDII benefit / excess stock-option benefit / state taxes']}/1834.977", fmt=F_PCT2); put(rd, 'T32', 'VERIFIED', 'note')
    lab(33, 'Structural effective tax rate (statutory + state − FDII)   → DCF tax rows', b=True); put(rd, 'S33', '=S29+S30+S31', fmt=F_PCT2, b=True)
    lab(34, 'Reported effective rate FY2026 / FY2025', i=True); put(rd, 'S34', f"='D 10-K FY26'!C{d['Effective tax rate FY2026 / FY2025']}", 'link', F_PCT2); put(rd, 'T34', f"='D 10-K FY26'!D{d['Effective tax rate FY2026 / FY2025']}", 'link', F_PCT2)
    lab(35, 'Cash taxes paid ÷ pre-tax income, FY2026 / FY2025', i=True, note='Supplemental cash flow'); put(rd, 'S35', f"='D 10-K FY26'!C{d['Income taxes paid, net of refunds ($m)']}/1834.977", fmt=F_PCT2); put(rd, 'T35', f"='D 10-K FY26'!D{d['Income taxes paid, net of refunds ($m)']}/1895.581", fmt=F_PCT2)
    lab(36, 'Barclays-implied rate FY2027E (1 − adj. net income ÷ adj. pre-tax)', i=True); b = ctx['barclays_rows']; put(rd, 'S36', f"=1-'D Barclays'!E{b['Net income (adj)']}/'D Barclays'!E{b['Pre-tax income (adj)']}", 'link', F_PCT2)
    # ---- DCF: retire the old WACC rows, link WACC and the forward tax rate to this build
    dcf = wb['DCF']
    for r in range(79, 88):
        for c in range(3, 16): dcf.cell(r, c).value = None
    put(dcf, 'B79', 'WACC is built bottom-up on the Reverse DCF tab, columns R–X (risk-free, ERP, industry betas, capital structure, tax)', 'note')
    put(dcf, 'H88', "='Reverse DCF'!S25", 'link', F_PCT2, b=True); put(dcf, 'P88', 'Link to the WACC build (Reverse DCF R–X)', 'note')
    for c in 'IJKLM': put(dcf, f'{c}38', "='Reverse DCF'!$S$33", 'link', F_PCT)
    put(dcf, 'P38', 'FY27+ = structural effective rate from the tax build (Reverse DCF R28–R36)', 'note')

    relink = {'H45': ('=DCF!H107', '=Cover!D12'), 'H46': ('=DCF!H108', '=-Cover!D13'), 'H47': ('=DCF!H109', '=-Cover!D14'), 'H50': ('=DCF!H112', '=Cover!D15'), 'H52': ('=DCF!H118', '=Cover!D6')}
    for ref, (old, new) in relink.items():
        if rd[ref].value == old: put(rd, ref, new, 'link')
    v = rd['H61'].value
    if isinstance(v, str) and 'DCF!H118' in v:
        rd['H61'].value = v.replace('DCF!H118', 'Cover!D6').replace('DCF!H112', 'Cover!D15').replace('DCF!H107', 'Cover!D12').replace('-DCF!H108', '+Cover!D13').replace('-DCF!H109', '+Cover!D14'); WRITTEN.add(('Reverse DCF', 'H61'))
