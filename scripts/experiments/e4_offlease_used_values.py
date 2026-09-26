#!/usr/bin/env python3
"""E4 — Off-lease / used-supply mechanism for used-car CPI (the value side of the totaling spread).

Explanation tested: used-vehicle values are set largely by the supply of 2–4-year-old vehicles, which is new sales two to
four years earlier. That supply is KNOWN through 2028 from sales already recorded. If it explains used-car CPI, the
spread's value side becomes a driver-based forecast, not an extrapolation.

Construction (all local, no network):
  SUP(m)      = Σ new light-vehicle sales in months m−48 … m−24  (FRED TOTALNSA, thousands, NSA)   → the 2–4-year-old cohort
  used_yoy(q) = used cars & trucks CPI, NSA (CUUR0000SETA02), quarterly mean, YoY %
  new_yoy(q)  = new vehicles CPI, NSA (CUUR0000SETA01), quarterly mean, YoY %          (substitution / price anchor)
  vmt_yoy(q)  = vehicle miles travelled, NSA (FRED TRFVOLUSM227NFWA), quarterly sum, YoY %  (demand control)
  model:  used_yoy = a + b·sup_yoy + c·new_yoy + d·vmt_yoy      fit 1995Q1–2019Q4 · tested 2020Q1–latest (never fitted on 2020–22)
Also reported: the raw lag profile corr(used_yoy_q, sales_yoy_{q−k}), k = 0…20 quarters, so the 30–42-month lead is seen, not assumed.
Forecast: sup_yoy is data through the month 24 months after the last sales print; new_yoy and vmt_yoy held at their last
4-quarter mean (ASSUMED). Value-side spread contribution = −Δ(used_yoy) × 0.0815 per the TLF calibration.
Outputs: data/csv/used_car_cpi_drivers.csv ; report reports/E4_offlease_values.md (written by hand from this output).
"""
import csv, pathlib, statistics as st, sys
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
def rd(p): return [r for r in csv.DictReader(l for l in open(p) if not l.startswith('#'))]
# ---- monthly inputs
sales = {r['observation_date'][:7]: float(r['TOTALNSA']) for r in rd(ROOT/'data/csv/fred_TOTALNSA.csv') if r['TOTALNSA'] not in ('', '.')}
vmt = {r['observation_date'][:7]: float(r['TRFVOLUSM227NFWA']) for r in rd(ROOT/'raw/fred/TRFVOLUSM227NFWA.csv') if r['TRFVOLUSM227NFWA'] not in ('', '.')}
cpi = {'CUUR0000SETA02': {}, 'CUUR0000SETA01': {}}
for line in open(ROOT/'raw/bls/cu.data.14.USTransportation', encoding='utf-8', errors='ignore'):
    p = [x.strip() for x in line.split('\t')]
    if len(p) >= 4 and p[0] in cpi and p[2].startswith('M') and p[2] != 'M13' and p[3] not in ('', '-'):
        cpi[p[0]][f"{p[1]}-{p[2][1:]}"] = float(p[3])
used_m, new_m = cpi['CUUR0000SETA02'], cpi['CUUR0000SETA01']
def ym(y, m): return f"{y:04d}-{m:02d}"
def shift(key, k):  # key 'YYYY-MM' shifted by k months
    y, m = int(key[:4]), int(key[5:]); i = y * 12 + (m - 1) + k; return ym(i // 12, i % 12 + 1)
months = sorted(sales)
SUP = {}
for k in [shift(months[0], i) for i in range(0, len(months) + 24)]:   # SUP is known 24 months past the last sales print
    w = [sales.get(shift(k, -j)) for j in range(24, 49)]
    if all(v is not None for v in w): SUP[k] = sum(w)
# ---- quarterly
def q_of(key): y, m = int(key[:4]), int(key[5:]); return f"{y}Q{(m - 1) // 3 + 1}"
def qmean(series, agg=st.mean):
    b = {}
    for k, v in series.items(): b.setdefault(q_of(k), []).append(v)
    return {q: agg(v) for q, v in b.items() if len(v) == 3}
def qshift(q, k): i = int(q[:4]) * 4 + int(q[-1]) - 1 + k; return f"{i // 4}Q{i % 4 + 1}"
def yoy(qs): return {q: (v / qs[qshift(q, -4)] - 1) * 100 for q, v in qs.items() if qshift(q, -4) in qs}
used_q, new_q, vmt_q, sup_q, sales_q = yoy(qmean(used_m)), yoy(qmean(new_m)), yoy(qmean(vmt, sum)), yoy(qmean(SUP)), yoy(qmean(sales, sum))
# ---- lag profile (raw): corr(used_yoy_q, sales_yoy_{q-k})
common = sorted(q for q in used_q if q >= '1980Q1')
print("Lag profile: corr(used-car CPI YoY_q, new-sales YoY_{q-k}), 1980Q1–2019Q4 then full sample")
for span, lo, hi in (('1980–2019', '1980Q1', '2019Q4'), ('1980–latest', '1980Q1', '2099Q4')):
    out = []
    for k in range(0, 21):
        pairs = [(used_q[q], sales_q[qshift(q, -k)]) for q in common if lo <= q <= hi and qshift(q, -k) in sales_q]
        a, b = np.array(pairs).T; out.append((k, np.corrcoef(a, b)[0, 1], len(pairs)))
    print(f"  {span}: " + " ".join(f"k{k}:{c:+.2f}" for k, c, n in out))
# ---- regression
def design(q): return [1.0, sup_q[q], new_q[q], vmt_q[q]]
have = [q for q in common if q in sup_q and q in new_q and q in vmt_q]
def fit(qs):
    X = np.array([design(q) for q in qs]); y = np.array([used_q[q] for q in qs])
    b, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ b; n, k = X.shape
    s2 = res @ res / (n - k); se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    r2 = 1 - res @ res / ((y - y.mean()) @ (y - y.mean())); rho = np.corrcoef(res[:-1], res[1:])[0, 1]
    return b, se, r2, rho, n
names = ['const', 'sup_yoy', 'new_yoy', 'vmt_yoy']
results = {}
for label, lo, hi in (('fit 1995Q1–2019Q4', '1995Q1', '2019Q4'), ('fit 1995Q1–latest', '1995Q1', '2099Q4'), ('fit 1980Q1–2019Q4', '1980Q1', '2019Q4')):
    qs = [q for q in have if lo <= q <= hi]; b, se, r2, rho, n = fit(qs); results[label] = (b, se, r2, rho, n)
    print(f"\n{label}: n={n} R²={r2:.3f} resid ρ1={rho:.2f} eff n≈{n*(1-rho)/(1+rho):.0f}")
    for nm, bi, si in zip(names, b, se): print(f"   {nm:8s} {bi:+8.3f}  (se {si:.3f}, t {bi/si:+.1f})")
b_pre = results['fit 1995Q1–2019Q4'][0]
# ---- out of sample 2020Q1–latest with the pre-2020 fit
oos = [q for q in have if q >= '2020Q1']
print("\nOut of sample (coefficients frozen at the 1995–2019 fit):")
print("  quarter  used_yoy  fitted  error   sup_yoy  new_yoy  vmt_yoy")
errs = []
for q in oos:
    f = float(np.array(design(q)) @ b_pre); errs.append(used_q[q] - f)
    print(f"  {q}  {used_q[q]:+7.1f}  {f:+6.1f}  {used_q[q]-f:+6.1f}   {sup_q[q]:+6.1f}   {new_q[q]:+5.1f}   {vmt_q[q]:+5.1f}")
e = np.array(errs); print(f"  OOS MAE {np.mean(np.abs(e)):.2f}pp (all) · {np.mean(np.abs(e[[i for i,q in enumerate(oos) if q>='2023Q1']])):.2f}pp (2023Q1+) · mean error {e.mean():+.2f}pp")
# ---- forecast: sup_yoy is data as far as sales allow; new/vmt held at trailing 4q means (ASSUMED)
last_q = have[-1]; new_hold = st.mean(new_q[qshift(last_q, -k)] for k in range(4)); vmt_hold = st.mean(vmt_q[qshift(last_q, -k)] for k in range(4))
fc = []
q = qshift(last_q, 1)
while q in sup_q:
    f = b_pre[0] + b_pre[1] * sup_q[q] + b_pre[2] * new_hold + b_pre[3] * vmt_hold; fc.append((q, sup_q[q], f)); q = qshift(q, 1)
print(f"\nForecast (1995–2019 coefficients; new_yoy held {new_hold:+.1f}, vmt_yoy held {vmt_hold:+.1f} — ASSUMED):")
print("  quarter  sup_yoy  used_yoy_fc  Δ vs last actual  value-side ΔTLF contribution (×0.0815, pp)")
for q, s, f in fc: print(f"  {q}  {s:+6.1f}   {f:+6.1f}     {f-used_q[last_q]:+6.1f}          {-(f-used_q[last_q])*0.0815:+.2f}")
# ---- alternative: LEVEL specification. log(used CPI / new CPI) on log(SUP / 10-yr trailing sales), quarterly, 1995Q1–2019Q4
ratio_m = {k: used_m[k] / new_m[k] for k in used_m if k in new_m}
scale = {k: sum(sales.get(shift(k, -j), 0) for j in range(0, 120)) for k in SUP}   # trailing 10y sales; last 24 months of SUP reuse the last 120 sales months (ASSUMED scale)
rel = {k: SUP[k] / scale[k] for k in SUP if k in scale and scale[k] > 0}
rq, relq = qmean(ratio_m), qmean(rel)
for label, lo, hi in (('LEVEL fit 1995Q1–2019Q4', '1995Q1', '2019Q4'), ('LEVEL fit 1995Q1–latest', '1995Q1', '2099Q4')):
    qs = [q for q in sorted(rq) if lo <= q <= hi and q in relq]
    X = np.array([[1.0, np.log(relq[q]), (int(q[:4]) + int(q[-1]) / 4 - 2000)] for q in qs]); y = np.log([rq[q] for q in qs])
    b, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ b; n, k = X.shape; se = np.sqrt(np.diag(res @ res / (n - k) * np.linalg.inv(X.T @ X)))
    rho = np.corrcoef(res[:-1], res[1:])[0, 1]; r2 = 1 - res @ res / ((y - y.mean()) @ (y - y.mean()))
    print(f"\n{label}: log(used/new) = a + b·log(2-4yo stock / 10y sales) + c·trend   n={n} R²={r2:.3f} ρ1={rho:.2f}")
    print(f"   elasticity b = {b[1]:+.3f} (se {se[1]:.3f}, t {b[1]/se[1]:+.1f}); trend {b[2]:+.4f}/yr")
    if label.startswith('LEVEL fit 1995Q1–2019Q4'):
        b_lvl = b[1]; base = qshift(have[-1], 0)
        print(f"   implied path from the KNOWN 2-4yo stock (elasticity {b_lvl:+.3f}, everything else constant):")
        print("   quarter   stock/scale vs 2026Q2   implied Δ log(used/new) %   → spread value-side pp   → ΔTLF pp (×0.0815)")
        for q in sorted(relq):
            if q > base and q <= qshift(base, 9):
                d = b_lvl * np.log(relq[q] / relq[base]) * 100
                print(f"   {q}   {relq[q]/relq[base]-1:+6.1%}                {d:+5.2f}                     {-d:+5.2f}               {-d*0.0815:+.3f}")
# ---- write CSV
out = ROOT/'data/csv/used_car_cpi_drivers.csv'
with open(out, 'w', newline='') as fh:
    fh.write("# E4 (scripts/experiments/e4_offlease_used_values.py): used-car CPI (CUUR0000SETA02, NSA, quarterly mean YoY %) vs the 2-4-year-old cohort supply "
             "(sum of FRED TOTALNSA sales in months m-48..m-24, YoY %), new-vehicle CPI YoY (CUUR0000SETA01) and VMT YoY (FRED TRFVOLUSM227NFWA). "
             f"fitted = 1995Q1-2019Q4 coefficients {['%.3f' % v for v in b_pre]} [const, sup, new, vmt]; rows with type=forecast hold new/vmt at trailing 4q means (ASSUMED). MEASURED inputs, FITTED coefficients.\n")
    w = csv.writer(fh); w.writerow(['quarter', 'type', 'used_yoy', 'sup_2to4yo_yoy', 'new_vehicle_cpi_yoy', 'vmt_yoy', 'fitted_used_yoy'])
    for q in have:
        w.writerow([q, 'in-sample' if q <= '2019Q4' else 'out-of-sample', round(used_q[q], 2), round(sup_q[q], 2), round(new_q[q], 2), round(vmt_q[q], 2), round(float(np.array(design(q)) @ b_pre), 2)])
    for q, s, f in fc: w.writerow([q, 'forecast', '', round(s, 2), round(new_hold, 2), round(vmt_hold, 2), round(f, 2)])
print(f"\nwrote {out}")
