#!/usr/bin/env python3
"""Recalculate model/CPRT_Model_v2.xlsx headlessly with LibreOffice and check key cells against the Python scripts."""
import subprocess, pathlib, csv, sys, openpyxl, shutil, tempfile
ROOT = pathlib.Path(__file__).resolve().parent.parent; SRC = ROOT / 'model/CPRT_Model_v2.xlsx'
tmp = pathlib.Path(tempfile.mkdtemp()); subprocess.run(['soffice', '--headless', '--calc', '--convert-to', 'xlsx', '--outdir', str(tmp), str(SRC)], check=True, capture_output=True, timeout=300)
RC = tmp / SRC.name; wb = openpyxl.load_workbook(RC, data_only=True); shutil.copy(RC, ROOT / 'model/CPRT_Model_v2_recalc.xlsx')
fails = 0
def check(name, got, exp, tol):
    global fails
    if not isinstance(got, (int, float)): got = None
    ok = got is not None and abs(got - exp) <= tol; fails += (not ok); print(f"{'PASS' if ok else 'FAIL'} {name}: got {got} expected {exp} (tol {tol})")
ws = wb['E1 Fleet']
# E1 vs the committed backtest CSV (fleet share by cell, 2025) and the CCC-implied shares
rows = [r for r in csv.DictReader(open(ROOT / 'docs/source_trace_2026-10-01/fleet_vs_ccc_claim_mix.csv'))]
body_map = {'Car': 'Car', 'Utility Vehicle': 'SUV', 'Pickup': 'Pickup', 'Van': 'Van'}; order = ['Car', 'SUV', 'Pickup', 'Van']; bands = ['0 (current/newer)', '1-3', '4-6', '7+']
col = {2020: 'E', 2021: 'F', 2022: 'G', 2023: 'H', 2024: 'I', 2025: 'J'}
tot25 = ws['J35'].value
for r in rows:
    if r['year'] != '2025': continue
    key = body_map[r['body']]; bi = bands.index(r['age_group']); row = 19 + order.index(key) * 4 + bi
    check(f'E1 fleet share 2025 {key} {r["age_group"]}', ws[f'J{row}'].value / tot25 if tot25 else None, float(r['model_fleet_share']), 0.002)
    check(f'E1 CCC-implied 2025 {key} {r["age_group"]}', ws[f'J{40+16+order.index(key)*4+bi}'].value, float(r['ccc_implied_claim_share']), 0.0005)
# body-adjusted claim shares: unadjusted × factor, renormalised
fac = {'Car': 1.110, 'SUV': 0.917, 'Pickup': 1.028, 'Van': 0.923}
for year in (2020, 2025):
    raw = {(body_map[r['body']], bands.index(r['age_group'])): float(r['model_claim_share']) * fac[body_map[r['body']]] for r in rows if int(r['year']) == year}
    s = sum(raw.values())
    for (key, bi), v in raw.items(): check(f'E1 model claim share {year} {key} band {bi}', ws[f'{col[year]}{40+order.index(key)*4+bi}'].value, v / s, 0.002)
for ref in ('G81', 'G82', 'G83', 'G84'): print('E1 check cell', ref, ws[ref].value, ws[f'D{ref[1:]}'].value)
print('total 2024 fleet (000s):', ws['I35'].value, 'share 7+ 2024:', ws['I36'].value, 'max gap by year:', [round(ws[f'{c}77'].value or 0, 4) for c in 'EFGHIJ'])
import json
if 'E2 Claims & Totals' in wb.sheetnames:
    e2 = wb['E2 Claims & Totals']
    check('E2 weights sum FQ1 FY26', e2['D13'].value, 1.0, 1e-6); check('E2 weights sum FQ4 FY28', e2['O13'].value, 1.0, 1e-6)
    check('E2 aggregate TLF FQ1 FY26 vs CCC-cell-weighted 2025 (0.2312; composition differs slightly)', e2['D73'].value, 0.23124, 0.006)
    print('E2 pool y/y FY27 quarters:', [round(e2[f'{c}72'].value, 4) for c in 'HIJK'], 'FY28:', [round(e2[f'{c}72'].value, 4) for c in 'LMNO'])
if 'E3 Carriers' in wb.sheetnames:
    e3 = wb['E3 Carriers']; inp = json.load(open(ROOT / 'model/linked_service_revenue_2026-09-28/inputs.json'))
    for col, idx in (('D', 0), ('G', 3), ('H', 4), ('K', 7)):
        exp = sum(c['weights'][3] * (c['allocations'][idx] if (idx <= 3 or c['name'] == 'Progressive') else c['allocations'][3]) for c in inp['carriers']); check(f'E3 base share col {col} (frozen weights; PGR path, others frozen at FQ4 FY26)', e3[f'{col}43'].value, exp, 1e-4)
    check('E3 weights sum', e3['D16'].value, 1.0, 1e-6)
    print('E3 share ratio y/y base FY27:', [round(e3[f'{c}48'].value, 4) for c in 'HIJK'], 'thesis A:', [round(e3[f'{c}49'].value, 4) for c in 'HIJK'])
if 'E4 Aftermarket' in wb.sheetnames:
    e4 = wb['E4 Aftermarket']; check('E4 bill change FQ4 FY27 (documented -1.03%)', e4['K14'].value, -0.0103, 0.0003)
    check('E4 unit change FQ4 FY27 vs engine larger-shift FY delta (-2.057%)', e4['K40'].value, -0.02057, 0.001)
    print('E4 price change FY27 quarters:', [round(e4[f'{c}41'].value or 0, 4) for c in 'HIJK'], 'engine dService FY27:', e4['Q26'].value)
if 'E5 Prices & Fees' in wb.sheetnames:
    e5 = wb['E5 Prices & Fees']; check('E5 FY26 insurance $ = 0.9 x US service', e5['P8'].value, 0.9 * e5['P6'].value, 0.01)
    check('E5 core RPU at anchor reproduces engine 851.51', e5['D23'].value, 851.51, 0.05); print('E5 implied FY26 units (000s):', [round(e5[f'{c}11'].value) for c in 'DEFG'], 'all-in RPU FY27 y/y:', [round(e5[f'{c}26'].value, 4) for c in 'HIJK'])
if 'E6 Other Branches' in wb.sheetnames:
    e6 = wb['E6 Other Branches']; print('E6 FY26A/FY27E other-US, intl, purchased:', [round(e6[f'{c}{r}'].value, 1) for r in (8, 12, 16) for c in 'PQ'])
if 'Scenarios' in wb.sheetnames:
    sc = wb['Scenarios']; rep = 3969.52  # FY26 global service revenue, 8-K (RPM H10)
    check('Scenarios FY26 legacy service (case 1) vs 8-K service total', sc['P16'].value, rep, 0.5)
    for k in range(1, 6): print(f'Scenarios case {k}: FY27 legacy', round(sc[f"Q{7+(k-1)*13+9}"].value, 1), 'FY28', round(sc[f"R{7+(k-1)*13+9}"].value, 1), 'FY27 units y/y', round(sc[f"Q{7+(k-1)*13+2}"].value, 4))
    s0 = 75 + 9; print('Summary dvsNeither / dvsJPM:', [(round(sc[f'E{s0+k}'].value, 1), round(sc[f'F{s0+k}'].value, 1)) for k in range(1, 6)], 'engine mask10/15:', sc[f'D{s0+7}'].value, sc[f'D{s0+8}'].value)
    rpm = wb['RPM']; print('RPM I10/J10/K10 service, I6 total, I21 units y/y, I33 RPU, D50 delta JPM:', [rpm[c].value for c in ('I10', 'J10', 'K10', 'I6', 'I21', 'I33', 'D50')])
    ck = wb['Checks']; print('Checks:', [(ck[f'B{r}'].value[:40], ck[f'G{r}'].value) for r in range(5, 15) if ck[f'B{r}'].value])
    print('Street brokers:', [wb['Street'][f'{c}4'].value for c in 'DEFGHIJKLMN' if wb['Street'][f'{c}4'].value]); print('Street B4:', wb['Street']['B4'].value); print('Street FY27 service row:', [wb['Street'][f'{c}7'].value for c in 'DEFGHIJKLMN'])
print('FAILS', fails); sys.exit(1 if fails else 0)
