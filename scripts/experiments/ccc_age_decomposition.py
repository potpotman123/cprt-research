#!/usr/bin/env python3
"""Decompose the 2020->2025 rise in CCC total-loss frequency into (a) claims-age MIX (fleet ageing) and (b) WITHIN-AGE
propensity (the spread cycle, technology, filing behaviour), using CCC's own bucket data rather than the fitted roll.

Inputs (both from Crash Course 2026 chart images, read 2026-09-26):
  P_t(b)  = total-loss share of claims by age bucket b, year t          data/csv/ccc_tl_share_by_age_2020_2025.csv
  T_t(b)  = share of total-loss valuations by age bucket b, year t      data/csv/ccc_tl_valuation_share_by_age_2020_2025.csv
Claims share by bucket falls out: w_t(b) ∝ T_t(b) / P_t(b)   (total losses in b = claims in b × P; so claims in b = TL in b / P).
TLF_t = Σ_b w_t(b) P_t(b) — check against the chart's own total.
Counterfactuals: mix effect = TLF(w_2025, P_2020) − TLF(w_2020, P_2020); propensity effect = TLF(w_2020, P_2025) − TLF(w_2020, P_2020);
interaction = remainder. Also reported year by year (chained). MEASURED given CCC's bucket data; no fitted curve involved.
Output: data/csv/ccc_tlf_mix_vs_propensity.csv
"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent; D = ROOT / 'data/csv'
def rd(f): return [r for r in csv.DictReader(l for l in open(D / f) if not l.startswith('#'))]
P = {r['age_bucket']: {y: float(r[y]) / 100 for y in r if y != 'age_bucket'} for r in rd('ccc_tl_share_by_age_2020_2025.csv')}
T = {r['age_bucket']: {y: float(r[y]) / 100 for y in r if y != 'age_bucket'} for r in rd('ccc_tl_valuation_share_by_age_2020_2025.csv')}
years = ['cy2020', 'cy2021', 'cy2022', 'cy2023', 'cy2024', 'cy2025']; B = [b for b in P if b != 'total']
W = {}
for y in years:
    raw = {b: T[b][y] / P[b][y] for b in B}; s = sum(raw.values()); W[y] = {b: v / s for b, v in raw.items()}
tlf = lambda w, p: sum(w[b] * p[b] for b in B)
print("year   TLF(chart total)  TLF(Σ w·P)   claims share by bucket: " + " ".join(f"{b:>7s}" for b in B))
for y in years:
    print(f"{y[2:]}   {P['total'][y]*100:6.1f}           {tlf(W[y], {b: P[b][y] for b in B})*100:6.1f}      " + " ".join(f"{W[y][b]*100:7.1f}" for b in B))
rows = []
def decomp(y0, y1):
    w0, w1 = W[y0], W[y1]; p0 = {b: P[b][y0] for b in B}; p1 = {b: P[b][y1] for b in B}
    base = tlf(w0, p0); mix = tlf(w1, p0) - base; prop = tlf(w0, p1) - base; tot = tlf(w1, p1) - base
    return base, mix, prop, tot - mix - prop, tot
print("\nDecomposition (pp of TLF):            base    mix(ageing)  within-age   interaction   total")
for y0, y1 in [('cy2020', 'cy2025'), ('cy2022', 'cy2025'), ('cy2020', 'cy2022')] + [(years[i], years[i + 1]) for i in range(5)]:
    base, mix, prop, inter, tot = decomp(y0, y1)
    print(f"  {y0[2:]}→{y1[2:]}                          {base*100:5.1f}     {mix*100:+6.2f}       {prop*100:+6.2f}      {inter*100:+6.2f}      {tot*100:+6.2f}")
    rows.append(dict(from_year=y0[2:], to_year=y1[2:], tlf_base_pct=round(base * 100, 2), mix_effect_pp=round(mix * 100, 2), within_age_effect_pp=round(prop * 100, 2), interaction_pp=round(inter * 100, 2), total_change_pp=round(tot * 100, 2)))
with open(D / 'ccc_tlf_mix_vs_propensity.csv', 'w', newline='') as f:
    f.write("# scripts/experiments/ccc_age_decomposition.py: CCC all-loss TLF change decomposed into claims-age mix (fleet ageing) vs within-bucket propensity, from Crash Course 2026 Figures 18 and 19 (claims share by bucket = TL share / P). MEASURED from CCC bucket data; no fitted curves. Six age buckets.\n")
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
# claims-share and P by bucket, for the workbook
with open(D / 'ccc_claims_share_by_age_2020_2025.csv', 'w', newline='') as f:
    f.write("# Derived: claims share by age bucket = (TL valuation share / TL share of claims) normalised, from CCC Crash Course 2026 Figures 18 and 19 (scripts/experiments/ccc_age_decomposition.py). MEASURED (derived from two VERIFIED charts).\n")
    w = csv.writer(f); w.writerow(['age_bucket'] + years)
    for b in B: w.writerow([b] + [round(W[y][b] * 100, 2) for y in years])
print("\nwrote ccc_tlf_mix_vs_propensity.csv, ccc_claims_share_by_age_2020_2025.csv")
