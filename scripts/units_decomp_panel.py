#!/usr/bin/env python3
"""Six-quarter units decomposition panel (built 2026-09-11).

    Copart US insurance units  =  Claims  x  Total-loss rate  x  Copart share
    YoY:  d(pool)% = (1 + d claims)(1 + d TLF) - 1 ;   RESIDUAL = Copart - pool   (= the share term)

Calendar 2025Q1..2026Q2  <->  Copart FY25Q3..FY26Q4 (2-of-3-month overlap mapping).

CLAIMS DENOMINATOR - the choice that matters. Three candidates, one anchor:
  * ISS Fast Track COLLISION claim counts (CollisionWeek headlines): -11/-10/-11% through 2025. Collision-only.
  * CCC all-coverage claim volume: -7.7% CY2025 (annual only; applied to each 2025 quarter).
  * CCC non-comprehensive claim volume: -5.7% CY2025.
  ANCHOR: CCC reports total-loss valuations DIRECTLY: -2.9% CY2025. That IS the pool, no decomposition needed.
  Copart US insurance ex-CAT, month-weighted to calendar 2025 = -3.48%  ->  anchor residual -0.58pp.
  Only the CCC all-coverage denominator reproduces that (-0.2pp four-quarter avg); collision-only gives +3.7
  (overstates the pool decline because PD-liability claims lack the deductible-avoidance effect; CCC: "liability
  claims are not following the same trajectory"), non-comp gives -2.3. => USE CCC ALL-COVERAGE.

TLF: CCC All Loss Categories quarterly, actual where published (through 2025Q3), management-cited for 2026Q2
(23.3 vs 22.4, 2026-09-10 call), model dTLF = 0.599 + 0.0815*spread(t-1) for 2025Q4 and 2026Q1.

Copart: hand-transcribed transcript series (reported_series.py). Ex-CAT where disclosed. FY26Q4 also has
assignments (-5.0%) and management's ex-one-account assignments (+2.3%).

PROVENANCE CAVEATS TO PRINT WITH ANY CHART: Copart units are transcript-provenance (no filing discloses them);
CCC is a market-share-weighted sample, not a census; CCC's quarterly series may be discontinued (last public
2025Q3); the 2026 claims term is a range (Fast Track "smallest decline since 1Q24"; mgmt frequency -3.4%).

INTERPRETING THE RESIDUAL (corrected 2026-09-11, findings.md Addendum 15a): a sell-side by-carrier table shows
the lost account (Progressive) fell from ~10-13k/month to ~600/month between APRIL and JULY 2026. So the
~-3pp residual in FY26Q1/FY26Q3 is the CARRIER-MIX drag (underweight the one fast-growing carrier), and the
further step to -6.8pp in FY26Q4 is the account itself. The comp fully laps in FY27Q4 (May-Jul 2027), not
earlier; the drag persists at near-full weight through FY27Q3.
"""
import csv, statistics as st, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

Q  = ['2025Q1','2025Q2','2025Q3','2025Q4','2026Q1','2026Q2']
FQ = ['FY25Q3','FY25Q4','FY26Q1','FY26Q2','FY26Q3','FY26Q4']
cprt_excat = [-2.0, -2.1, -7.3, -4.8, -3.1, -7.5]
cprt_asrep = [-1.0, -2.1, -9.5, -10.7, -4.2, -7.5]
tlf_now  = [22.9, 22.4, 22.8, None, None, 23.3]
tlf_prev = [21.8, 21.5, 21.9, 24.1, 22.9, 22.4]
tlf_src  = ['CCC actual','CCC actual','CCC actual','model spread(3Q25)=+2.27','model spread(4Q25)=+3.56 (2/3 mo)','mgmt-cited CCC 2026-09-10']
spread_prev = {3: 2.27, 4: 3.56}
A, B = 0.599, 0.0815
den = {
  'fasttrack_collision': ([-12.0,-11.5,-10.5,-11.5,-3.5,-4.5], 'CollisionWeek headlines; 1Q25 bound (<-11); 2026 = range'),
  'ccc_all_coverage':    ([-7.7,-7.7,-7.7,-7.7,-3.5,-4.5],     'CCC Crash Course 2026: total claim volume -7.7% CY2025; 2026 = FT/mgmt range'),
  'ccc_non_comp':        ([-5.7,-5.7,-5.7,-5.7,-3.5,-4.5],     'CCC: ex-comprehensive -5.7% CY2025'),
}
claims_2026_range = {4: (-5.0, -2.0), 5: (-6.0, -3.4)}   # index -> (lo, hi)

pool = lambda c, tr: 100*((1+c/100)*(1+tr/100)-1)
tlf_rel = []
for i in range(6):
    now = tlf_now[i] if tlf_now[i] is not None else tlf_prev[i] + A + B*spread_prev[i]
    tlf_rel.append(100*(now/tlf_prev[i]-1))

print("SIX-QUARTER UNITS DECOMPOSITION — residual (Copart US ins exCAT − pool), pp")
print(f"{'cal Q':7s} {'FQ':7s} {'CPRT':>6s} {'TLF%':>6s} | " + " | ".join(f"{k:>22s}" for k in den))
res = {k: [] for k in den}
for i in range(6):
    cells = []
    for k, (v, _) in den.items():
        p = pool(v[i], tlf_rel[i]); r = cprt_excat[i]-p; res[k].append(r); cells.append(f"pool {p:+5.1f} res {r:+5.1f}")
    print(f"{Q[i]:7s} {FQ[i]:7s} {cprt_excat[i]:+6.1f} {tlf_rel[i]:+6.1f} | " + " | ".join(f"{c:>22s}" for c in cells))
print()
for k in den:
    r = res[k]
    print(f"  {k:20s} 2025H1 {st.mean(r[:2]):+5.1f} | 2025H2 {st.mean(r[2:4]):+5.1f} | 2026H1 {st.mean(r[4:]):+5.1f} | 2025 avg {st.mean(r[:4]):+5.1f} | step H1'25→H1'26 {st.mean(r[4:])-st.mean(r[:2]):+5.1f}pp")
w = {'FY25Q2': (1, 2.0), 'FY25Q3': (3, -2.0), 'FY25Q4': (3, -2.1), 'FY26Q1': (3, -7.3), 'FY26Q2': (2, -4.8)}
cp25 = sum(m*v for m, v in w.values())/12
print(f"\n  ANCHOR CY2025: CCC total-loss valuations -2.9% vs Copart exCAT month-weighted {cp25:+.2f}% -> residual {cp25+2.9:+.2f}pp  (CCC all-coverage 2025 avg {st.mean(res['ccc_all_coverage'][:4]):+.1f} reconciles; others do not)")
p26q2 = pool(den['ccc_all_coverage'][0][5], tlf_rel[5])
print(f"  FY26Q4 with ASSIGNMENTS -5.0 -> residual {-5.0-p26q2:+.1f}pp;  ex-one-account +2.3 -> {2.3-p26q2:+.1f}pp;  mgmt's implied account = -7.3pp vs panel step {st.mean(res['ccc_all_coverage'][4:])-st.mean(res['ccc_all_coverage'][:2]):+.1f}pp")
print("\n  LAG-1 sensitivity (units lag claims ~1 quarter via title wait), CCC-all denominator:")
pa = [pool(den['ccc_all_coverage'][0][i], tlf_rel[i]) for i in range(6)]
for i in range(1, 6): print(f"    {FQ[i]} {cprt_excat[i]:+5.1f} vs pool({Q[i-1]}) {pa[i-1]:+5.1f} -> {cprt_excat[i]-pa[i-1]:+5.1f}pp")

with open(ROOT/'data/csv/units_decomp_panel_v2.csv', 'w', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(['calendar_q','cprt_fq','cprt_us_ins_asrep','cprt_us_ins_excat','tlf_yoy_rel_pct','tlf_source']
                + [f'claims__{k}' for k in den] + [f'pool__{k}' for k in den] + [f'residual__{k}' for k in den] + ['claims_2026_lo','claims_2026_hi'])
    for i in range(6):
        lo, hi = claims_2026_range.get(i, ('', ''))
        wr.writerow([Q[i], FQ[i], cprt_asrep[i], cprt_excat[i], round(tlf_rel[i], 2), tlf_src[i]]
                    + [den[k][0][i] for k in den] + [round(pool(den[k][0][i], tlf_rel[i]), 2) for k in den] + [round(res[k][i], 2) for k in den] + [lo, hi])
print("\n-> data/csv/units_decomp_panel_v2.csv")
