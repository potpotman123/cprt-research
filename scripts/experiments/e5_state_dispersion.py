#!/usr/bin/env python3
"""E5 step 1 — the screen: is there cross-state STRUCTURE in how Copart's listed inventory moved 2022-2026?
(2026-09-26, second Fable session.)  If title-processing speed (electronic salvage titles) changes inventory velocity, it
does so state by state on different dates, so states should diverge from the national series in a structured way (large,
persistent, regionally clustered, not explained by CAT events).  If the state shares just wobble, E5 stops here (kill rule).

Input: data/csv/state_panel.csv — listed lots by state per capture (archive months 2022-09 → 2025-09 from lot.xml, live
Sep-2026 from lot_snapshots), 51 states, 16 captures.  Listings, not yard inventory; captures can be page-out-of-sync
(ARCHITECTURE.md), which is why SHARES of the national total are used, never levels.
Method: share_s(m) = lots_s(m) / Σ_s lots_s(m).  Annual mean share per state; change 2023→2026 in relative terms
(share_2026/share_2023 − 1).  Noise benchmark: the within-year dispersion of a state's share across the captures of one
year (2023: 5 captures; 2024: 5) — if between-year moves are not larger than within-year wobble there is nothing to explain.
Structure tests: (a) size dependence (small states noisier?), (b) regional means, (c) CAT-state flags (Helene/Milton
Sep-Oct 2024: FL GA NC SC TN VA; Texas/Florida hurricane seasons), (d) persistence: corr(change 23→24, change 24→26).
Output: data/csv/state_share_dispersion.csv.  No network.
"""
import csv, collections, math, pathlib, statistics as st
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent; D = ROOT / 'data/csv'
rows = [r for r in csv.DictReader(l for l in open(D / 'state_panel.csv') if not l.startswith('#'))]
lots = collections.defaultdict(dict)
for r in rows: lots[r['month']][r['state']] = int(r['lots'])
months = sorted(lots); states = sorted({r['state'] for r in rows})
tot = {m: sum(lots[m].values()) for m in months}
share = {m: {s: lots[m].get(s, 0) / tot[m] for s in states} for m in months}
byyear = collections.defaultdict(list)
for m in months: byyear[m[:4]].append(m)
print("captures per year: " + ", ".join(f"{y}: {len(v)}" for y, v in sorted(byyear.items())))
ymean = {y: {s: st.mean(share[m][s] for m in ms) for s in states} for y, ms in byyear.items()}
# within-year wobble (noise benchmark): CV of a state's share across the captures of a year, 2023 and 2024 (5 captures each)
def cv(vals): return st.pstdev(vals) / st.mean(vals) if st.mean(vals) > 0 else float('nan')
wobble = {s: st.mean([cv([share[m][s] for m in byyear['2023']]), cv([share[m][s] for m in byyear['2024']])]) for s in states}
REGION = {'Northeast': 'CT ME MA NH RI VT NJ NY PA'.split(), 'Midwest': 'IL IN MI OH WI IA KS MN MO NE ND SD'.split(),
          'South': 'DE FL GA MD NC SC VA DC WV AL KY MS TN AR LA OK TX'.split(), 'West': 'AZ CO ID MT NV NM UT WY AK CA HI OR WA'.split()}
reg_of = {s: r for r, ss in REGION.items() for s in ss}
CAT24 = set('FL GA NC SC TN VA'.split())          # Helene (late Sep 2024) + Milton (Oct 2024) footprint; the 202410 capture sits inside it
out = []
for s in states:
    s23, s24, s25, s26 = ymean['2023'][s], ymean['2024'][s], ymean['2025'][s], ymean['2026'][s]
    if min(s23, s24) == 0: print(f"   {s}: absent in 2023 or 2024 captures — skipped"); continue
    out.append(dict(state=s, region=reg_of.get(s, ''), share_2023_pct=round(s23 * 100, 3), share_2024_pct=round(s24 * 100, 3), share_2025_pct=round(s25 * 100, 3), share_2026_pct=round(s26 * 100, 3),
                    rel_change_23_24_pct=round((s24 / s23 - 1) * 100, 1), rel_change_24_26_pct=round((s26 / s24 - 1) * 100, 1), rel_change_23_26_pct=round((s26 / s23 - 1) * 100, 1),
                    within_year_cv_pct=round(wobble[s] * 100, 1), cat_2024=int(s in CAT24), lots_sep2026=lots['202609'].get(s, 0)))
out.sort(key=lambda r: r['rel_change_23_26_pct'])
big = [r for r in out if r['share_2023_pct'] >= 0.5]        # states ≥0.5% of the national pool (~ >800 lots): 30-ish states carry the signal
print(f"\nstates with ≥0.5% share in 2023: {len(big)} of {len(out)} (they hold {sum(r['share_2023_pct'] for r in big):.1f}% of listings)")
chg = [r['rel_change_23_26_pct'] for r in big]; wob = [r['within_year_cv_pct'] for r in big]
print(f"relative share change 2023→2026, ≥0.5% states: mean {st.mean(chg):+.1f}%, stdev {st.pstdev(chg):.1f}%, IQR {sorted(chg)[len(chg)//4]:+.1f} … {sorted(chg)[3*len(chg)//4]:+.1f}")
print(f"within-year wobble of the same states (CV of share across captures in a year): mean {st.mean(wob):.1f}%, max {max(wob):.1f}%")
print(f"→ ratio between-year stdev / within-year wobble = {st.pstdev(chg)/st.mean(wob):.1f}×  (≈1 = noise; ≫1 = something moved)")
def corr(x, y):
    mx, my = st.mean(x), st.mean(y); sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxy / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
print(f"persistence: corr(change 23→24, change 24→26) over ≥0.5% states = {corr([r['rel_change_23_24_pct'] for r in big], [r['rel_change_24_26_pct'] for r in big]):+.2f}  (a titling change would persist; a CAT or a capture artefact reverses)")
print(f"size dependence: corr(|change 23→26|, log share) = {corr([abs(r['rel_change_23_26_pct']) for r in big], [math.log(r['share_2023_pct']) for r in big]):+.2f}")
print("\nregional means of the relative share change (≥0.5% states, unweighted): " + "; ".join(f"{reg}: {st.mean([r['rel_change_23_26_pct'] for r in big if r['region'] == reg]):+.1f}% (n={sum(1 for r in big if r['region'] == reg)})" for reg in REGION))
print("CAT-2024 states vs others, change 23→24: " + f"{st.mean([r['rel_change_23_24_pct'] for r in big if r['cat_2024']]):+.1f}% vs {st.mean([r['rel_change_23_24_pct'] for r in big if not r['cat_2024']]):+.1f}%;  change 24→26: "
      + f"{st.mean([r['rel_change_24_26_pct'] for r in big if r['cat_2024']]):+.1f}% vs {st.mean([r['rel_change_24_26_pct'] for r in big if not r['cat_2024']]):+.1f}%")
print(f"\n{'state':5s} {'reg':9s} {'sh23%':>6s} {'sh26%':>6s} {'23→24':>7s} {'24→26':>7s} {'23→26':>7s} {'wobble':>7s} CAT24")
for r in out:
    if r['share_2023_pct'] >= 0.5:
        print(f"{r['state']:5s} {r['region']:9s} {r['share_2023_pct']:6.2f} {r['share_2026_pct']:6.2f} {r['rel_change_23_24_pct']:+7.1f} {r['rel_change_24_26_pct']:+7.1f} {r['rel_change_23_26_pct']:+7.1f} {r['within_year_cv_pct']:7.1f} {'*' if r['cat_2024'] else ''}")
# national context
print("\nnational listed total by capture (levels are capture-quality dependent; shown for context only):")
print("  " + ", ".join(f"{m}: {tot[m]:,}" for m in months))
with open(D / 'state_share_dispersion.csv', 'w', newline='') as fh:
    fh.write("# E5 step 1 (scripts/experiments/e5_state_dispersion.py, 2026-09-26): each state's share of Copart's listed lots (state_panel.csv), annual means of the captures (2023: 5, 2024: 5, 2025: 2, 2026: 1 live Sep), relative change, within-year wobble (CV of the share across a year's captures, mean of 2023 and 2024), Census region, Helene/Milton-2024 footprint flag. Listings, not yard inventory; shares only. MEASURED (screen).\n")
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print("\nwrote data/csv/state_share_dispersion.csv")
