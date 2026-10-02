"""Targeted edits to model/CPRT_Model_v3.xlsx (the owner's file of record). No tab is regenerated; every cell touched is printed.
1. DCF row 58: ΔNWC shown as % of revenue (was % of the change in revenue → 586% when revenue is flat).
2. Broken references after the owner's row deletions: DCF sensitivity header D108:H108; Summary rows 25–26; WACC tab rows 55–70.
3. Reverse DCF solve: one lever (dropdown) makes the implied price equal the current price — flat revenue growth at the input
   exit multiple, or the exit multiple on Barclays' revenue path; both solved live (no Goal Seek). Two sensitivities.
4. WACC tab compaction: shorter labels in column M (detail moved to the notes column R), narrower columns, dashes in empty data cells."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
import openpyxl
from cprt_model.common import *
P = ROOT / 'model/CPRT_Model_v3.xlsx'; wb = openpyxl.load_workbook(P); W = 'WACC, Tax, and Reverse DCF'; ws = wb[W]; dcf = wb['DCF']; sm = wb['Summary']
touched = []
def setc(sheet, ref, value, kind=None, fmt=None, b=False, i=False):
    old = sheet[ref].value; kind = kind or ('link' if isinstance(value, str) and '!' in value else 'formula' if isinstance(value, str) and value.startswith('=') else 'label' if isinstance(value, str) else 'input')
    put(sheet, ref, value, kind, fmt, b=b, i=i); touched.append((sheet.title, ref, str(old)[:50], str(value)[:60]))
# ---------------------------------------------------------------- 1. DCF ΔNWC ratio
setc(dcf, 'B58', '   Increase in NWC as % of revenue (reads the 3SM)')
for c in 'IJKLM': setc(dcf, f'{c}58', f'=-{c}57/{c}6', 'formula', F_PCT)
# ---------------------------------------------------------------- 2a. DCF sensitivity header: WACC anchor lost when the old WACC block was deleted
for c, step in zip('DEFGH', (-0.01, -0.005, 0, 0.005, 0.01)): setc(dcf, f'{c}108', f"='{W}'!$N$31+({step})", 'link', F_PCT2)
# ---------------------------------------------------------------- 2b. Summary rows 25–26 pointed at the deleted consensus row
setc(sm, 'B25', "DCF diluted EPS (owner's DCF row 41; the DCF keeps its own cost build)"); setc(sm, 'B26', '% Δ DCF EPS vs Barclays')
for c, dc in zip('FGHI', 'HIJK'): setc(sm, f'{c}25', f'=DCF!{dc}41', 'link', F_USD + '0'); setc(sm, f'{c}26', f'=IF({c}23=0,0,{c}25/{c}23-1)', 'formula', F_PCT, b=True)
for c in 'DE':
    for r in (25, 26): setc(sm, f'{c}{r}', DASH, 'note')
setc(sm, 'L25', 'DCF row 41 (DCF EBIT build differs from the 3SM; see 3SM schedule 9)', 'note'); setc(sm, 'L26', 'Summary row 23 holds Barclays EPS', 'note')
# ---------------------------------------------------------------- 3. Reverse DCF solve (WACC tab)
a1 = '($I$14*(1-DCF!$I$38)+DCF!$I$54-DCF!$I$56)'; a2 = '($J$14*(1-DCF!$J$38)+DCF!$J$54-DCF!$J$56)'   # UFCF per $ of revenue: margin×(1−t) + SBC% − capex%
b1 = '($I$17*DCF!$I$38+$I$28)'; b2 = '($J$17*DCF!$J$38+$J$28)'                                       # fixed part: D&A tax shield + ΔNWC
A = f'($J$31*$H$10*({a2}+$H$57*$J$14))'; B = f'($I$31*$H$10*{a1})'; C = f'($I$31*{b1}+$J$31*{b2}-$H$58)'
setc(ws, 'B5', "Flat revenue growth, FY27–FY28: solved so the implied price equals the current price (lever 1), or Barclays' path CAGR (lever 2)")
setc(ws, 'H5', '=IF($I$56=1,H59,(J10/H10)^(1/2)-1)', 'formula', F_PCT2, b=True)
setc(ws, 'I10', '=IF($I$56=1,H10*(1+$H$5),I61)', 'formula', F_MONEY, b=True); setc(ws, 'J10', '=IF($I$56=1,I10*(1+$H$5),J61)', 'formula', F_MONEY, b=True)
setc(ws, 'B36', 'Exit EV / EBITDA multiple (input H57 under lever 1; solved H60 under lever 2)'); setc(ws, 'H36', '=IF($I$56=1,H57,H60)', 'formula', F_X, b=True)
setc(ws, 'B55', 'Reverse DCF solve — the one lever that makes the implied price (H51) equal the current price (H52)')
setc(ws, 'B56', "Lever (click H56): solve flat revenue growth at the input multiple, or solve the exit multiple on Barclays' revenue path")
ws.data_validations.dataValidation = [d for d in ws.data_validations.dataValidation if 'H56' not in str(d.sqref)]
dropdown(ws, 'H56', ['1 · Solve growth (multiple fixed)', '2 · Solve exit multiple (Barclays revenue)'], index_cell='I56', default_index=1, list_col='T', list_row=55, title='Lever options (list source for H56)'); touched += [(W, 'H56', '=H5', 'dropdown'), (W, 'I56', 'None', '=MATCH(H56, T56:T57, 0)')]
setc(ws, 'B57', 'Exit EV / EBITDA multiple — input used under lever 1 (Barclays uses 10×)'); setc(ws, 'H57', 9, 'input', F_X)
setc(ws, 'B58', 'Enterprise value the current price requires = price × FDSO − (cash − debt − NCI − ACV)'); setc(ws, 'H58', '=H52*H50-(H45+H46+H47+H48)', 'formula', F_MONEY)
setc(ws, 'B59', 'Solved flat revenue growth (lever 1): root of the two-year UFCF-plus-exit-value quadratic in (1 + g)')
setc(ws, 'H59', f'=(-{B}+SQRT({B}^2-4*{A}*{C}))/(2*{A})-1', 'link', F_PCT2, b=True)
setc(ws, 'B60', "Solved exit multiple (lever 2): (required EV − PV of UFCF on Barclays' path) ÷ (FY28E EBITDA × discount factor)")
setc(ws, 'H60', f'=($H$58-(($I$61*{a1}+{b1})*$I$31+($J$61*{a2}+{b2})*$J$31))/($J$61*$J$14*$J$31)', 'link', F_X, b=True)
setc(ws, 'B61', "Barclays revenue path, FY27E / FY28E ($M; the 25 Aug 2026 note, as typed in your model)"); setc(ws, 'I61', 4759, 'input', F_MONEY); setc(ws, 'J61', 4939, 'input', F_MONEY)
setc(ws, 'B62', 'DCF base-case revenue CAGR, FY26–FY31'); setc(ws, 'H62', '=(DCF!M6/DCF!H6)^(1/5)-1', 'link', F_PCT2)
setc(ws, 'B63', 'DCF base-case FY2031E EBITDA'); setc(ws, 'H63', '=DCF!M31', 'link', F_MONEY)
setc(ws, 'B64', "Implied exit multiple if you keep the DCF's cash flows and WACC"); setc(ws, 'H64', '=((Cover!D6*Cover!D15-Cover!D12+Cover!D13+Cover!D14-DCF!H95)-DCF!H86)/DCF!M63/DCF!M31', 'link', F_X)
setc(ws, 'B65', "Implied perpetuity growth on the DCF's cash flows at that multiple"); setc(ws, 'H65', '=(H64*DCF!M31*N31-DCF!M59)/(H64*DCF!M31+DCF!M59)', 'link', F_PCT2)
setc(ws, 'B66', 'Sensitivity — implied share price by flat revenue growth (exit multiple in H36) and by exit multiple (Barclays revenue path)')
setc(ws, 'B67', 'Flat revenue growth →'); setc(ws, 'B68', 'Implied share price ($)'); setc(ws, 'B69', 'Exit EV / EBITDA multiple →'); setc(ws, 'B70', "Implied share price on Barclays' revenue path ($)")
for c, g, mult in zip('DEFGHIJK', (-0.04, -0.02, 0, 0.02, 0.03, 0.04, 0.06, 0.08), (8, 9, 10, 11, 12, 13, 14, 15)):
    setc(ws, f'{c}67', g, 'input', F_PCT); setc(ws, f'{c}69', mult, 'input', F_X)
    setc(ws, f'{c}68', f'=(($H$10*(1+{c}$67)*{a1}+{b1})*$I$31+($H$10*(1+{c}$67)^2*{a2}+{b2})*$J$31+$H$36*$J$14*$H$10*(1+{c}$67)^2*$J$31+$H$45+$H$46+$H$47+$H$48)/$H$50', 'link', F_USD)
    setc(ws, f'{c}70', f'=((($I$61*{a1}+{b1})*$I$31+($J$61*{a2}+{b2})*$J$31)+{c}$69*$J$14*$J$61*$J$31+$H$45+$H$46+$H$47+$H$48)/$H$50', 'link', F_USD)
for ref in ('O67', 'H61'):
    if ws[ref].value is not None: touched.append((W, ref, str(ws[ref].value)[:50], 'cleared')); ws[ref].value = None
# ---------------------------------------------------------------- 4. compaction: shorter WACC labels (detail → notes), widths, dashes
short = {'M17': 'Risk-free rate (10-yr US Treasury, 1 Oct 2026)', 'M18': 'Equity risk premium (Damodaran, Jan 2026)', 'M19': 'Industry beta (Damodaran, Jan 2026)', 'M25': 'Peer betas, 5-yr monthly: RBA / KAR / ACVA / CVNA',
         'M26': 'Selected unlevered beta (avg of two closest)', 'M29': 'Pre-tax cost of debt (revolver proxy; weight ≈ 0)', 'M32': "Memo: DCF's previous WACC inputs → 8.725%", 'M36': '(+) State income taxes ÷ pre-tax income',
         'M38': '(−) Excess option tax benefit ÷ pre-tax income', 'M39': 'Structural effective tax rate → DCF, 3SM', 'M41': 'Cash taxes paid ÷ pre-tax income, FY26 / FY25', 'M42': 'Barclays-implied tax rate, FY2027E'}
for ref, text in short.items():
    old = ws[ref].value; note = ws[f'R{ref[1:]}'].value or ''
    if old and old.strip() != text: setc(ws, ref, text); ws[f'R{ref[1:]}'].value = (f'{old.strip()}. {note}' if note and old.strip() not in note else (old.strip() if not note else note)); ws[f'R{ref[1:]}'].font = font(C_NOTE, i=True, sz=10)
for col, w in (('L', 2.5), ('M', 46), ('R', 44), ('T', 40)): ws.column_dimensions[col].width = w
n = 0
for r in range(10, 71):
    for lab_col, c0, c1 in (('B', 4, 11), ('M', 14, 17)):
        lab = ws[f'{lab_col}{r}']
        if lab.value is None or (lab.fill is not None and lab.fill.fill_type == 'solid') or r in (8, 9): continue
        cells = [ws.cell(r, c) for c in range(c0, c1 + 1)]
        if not any(c.value is not None for c in cells): continue
        for c in cells:
            if c.value is None and not isinstance(c, MergedCell): c.value = DASH; c.font = font(C_NOTE, i=True, sz=10); c.alignment = Alignment(horizontal='center'); n += 1
wb.save(P); print(f'saved {P.name}; {len(touched)} cells edited, {n} dashes added on the WACC tab')
for t in touched: print('  ', t)
