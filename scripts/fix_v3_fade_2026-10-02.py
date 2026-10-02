"""RPM FY29–31: replace the typed 3% service-revenue fade with a derivation. Each driver fades from its FY28 engine value to a
long-run anchor: g(t) = anchor + (g_FY28 − anchor) × decay^(t−2028). Anchors: fleet growth (E1 roll) + TLF drift input for US
insurance units; BLS used-car CPI 10-yr CAGR × fee pass-through (E5) for revenue per unit. Service revenue = units × RPU."""
import sys, pathlib, re; sys.path.insert(0, str(pathlib.Path(__file__).parent))
import openpyxl
from cprt_model.common import *
P = ROOT / 'model/CPRT_Model_v3.xlsx'; wb = openpyxl.load_workbook(P); rpm = wb['RPM']; df = wb['D Facts']; src = wb['Sources']
# ---- BLS used cars and trucks CPI (CUUR0000SETA02), annual averages, from the file on disk
ann = {}
for line in open(ROOT / 'raw/bls/cu.data.14.USTransportation'):
    p = [x.strip() for x in line.split('\t')]
    if p[0] == 'CUUR0000SETA02' and p[2] == 'M13': ann[int(p[1])] = float(p[3])
c10 = (ann[2025] / ann[2015]) ** 0.1 - 1; c20 = (ann[2025] / ann[2005]) ** 0.05 - 1
print(f'BLS used-car CPI annual averages 2015 {ann[2015]:.3f} → 2025 {ann[2025]:.3f}: 10-yr CAGR {c10:.4%}; 2005 {ann[2005]:.3f}: 20-yr CAGR {c20:.4%}')
for r, (yrs, val, key) in zip((52, 53), ((('2015→2025', 10), c10, 'bls_used_car_cpi_cagr_10y'), (('2005→2025', 20), c20, 'bls_used_car_cpi_cagr_20y'))):
    put(df, f'B{r}', f'Used cars and trucks CPI, {yrs[1]}-year CAGR of annual averages, {yrs[0]}', 'label'); put(df, f'C{r}', key, 'label', i=True); put(df, f'D{r}', round(val, 6), 'input', F_PCT2); put(df, f'E{r}', '%', 'label', i=True)
    put(df, f'F{r}', 'MEASURED', 'note'); put(df, f'G{r}', f'BLS CPI-U series CUUR0000SETA02 (used cars and trucks, U.S. city average, NSA), annual averages (period M13): {ann[2025 - yrs[1]]:.3f} → {ann[2025]:.3f}', 'note'); put(df, f'H{r}', '2025 annual average', 'note'); put(df, f'I{r}', 'raw/bls/cu.data.14.USTransportation (on disk; no new request)', 'note')
# ---- RPM fade block, rows 53–60
group(rpm, 53, 'FY29–31 fade derivation — each driver: g(t) = anchor + (g_FY28 − anchor) × decay^(t − 2028); service revenue = fee units × revenue per unit')
rows = [(54, 'Long-run fleet growth: total vehicles on the road, CY2027 → CY2028 (E1 fleet roll, row 35)', "='E1 Fleet'!M35/'E1 Fleet'!L35-1", 'link', F_PCT2, 'ENGINE / MEASURED: births held at the 2027 level with the stretched EPA survival schedule (E1 inputs); claims scale with the fleet'),
        (55, 'Total-loss-frequency drift beyond FY28 (points of US insurance unit growth a year)', 0, 'input', F_PCT2, 'ASSUMED 0: the thesis-2 case holds its FY27 endpoint through FY28 (E4 D56). Negative continues the aftermarket drift; positive restores the pre-2024 CCC uptrend'),
        (56, 'US insurance unit growth — long-run anchor', '=D54+D55', 'formula', F_PCT2, 'Fleet growth + TLF drift; row 21 fades from the FY28 engine value to this'),
        (57, 'Used-vehicle price inflation — long-run anchor (BLS CPI used cars and trucks, 10-yr CAGR)', "='D Facts'!D52", 'link', F_PCT2, 'MEASURED 2.3% (2015→2025 annual averages; includes the 2021–22 spike). 20-yr CAGR 1.4% on D Facts D53 is the conservative alternative'),
        (58, 'Fee pass-through of ASP to all-in revenue per unit (buyer-fee elasticity, E5 D51)', "='E5 Prices & Fees'!D51", 'link', '0.00', 'ENGINE-derived 0.42: fees are tiered on the sale price, so revenue per unit rises less than ASP'),
        (59, 'Revenue per unit growth — long-run anchor', '=D57*D58', 'formula', F_PCT2, 'ASP inflation × pass-through; row 34 fades from the FY28 engine value to this'),
        (60, 'Fade speed: share of the gap to the anchor remaining after one year', 0.5, 'input', '0.00', 'ASSUMED: half the FY28 gap closes each year (FY29 ½, FY30 ¼, FY31 ⅛)')]
for r, lab, val, kind, fmt, note in rows:
    put(rpm, f'B{r}', lab, 'label', b=(r in (56, 59))); put(rpm, f'D{r}', val, kind, fmt, b=(r in (56, 59))); put(rpm, f'P{r}', note, 'note')
# ---- drivers FY29–31
for k, c, p in ((1, 'K', 'J'), (2, 'L', 'K'), (3, 'M', 'L')):
    put(rpm, f'{c}21', f'=$D$56+($J$21-$D$56)*$D$60^{k}', 'formula', F_PCT)
    put(rpm, f'{c}34', f'=$D$59+($J$34-$D$59)*$D$60^{k}', 'formula', F_PCT)
    put(rpm, f'{c}33', f'={p}33*(1+{c}34)', 'formula', F_USD)
    put(rpm, f'{c}10', f'=IF(ISNUMBER($D$43),{p}10*(1+$D$43),{c}29*{c}33/1000)', 'formula', F_MONEY)
put(rpm, 'B42', 'Beyond the engine horizon (FY29–31): drivers fade from the FY28 engine values to long-run anchors (derivation in rows 53–60)', 'label', b=True)
put(rpm, 'B43', 'Service revenue growth, FY29–31 — derived (units × revenue per unit, rows 53–60); type a rate in D43 to override', 'label'); rpm['D43'].value = None
put(rpm, 'P43', 'Override cell: blank = derivation; a typed rate replaces it for all three years', 'note')
put(rpm, 'B45', 'US insurance unit growth, FY29–31 — derived per year in row 21; long-run anchor shown here', 'label'); put(rpm, 'D45', '=D56', 'link', F_PCT2); put(rpm, 'P45', 'Row 21 K–M fade from the FY28 engine value (J21) to this anchor', 'note')
put(rpm, 'P10', 'FY27–28 from Scenarios (selected case); FY29–31 = fee units × revenue per unit (fade, rows 53–60) unless D43 is typed', 'note')
put(rpm, 'P21', 'FY27–28 from Scenarios (E2 pool × E3 share × E4); FY29–31 fade from the FY28 value to the anchor in D56', 'note')
put(rpm, 'P33', 'FY22–28 implied: service revenue ÷ global fee units. FY29–31 driver: prior × (1 + row 34)', 'note'); put(rpm, 'P34', 'FY23–28 implied from row 33; FY29–31 fade from the FY28 value to the anchor in D59', 'note')
# ---- Sources tab: the two RPM entries that were typed inputs
for r in range(5, src.max_row + 1):
    if src[f'B{r}'].value == 'RPM' and src[f'C{r}'].value in ('D43', 'D45'):
        put(src, f'D{r}', rpm[f"B{src[f'C{r}'].value[1:]}"].value, 'label'); put(src, f'E{r}', f"=RPM!{src[f'C{r}'].value}", 'link'); put(src, f'F{r}', 'derived (RPM rows 53–60)', 'note'); print('Sources row updated:', r, src[f'C{r}'].value)
wb.save(P); print('saved')
