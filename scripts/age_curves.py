#!/usr/bin/env python3
"""Mechanism A age curves - S(age), R(age), P(age): extraction, validation, fit.  (built 2026-09-14)

WHAT THIS ANSWERS: "how exactly are the survival, claim-frequency and totaling-propensity curves calculated,
and what evidence backs them?"

  S(age)  survival        : EPA schedule (ORNL TEDB Ed.40 Table 3.15) with ONE stretch parameter k per body type,
                            S_k(a) = S_EPA(a / k).  k is fitted to the IHS/Polk fleet-age census (Tables 3.11/3.12,
                            2000 and 2013) and to S&P's 2024/25 anchors (avg age, 66% 7+, VIO).  Rising k = cars last longer.
  R(age)  rel. claim freq : R(a) = e(a)*exp(-lam*max(a-6,0)): flat through age 6, then declines.  Fitted jointly with P to CCC's published
                            claim-mix statistics (share of repairables 7+, avg age of claim vehicles, ...).  Miles-by-age
                            (Table 3.14) shows how much of the decline is exposure vs coverage/reporting.
  P(age)  TL propensity   : logistic pmin + (pmax-pmin)/(1+exp(-(a-c)/s)).  Fitted jointly with R to CCC: TLF level,
                            share of TL valuations 7+, avg age of TL vs repairable vehicles, 1-in-10 for <=3 yrs.
  OUT-OF-SAMPLE          : R,P fitted on the 2024 cross-section are applied to the 2019/2020 fleet; CCC published the
                            same statistics for those years, so the demographic model is tested on years it never saw.

Inputs (all public, robots-open, provenance in PROVENANCE.md s.5):
  raw/ornl/tedb40/Table3_06 (Ward's new retail sales 1970-2021), 3_11/3_12 (IHS cars/trucks in operation by age,
  1970/2000/2013), 3_13 (S&P avg age 1970-2020), 3_14 (EPA/NHTSA annual miles by age), 3_15 (EPA survival by age),
  3_16 (heavy-truck survival, Schmoyer/ORNL).  data/csv/fred_TOTALNSA.csv + fred_LTRUCKNSA.csv (2022-2025 sales).
  CCC Crash Course statements quoted in docs/AGE_CURVES.md.
Outputs: data/csv/ornl_tedb40_*.csv (EPA/Ward's extracts; the IHS-sourced census and avg-age extracts go to raw/ornl/tedb40/extracts/, gitignored), light_vehicle_sales_by_year.csv, age_curves.csv,
         age_curves_validation.csv.
Usage:  ./.venv/bin/python scripts/age_curves.py
"""
import csv, glob, math, pathlib, random, sys
from openpyxl import load_workbook
ROOT = pathlib.Path(__file__).resolve().parent.parent
ORNL = ROOT / 'raw/ornl/tedb40'; OUT = ROOT / 'data/csv'
SRC = ("ORNL Transportation Energy Data Book Ed.40 (June 2022) spreadsheets, "
       "https://tedb.ornl.gov/wp-content/uploads/2022/06/TEDB_40_Spreadsheets_06012022.zip (robots-open, fetched 2026-09-14)")

def rows_of(prefix):
    f = sorted(glob.glob(str(ORNL / f'{prefix}_*.xlsx')))[0]
    return list(load_workbook(f, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True)), f.split('/')[-1]
def isnum(v): return isinstance(v, (int, float)) and not isinstance(v, bool)
def nums(row): return [v for v in row if isnum(v)]
LOCAL = ORNL / 'extracts'   # IHS-sourced tables (3.11/3.12/3.13) carry 'FURTHER REPRODUCTION PROHIBITED' -> extracts stay gitignored
def write_csv(name, hdr, cols, rows, local=False):
    dest = (LOCAL if local else OUT) / name
    with open(dest, 'w', newline='') as fh:
        for h in hdr: fh.write(f"# {h}\n")
        w = csv.writer(fh); w.writerow(cols); w.writerows(rows)
    print(f"  -> {dest.relative_to(ROOT)} ({len(rows)} rows)")

# ----------------------------------------------------------------------------------------------------- 0. EXTRACT
print("0. EXTRACT ORNL TEDB Ed.40 tables")
R, f15 = rows_of('Table3_15'); S_EPA = {}
for r in R:
    n = nums(r)
    if len(n) >= 3 and float(n[0]).is_integer() and 0 <= n[0] <= 31 and n[1] <= 1 and n[2] <= 1: S_EPA[int(n[0])] = (n[1], n[2])
assert len(S_EPA) == 32, len(S_EPA)
write_csv('ornl_tedb40_survival_by_age.csv', [SRC, f"Table 3.15 ({f15}): EPA estimated survival rates by vehicle age, cars and light trucks (MY2015 rulemaking schedules)"],
          ['age', 'survival_cars', 'survival_light_trucks'], [[a, *S_EPA[a]] for a in sorted(S_EPA)])

R, f14 = rows_of('Table3_14'); MILES = {}
for r in R:
    n = nums(r)
    if len(n) >= 3 and float(n[0]).is_integer() and 0 <= n[0] <= 30 and n[1] > 1000: MILES[int(n[0])] = (n[1], n[2])
assert len(MILES) == 31, len(MILES)
write_csv('ornl_tedb40_miles_by_age.csv', [SRC, f"Table 3.14 ({f14}): EPA estimated annual miles per vehicle by age, cars and light trucks"],
          ['age', 'miles_cars', 'miles_light_trucks'], [[a, *MILES[a]] for a in sorted(MILES)])

R, f06 = rows_of('Table3_06'); SALES = {}
for r in R:
    n = nums(r)
    if len(n) >= 5 and float(n[0]).is_integer() and 1970 <= n[0] <= 2021: SALES[int(n[0])] = dict(cars=n[1], lt=n[2], heavy=n[4])
assert len(SALES) == 52
write_csv('ornl_tedb40_new_sales.csv', [SRC, f"Table 3.6 ({f06}): New retail vehicle sales (thousands), Ward's"],
          ['year', 'cars_k', 'light_trucks_k', 'heavy_trucks_k'], [[y, SALES[y]['cars'], SALES[y]['lt'], SALES[y]['heavy']] for y in sorted(SALES)])

R, f13 = rows_of('Table3_13'); AVGAGE = {}
for r in R:
    c = [v for v in r if v is not None]
    if c and isnum(c[0]) and 1970 <= c[0] <= 2021 and len(c) >= 3:
        g = lambda v: v if isnum(v) else None
        AVGAGE[int(c[0])] = (g(c[1]), g(c[2]), g(c[3]) if len(c) > 3 else None)
write_csv('ornl_tedb40_avg_age.csv', [SRC, f"Table 3.13 ({f13}): U.S. average age of cars and light trucks (S&P Global Mobility / Polk)"],
          ['year', 'avg_age_cars', 'avg_age_light_trucks', 'avg_age_all_light'], [[y, *AVGAGE[y]] for y in sorted(AVGAGE)], local=True)

def parse_inop(prefix):
    R, f = rows_of(prefix); out = {}
    for r in R:
        lab = next((v for v in r if v is not None), None)      # label sits in column B in these two tables
        if isnum(lab) and 1 <= lab <= 14:                       # ages 1..14 are stored as numbers
            n = nums(r)[1:]
            if len(n) >= 9: out[int(lab)] = dict(v1970=n[0], v2000=n[3], v2013=n[6])
        elif isinstance(lab, str) and (lab.lower().startswith('under 1') or lab.lower().startswith('15 and')):
            n = nums(r)
            if len(n) >= 9:
                out[0 if lab.lower().startswith('under') else 15] = dict(v1970=n[0], v2000=n[3], v2013=n[6])
        elif isinstance(lab, str) and lab.lower().startswith('subtotal'):
            n = nums(r); out['total'] = dict(v1970=n[0], v2000=n[2], v2013=n[4])
    return out, f
CARS_INOP, f11 = parse_inop('Table3_11'); TRK_INOP, f12 = parse_inop('Table3_12')
assert len(CARS_INOP) == 17 and len(TRK_INOP) == 17
write_csv('ornl_tedb40_vehicles_in_operation_by_age.csv',
          [SRC, f"Tables 3.11 ({f11}) and 3.12 ({f12}): cars / trucks in operation by age (thousands), IHS Automotive (Polk). 'trucks' INCLUDES heavy trucks. age 15 = 15 and older. Snapshot as of July 1."],
          ['age', 'cars_1970_k', 'cars_2000_k', 'cars_2013_k', 'trucks_1970_k', 'trucks_2000_k', 'trucks_2013_k'],
          [[a, CARS_INOP[a]['v1970'], CARS_INOP[a]['v2000'], CARS_INOP[a]['v2013'], TRK_INOP[a]['v1970'], TRK_INOP[a]['v2000'], TRK_INOP[a]['v2013']] for a in range(16)], local=True)

R, f16 = rows_of('Table3_16'); S_HEAVY = {a: 1.0 - 0.0015 * a for a in range(4)}     # ages 0-3 not tabulated; ASSUMED ~1
for r in R:
    n = nums(r)
    if len(n) >= 6 and float(n[0]).is_integer() and 4 <= n[0] <= 30 and n[1] <= 100: S_HEAVY[int(n[0])] = n[5] / 100   # 1990-MY column
assert len(S_HEAVY) == 31

# sales 2022-2025 from FRED (thousands, NSA monthly -> calendar sums), rescaled to Ward's basis on the 2021 overlap
def fred_annual(path, col):
    d = {}
    for r in csv.DictReader(open(path)):
        v = r.get(col) or r.get('value')
        if v and v != '.': d.setdefault(int(r['observation_date'][:4]), []).append(float(v))
    return {y: sum(v) for y, v in d.items() if len(v) == 12}
TOT = fred_annual(OUT / 'fred_TOTALNSA.csv', 'TOTALNSA'); LTR = fred_annual(OUT / 'fred_LTRUCKNSA.csv', 'LTRUCKNSA')
sc_lt = SALES[2021]['lt'] / LTR[2021]; sc_car = SALES[2021]['cars'] / (TOT[2021] - LTR[2021])
print(f"  FRED vs Ward's 2021 overlap: light {TOT[2021]:,.0f}k vs {SALES[2021]['cars']+SALES[2021]['lt']:,.0f}k; LT {LTR[2021]:,.0f}k vs {SALES[2021]['lt']:,.0f}k "
      f"-> FRED 2022-25 scaled by cars x{sc_car:.4f}, LT x{sc_lt:.4f} (BEA counts fleet deliveries Ward's retail series does not)")
for y in range(2022, 2026):
    SALES[y] = dict(cars=(TOT[y] - LTR[y]) * sc_car, lt=LTR[y] * sc_lt, heavy=SALES[2021]['heavy'], src="FRED TOTALNSA/LTRUCKNSA x Ward's-basis scale")
write_csv('light_vehicle_sales_by_year.csv',
          ["Cohort sizes for the fleet roll. 1970-2021 Ward's via ORNL TEDB Ed.40 Table 3.6; 2022-2025 FRED TOTALNSA (light vehicles) and LTRUCKNSA (light trucks), NSA monthly summed by calendar year (fetched 2026-09-14),",
           f" rescaled to Ward's basis using the 2021 overlap (cars x{sc_car:.4f}, light trucks x{sc_lt:.4f}). heavy trucks 2022-25 = 2021 carried (used only for the 2013 truck-census check)."],
          ['year', 'cars_k', 'light_trucks_k', 'heavy_trucks_k', 'source'],
          [[y, round(SALES[y]['cars'], 1), round(SALES[y]['lt'], 1), round(SALES[y]['heavy'], 1), SALES[y].get('src', "Ward's (ORNL TEDB40 T3.6)")] for y in sorted(SALES)])

# ----------------------------------------------------------------------------------------------------- 1. S(age)
def S_of(table_idx, a, k):
    """EPA survival evaluated at stretched age a/k, linear interpolation; zero beyond the table."""
    x = a / k
    if x >= 31: return 0.0
    i = int(x); fr = x - i
    s0 = S_EPA[i][table_idx]; s1 = S_EPA[min(i + 1, 31)][table_idx]
    return s0 + fr * (s1 - s0)

def fleet(t, kc, kl):
    """Vehicles on the road at end of year t by age a = t - MY (thousands): dict age -> (cars, light trucks, heavy)."""
    out = {}
    for a in range(0, t - 1969):
        my = t - a
        if my not in SALES: break
        c = SALES[my]['cars'] * S_of(0, a, kc); l = SALES[my]['lt'] * S_of(1, a, kl)
        h = SALES[my]['heavy'] * (S_HEAVY[min(a, 30)] if a <= 30 else max(0.0, S_HEAVY[30] - 0.02 * (a - 30)))
        out[a] = (c, l, h)
    return out

def bucket(fl, idx):
    b = {a: 0.0 for a in range(16)}
    for a, v in fl.items(): b[min(a, 15)] += v[idx] if isinstance(idx, int) else sum(v[i] for i in idx)
    return b
def stats(fl, idx=(0, 1), half=0.5):
    """total (k), avg age (a + half), share 7+, share 15+, count <=6 (k)"""
    tot = sum(sum(v[i] for i in idx) for v in fl.values())
    avg = sum(sum(v[i] for i in idx) * (a + half) for a, v in fl.items()) / tot
    s7 = sum(sum(v[i] for i in idx) for a, v in fl.items() if a >= 7) / tot
    s15 = sum(sum(v[i] for i in idx) for a, v in fl.items() if a >= 15) / tot
    le6 = sum(sum(v[i] for i in idx) for a, v in fl.items() if a <= 6)
    return tot, avg, s7, s15, le6

def census_loss(k, year, body):
    """Fit metric vs IHS census: squared bucket-share errors (0-1 combined, 2..14, 15+) + total error."""
    fl = fleet(year, k, k)
    if body == 'cars':   pred = bucket(fl, 0); act = {a: CARS_INOP[a][f'v{year}'] for a in range(16)}
    else:                pred = bucket(fl, (1, 2)); act = {a: TRK_INOP[a][f'v{year}'] for a in range(16)}
    tp, ta = sum(pred.values()), sum(act.values())
    ps = {a: pred[a] / tp for a in pred}; as_ = {a: act[a] / ta for a in act}
    e = (ps[0] + ps[1] - as_[0] - as_[1]) ** 2 + sum((ps[a] - as_[a]) ** 2 for a in range(2, 16))
    return e + 0.5 * (tp / ta - 1) ** 2, pred, act

def minimize1d(fn, lo, hi, n=60):
    best = min(((fn(lo + (hi - lo) * i / n), lo + (hi - lo) * i / n) for i in range(n + 1)), key=lambda x: x[0])[1]
    a, b = max(lo, best - (hi - lo) / n), min(hi, best + (hi - lo) / n)
    for _ in range(40):
        m1, m2 = a + (b - a) / 3, b - (b - a) / 3
        if fn(m1) < fn(m2): b = m2
        else: a = m1
    return (a + b) / 2

print("\n1. S(age): EPA schedule vs the IHS/Polk census (share by age, thousands)")
KFIT = {}
for year in (2000, 2013):
    for body in ('cars', 'trucks'):
        k = minimize1d(lambda k: census_loss(k, year, body)[0], 0.7, 2.0)
        KFIT[(year, body)] = k
        _, pred1, act = census_loss(1.0, year, body); _, predk, _ = census_loss(k, year, body)
        tp1, tpk, ta = sum(pred1.values()), sum(predk.values()), sum(act.values())
        mae1 = sum(abs(pred1[a] / tp1 - act[a] / ta) for a in range(16)) / 16 * 100
        maek = sum(abs(predk[a] / tpk - act[a] / ta) for a in range(16)) / 16 * 100
        print(f"  {year} {body:6s}: raw EPA total {tp1/1e3:6.1f}M vs census {ta/1e3:6.1f}M ({tp1/ta-1:+.1%}); share15+ raw {pred1[15]/tp1:.1%} vs {act[15]/ta:.1%}; "
              f"bucket MAE {mae1:.2f}pp  ->  k={k:.3f}: total {tpk/1e3:6.1f}M ({tpk/ta-1:+.1%}), share15+ {predk[15]/tpk:.1%}, MAE {maek:.2f}pp")
        if year == 2013:
            print("        age : " + " ".join(f"{a:>5d}" for a in range(16)))
            print("        IHS : " + " ".join(f"{act[a]/ta*100:5.1f}" for a in range(16)))
            print("        k   : " + " ".join(f"{predk[a]/tpk*100:5.1f}" for a in range(16)))
            print("        EPA : " + " ".join(f"{pred1[a]/tp1*100:5.1f}" for a in range(16)))
kc13, kl13 = KFIT[(2013, 'cars')], KFIT[(2013, 'trucks')]

# --- S&P "average age" is NOT a usable anchor: the IHS census buckets themselves cannot reproduce it ---
print("\n  Why average age is not the calibration target: avg age implied by the IHS 2013 census (the same Polk data S&P uses),")
print("  under three assumptions for the mean age of the '15 and older' bucket, vs S&P's published figure (Table 3.13):")
for col, inop, sp in (('cars', CARS_INOP, AVGAGE[2013][0]), ('trucks', TRK_INOP, AVGAGE[2013][1])):
    tot = sum(inop[a]['v2013'] for a in range(16))
    line = "  ".join(f"tail {tail}: {(sum(inop[a]['v2013']*(a+0.5) for a in range(15)) + inop[15]['v2013']*(tail+0.5))/tot:4.1f}" for tail in (19, 23, 27))
    print(f"    {col:6s} 2013: {line}   S&P {sp}")
print("  -> reproducing S&P needs a 15+ bucket averaging ~27 yrs: registrations that are barely driven. Any curve calibrated to")
print("     12.8 must inflate that tail (the blueprint tab's flat-survival artefact). Calibrate S to COUNTS instead (below).")

# --- k drift after 2013: fit ONE multiplier on both k's to S&P's 2024/25 count anchors (VIO ~289M light, 66% aged 7+) ---
VIO_SP, SH7_SP = 289_000, 0.66
def loss_2024(m):
    tot, avg, s7, s15, le6 = stats(fleet(2024, kc13 * m, kl13 * m))
    return ((tot / VIO_SP - 1) / 0.015) ** 2 + ((s7 - SH7_SP) / 0.01) ** 2
m24 = minimize1d(loss_2024, 0.9, 1.6)
def kmult(t):
    """survival stretch multiplier vs the 2013 census fit: linear 2013->2024, flat after (conservative base case)."""
    return 1.0 if t <= 2013 else (m24 if t >= 2024 else 1 + (m24 - 1) * (t - 2013) / 11)
def FL(t): return fleet(t, kc13 * kmult(t), kl13 * kmult(t))
fl24, fl20, fl19, fl25 = FL(2024), FL(2020), FL(2019), FL(2025)
tot24, avg24, s7_24, s15_24, le6_24 = stats(fl24); tot20, avg20, s7_20, s15_20, le6_20 = stats(fl20); tot25, avg25, s7_25, s15_25, le6_25 = stats(fl25)
_, avgc24, *_ = stats(fl24, (0,)); _, avgl24, *_ = stats(fl24, (1,))
kc24, kl24 = kc13 * m24, kl13 * m24
print(f"\n  k drift: multiplier {m24:.3f} by 2024 (fitted to VIO {VIO_SP/1e3:.0f}M and 66% aged 7+)  ->  k_cars {kc24:.3f}, k_LT {kl24:.3f}   (k=1 = raw EPA; k>1 = vehicles last longer)")
print(f"    2024 roll: VIO {tot24/1e3:.0f}M | 7+ {s7_24:.1%} | 15+ {s15_24:.1%} | avg age (t-MY+0.5) {avg24:.1f} [S&P 12.8; see convention note] | cars {avgc24:.1f} vs S&P 14.5, LT {avgl24:.1f} vs 11.9 (not fitted)")
print(f"    2020->2025 roll: VIO {tot20/1e3:.0f}M -> {tot25/1e3:.0f}M ({tot25/tot20-1:+.1%}) vs Experian +5.1% (2020->Q3-25); <=6-yr count {le6_20/1e3:.1f}M -> {le6_25/1e3:.1f}M ({(le6_25-le6_20)/1e3:+.1f}M) vs Experian 'over 12 million less'")
print(f"    NOTE: sales alone (no survival) give <=6 yrs MY2014-20 = {sum(SALES[y]['cars']+SALES[y]['lt'] for y in range(2014,2021))/1e3:.0f}M vs MY2019-25 = {sum(SALES[y]['cars']+SALES[y]['lt'] for y in range(2019,2026))/1e3:.0f}M "
      f"({(sum(SALES[y]['cars']+SALES[y]['lt'] for y in range(2019,2026))-sum(SALES[y]['cars']+SALES[y]['lt'] for y in range(2014,2021)))/1e3:+.1f}M): Experian's -12M is not reproducible from sales under ANY survival curve -> definitional; recorded, not fitted.")
med_c = minimize1d(lambda a: (S_of(0, a, kc24) - 0.5) ** 2, 5, 30); med_l = minimize1d(lambda a: (S_of(1, a, kl24) - 0.5) ** 2, 5, 30)
print(f"    implied median lifetime 2024 curves: cars {med_c:.1f} yrs, light trucks {med_l:.1f} yrs   (raw EPA: cars 15.1, LT 16.0; 2013 fit: cars {minimize1d(lambda a: (S_of(0, a, kc13) - 0.5) ** 2, 5, 30):.1f}, LT {minimize1d(lambda a: (S_of(1, a, kl13) - 0.5) ** 2, 5, 30):.1f})")

# ----------------------------------------------------------------------------------------------------- 2. R(age), P(age)
print("\n2. R(age) and P(age): joint fit to CCC's 2024 claim-mix statistics, then out-of-sample on 2019/2020/2025")
AGES = range(0, 46)   # sum to 45: with k~1.27 the stretched EPA schedule is non-zero to ~age 39 (the workbook does the same)
def fleet_by_age(fl): return {a: v[0] + v[1] for a, v in fl.items()}
F24, F20, F19, F25 = map(fleet_by_age, (fl24, fl20, fl19, fl25))
def miles(a):
    a = min(a, 30); c, l = MILES[a]; w = fl24[min(a, max(fl24))]
    return (c * w[0] + l * w[1]) / (w[0] + w[1]) if (w[0] + w[1]) > 0 else (c + l) / 2
EXPO0 = 0.5     # a model-year-t vehicle is on the road ~half of calendar year t (sales spread through the year)
def Rf(a, lam):
    """relative insured-claim frequency per vehicle on the road: FLAT through age 6, then log-linear decline; age-0 exposure = half a year.
    (A free 0-6 slope is not identified by the CCC targets: fitting one gives +1.6%/yr with the same loss, so it is fixed at zero.)"""
    return (EXPO0 if a == 0 else 1.0) * math.exp(-lam * max(a - 6, 0))
def Pf(a, pmin, pmax, c, s): return pmin + (pmax - pmin) / (1 + math.exp(-(a - c) / s))
def mix(F, th):
    lam, pmin, pmax, c, s = th
    cl = {a: F.get(a, 0) * Rf(a, lam) for a in AGES}
    tl = {a: cl[a] * Pf(a, pmin, pmax, c, s) for a in AGES}
    rp = {a: cl[a] - tl[a] for a in AGES}
    C, T, Rp = sum(cl.values()), sum(tl.values()), sum(rp.values())
    avg = lambda d, tot: sum(d[a] * a for a in AGES) / tot
    sh = lambda d, tot, lo, hi: sum(d[a] for a in AGES if lo <= a <= hi) / tot
    return dict(tlf=T / C, tl7=sh(tl, T, 7, 99), rp7=sh(rp, Rp, 7, 99), rp3=sh(rp, Rp, 0, 3), cl7=sh(cl, C, 7, 99),
                age_cl=avg(cl, C), age_rp=avg(rp, Rp), age_tl=avg(tl, T), p03=sum(tl[a] for a in range(4)) / sum(cl[a] for a in range(4)))

TGT = {   # CCC 2024 statistics -> (value, scale, source).  scale = error that costs one loss unit
 'tlf':    (0.223, 0.005, "CCC annual all-loss TLF 2024 = 22.3% (data/csv/ccc_tlf_annual.csv)"),
 'tl7':    (0.72,  0.010, "Crash Course 2024/Q4: 'almost 72% of valuations across all loss categories are for vehicles 7 years or older'"),
 'rp7':    (0.45,  0.010, "2024/Q4: 'vehicles seven years or older now make up nearly 45% of all repairable claims'"),
 'rp3':    (0.30,  0.020, "2024/Q4: 'only 26.3% of repairable ICE vehicles are three years or newer'; all-fuel ~30% after adding EV/hybrid (79%/60% of which are <=3 yrs)"),
 'age_cl': (7.6,   0.15,  "2025/Q1: 'for claims, the average age of vehicles has increased to 7.6 years' (2024)"),
 'age_rp': (6.8,   0.15,  "2025/Q1: 'the average age of repairable vehicles was 6.8 years in 2024'"),
 'age_tl': (10.6,  0.15,  "2025/Q1: '... and 10.6 years for total loss vehicles' (2024)"),
 'p03':    (0.10,  0.010, "2026 annual: 'for claims that are three years old or newer, 1 in 10 are flagged as a total loss'"),
}
def make_loss(F):
    def loss(th):
        lam, pmin, pmax, c, s = th
        if not (0 <= lam <= 0.5 and 0.01 <= pmin <= 0.3 and pmin < pmax <= 0.95 and 0 <= c <= 30 and 0.3 <= s <= 12): return 1e9
        m = mix(F, th); return sum(((m[k] - v) / sc) ** 2 for k, (v, sc, _) in TGT.items())
    return loss

def nelder_mead(fn, x0, step, iters=4000):
    n = len(x0); pts = [list(x0)] + [[x0[j] + (step[j] if j == i else 0) for j in range(n)] for i in range(n)]
    vals = [fn(p) for p in pts]
    for _ in range(iters):
        o = sorted(range(n + 1), key=lambda i: vals[i]); pts = [pts[i] for i in o]; vals = [vals[i] for i in o]
        cen = [sum(p[j] for p in pts[:-1]) / n for j in range(n)]
        xr = [cen[j] + (cen[j] - pts[-1][j]) for j in range(n)]; fr = fn(xr)
        if fr < vals[0]:
            xe = [cen[j] + 2 * (cen[j] - pts[-1][j]) for j in range(n)]; fe = fn(xe)
            pts[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]: pts[-1], vals[-1] = xr, fr
        else:
            xc = [cen[j] + 0.5 * (pts[-1][j] - cen[j]) for j in range(n)]; fc = fn(xc)
            if fc < vals[-1]: pts[-1], vals[-1] = xc, fc
            else:
                for i in range(1, n + 1):
                    pts[i] = [pts[0][j] + 0.5 * (pts[i][j] - pts[0][j]) for j in range(n)]; vals[i] = fn(pts[i])
        if max(vals) - min(vals) < 1e-10: break
    i = min(range(n + 1), key=lambda i: vals[i]); return pts[i], vals[i]

def fit(F, seed=7, restarts=40):
    random.seed(seed); best = (None, 1e18); L = make_loss(F)
    for _ in range(restarts):
        x0 = [random.uniform(0.02, 0.2), random.uniform(0.03, 0.15), random.uniform(0.3, 0.8), random.uniform(4, 16), random.uniform(1, 6)]
        th, v = nelder_mead(L, x0, [0.02, 0.02, 0.05, 2, 1])
        if v < best[1]: best = (th, v)
    return best
TH, L = fit(F24); lam, pmin, pmax, c, s = TH
m24x = mix(F24, TH)
print(f"  fitted  R(a) = exposure(a) x exp(-{lam:.4f} x max(a-6,0))   [flat through age 6],  exposure(0)={EXPO0}, else 1")
print(f"          P(a) = {pmin:.3f} + ({pmax:.3f} - {pmin:.3f}) / (1 + exp(-(a - {c:.2f}) / {s:.2f}))          loss {L:.1f} on 8 targets, 5 params")
print(f"  {'statistic':10s} {'CCC 2024':>9s} {'model':>7s}   source")
for k, (v, sc, q) in TGT.items():
    fmt = (lambda x: f"{x:9.1f}") if k.startswith('age') else (lambda x: f"{x:9.1%}")
    print(f"  {k:10s} {fmt(v)} {fmt(m24x[k])[-7:]}   {q}")

w06 = sum(F24[a] for a in range(7)); w7 = sum(F24[a] for a in range(7, 32))
mi06 = sum(F24[a] * miles(a) for a in range(7)) / w06; mi7 = sum(F24[a] * miles(a) for a in range(7, 32)) / w7
r06 = sum(F24[a] * Rf(a, lam) for a in range(7)) / w06; r7 = sum(F24[a] * Rf(a, lam) for a in range(7, 32)) / w7
print(f"\n  R decomposition, 7+ vs 0-6 (2024 fleet weights): fitted R ratio {r7/r06:.3f}; miles-per-vehicle ratio {mi7/mi06:.3f} (EPA T3.14) "
      f"-> residual {r7/r06/(mi7/mi06):.3f} = coverage/filing (liability-only, higher deductibles, unfiled small claims on older cars)")
C = sum(F24[a] * Rf(a, lam) for a in AGES); T = sum(F24[a] * Rf(a, lam) * Pf(a, pmin, pmax, c, s) for a in AGES)
print("  bucket        fleet%  claims%   TL%   R(a)   P(a)  miles/yr")
BUCK = []
for lo, hi, lab in ((0, 0, '0 (new)'), (1, 3, '1-3'), (4, 6, '4-6'), (7, 12, '7-12'), (13, 99, '13+')):
    fw = sum(F24[a] for a in AGES if lo <= a <= hi); cw = sum(F24[a] * Rf(a, lam) for a in AGES if lo <= a <= hi)
    tw = sum(F24[a] * Rf(a, lam) * Pf(a, pmin, pmax, c, s) for a in AGES if lo <= a <= hi)
    mi = sum(F24[a] * miles(a) for a in AGES if lo <= a <= hi) / fw
    BUCK.append((lab, fw / sum(F24.values()), cw / C, tw / T, cw / fw, tw / cw, mi))
    print(f"  {lab:12s} {fw/sum(F24.values()):6.1%} {cw/C:7.1%} {tw/T:6.1%}  {cw/fw:5.3f}  {tw/cw:5.3f}  {mi:7,.0f}")

print("\n  OUT-OF-SAMPLE (R,P fixed at the 2024 fit; only the fleet changes)")
m19, m20, m25 = mix(F19, TH), mix(F20, TH), mix(F25, TH)
oos = [('2019 repairables 7+ share', 0.35, m19['rp7'], "2024/Q4: 'up from 35% in 2019'"),
       ('2019 repairables <=3 share', 0.385, m19['rp3'], "2025/Q1: 'vehicles 3 years or newer represented 38.5% of the repairable mix in 2019'"),
       ('2020 avg age, claims', 6.9, m20['age_cl'], "2025/Q1: 'up from 6.9 years in 2020'"),
       ('2020 avg age, repairables', 6.1, m20['age_rp'], "2025/Q1: 'up from 6.1 years old in 2020'"),
       ('2020 avg age, total loss', 10.0, m20['age_tl'], "2025/Q1: 'up from 10.0 years old in 2020'"),
       ('2019 TLF (demographics only)', 0.192, m19['tlf'], "CCC annual 2019 = 19.2%; gap = non-demographic (cycle / technology / filing)"),
       ('2020 TLF (demographics only)', 0.206, m20['tlf'], "CCC annual 2020 = 20.6%"),
       ('2025 TLF (demographics only)', 0.231, m25['tlf'], "CCC annual 2025 = 23.1%"),
       ('2025 TL 7+ share', 0.72, m25['tl7'], "2025/Q4: 'over 72% of total loss valuations are on vehicles 7 years or older'"),
       ('2025 repairables 7+ share', 0.46, m25['rp7'], "2025/Q4: 'almost 46% of repairable vehicles are 7 years or older'")]
for lab, act, pred, q in oos:
    fmt = (lambda x: f"{x:6.1f}") if 'age' in lab else (lambda x: f"{x:6.1%}")
    print(f"  {lab:30s} actual {fmt(act)}  model {fmt(pred)}  err {fmt(pred-act) if 'age' in lab else f'{(pred-act)*100:+5.1f}pp':>7s}   {q}")
drift = (m25['tlf'] - m19['tlf']) * 100
print(f"  demographic TLF drift 2019->2025 = {drift:+.2f}pp ({drift/6:+.2f}pp/yr) of the actual +3.9pp  ->  {drift/3.9:.0%} of the rise is fleet ageing; the rest is level (cycle, technology, filing behaviour)")

# sensitivity: refit R,P under a weaker / stronger survival drift -> are the bucket ratios robust to S?
print("\n  SENSITIVITY of the R,P bucket ratios to the survival drift assumption (R,P refitted each time)")
print(f"  {'k mult 2024':>12s} {'VIO':>6s} {'7+':>6s} | {'R 7+/0-6':>9s} {'P 7+':>6s} {'P 0-6':>6s} | {'drift/yr 19->25':>15s}")
SENS = []
for mm in (1.0, 1.10, m24, 1.30):
    def FLm(t, mm=mm):
        k = 1.0 if t <= 2013 else (mm if t >= 2024 else 1 + (mm - 1) * (t - 2013) / 11)
        return fleet_by_age(fleet(t, kc13 * k, kl13 * k))
    F = FLm(2024); th, v = fit(F, restarts=20); mx = mix(F, th)
    tot = sum(F.values()); s7 = sum(F[a] for a in AGES if a >= 7) / tot
    w06 = sum(F[a] for a in range(7)); w7 = sum(F[a] for a in range(7, 32))
    rr = (sum(F[a] * Rf(a, th[0]) for a in range(7, 32)) / w7) / (sum(F[a] * Rf(a, th[0]) for a in range(7)) / w06)
    cl = {a: F[a] * Rf(a, th[0]) for a in AGES}; tl = {a: cl[a] * Pf(a, *th[1:]) for a in AGES}
    p7 = sum(tl[a] for a in range(7, 32)) / sum(cl[a] for a in range(7, 32)); p06 = sum(tl[a] for a in range(7)) / sum(cl[a] for a in range(7))
    d = (mix(FLm(2025), th)['tlf'] - mix(FLm(2019), th)['tlf']) * 100 / 6
    SENS.append((mm, tot / 1e3, s7, rr, p7, p06, d, v))
    print(f"  {mm:12.3f} {tot/1e3:6.0f} {s7:6.1%} | {rr:9.3f} {p7:6.1%} {p06:6.1%} | {d:+15.2f}   (fit loss {v:.0f})")

# ----------------------------------------------------------------------------------------------------- 3. WRITE
rows = []
for a in AGES:
    sE = S_EPA.get(a, (0.0, 0.0))                     # EPA table ends at 31; the stretched curve is still >0 to ~39
    rows.append([a, sE[0], sE[1], round(S_of(0, a, kc24), 4), round(S_of(1, a, kl24), 4),
                 MILES[min(a, 30)][0], MILES[min(a, 30)][1], round(Rf(a, lam), 4), round(Pf(a, pmin, pmax, c, s), 4),
                 round(F24.get(a, 0) / 1e3, 3), round(F24.get(a, 0) * Rf(a, lam) / sum(F24[b] * Rf(b, lam) for b in AGES), 4),
                 round(F24.get(a, 0) * Rf(a, lam) * Pf(a, pmin, pmax, c, s) / sum(F24[b] * Rf(b, lam) * Pf(b, pmin, pmax, c, s) for b in AGES), 4)])
write_csv('age_curves.csv',
          ["Mechanism A age curves (scripts/age_curves.py, 2026-09-14). S_epa_* = ORNL TEDB40 T3.15 raw; S_2024_* = stretched S(a/k) with "
           f"k_cars={kc24:.3f}, k_LT={kl24:.3f} (fitted: IHS 2013 census shape, then S&P 2024 counts: VIO 289M, 66% aged 7+); miles = T3.14;",
           f"R(a) = exposure(a) * exp(-{lam:.5f}*max(a-6,0)) [flat through age 6], exposure(0)={EXPO0}; P(a) = {pmin:.4f} + ({pmax:.4f}-{pmin:.4f})/(1+exp(-(a-{c:.3f})/{s:.3f})); both fitted jointly to 8 CCC 2024 statistics (see age_curves_validation.csv)",
           "fleet_2024_M = modelled light vehicles by age (end-2024). claims_share / tl_share = modelled 2024 distribution of claims and total losses by age."],
          ['age', 'S_epa_cars', 'S_epa_lt', 'S_2024_cars', 'S_2024_lt', 'miles_cars', 'miles_lt', 'R', 'P', 'fleet_2024_M', 'claims_share_2024', 'tl_share_2024'], rows)
val = [['fit', 2024, k, v, round(m24x[k], 4), q] for k, (v, sc, q) in TGT.items()]
val += [['out_of_sample', int(lab[:4]), lab, act, round(pred, 4), q] for lab, act, pred, q in oos]
val += [['S_check', 2024, 'avg age all light (t-MY+0.5)', 12.8, round(avg24, 2), 'S&P via CCC 2026 — NOT fitted; convention gap documented in docs/AGE_CURVES.md'], ['S_check', 2024, 'avg age cars', 14.5, round(avgc24, 2), 'S&P via CCC 2025/Q2 (not fitted)'],
        ['S_check', 2024, 'avg age light trucks', 11.9, round(avgl24, 2), 'S&P via CCC 2025/Q2 (not fitted)'], ['S_check', 2024, 'share 7+', 0.66, round(s7_24, 4), 'S&P via CCC 2024/Q4 (fitted)'],
        ['S_check', 2024, 'VIO light (M)', 289, round(tot24 / 1e3, 1), 'S&P ~289M light VIO 2025 release (fitted)'],
        ['S_check', 2025, 'change in <=6yr count vs 2020 (M)', -12, round((le6_25 - le6_20) / 1e3, 1), "CCC 2026 (Experian): 'over 12 million less newer vehicles (6 years old or newer)' vs 2020 — NOT reproducible from sales under any survival curve; definitional"],
        ['S_check', 2013, 'k cars (census fit)', '', round(KFIT[(2013, 'cars')], 3), 'IHS 2013 cars by age'], ['S_check', 2013, 'k trucks (census fit)', '', round(KFIT[(2013, 'trucks')], 3), 'IHS 2013 trucks by age (incl. heavy)'],
        ['S_check', 2000, 'k cars (census fit)', '', round(KFIT[(2000, 'cars')], 3), 'IHS 2000 cars by age'], ['S_check', 2000, 'k trucks (census fit)', '', round(KFIT[(2000, 'trucks')], 3), 'IHS 2000 trucks by age (incl. heavy)']]
val += [['sensitivity', 2024, f'k mult {mm:.3f}: VIO {tot:.0f}M, 7+ {s7:.1%}', '', f'R7+/0-6 {rr:.3f}; P7+ {p7:.3f}; P0-6 {p06:.3f}; drift {d:+.2f}pp/yr', 'R,P refitted under this survival drift'] for mm, tot, s7, rr, p7, p06, d, v in SENS]
val += [['bucket', 2024, lab, '', f'fleet {fw:.3f}; claims {cw:.3f}; TL {tw:.3f}; R {r:.3f}; P {p:.3f}; miles {mi:.0f}', 'model 2024'] for lab, fw, cw, tw, r, p, mi in BUCK]
write_csv('age_curves_validation.csv', ["Targets and model values for the age curves (scripts/age_curves.py, 2026-09-14). 'fit' rows were used to fit R,P; 'out_of_sample' rows were not."],
          ['kind', 'year', 'statistic', 'actual', 'model', 'source'], val)
