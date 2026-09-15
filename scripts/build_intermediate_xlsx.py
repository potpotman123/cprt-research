#!/usr/bin/env python3
"""Build model/CPRT_Intermediate.xlsx — the intermediate workbook the user copies from into "CPRT Model".

Every committed dataset in data/csv/ goes in as a Data_* tab with its provenance line. The mechanism-A machinery
(fleet roll -> baseline TLF), the Solver calibration for R and P, the totaling-spread regression and the RPU chain
are built as LIVE FORMULAS off those data tabs. No named ranges (so sheets survive "Move or Copy" into another
workbook); every cross-sheet reference is explicit.

Colour convention: BLUE = hard-coded input · BLACK = formula · GREEN = link to another sheet · YELLOW fill =
calibrated parameter (fitted, with the fit reproducible on the Calibration tab).

Usage:  ./.venv/bin/python scripts/build_intermediate_xlsx.py
Verify: ./.venv/bin/python scripts/verify_intermediate_xlsx.py   (pycel evaluation of the key outputs)
"""
import csv, pathlib, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / 'data/csv'; OUT = ROOT / 'model/CPRT_Intermediate.xlsx'
TODAY = datetime.date.today().isoformat()

# fitted parameters come from the header of data/csv/age_curves.csv (written by scripts/age_curves.py) so the workbook
# always matches the script:  "R(a) = exposure(a) * exp(-0.0903*max(a-6,0)) ...; P(a) = 0.048 + (0.480-0.048)/(1+exp(-(a-9.22)/3.73))"
import re as _re
_hdr = " ".join(l for l in open(CSV / 'age_curves.csv', encoding='utf-8') if l.startswith('#'))
FIT = dict(
    k_cars=float(_re.search(r"k_cars=([\d.]+)", _hdr).group(1)), k_lt=float(_re.search(r"k_LT=([\d.]+)", _hdr).group(1)),
    r_slope=float(_re.search(r"exp\(-([\d.]+)\*max\(a-6,0\)\)", _hdr).group(1)),
    pmin=float(_re.search(r"P\(a\) = ([\d.]+) \+", _hdr).group(1)), pmax=float(_re.search(r"P\(a\) = [\d.]+ \+ \(([\d.]+)-", _hdr).group(1)),
    pmid=float(_re.search(r"exp\(-\(a-([\d.]+)\)/", _hdr).group(1)), pwid=float(_re.search(r"exp\(-\(a-[\d.]+\)/([\d.]+)\)", _hdr).group(1)))
print("fitted parameters from age_curves.csv:", FIT)

# ---------------------------------------------------------------- styles
FONT = 'Arial'
BLUE = Font(name=FONT, size=10, color='0000FF'); BLK = Font(name=FONT, size=10); GRN = Font(name=FONT, size=10, color='008000')
BOLD = Font(name=FONT, size=10, bold=True); TITLE = Font(name=FONT, size=13, bold=True); NOTE = Font(name=FONT, size=9, italic=True, color='555555')
YEL = PatternFill('solid', fgColor='FFFF00'); LIGHT = PatternFill('solid', fgColor='EEEEEE'); HDR = PatternFill('solid', fgColor='DDE4F0')
THIN = Side(style='thin', color='BBBBBB'); BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
PCT = '0.0%'; PCT2 = '0.00%'; NUM1 = '#,##0.0'; NUM0 = '#,##0'; DEC3 = '0.000'; DEC4 = '0.0000'; YR = '0'

def put(ws, ref, v, font=BLK, fmt=None, fill=None, wrap=False, bold=False, align=None):
    c = ws[ref]; c.value = v
    c.font = Font(name=font.name, size=font.size, bold=bold or font.bold, italic=font.italic, color=font.color)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap or align: c.alignment = Alignment(wrap_text=wrap, vertical='top', horizontal=align)
    return c

def widths(ws, spec):
    for col, w in spec.items(): ws.column_dimensions[col].width = w

def read_csv(name):
    prov, rows = [], []
    with open(CSV / name, encoding='utf-8') as fh:
        for line in fh:
            if line.startswith('#'): prov.append(line[1:].strip())
            else: rows.append(line)
    rd = list(csv.reader(rows)); return prov, rd[0], rd[1:]

def num(v):
    if v is None or v == '': return None
    try:
        f = float(v); return int(f) if f.is_integer() and '.' not in v and 'e' not in v.lower() else f
    except ValueError: return v

# ---------------------------------------------------------------- data tabs
DESC = {  # description + source for CSVs that carry no '#' provenance header
 'reported_units.csv': "Copart quarterly YoY series, HAND-TRANSCRIBED from earnings-call transcripts (no filing discloses them). Tier 2. scripts/reported_series.py",
 'quarterly_pl.csv': "Copart quarterly P&L lines from 8-K Ex-99.1 press releases (SEC EDGAR). Tier 1.",
 'quarterly_margin.csv': "Copart quarterly gross margin and facility-operations % of revenue, from 8-K Ex-99.1. Tier 1.",
 'quarterly_segments.csv': "Copart US / international service and vehicle-sales revenue from 8-K, where disclosed. Tier 1.",
 'segment_service_rev_8k.csv': "US and international service revenue, 8-K Ex-99.1 (FY26). Tier 1.",
 'facility_ops_quarterly.csv': "Facility operations expense by quarter, 8-K Ex-99.1. Tier 1.",
 'sec_annual.csv': "Copart annual figures from 10-K XBRL (SEC EDGAR). Tier 1.",
 'elasticity_rebuild.csv': "RPU/ASP elasticity inputs, n=17 FY22Q4-FY26Q4: service & total revenue YoY (8-K), global units and global ASP YoY (transcripts, aligned). Implied RPU = (1+rev)/(1+units)-1. scripts/analysis_20260911.py",
 'units_decomp_panel_v2.csv': "Six-quarter US insurance units decomposition (Copart ex-CAT vs claims x TLF pool) under three claims denominators. scripts/units_decomp_panel.py; findings.md Addendum 15/15a",
 'decomposition.csv': "Matched-denominator decomposition, CY2025 and FQ4 FY26 windows. scripts/analysis_20260911.py",
 'tlf_calibration.csv': "Regression outputs: dTLF(pp, YoY) = a + b x spread(t-1), CCC quarterly 2019Q1-2025Q3 (n=27). scripts/analysis_20260911.py",
 'totaling_spread_quarterly.csv': "Totaling spread = repair CPI YoY - used-car CPI YoY (BLS CUUR0000SETD minus CUUR0000SETA02, NSA), quarterly average of monthly values. months<3 = partial quarter. scripts/analysis_20260911.py",
 'cprt_cpi_three_series.csv': "BLS CPI flat files (download.bls.gov/pub/time.series/cu): SETA02 used cars & trucks, SETD motor vehicle maintenance & repair, SETE motor vehicle insurance; SA (CUSR) and NSA (CUUR); footnote code X marks the 2025 appropriations-lapse gap (left blank, never interpolated).",
 'fasttrack_collision_claims_cw.csv': "ISS Fast Track quarterly collision-claim-count headlines as reported by CollisionWeek (collisionweek.com/tag/losses/, headline + teaser only). Headline figures carry qualifiers.",
 'pgr_monthly_pif.csv': "Progressive personal-auto policies in force, monthly 8-K EX-99 (CIK 0000080661), SEC EDGAR.",
 'geico_frequency_series.csv': "Berkshire Hathaway 10-Q/10-K sentences on GEICO claims frequency, SEC EDGAR (CIK 0001067983).",
 'rba_automotive_series.csv': "RB Global (IAA parent) automotive lots / GTV / take rate from 8-K Ex-99.1 (CIK 0001046102). 5 of 18 quarters are pro forma - see basis column.",
 'duopoly_compare.csv': "RB Global automotive lots YoY vs Copart US insurance units YoY by matched quarter.",
 'duopoly_daily.csv': "Daily listed US inventory: Copart (lot.xml sitemap union) vs IAA (vehicledetail sitemap). scripts/job1_snapshot.py, job1_iaa.py. Listed inventory, not yard inventory.",
 'yard_panel_us.csv': "Copart US yards and dated sale events per sitemap snapshot (Wayback 2022-2025 + live).",
 'cadence_fixed.csv': "Sale-event cadence per yard per snapshot.",
 'lots_per_sale_event.csv': "Listed lots (union, overlap-gated) per 7-day sale events; events per yard per week.",
 'backtest_inventory_v2.csv': "Sitemap inventory YoY vs Copart reported US inventory YoY, overlap<=1% gate. scripts/backtest_inventory_v2.py",
 'fred_TOTALNSA.csv': "FRED TOTALNSA: light weight vehicle sales, autos and light trucks, thousands of units, monthly NSA (BEA).",
 'fred_LTRUCKNSA.csv': "FRED LTRUCKNSA: light weight vehicle sales, light trucks, thousands of units, monthly NSA (BEA). Fetched 2026-09-14.",
 'fred_HTRUCKSNSA.csv': "FRED HTRUCKSNSA: motor vehicle retail sales, heavy weight trucks (>14,000 lb GVW), thousands of units, monthly NSA (BEA). Fetched 2026-09-15. Ward's 'heavy' is >10,000 lb, so the 2021 overlap ratio (~1.8) is a class-3 definitional gap.",
 'capex_decomp.csv': "Copart capex decomposition from 10-K PP&E roll-forward (XBRL).",
 'owner_earnings.csv': "Owner-earnings bridge (EBIT less non-land capex above D&A), 10-K XBRL.",
}
DATA_TABS = [  # (sheet name, csv)
 ('Data_ReportedUnits', 'reported_units.csv'), ('Data_QuarterlyPL', 'quarterly_pl.csv'), ('Data_QuarterlyMargin', 'quarterly_margin.csv'),
 ('Data_Segments', 'quarterly_segments.csv'), ('Data_SegmentSvc8K', 'segment_service_rev_8k.csv'), ('Data_FacilityOps', 'facility_ops_quarterly.csv'),
 ('Data_SECAnnual', 'sec_annual.csv'), ('Data_Elasticity', 'elasticity_rebuild.csv'), ('Data_CCC_TLF_Annual', 'ccc_tlf_annual.csv'),
 ('Data_CCC_TLF_Quarterly', 'ccc_tlf_quarterly.csv'), ('Data_CPI', 'cprt_cpi_three_series.csv'), ('Data_Spread', 'totaling_spread_quarterly.csv'),
 ('Data_TLFCalibration', 'tlf_calibration.csv'), ('Data_UnitsPanel', 'units_decomp_panel_v2.csv'), ('Data_Decomposition', 'decomposition.csv'),
 ('Data_FastTrack', 'fasttrack_collision_claims_cw.csv'), ('Data_PGR_PIF', 'pgr_monthly_pif.csv'), ('Data_GEICO', 'geico_frequency_series.csv'),
 ('Data_RBA', 'rba_automotive_series.csv'), ('Data_DuopolyCompare', 'duopoly_compare.csv'), ('Data_DuopolyDaily', 'duopoly_daily.csv'),
 ('Data_Yards', 'yard_panel_us.csv'), ('Data_Cadence', 'cadence_fixed.csv'), ('Data_LotsPerEvent', 'lots_per_sale_event.csv'),
 ('Data_BacktestInv', 'backtest_inventory_v2.csv'), ('Data_FRED_TOTALNSA', 'fred_TOTALNSA.csv'), ('Data_FRED_LTRUCKNSA', 'fred_LTRUCKNSA.csv'), ('Data_FRED_HTRUCKSNSA', 'fred_HTRUCKSNSA.csv'),
 ('Data_EPA_Miles', 'ornl_tedb40_miles_by_age.csv'), ('Data_AgeCurvesPy', 'age_curves.csv'), ('Data_AgeCurvesValid', 'age_curves_validation.csv'),
 ('Data_Capex', 'capex_decomp.csv'), ('Data_OwnerEarnings', 'owner_earnings.csv'),
]

def add_data_sheet(wb, name, fname, title=None):
    prov, hdr, rows = read_csv(fname); ws = wb.create_sheet(name)
    put(ws, 'A1', title or f"{fname}", TITLE)
    put(ws, 'A2', " | ".join(prov) if prov else DESC.get(fname, "see PROVENANCE.md"), NOTE, wrap=True)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max(6, len(hdr))); ws.row_dimensions[2].height = 42
    put(ws, 'A3', f"data/csv/{fname} · {len(rows)} rows · BLUE = raw data as committed; do not type over it — edit the CSV and rebuild.", NOTE)
    for j, h in enumerate(hdr): put(ws, f"{L(j+1)}4", h, BOLD, fill=HDR)
    for i, r in enumerate(rows):
        for j, v in enumerate(r): put(ws, f"{L(j+1)}{5+i}", num(v), BLUE)
    ws.freeze_panes = 'A5'
    for j, h in enumerate(hdr): ws.column_dimensions[L(j+1)].width = min(40, max(10, len(h) + 2))
    return ws, 5, 4 + len(rows)

# ---------------------------------------------------------------- workbook
wb = Workbook(); ws = wb.active; ws.title = 'README'
Y0, Y1 = 2013, 2030; YEARS = list(range(Y0, Y1 + 1)); NY = len(YEARS); YC = [L(3 + i) for i in range(NY)]   # C..T
AGES = list(range(0, 46)); NA = len(AGES)
MY0, MY1 = 1970, 2030; MYS = list(range(MY0, MY1 + 1))

# ---- Inputs
wi = wb.create_sheet('Inputs')
put(wi, 'A1', 'Inputs — every parameter of the fleet roll in one place', TITLE)
put(wi, 'A2', 'BLUE = hard-coded input (change freely) · YELLOW = calibrated (fitted on the Calibration tab / scripts/age_curves.py; copy new Solver results here) · model tabs reference ONLY this sheet for parameters.', NOTE, wrap=True)
wi.merge_cells('A2:F2'); wi.row_dimensions[2].height = 30
rows = [
 (4,  'Survival stretch k, cars, 2013',      round(FIT['k_cars']/1.194, 3), DEC3, 'yellow', "fitted to the IHS/Polk 2013 census of cars by single year of age (ORNL TEDB40 T3.11); S_k(a)=S_EPA(a/k). docs/AGE_CURVES.md §2.2"),
 (5,  'Survival stretch k, light trucks, 2013', round(FIT['k_lt']/1.194, 3), DEC3, 'yellow', "fitted to the IHS 2013 census of trucks (T3.12, includes heavy). §2.2"),
 (6,  'k multiplier by drift-end year',       1.194, DEC3, 'yellow', "fitted so the 2024 roll hits VIO anchor and 66% aged 7+. 289M anchor is unverified (from memory); Experian 292.1M (on disk) gives 1.204 — same downstream. §2.4"),
 (7,  'Drift start year',                     2013,  YR,   'blue',   "k = 2013 value up to here"),
 (8,  'Drift end year',                       2024,  YR,   'blue',   "k reaches k_2013 × multiplier here; FLAT after (base case). Sensitivity: keep drifting"),
 (9,  'Exposure factor, age 0',               0.5,   '0.00', 'blue', "a model-year-t vehicle is on the road ~half of calendar year t. Necessary: without it the ≤3-yr repairable share fits at 36% vs CCC ~30%. §3.2"),
 (10, 'R kink age',                           6,     YR,   'blue',   "R is flat through this age (a free 0–6 slope is not identified by the CCC targets). §3.3"),
 (11, 'R slope after kink (per year of age)', FIT['r_slope'], DEC4, 'yellow', "R(a) = e(a)·exp(−slope·max(a−kink,0)). Solver-fitted on Calibration tab. §3.3"),
 (12, 'P floor (pmin)',                       FIT['pmin'], DEC3, 'yellow', "P(a) = pmin + (pmax−pmin)/(1+exp(−(a−mid)/width)). Solver-fitted. §4.3"),
 (13, 'P ceiling (pmax)',                     FIT['pmax'], DEC3, 'yellow', ""),
 (14, 'P midpoint age (mid)',                 FIT['pmid'],  '0.00', 'yellow', ""),
 (15, 'P width (yrs)',                        FIT['pwid'],  '0.00', 'yellow', ""),
 (16, 'Future new-vehicle sales, cars (thousands per year, 2026+)', None, NUM0, 'blue', "ASSUMED = 2025 level (Data_Sales). Flex for a sales-recovery case"),
 (17, 'Future new-vehicle sales, light trucks (thousands per year, 2026+)', None, NUM0, 'blue', "ASSUMED = 2025 level"),
 (18, 'VIO anchor, end-2024 (M light vehicles)', 289, NUM0, 'blue', "S&P Global Mobility 2025 avg-age release — NOT ON DISK, confirm; Experian Q3-2024 = 292.1M (Crash Course 2025/Q1)"),
 (19, 'Share aged 7+ anchor, 2024',           0.66,  PCT,  'blue',   "'66% of vehicles in operation are seven years or older' — S&P via CCC Crash Course 2024/Q4"),
]
put(wi, 'A3', 'Parameter', BOLD, fill=HDR); put(wi, 'B3', 'Value', BOLD, fill=HDR); put(wi, 'C3', 'Source / note', BOLD, fill=HDR)
for r, lab, v, fmt, kind, note in rows:
    put(wi, f'A{r}', lab, BLK); put(wi, f'C{r}', note, NOTE, wrap=True)
    put(wi, f'B{r}', v, BLUE, fmt, fill=(YEL if kind == 'yellow' else None))
# future sales default = 2025 values, pulled from the sales CSV
_, _, sales_rows = read_csv('light_vehicle_sales_by_year.csv'); S25 = [r for r in sales_rows if r[0] == '2025'][0]
wi['B16'].value = round(float(S25[1]), 1); wi['B17'].value = round(float(S25[2]), 1)
put(wi, 'A22', 'Survival stretch by calendar year (formulas)', BOLD)
put(wi, 'A23', 'Year', BOLD, fill=LIGHT); put(wi, 'A24', 'k multiplier', BLK); put(wi, 'A25', 'k cars', BLK); put(wi, 'A26', 'k light trucks', BLK)
for i, y in enumerate(YEARS):
    c = YC[i]
    put(wi, f'{c}23', y, BLUE, YR, fill=LIGHT)
    put(wi, f'{c}24', f'=1+($B$6-1)*MIN(MAX({c}23-$B$7,0),$B$8-$B$7)/($B$8-$B$7)', BLK, DEC4)
    put(wi, f'{c}25', f'=$B$4*{c}24', BLK, DEC4); put(wi, f'{c}26', f'=$B$5*{c}24', BLK, DEC4)
put(wi, 'A28', 'Sensitivity idea: set B8 = 2030 to let survival keep improving; set B6 = 1.0 for the raw EPA schedule. Baseline TLF drift moves 0.05–0.18pp/yr across that range; P buckets do not move. §6', NOTE, wrap=True); wi.merge_cells('A28:F28'); wi.row_dimensions[28].height = 30
widths(wi, {'A': 46, 'B': 12, 'C': 90}); wi.freeze_panes = 'A4'

# ---- Data_Sales (specific layout: MY 1970..2030)
wsl = wb.create_sheet('Data_Sales')
prov, hdr, rows = read_csv('light_vehicle_sales_by_year.csv')
put(wsl, 'A1', 'Cohort sizes — new light-vehicle sales by model year (thousands of vehicles)', TITLE)
put(wsl, 'A2', " | ".join(prov), NOTE, wrap=True); wsl.merge_cells('A2:F2'); wsl.row_dimensions[2].height = 42
put(wsl, 'A3', "Unit: thousands of vehicles (8,321 = 8,321,000 cars). Ward's reports to the single vehicle, so the source carries decimals (e.g. 8,720.3); they are kept in the cells and hidden by the format. Ward's via ORNL TEDB Ed.40 Table 3.6 for 1970–2021; FRED TOTALNSA / LTRUCKNSA / HTRUCKSNSA rescaled to Ward's basis on the 2021 overlap for 2022–2025 (estimates — the decimals there mean nothing); 2026+ = Inputs (green). Heavy trucks (>10,000 lb) are NOT in the fleet roll; the column exists for the 2013 census check only. data/csv/light_vehicle_sales_by_year.csv", NOTE, wrap=True)
wsl.merge_cells('A3:F3'); wsl.row_dimensions[3].height = 42
for j, h in enumerate(['model year', 'cars (thousands)', 'light trucks (thousands)', 'heavy trucks (thousands)', 'source']): put(wsl, f'{L(j+1)}4', h, BOLD, fill=HDR, wrap=True)
wsl.row_dimensions[4].height = 30
byy = {int(r[0]): r for r in rows}
SR0 = 5
for i, my in enumerate(MYS):
    r = SR0 + i; put(wsl, f'A{r}', my, BLUE, YR)
    if my in byy:
        put(wsl, f'B{r}', round(float(byy[my][1]), 1), BLUE, NUM0); put(wsl, f'C{r}', round(float(byy[my][2]), 1), BLUE, NUM0)
        put(wsl, f'D{r}', round(float(byy[my][3]), 1), BLUE, NUM0); put(wsl, f'E{r}', byy[my][4], NOTE)
    else:
        put(wsl, f'B{r}', '=Inputs!$B$16', GRN, NUM0); put(wsl, f'C{r}', '=Inputs!$B$17', GRN, NUM0); put(wsl, f'D{r}', None, BLUE, NUM0); put(wsl, f'E{r}', 'ASSUMED — Inputs B16/B17; heavy trucks not modelled (outside the light-vehicle roll)', NOTE)
SR1 = SR0 + len(MYS) - 1     # 65
widths(wsl, {'A': 8, 'B': 12, 'C': 14, 'D': 14, 'E': 44}); wsl.freeze_panes = 'A5'
SALES_Y = f"Data_Sales!$A${SR0}:$A${SR1}"; SALES_C = f"Data_Sales!$B${SR0}:$B${SR1}"; SALES_L = f"Data_Sales!$C${SR0}:$C${SR1}"

# ---- Data_EPA_Survival
wse = wb.create_sheet('Data_EPA_Survival')
prov, hdr, rows = read_csv('ornl_tedb40_survival_by_age.csv')
put(wse, 'A1', 'EPA survival rates by vehicle age — cars and light trucks', TITLE)
put(wse, 'A2', " | ".join(prov), NOTE, wrap=True); wse.merge_cells('A2:F2'); wse.row_dimensions[2].height = 42
put(wse, 'A3', 'Primary: U.S. EPA, Draft Technical Assessment Report, Midterm Evaluation of LD GHG / CAFE Standards MY2022–2025, EPA-420-D-16-900, July 2016 — republished as ORNL Transportation Energy Data Book Ed.40 Table 3.15. Values verbatim.', NOTE)
for j, h in enumerate(hdr): put(wse, f'{L(j+1)}4', h, BOLD, fill=HDR)
for i, r in enumerate(rows):
    put(wse, f'A{5+i}', int(r[0]), BLUE, YR); put(wse, f'B{5+i}', float(r[1]), BLUE, DEC3); put(wse, f'C{5+i}', float(r[2]), BLUE, DEC3)
EPA_C = "Data_EPA_Survival!$B$5:$B$36"; EPA_L = "Data_EPA_Survival!$C$5:$C$36"
widths(wse, {'A': 8, 'B': 16, 'C': 22}); wse.freeze_panes = 'A5'

# ---- Data_CCC_Targets
wt = wb.create_sheet('Data_CCC_Targets')
put(wt, 'A1', 'CCC Crash Course statistics used to fit and test R(age) and P(age)', TITLE)
put(wt, 'A2', 'Quotes verbatim from the ungated report pages (PROVENANCE.md §5). FIT rows are used by the Calibration tab; OOS rows are the out-of-sample tests on TLF_Roll. Tolerance = the error that costs one unit of Solver loss.', NOTE, wrap=True)
wt.merge_cells('A2:G2'); wt.row_dimensions[2].height = 30
for j, h in enumerate(['use', 'year', 'key', 'statistic', 'value', 'tolerance', 'quote', 'page']): put(wt, f'{L(j+1)}4', h, BOLD, fill=HDR)
TGT = [
 ('FIT', 2024, 'tlf',    'Total-loss frequency, all loss categories', 0.223, 0.005, 'printed data label, chart "Total Loss Frequency Remains High as Vehicle Values Trend Up" (2024 = 22.3%)', 'https://www.cccis.com/reports/crash-course-2026'),
 ('FIT', 2024, 'tl7',    'Share of total-loss valuations on vehicles 7+ yrs', 0.72, 0.01, 'almost 72% of valuations across all loss categories are for vehicles 7 years or older', 'https://www.cccis.com/reports/crash-course-2024/q4'),
 ('FIT', 2024, 'rp7',    'Share of repairable claims on vehicles 7+ yrs', 0.45, 0.01, 'vehicles seven years or older now make up nearly 45% of all repairable claims, up from 35% in 2019', 'https://www.cccis.com/reports/crash-course-2024/q4'),
 ('FIT', 2024, 'rp3',    'Share of repairable claims on vehicles ≤3 yrs (all fuel)', 0.30, 0.02, 'Only 26.3% of repairable ICE vehicles are three years or newer (EVs 79.4% / hybrids 60.3% ≤3 yrs → all-fuel ≈30%)', 'https://www.cccis.com/reports/crash-course-2024/q4'),
 ('FIT', 2024, 'age_cl', 'Average age of vehicles in claims (yrs)', 7.6, 0.15, 'For claims, the average age of vehicles has increased to 7.6 years – up from 6.9 years in 2020', 'https://www.cccis.com/reports/crash-course-2025/q1'),
 ('FIT', 2024, 'age_rp', 'Average age of repairable vehicles (yrs)', 6.8, 0.15, 'The average age of repairable vehicles was 6.8 years in 2024 (up from 6.1 years old in 2020)', 'https://www.cccis.com/reports/crash-course-2025/q1'),
 ('FIT', 2024, 'age_tl', 'Average age of total-loss vehicles (yrs)', 10.6, 0.15, '... and 10.6 years for total loss vehicles (up from 10.0 years old in 2020)', 'https://www.cccis.com/reports/crash-course-2025/q1'),
 ('FIT', 2024, 'p03',    'Total-loss rate for claims on vehicles ≤3 yrs', 0.10, 0.01, 'For claims that are three years old or newer, 1 in 10 are flagged as a total loss by the insurer', 'https://www.cccis.com/reports/crash-course-2026'),
 ('OOS', 2019, 'rp7',    'Share of repairable claims on vehicles 7+ yrs', 0.35, None, 'up from 35% in 2019', 'https://www.cccis.com/reports/crash-course-2024/q4'),
 ('OOS', 2019, 'rp3',    'Share of repairable claims on vehicles ≤3 yrs', 0.385, None, 'vehicles 3 years or newer represented 38.5% of the repairable mix in 2019', 'https://www.cccis.com/reports/crash-course-2025/q1'),
 ('OOS', 2020, 'age_cl', 'Average age of vehicles in claims (yrs)', 6.9, None, 'up from 6.9 years in 2020', 'https://www.cccis.com/reports/crash-course-2025/q1'),
 ('OOS', 2020, 'age_rp', 'Average age of repairable vehicles (yrs)', 6.1, None, 'up from 6.1 years old in 2020', 'https://www.cccis.com/reports/crash-course-2025/q1'),
 ('OOS', 2020, 'age_tl', 'Average age of total-loss vehicles (yrs)', 10.0, None, 'up from 10.0 years old in 2020', 'https://www.cccis.com/reports/crash-course-2025/q1'),
 ('OOS', 2025, 'tl7',    'Share of total-loss valuations on vehicles 7+ yrs', 0.72, None, 'over 72% of total loss valuations are on vehicles 7 years or older', 'https://www.cccis.com/reports/crash-course-2025/q4'),
 ('OOS', 2025, 'rp7',    'Share of repairable claims on vehicles 7+ yrs', 0.46, None, 'almost 46% of repairable vehicles are 7 years or older', 'https://www.cccis.com/reports/crash-course-2025/q4'),
 ('OOS', 2019, 'tlf',    'TLF all loss categories (demographics-only model vs actual)', 0.192, None, 'CCC annual 2019 = 19.2%; the gap is the non-demographic LEVEL (spread cycle, technology, filing)', 'Data_CCC_TLF_Annual'),
 ('OOS', 2020, 'tlf',    'TLF all loss categories', 0.206, None, 'CCC annual 2020 = 20.6%', 'Data_CCC_TLF_Annual'),
 ('OOS', 2025, 'tlf',    'TLF all loss categories', 0.231, None, 'CCC annual 2025 = 23.1%', 'Data_CCC_TLF_Annual'),
 ('S',   2024, 'vio',    'Light vehicles in operation (M)', 289, None, 'S&P 2025 release — NOT on disk (from memory); Experian 292.1M at Q3-2024 is on disk (Crash Course 2025/Q1)', 'https://www.cccis.com/reports/crash-course-2025/q1'),
 ('S',   2024, 'sh7',    'Share of fleet aged 7+', 0.66, None, '66% of vehicles in operation are seven years or older (S&P Mobility)', 'https://www.cccis.com/reports/crash-course-2024/q4'),
 ('S',   2025, 'viogr',  'VIO growth 2020→Q3-2025', 0.051, None, 'Vehicles in operation reached almost 296 million as of Q3 2025 (Experian), +5.1% relative to 2020', 'https://www.cccis.com/reports/crash-course-2026'),
]
for i, t in enumerate(TGT):
    r = 5 + i
    for j, v in enumerate(t):
        fmt = None
        if j == 4: fmt = ('0.0' if t[2].startswith('age') else ('#,##0' if t[2] == 'vio' else PCT))
        if j == 5: fmt = ('0.00' if t[2].startswith('age') else PCT2)
        put(wt, f'{L(j+1)}{r}', v, BLUE if j in (4, 5) else BLK, fmt, wrap=(j == 6))
TR0, TR1 = 5, 4 + len(TGT)
widths(wt, {'A': 5, 'B': 6, 'C': 8, 'D': 46, 'E': 9, 'F': 10, 'G': 80, 'H': 46}); wt.freeze_panes = 'A5'

# ---- Survival: S(a, t) for cars (rows 6..51) and light trucks (rows 55..100)
wsv = wb.create_sheet('Survival')
put(wsv, 'A1', 'Survival by age and calendar year — EPA schedule stretched by k(t)', TITLE)
put(wsv, 'A2', 'S(a,t) = S_EPA(a / k(t)), linearly interpolated between the table’s integer ages, zero beyond age 31·k. k(t) from Inputs row 25/26. Ages 0–45 (S is ~0 past 40).', NOTE, wrap=True)
wsv.merge_cells('A2:J2'); wsv.row_dimensions[2].height = 30
CR0, CR1 = 6, 6 + NA - 1      # cars rows 6..51
LR0, LR1 = CR1 + 4, CR1 + 4 + NA - 1   # LT rows 55..100
put(wsv, 'A3', 'Year →', BOLD, fill=LIGHT); put(wsv, 'A4', 'k cars (Inputs)', BOLD); put(wsv, f'A{CR0-1}', 'CARS: age', BOLD, fill=LIGHT)
put(wsv, f'A{LR0-2}', 'k light trucks (Inputs)', BOLD); put(wsv, f'A{LR0-1}', 'LIGHT TRUCKS: age', BOLD, fill=LIGHT)
for i, y in enumerate(YEARS):
    c = YC[i]
    put(wsv, f'{c}3', f'=Inputs!{c}23', GRN, YR, fill=LIGHT); put(wsv, f'{c}4', f'=Inputs!{c}25', GRN, DEC4); put(wsv, f'{c}{LR0-2}', f'=Inputs!{c}26', GRN, DEC4)
    put(wsv, f'{c}{CR0-1}', f'={c}3', BLK, YR, fill=LIGHT); put(wsv, f'{c}{LR0-1}', f'={c}3', BLK, YR, fill=LIGHT)
for i, a in enumerate(AGES):
    put(wsv, f'A{CR0+i}', a, BLUE, YR); put(wsv, f'A{LR0+i}', a, BLUE, YR)
    for c in YC:
        x = f'($A{CR0+i}/{c}$4)'
        put(wsv, f'{c}{CR0+i}', f'=IF({x}>=31,0,INDEX({EPA_C},INT({x})+1)+({x}-INT({x}))*(INDEX({EPA_C},INT({x})+2)-INDEX({EPA_C},INT({x})+1)))', BLK, DEC3)
        x = f'($A{LR0+i}/{c}${LR0-2})'
        put(wsv, f'{c}{LR0+i}', f'=IF({x}>=31,0,INDEX({EPA_L},INT({x})+1)+({x}-INT({x}))*(INDEX({EPA_L},INT({x})+2)-INDEX({EPA_L},INT({x})+1)))', BLK, DEC3)
widths(wsv, {'A': 22}); wsv.freeze_panes = f'B{CR0}'
SV_YEARS = f"Survival!$C$3:${YC[-1]}$3"; SV_CARS = f"Survival!$C${CR0}:${YC[-1]}${CR1}"; SV_LT = f"Survival!$C${LR0}:${YC[-1]}${LR1}"

# ---- Fleet: model year x calendar year (thousands, cars + light trucks)
wf = wb.create_sheet('Fleet')
put(wf, 'A1', 'Fleet roll — vehicles on the road by model year and calendar year (thousands, cars + light trucks)', TITLE)
put(wf, 'A2', 'cell = sales_cars(MY) × S_cars(t−MY, t) + sales_LT(MY) × S_LT(t−MY, t). Blank where the model year is after the calendar year. Row 68 = total VIO.', NOTE, wrap=True)
wf.merge_cells('A2:J2'); wf.row_dimensions[2].height = 30
FR0 = 6; FR1 = FR0 + len(MYS) - 1     # rows 6..66
put(wf, 'A4', 'Model year ↓  /  Year →', BOLD, fill=LIGHT)
for i, y in enumerate(YEARS): put(wf, f'{YC[i]}4', f'=Inputs!{YC[i]}23', GRN, YR, fill=LIGHT)
for i, my in enumerate(MYS):
    r = FR0 + i; put(wf, f'A{r}', my, BLUE, YR)
    for c in YC:
        age = f'({c}$4-$A{r})'
        put(wf, f'{c}{r}', f'=IF({c}$4<$A{r},"",IF({age}>45,0,INDEX({SALES_C},MATCH($A{r},{SALES_Y},0))*INDEX({SV_CARS},{age}+1,MATCH({c}$4,{SV_YEARS},0))+INDEX({SALES_L},MATCH($A{r},{SALES_Y},0))*INDEX({SV_LT},{age}+1,MATCH({c}$4,{SV_YEARS},0))))', BLK, NUM0)
put(wf, f'A{FR1+2}', 'Total VIO (thousands)', BOLD)
for c in YC: put(wf, f'{c}{FR1+2}', f'=SUM({c}{FR0}:{c}{FR1})', BLK, NUM0, bold=True)
widths(wf, {'A': 24}); wf.freeze_panes = f'B{FR0}'
FL_YEARS = f"Fleet!$C$4:${YC[-1]}$4"; FL_MY = f"Fleet!$A${FR0}:$A${FR1}"; FL_MAT = f"Fleet!$C${FR0}:${YC[-1]}${FR1}"

# ---- FleetByAge
wa = wb.create_sheet('FleetByAge')
put(wa, 'A1', 'Fleet by age and calendar year (thousands) + fleet statistics', TITLE)
put(wa, 'A2', 'fleet(a,t) = Fleet[MY = t−a, t]. Rows 53–57: VIO, share 7+, share 15+, count ≤6, average age (t−MY+0.5). Compare with Data_CCC_Targets rows marked S.', NOTE, wrap=True)
wa.merge_cells('A2:J2'); wa.row_dimensions[2].height = 30
AR0 = 6; AR1 = AR0 + NA - 1     # 6..51
put(wa, 'A4', 'Age ↓ / Year →', BOLD, fill=LIGHT); put(wa, 'B4', 'age+0.5', BOLD, fill=LIGHT)
for i, y in enumerate(YEARS): put(wa, f'{YC[i]}4', f'=Inputs!{YC[i]}23', GRN, YR, fill=LIGHT)
for i, a in enumerate(AGES):
    r = AR0 + i; put(wa, f'A{r}', a, BLUE, YR); put(wa, f'B{r}', f'=A{r}+0.5', BLK, '0.0')
    for c in YC:
        put(wa, f'{c}{r}', f'=IF({c}$4-$A{r}<{MY0},0,INDEX({FL_MAT},MATCH({c}$4-$A{r},{FL_MY},0),MATCH({c}$4,{FL_YEARS},0)))', BLK, NUM0)
ST = {'vio': AR1 + 2, 'sh7': AR1 + 3, 'sh15': AR1 + 4, 'le6': AR1 + 5, 'avg': AR1 + 6}
put(wa, f"A{ST['vio']}", 'VIO (M)', BOLD); put(wa, f"A{ST['sh7']}", 'Share aged 7+', BOLD); put(wa, f"A{ST['sh15']}", 'Share aged 15+', BOLD)
put(wa, f"A{ST['le6']}", 'Count aged ≤6 (M)', BOLD); put(wa, f"A{ST['avg']}", 'Average age (t−MY+0.5)', BOLD)
for c in YC:
    rng = f'{c}{AR0}:{c}{AR1}'
    put(wa, f"{c}{ST['vio']}", f'=SUM({rng})/1000', BLK, NUM1, bold=True)
    put(wa, f"{c}{ST['sh7']}", f'=SUMIF($A${AR0}:$A${AR1},">=7",{rng})/SUM({rng})', BLK, PCT)
    put(wa, f"{c}{ST['sh15']}", f'=SUMIF($A${AR0}:$A${AR1},">=15",{rng})/SUM({rng})', BLK, PCT)
    put(wa, f"{c}{ST['le6']}", f'=SUMIF($A${AR0}:$A${AR1},"<=6",{rng})/1000', BLK, NUM1)
    put(wa, f"{c}{ST['avg']}", f'=SUMPRODUCT($B${AR0}:$B${AR1},{rng})/SUM({rng})', BLK, '0.0')
put(wa, f"A{ST['avg']+2}", "Average age here is NOT comparable to S&P's 12.8 (S&P's figure needs a 15+ tail averaging ~27 yrs — registrations that are barely driven). Calibrate to counts, not to average age. docs/AGE_CURVES.md §2.3", NOTE, wrap=True)
wa.merge_cells(f"A{ST['avg']+2}:J{ST['avg']+2}"); wa.row_dimensions[ST['avg']+2].height = 30
widths(wa, {'A': 22, 'B': 8}); wa.freeze_panes = f'C{AR0}'
FA_YEARS = f"FleetByAge!$C$4:${YC[-1]}$4"; FA_MAT = f"FleetByAge!$C${AR0}:${YC[-1]}${AR1}"; FA_AGES = f"FleetByAge!$A${AR0}:$A${AR1}"
def fa_col(c): return f"FleetByAge!{c}${AR0}:{c}${AR1}"

# ---- Curves: R, P, miles by age (+ flags, 2024 body split for the miles decomposition)
wc = wb.create_sheet('Curves')
put(wc, 'A1', 'Age curves — R(a) relative insured-claim frequency, P(a) total-loss propensity, miles by age', TITLE)
put(wc, 'A2', 'R and P read their parameters from Inputs (yellow cells). Flags feed the SUMPRODUCTs on TLF_Roll. Miles: EPA schedule (Data_EPA_Miles), age>30 = age-30 value. Columns I–K: 2024 fleet split by body for the fleet-weighted miles ratio (docs/AGE_CURVES.md §3.4).', NOTE, wrap=True)
wc.merge_cells('A2:K2'); wc.row_dimensions[2].height = 42
hdrs = ['age', 'R(a)', 'P(a)', 'miles/yr cars', 'miles/yr light trucks', 'flag age≥7', 'flag age≤3', '(unused)', 'cars fleet 2024 (thousands)', 'LT fleet 2024 (thousands)', 'miles/yr fleet-weighted 2024']
for j, h in enumerate(hdrs): put(wc, f'{L(j+1)}4', h, BOLD, fill=HDR, wrap=True)
wc.row_dimensions[4].height = 30
QR0 = 6; QR1 = QR0 + NA - 1
for i, a in enumerate(AGES):
    r = QR0 + i; put(wc, f'A{r}', a, BLUE, YR)
    put(wc, f'B{r}', f'=IF($A{r}=0,Inputs!$B$9,1)*EXP(-Inputs!$B$11*MAX($A{r}-Inputs!$B$10,0))', GRN, DEC3)
    put(wc, f'C{r}', f'=Inputs!$B$12+(Inputs!$B$13-Inputs!$B$12)/(1+EXP(-($A{r}-Inputs!$B$14)/Inputs!$B$15))', GRN, DEC3)
    put(wc, f'D{r}', f'=INDEX(Data_EPA_Miles!$B$5:$B$35,MIN($A{r},30)+1)', GRN, NUM0)
    put(wc, f'E{r}', f'=INDEX(Data_EPA_Miles!$C$5:$C$35,MIN($A{r},30)+1)', GRN, NUM0)
    put(wc, f'F{r}', f'=IF($A{r}>=7,1,0)', BLK, '0'); put(wc, f'G{r}', f'=IF($A{r}<=3,1,0)', BLK, '0')
    put(wc, f'I{r}', f'=IF(2024-$A{r}<{MY0},0,INDEX({SALES_C},MATCH(2024-$A{r},{SALES_Y},0))*INDEX({SV_CARS},$A{r}+1,MATCH(2024,{SV_YEARS},0)))', GRN, NUM0)
    put(wc, f'J{r}', f'=IF(2024-$A{r}<{MY0},0,INDEX({SALES_L},MATCH(2024-$A{r},{SALES_Y},0))*INDEX({SV_LT},$A{r}+1,MATCH(2024,{SV_YEARS},0)))', GRN, NUM0)
    put(wc, f'K{r}', f'=IF(I{r}+J{r}=0,D{r},(D{r}*I{r}+E{r}*J{r})/(I{r}+J{r}))', BLK, NUM0)
CV = dict(R=f"Curves!$B${QR0}:$B${QR1}", P=f"Curves!$C${QR0}:$C${QR1}", F7=f"Curves!$F${QR0}:$F${QR1}", LE3=f"Curves!$G${QR0}:$G${QR1}", AGE=f"Curves!$A${QR0}:$A${QR1}")
# miles-ratio memo
m0 = QR1 + 2
put(wc, f'A{m0}', 'R decomposition, 7+ vs 0–6 (2024 fleet weights)', BOLD)
put(wc, f'A{m0+1}', 'Fleet-weighted miles ratio 7+ / 0–6', BLK); put(wc, f'A{m0+2}', 'Fitted R ratio 7+ / 0–6 (claims per vehicle)', BLK); put(wc, f'A{m0+3}', 'Residual = coverage / filing', BLK)
N24 = fa_col(YC[YEARS.index(2024)])
put(wc, f'B{m0+1}', f'=(SUMPRODUCT($K${QR0}:$K${QR1},$F${QR0}:$F${QR1},{N24})/SUMPRODUCT($F${QR0}:$F${QR1},{N24}))/(SUMPRODUCT($K${QR0}:$K${QR1},1-$F${QR0}:$F${QR1},{N24})/SUMPRODUCT(1-$F${QR0}:$F${QR1},{N24}))', BLK, DEC3)
put(wc, f'B{m0+2}', f'=(SUMPRODUCT($B${QR0}:$B${QR1},$F${QR0}:$F${QR1},{N24})/SUMPRODUCT($F${QR0}:$F${QR1},{N24}))/(SUMPRODUCT($B${QR0}:$B${QR1},1-$F${QR0}:$F${QR1},{N24})/SUMPRODUCT(1-$F${QR0}:$F${QR1},{N24}))', BLK, DEC3)
put(wc, f'B{m0+3}', f'=B{m0+2}/B{m0+1}', BLK, DEC3)
put(wc, f'C{m0+1}', 'EPA T3.14 miles × 2024 fleet (≈0.65)', NOTE); put(wc, f'C{m0+2}', 'claims per vehicle, 7+ vs 0–6 (≈0.56)', NOTE); put(wc, f'C{m0+3}', 'liability-only, higher deductibles, unfiled small claims on older cars (≈0.87)', NOTE)
widths(wc, {'A': 8, 'B': 10, 'C': 10, 'D': 12, 'E': 12, 'F': 9, 'G': 9, 'H': 4, 'I': 12, 'J': 12, 'K': 14}); wc.freeze_panes = 'B6'

# ---- Calibration (Solver)
wk = wb.create_sheet('Calibration')
put(wk, 'A1', 'Calibration — fit R(a) and P(a) to CCC 2024 with Solver', TITLE)
put(wk, 'A2', 'Working parameters B4:B8 (yellow) are what Solver changes. They start at the fitted values. After a run, copy B4:B8 → Inputs!B11:B15 so the model does not depend on Solver being re-run.', NOTE, wrap=True)
wk.merge_cells('A2:N2'); wk.row_dimensions[2].height = 30
put(wk, 'A3', 'Working parameter', BOLD, fill=HDR); put(wk, 'B3', 'Value', BOLD, fill=HDR); put(wk, 'C3', 'Bounds for Solver', BOLD, fill=HDR)
for r, lab, v, fmt, b in [(4, 'R slope after kink', FIT['r_slope'], DEC4, '0 to 0.5'), (5, 'P floor (pmin)', FIT['pmin'], DEC3, '0.01 to 0.3'), (6, 'P ceiling (pmax)', FIT['pmax'], DEC3, '0.3 to 0.95, and ≥ B5'),
                          (7, 'P midpoint age', FIT['pmid'], '0.00', '0 to 30'), (8, 'P width', FIT['pwid'], '0.00', '0.3 to 12')]:
    put(wk, f'A{r}', lab, BLK); put(wk, f'B{r}', v, BLUE, fmt, fill=YEL); put(wk, f'C{r}', b, NOTE)
put(wk, 'A9', 'Exposure age 0 (from Inputs)', BLK); put(wk, 'B9', '=Inputs!$B$9', GRN, '0.00'); put(wk, 'A10', 'R kink age (from Inputs)', BLK); put(wk, 'B10', '=Inputs!$B$10', GRN, YR)
KR0 = 13; KR1 = KR0 + NA - 1     # 13..58
for j, h in enumerate(['age', 'fleet 2024 (thousands)', 'R(a)', 'P(a)', 'claims = fleet×R', 'total losses = claims×P', 'repairables = claims−TL']): put(wk, f'{L(j+1)}12', h, BOLD, fill=HDR, wrap=True)
wk.row_dimensions[12].height = 30
for i, a in enumerate(AGES):
    r = KR0 + i; put(wk, f'A{r}', a, BLUE, YR)
    put(wk, f'B{r}', f'=INDEX({FA_MAT},MATCH($A{r},{FA_AGES},0),MATCH(2024,{FA_YEARS},0))', GRN, NUM0)
    put(wk, f'C{r}', f'=IF($A{r}=0,$B$9,1)*EXP(-$B$4*MAX($A{r}-$B$10,0))', BLK, DEC3)
    put(wk, f'D{r}', f'=$B$5+($B$6-$B$5)/(1+EXP(-($A{r}-$B$7)/$B$8))', BLK, DEC3)
    put(wk, f'E{r}', f'=B{r}*C{r}', BLK, NUM0); put(wk, f'F{r}', f'=E{r}*D{r}', BLK, NUM0); put(wk, f'G{r}', f'=E{r}-F{r}', BLK, NUM0)
A_, E_, F_, G_ = f'$A${KR0}:$A${KR1}', f'$E${KR0}:$E${KR1}', f'$F${KR0}:$F${KR1}', f'$G${KR0}:$G${KR1}'
stats = [
 ('tlf',    'Total-loss frequency',                 f'=SUM({F_})/SUM({E_})', PCT),
 ('tl7',    'Total losses from vehicles 7+',        f'=SUMIF({A_},">=7",{F_})/SUM({F_})', PCT),
 ('rp7',    'Repairables from vehicles 7+',         f'=SUMIF({A_},">=7",{G_})/SUM({G_})', PCT),
 ('rp3',    'Repairables from vehicles ≤3',         f'=SUMIF({A_},"<=3",{G_})/SUM({G_})', PCT),
 ('age_cl', 'Average age, claim vehicles',          f'=SUMPRODUCT({A_},{E_})/SUM({E_})', '0.00'),
 ('age_rp', 'Average age, repairables',             f'=SUMPRODUCT({A_},{G_})/SUM({G_})', '0.00'),
 ('age_tl', 'Average age, total losses',            f'=SUMPRODUCT({A_},{F_})/SUM({F_})', '0.00'),
 ('p03',    'Total-loss rate, vehicles ≤3',         f'=SUMIF({A_},"<=3",{F_})/SUMIF({A_},"<=3",{E_})', PCT),
]
for j, h in enumerate(['key', 'statistic (2024)', 'model', 'CCC target', 'tolerance', 'scaled sq. error', 'source quote']): put(wk, f'{L(9+j)}12', h, BOLD, fill=HDR)
for i, (k, lab, f, fmt) in enumerate(stats):
    r = 13 + i
    put(wk, f'I{r}', k, BLK); put(wk, f'J{r}', lab, BLK); put(wk, f'K{r}', f, BLK, fmt)
    trow = TR0 + [t[2] for t in TGT if t[0] == 'FIT'].index(k)          # FIT rows sit at the top of Data_CCC_Targets in this order
    put(wk, f'L{r}', f'=Data_CCC_Targets!$E${trow}', GRN, fmt)
    put(wk, f'M{r}', f'=Data_CCC_Targets!$F${trow}', GRN, ('0.00' if k.startswith('age') else PCT2))
    put(wk, f'N{r}', f'=((K{r}-L{r})/M{r})^2', BLK, '0.000')
    put(wk, f'O{r}', f'=Data_CCC_Targets!$G${trow}', GRN)
put(wk, 'J22', 'LOSS (Solver objective → minimise)', BOLD); put(wk, 'N22', '=SUM(N13:N20)', BLK, '0.000', fill=YEL, bold=True)
put(wk, 'J23', 'Reference: the Python fit (scripts/age_curves.py) lands at ~1.0. One unit = one statistic off by exactly its tolerance.', NOTE)
solver = ["SOLVER SET-UP (Excel → Data → Solver; on Mac enable once via Tools → Excel Add-ins → Solver):",
          "1. Set Objective: $N$22, To: Min.",
          "2. By Changing Variable Cells: $B$4:$B$8.",
          "3. Constraints: B4 ≥ 0; B4 ≤ 0.5; B5 ≥ 0.01; B5 ≤ 0.3; B6 ≥ 0.3; B6 ≤ 0.95; B6 ≥ B5; B7 ≥ 0; B7 ≤ 30; B8 ≥ 0.3; B8 ≤ 12.",
          "4. Method: GRG Nonlinear. Options → GRG Nonlinear tab: tick Use Multistart, Population Size 100, Random Seed 7, tick Require Bounds on Variables. Untick 'Make Unconstrained Variables Non-Negative' (bounds are set explicitly).",
          "5. Solve. Expect LOSS ≈ 1.0 and B4:B8 within a few thousandths of the starting values. Copy B4:B8 → Inputs!B11:B15 (paste values).",
          "What this does in words: turn the five knobs until the model's eight 2024 statistics match CCC's published ones. Multistart = try from many random starting points so Solver does not settle in a shallow dip."]
for i, t in enumerate(solver): put(wk, f'I{25+i}', t, BOLD if i == 0 else BLK, wrap=False)
widths(wk, {'A': 8, 'B': 12, 'C': 22, 'D': 9, 'E': 14, 'F': 16, 'G': 16, 'H': 3, 'I': 8, 'J': 34, 'K': 10, 'L': 11, 'M': 10, 'N': 13, 'O': 90}); wk.freeze_panes = 'A13'

# ---- TLF_Roll
wr = wb.create_sheet('TLF_Roll')
put(wr, 'A1', 'Baseline total-loss frequency from demographics alone, by year — and the out-of-sample tests', TITLE)
put(wr, 'A2', 'claims index = Σ_a fleet(a,t)·R(a); TL index = Σ_a fleet(a,t)·R(a)·P(a); baseline TLF = TL/claims. R and P are FROZEN (Inputs); only the fleet changes year to year. The YoY drift row is the demographic contribution to TLF; everything else in actual TLF is level (spread cycle, technology, filing).', NOTE, wrap=True)
wr.merge_cells('A2:N2'); wr.row_dimensions[2].height = 42
put(wr, 'A4', 'Year →', BOLD, fill=LIGHT)
for i, y in enumerate(YEARS): put(wr, f'{YC[i]}4', f'=Inputs!{YC[i]}23', GRN, YR, fill=LIGHT)
RW = {'cl': 6, 'tl': 7, 'tlf': 8, 'drift': 9, 'cl7': 10, 'tl7': 11, 'rp7': 12, 'rp3': 13, 'age_cl': 14, 'age_tl': 15, 'age_rp': 16, 'p03': 17, 'vio': 18, 'sh7': 19, 'avg': 20, 'tlgr': 21}
labels = {'cl': 'Claims index Σ fleet·R (thousands)', 'tl': 'Total-loss index Σ fleet·R·P (thousands)', 'tlf': 'Baseline TLF (demographics only)', 'drift': 'YoY change in baseline TLF (pp)',
          'cl7': 'Claims share, vehicles 7+', 'tl7': 'Total-loss share, vehicles 7+', 'rp7': 'Repairable share, vehicles 7+', 'rp3': 'Repairable share, vehicles ≤3',
          'age_cl': 'Average age, claim vehicles', 'age_tl': 'Average age, total losses', 'age_rp': 'Average age, repairables', 'p03': 'Total-loss rate, vehicles ≤3',
          'vio': 'VIO (M) — FleetByAge', 'sh7': 'Fleet share aged 7+ — FleetByAge', 'avg': 'Average fleet age (t−MY+0.5)', 'tlgr': 'Total-loss index YoY % (demographic TL pool growth)'}
for k, r in RW.items(): put(wr, f'A{r}', labels[k], BOLD if k in ('tlf', 'drift') else BLK)
for i, c in enumerate(YC):
    F = fa_col(c); prev = YC[i - 1] if i > 0 else None
    put(wr, f'{c}{RW["cl"]}', f'=SUMPRODUCT({F},{CV["R"]})', BLK, NUM0)
    put(wr, f'{c}{RW["tl"]}', f'=SUMPRODUCT({F},{CV["R"]},{CV["P"]})', BLK, NUM0)
    put(wr, f'{c}{RW["tlf"]}', f'={c}{RW["tl"]}/{c}{RW["cl"]}', BLK, PCT2, bold=True, fill=YEL)
    put(wr, f'{c}{RW["drift"]}', (f'=({c}{RW["tlf"]}-{prev}{RW["tlf"]})*100' if prev else ''), BLK, '+0.00;-0.00', bold=True)
    put(wr, f'{c}{RW["cl7"]}', f'=SUMPRODUCT({F},{CV["R"]},{CV["F7"]})/{c}{RW["cl"]}', BLK, PCT)
    put(wr, f'{c}{RW["tl7"]}', f'=SUMPRODUCT({F},{CV["R"]},{CV["P"]},{CV["F7"]})/{c}{RW["tl"]}', BLK, PCT)
    put(wr, f'{c}{RW["rp7"]}', f'=(SUMPRODUCT({F},{CV["R"]},{CV["F7"]})-SUMPRODUCT({F},{CV["R"]},{CV["P"]},{CV["F7"]}))/({c}{RW["cl"]}-{c}{RW["tl"]})', BLK, PCT)
    put(wr, f'{c}{RW["rp3"]}', f'=(SUMPRODUCT({F},{CV["R"]},{CV["LE3"]})-SUMPRODUCT({F},{CV["R"]},{CV["P"]},{CV["LE3"]}))/({c}{RW["cl"]}-{c}{RW["tl"]})', BLK, PCT)
    put(wr, f'{c}{RW["age_cl"]}', f'=SUMPRODUCT({F},{CV["R"]},{CV["AGE"]})/{c}{RW["cl"]}', BLK, '0.0')
    put(wr, f'{c}{RW["age_tl"]}', f'=SUMPRODUCT({F},{CV["R"]},{CV["P"]},{CV["AGE"]})/{c}{RW["tl"]}', BLK, '0.0')
    put(wr, f'{c}{RW["age_rp"]}', f'=(SUMPRODUCT({F},{CV["R"]},{CV["AGE"]})-SUMPRODUCT({F},{CV["R"]},{CV["P"]},{CV["AGE"]}))/({c}{RW["cl"]}-{c}{RW["tl"]})', BLK, '0.0')
    put(wr, f'{c}{RW["p03"]}', f'=SUMPRODUCT({F},{CV["R"]},{CV["P"]},{CV["LE3"]})/SUMPRODUCT({F},{CV["R"]},{CV["LE3"]})', BLK, PCT)
    put(wr, f'{c}{RW["vio"]}', f"=FleetByAge!{c}{ST['vio']}", GRN, NUM1); put(wr, f'{c}{RW["sh7"]}', f"=FleetByAge!{c}{ST['sh7']}", GRN, PCT); put(wr, f'{c}{RW["avg"]}', f"=FleetByAge!{c}{ST['avg']}", GRN, '0.0')
    put(wr, f'{c}{RW["tlgr"]}', (f'=({c}{RW["tl"]}/{prev}{RW["tl"]}-1)*100' if prev else ''), BLK, '+0.0;-0.0')
# checks vs CCC (OOS + fit-year)
CK0 = 24
put(wr, f'A{CK0}', 'Checks against CCC (R,P frozen at the 2024 fit — rows marked OOS were never used in the fit)', BOLD)
for j, h in enumerate(['use', 'year', 'statistic', 'CCC actual', 'model', 'error', 'quote']): put(wr, f'{L(1+j)}{CK0+1}', h, BOLD, fill=HDR)
keymap = {'tlf': 'tlf', 'tl7': 'tl7', 'rp7': 'rp7', 'rp3': 'rp3', 'age_cl': 'age_cl', 'age_rp': 'age_rp', 'age_tl': 'age_tl', 'p03': 'p03', 'vio': 'vio', 'sh7': 'sh7'}
r = CK0 + 2
for use, year, key, statname, val, tol, quote, page in TGT:
    if key not in keymap: continue
    isage = key.startswith('age')
    put(wr, f'A{r}', use, BLK); put(wr, f'B{r}', year, BLUE, YR); put(wr, f'C{r}', statname, BLK); put(wr, f'D{r}', val, BLUE, ('0.0' if isage else ('#,##0' if key == 'vio' else PCT)))
    put(wr, f'E{r}', f'=INDEX($C${RW[keymap[key]]}:${YC[-1]}${RW[keymap[key]]},1,MATCH(B{r},$C$4:${YC[-1]}$4,0))', BLK, ('0.0' if isage else ('#,##0.0' if key == 'vio' else PCT)))
    put(wr, f'F{r}', (f'=E{r}-D{r}' if (isage or key == 'vio') else f'=(E{r}-D{r})*100'), BLK, ('+0.0;-0.0' if (isage or key == 'vio') else '+0.0"pp";-0.0"pp"'))
    put(wr, f'G{r}', quote, NOTE); r += 1
put(wr, f'A{r+1}', 'Demographic drift 2019→2025 (pp/yr) vs actual CCC rise', BOLD)
c19, c25 = YC[YEARS.index(2019)], YC[YEARS.index(2025)]
put(wr, f'E{r+1}', f'=({c25}{RW["tlf"]}-{c19}{RW["tlf"]})*100/6', BLK, '+0.00', fill=YEL); put(wr, f'F{r+1}', '=(0.231-0.192)*100/6', BLK, '+0.00'); put(wr, f'G{r+1}', 'model drift per year vs actual +0.65pp/yr (19.2% → 23.1%); the ratio is the share of the rise that is demographics (~24%)', NOTE)
widths(wr, {'A': 46, 'B': 7, 'C': 44, 'D': 11, 'E': 11, 'F': 10, 'G': 90}); wr.freeze_panes = 'B6'

# ---- Spread_Reg
wsp = wb.create_sheet('Spread_Reg')
put(wsp, 'A1', 'Totaling-spread regression — ΔTLF(pp, YoY) = a + b × spread(t−1), CCC quarterly', TITLE)
put(wsp, 'A2', 'spread = repair CPI YoY − used-car CPI YoY (BLS NSA, quarterly mean of monthly values; Data_Spread). ΔTLF = CCC quarterly TLF minus the same quarter a year earlier (Data_CCC_TLF_Quarterly). One-quarter lag. Reproduces scripts/analysis_20260911.py: all-loss a=0.599 b=0.0815 R²=0.81 n=27; non-comp a=0.609 b=0.0834 R²=0.79.', NOTE, wrap=True)
wsp.merge_cells('A2:V2'); wsp.row_dimensions[2].height = 42
_, _, sp_rows = read_csv('totaling_spread_quarterly.csv'); sp_rows = [r for r in sp_rows if r[0] >= '2016Q1']
_, _, tq_rows = read_csv('ccc_tlf_quarterly.csv')
for j, h in enumerate(['quarter', 'spread (pp)', 'months', 'note']): put(wsp, f'{L(1+j)}4', h, BOLD, fill=HDR)
for i, r in enumerate(sp_rows):
    put(wsp, f'A{5+i}', r[0], BLUE); put(wsp, f'B{5+i}', float(r[1]), BLUE, '0.00'); put(wsp, f'C{5+i}', int(r[2]), BLUE, '0'); put(wsp, f'D{5+i}', r[3], NOTE)
SP0, SP1 = 5, 4 + len(sp_rows)
for j, h in enumerate(['quarter', 'TLF non-comp %', 'TLF all-loss %']): put(wsp, f'{L(6+j)}4', h, BOLD, fill=HDR)
for i, r in enumerate(tq_rows):
    put(wsp, f'F{5+i}', r[0], BLUE); put(wsp, f'G{5+i}', float(r[1]), BLUE, '0.0'); put(wsp, f'H{5+i}', float(r[2]), BLUE, '0.0')
TQ0, TQ1 = 5, 4 + len(tq_rows)
pairs_q = [r[0] for r in tq_rows if any(t[0] == f"{int(r[0][:4])-1}{r[0][4:]}" for t in tq_rows)]
for j, h in enumerate(['quarter t', 'year', 'q', 'prior-year quarter', 'lag quarter t−1', 'ΔTLF all-loss (pp)', 'ΔTLF non-comp (pp)', 'spread(t−1)']): put(wsp, f'{L(10+j)}4', h, BOLD, fill=HDR)
for i, q in enumerate(pairs_q):
    r = 5 + i
    put(wsp, f'J{r}', q, BLUE); put(wsp, f'K{r}', f'=VALUE(LEFT(J{r},4))', BLK, '0'); put(wsp, f'L{r}', f'=VALUE(RIGHT(J{r},1))', BLK, '0')
    put(wsp, f'M{r}', f'=(K{r}-1)&"Q"&L{r}', BLK); put(wsp, f'N{r}', f'=IF(L{r}=1,(K{r}-1)&"Q4",K{r}&"Q"&(L{r}-1))', BLK)
    put(wsp, f'O{r}', f'=INDEX($H${TQ0}:$H${TQ1},MATCH(J{r},$F${TQ0}:$F${TQ1},0))-INDEX($H${TQ0}:$H${TQ1},MATCH(M{r},$F${TQ0}:$F${TQ1},0))', BLK, '+0.0;-0.0')
    put(wsp, f'P{r}', f'=INDEX($G${TQ0}:$G${TQ1},MATCH(J{r},$F${TQ0}:$F${TQ1},0))-INDEX($G${TQ0}:$G${TQ1},MATCH(M{r},$F${TQ0}:$F${TQ1},0))', BLK, '+0.0;-0.0')
    put(wsp, f'Q{r}', f'=INDEX($B${SP0}:$B${SP1},MATCH(N{r},$A${SP0}:$A${SP1},0))', BLK, '0.00')
PR0, PR1 = 5, 4 + len(pairs_q)
for j, h in enumerate(['regression', 'all-loss', 'non-comp']): put(wsp, f'{L(19+j)}4', h, BOLD, fill=HDR)
regrows = [('slope b (pp TLF per pp spread)', 'SLOPE', DEC4), ('intercept a (pp/yr, unexplained drift)', 'INTERCEPT', DEC3), ('R²', 'RSQ', DEC3), ('n', 'COUNT', '0')]
for i, (lab, fn, fmt) in enumerate(regrows):
    r = 5 + i; put(wsp, f'S{r}', lab, BLK)
    if fn == 'COUNT': put(wsp, f'T{r}', f'=COUNT($O${PR0}:$O${PR1})', BLK, fmt); put(wsp, f'U{r}', f'=COUNT($P${PR0}:$P${PR1})', BLK, fmt)
    else:
        put(wsp, f'T{r}', f'={fn}($O${PR0}:$O${PR1},$Q${PR0}:$Q${PR1})', BLK, fmt, fill=(YEL if fn != 'RSQ' else None)); put(wsp, f'U{r}', f'={fn}($P${PR0}:$P${PR1},$Q${PR0}:$Q${PR1})', BLK, fmt, fill=(YEL if fn != 'RSQ' else None))
put(wsp, 'S10', 'Prediction', BOLD); put(wsp, 'S11', 'Spread quarter to use (t−1)', BLK); put(wsp, 'T11', '2026Q1', BLUE); put(wsp, 'S12', 'spread(t−1)', BLK); put(wsp, 'T12', f'=INDEX($B${SP0}:$B${SP1},MATCH(T11,$A${SP0}:$A${SP1},0))', BLK, '0.00')
put(wsp, 'S13', 'Predicted ΔTLF all-loss, quarter t (pp YoY)', BLK); put(wsp, 'T13', '=T6+T5*T12', BLK, '+0.00', fill=YEL)
put(wsp, 'S14', 'Live OOS: mgmt-cited CCC 2Q26 23.3 vs 22.4 (2026-09-10 call)', NOTE); put(wsp, 'T14', 0.9, BLUE, '+0.00'); put(wsp, 'S15', 'error (pp)', BLK); put(wsp, 'T15', '=T13-T14', BLK, '+0.00')
put(wsp, 'S17', 'Why the intercept matters: with spread = 0 the model still adds ~0.6pp/yr of TLF; the cohort roll (TLF_Roll) explains ~0.15pp of that. Use the spread term for 12 months, not for the decade. MODEL_BLUEPRINT §3.', NOTE, wrap=True); wsp.merge_cells('S17:V19')
widths(wsp, {'A': 9, 'B': 11, 'C': 7, 'D': 34, 'E': 2, 'F': 9, 'G': 13, 'H': 13, 'I': 2, 'J': 10, 'K': 6, 'L': 4, 'M': 16, 'N': 14, 'O': 16, 'P': 16, 'Q': 11, 'R': 2, 'S': 46, 'T': 11, 'U': 11}); wsp.freeze_panes = 'A5'

# ---- RPU_Reg
wq = wb.create_sheet('RPU_Reg')
put(wq, 'A1', 'RPU chain — ASP ~ used-car CPI (nowcast) and service RPU ~ ASP (elasticity)', TITLE)
put(wq, 'A2', 'Step 1: Copart US insurance ASP YoY (transcripts, Data_ReportedUnits) on used-car CPI YoY (BLS CUSR0000SETA02, SA, fiscal-quarter average of the three months vs the same months a year earlier; Data_CPI col B). Step 2: implied service RPU YoY on global ASP YoY, n=17 (Data_Elasticity). Reference values: step 1 a=3.23 b=0.599 r=0.77 (n=15); step 2 b=0.514 a=4.13 R²=0.61; total-RPU b=0.752 a=2.84.', NOTE, wrap=True)
wq.merge_cells('A2:P2'); wq.row_dimensions[2].height = 55
FQM = [("FY2023 Q1", "2022-08", "2022-09", "2022-10"), ("FY2023 Q2", "2022-11", "2022-12", "2023-01"), ("FY2023 Q3", "2023-02", "2023-03", "2023-04"), ("FY2023 Q4", "2023-05", "2023-06", "2023-07"),
       ("FY2024 Q1", "2023-08", "2023-09", "2023-10"), ("FY2024 Q2", "2023-11", "2023-12", "2024-01"), ("FY2024 Q3", "2024-02", "2024-03", "2024-04"), ("FY2024 Q4", "2024-05", "2024-06", "2024-07"),
       ("FY2025 Q1", "2024-08", "2024-09", "2024-10"), ("FY2025 Q2", "2024-11", "2024-12", "2025-01"), ("FY2025 Q3", "2025-02", "2025-03", "2025-04"), ("FY2025 Q4", "2025-05", "2025-06", "2025-07"),
       ("FY2026 Q1", "2025-08", "2025-09", "2025-10"), ("FY2026 Q2", "2025-11", "2025-12", "2026-01"), ("FY2026 Q3", "2026-02", "2026-03", "2026-04"), ("FY2026 Q4", "2026-05", "2026-06", "2026-07")]
_, cpi_hdr, cpi_rows = read_csv('cprt_cpi_three_series.csv'); CPI0, CPI1 = 5, 4 + len(cpi_rows)
_, ru_hdr, ru_rows = read_csv('reported_units.csv'); RU0, RU1 = 5, 4 + len(ru_rows)
for j, h in enumerate(['fiscal quarter', 'month 1', 'month 2', 'month 3', 'CPI used cars, qtr avg', 'same qtr prior year', 'CPI YoY %', 'US ins ASP YoY % (reported)']): put(wq, f'{L(1+j)}4', h, BOLD, fill=HDR, wrap=True)
wq.row_dimensions[4].height = 30
cpiA = f'Data_CPI!$A${CPI0}:$A${CPI1}'; cpiB = f'Data_CPI!$B${CPI0}:$B${CPI1}'
for i, (fq, m1, m2, m3) in enumerate(FQM):
    r = 5 + i; put(wq, f'A{r}', fq, BLUE); put(wq, f'B{r}', m1, BLUE); put(wq, f'C{r}', m2, BLUE); put(wq, f'D{r}', m3, BLUE)
    cur = ",".join(f'INDEX({cpiB},MATCH({c}{r},{cpiA},0))' for c in 'BCD'); pri = ",".join(f'INDEX({cpiB},MATCH((VALUE(LEFT({c}{r},4))-1)&RIGHT({c}{r},3),{cpiA},0))' for c in 'BCD')
    put(wq, f'E{r}', f'=IFERROR(AVERAGE({cur}),"")', GRN, '0.0'); put(wq, f'F{r}', f'=IFERROR(AVERAGE({pri}),"")', GRN, '0.0')
    put(wq, f'G{r}', f'=IF(OR(E{r}="",F{r}=""),"",(E{r}/F{r}-1)*100)', BLK, '+0.0;-0.0')
    put(wq, f'H{r}', f'=IFERROR(INDEX(Data_ReportedUnits!$F${RU0}:$F${RU1},MATCH(A{r},Data_ReportedUnits!$A${RU0}:$A${RU1},0)),"")', GRN, '+0.0;-0.0')
Q0, Q1 = 5, 4 + 15   # regression rows: FY2023Q1..FY2026Q3 (15); FY2026 Q4 row is the nowcast row
put(wq, 'J4', 'Step 1: ASP = a + b × CPI', BOLD, fill=HDR); put(wq, 'K4', 'value', BOLD, fill=HDR)
put(wq, 'J5', 'slope b', BLK); put(wq, 'K5', f'=SLOPE(H{Q0}:H{Q1},G{Q0}:G{Q1})', BLK, DEC3, fill=YEL)
put(wq, 'J6', 'intercept a (pp)', BLK); put(wq, 'K6', f'=INTERCEPT(H{Q0}:H{Q1},G{Q0}:G{Q1})', BLK, '0.00', fill=YEL)
put(wq, 'J7', 'correlation r', BLK); put(wq, 'K7', f'=CORREL(H{Q0}:H{Q1},G{Q0}:G{Q1})', BLK, DEC3); put(wq, 'J8', 'n', BLK); put(wq, 'K8', f'=COUNT(H{Q0}:H{Q1})', BLK, '0')
put(wq, 'J9', f'Nowcast row: FY2026 Q4 (A{Q1+1}) has CPI but ASP is not in the CSV yet (call: US ins ASP +3.7%). Extend Q0:Q1 when the CSV is updated.', NOTE)
_, el_hdr, el_rows = read_csv('elasticity_rebuild.csv'); EL0, EL1 = 5, 4 + len(el_rows)
elE = f'Data_Elasticity!$E${EL0}:$E${EL1}'; elF = f'Data_Elasticity!$F${EL0}:$F${EL1}'; elG = f'Data_Elasticity!$G${EL0}:$G${EL1}'
put(wq, 'J11', 'Step 2: RPU = a + b × ASP (global, n=17)', BOLD, fill=HDR); put(wq, 'K11', 'service RPU', BOLD, fill=HDR); put(wq, 'L11', 'total RPU (mgmt def.)', BOLD, fill=HDR)
put(wq, 'J12', 'slope b (elasticity)', BLK); put(wq, 'K12', f'=SLOPE({elF},{elE})', GRN, DEC3, fill=YEL); put(wq, 'L12', f'=SLOPE({elG},{elE})', GRN, DEC3, fill=YEL)
put(wq, 'J13', 'intercept a (pp = fee/mix growth at flat ASP)', BLK); put(wq, 'K13', f'=INTERCEPT({elF},{elE})', GRN, '0.00', fill=YEL); put(wq, 'L13', f'=INTERCEPT({elG},{elE})', GRN, '0.00', fill=YEL)
put(wq, 'J14', 'R²', BLK); put(wq, 'K14', f'=RSQ({elF},{elE})', GRN, DEC3); put(wq, 'L14', f'=RSQ({elG},{elE})', GRN, DEC3)
put(wq, 'J15', 'n', BLK); put(wq, 'K15', f'=COUNT({elF})', GRN, '0'); put(wq, 'L15', f'=COUNT({elG})', GRN, '0')
put(wq, 'J16', 'Caveat: residual autocorrelation → effective n ≈ 6; 95% CI on service-RPU slope [0.29, 0.73]. The INTERCEPT is the robust finding (fee/mix adds ~4pp/yr at flat ASP), and it decelerated in FY26 (+1.3 to +3.5pp).', NOTE, wrap=True); wq.merge_cells('J16:P17'); wq.row_dimensions[16].height = 30
put(wq, 'J19', 'Chain (type a used-car CPI YoY assumption)', BOLD, fill=HDR)
put(wq, 'J20', 'Used-car CPI YoY % (assumption)', BLK); put(wq, 'K20', -2.0, BLUE, '+0.0;-0.0')
put(wq, 'J21', '→ US insurance ASP YoY %', BLK); put(wq, 'K21', '=K6+K5*K20', BLK, '+0.0;-0.0')
put(wq, 'J22', '→ Service RPU YoY %', BLK); put(wq, 'K22', '=K13+K12*K21', BLK, '+0.0;-0.0', fill=YEL)
put(wq, 'J23', '→ Total RPU YoY % (mgmt definition)', BLK); put(wq, 'K23', '=L13+L12*K21', BLK, '+0.0;-0.0')
put(wq, 'J24', 'Back-test FY26Q4: used-car CPI ≈ −1.9% → service RPU ≈ +4.4%; reported +4.4%. RPU is low-variance: +3.3% to +8.9% across used-car CPI −8% to +10%.', NOTE, wrap=True); wq.merge_cells('J24:P25')
widths(wq, {'A': 12, 'B': 9, 'C': 9, 'D': 9, 'E': 12, 'F': 12, 'G': 10, 'H': 14, 'I': 2, 'J': 44, 'K': 12, 'L': 16}); wq.freeze_panes = 'A5'

# ---- Checks
wch = wb.create_sheet('Checks')
put(wch, 'A1', 'Checks — every one should read OK', TITLE)
for j, h in enumerate(['check', 'value', 'target', 'tolerance', 'status']): put(wch, f'{L(1+j)}3', h, BOLD, fill=HDR)
c24 = YC[YEARS.index(2024)]; c13 = YC[0]
checks = [
 ('Calibration loss (Solver objective) small', '=Calibration!N22', 0, 3, 'abs'),
 ('Baseline TLF 2024 ≈ CCC 22.3%', f'=TLF_Roll!{c24}{RW["tlf"]}', 0.223, 0.005, 'abs'),
 ('VIO 2024 ≈ 292M (Experian) / 289M (S&P)', f'=TLF_Roll!{c24}{RW["vio"]}', 292, 9, 'abs'),
 ('Fleet share 7+ 2024 ≈ 66%', f'=TLF_Roll!{c24}{RW["sh7"]}', 0.66, 0.025, 'abs'),
 ('Survival at age 0 = 1 in every year', f'=MIN(Survival!C{CR0}:{YC[-1]}{CR0},Survival!C{LR0}:{YC[-1]}{LR0})', 1, 0.0001, 'abs'),
 ('Fleet matrix: 2013 total ≈ 2013 census light vehicles (~243M)', f'=Fleet!{c13}{FR1+2}/1000', 243, 12, 'abs'),
 ('Spread regression slope ≈ 0.0815 (all-loss)', '=Spread_Reg!T5', 0.0815, 0.003, 'abs'),
 ('Spread regression intercept ≈ 0.599 (all-loss)', '=Spread_Reg!T6', 0.599, 0.03, 'abs'),
 ('Service-RPU elasticity ≈ 0.514', '=RPU_Reg!K12', 0.514, 0.01, 'abs'),
 ('Service-RPU intercept ≈ 4.13', '=RPU_Reg!K13', 4.13, 0.1, 'abs'),
 ('ASP ~ CPI slope ≈ 0.60 (n=15)', '=RPU_Reg!K5', 0.599, 0.05, 'abs'),
 ('P(≤3) 2024 ≈ 10%', f'=TLF_Roll!{c24}{RW["p03"]}', 0.10, 0.01, 'abs'),
]
for i, (lab, f, tgt, tol, kind) in enumerate(checks):
    r = 4 + i; put(wch, f'A{r}', lab, BLK); put(wch, f'B{r}', f, GRN, '0.0000'); put(wch, f'C{r}', tgt, BLUE, '0.0000'); put(wch, f'D{r}', tol, BLUE, '0.0000')
    put(wch, f'E{r}', f'=IF(ABS(B{r}-C{r})<=D{r},"OK","FAIL")', BLK, bold=True)
put(wch, f'A{4+len(checks)+1}', 'ALL CHECKS', BOLD); put(wch, f'E{4+len(checks)+1}', f'=IF(COUNTIF(E4:E{3+len(checks)},"OK")={len(checks)},"OK","FAIL")', BLK, bold=True, fill=YEL)
widths(wch, {'A': 58, 'B': 12, 'C': 12, 'D': 12, 'E': 8})

# ---- generic Data tabs
for name, fname in DATA_TABS: add_data_sheet(wb, name, fname)

# ---- README (filled last so it can index the tabs)
put(ws, 'A1', 'CPRT Intermediate — data and formulas to copy into "CPRT Model"', TITLE)
put(ws, 'A2', f'Built {TODAY} by scripts/build_intermediate_xlsx.py from the committed CSVs in data/csv/. Rebuild after any data update; do not hand-edit Data_* tabs.', NOTE)
readme = [
 ('HOW TO USE', ''),
 ('Copy whole sheets, not cells', 'Right-click a tab → Move or Copy → To book: CPRT Model → tick Create a copy. Copy the tabs a formula sheet depends on FIRST (Inputs, Data_Sales, Data_EPA_Survival, Data_EPA_Miles, Data_CCC_Targets, then Survival, Fleet, FleetByAge, Curves, then TLF_Roll / Calibration). References are explicit sheet names, no named ranges, so they survive the copy as long as the tab names are unchanged.'),
 ('Colour legend', 'BLUE = hard-coded input · BLACK = formula · GREEN = link to another sheet · YELLOW fill = calibrated parameter (fitted; reproducible on Calibration / Spread_Reg / RPU_Reg).'),
 ('One assumption per cell', 'Every parameter lives once, on Inputs. Formula tabs never contain a typed number except the fixed 2024 cross-section on Calibration and Curves I:K.'),
 ('Check before you trust', 'Checks tab must read OK everywhere after Excel recalculates (it does on open). If a check FAILs, a reference broke in the copy.'),
 ('', ''),
 ('TAB INDEX', ''),
 ('Inputs', 'All parameters (survival stretch, R/P, exposure, future sales, anchors) + the k(t) path by year.'),
 ('Data_Sales', 'Cohort sizes: new light-vehicle sales by model year, cars and light trucks, 1970–2030 (2026+ from Inputs).'),
 ('Data_EPA_Survival', 'EPA survival schedule by age (ORNL TEDB Ed.40 T3.15). Data_EPA_Miles: EPA miles by age (T3.14).'),
 ('Data_CCC_Targets', 'The CCC statistics R and P are fitted to (FIT), tested against (OOS), and the fleet-count anchors (S), each with its verbatim quote and page.'),
 ('Survival', 'S(a,t) = EPA(a/k(t)) for cars and light trucks, ages 0–45 × years 2013–2030.'),
 ('Fleet', 'Vehicles on the road by model year × calendar year (thousands). Row 68 = VIO.'),
 ('FleetByAge', 'Same fleet re-indexed by age; VIO, share 7+/15+, count ≤6, average age.'),
 ('Curves', 'R(a), P(a), miles by age, flags; the 7+ vs 0–6 miles/coverage decomposition.'),
 ('Calibration', 'Solver set-up: five parameters → eight CCC 2024 statistics → LOSS. Instructions on the sheet.'),
 ('TLF_Roll', 'Baseline TLF from demographics by year, its YoY drift, claim/TL age mix, and the out-of-sample checks vs CCC 2019/2020/2025.'),
 ('Spread_Reg', 'ΔTLF = a + b·spread(t−1): pairs built by formula from Data_Spread and Data_CCC_TLF_Quarterly; SLOPE/INTERCEPT/RSQ; prediction and the live 2Q26 test.'),
 ('RPU_Reg', 'ASP ~ used-car CPI by fiscal quarter (formulas on Data_CPI, Data_ReportedUnits); service and total RPU ~ ASP (Data_Elasticity); the chain calculator.'),
 ('Checks', 'OK/FAIL on the key outputs and the reference regression values.'),
 ('Data_* (everything else)', 'Every committed CSV in data/csv/, one tab each, provenance in row 2. Copart transcript series are Tier 2 (hand-transcribed); SEC filings Tier 1; sitemap-derived series Tier 3.'),
 ('', ''),
 ('WHERE THE METHOD IS WRITTEN UP', 'docs/AGE_CURVES.md (S, R, P: evidence, fit, validation, manual pulls) · MODEL_BLUEPRINT.md (architecture, mechanisms A–E, build order) · findings.md Addenda 14–16 · PROVENANCE.md §5 (every host and file).'),
 ('NOT IN THIS WORKBOOK', 'Licensed material (S&P transcripts, Stephens preview, SOLS model) and the IHS-sourced ORNL tables (3.11/3.12/3.13, "further reproduction prohibited") — cited by table number only. Lot-level sitemap rows (1.3M) — in data/cprt.db.'),
]
for i, (a, b) in enumerate(readme):
    r = 4 + i; put(ws, f'A{r}', a, BOLD if (b == '' and a) else BLK); put(ws, f'B{r}', b, BLK, wrap=True)
    if b: ws.row_dimensions[r].height = max(15, 15 * (1 + len(b) // 110))
widths(ws, {'A': 30, 'B': 120})

wb.move_sheet('README', offset=-wb.index(wb['README']))
OUT.parent.mkdir(exist_ok=True); wb.save(OUT)
nform = sum(1 for s in wb.worksheets for row in s.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith('='))
print(f"-> {OUT.relative_to(ROOT)}  sheets={len(wb.worksheets)}  formulas={nform}")
