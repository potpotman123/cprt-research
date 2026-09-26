#!/usr/bin/env python3
"""E2 step 2 — does the auto-insurance price cycle explain claim frequency with a lag, net of miles driven?

freq_q  = Progressive personal-auto incurred accident frequency, YoY % (data/csv/pgr_frequency_quarterly.csv; Q1–Q3 each year from
          10-Qs; Q4 absent because the 10-K primary document carries no MD&A)
vmt_q   = FRED TRFVOLUSM227NFWA, quarterly sum, YoY %                    (exposure: accidents scale with miles)
ins_q   = BLS motor-vehicle insurance CPI (CUUR0000SETE), quarterly mean, YoY %   (affordability shock)
Model:  freq_q = a + b·vmt_q + Σ_k c_k·ins_{q−k}, one lag at a time k = 0…8, and a restricted form with the best lag.
The affordability channel predicts c_k < 0 at a policy-cycle lag (2–4 quarters): dearer insurance → higher deductibles,
liability-only, non-renewal → fewer FILED claims per mile. Also reports the same for Progressive's collision-only bullet and
for CCC's $1,000+ deductible share (2021Q1–2025Q4) as the mechanism's direct footprint.
"""
import csv, pathlib, statistics as st
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent; D = ROOT / 'data/csv'
def rd(f): return [r for r in csv.DictReader(l for l in open(f) if not l.startswith('#'))]
def qshift(q, k): i = int(q[:4]) * 4 + int(q[-1]) - 1 + k; return f"{i // 4}Q{i % 4 + 1}"
# --- Progressive frequency: filing date → quarter covered (10-Q filed May→Q1, Aug→Q2, Nov→Q3)
freq, coll, sev = {}, {}, {}
for r in rd(D / 'pgr_frequency_quarterly.csv'):
    if r['form'] != '10-Q' or r['freq_total_q'] in ('', 'None'): continue
    y, m = int(r['filing_date'][:4]), int(r['filing_date'][5:7]); q = f"{y}Q{1 if m <= 5 else 2 if m <= 8 else 3}"
    freq[q] = float(r['freq_total_q'])
    if r['freq_collision_q'] not in ('', 'None'): coll[q] = float(r['freq_collision_q'])
    if r['severity_total_q'] not in ('', 'None'): sev[q] = float(r['severity_total_q'])
# --- VMT and insurance CPI, quarterly YoY
def q_of(k): y, m = int(k[:4]), int(k[5:7]); return f"{y}Q{(m - 1) // 3 + 1}"
vmt_m = {r['observation_date'][:7]: float(r['TRFVOLUSM227NFWA']) for r in rd(ROOT / 'raw/fred/TRFVOLUSM227NFWA.csv') if r['TRFVOLUSM227NFWA'] not in ('', '.')}
ins_m = {r['date']: float(r['CUUR0000SETE']) for r in rd(D / 'cprt_cpi_three_series.csv') if r.get('CUUR0000SETE')}
def qagg(series, agg):
    b = {}
    for k, v in series.items(): b.setdefault(q_of(k), []).append(v)
    return {q: agg(v) for q, v in b.items() if len(v) == 3}
def yoy(qs): return {q: (v / qs[qshift(q, -4)] - 1) * 100 for q, v in qs.items() if qshift(q, -4) in qs}
vmt, ins = yoy(qagg(vmt_m, sum)), yoy(qagg(ins_m, st.mean))
def ols(X, y):
    X = np.array(X); y = np.array(y); b, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ b; n, k = X.shape
    se = np.sqrt(np.diag(res @ res / (n - k) * np.linalg.inv(X.T @ X))); r2 = 1 - res @ res / ((y - y.mean()) @ (y - y.mean()))
    rho = np.corrcoef(res[:-1], res[1:])[0, 1] if n > 3 else float('nan'); return b, se, r2, rho, n
def run(dep, label, exclude_covid=True):
    qs = [q for q in sorted(dep) if q in vmt and q in ins and all(qshift(q, -k) in ins for k in range(9))]
    if exclude_covid: qs = [q for q in qs if not ('2020Q1' <= q <= '2021Q4')]
    print(f"\n== {label}: n={len(qs)} quarters {qs[0]}–{qs[-1]}" + (" (2020–21 excluded)" if exclude_covid else ""))
    b, se, r2, rho, n = ols([[1, vmt[q]] for q in qs], [dep[q] for q in qs])
    print(f"   VMT only: b_vmt {b[1]:+.2f} (t {b[1]/se[1]:+.1f}) R² {r2:.2f}")
    print("   lag k   c_k (ins CPI YoY, lagged k)    t      R²")
    best = None
    for k in range(9):
        b, se, r2, rho, n = ols([[1, vmt[q], ins[qshift(q, -k)]] for q in qs], [dep[q] for q in qs])
        print(f"     {k}    {b[2]:+.3f}                      {b[2]/se[2]:+.1f}   {r2:.2f}")
        if best is None or r2 > best[1]: best = (k, r2, b, se, rho)
    k, r2, b, se, rho = best
    print(f"   best lag {k}: freq = {b[0]:+.2f} {b[1]:+.2f}·vmt {b[2]:+.3f}·ins(t−{k});  R² {r2:.2f}, resid ρ1 {rho:.2f}")
    return qs
qs = run(freq, "Progressive total auto accident frequency YoY")
run(freq, "Progressive total auto accident frequency YoY", exclude_covid=False)
if len(coll) > 12: run(coll, "Progressive collision frequency YoY")
# --- deductible share vs insurance CPI (level on level; 20 quarters)
ded = {r['quarter']: float(r['ded_1000_plus']) for r in rd(D / 'ccc_deductible_share_quarterly.csv')}
print("\n== CCC $1,000+ deductible share (pp change YoY) vs insurance CPI YoY lagged k, 2022Q1–2025Q4")
dq = [q for q in sorted(ded) if qshift(q, -4) in ded]
for k in range(0, 7):
    xs = [ins[qshift(q, -k)] for q in dq if qshift(q, -k) in ins]; ys = [ded[q] - ded[qshift(q, -4)] for q in dq if qshift(q, -k) in ins]
    c = np.corrcoef(xs, ys)[0, 1]; print(f"   lag {k}: corr {c:+.2f} (n={len(xs)})")
with open(D / 'claims_term_drivers.csv', 'w', newline='') as f:
    f.write("# E2 (scripts/experiments/e2_affordability_claims.py): Progressive personal-auto accident frequency YoY (10-Q MD&A), VMT YoY (FRED), motor-vehicle insurance CPI YoY (BLS SETE) by quarter. MEASURED inputs.\n")
    w = csv.writer(f); w.writerow(['quarter', 'pgr_freq_yoy', 'pgr_collision_freq_yoy', 'pgr_severity_yoy', 'vmt_yoy', 'ins_cpi_yoy'])
    for q in sorted(set(freq) | set(ins)):
        if q >= '2014Q1': w.writerow([q, freq.get(q, ''), coll.get(q, ''), sev.get(q, ''), round(vmt[q], 2) if q in vmt else '', round(ins[q], 2) if q in ins else ''])
print("\nwrote claims_term_drivers.csv")
