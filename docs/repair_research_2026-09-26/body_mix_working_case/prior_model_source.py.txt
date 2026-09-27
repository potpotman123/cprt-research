#!/usr/bin/env python3
"""E1 steps 4-6 — body-specific totaling propensity P_car(age), P_LT(age), and what the light-truck cohort wave does to
total-loss frequency (supply) and Copart's realised price (ASP) through 2030.  (2026-09-26, second Fable session)

MECHANISM (stated before any number).  A claim is totaled when repair cost C exceeds a threshold share of the vehicle's
value V:  P = Pr[C > θ·V].  With C and V lognormal, P(a) = Φ((μ_C − ln θ − ln V(a)) / σ)  — a probit in ln V, so a probit in
age if value depreciates geometrically (ln V(a) = ln V0 − δ·a).  For two bodies at the same age, everything except
μ_C and V is common, so the body difference is ONE number, a shift in the probit index:
    Δz = ( ln(V_LT / V_car) − ln(C_LT / C_car) ) / σ_eff
  V_LT/V_car = 1.50 (E8: KBB ATP × iSeeCars retention, range 1.3-1.7; ASSUMED level, MEASURED direction)
  C_LT/C_car = 1.01 (E1 step 3: HLDI collision claim severity by class, 2022-24 MY, class-mean ratio; MEASURED)
  σ_eff      = dispersion of ln(C/V) within an age.  Two estimates: (i) from the HLDI 2024 claim-size distribution alone
               (median ≈ $4.5k, 25% ≥ $9k, 10% ≥ $18k → lognormal σ_C ≈ 1.05) — a LOWER bound, since value also varies within
               an age; (ii) from CCC's measured P by age bucket (Figure 19): the probit slope in age γ = δ/σ_eff, with the
               depreciation rate δ from iSeeCars (5-yr retention 58.2% → δ ≈ 0.108/yr; cross-section adds ~0.01 for
               older stickers).  (ii) is used as the base, (i) as the sensitivity.
Frequency: HLDI's adjusted collision claim frequency for light trucks is 0.67× cars (step 3).  That relative is adjusted for
driver age, gender, marital status, density, risk class etc., i.e. it isolates the vehicle; in the real fleet those driver
factors partly offset it.  So f = R_LT/R_car is run at 1.00 / 0.85 / 0.67, and the light-truck share of Copart's own listed
salvage pool (E1 step 1: 50.8% in 2024, 56.7% in Sep-2026) is used to say which f the data prefer.

IDENTIFICATION.  The single fitted P(a) reproduces CCC 2024 (docs/AGE_CURVES.md).  For each age the two body curves are
pinned by two conditions: (1) the claims-weighted mix  s(a)·P_LT(a) + (1−s(a))·P_car(a) = P(a)  with s(a) the LT share of
claims at age a from the fleet roll × f; (2) P_LT = Φ(z_car − Δz).  One unknown (z_car) per age, one equation → exact.
Nothing is refitted to the eight CCC statistics; the aggregate 2024 cross-section is unchanged by construction.

OUTPUTS  data/csv/age_curves_by_body.csv            P_car, P_LT by age for the base variant and the sensitivities
         data/csv/body_mix_tlf_asp_2015_2030.csv    TLF one-body vs two-body roll, LT share of claims / TL, ΔTLF and ΔASP
                                                    attributable to body mix by year, per variant
Inputs are all committed CSVs: light_vehicle_sales_by_year.csv, ornl_tedb40_survival_by_age.csv, age_curves.csv (header
carries the fitted R and P parameters and the k's), ccc_tl_share_by_age_2020_2025.csv, listed_body_share_monthly.csv.
No network.  Pure python.
"""
import csv, math, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent; D = ROOT / 'data/csv'
def rd(f): return [r for r in csv.DictReader(l for l in open(D / f) if not l.startswith('#'))]
Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
def Phi_inv(p, lo=-8.0, hi=8.0):
    for _ in range(80):
        m = (lo + hi) / 2
        if Phi(m) < p: lo = m
        else: hi = m
    return (lo + hi) / 2

# ------------------------------------------------------------------ fleet roll by body (same construction as asp_vintage_effect.py)
S = {int(r['age']): (float(r['survival_cars']), float(r['survival_light_trucks'])) for r in rd('ornl_tedb40_survival_by_age.csv')}
SL = {int(r['year']): (float(r['cars_k']), float(r['light_trucks_k'])) for r in rd('light_vehicle_sales_by_year.csv')}
LAST_SALES = max(SL)
for y in range(LAST_SALES + 1, 2031): SL[y] = SL[LAST_SALES]          # sales held flat after the last actual year (ASSUMED; 2025 mix = 83% LT)
hdr = " ".join(l for l in open(D / 'age_curves.csv') if l.startswith('#'))
lam = float(re.search(r"exp\(-([\d.]+)\*max", hdr).group(1))
pm = re.search(r"P\(a\) = ([\d.]+) \+ \(([\d.]+)-[\d.]+\)/\(1\+exp\(-\(a-([\d.]+)\)/([\d.]+)\)\)", hdr); pmin, pmax, pc, ps = map(float, pm.groups())
kc13, kl13 = (float(re.search(r"k_cars=([\d.]+)", hdr).group(1)) / 1.194, float(re.search(r"k_LT=([\d.]+)", hdr).group(1)) / 1.194)
Rf = lambda a: (0.5 if a == 0 else 1.0) * math.exp(-lam * max(a - 6, 0))
Pf = lambda a: pmin + (pmax - pmin) / (1 + math.exp(-(a - pc) / ps))
def Sk(i, a, k):
    x = a / k
    if x >= 31: return 0.0
    j = int(x); f = x - j; return S[j][i] + f * (S[min(j + 1, 31)][i] - S[j][i])
kmult = lambda t: 1.0 if t <= 2013 else (1.194 if t >= 2024 else 1 + 0.194 * (t - 2013) / 11)
AGES = range(0, 46)
def fleet(t):
    """{age: (cars_k, LT_k)} on the road at end of year t."""
    kc, kl = kc13 * kmult(t), kl13 * kmult(t); out = {}
    for a in AGES:
        my = t - a
        if my not in SL: continue
        out[a] = (SL[my][0] * Sk(0, a, kc), SL[my][1] * Sk(1, a, kl))
    return out
FL = {t: fleet(t) for t in range(2015, 2031)}

# ------------------------------------------------------------------ 1. σ_eff from CCC's measured P by bucket (probit slope in age)
CCC = {r['age_bucket']: {y: float(r[y]) / 100 for y in r if y != 'age_bucket'} for r in rd('ccc_tl_share_by_age_2020_2025.csv')}
BUCK = [('current_year_or_newer', 0, 0), ('1-3', 1, 3), ('4-6', 4, 6), ('7-9', 7, 9), ('10-12', 10, 12), ('13+', 13, 45)]
def bucket_mean_age(t):
    """claims-weighted mean age within each CCC bucket, from the roll (R common to both bodies)."""
    F = FL[t]; out = {}
    for b, lo, hi in BUCK:
        w = [(a, (F[a][0] + F[a][1]) * Rf(a)) for a in AGES if lo <= a <= hi and a in F]
        out[b] = sum(a * x for a, x in w) / sum(x for _, x in w)
    return out
def ols(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    b = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / sum((xi - mx) ** 2 for xi in x); a = my - b * mx
    ss = sum((yi - my) ** 2 for yi in y); sr = sum((yi - a - b * xi) ** 2 for xi, yi in zip(x, y))
    return a, b, 1 - sr / ss
print("1. σ_eff from CCC Figure 19 (P by bucket) — probit index z = Φ⁻¹(P) regressed on claims-weighted bucket mean age")
GAM = {}
for yr in ('cy2024', 'cy2025'):
    t = int(yr[2:]); ma = bucket_mean_age(t)
    xs = [ma[b] for b, _, _ in BUCK]; zs = [Phi_inv(CCC[b][yr]) for b, _, _ in BUCK]
    a0, g, r2 = ols(xs, zs); GAM[t] = g
    print(f"   {t}: z = {a0:+.3f} + {g:.4f}·age   R² {r2:.3f}   (buckets: " + ", ".join(f"{b} age {ma[b]:.1f} P {CCC[b][yr]*100:.1f}" for b, _, _ in BUCK) + ")")
    print("         fitted P by bucket: " + ", ".join(f"{Phi(a0 + g * ma[b])*100:.1f}" for b, _, _ in BUCK))
gamma = GAM[2024]
DELTA = {'low': 0.08, 'base': 0.11, 'high': 0.14}     # cross-sectional depreciation of ln V per year of age (ASSUMED; iSeeCars 5-yr 0.108 + sticker drift)
SIG = {k: d / gamma for k, d in DELTA.items()}; SIG['claim_size_only'] = 1.05
print(f"   γ(2024) = {gamma:.4f}/yr → σ_eff = δ/γ = " + ", ".join(f"{k} (δ={DELTA.get(k, '-')}): {v:.2f}" for k, v in SIG.items()))
print("   (claim-size-only σ 1.05 from HLDI 2024 quantiles: median 4.5k, 25% ≥ 9k → σ 1.03; 10% ≥ 18k → σ 1.08; it omits within-age value dispersion, so it is a lower bound → an UPPER bound on Δz)")

# ------------------------------------------------------------------ 2. body offset Δz and the split
VRATIO = {'low': 1.30, 'base': 1.50, 'high': 1.70}; SEV = 1.01
def dz(vr, sig): return (math.log(vr) - math.log(SEV)) / sig
def split(t, f, d):
    """P_car(a), P_LT(a), s(a) for year t's claims mix, frequency ratio f, probit offset d, given the single P(a)."""
    F = FL[t]; out = {}
    for a in AGES:
        if a not in F: continue
        c, l = F[a]; s = l * f / (l * f + c) if (l * f + c) > 0 else 0.0; p = Pf(a)
        lo, hi = -6.0, 6.0
        for _ in range(80):
            m = (lo + hi) / 2
            if s * Phi(m - d) + (1 - s) * Phi(m) < p: lo = m
            else: hi = m
        zc = (lo + hi) / 2; out[a] = (Phi(zc), Phi(zc - d), s)
    return out
def roll(f, curves):
    """TLF by year with body-specific P (curves: age -> (Pcar, Plt, _)) and R_LT = f·R_car; also LT share of claims and TL."""
    res = {}
    for t, F in FL.items():
        C = T = Cl = Tl = 0.0
        for a, (c, l) in F.items():
            pc_, pl_ = curves[a][0], curves[a][1]
            cc, cl = c * Rf(a), l * Rf(a) * f
            C += cc + cl; Cl += cl; T += cc * pc_ + cl * pl_; Tl += cl * pl_
        res[t] = (T / C, Cl / C, Tl / T)
    return res
one = {a: (Pf(a), Pf(a), 0) for a in AGES}
LISTED = {2024: 0.508, 2026: 0.567}      # E1 step 1: LT share of the listed salvage-title pool (MEASURED)
print("\n2. Variants: Δz = (ln V-ratio − ln severity-ratio)/σ_eff;  P_LT = Φ(z_car − Δz);  aggregate 2024 P(a) preserved at every age")
VAR = []
for fname, f in (('f=1.00', 1.0), ('f=0.85', 0.85), ('f=0.67 (HLDI adj.)', 0.67)):
    for vname, vr in (('V 1.50', 1.5),):
        for sname in ('base', 'claim_size_only'):
            VAR.append((fname, f, vname, vr, sname, SIG[sname]))
VAR += [('f=1.00', 1.0, 'V 1.30', 1.3, 'base', SIG['base']), ('f=1.00', 1.0, 'V 1.70', 1.7, 'base', SIG['base']),
        ('f=1.00', 1.0, 'V 1.50', 1.5, 'low', SIG['low']), ('f=1.00', 1.0, 'V 1.50', 1.5, 'high', SIG['high'])]
base_roll = roll(1.0, one)
print(f"   one-body roll (reference): TLF 2024 {base_roll[2024][0]*100:.2f}%, LT share of TL 2024 {base_roll[2024][2]*100:.1f}%, 2026 {base_roll[2026][2]*100:.1f}%, 2030 {base_roll[2030][2]*100:.1f}%")
print(f"   {'variant':44s} {'Δz':>5s} {'P_LT/P_car @8':>13s} {'@12':>6s} | {'LT%TL 24':>8s} {'26':>5s} {'30':>5s} | listed 50.8 / 56.7 | {'ΔTLF vs one-body, pp: 24→27':>26s} {'27→30':>6s} {'per yr 24→30':>12s}")
RES = {}
for fname, f, vname, vr, sname, sig in VAR:
    d = dz(vr, sig); cur = split(2024, f, d); rr = roll(f, cur); RES[(fname, vname, sname)] = (d, cur, rr)
    dd = lambda t0, t1: ((rr[t1][0] - rr[t0][0]) - (base_roll[t1][0] - base_roll[t0][0])) * 100
    print(f"   {fname:18s} {vname:7s} σ {sname:15s} {d:5.2f} {cur[8][1]/cur[8][0]:13.2f} {cur[12][1]/cur[12][0]:6.2f} | {rr[2024][2]*100:8.1f} {rr[2026][2]*100:5.1f} {rr[2030][2]*100:5.1f} |"
          f"  gap {rr[2024][2]*100-50.8:+5.1f} / {rr[2026][2]*100-56.7:+5.1f}    | {dd(2024, 2027):+26.2f} {dd(2027, 2030):+6.2f} {dd(2024, 2030)/6:+12.3f}")

# which f does the listed pool prefer, at the base Δz?  solve f so that the two-body roll's LT share of TL matches the listing
print("\n3. Listing-calibrated frequency ratio: f such that the roll's LT share of total losses equals the listed salvage-title share")
def f_for(target, t, d):
    lo, hi = 0.3, 1.5
    for _ in range(60):
        m = (lo + hi) / 2
        if roll(m, split(2024, m, d))[t][2] < target: lo = m
        else: hi = m
    return (lo + hi) / 2
for sname in ('base', 'claim_size_only'):
    d = dz(1.5, SIG[sname])
    for t in (2024, 2026):
        fs = f_for(LISTED[t], t, d); cur = split(2024, fs, d); rr = roll(fs, cur)
        print(f"   σ {sname:15s} Δz {d:.2f}: match {t} listed {LISTED[t]*100:.1f}% → f = {fs:.2f};  ΔTLF vs one-body 2024→2030 {((rr[2030][0]-rr[2024][0])-(base_roll[2030][0]-base_roll[2024][0]))*100:+.2f}pp ({((rr[2030][0]-rr[2024][0])-(base_roll[2030][0]-base_roll[2024][0]))*100/6:+.3f}/yr)")
print("   NOTE: the listed share is listings (incl. non-insurance consignments, excl. the clean-title pool) and the roll is modelled insurance total losses;")
print("         the comparison calibrates the COMBINED body effect f·P_LT/P_car, not f alone. f=1 with the base Δz already sits within ~1pp of the listing in 2026.")

# ------------------------------------------------------------------ 4. KPI table for the pitch: ΔTLF (supply) and ΔASP (price) by year, base variant
BASE = ('f=1.00', 'V 1.50', 'base'); d, cur, rr = RES[BASE]
print("\n4. Base variant (f=1.00, V-ratio 1.50, σ base): by year")
print(f"   {'year':4s} {'TLF 1-body':>10s} {'TLF 2-body':>10s} {'ΔTLF yoy 1-body':>15s} {'2-body':>7s} {'body-mix ΔTLF pp':>17s} {'LT%claims':>9s} {'LT%TL':>6s} {'ΔLT%TL pp':>9s} {'ASP body-mix pp':>15s} {'Copart units %':>14s} {'svc RPU %':>9s} {'revenue %':>9s}")
rows = []; prev = None
for t in range(2015, 2031):
    tl1, tl2 = base_roll[t][0], rr[t][0]; ltc, ltt = rr[t][1], rr[t][2]
    if prev:
        d1 = (tl1 - base_roll[t - 1][0]) * 100; d2 = (tl2 - rr[t - 1][0]) * 100; dm = d2 - d1
        dsh = (ltt - rr[t - 1][2]) * 100; asp = (1.5 - 1) * dsh / (1 + (1.5 - 1) * rr[t - 1][2])     # ASP_Drivers!H formula with the two-body share path
        units = dm / (rr[t - 1][0] * 100) * 100; rpu = 0.514 * asp; rev = units + rpu
        print(f"   {t:4d} {tl1*100:10.2f} {tl2*100:10.2f} {d1:+15.2f} {d2:+7.2f} {dm:+17.3f} {ltc*100:9.1f} {ltt*100:6.1f} {dsh:+9.2f} {asp:+15.2f} {units:+14.2f} {rpu:+9.2f} {rev:+9.2f}")
        rows.append(dict(year=t, tlf_one_body_pct=round(tl1 * 100, 3), tlf_two_body_pct=round(tl2 * 100, 3), dtlf_one_body_pp=round(d1, 3), dtlf_two_body_pp=round(d2, 3),
                         body_mix_supply_effect_pp=round(dm, 3), lt_share_claims_pct=round(ltc * 100, 2), lt_share_tl_pct=round(ltt * 100, 2), d_lt_share_tl_pp=round(dsh, 2),
                         asp_body_mix_effect_pp=round(asp, 3), copart_units_effect_pct=round(units, 3), service_rpu_effect_pct=round(rpu, 3), revenue_effect_pct=round(rev, 3)))
    prev = t

# ------------------------------------------------------------------ 5. write
with open(D / 'body_mix_tlf_asp_2015_2030.csv', 'w', newline='') as fh:
    fh.write("# E1 steps 4-6 (scripts/experiments/e1_body_propensity.py, 2026-09-26): fleet roll with body-specific totaling propensity. Base variant: R_LT = R_car (f=1.00), value ratio LT/car 1.50 (E8), HLDI severity ratio 1.01, probit offset dz = (ln1.50 - ln1.01)/sigma_eff with sigma_eff = delta/gamma, delta = 0.11/yr (ASSUMED), gamma = probit slope of CCC 2024 P-by-bucket in age (MEASURED). Aggregate 2024 P(a) preserved at every age.\n")
    fh.write("# body_mix_supply_effect_pp = (two-body dTLF) - (one-body dTLF): the change in TLF each year attributable to the light-truck share of claims rising, i.e. what the single-curve roll (TLF_Roll) overstates. asp_body_mix_effect_pp = ASP_Drivers!H formula on the two-body LT-share-of-TL path with ratio 1.50. copart_units_effect = supply effect / TLF; service_rpu_effect = 0.514 x ASP effect; revenue = sum. Sales after the last actual year held at that year's level and mix (ASSUMED). FITTED/ASSUMED: sigma_eff, delta, value ratio; MEASURED: severity ratio, gamma, sales, CCC buckets.\n")
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
with open(D / 'age_curves_by_body.csv', 'w', newline='') as fh:
    fh.write("# E1 step 4 (scripts/experiments/e1_body_propensity.py, 2026-09-26): totaling propensity by age and body. P_single = fitted P(a) from age_curves.csv (reproduces CCC 2024). P_car/P_lt solve s(a)*P_lt + (1-s(a))*P_car = P_single(a) with P_lt = PHI(PHI^-1(P_car) - dz); s(a) = LT share of claims at age a (2024 fleet roll x f). Columns for the base variant (f=1.00, V 1.50, sigma base) and sensitivities. Structural, not refitted: MEASURED direction (HLDI severity, E8 value), FITTED/ASSUMED magnitude (sigma_eff, delta).\n")
    w = csv.writer(fh)
    keys = [BASE, ('f=1.00', 'V 1.50', 'claim_size_only'), ('f=0.85', 'V 1.50', 'base'), ('f=0.67 (HLDI adj.)', 'V 1.50', 'base'), ('f=1.00', 'V 1.30', 'base'), ('f=1.00', 'V 1.70', 'base')]
    lab = ['base', 'sigma_claim_size_only', 'f085', 'f067', 'V130', 'V170']
    w.writerow(['age', 'P_single', 'lt_share_claims_2024'] + [f'P_car_{l}' for l in lab] + [f'P_lt_{l}' for l in lab] + [f'dz_{l}' for l in lab])
    for a in AGES:
        if a not in RES[BASE][1]: continue
        w.writerow([a, round(Pf(a), 4), round(RES[BASE][1][a][2], 4)] + [round(RES[k][1][a][0], 4) for k in keys] + [round(RES[k][1][a][1], 4) for k in keys] + [round(RES[k][0], 3) for k in keys])
print("\nwrote data/csv/body_mix_tlf_asp_2015_2030.csv, data/csv/age_curves_by_body.csv")
