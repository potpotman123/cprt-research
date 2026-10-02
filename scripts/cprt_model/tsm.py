"""3SM: Via-style three-statement model, FY2022A–FY2031E. Revenue from the RPM; facility cost = fee units × cost per unit (volume-driven
gross margin); every other line follows Barclays (11 Sep 2026) where it publishes one and Copart's FY2026 actual ratio, held, where it does not.
FY2030–31 extend Barclays' FY2029 ratios (no broker projects FY2030); FY2031 is carried only because the owner's DCF ends there."""
from .common import *
YEARS = list(range(2022, 2032)); HIST = [y for y in YEARS if y <= 2026]; PROJ = [y for y in YEARS if y >= 2027]
YC = {y: L(4 + i) for i, y in enumerate(YEARS)}                    # D..M  (same letters as RPM and DCF)
PBC = {2026: 'M', 2025: 'N', 2024: 'O', 2023: 'P', 2022: 'Q'}      # PitchBook annual tabs
BC = {2026: 'D', 2027: 'E', 2028: 'F', 2029: 'G'}                  # D Barclays (C holds the line label)
D10C = {2026: 'C', 2025: 'D', 2024: 'E'}; D10C24 = {2024: 'C', 2023: 'D', 2022: 'E'}
NOTES = 'O'
def build(wb, ctx):
    ws = wb.create_sheet('3SM'); tab_color(ws, NAVY); setup(ws, label_w=62, ncols=10, notes_col=NOTES); NOTES_COL['3SM'] = NOTES
    title(ws, 'Copart, Inc. — Three-statement model (3SM), FY2022A–FY2031E ($M; fiscal year ends 31 July)',
          'Revenue = RPM (selected case). Facility operations = fee units × cost per unit. Other lines: Barclays 11 Sep 2026 where published, else FY2026 actual ratio held. Blue = input, black = formula, green = link, red = selector. History = PitchBook / 10-K.')
    header(ws, 4, None, hist_span=(4, 8), proj_span=(9, 13), notes_col=NOTES)
    b = ctx['barclays_rows']; d = ctx['d10k_rows']
    bk = lambda pre: next(k for k in b if k.startswith(pre)); dk = lambda pre: next(k for k in d if k.startswith(pre))
    B = lambda pre, fy: f"'D Barclays'!{BC[fy]}{b[bk(pre)]}"
    D10 = lambda pre, col: f"'D 10-K FY26'!{col}{d[dk(pre)]}"
    PB = lambda tab, row, fy: f"'PB {tab} (Annual)'!{PBC[fy]}{row}/1000"
    R = {}; cur = [4]; cells = []
    def nxt(n=1): cur[0] += n; return cur[0]
    def line(key, text, units='', hist=None, proj=None, fmt=F_MONEY, note='', bold=False, ital=False, indent=0, hk='link', pk='formula'):
        r = nxt(); R[key] = r; label(ws, r, text, units, b=bold, i=ital, indent=indent, note=note)
        for fy in YEARS:
            c = YC[fy]; p = YC.get(fy - 1); fn = hist if fy <= 2026 else proj; kind = hk if fy <= 2026 else pk
            if fn is None: continue
            v = fn(fy, c, p) if callable(fn) else fn
            if v is None: continue
            if isinstance(v, tuple): v, kind = v
            cells.append((f'{c}{r}', v, kind, fmt, bold))
        return r
    def sec(text): r = nxt(); section(ws, r, text, [f'FY{y}{"A" if y <= 2026 else "E"}' for y in YEARS]); return r
    def grp(text): r = nxt(); group(ws, r, text); return r
    def memo(key, text, value, kind='link', fmt=F_PCT2, note=''):
        r = nxt(); R[key] = r; label(ws, r, text, note=note); cells.append((f'D{r}', value, kind, fmt, False)); return r
    pct = lambda num, den: (lambda fy, c, p: f'=IF({c}{{{den}}}=0,0,{c}{{{num}}}/{c}{{{den}}})')
    grow = lambda key: (lambda fy, c, p: f'=IF({p}{{{key}}}=0,0,{c}{{{key}}}/{p}{{{key}}}-1)' if p else None)
    hold = lambda key: (lambda fy, c, p: f'={p}{{{key}}}')
    held26 = lambda key: (lambda fy, c, p: f'=$H${{{key}}}')
    par = lambda pre: (lambda fy, c, p: f'={B(pre, fy)}' if fy in BC else None)
    dpar = lambda ours, theirs: (lambda fy, c, p: f'={c}{{{ours}}}-{c}{{{theirs}}}' if fy in BC else None)
    # ------------------------------------------------------------------ income statement
    R['sec_is'] = sec('Income statement')
    line('svc', 'Service revenue', '$M', lambda fy, c, p: f'=RPM!{c}10', lambda fy, c, p: f'=RPM!{c}10', note='RPM row 10: FY24–26 per 10-K; FY27–28 from the engines (selected case, RPM D3); FY29–31 fade (RPM row 43)')
    line('veh', 'Vehicle sales', '$M', lambda fy, c, p: f'=RPM!{c}12', lambda fy, c, p: f'=RPM!{c}12', note='RPM row 12')
    line('rev', 'Total revenue', '$M', lambda fy, c, p: f'=RPM!{c}6', lambda fy, c, p: f'=RPM!{c}6', bold=True, note='RPM row 6 (history = PitchBook total revenue)')
    line('revg', 'y/y growth', '%', grow('rev'), grow('rev'), F_PCT, ital=True, indent=1, hk='formula')
    line('fac', 'Facility operations (incl. yard D&A)', '$M', lambda fy, c, p: f"={PB('IS', 19, fy)}-{c}{{cvs}}", lambda fy, c, p: f'={c}{{units}}*{c}{{cpu}}/1000',
         note='History: PitchBook total cost of revenue − cost of vehicle sales (10-K). Projection: global fee units (RPM row 29) × facility cost per unit (schedule 1) — the volume-driven margin lever')
    line('cvs', 'Cost of vehicle sales', '$M', lambda fy, c, p: f"={D10('Cost of vehicle sales ($m), FY2026', D10C[fy])}" if fy in D10C else f"={D10('Cost of vehicle sales ($m), FY2024', D10C24[fy])}",
         lambda fy, c, p: f'={c}{{veh}}*{c}{{cvsr}}', note='History: 10-K income statements (FY2026 and FY2024 filings, D 10-K FY26). Projection: vehicle sales × FY2026 ratio (schedule 1)')
    line('gp', 'Gross profit', '$M', lambda fy, c, p: f'={c}{{rev}}-{c}{{fac}}-{c}{{cvs}}', lambda fy, c, p: f'={c}{{rev}}-{c}{{fac}}-{c}{{cvs}}', bold=True, hk='formula')
    line('gpm', 'Gross margin', '%', pct('gp', 'rev'), pct('gp', 'rev'), F_PCT, ital=True, indent=1, hk='formula')
    line('ga', 'General and administrative (incl. D&A, SBC)', '$M', lambda fy, c, p: f"={PB('IS', 31, fy)}", lambda fy, c, p: f'={c}{{rev}}*{c}{{gar}}',
         note='History: PitchBook total operating expenses = 10-K G&A. Projection: revenue × Barclays-implied G&A ratio (schedule 1)')
    line('ebit', 'Operating income (EBIT)', '$M', lambda fy, c, p: f'={c}{{gp}}-{c}{{ga}}', lambda fy, c, p: f'={c}{{gp}}-{c}{{ga}}', bold=True, hk='formula')
    line('ebitm', 'Operating margin', '%', pct('ebit', 'rev'), pct('ebit', 'rev'), F_PCT, ital=True, indent=1, hk='formula')
    line('da', 'Depreciation and amortization', '$M', lambda fy, c, p: f"={PB('IS', 93, fy)}", lambda fy, c, p: f'={c}{{da_s}}', note='History: PitchBook supplemental D&A (10-K). Projection: schedule 2 (Barclays EBITDA − EBIT for FY27–29)')
    line('ebitda', 'Adjusted EBITDA (EBIT + D&A; Barclays definition)', '$M', lambda fy, c, p: f'={c}{{ebit}}+{c}{{da}}', lambda fy, c, p: f'={c}{{ebit}}+{c}{{da}}', bold=True, hk='formula',
         note='Barclays\' "EBITDA (adj)" = EBIT + D&A (FY26: 1,882); no SBC add-back')
    line('ebitdam', 'Adjusted EBITDA margin', '%', pct('ebitda', 'rev'), pct('ebitda', 'rev'), F_PCT, ital=True, indent=1, hk='formula')
    line('int', 'Interest and other income, net', '$M', lambda fy, c, p: f"={PB('IS', 48, fy)}", lambda fy, c, p: f'={c}{{int_s}}', note='History: PitchBook total non-operating income (interest income, net + other). Projection: yield × opening cash & HTM (schedule 3)')
    line('pbt', 'Pre-tax income', '$M', lambda fy, c, p: f'={c}{{ebit}}+{c}{{int}}', lambda fy, c, p: f'={c}{{ebit}}+{c}{{int}}', bold=True, hk='formula')
    line('tax', 'Income tax expense', '$M', lambda fy, c, p: f"={PB('IS', 50, fy)}", lambda fy, c, p: f'={c}{{pbt}}*{c}{{etr}}', note='Projection: pre-tax × structural rate')
    line('etr', 'Effective tax rate', '%', pct('tax', 'pbt'), lambda fy, c, p: "='Reverse DCF'!$S$33", F_PCT, ital=True, indent=1, hk='formula', pk='link',
         note='FY27+: structural rate from the tax build (Reverse DCF S29–S33: 21% statutory + state − FDII − option benefit); Barclays-implied 20.3% in schedule 7')
    line('ni', 'Net income (consolidated)', '$M', lambda fy, c, p: f'={c}{{pbt}}-{c}{{tax}}', lambda fy, c, p: f'={c}{{pbt}}-{c}{{tax}}', bold=True, hk='formula')
    line('nci', 'Net (income) loss attributable to noncontrolling interest', '$M', lambda fy, c, p: f"={PB('IS', 56, fy)}-{PB('IS', 54, fy)}", (0, 'input'),
         note='History: NI to Copart − consolidated NI (positive = NCI loss added back). Projection: ASSUMED 0 (Barclays ignores NCI; FY26 was +3.9)')
    line('nic', 'Net income attributable to Copart', '$M', lambda fy, c, p: f'={c}{{ni}}+{c}{{nci}}', lambda fy, c, p: f'={c}{{ni}}+{c}{{nci}}', bold=True, hk='formula')
    line('dsh', 'Diluted weighted-average shares', 'M', lambda fy, c, p: f"='PB IS (Annual)'!{PBC[fy]}68/1000000", lambda fy, c, p: f'={c}{{dil_s}}', '0.0', note='Projection: schedule 5')
    line('eps', 'Diluted EPS', '$', pct('nic', 'dsh'), pct('nic', 'dsh'), F_USD + '0', bold=True, hk='formula')
    line('epsg', 'y/y growth', '%', grow('eps'), grow('eps'), F_PCT, ital=True, indent=1, hk='formula')
    grp('Barclays parity — income statement (Barclays publishes FY2026A–FY2029E only; Δ = 3SM − Barclays)')
    line('b_rev', 'Barclays revenue', '$M', par('Revenue'), par('Revenue'), note='D Barclays row ' + str(b[bk('Revenue')]))
    line('d_rev', 'Δ revenue', '$M', dpar('rev', 'b_rev'), dpar('rev', 'b_rev'), ital=True, indent=1, hk='formula')
    line('b_ebitda', 'Barclays adjusted EBITDA', '$M', par('EBITDA (adj)'), par('EBITDA (adj)'))
    line('d_ebitda', 'Δ adjusted EBITDA', '$M', dpar('ebitda', 'b_ebitda'), dpar('ebitda', 'b_ebitda'), ital=True, indent=1, hk='formula')
    line('b_ebit', 'Barclays EBIT', '$M', par('EBIT (adj)'), par('EBIT (adj)'))
    line('d_ebit', 'Δ EBIT', '$M', dpar('ebit', 'b_ebit'), dpar('ebit', 'b_ebit'), ital=True, indent=1, hk='formula')
    line('b_pbt', 'Barclays pre-tax income', '$M', par('Pre-tax income (adj)'), par('Pre-tax income (adj)'))
    line('d_pbt', 'Δ pre-tax income', '$M', dpar('pbt', 'b_pbt'), dpar('pbt', 'b_pbt'), ital=True, indent=1, hk='formula')
    line('b_ni', 'Barclays net income', '$M', par('Net income (adj)'), par('Net income (adj)'))
    line('d_ni', 'Δ net income', '$M', dpar('nic', 'b_ni'), dpar('nic', 'b_ni'), ital=True, indent=1, hk='formula')
    line('b_eps', 'Barclays diluted EPS', '$', par('EPS (adj)'), par('EPS (adj)'), F_USD + '0')
    line('d_eps', 'Δ EPS, %', '%', lambda fy, c, p: f'=IF({c}{{b_eps}}=0,0,{c}{{eps}}/{c}{{b_eps}}-1)' if fy in BC else None, lambda fy, c, p: f'=IF({c}{{b_eps}}=0,0,{c}{{eps}}/{c}{{b_eps}}-1)' if fy in BC else None, F_PCT, ital=True, indent=1, hk='formula')
    # ------------------------------------------------------------------ balance sheet
    sec('Balance sheet'); r = nxt(); label(ws, r, 'Assets', b=True)
    line('cash', 'Cash and cash equivalents', '$M', lambda fy, c, p: f"={PB('BS', 14, fy)}", lambda fy, c, p: f'={c}{{cf_end}}', note='Projection: cash-flow statement ending cash (the plug)')
    line('htm', 'Held-to-maturity securities (Treasury bills)', '$M', lambda fy, c, p: f"={PB('BS', 16, fy)}", hold('htm'), note='ASSUMED held flat: no net HTM purchases modelled; all liquidity accrues in cash (same pool for interest income)')
    line('cashhtm', 'Cash & HTM securities', '$M', lambda fy, c, p: f'={c}{{cash}}+{c}{{htm}}', lambda fy, c, p: f'={c}{{cash}}+{c}{{htm}}', ital=True, indent=1, hk='formula', note='Barclays\' "cash and equivalents" line combines both (FY26: 4,490)')
    line('ar', 'Accounts receivable, net', '$M', lambda fy, c, p: f"={PB('BS', 28, fy)}-{PB('BS', 25, fy)}", lambda fy, c, p: f'={c}{{rev}}*{c}{{ar_d}}/365', note='History: PitchBook trade and other receivables − taxes receivable (= 10-K AR, net). Projection: days of revenue (schedule 6)')
    line('taxrec', 'Income taxes receivable', '$M', lambda fy, c, p: f"={PB('BS', 25, fy)}", hold('taxrec'), note='ASSUMED held flat')
    line('pool', 'Vehicle pooling costs', '$M', lambda fy, c, p: f"={PB('BS', 31, fy)}", lambda fy, c, p: f'={c}{{fac}}*{c}{{pool_d}}/365', note='Projection: days of facility operations (schedule 6)')
    line('inv', 'Inventories', '$M', lambda fy, c, p: f"={PB('BS', 19, fy)}", lambda fy, c, p: f'={c}{{cvs}}*{c}{{inv_d}}/365', note='Projection: days of cost of vehicle sales (schedule 6)')
    line('prep', 'Prepaid expenses and other current assets', '$M', lambda fy, c, p: f"={PB('BS', 33, fy)}", lambda fy, c, p: f'={c}{{rev}}*{c}{{prep_d}}/365', note='Projection: days of revenue (schedule 6)')
    line('oth_op', 'Other operating assets (Barclays ΔNWC reconciliation)', '$M', (0, 'formula'), lambda fy, c, p: f'={p}{{oth_op}}+({c}{{dnwc_days}}-{c}{{dnwc_sel}})',
         note='Zero under the days schedule; under the Barclays ΔNWC method it carries the working capital Barclays assumes beyond what the days lines generate, so the balance sheet still balances')
    line('tca', 'Total current assets', '$M', lambda fy, c, p: f'=SUM({c}{{cash}}:{c}{{oth_op}})-{c}{{cashhtm}}', lambda fy, c, p: f'=SUM({c}{{cash}}:{c}{{oth_op}})-{c}{{cashhtm}}', bold=True, hk='formula')
    line('ppe', 'Property and equipment, net (excl. lease ROU)', '$M', lambda fy, c, p: f"={PB('BS', 52, fy)}-{PB('BS', 46, fy)}", lambda fy, c, p: f'={c}{{ppe_close}}', note='History: PitchBook net PP&E − leased assets (= 10-K PP&E, net). Projection: schedule 2')
    line('rou', 'Operating lease right-of-use assets', '$M', lambda fy, c, p: f"={PB('BS', 46, fy)}", hold('rou'), note='ASSUMED held flat (Barclays holds lease debt flat at 88)')
    line('gw', 'Goodwill', '$M', lambda fy, c, p: f"={PB('BS', 55, fy)}", lambda fy, c, p: f'={p}{{gw}}+{c}{{acv_y}}', note='Flat; rises by the ACV consideration in the close year if the DCF toggle is on (schedule 8)')
    line('intang', 'Intangible assets, net', '$M', lambda fy, c, p: f"={PB('BS', 73, fy)}-{PB('BS', 55, fy)}", hold('intang'), note='ASSUMED held flat (amortisation is carried inside D&A against PP&E)')
    line('onca', 'Other non-current assets', '$M', lambda fy, c, p: f"={PB('BS', 76, fy)}", hold('onca'), note='ASSUMED held flat')
    line('ta', 'Total assets', '$M', lambda fy, c, p: f'={c}{{tca}}+SUM({c}{{ppe}}:{c}{{onca}})', lambda fy, c, p: f'={c}{{tca}}+SUM({c}{{ppe}}:{c}{{onca}})', bold=True, hk='formula')
    r = nxt(); label(ws, r, 'Liabilities', b=True)
    line('ap', 'Accounts payable, accrued liabilities and deferred revenue', '$M', lambda fy, c, p: f"={PB('BS', 112, fy)}-{PB('BS', 85, fy)}-{PB('BS', 98, fy)}", lambda fy, c, p: f'=({c}{{fac}}+{c}{{cvs}}+{c}{{ga}}-{c}{{da}})*{c}{{ap_d}}/365',
         note='History: PitchBook total current liabilities − income taxes payable − current lease liabilities (FY26: 634.7 AP & accrued + 32.5 deferred revenue). Projection: days of cash operating costs (schedule 6)')
    line('taxpay', 'Income taxes payable', '$M', lambda fy, c, p: f"={PB('BS', 85, fy)}", hold('taxpay'), note='ASSUMED held flat')
    line('lease_c', 'Lease liabilities, current', '$M', lambda fy, c, p: f"={PB('BS', 98, fy)}", hold('lease_c'), note='ASSUMED held flat')
    line('tcl', 'Total current liabilities', '$M', lambda fy, c, p: f'=SUM({c}{{ap}}:{c}{{lease_c}})', lambda fy, c, p: f'=SUM({c}{{ap}}:{c}{{lease_c}})', bold=True, hk='formula')
    line('lease_nc', 'Lease liabilities and debt, non-current', '$M', lambda fy, c, p: f"={PB('BS', 119, fy)}", hold('lease_nc'), note='ASSUMED held flat; with the current portion this is Barclays\' "debt" of 88')
    line('dtl', 'Deferred tax liabilities', '$M', lambda fy, c, p: f"={PB('BS', 121, fy)}", hold('dtl'), note='ASSUMED held flat')
    line('onc', 'Other non-current liabilities (taxes payable)', '$M', lambda fy, c, p: f"={PB('BS', 125, fy)}", hold('onc'), note='ASSUMED held flat')
    line('tl', 'Total liabilities', '$M', lambda fy, c, p: f'={c}{{tcl}}+SUM({c}{{lease_nc}}:{c}{{onc}})', lambda fy, c, p: f'={c}{{tcl}}+SUM({c}{{lease_nc}}:{c}{{onc}})', bold=True, hk='formula')
    r = nxt(); label(ws, r, 'Equity', b=True)
    line('eq', "Copart stockholders' equity", '$M', lambda fy, c, p: f"={PB('BS', 147, fy)}", lambda fy, c, p: f'={p}{{eq}}+{c}{{nic}}+{c}{{sbc_cf}}+{c}{{opt_cf}}+{c}{{bb_cf}}',
         note='Projection: prior + net income to Copart + SBC + option proceeds − repurchases (no OCI movement assumed)')
    line('ncieq', 'Noncontrolling interest', '$M', lambda fy, c, p: f"={PB('BS', 148, fy)}", lambda fy, c, p: f'={p}{{ncieq}}-{c}{{nci}}', note='Projection: prior less the NCI loss carried on the income statement (0 by assumption)')
    line('te', 'Total equity', '$M', lambda fy, c, p: f'={c}{{eq}}+{c}{{ncieq}}', lambda fy, c, p: f'={c}{{eq}}+{c}{{ncieq}}', bold=True, hk='formula')
    line('tle', 'Total liabilities and equity', '$M', lambda fy, c, p: f'={c}{{tl}}+{c}{{te}}', lambda fy, c, p: f'={c}{{tl}}+{c}{{te}}', bold=True, hk='formula')
    line('bal', 'Balance check (assets − liabilities and equity; should be 0)', '$M', lambda fy, c, p: f'=ROUND({c}{{ta}}-{c}{{tle}},3)', lambda fy, c, p: f'=ROUND({c}{{ta}}-{c}{{tle}},3)', '0.000', ital=True, hk='formula')
    grp('Barclays parity — balance sheet')
    line('debt', 'Debt, Barclays definition (lease liabilities, current + non-current)', '$M', lambda fy, c, p: f'={c}{{lease_c}}+{c}{{lease_nc}}', lambda fy, c, p: f'={c}{{lease_c}}+{c}{{lease_nc}}', hk='formula')
    line('b_cash', 'Barclays cash and equivalents', '$M', par('Cash and equivalents'), par('Cash and equivalents'))
    line('d_cash', 'Δ cash & HTM', '$M', dpar('cashhtm', 'b_cash'), dpar('cashhtm', 'b_cash'), ital=True, indent=1, hk='formula')
    line('b_ta', 'Barclays total assets', '$M', par('Total assets'), par('Total assets'))
    line('d_ta', 'Δ total assets', '$M', dpar('ta', 'b_ta'), dpar('ta', 'b_ta'), ital=True, indent=1, hk='formula')
    line('b_debt', 'Barclays debt', '$M', par('Short and long-term debt'), par('Short and long-term debt'))
    line('d_debt', 'Δ debt', '$M', dpar('debt', 'b_debt'), dpar('debt', 'b_debt'), ital=True, indent=1, hk='formula')
    line('b_eq', "Barclays shareholders' equity", '$M', par("Shareholders' equity"), par("Shareholders' equity"))
    line('d_eq', "Δ Copart stockholders' equity", '$M', dpar('eq', 'b_eq'), dpar('eq', 'b_eq'), ital=True, indent=1, hk='formula')
    # ------------------------------------------------------------------ cash flow statement
    sec('Cash flow statement'); r = nxt(); label(ws, r, 'Operating activities', b=True)
    line('cf_ni', 'Net income (consolidated)', '$M', lambda fy, c, p: f"={PB('CF', 14, fy)}", lambda fy, c, p: f'={c}{{ni}}', pk='formula')
    line('cf_da', '(+) Depreciation and amortization', '$M', lambda fy, c, p: f"={PB('CF', 17, fy)}", lambda fy, c, p: f'={c}{{da}}', note='History: cash-flow D&A incl. debt-cost amortisation (FY26 238.5 vs 229.4 on the income statement)')
    line('sbc_cf', '(+) Stock-based compensation', '$M', lambda fy, c, p: f"={PB('CF', 20, fy)}", lambda fy, c, p: f'={c}{{sbc_s}}', note='Projection: schedule 4')
    line('cf_oth', '(+) Other non-cash items (deferred taxes, disposals, other)', '$M', lambda fy, c, p: f"={PB('CF', 35, fy)}-{PB('CF', 17, fy)}-{PB('CF', 20, fy)}", (0, 'input'), note='ASSUMED 0 in projection (FY26: 54.4, mostly deferred taxes)')
    line('cf_nwc', '(−) Change in operating working capital', '$M', lambda fy, c, p: f"={PB('CF', 55, fy)}", lambda fy, c, p: f'={c}{{dnwc_sel}}', note='Projection: selected method (schedule 6; default = Barclays −83 a year)')
    line('cfo', 'Cash flow from operations', '$M', lambda fy, c, p: f'=SUM({c}{{cf_ni}}:{c}{{cf_nwc}})', lambda fy, c, p: f'=SUM({c}{{cf_ni}}:{c}{{cf_nwc}})', bold=True, hk='formula')
    r = nxt(); label(ws, r, 'Investing activities', b=True)
    line('capex', '(−) Purchases of property and equipment', '$M', lambda fy, c, p: f"={PB('CF', 64, fy)}", lambda fy, c, p: f'={c}{{capex_s}}', note='Projection: schedule 2 (Barclays −500 a year FY27–29)')
    line('disp', '(+) Proceeds from disposals of property and equipment', '$M', lambda fy, c, p: f"={PB('CF', 65, fy)}", (0, 'input'), note='ASSUMED 0')
    line('acq', '(−) Acquisitions and investments in businesses (ACV if toggled)', '$M', lambda fy, c, p: f"={PB('CF', 70, fy)}+{PB('CF', 73, fy)}", lambda fy, c, p: f'=-{c}{{acv_y}}', note='Projection: ACV cash consideration in the close year when the DCF toggle is on (schedule 8)')
    line('htm_cf', '(−) Net purchases of held-to-maturity securities', '$M', lambda fy, c, p: f"={PB('CF', 77, fy)}", (0, 'input'), note='ASSUMED 0: HTM held flat (balance sheet)')
    line('oth_inv', 'Other investing', '$M', lambda fy, c, p: f"={PB('CF', 84, fy)}-({c}{{capex}}+{c}{{disp}}+{c}{{acq}}+{c}{{htm_cf}})", (0, 'input'), note='History: residual to PitchBook total investing cash flow')
    line('cfi', 'Cash flow from investing', '$M', lambda fy, c, p: f'=SUM({c}{{capex}}:{c}{{oth_inv}})', lambda fy, c, p: f'=SUM({c}{{capex}}:{c}{{oth_inv}})', bold=True, hk='formula')
    r = nxt(); label(ws, r, 'Financing activities', b=True)
    line('bb_cf', '(−) Repurchases of common stock', '$M', lambda fy, c, p: f"={PB('CF', 90, fy)}", lambda fy, c, p: f'=-{c}{{bb_s}}', note='Projection: schedule 5 (input, default 0)')
    line('opt_cf', '(+) Proceeds from stock options and ESPP', '$M', lambda fy, c, p: f"={PB('CF', 109, fy)}", hold('opt_cf'), note='ASSUMED held at FY2026 (31.0)')
    line('debt_cf', 'Debt and lease repayments, issuance costs', '$M', lambda fy, c, p: f"={PB('CF', 100, fy)}+{PB('CF', 103, fy)}+{PB('CF', 106, fy)}", (0, 'input'), note='ASSUMED 0 (no funded debt)')
    line('oth_fin', 'Other financing (incl. tax withholding on equity awards, NCI)', '$M', lambda fy, c, p: f"={PB('CF', 112, fy)}-({c}{{bb_cf}}+{c}{{opt_cf}}+{c}{{debt_cf}})", (0, 'input'), note='History: residual to PitchBook total financing cash flow. ASSUMED 0')
    line('cff', 'Cash flow from financing', '$M', lambda fy, c, p: f'=SUM({c}{{bb_cf}}:{c}{{oth_fin}})', lambda fy, c, p: f'=SUM({c}{{bb_cf}}:{c}{{oth_fin}})', bold=True, hk='formula')
    line('fx', 'Effect of exchange rates on cash', '$M', lambda fy, c, p: f"={PB('CF', 115, fy)}", (0, 'input'), note='ASSUMED 0')
    line('netchg', 'Net change in cash and cash equivalents', '$M', lambda fy, c, p: f'={c}{{cfo}}+{c}{{cfi}}+{c}{{cff}}+{c}{{fx}}', lambda fy, c, p: f'={c}{{cfo}}+{c}{{cfi}}+{c}{{cff}}+{c}{{fx}}', bold=True, hk='formula')
    line('cf_beg', 'Beginning cash and cash equivalents', '$M', lambda fy, c, p: f"={PB('CF', 117, fy)}", lambda fy, c, p: f'={p}{{cf_end}}')
    line('cf_end', 'Ending cash and cash equivalents', '$M', lambda fy, c, p: f'={c}{{cf_beg}}+{c}{{netchg}}', lambda fy, c, p: f'={c}{{cf_beg}}+{c}{{netchg}}', bold=True, hk='formula')
    line('cf_chk', 'Cash check (ending cash − balance-sheet cash; should be 0)', '$M', lambda fy, c, p: f'=ROUND({c}{{cf_end}}-{c}{{cash}},3)', lambda fy, c, p: f'=ROUND({c}{{cf_end}}-{c}{{cash}},3)', '0.000', ital=True, hk='formula')
    line('fcf', 'Free cash flow (CFO + capex)', '$M', lambda fy, c, p: f'={c}{{cfo}}+{c}{{capex}}', lambda fy, c, p: f'={c}{{cfo}}+{c}{{capex}}', bold=True, hk='formula')
    line('fcfm', 'FCF margin', '%', pct('fcf', 'rev'), pct('fcf', 'rev'), F_PCT, ital=True, indent=1, hk='formula')
    grp('Barclays parity — cash flow')
    line('b_cfo', 'Barclays cash flow from operations', '$M', par('Cash flow from operations'), par('Cash flow from operations'))
    line('d_cfo', 'Δ CFO', '$M', dpar('cfo', 'b_cfo'), dpar('cfo', 'b_cfo'), ital=True, indent=1, hk='formula')
    line('b_capex', 'Barclays capital expenditure', '$M', par('Capital expenditure'), par('Capital expenditure'))
    line('d_capex', 'Δ capex', '$M', dpar('capex', 'b_capex'), dpar('capex', 'b_capex'), ital=True, indent=1, hk='formula')
    line('b_nwc', 'Barclays change in working capital', '$M', par('Change in working capital'), par('Change in working capital'))
    line('d_nwc', 'Δ change in working capital', '$M', dpar('cf_nwc', 'b_nwc'), dpar('cf_nwc', 'b_nwc'), ital=True, indent=1, hk='formula')
    line('b_fcf', 'Barclays free cash flow (memo; Barclays\' definition not stated, exceeds CFO + capex)', '$M', par('Free cash flow'), par('Free cash flow'), ital=True)
    # ------------------------------------------------------------------ schedules
    sec('Supporting schedules'); grp('1. Revenue drivers and facility cost (the volume-driven gross margin)')
    line('units', 'Global fee units', '000s', lambda fy, c, p: f'=RPM!{c}29', lambda fy, c, p: f'=RPM!{c}29', F_INT, note='RPM row 29 (FY26 anchor 4.0m; FY27–28 from the engines; FY29–31 fade). History before FY26 is blank where the RPM has no units')
    line('cpu', 'Facility cost per fee unit (incl. yard D&A)', '$', lambda fy, c, p: f'=IFERROR({c}{{fac}}*1000/{c}{{units}},"")', lambda fy, c, p: f'={p}{{cpu}}*(1+{c}{{cpug}})', F_USD, hk='formula', note='FY26: 1,965.9 ÷ 4.0m units ≈ $491. Projection: prior × (1 + growth)')
    line('cpug', 'Facility cost per unit, y/y', '%', lambda fy, c, p: f'=IFERROR({c}{{cpu}}/{p}{{cpu}}-1,"")' if p else None, lambda fy, c, p: f'=DCF!{c}15', F_PCT, ital=True, indent=1, hk='formula', pk='link',
         note='ASSUMED (owner, DCF row 15): +4.5% FY27 fading to +2.0% FY31 — one input shared with the DCF so the two builds move together')
    line('cvsr', 'Cost of vehicle sales, % of vehicle sales', '%', pct('cvs', 'veh'), held26('cvsr'), F_PCT, hk='formula', note='CALIBRATED: FY2026 actual (10-K) held')
    line('gar', 'G&A (incl. D&A, SBC), % of revenue', '%', pct('ga', 'rev'), lambda fy, c, p: (f"=({B('Revenue', fy)}-{B('EBIT (adj)', fy)})/{B('Revenue', fy)}-($H${{fac}}+$H${{cvs}})/$H${{rev}}" if fy in BC else f'={p}{{gar}}'), F_PCT, hk='formula',
         note='Barclays-implied: Barclays\' (revenue − EBIT) ÷ revenue less Copart\'s FY2026 facility and vehicle-cost ratios (FY27 9.2%, FY28 8.6%, FY29 8.1%); held at FY29 after. Barclays\' margin expansion therefore sits in G&A; volume leverage sits in facility cost')
    grp('2. Property and equipment, capex and D&A')
    line('ppe_open', 'Opening net PP&E', '$M', None, lambda fy, c, p: f'={p}{{ppe}}')
    line('capex_s', 'Capital expenditure (negative = outflow)', '$M', lambda fy, c, p: f'={c}{{capex}}', lambda fy, c, p: (f"={B('Capital expenditure', fy)}" if fy in BC else f'=-{c}{{rev}}*${YC[2029]}${{capex_r}}'), hk='formula', pk='link',
         note='FY27–29: Barclays −500 a year (D Barclays). FY30–31: Barclays\' FY29 capex-to-revenue ratio applied to model revenue (no broker projects FY30)')
    line('capex_r', 'Capex, % of revenue', '%', lambda fy, c, p: f'=IF({c}{{rev}}=0,0,-{c}{{capex_s}}/{c}{{rev}})', lambda fy, c, p: f'=IF({c}{{rev}}=0,0,-{c}{{capex_s}}/{c}{{rev}})', F_PCT, ital=True, indent=1, hk='formula')
    line('da_s', 'Depreciation and amortization', '$M', lambda fy, c, p: f'={c}{{da}}', lambda fy, c, p: (f"={B('EBITDA (adj)', fy)}-{B('EBIT (adj)', fy)}" if fy in BC else f'={c}{{ppe_open}}*${YC[2029]}${{da_r}}'), hk='formula', pk='link',
         note='FY27–29: Barclays EBITDA − EBIT (226 / 234 / 243). FY30–31: Barclays\' FY29 D&A-to-opening-PP&E rate applied to the model\'s opening balance')
    line('da_r', 'D&A, % of opening net PP&E', '%', lambda fy, c, p: f'=IF({p}{{ppe}}=0,0,{c}{{da}}/{p}{{ppe}})' if p else None, lambda fy, c, p: f'=IF({c}{{ppe_open}}=0,0,{c}{{da_s}}/{c}{{ppe_open}})', F_PCT, ital=True, indent=1, hk='formula')
    line('ppe_close', 'Closing net PP&E (opening + capex − D&A)', '$M', None, lambda fy, c, p: f'={c}{{ppe_open}}-{c}{{capex_s}}-{c}{{da_s}}', bold=True, note='All D&A is charged against PP&E (intangibles held flat); ROU assets sit on their own line')
    grp('3. Cash, HTM securities and interest income')
    line('cash_open', 'Opening cash & HTM securities', '$M', None, lambda fy, c, p: f'={p}{{cashhtm}}')
    line('yld', 'Yield on opening cash & HTM (interest and other income)', '%', lambda fy, c, p: f'=IF({p}{{cashhtm}}=0,0,{c}{{int}}/{p}{{cashhtm}})' if p else None, lambda fy, c, p: (f"=({B('Pre-tax income (adj)', fy)}-{B('EBIT (adj)', fy)})/{B('Cash and equivalents', fy - 1)}" if fy in BC else f'={p}{{yld}}'), F_PCT2, hk='formula',
         note='FY27–29: Barclays-implied (pre-tax − EBIT = 140 a year ÷ Barclays\' opening cash): 3.1% / 2.5% / 2.0%; held at FY29 after. FY26 actual on opening cash & HTM: 3.8% (10-K interest income 181.9). Opening balance avoids a circular reference')
    line('int_s', 'Interest and other income, net', '$M', None, lambda fy, c, p: f'={c}{{cash_open}}*{c}{{yld}}')
    grp('4. Stock-based compensation')
    line('sbc_r', 'SBC, % of revenue', '%', pct('sbc_cf', 'rev'), held26('sbc_r'), F_PCT2, hk='formula', note='CALIBRATED: FY2026 actual (cash-flow statement 38.8 = 0.83%) held; Barclays publishes no SBC line')
    line('sbc_s', 'Stock-based compensation', '$M', None, lambda fy, c, p: f'={c}{{rev}}*{c}{{sbc_r}}')
    grp('5. Shares and buybacks')
    line('bb_s', 'Share repurchases ($, input)', '$M', lambda fy, c, p: f'=-{c}{{bb_cf}}', (0, 'input'), hk='formula',
         note='ASSUMED 0: Barclays\' flat 933m diluted share count implies no repurchases after FY26. Enter dollars to test; the owner\'s DCF cash roll carries $600m a year (DCF row 73) as an alternative')
    line('bb_px', 'Average repurchase price', '$', lambda fy, c, p: f"={D10('FY2026 share repurchases', 'D')}" if fy == 2026 else None, lambda fy, c, p: f'=DCF!{c}74', F_USD, note='FY26: $37.63 (10-K). Projection: owner\'s DCF row 74')
    line('bb_sh', 'Shares repurchased', 'M', lambda fy, c, p: f"={D10('FY2026 share repurchases', 'C')}" if fy == 2026 else f'=IF(N({c}{{bb_px}})=0,0,{c}{{bb_s}}/N({c}{{bb_px}}))', lambda fy, c, p: f'=IF({c}{{bb_px}}=0,0,{c}{{bb_s}}/{c}{{bb_px}})', '0.00', note='FY26: 43.4m (10-K)')
    line('iss', 'Net shares issued (options, RSUs, ESPP)', 'M', lambda fy, c, p: f'={c}{{sh_end}}-{p}{{sh_end}}+N({c}{{bb_sh}})' if p else None, held26('iss'), '0.00', hk='formula', note='History: change in year-end shares + repurchased shares. Projection: FY2026 actual (1.8m) held')
    line('sh_end', 'Basic shares outstanding, year-end', 'M', lambda fy, c, p: f"='PB BS (Annual)'!{PBC[fy]}152/1000000", lambda fy, c, p: f'={p}{{sh_end}}+{c}{{iss}}-{c}{{bb_sh}}', '0.0', note='History: PitchBook common shares outstanding (FY26 925.8m; the 10-K cover count 926.3m is a later date)')
    line('sh_avg', 'Basic weighted-average shares', 'M', lambda fy, c, p: f"='PB IS (Annual)'!{PBC[fy]}67/1000000", lambda fy, c, p: f'=({p}{{sh_end}}+{c}{{sh_end}})/2', '0.0')
    line('dil', 'Dilutive securities (options, RSUs; treasury method)', 'M', lambda fy, c, p: f'={c}{{dsh}}-{c}{{sh_avg}}', held26('dil'), '0.00', hk='formula', note='History: diluted − basic weighted-average shares. Projection: FY2026 actual (7.2m) held — matches Barclays\' 933m (925.8 + 7.2)')
    line('dil_s', 'Diluted weighted-average shares', 'M', lambda fy, c, p: f'={c}{{dsh}}', lambda fy, c, p: f'={c}{{sh_avg}}+{c}{{dil}}', '0.0', bold=True, hk='formula')
    line('b_sh', 'Barclays diluted shares', 'M', par('Diluted shares'), par('Diluted shares'), '0.0')
    line('d_sh', 'Δ diluted shares', 'M', dpar('dil_s', 'b_sh'), dpar('dil_s', 'b_sh'), '0.0', ital=True, indent=1, hk='formula')
    grp('6. Working capital (days; FY2026 actual held) and the Barclays ΔNWC method')
    line('ar_d', 'Receivables, days of revenue', 'days', lambda fy, c, p: f'=IF({c}{{rev}}=0,0,{c}{{ar}}/{c}{{rev}}*365)', held26('ar_d'), '0.0', hk='formula')
    line('pool_d', 'Vehicle pooling costs, days of facility operations', 'days', lambda fy, c, p: f'=IF({c}{{fac}}=0,0,{c}{{pool}}/{c}{{fac}}*365)', held26('pool_d'), '0.0', hk='formula')
    line('inv_d', 'Inventories, days of cost of vehicle sales', 'days', lambda fy, c, p: f'=IF({c}{{cvs}}=0,0,{c}{{inv}}/{c}{{cvs}}*365)', held26('inv_d'), '0.0', hk='formula')
    line('prep_d', 'Prepaid and other current assets, days of revenue', 'days', lambda fy, c, p: f'=IF({c}{{rev}}=0,0,{c}{{prep}}/{c}{{rev}}*365)', held26('prep_d'), '0.0', hk='formula')
    line('ap_d', 'Payables, accrued and deferred revenue, days of cash operating costs', 'days', lambda fy, c, p: f'=IF(({c}{{fac}}+{c}{{cvs}}+{c}{{ga}}-{c}{{da}})=0,0,{c}{{ap}}/({c}{{fac}}+{c}{{cvs}}+{c}{{ga}}-{c}{{da}})*365)', held26('ap_d'), '0.0', hk='formula',
         note='Cash operating costs = facility operations + cost of vehicle sales + G&A − D&A')
    line('nwc_days', 'Operating working capital (days-driven lines)', '$M', lambda fy, c, p: f'={c}{{ar}}+{c}{{pool}}+{c}{{inv}}+{c}{{prep}}-{c}{{ap}}', lambda fy, c, p: f'={c}{{ar}}+{c}{{pool}}+{c}{{inv}}+{c}{{prep}}-{c}{{ap}}', hk='formula')
    line('dnwc_days', 'Change in working capital, days basis (cash effect)', '$M', lambda fy, c, p: f'=-({c}{{nwc_days}}-{p}{{nwc_days}})' if p else None, lambda fy, c, p: f'=-({c}{{nwc_days}}-{p}{{nwc_days}})', hk='formula',
         note='FY2026 days held produce only a small outflow (the lines grow with revenue); Copart\'s reported outflows have been larger (FY22–26 average −102)')
    line('b_nwc_s', 'Barclays change in working capital (FY30–31 held at FY29)', '$M', par('Change in working capital'), lambda fy, c, p: (f"={B('Change in working capital', fy)}" if fy in BC else f'={p}{{b_nwc_s}}'), pk='link')
    r = nxt(); R['nwc_sel'] = r; label(ws, r, 'ΔNWC method (click D to choose; index in F): days schedule or Barclays', note='Selector. Barclays keeps the cash flow on −83 a year; the days schedule lets the lines above drive it')
    line('dnwc_sel', 'Change in working capital, selected (to the cash flow statement)', '$M', None, lambda fy, c, p: f'=IF($F${{nwc_sel}}=1,{c}{{dnwc_days}},{c}{{b_nwc_s}})', bold=True)
    grp('7. Tax (rates; the build lives on the Reverse DCF tab, columns R–X)')
    memo('etr_s', 'Structural effective tax rate applied FY27+ (Reverse DCF S33)', "='Reverse DCF'!S33", note='21% statutory + state − FDII − excess option benefit (10-K tax note)')
    memo('etr_b', 'Barclays-implied FY2027E rate (Reverse DCF S36)', "='Reverse DCF'!S36", note='1 − Barclays adj. net income ÷ adj. pre-tax')
    memo('etr_a', 'FY2026 actual effective rate (10-K)', f"={D10('Effective tax rate', 'C')}", note='MD&A: 19.3%')
    grp('8. ACV Auctions acquisition gate (links to the owner\'s DCF toggle)')
    memo('acv_tog', 'Toggle (1 = include cash consideration; DCF H115)', '=DCF!H115', fmt='0')
    memo('acv_cons', 'Cash consideration ($M; DCF H116)', '=DCF!H116', fmt=F_MONEY)
    memo('acv_year', 'Closes in fiscal year (DCF I117)', '=DCF!I117', fmt='@')
    line('acv_y', 'Cash consideration by year (to investing cash flow and goodwill)', '$M', None, lambda fy, c, p: f'=IF(AND($D${{acv_tog}}=1,{c}${R["sec_is"]}=$D${{acv_year}}),$D${{acv_cons}},0)',
         note='ACV\'s revenue and EBITDA contribution is excluded until the deal is classified (plan §2.8); only the cash outflow and goodwill are carried')
    grp('9. Memo: the owner\'s DCF operating build')
    line('dcf_ebit', 'DCF operating income (DCF row 24)', '$M', None, lambda fy, c, p: f'=DCF!{c}24', pk='link')
    line('d_dcf', 'Δ 3SM EBIT − DCF EBIT', '$M', None, lambda fy, c, p: f'={c}{{ebit}}-{c}{{dcf_ebit}}', ital=True, indent=1, note='The DCF grows G&A at its own rates (DCF row 22); the 3SM uses the Barclays-implied ratio. Link DCF row 24 here to make them one build')
    # ------------------------------------------------------------------ write deferred cells
    for ref, v, kind, fmt, bold in cells:
        put(ws, ref, v.format_map(R) if isinstance(v, str) else v, kind, fmt, b=bold)
    ws.merge_cells(f"D{R['nwc_sel']}:E{R['nwc_sel']}"); dropdown(ws, f"D{R['nwc_sel']}", ['1 · Days schedule', '2 · Barclays ΔNWC (−83 a year)'], index_cell=f"F{R['nwc_sel']}", default_index=2, list_col='Q', list_row=R['nwc_sel'] - 1, title='ΔNWC options (list source)')
    ws.freeze_panes = 'D6'; ctx['tsm_rows'] = R
    # ------------------------------------------------------------------ DCF: D&A, SBC, capex and ΔNWC now read the 3SM (no longer % of revenue)
    dcf = wb['DCF']
    for fy in PROJ:
        c = YC[fy]; p = YC[fy - 1]
        put(dcf, f'{c}29', f"='3SM'!{c}{R['da']}", 'link'); put(dcf, f'{c}30', f'={c}29/{c}6', 'formula')
        put(dcf, f'{c}57', f"='3SM'!{c}{R['sbc_cf']}", 'link'); put(dcf, f'{c}58', f'={c}57/{c}6', 'formula')
        put(dcf, f'{c}59', f"='3SM'!{c}{R['capex']}", 'link'); put(dcf, f'{c}60', f'=-{c}59/{c}6', 'formula')
        put(dcf, f'{c}61', f"='3SM'!{c}{R['cf_nwc']}", 'link'); put(dcf, f'{c}62', f'=IFERROR(-{c}61/({c}6-{p}6),0)', 'formula')
    for r_, txt in ((29, f"From the 3SM row {R['da']} (Barclays D&A FY27–29; FY30–31 at the FY29 rate); row 30 is now the implied %"), (57, f"From the 3SM row {R['sbc_cf']} (FY26 % of revenue held); row 58 implied"),
                    (59, f"From the 3SM row {R['capex']} (Barclays −500 FY27–29; FY29 ratio after); row 60 implied"), (61, f"From the 3SM row {R['cf_nwc']} (selected ΔNWC method, 3SM D{R['nwc_sel']}); row 62 implied")):
        put(dcf, f'P{r_}', txt, 'note')
    # ------------------------------------------------------------------ checks for the Checks tab
    I, M, H = YC[2027], YC[2031], YC[2026]
    ctx.setdefault('extra_checks', []).extend([
        ('3SM: balance sheet balances, FY2027E', f"='3SM'!{I}{R['bal']}", 0, 0.01, '0.000'),
        ('3SM: balance sheet balances, FY2031E', f"='3SM'!{M}{R['bal']}", 0, 0.01, '0.000'),
        ('3SM: cash flow ending cash ties to balance-sheet cash, FY2031E', f"='3SM'!{M}{R['cf_chk']}", 0, 0.01, '0.000'),
        ('3SM: FY2026A total assets tie to PitchBook', f"='3SM'!{H}{R['ta']}", "='PB BS (Annual)'!M78/1000", 0.01, F_MONEY),
        ('3SM: FY2026A operating income ties to the 10-K (1,652.6)', f"='3SM'!{H}{R['ebit']}", f"={D10('Operating income', 'C')}", 0.05, F_MONEY),
        ('3SM: FY2026A adjusted EBITDA ties to Barclays (1,882) within $1m', f"='3SM'!{H}{R['ebitda']}", f"={B('EBITDA (adj)', 2026)}", 1.0, F_MONEY),
        ('3SM: FY2026A CFO ties to PitchBook / 10-K (1,604.5)', f"='3SM'!{H}{R['cfo']}", "='PB CF (Annual)'!M56/1000", 0.01, F_MONEY),
        ('RPM FY2026 service revenue (owner-typed) equals the 10-K (3,969.5)', '=RPM!H10', f"={D10('Service revenues', 'C')}", 0.1, F_MONEY),
        ('DCF reads the 3SM: D&A FY2027E', '=DCF!I29', f"='3SM'!{I}{R['da']}", 0.001, F_MONEY),
        ('DCF reads the 3SM: capex FY2027E', '=DCF!I59', f"='3SM'!{I}{R['capex']}", 0.001, F_MONEY)])
