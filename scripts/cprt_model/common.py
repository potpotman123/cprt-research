"""Shared styles, periods and helpers for the CPRT model workbook build (Black Diamond / Via conventions)."""
import csv, json, pathlib, datetime
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
ROOT = pathlib.Path(__file__).resolve().parents[2]
FONT = 'Garamond'
NAVY, BLUE, GREY, LIGHT = '0E2841', '215E99', 'D0D0D0', 'F2F2F2'
C_INPUT, C_LINK, C_TOGGLE, C_ENGINE, C_NOTE, C_BLACK, C_WHITE = '0000FF', '008000', 'FF0000', '7030A0', '595959', '000000', 'FFFFFF'
F_PCT, F_PCT2, F_MONEY, F_INT, F_USD, F_X = '0.0%_);\\(0.0%\\);\\-_)', '0.00%_);\\(0.00%\\);\\-_)', '#,##0.0_);\\(#,##0.0\\);\\-_)', '#,##0_);\\(#,##0\\);\\-_)', '"$"#,##0_);\\("$"#,##0\\);\\-_)', '0.000'
thin = Side(style='thin'); BOT = Border(bottom=thin); TOP = Border(top=thin); TB = Border(top=thin, bottom=thin)

# ---- periods: 12 fiscal quarters FQ1 FY26 .. FQ4 FY28 in columns D..O, annual FY26A/FY27E/FY28E in P..R, notes in S
QUARTERS = [(fy, q) for fy in (2026, 2027, 2028) for q in (1, 2, 3, 4)]
def qlabel(fy, q): return f"FQ{q} FY{str(fy)[2:]}{'A' if fy <= 2026 else 'E'}"
QCOL = {fq: L(4 + i) for i, fq in enumerate(QUARTERS)}           # D..O
ACOL = {2026: 'P', 2027: 'Q', 2028: 'R'}; NOTE_COL = 'S'
CYEARS = list(range(2019, 2029)); CYCOL = {y: L(4 + i) for i, y in enumerate(CYEARS)}   # D..M on calendar tabs
def q_end(fy, q): return datetime.date(fy - 1 + (1 if q >= 2 else 0), {1: 10, 2: 1, 3: 4, 4: 7}[q], 31 if q in (1, 2, 4) else 30)
def cy_weights(fy, q):
    """Fleet interpolation weights by calendar year for a fiscal quarter: average over the quarter's three month-midpoints
    of a linear interpolation between year-end fleets (reproduces linked_service_revenue inputs.json periods[].weights)."""
    end = q_end(fy, q); w = {}
    for k in (2, 1, 0):
        m = end.month - k; y = end.year
        while m <= 0: m += 12; y -= 1
        frac = (m - 0.5) / 12.0                     # position of the month midpoint inside calendar year y
        w[y - 1] = w.get(y - 1, 0) + (1 - frac) / 3; w[y] = w.get(y, 0) + frac / 3
    return w

def font(color=C_BLACK, b=False, i=False, sz=11, u=None): return Font(name=FONT, size=sz, bold=b, italic=i, color=color, underline=u)
def fill(c): return PatternFill('solid', fgColor=c)
def setup(ws, label_w=56, ncols=16, zoom=90, notes_col=NOTE_COL):
    ws.sheet_view.showGridLines = False; ws.sheet_view.zoomScale = zoom
    ws.column_dimensions['A'].width = 2.5; ws.column_dimensions['B'].width = label_w; ws.column_dimensions['C'].width = 8
    for i in range(4, ncols + 4): ws.column_dimensions[L(i)].width = 13
    ws.column_dimensions[notes_col].width = 48
def title(ws, text, equation, last_col='S'):
    for c in range(2, 20): ws.cell(1, c).fill = fill(NAVY)
    ws['B1'] = text; ws['B1'].font = font(C_WHITE, b=True, sz=13)
    ws['B2'] = equation; ws['B2'].font = font(C_NOTE, i=True, sz=10)
def header(ws, row, cols, hist_span=None, proj_span=None, notes_col=NOTE_COL):
    """Row with Units / Historicals / Projected / Notes labels (row 4 style)."""
    ws.cell(row, 3, 'Units').font = font(i=True); ws.cell(row, 3).alignment = Alignment(horizontal='center'); ws.cell(row, 3).border = BOT
    for span, text in ((hist_span, 'Historicals'), (proj_span, 'Projected')):
        if span:
            c0, c1 = span; ws.cell(row, c0, text).font = font(b=True); ws.cell(row, c0).alignment = Alignment(horizontal='center')
            ws.merge_cells(start_row=row, start_column=c0, end_row=row, end_column=c1)
            for c in range(c0, c1 + 1): ws.cell(row, c).border = BOT
    ws[f'{notes_col}{row}'] = 'Notes / sources'; ws[f'{notes_col}{row}'].font = font(C_NOTE, i=True, sz=10); ws[f'{notes_col}{row}'].border = BOT
def section(ws, row, label, period_labels=None, first_col=4):
    """Blue section bar with period labels (row 5 style)."""
    ws.cell(row, 2, label).font = font(C_WHITE, b=True)
    for c in range(2, 20): ws.cell(row, c).fill = fill(BLUE); ws.cell(row, c).border = BOT
    if period_labels:
        for i, p in enumerate(period_labels):
            cell = ws.cell(row, first_col + i, p); cell.font = font(C_WHITE, b=True); cell.alignment = Alignment(horizontal='right')
def group(ws, row, label):
    ws.cell(row, 2, label).font = font(b=True)
    for c in range(2, 20): ws.cell(row, c).fill = fill(GREY); ws.cell(row, c).border = TB
WRITTEN = set()   # (sheet, cell) written by the build; the recolour pass may touch these on owner tabs
def put(ws, ref, value, kind='formula', fmt=None, b=False, i=False, indent=0):
    c = ws[ref]; c.value = value; WRITTEN.add((ws.title, ref))
    color = {'input': C_INPUT, 'formula': C_BLACK, 'link': C_LINK, 'toggle': C_TOGGLE, 'engine': C_INPUT, 'note': C_NOTE, 'label': C_BLACK}[kind]
    c.font = font(color, b=b, i=i or kind == 'note', sz=10 if kind == 'note' else 11)
    if fmt: c.number_format = fmt
    if indent: c.alignment = Alignment(indent=indent)
    return c
def label(ws, row, text, units='', b=False, i=False, indent=0, note='', notes_col=None):
    notes_col = notes_col or NOTES_COL.get(ws.title, NOTE_COL)
    put(ws, f'B{row}', text, 'label', b=b, i=i, indent=indent)
    if units: put(ws, f'C{row}', units, 'label', i=True).alignment = Alignment(horizontal='center')
    if note: put(ws, f'{notes_col}{row}', note, 'note')
def tab_color(ws, c): ws.sheet_properties.tabColor = c
def divider(wb, name, color, index=None):
    ws = wb.create_sheet(name, index); ws.sheet_view.showGridLines = False; tab_color(ws, color)
    ws['B3'] = name; ws['B3'].font = font(b=True, sz=14); ws.column_dimensions['B'].width = 40; return ws
def read_csv(path):
    with open(ROOT / path) as f: return [r for r in csv.DictReader(l for l in f if not l.startswith('#'))]
def write_table(ws, r0, c0, headers, rows, kind='input', fmt_by_col=None, header_fill=LIGHT):
    for j, h in enumerate(headers):
        cell = ws.cell(r0, c0 + j, h); cell.font = font(b=True); cell.fill = fill(header_fill); cell.border = BOT; cell.alignment = Alignment(horizontal='right' if j else 'left')
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            cell = ws.cell(r0 + 1 + i, c0 + j, v); cell.font = font(C_INPUT if (kind == 'input' and isinstance(v, (int, float))) else (C_INPUT if kind == 'engine' and isinstance(v, (int, float)) else C_BLACK))
            if fmt_by_col and j in fmt_by_col and isinstance(v, (int, float)): cell.number_format = fmt_by_col[j]
    return r0 + 1 + len(rows)
def num(x):
    try: return float(x)
    except (TypeError, ValueError): return x

# ---- cross-tab row contracts (engines publish on these rows; consumers reference them)
E2_POOL_RATIO_ROW = 75     # E2: total-loss pool, ratio to same quarter prior year
E3_SR_BASE_ROW, E3_SR_A_ROW = 48, 49     # E3: Copart share ratio y/y, base and thesis-A
E3_SELLER_BASE_ROW, E3_SELLER_A_ROW = 55, 56   # E3: effective seller commission rate, base and thesis-A
E4_DU_ROW, E4_DP_ROW = 40, 41            # E4: relative change in total-loss units and in auction prices (thesis B)
def prev_q(fy, q): return (fy - 1, q)
def quarter_labels(): return [qlabel(fy, q) for fy, q in QUARTERS] + ['FY26A', 'FY27E', 'FY28E']
def std_header(ws, equation, title_text):
    title(ws, title_text, equation); header(ws, 4, None, hist_span=(4, 7), proj_span=(8, 15))
def annual_sum(ws, row, fmt=F_MONEY, b=False):
    for fy, col in ACOL.items():
        cols = [QCOL[(fy, q)] for q in (1, 2, 3, 4)]; put(ws, f'{col}{row}', f'=SUM({cols[0]}{row}:{cols[3]}{row})', fmt=fmt, b=b)
def annual_avg(ws, row, fmt=F_PCT):
    for fy, col in ACOL.items():
        cols = [QCOL[(fy, q)] for q in (1, 2, 3, 4)]; put(ws, f'{col}{row}', f'=AVERAGE({cols[0]}{row}:{cols[3]}{row})', fmt=fmt, i=True)

# ---- thesis-1 coverage rows published by E2 (year-over-year coverage ratios by path)
E2_COV_STICKY_ROW, E2_COV_PREMIUM_ROW, E2_COV_RECOVERY_ROW = 116, 117, 118
NOTES_COL = {}   # sheet title -> notes column letter, recorded by setup()
_setup = setup
def setup(ws, label_w=56, ncols=16, zoom=90, notes_col='S'):
    NOTES_COL[ws.title] = notes_col; return _setup(ws, label_w, ncols, zoom, notes_col)

KEY_COLS = {'E1a Fleet (roll)': (2, 3), 'D Engine': (2,)}
def recolor(wb, full_sheets, owner_sheets=()):
    """Colour by content: formula referencing another tab = green; other formula = black; typed number = blue (red toggles kept);
    typed integers in label columns B–C and year-like headers in rows 1–5 are labels (black / unchanged). Full pass on generated tabs;
    on owner tabs only cells the build wrote. Returns a count of recoloured cells by sheet."""
    out = {}
    for ws in wb.worksheets:
        if ws.title not in full_sheets and ws.title not in owner_sheets: continue
        n = 0
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if v is None or isinstance(v, bool) or (ws.title in owner_sheets and (ws.title, c.coordinate) not in WRITTEN): continue
                cur = c.font.color.rgb[-6:] if (c.font and c.font.color is not None and isinstance(c.font.color.rgb, str)) else None
                if isinstance(v, str) and v.startswith('='): new = C_LINK if '!' in v else C_BLACK
                elif isinstance(v, (int, float)):
                    if c.row <= 5 and isinstance(v, int) and 1900 <= v <= 2100: continue          # year header
                    if c.column in KEY_COLS.get(ws.title, ()): new = C_BLACK                           # table keys (body/age index, engine mask)
                    elif cur == C_TOGGLE: continue
                    else: new = C_INPUT
                else: continue
                if cur != new:
                    f = c.font; c.font = Font(name=f.name, size=f.size, bold=f.bold, italic=f.italic, underline=f.underline, color=new); n += 1
        if n: out[ws.title] = n
    return out

from openpyxl.worksheet.datavalidation import DataValidation
def dropdown(ws, cell, options, index_cell=None, default_index=1, list_col='U', list_row=4, title='Selector options (list source; do not edit)'):
    """Clickable data-validation list on `cell` (red, bold). The option texts live in `list_col` below `list_row` on the same tab and the list
    points at that range; `index_cell` gets =MATCH(cell, range, 0) so dependent formulas keep a 1..n index."""
    r0, r1 = list_row + 1, list_row + len(options); rng = f'${list_col}${r0}:${list_col}${r1}'
    put(ws, f'{list_col}{list_row}', title, 'note')
    for i, o in enumerate(options): put(ws, f'{list_col}{r0 + i}', o, 'note')
    ws.data_validations.dataValidation = [d for d in ws.data_validations.dataValidation if cell not in str(d.sqref)]
    dv = DataValidation(type='list', formula1=rng, allow_blank=False); dv.showErrorMessage = True; dv.errorTitle = 'Selector'; dv.error = 'Choose a value from the list'
    dv.showInputMessage = True; dv.promptTitle = 'Selector'; dv.prompt = 'Click the arrow and choose a case'; ws.add_data_validation(dv); dv.add(cell)
    put(ws, cell, options[default_index - 1], 'toggle', b=True)
    if index_cell: put(ws, index_cell, f'=MATCH({cell},{rng},0)', 'formula', '0')
    ws.column_dimensions[list_col].width = max(ws.column_dimensions[list_col].width or 0, 46)
def toggle_lists(wb, sheets):
    """Attach a clickable 0/1 list to every red integer toggle (1/2/3 for the Scenarios coverage-path codes in column H)."""
    n = 0
    for name in sheets:
        ws = wb[name]; dv01 = DataValidation(type='list', formula1='"0,1"', allow_blank=False); dv123 = DataValidation(type='list', formula1='"1,2,3"', allow_blank=False)
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, (int, float)) and not isinstance(c.value, bool) and c.font.color is not None and isinstance(c.font.color.rgb, str) and c.font.color.rgb[-6:] == C_TOGGLE:
                    if name == 'Scenarios' and c.column == 8 and c.value in (1, 2, 3): dv123.add(c.coordinate); n += 1
                    elif c.value in (0, 1): dv01.add(c.coordinate); n += 1
        for dv in (dv01, dv123):
            if str(dv.sqref): dv.showErrorMessage = True; dv.error = 'Choose 0 or 1' if dv is dv01 else 'Choose 1, 2 or 3'; ws.add_data_validation(dv)
    return n
