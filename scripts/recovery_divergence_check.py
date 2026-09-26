#!/usr/bin/env python3
"""Cheap check of the 'salvage-recovery divergence' hypothesis (external research note, 2026-09-25).

Hypothesis: when expected salvage recovery rises faster than vehicle values, the repair-vs-total decision tips more
marginal cars into total losses, so recovery/value divergence should ADD to total-loss frequency beyond the repair-cost
vs used-car-value spread we already use.

Test, all from data on disk:
  divergence(q) = Copart US insurance ASP YoY (transcripts) − used-car CPI YoY (BLS SA, fiscal-quarter average),
                  mapped to the calendar quarter sharing two of three months.
  ΔTLF(q+1) regressed on spread(q) alone and with divergence(q) (raw, and orthogonalised on CPI to remove the shared
  −CPI component). n = 11 overlapping quarters — a direction check, not a coefficient to pitch.

Result (2026-09-25): divergence averages +4.2pp/yr and is persistent, but adds nothing to the spread regression on this
sample; its marginal coefficient is NEGATIVE (wrong sign) and the two regressors are 0.85 correlated. Contemporaneous
correlation with ΔTLF is +0.64, which is what selection/mix would produce (more totals -> higher average salvage price),
so it cannot identify the mechanism. Findings.md Addendum 18. Output: data/csv/recovery_divergence_quarterly.csv
"""
import csv, math, pathlib, statistics as st
ROOT = pathlib.Path(__file__).resolve().parent.parent; D = ROOT / 'data/csv'
def rd(f): return [r for r in csv.DictReader(l for l in open(D / f) if not l.startswith('#'))]
ru = {r['fiscal_q']: r for r in rd('reported_units.csv')}
ru['FY2026 Q4'] = {'us_ins_asp_yoy': '3.7', 'global_asp_yoy': '3.5'}                 # FQ4 FY26 call 2026-09-10; not yet in the CSV
cpi = {r['date']: float(r['CUSR0000SETA02']) for r in rd('cprt_cpi_three_series.csv') if r['CUSR0000SETA02']}
tlf = {r['quarter']: float(r['all_loss_categories_pct']) for r in rd('ccc_tlf_quarterly.csv')}
tlf['2026Q2'] = 23.3                                                                   # mgmt-cited CCC figure, 2026-09-10 call
spread = {r['quarter']: float(r['spread_pp']) for r in rd('totaling_spread_quarterly.csv') if r['months'] == '3'}
def months(fy, q): return {1: [f"{fy-1}-08", f"{fy-1}-09", f"{fy-1}-10"], 2: [f"{fy-1}-11", f"{fy-1}-12", f"{fy}-01"], 3: [f"{fy}-02", f"{fy}-03", f"{fy}-04"], 4: [f"{fy}-05", f"{fy}-06", f"{fy}-07"]}[q]
def cpi_yoy(fy, q):
    ms = months(fy, q); cur = [cpi.get(m) for m in ms]; pri = [cpi.get(f"{int(m[:4])-1}{m[4:]}") for m in ms]
    return None if None in cur or None in pri else (sum(cur) / sum(pri) - 1) * 100
def cal_q(fy, q): return {1: f"{fy-1}Q3", 2: f"{fy-1}Q4", 3: f"{fy}Q1", 4: f"{fy}Q2"}[q]
def shift(q, k):
    y, n = int(q[:4]), int(q[5]) + k
    while n < 1: n += 4; y -= 1
    while n > 4: n -= 4; y += 1
    return f"{y}Q{n}"
def dtlf(q):
    p = f"{int(q[:4])-1}{q[4:]}"; return tlf[q] - tlf[p] if q in tlf and p in tlf else None
rows = []
for fq, r in sorted(ru.items()):
    fy, q = int(fq[2:6]), int(fq[-1]); c = cpi_yoy(fy, q)
    if c is None or not r.get('us_ins_asp_yoy'): continue
    cq = cal_q(fy, q); asp = float(r['us_ins_asp_yoy'])
    rows.append(dict(fiscal_q=fq, calendar_q=cq, used_car_cpi_yoy=round(c, 2), us_ins_asp_yoy=asp, divergence_pp=round(asp - c, 2),
                     dtlf_same_q=dtlf(cq), dtlf_next_q=dtlf(shift(cq, 1)), spread_pp=spread.get(cq)))
def ols(X, y):
    n, k = len(y), len(X[0]); M = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] + [sum(X[i][a] * y[i] for i in range(n))] for a in range(k)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(k):
            if r != c: f = M[r][c] / M[c][c]; M[r] = [M[r][j] - f * M[c][j] for j in range(k + 1)]
    beta = [M[i][k] / M[i][i] for i in range(k)]
    yhat = [sum(b * x for b, x in zip(beta, X[i])) for i in range(n)]; sse = sum((a - b) ** 2 for a, b in zip(y, yhat)); sst = sum((v - st.mean(y)) ** 2 for v in y)
    return beta, 1 - sse / sst
def corr(a, b):
    ma, mb = st.mean(a), st.mean(b); return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
divs = [r['divergence_pp'] for r in rows]
print(f"divergence (ASP − used-car CPI): mean {st.mean(divs):+.2f}pp/yr, sd {st.pstdev(divs):.2f}, n={len(divs)}; halves {st.mean(divs[:len(divs)//2]):+.2f} / {st.mean(divs[len(divs)//2:]):+.2f}")
S = [r for r in rows if r['dtlf_next_q'] is not None and r['spread_pp'] is not None]
y = [r['dtlf_next_q'] for r in S]; sp = [r['spread_pp'] for r in S]; dv = [r['divergence_pp'] for r in S]
b0, _ = ols([[1, r['used_car_cpi_yoy']] for r in rows], [r['us_ins_asp_yoy'] for r in rows]); od = [r['us_ins_asp_yoy'] - (b0[0] + b0[1] * r['used_car_cpi_yoy']) for r in S]
print(f"ASP on CPI: {b0[0]:.2f} + {b0[1]:.3f}×CPI (n={len(rows)}); overlap sample n={len(S)} ({S[0]['calendar_q']}..{S[-1]['calendar_q']}); corr(div,spread)={corr(dv,sp):+.2f}")
for lab, X in (("spread only", [[1, s] for s in sp]), ("spread + divergence", [[1, s, d] for s, d in zip(sp, dv)]), ("spread + orthogonal divergence", [[1, s, d] for s, d in zip(sp, od)])):
    beta, r2 = ols(X, y); print(f"  ΔTLF(t+1) ~ {lab:32s} a={beta[0]:+.3f} b_spread={beta[1]:+.4f}" + (f" c_div={beta[2]:+.4f}" if len(beta) > 2 else "") + f" R²={r2:.3f}")
print(f"  corr(ΔTLF(t+1), div(t))={corr(y, dv):+.2f}; corr(ΔTLF(t), div(t))={corr([r['dtlf_same_q'] for r in S if r['dtlf_same_q'] is not None], [r['divergence_pp'] for r in S if r['dtlf_same_q'] is not None]):+.2f} (contemporaneous — selection/mix, not identification)")
with open(D / 'recovery_divergence_quarterly.csv', 'w', newline='') as fh:
    fh.write("# Salvage-recovery divergence check (scripts/recovery_divergence_check.py, 2026-09-25): Copart US insurance ASP YoY (transcripts; FY26Q4 from the 2026-09-10 call) minus used-car CPI YoY (BLS CUSR0000SETA02, fiscal-quarter avg), by fiscal quarter mapped to the calendar quarter sharing 2 of 3 months; CCC all-loss TLF changes; totaling spread. Result: divergence persistent (~+4pp/yr) but adds nothing to the spread regression on n=11 (marginal coefficient negative). findings.md Addendum 18.\n")
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("-> data/csv/recovery_divergence_quarterly.csv")
