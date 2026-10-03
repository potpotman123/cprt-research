"""DCF: remove the exit-multiple method (selector, multiple input, exit TV, selected TV, exit-multiple sensitivity). Terminal value is
Gordon growth only; the implied exit multiple stays as an output. The block compresses by four rows and everything beneath moves up;
all references into the moved rows (other tabs and the DCF's own cash roll) are remapped. Usage: python fix_v5_dcf_gordon_2026-10-02.py <xlsx>"""
import sys, pathlib, re; sys.path.insert(0, str(pathlib.Path(__file__).parent))
import openpyxl
from openpyxl.formatting.formatting import ConditionalFormattingList
from cprt_model.common import *
P = pathlib.Path(sys.argv[1]); wb = openpyxl.load_workbook(P); d = wb['DCF']; W = 'WACC, Tax, and Reverse DCF'; WN = f"'{W}'!N31"
SHIFT = 4; FIRST_MOVED = 89
# ---- 1. new Gordon-only terminal block, rows 75–84 (old 76–88 cleared first)
note78 = d['P78'].value
for r in range(76, 89):
    for c in range(2, 20): d.cell(r, c).value = None
put(d, 'B75', 'Terminal value & valuation (perpetuity growth)', 'label', b=True)
blk = [(76, 'Perpetuity growth rate (FY2031E revenue growth of the selected case)', '=M7', 'formula', F_PCT2, note78),
       (77, 'Terminal year UFCF (FY2031E)', '=M59', 'formula', F_MONEY, None),
       (78, 'Terminal value = UFCF × (1 + g) ÷ (WACC − g)', f'=H77*(1+H76)/({WN}-H76)', 'link', F_MONEY, None),
       (79, 'Terminal year EBITDA (FY2031E)', '=M31', 'formula', F_MONEY, None),
       (80, '   Implied exit EV / EBITDA multiple (output)', '=H78/H79', 'formula', F_X, 'Terminal value ÷ FY2031E EBITDA; read against Barclays\' 10× and the 13× the market pays'),
       (81, 'PV of terminal value', '=H78*M63', 'formula', F_MONEY, None),
       (82, 'PV of explicit UFCF (FY27–FY31)', '=SUM(I64:M64)', 'formula', F_MONEY, None),
       (83, 'Enterprise value', '=H81+H82', 'formula', F_MONEY, None),
       (84, '   terminal value as % of EV', '=H81/H83', 'formula', F_PCT, None)]
for r, lab, f, kind, fmt, note in blk:
    put(d, f'B{r}', lab, 'label', b=(r in (78, 83))); put(d, f'H{r}', f, kind, fmt, b=(r in (78, 83)))
    if note: put(d, f'P{r}', note, 'note')
# ---- 2. move rows 89–120 up by four (relative refs inside the block translate; absolute refs handled below)
cf_rules = [(str(rng.sqref), rules) for rng, rules in d.conditional_formatting._cf_rules.items()]
d.conditional_formatting = ConditionalFormattingList()
ROWMAP = {84: 80, 85: 81, 86: 82, 87: 83, 88: 84}
def remap_same(f):
    """Shift same-sheet references: rows >= 89 move up four; the old PV/EV rows map onto the new block; cross-sheet refs untouched."""
    s = re.sub(r"'[^']+'![\$A-Z]+\$?\d+|(?<![A-Za-z])[A-Za-z0-9_]+![\$A-Z]+\$?\d+", lambda m: m.group(0).replace('$', '§').replace('!', '¡'), f)
    def sub(m):
        row = int(m.group(2)); row = row - SHIFT if row >= FIRST_MOVED else ROWMAP.get(row, row); return f"{m.group(1)}{row}"
    s = re.sub(r"(?<![A-Za-z!¡§])(\$?[A-Z]{1,2}\$?)(\d{1,3})\b", sub, s)
    return s.replace('§', '$').replace('¡', '!')
d.move_range(f'A{FIRST_MOVED}:S{d.max_row}', rows=-SHIFT, translate=False)
for row in d.iter_rows(min_row=FIRST_MOVED - SHIFT, max_row=d.max_row):
    for c in row:
        if isinstance(c.value, str) and c.value.startswith('='): c.value = remap_same(c.value)
for sq, rules in cf_rules:
    m = re.match(r'([A-Z]+)(\d+):([A-Z]+)(\d+)', sq); new = f'{m.group(1)}{int(m.group(2)) - SHIFT}:{m.group(3)}{int(m.group(4)) - SHIFT}' if int(m.group(2)) >= FIRST_MOVED else sq
    for rule in rules: d.conditional_formatting.add(new, rule)
# ---- 3. remap references into the moved rows: other tabs ('DCF'!X) and the DCF's own rows above the move
def remap_ext(f):
    def sub(m):
        col, dol, row = m.group(2), m.group(3), int(m.group(4)); row = row - SHIFT if row >= FIRST_MOVED else {84: 80, 86: 82}.get(row, row)
        return f"{m.group(1)}{col}{dol}{row}"
    return re.sub(r"((?:'DCF'|DCF)!\$?)([A-Z]{1,2})(\$?)(\d+)", sub, f)
def remap_int(f):
    s = re.sub(r"'[^']+'![\$A-Z]+\$?\d+", lambda m: m.group(0).replace('$', '§'), f)        # shield cross-sheet refs
    s = re.sub(r"(?<![A-Za-z!'§])(\$?[A-Z]{1,2}\$?)(\d{2,3})\b", lambda m: f"{m.group(1)}{int(m.group(2)) - SHIFT}" if int(m.group(2)) >= FIRST_MOVED else m.group(0), s)
    return s.replace('§', '$')
n_ext = n_int = 0
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if not (isinstance(c.value, str) and c.value.startswith('=')): continue
            if ws.title != 'DCF' and 'DCF!' in c.value:
                new = remap_ext(c.value)
                if new != c.value: c.value = new; n_ext += 1
            elif ws.title == 'DCF' and c.row < 75:
                new = remap_same(c.value)
                if new != c.value: c.value = new; n_int += 1
# ---- 4. sensitivity: perpetuity growth (down) × WACC (across), rows 103–109 after the move
put(d, 'B103', 'Sensitivity — implied share price: perpetuity growth (down) × WACC (across)', 'label', b=True); put(d, 'B104', 'Growth \\ WACC', 'label')
for i, g in enumerate((0.01, 0.015, 0.02, 0.025, 0.03)):
    r = 105 + i; put(d, f'C{r}', g, 'input', F_PCT2)
    for c in 'DEFGH': put(d, f'{c}{r}', f'=(($H$77*(1+$C{r})/({c}$104-$C{r}))/(1+{c}$104)^$M$62+SUMPRODUCT($I$59:$M$59,1/(1+{c}$104)^$I$62:$M$62)+$H$88+$H$89+$H$90+$H$91)/$H$93', 'formula', F_USD)
put(d, 'B112', 'Sensitivity uses the perpetuity method; the base growth is the FY2031E revenue growth in H76', 'note')
for r in range(113, 121):
    for c in range(1, 20): d.cell(r, c).value = None
wb.save(P); print(f'saved {P.name}: external refs remapped {n_ext}, DCF cash-roll refs remapped {n_int}')
