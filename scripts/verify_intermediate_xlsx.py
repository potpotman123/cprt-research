#!/usr/bin/env python3
"""Evaluate the key formulas of model/CPRT_Intermediate.xlsx with pycel and compare with scripts/age_curves.py.

No LibreOffice on this machine, so the workbook cannot be recalculated in place; pycel evaluates the formula graph
directly from the file. RSQ and CORREL are not implemented in pycel — those two cells are checked by recomputing the
statistics in Python from the same Data_* ranges.

Usage:  ./.venv/bin/python scripts/verify_intermediate_xlsx.py
"""
import csv, pathlib, re, statistics as st, sys, warnings
warnings.filterwarnings('ignore')
from pycel import ExcelCompiler
ROOT = pathlib.Path(__file__).resolve().parent.parent
XL = ROOT / 'model/CPRT_Intermediate.xlsx'
xl = ExcelCompiler(filename=str(XL))

def val(name):   # age_curves_validation.csv model values by key
    out = {}
    for r in csv.DictReader(l for l in open(ROOT / 'data/csv/age_curves_validation.csv') if not l.startswith('#')):
        out[(r['kind'], r['year'], r['statistic'])] = r['model']
    return out
V = val('x'); fitv = lambda k: float(V[('fit', '2024', k)])
YEARS = list(range(2013, 2031)); col = lambda y: chr(ord('C') + YEARS.index(y))
c24, c19, c20, c25 = col(2024), col(2019), col(2020), col(2025)

tests = [  # cell, expected, tolerance, label
 ('Inputs!%s34' % c24, 1.194, 1e-3, 'k multiplier 2024'),
 ('Survival!C6', 1.0, 1e-9, 'S(0)=1'),
 ('FleetByAge!%s53' % c24, 292, 3, 'VIO 2024 (M)'), ('FleetByAge!%s54' % c24, 0.645, 0.005, 'share 7+ 2024'),
 ('Calibration!K13', fitv('tlf'), 0.0015, 'cal tlf'), ('Calibration!K14', fitv('tl7'), 0.004, 'cal tl7'), ('Calibration!K15', fitv('rp7'), 0.004, 'cal rp7'),
 ('Calibration!K16', fitv('rp3'), 0.004, 'cal rp3'), ('Calibration!K17', fitv('age_cl'), 0.06, 'cal age_cl'), ('Calibration!K18', fitv('age_rp'), 0.06, 'cal age_rp'),
 ('Calibration!K19', fitv('age_tl'), 0.06, 'cal age_tl'), ('Calibration!K20', fitv('p03'), 0.003, 'cal p03'), ('Calibration!N22', 1.0, 0.5, 'Solver loss at the fitted parameters'),
 ('TLF_Roll!%s8' % c24, fitv('tlf'), 0.0015, 'baseline TLF 2024'),
 ('TLF_Roll!%s8' % c19, float(V[('out_of_sample', '2019', '2019 TLF (demographics only)')]), 0.003, 'TLF 2019 (OOS)'),
 ('TLF_Roll!%s8' % c25, float(V[('out_of_sample', '2025', '2025 TLF (demographics only)')]), 0.003, 'TLF 2025 (OOS)'),
 ('TLF_Roll!%s14' % c20, float(V[('out_of_sample', '2020', '2020 avg age, claims')]), 0.06, '2020 avg claim age (OOS)'),
 ('TLF_Roll!%s11' % c25, float(V[('out_of_sample', '2025', '2025 TL 7+ share')]), 0.004, '2025 TL 7+ (OOS)'),
 ('Spread_Reg!T5', 0.0815, 0.001, 'spread slope (all-loss)'), ('Spread_Reg!T6', 0.599, 0.01, 'spread intercept'), ('Spread_Reg!T8', 27, 0, 'n'),
 ('Spread_Reg!U5', 0.0834, 0.001, 'spread slope (non-comp)'), ('Spread_Reg!T13', 1.28, 0.05, 'predicted 2Q26 dTLF'),
 ('RPU_Reg!K5', 0.599, 0.02, 'ASP~CPI slope'), ('RPU_Reg!K6', 3.23, 0.15, 'ASP~CPI intercept'), ('RPU_Reg!K8', 15, 0, 'n'),
 ('RPU_Reg!K12', 0.514, 0.003, 'service-RPU slope'), ('RPU_Reg!K13', 4.13, 0.05, 'service-RPU intercept'), ('RPU_Reg!L12', 0.752, 0.005, 'total-RPU slope'),
]
bad = 0
for cell, exp, tol, lab in tests:
    try: v = xl.evaluate(cell)
    except Exception as e: print(f"  ERR  {cell:18s} {lab:34s} {type(e).__name__}"); bad += 1; continue
    ok = isinstance(v, (int, float)) and abs(v - exp) <= tol; bad += (not ok)
    print(f"  {'ok ' if ok else 'BAD'}  {cell:18s} {lab:34s} = {round(v, 4) if isinstance(v, float) else v}   (expected {exp})")

# RSQ / CORREL: recompute in Python from the same ranges pycel cannot evaluate
def pear(x, y):
    mx, my = st.mean(x), st.mean(y); sxy = sum((a-mx)*(b-my) for a, b in zip(x, y))
    return sxy / (sum((a-mx)**2 for a in x) * sum((b-my)**2 for b in y)) ** 0.5
o = [xl.evaluate(f'Spread_Reg!O{r}') for r in range(5, 32)]; q = [xl.evaluate(f'Spread_Reg!Q{r}') for r in range(5, 32)]
print(f"  py   Spread_Reg!T7 RSQ (all-loss)            = {pear(o, q)**2:.3f}   (expected 0.814)")
g = [xl.evaluate(f'RPU_Reg!G{r}') for r in range(5, 20)]; h = [xl.evaluate(f'RPU_Reg!H{r}') for r in range(5, 20)]
print(f"  py   RPU_Reg!K7 CORREL (ASP~CPI)            = {pear(g, h):.3f}   (expected 0.770)")
e = [xl.evaluate(f'Data_Elasticity!E{r}') for r in range(5, 22)]; f = [xl.evaluate(f'Data_Elasticity!F{r}') for r in range(5, 22)]
print(f"  py   RPU_Reg!K14 RSQ (service RPU ~ ASP)     = {pear(e, f)**2:.3f}   (expected 0.61)")

for r in range(5, 17):
    s = xl.evaluate(f'Checks!E{r}'); bad += (s != 'OK'); print(f"  Checks!E{r}: {s:4s} <- {xl.evaluate(f'Checks!A{r}')}")
print("  ALL CHECKS:", xl.evaluate('Checks!E18'))
print(f"problems: {bad}"); sys.exit(1 if bad else 0)
