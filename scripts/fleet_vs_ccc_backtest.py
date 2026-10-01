#!/usr/bin/env python3
"""Backtest: does the fleet roll's claims-weighted age x body composition reproduce the claim mix implied by the
owner-supplied CCC workbook (Data for Harvard Research, Daniella Biblin, 9.29.2026; SHA 2a127900...) for 2020-2025?
CCC-implied claim share of cell = (tl_mix / tlf) normalised. Model claim share = Fleet(age, body, year) x R(age), normalised,
with Fleet from candidate_body_births.csv x EPA survival stretched by k_body x m(year) (docs/AGE_CURVES.md), and
R(a) = exposure(a) x exp(-0.09027 x max(a-6, 0)), exposure(0) = 0.5 (data/csv/age_curves.csv header).
2025 is the model's calibration anchor (claim weights backed out of these cells); 2020-2024 are NOT calibrated and are the test.
Writes docs/source_trace_2026-10-01/fleet_vs_ccc_claim_mix.csv. MEASURED by this script; conventions reconstructed, see README."""
import csv, math, collections, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
K13 = {'Car': 1.064, 'LT': 0.921}           # fitted to IHS 2013 census (AGE_CURVES.md s.2.3)
def kmult(year):                              # linear 1.000 (2013) -> 1.194 (2024), held after 2024
    return 1.0 + (1.194 - 1.0) * min(max(year - 2013, 0), 11) / 11
surv = {}
for r in csv.DictReader(l for l in open(ROOT/'data/csv/ornl_tedb40_survival_by_age.csv') if not l.startswith('#')):
    surv[int(float(r['age']))] = (float(r['survival_cars']), float(r['survival_light_trucks']))
AMAX = max(surv)
def S(a, k, idx):
    x = a / k
    if x >= AMAX: return surv[AMAX][idx] * (0.0 if x > AMAX + 5 else 1.0)
    i = int(math.floor(x)); f = x - i
    return surv[i][idx] * (1 - f) + surv[min(i + 1, AMAX)][idx] * f
births = collections.defaultdict(dict)
for r in csv.DictReader(open(ROOT/'docs/historical_body_births_2026-09-28/candidate_body_births.csv')):
    births[r['body']][int(r['year'])] = float(r['births_thousands'])
def R(a): return (0.5 if a == 0 else 1.0) * math.exp(-0.09027 * max(a - 6, 0))
def group(a): return 0 if a == 0 else 1 if a <= 3 else 2 if a <= 6 else 3
BODY = {'Car': ('Car', 0), 'SUV': ('Utility Vehicle', 1), 'Pickup': ('Pickup', 1), 'Van': ('Van', 1)}
def model_mix(year, body_adj=None):
    m = collections.Counter(); fleet = collections.Counter()
    for b, (ccc, idx) in BODY.items():
        k = K13['Car' if b == 'Car' else 'LT'] * kmult(year)
        for a in range(0, 46):
            y0 = year - a
            if y0 not in births[b]: continue
            n = births[b][y0] * S(a, k, idx)
            fleet[(ccc, group(a))] += n
            m[(ccc, group(a))] += n * R(a) * (body_adj or {}).get(ccc, 1.0)
    tot = sum(m.values()); ftot = sum(fleet.values())
    return {c: v / tot for c, v in m.items()}, {c: v / ftot for c, v in fleet.items()}
ccc = collections.defaultdict(dict)
for r in csv.DictReader(open(ROOT/'model/ccc_age_body_2026-09-29/source_cells.csv')):
    ccc[int(r['year'])][(r['source_body'], int(r['age_group']))] = (float(r['tlf']), float(r['tl_mix']))
AGES = ['0 (current/newer)', '1-3', '4-6', '7+']; BODIES = ['Car', 'Pickup', 'Utility Vehicle', 'Van']
rows = []; summary = []
for year in sorted(ccc):
    raw = {c: tm / tlf for c, (tlf, tm) in ccc[year].items()}; s = sum(raw.values()); cimp = {c: v / s for c, v in raw.items()}
    mm, fm = model_mix(year)
    maxerr = 0
    for b in BODIES:
        for g in range(4):
            c = (b, g); e = mm.get(c, 0) - cimp[c]; maxerr = max(maxerr, abs(e))
            rows.append([year, b, AGES[g], round(cimp[c], 5), round(mm.get(c, 0), 5), round(e, 5), round(fm.get(c, 0), 5)])
    body_m = {b: sum(mm.get((b, g), 0) for g in range(4)) for b in BODIES}; body_c = {b: sum(cimp[(b, g)] for g in range(4)) for b in BODIES}
    age_m = {g: sum(mm.get((b, g), 0) for b in BODIES) for g in range(4)}; age_c = {g: sum(cimp[(b, g)] for b in BODIES) for g in range(4)}
    summary.append((year, body_c, body_m, age_c, age_m, maxerr))
out = ROOT/'docs/source_trace_2026-10-01/fleet_vs_ccc_claim_mix.csv'
with open(out, 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['year', 'body', 'age_group', 'ccc_implied_claim_share', 'model_claim_share', 'model_minus_ccc', 'model_fleet_share']); w.writerows(rows)
print('year | body share of claims: CCC-implied vs model (Car, Pickup, Utility, Van) | age-group share: CCC vs model (0,1-3,4-6,7+) | max cell |err|')
for year, bc, bm, ac, am, me in summary:
    print(f"{year} | " + ' '.join(f"{b[:3]} {bc[b]*100:4.1f}/{bm[b]*100:4.1f}" for b in BODIES) + ' | ' + ' '.join(f"{ac[g]*100:4.1f}/{am[g]*100:4.1f}" for g in range(4)) + f" | {me*100:4.1f}pp")
print('\n2025 grid, CCC-implied / model claim share (%), rows=body, cols=age group 0,1-3,4-6,7+:')
for b in BODIES:
    print(f"  {b:<16}" + ' '.join(f"{r[3]*100:5.1f}/{r[4]*100:5.1f}" for r in rows if r[0] == 2025 and r[1] == b))
print('\n2020 grid:')
for b in BODIES:
    print(f"  {b:<16}" + ' '.join(f"{r[3]*100:5.1f}/{r[4]*100:5.1f}" for r in rows if r[0] == 2020 and r[1] == b))
# change 2020->2025 in body share: does the roll reproduce the direction and size of the mix shift?
y0, y1 = summary[0], summary[-1]
print('\nChange 2020->2025 in body share of claims (pp): ' + ' '.join(f"{b[:3]} CCC {100*(y1[1][b]-y0[1][b]):+4.1f} / model {100*(y1[2][b]-y0[2][b]):+4.1f}" for b in BODIES))
print('Change 2020->2025 in age share of claims (pp): ' + ' '.join(f"{AGES[g]} CCC {100*(y1[3][g]-y0[3][g]):+4.1f} / model {100*(y1[4][g]-y0[4][g]):+4.1f}" for g in range(4)))

# ---- Variant: body-specific claims factors fitted to the 2025 anchor only; 2020-2024 out of sample ----
mm25, _ = model_mix(2025)
raw25 = {c: tm / tlf for c, (tlf, tm) in ccc[2025].items()}; s25 = sum(raw25.values()); c25 = {c: v / s25 for c, v in raw25.items()}
body_adj = {b: sum(c25[(b, g)] for g in range(4)) / sum(mm25.get((b, g), 0) for g in range(4)) for b in BODIES}
md = ['# Fleet roll versus the CCC age-and-type constraints, 1 October 2026', '',
 'Source: owner-supplied CCC workbook *Data for Harvard Research (Daniella Biblin) 9.29.2026* (SHA-256 2a127900…, identical to the file integrated 29 Sep). Script: `scripts/fleet_vs_ccc_backtest.py` (MEASURED). The CCC cells give, per body and age group, the share of claims declared a total loss and each cell\'s share of all total losses; dividing the second by the first gives the share of **claims** in each cell, which is what a fleet roll times a claims-propensity curve must reproduce.', '',
 'The Python engine already matches all 16 cells in 2025 by construction (claim weights are backed out of them). The test below is of the fleet roll itself: births × stretched EPA survival × the age-exposure curve, with nothing fitted to these cells except, in the second table, four body factors fitted to 2025 alone.', '',
 '## 1. Roll with one claims curve for all bodies (nothing fitted to CCC)', '',
 '| Year | Car CCC / model | Pickup | Utility | Van | Age 0 | 1–3 | 4–6 | 7+ | Max cell gap |', '|---|---|---|---|---|---|---|---|---|---|']
for year, bc, bm, ac, am, me in summary:
    md.append(f"| {year} | " + ' | '.join(f"{bc[b]*100:.1f} / {bm[b]*100:.1f}" for b in BODIES) + ' | ' + ' | '.join(f"{ac[g]*100:.1f} / {am[g]*100:.1f}" for g in range(4)) + f" | {me*100:.1f} pp |")
md += ['', 'Shares of claims, per cent. The roll puts cars about four points too low and utility vehicles about four points too high in every year, so cars claim more per vehicle on the road than SUVs; the age-group shares are within about 1.5 points except the newest group, where the half-year exposure assumption for age 0 looks too low.', '',
 '## 2. Same roll with body factors fitted to 2025 only (2020–2024 out of sample)', '',
 'Body factors (claims per vehicle relative to the common curve): ' + ', '.join(f"{b} {body_adj[b]:.3f}" for b in BODIES) + '.', '',
 '| Year | Car CCC / model | Pickup | Utility | Van | Age 0 | 1–3 | 4–6 | 7+ | Max cell gap |', '|---|---|---|---|---|---|---|---|---|---|']
summary2 = []
for year in sorted(ccc):
    raw = {c: tm / tlf for c, (tlf, tm) in ccc[year].items()}; s = sum(raw.values()); cimp = {c: v / s for c, v in raw.items()}
    mm, _ = model_mix(year, body_adj)
    me = max(abs(mm.get(c, 0) - cimp[c]) for c in cimp)
    bc = {b: sum(cimp[(b, g)] for g in range(4)) for b in BODIES}; bm = {b: sum(mm.get((b, g), 0) for g in range(4)) for b in BODIES}
    ac = {g: sum(cimp[(b, g)] for b in BODIES) for g in range(4)}; am = {g: sum(mm.get((b, g), 0) for b in BODIES) for g in range(4)}
    summary2.append((year, bc, bm, ac, am, me))
    md.append(f"| {year} | " + ' | '.join(f"{bc[b]*100:.1f} / {bm[b]*100:.1f}" for b in BODIES) + ' | ' + ' | '.join(f"{ac[g]*100:.1f} / {am[g]*100:.1f}" for g in range(4)) + f" | {me*100:.1f} pp |")
y0, y1 = summary[0], summary[-1]
md += ['', '## 3. Does the roll reproduce the 2020→2025 shift?', '',
 '| Shift 2020→2025, points of claim share | CCC | Roll |', '|---|---|---|']
for b in BODIES: md.append(f"| {b} | {100*(y1[1][b]-y0[1][b]):+.1f} | {100*(y1[2][b]-y0[2][b]):+.1f} |")
for g in range(4): md.append(f"| Age {AGES[g]} | {100*(y1[3][g]-y0[3][g]):+.1f} | {100*(y1[4][g]-y0[4][g]):+.1f} |")
md += ['', '## 4. Conclusion for the build', '',
 '- The fleet roll reproduces the direction and most of the size of the five-year shift in the claim mix (cars down ten points, utility vehicles up ten; the 7+ group up) without being fitted to it. That is a genuine out-of-sample check and it passes at the body level.',
 '- It understates the ageing shift (7+ up 6 points against 8; the 1–3 group down 3.5 against 5.5), so the roll is slightly too slow to age the claiming fleet. The births for 2021–2023 or the young-vehicle survival are the likely cause; this is the one place more precision would change a number.',
 '- Levels need body-specific claims factors (cars ≈ 1.11×, SUVs ≈ 0.92×). The engine\'s 2025 cell weights already embed these implicitly; the workbook should make them explicit inputs on E2, labelled CALIBRATED to the 2025 CCC cells, with the 2020–2024 comparison shown as the test.',
 '- E1 Fleet therefore gets a Checks block with this table live: model claim share minus CCC-implied share per cell and year, PASS if every cell is within 2 points and every body total within 1 point.']
(ROOT/'docs/source_trace_2026-10-01/FLEET_VS_CCC.md').write_text('\n'.join(md) + '\n')
print('\nbody factors from 2025:', {b: round(v, 3) for b, v in body_adj.items()})
for year, bc, bm, ac, am, me in summary2:
    print(f"{year} adj | " + ' '.join(f"{b[:3]} {bc[b]*100:4.1f}/{bm[b]*100:4.1f}" for b in BODIES) + ' | ' + ' '.join(f"{ac[g]*100:4.1f}/{am[g]*100:4.1f}" for g in range(4)) + f" | {me*100:4.1f}pp")
