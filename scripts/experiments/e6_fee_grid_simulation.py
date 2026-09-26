#!/usr/bin/env python3
"""E6 — what the buyer-fee grid implies for revenue-per-unit elasticity to price (mechanism C in MODEL_BLUEPRINT.md).
Total buyer-side fee(p) = band fee(p) + gate + environmental + live virtual-bid fee(p). Apply to a lognormal price distribution
(median m, sigma s — ASSUMED; Copart discloses no ASP level or distribution), shift the distribution by ±10% and read off
d ln(mean fee) / d ln(price). Also prints the fee as % of price by price. Grid: data/csv/copart_fee_grid_2026-09.csv."""
import csv, math, pathlib, sys
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
rows = [r for r in csv.DictReader(l for l in open(ROOT / 'data/csv/copart_fee_grid_2026-09.csv') if not l.startswith('#'))]
def grid(page, title, vclass, ftype, pm):
    g = [(float(r['band_low_usd']), float(r['band_high_usd']) if r['band_high_usd'] else float('inf'), float(r['fee_usd']) if r['fee_usd'] else None, float(r['fee_pct']) if r['fee_pct'] else None)
         for r in rows if r['page'] == page and r['title_group'] == title and r['vehicle_class'] == vclass and r['fee_type'] == ftype and r['payment_method'] == pm]
    return sorted(g)
def fee_of(g, p):
    for lo, hi, usd, pct in g:
        if lo <= p <= hi: return usd if usd is not None else p * pct / 100
    return g[-1][2] if g[-1][2] is not None else p * g[-1][3] / 100
def total_fee(page, title, p, gate):
    return fee_of(grid(page, title, 'standard', 'buyer_fee', 'secured'), p) + gate + 15 + fee_of(grid(page, title, 'standard', 'virtual_bid_live_bid', 'any'), p)
print("Buyer-side fee (band + gate + $15 env + live virtual bid) as % of price — Standard non-clean / Preferred non-clean / Standard clean:")
for p in [300, 500, 1000, 2000, 3000, 5000, 8000, 12000, 15000, 20000, 30000]:
    a, b, c = total_fee('non-licensed', 'non-clean', p, 95), total_fee('licensed-high-volume', 'non-clean', p, 95), total_fee('non-licensed', 'clean', p, 79)
    print(f"  ${p:>6,}: {a/p*100:5.1f}%  {b/p*100:5.1f}%  {c/p*100:5.1f}%   (${a:,.0f} / ${b:,.0f} / ${c:,.0f})")
rng = np.random.default_rng(7)
print("\nElasticity of mean buyer fee per unit to a uniform price shift, lognormal price distribution (ASSUMED median, sigma):")
print("  median  sigma   mean fee(Std non-clean)  elasticity Std  elasticity Preferred  elasticity Std clean")
for m in (2500, 3500, 5000, 7000):
    for s in (0.8, 1.0):
        base = np.exp(np.log(m) + s * rng.standard_normal(200000)); base = base[base < 60000]
        def meanfee(page, title, gate, k): return np.mean([total_fee(page, title, p, gate) for p in base[:20000] * k])
        out = []
        for page, title, gate in (('non-licensed', 'non-clean', 95), ('licensed-high-volume', 'non-clean', 95), ('non-licensed', 'clean', 79)):
            up, dn = meanfee(page, title, gate, 1.1), meanfee(page, title, gate, 0.9); out.append((meanfee(page, title, gate, 1.0), (math.log(up) - math.log(dn)) / (math.log(1.1) - math.log(0.9))))
        print(f"  {m:>6}  {s:.1f}    ${out[0][0]:,.0f}                {out[0][1]:.2f}            {out[1][1]:.2f}                {out[2][1]:.2f}")
