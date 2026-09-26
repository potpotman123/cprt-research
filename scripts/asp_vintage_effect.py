#!/usr/bin/env python3
"""Vintage effect on Copart's realised price: how much the sticker price of the total-loss pool rises each year purely
because the typical totaled car is one model year newer (findings Addendum 20, driver (a) of the ASP intercept).

sticker index of the TL pool in year t  =  Σ_MY w_t(MY) · NV(MY)  /  Σ_MY w_t(MY)
  w_t(MY)  = total losses contributed by model year MY in year t, from the fleet roll (sales × S × R × P, both bodies)
  NV(MY)   = BLS CPI new vehicles (CUUR0000SETA01), mean of the annual averages for years MY−1 and MY
             (model years launch mid-way through the prior calendar year); MY > last data year held flat (ASSUMED)
vintage effect_t (pp) = (index_t / index_{t−1} − 1) × 100

Used-car CPI is quality-adjusted: it prices a constant-quality car. It does not capture that a 10-year-old car in 2027
is a MY2017 vehicle with a MY2017 sticker rather than a MY2013 one. This series is that missing term.
Input: raw/bls/cu.data.14.USTransportation (download.bls.gov flat file; PROVENANCE §5). Output: data/csv/asp_vintage_effect.csv
"""
import csv, math, pathlib, re, statistics as st, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent; D = ROOT / 'data/csv'; BLS = ROOT / 'raw/bls/cu.data.14.USTransportation'
if not BLS.exists(): sys.exit("BLS flat file not on disk: raw/bls/cu.data.14.USTransportation")
def rd(f): return [r for r in csv.DictReader(l for l in open(D / f) if not l.startswith('#'))]
# ---- BLS annual averages (M13 where present, else mean of available months)
want = {'CUUR0000SETA01': 'new_vehicles', 'CUUR0000SS45011': 'new_cars', 'CUUR0000SS45021': 'new_trucks', 'CUUR0000SETA02': 'used_cars_trucks'}
months, annual = {k: {} for k in want}, {k: {} for k in want}
for line in open(BLS, encoding='utf-8', errors='ignore'):
    p = [x.strip() for x in line.split('\t')]
    if len(p) < 4 or p[0] not in want: continue
    sid, yr, per, val = p[0], int(p[1]), p[2], p[3]
    if val in ('', '-'): continue
    if per == 'M13': annual[sid][yr] = float(val)
    elif per.startswith('M'): months[sid].setdefault(yr, []).append(float(val))
for sid in want:
    for yr, v in months[sid].items(): annual[sid].setdefault(yr, st.mean(v))
NV = annual['CUUR0000SETA01']; last = max(NV); print(f"new-vehicle CPI: {min(NV)}–{last} ({len(NV)} years; {last} from {len(months['CUUR0000SETA01'].get(last, []))} months)")
for sid, nm in want.items():
    a = annual[sid]
    if a: print(f"  {nm:16s} {min(a)}–{max(a)}  2013→2019 {(a.get(2019,0)/a.get(2013,1)-1)*100:+.1f}%   2019→{max(a)} {(a[max(a)]/a.get(2019,1)-1)*100:+.1f}%")
nv = lambda my: (NV.get(min(my, last) - 1, NV[min(my, last)]) + NV[min(my, last)]) / 2 if min(my, last) in NV else None
# ---- fleet roll weights (same construction as scripts/age_curves.py; sales held at 2025 after 2025)
S = {int(r['age']): (float(r['survival_cars']), float(r['survival_light_trucks'])) for r in rd('ornl_tedb40_survival_by_age.csv')}
SL = {int(r['year']): (float(r['cars_k']), float(r['light_trucks_k'])) for r in rd('light_vehicle_sales_by_year.csv')}
for y in range(2026, 2031): SL.setdefault(y, SL[2025])
hdr = " ".join(l for l in open(D / 'age_curves.csv') if l.startswith('#'))
lam = float(re.search(r"exp\(-([\d.]+)\*max", hdr).group(1)); pm = re.search(r"P\(a\) = ([\d.]+) \+ \(([\d.]+)-[\d.]+\)/\(1\+exp\(-\(a-([\d.]+)\)/([\d.]+)\)\)", hdr); pmin, pmax, pc, ps = map(float, pm.groups())
Rf = lambda a: (0.5 if a == 0 else 1) * math.exp(-lam * max(a - 6, 0)); Pf = lambda a: pmin + (pmax - pmin) / (1 + math.exp(-(a - pc) / ps))
def Sk(i, a, k):
    x = a / k
    if x >= 31: return 0.0
    j = int(x); f = x - j; return S[j][i] + f * (S[min(j + 1, 31)][i] - S[j][i])
kmult = lambda t: 1.0 if t <= 2013 else (1.194 if t >= 2024 else 1 + 0.194 * (t - 2013) / 11)
rows = []; prev = {}
for t in range(2015, 2031):
    kc, kl = 1.064 * kmult(t), 0.921 * kmult(t); wt = wc = it = ic = 0.0; myt = 0.0; wlt = 0.0
    for a in range(0, 46):
        my = t - a
        if my not in SL or nv(my) is None: continue
        fc_, fl_ = SL[my][0] * Sk(0, a, kc), SL[my][1] * Sk(1, a, kl); f = fc_ + fl_; cl = f * Rf(a); tl = cl * Pf(a)
        wt += tl; it += tl * nv(my); wc += cl; ic += cl * nv(my); myt += tl * my; wlt += fl_ * Rf(a) * Pf(a)
    idx_tl, idx_cl = it / wt, ic / wc
    r = dict(year=t, tl_sticker_index=round(idx_tl, 2), claims_sticker_index=round(idx_cl, 2), mean_model_year_tl=round(myt / wt, 2), lt_share_tl=round(wlt / wt, 4),
             vintage_effect_tl_pp=(round((idx_tl / prev['tl'] - 1) * 100, 2) if prev else None), vintage_effect_claims_pp=(round((idx_cl / prev['cl'] - 1) * 100, 2) if prev else None))
    rows.append(r); prev = dict(tl=idx_tl, cl=idx_cl)
print(f"\n{'year':5s} {'TL sticker idx':>14s} {'vintage effect pp':>18s} {'mean MY of TL':>14s}")
for r in rows[1:]: print(f"{r['year']:5d} {r['tl_sticker_index']:14.1f} {r['vintage_effect_tl_pp']:18.2f} {r['mean_model_year_tl']:14.1f}")
v = [r['vintage_effect_tl_pp'] for r in rows if r['year'] in range(2022, 2027)]
print(f"\nmean vintage effect 2022–2026: {st.mean(v):+.2f} pp/yr  vs ASP intercept ~3.3 pp/yr  -> explains {st.mean(v)/3.3:.0%} of it (direction MEASURED; level assumes model-year sticker ≈ new-vehicle CPI of the vintage)")
v2 = [r['vintage_effect_tl_pp'] for r in rows if r['year'] in range(2027, 2031)]
print(f"mean vintage effect 2027–2030: {st.mean(v2):+.2f} pp/yr (MY2016–2020 vintages entering the pool; the 2021–23 new-vehicle inflation reaches the 10-year-old pool only in the early 2030s)")
with open(D / 'asp_vintage_effect.csv', 'w', newline='') as fh:
    fh.write("# Vintage effect on the total-loss pool's sticker price (scripts/asp_vintage_effect.py). Weights: fleet roll (sales x EPA survival x fitted R,P), both bodies; NV(MY) = BLS CPI new vehicles CUUR0000SETA01 annual avg, mean of years MY-1 and MY; model years past the last BLS year held flat (ASSUMED). findings.md Addendum 20/21.\n")
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("-> data/csv/asp_vintage_effect.csv")
