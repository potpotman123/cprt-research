#!/usr/bin/env python3
"""Reproducible build of the 2026-09-11 analyses. Writes CSVs to data/csv/ and prints.
  1. TLF calibration:   dTLF(pp) = a + b*spread(t-1), CCC quarterly 2018Q1-2025Q3 (borrow-strength leg)
  2. Elasticity rebuild: implied RPU YoY vs global ASP YoY on aligned, basis-matched inputs
  3. Matched-denominator decomposition: calendar 2025 and FQ4 FY26
Every hand-transcribed input is listed inline with its source so a judge can check it.
"""
import csv, statistics as st, pathlib
from collections import defaultdict
ROOT = pathlib.Path(__file__).resolve().parent.parent; OUT = ROOT / "data/csv"

def ols(x, y):
    n = len(x); mx = st.mean(x); my = st.mean(y)
    sxx = sum((a-mx)**2 for a in x); sxy = sum((a-mx)*(b-my) for a, b in zip(x, y))
    b = sxy/sxx; a = my - b*mx; res = [yy-(a+b*xx) for xx, yy in zip(x, y)]
    sse = sum(r*r for r in res); sst = sum((v-my)**2 for v in y)
    rho = sum(res[i]*res[i+1] for i in range(len(res)-1))/sse if sse else 0
    return dict(a=a, b=b, se=(sse/(n-2)/sxx)**0.5, r2=1-sse/sst, n=n, rmse=(sse/(n-2))**0.5, rho1=rho, neff=n*(1-rho)/(1+rho))

# ============ 1. TLF calibration ============
cpi = {}
with open(OUT/"cprt_cpi_three_series.csv") as f:
    for r in csv.DictReader(f):
        g = lambda k: (float(r[k]) if r.get(k) not in ("", None) else None)
        cpi[r["date"]] = (g("CUUR0000SETA02_yoy_pct"), g("CUUR0000SETD_yoy_pct"))
qof = lambda d: f"{d[:4]}Q{(int(d[5:7])-1)//3+1}"
sq = defaultdict(list)
for d, (u, rp) in cpi.items():
    if len(d) == 7 and u is not None and rp is not None: sq[qof(d)].append(rp-u)
spread = {k: st.mean(v) for k, v in sq.items() if len(v) == 3}
spread_partial = {k: (st.mean(v), len(v)) for k, v in sq.items() if 0 < len(v) < 3}
tlf = {}
for line in open(OUT/"ccc_tlf_quarterly.csv"):
    if line[0] == "#" or line.startswith("quarter"): continue
    p = line.strip().split(",");  tlf[p[0]] = (float(p[1]), float(p[2]))
def lagq(q, k):
    y, qq = q.split("Q"); n = int(qq)-k; y = int(y)
    while n < 1: n += 4; y -= 1
    return f"{y}Q{n}"
py = lambda q: f"{int(q[:4])-1}Q{q[5]}"
rows = []
print("=== 1. TLF CALIBRATION  dTLF(pp,YoY) = a + b*spread(t-1) ===")
for name, idx in (("non_comprehensive", 0), ("all_loss_categories", 1)):
    pairs = [(spread[lagq(q, 1)], tlf[q][idx]-tlf[py(q)][idx], q) for q in sorted(tlf) if py(q) in tlf and lagq(q, 1) in spread]
    X = [p[0] for p in pairs]; Y = [p[1] for p in pairs]
    f = ols(X, Y)
    tr = [(x, y) for x, y, q in pairs if int(q[:4]) <= 2023]; te = [(x, y, q) for x, y, q in pairs if int(q[:4]) >= 2024]
    f2 = ols([t[0] for t in tr], [t[1] for t in tr]); mae = st.mean(abs(f2["a"]+f2["b"]*x-y) for x, y, q in te)
    print(f"  {name:22s} n={f['n']} a={f['a']:+.3f} b={f['b']:+.4f} se={f['se']:.4f} R2={f['r2']:.3f} rho1={f['rho1']:+.2f} neff~{f['neff']:.0f}  OOS(fit<=2023,7q) MAE={mae:.2f}pp")
    rows.append((name, f["n"], f["a"], f["b"], f["se"], f["r2"], f["rho1"], f["neff"], mae))
# live OOS: mgmt-cited CCC 2Q26 = 23.3 vs 2Q25 = 22.4 (all-loss variant)
fa = [r for r in rows if r[0] == "all_loss_categories"][0]
pred = fa[2] + fa[3]*spread["2026Q1"]
print(f"  LIVE OOS (all-loss): spread(2026Q1)={spread['2026Q1']:+.2f} -> pred dTLF {pred:+.2f}pp vs mgmt-cited actual +0.90pp (23.3-22.4); error {pred-0.9:+.2f}pp")
with open(OUT/"tlf_calibration.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["variant", "n", "intercept_pp", "beta", "se", "r2", "resid_rho1", "eff_n", "oos_mae_pp"]); w.writerows(rows)
with open(OUT/"totaling_spread_quarterly.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["quarter", "spread_pp", "months", "note"])
    for q in sorted(set(spread) | set(spread_partial)):
        if q in spread: w.writerow([q, round(spread[q], 3), 3, ""])
        else: w.writerow([q, round(spread_partial[q][0], 3), spread_partial[q][1], "partial quarter (BLS gap or not yet published)"])

# ============ 2. Elasticity rebuild ============
# global service revenue YoY: 8-K Ex-99.1 income statements (quarterly_pl.csv; FY26Q2 = 952,051/991,281)
# global TOTAL units YoY: earnings-call transcripts, hand-read ('over/nearly N' -> N; FY26Q3 derived from US -4.2 @82% + intl +5.9 @18%)
# global ASP YoY: reported_series.py (hand-verified). NOT stephens_exhibit7.global_asp_yoy, which is shifted one quarter.
Q     = ["FY22Q4","FY23Q1","FY23Q2","FY23Q3","FY23Q4","FY24Q1","FY24Q2","FY24Q3","FY24Q4","FY25Q1","FY25Q2","FY25Q3","FY25Q4","FY26Q1","FY26Q2","FY26Q3","FY26Q4"]
svc   = [14.2,8.8,11.1,10.6,17.9,18.3,9.1,11.7,7.1,14.8,15.0,9.3,7.1,0.6,-4.0,2.1,1.4]
totrev= [18.0,10.3,10.3,8.7,12.9,14.2,6.6,10.3,7.2,12.4,14.0,7.5,5.2,0.7,-3.6,2.1,2.4]
units = [5.1,1.9,4.7,5.0,10.0,13.0,7.0,11.0,8.0,12.0,8.0,1.0,-0.9,-6.7,-8.0,-2.4,-2.9]
asp   = [8.3,5.0,0.0,-1.0,2.0,-1.0,-5.0,-3.0,-5.0,-1.0,2.0,3.0,5.6,8.5,6.0,4.6,3.5]
rpu = lambda s, u: 100*((1+s/100)/(1+u/100)-1)
print("\n=== 2. ELASTICITY REBUILD (n=17, global basis, aligned ASP) ===")
res = {}
for lbl, num in (("service_rpu", svc), ("total_rpu_mgmt_def", totrev)):
    Y = [rpu(s, u) for s, u in zip(num, units)]; f = ols(asp, Y); res[lbl] = f
    jk = [ols([asp[i] for i in range(17) if i != k], [Y[i] for i in range(17) if i != k])["b"] for k in range(17)]
    print(f"  {lbl:20s} beta={f['b']:+.3f} se={f['se']:.3f} CI95[{f['b']-2.13*f['se']:+.2f},{f['b']+2.13*f['se']:+.2f}] int={f['a']:+.2f}pp R2={f['r2']:.2f} jackknife[{min(jk):+.3f},{max(jk):+.3f}]")
Ys = [rpu(s, u) for s, u in zip(svc, units)]
for lbl, sel in (("FY22Q4-FY24Q4", range(0, 9)), ("FY25Q1-FY26Q4", range(9, 17))):
    f = ols([asp[i] for i in sel], [Ys[i] for i in sel]); print(f"  sub {lbl:14s} beta={f['b']:+.3f} se={f['se']:.3f} int={f['a']:+.2f} R2={f['r2']:.2f} n={f['n']}")
b = res["service_rpu"]["b"]
with open(OUT/"elasticity_rebuild.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["fiscal_q", "service_rev_yoy", "total_rev_yoy", "global_units_yoy", "global_asp_yoy", "service_rpu_yoy", "total_rpu_yoy", "fee_mix_component_pp"])
    for i, q in enumerate(Q): w.writerow([q, svc[i], totrev[i], units[i], asp[i], round(rpu(svc[i], units[i]), 2), round(rpu(totrev[i], units[i]), 2), round(rpu(svc[i], units[i]) - b*asp[i], 2)])

# ============ 3. Decomposition ============
print("\n=== 3. MATCHED-DENOMINATOR DECOMPOSITION ===")
tlf24, tlf25, tl, rep = 22.3, 23.1, -2.9, -9.7                       # CCC Crash Course 2026, All Loss Categories
claims = 100*((1+tl/100)/(tlf25/tlf24)-1); tlfrel = 100*(tlf25/tlf24-1)
cf = 100*(tlf24*(1+tl/100))/(tlf24*(1+tl/100)+(100-tlf24))            # flat repairable volume counterfactual
cprt_cy25 = st.mean([2.0, -2.0, -2.1, -7.3])                           # US ins ex-CAT: FY25Q2, Q3, Q4(no CAT comp), FY26Q1
print(f"  CY2025: claims {claims:+.1f}% + TLF {tlfrel:+.1f}% -> pool {tl:+.1f}%;  counterfactual TLF (flat repairable) {cf:.2f}% ({cf-tlf24:+.2f}pp);  Copart US ins exCAT {cprt_cy25:+.2f}% -> residual {cprt_cy25-tl:+.2f}pp")
freq, t25, t26, assign, exacct = -3.4, 22.4, 23.3, -5.0, 2.3           # FQ4 FY26 call, 2026-09-10
pool = 100*((1+freq/100)*(t26/t25)-1)
print(f"  FQ4FY26: freq {freq:+.1f}% x TLF {100*(t26/t25-1):+.1f}% -> pool {pool:+.2f}%;  assignments {assign:+.1f}%, ex-account {exacct:+.1f}% -> account {assign-exacct:+.1f}pp;  residual all-in {assign-pool:+.2f}pp, ex-account {exacct-pool:+.2f}pp")
with open(OUT/"decomposition.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["window", "claims_term_pct", "tlf_term_pct", "industry_pool_pct", "copart_measure", "copart_pct", "residual_pp", "notes"])
    w.writerow(["CY2025", round(claims, 2), round(tlfrel, 2), tl, "US ins units exCAT (avg FY25Q2-FY26Q1)", round(cprt_cy25, 2), round(cprt_cy25-tl, 2), f"CCC all-loss; counterfactual flat-repairable TLF {cf:.2f}% ({cf-tlf24:+.2f}pp); 0.48pp valuations!=flagged overshoot"])
    w.writerow(["FQ4FY26", freq, round(100*(t26/t25-1), 2), round(pool, 2), "US ins ASSIGNMENTS", assign, round(assign-pool, 2), "mgmt-cited Fast Track freq (per exposure) and CCC 2Q26 TLF; transcript provenance"])
    w.writerow(["FQ4FY26_ex_account", freq, round(100*(t26/t25-1), 2), round(pool, 2), "US ins ASSIGNMENTS ex 1 account", exacct, round(exacct-pool, 2), f"the account = {assign-exacct:+.1f}pp"])
print("\n-> tlf_calibration.csv, totaling_spread_quarterly.csv, elasticity_rebuild.csv, decomposition.csv")
