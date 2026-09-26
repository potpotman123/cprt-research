#!/usr/bin/env python3
"""E3 — the repair side of the totaling spread, taken apart into drivers (decomposition, not regression).

Series (all MEASURED, on disk):
  repair CPI     BLS CUUR0000SETD  motor vehicle maintenance & repair, NSA         data/csv/cprt_cpi_three_series.csv
  parts PPI      BLS PCU3363--3363-- motor vehicle parts manufacturing              data/csv/ppi_motor_vehicle_parts.csv
  body-shop wages  CES8081110003 avg hourly earnings, automotive repair & maintenance (SA)   raw/bls/ce.data.80b.*
  body-shop jobs   CES8081110001 all employees, automotive repair & maintenance (SA)         raw/bls/ce.data.80a.*
  all-private wages CES0500000003 (comparator)                                              raw/bls/ce.data.05b.* (if fetched)
  CCC TCOR / labor-rate statements                                                          data/csv/ccc_affordability_points.csv
Accounting identity for collision repair cost (CCC TCOR):  ΔTCOR ≈ w_L·(Δrate + Δhours) + w_P·(Δparts price + Δparts count) + w_M·Δmisc,
with CCC's cost shares w_L / w_P / w_M ASSUMED 0.45 / 0.40 / 0.15 (CCC publishes the split only as chart contributions). We do
not regress; we tabulate each driver's YoY by year and ask which of them the current +6–7% repair CPI is coming from.
"""
import csv, glob, pathlib, statistics as st
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent; D = ROOT / 'data/csv'
def rd(f): return [r for r in csv.DictReader(l for l in open(f) if not l.startswith('#'))]
def bls_flat(path, sid):
    out = {}
    for line in open(path, encoding='utf-8', errors='ignore'):
        p = [x.strip() for x in line.split('\t')]
        if len(p) >= 4 and p[0] == sid and p[2].startswith('M') and p[2] != 'M13' and p[3] not in ('', '-'): out[f"{p[1]}-{p[2][1:]}"] = float(p[3])
    return out
def annual(m): 
    b = {}
    for k, v in m.items(): b.setdefault(int(k[:4]), []).append(v)
    return {y: st.mean(v) for y, v in b.items() if len(v) >= 6}
def yoy(a): return {y: (a[y] / a[y - 1] - 1) * 100 for y in a if y - 1 in a}
repair = annual({r['date']: float(r['CUUR0000SETD']) for r in rd(D / 'cprt_cpi_three_series.csv') if r.get('CUUR0000SETD')})
used = annual({r['date']: float(r['CUUR0000SETA02']) for r in rd(D / 'cprt_cpi_three_series.csv') if r.get('CUUR0000SETA02')})
parts = annual({r['month']: float(r['ppi_mv_parts']) for r in rd(D / 'ppi_motor_vehicle_parts.csv')})
ces_b = glob.glob(str(ROOT / 'raw/bls/ce.data.80b*')); ces_a = glob.glob(str(ROOT / 'raw/bls/ce.data.80a*')); ces_p = glob.glob(str(ROOT / 'raw/bls/ce.data.05b*'))
wage = annual(bls_flat(ces_b[0], 'CES8081110003')) if ces_b else {}
jobs = annual(bls_flat(ces_a[0], 'CES8081110001')) if ces_a else {}
allw = annual(bls_flat(ces_p[0], 'CES0500000003')) if ces_p else {}
R, U, P, W, J, A = yoy(repair), yoy(used), yoy(parts), yoy(wage), yoy(jobs), yoy(allw)
print("year  repairCPI  usedCPI  spread   partsPPI  8111 AHE  allPriv AHE  8111 jobs   (annual averages, YoY %)")
for y in range(2012, 2027):
    f = lambda d: f"{d[y]:6.1f}" if y in d else "   n/a"
    print(f"{y}  {f(R)}     {f(U)}   {f({k: R[k]-U[k] for k in R if k in U})}    {f(P)}    {f(W)}     {f(A)}       {f(J)}")
# accounting decomposition of collision repair cost (CCC TCOR) with ASSUMED shares, using labor rate ≈ 8111 AHE and parts price ≈ parts PPI
wl, wp, wm = 0.45, 0.40, 0.15
tcor = {2024: 3.7, 2025: 1.7}  # CCC: TCOR +3.7% (2024), +1.7% prelim (2025) — ccc_affordability_points.csv
print("\nCollision repair cost (CCC TCOR) vs its drivers (shares ASSUMED 45/40/15 labor/parts/misc; hours & parts count from CCC text: down slightly):")
for y in (2024, 2025):
    if y in W and y in P:
        implied = wl * W[y] + wp * P[y]
        print(f"  {y}: TCOR {tcor[y]:+.1f}%  | labor rate {W[y]:+.1f}% × {wl} + parts price {P[y]:+.1f}% × {wp} = {implied:+.1f}% before hours/count/mix; CCC labor rate stated {'+4.7' if y == 2024 else '+3.0/+3.1'}%")
print("\nReading: repair CPI (SETD) is a constant-quality service price; CCC TCOR is the mix-affected average claim. Where they diverge, the mix (older, cheaper-to-repair cars taking a larger share of repairables) is the wedge — see reports/E3_repair_labour.md.")
with open(D / 'repair_cost_drivers.csv', 'w', newline='') as f:
    f.write("# E3 (scripts/experiments/e3_repair_cost_drivers.py): annual-average YoY % of repair CPI (SETD), used-car CPI (SETA02), motor-vehicle-parts PPI (PCU3363), automotive repair & maintenance avg hourly earnings (CES8081110003) and employment (CES8081110001), all-private AHE (CES0500000003). MEASURED.\n")
    w = csv.writer(f); w.writerow(['year', 'repair_cpi_yoy', 'used_cpi_yoy', 'parts_ppi_yoy', 'auto_repair_ahe_yoy', 'all_private_ahe_yoy', 'auto_repair_jobs_yoy'])
    for y in range(2007, 2027): w.writerow([y] + [round(d[y], 2) if y in d else '' for d in (R, U, P, W, A, J)])
print("wrote repair_cost_drivers.csv")
