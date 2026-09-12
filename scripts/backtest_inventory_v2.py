#!/usr/bin/env python3
"""Backtest the sitemap inventory nowcast against Copart's REPORTED US inventory YoY.

Supersedes scripts/backtest_final.py, which regressed on `inventory_level` — the SUM of page
counts. Pages overlap when out of sync, so the sum overcounts by up to 14.8% and the overcount
varies by capture. This version uses `inventory_v2` (UNION across pages) and treats cross-page
overlap as a QUALITY GATE rather than a nuisance.

THE HEADLINE RESULT: the gate is the entire difference between a useless series and a good one.
  all complete months, union      n=11  r=0.83  MAE 6.85pp
  overlap <= 1% only              n= 4  r=0.99  MAE 1.69pp
Every large error in the ungated run traces to ONE bad base capture (Jun-2023, 6.69% overlap),
which undercounts the denominator and inflates three YoY pairs by +11 to +25pp.

AND THE CATCH: the gate leaves 4 usable pairs. High r on n=4 is not evidence of skill. The
honest summary is that the method works when the capture is in sync and is unusable when it is
not, and that we can tell which is which BEFORE looking at the answer — overlap is observable at
collection time. That is the defensible claim; "r=0.99" is not.

Usage:  ./.venv/bin/python scripts/backtest_inventory_v2.py
"""
import sqlite3, glob, re, datetime, statistics as st, csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
con = sqlite3.connect(ROOT / "data/cprt.db")

# Capture dates come from the archived filename timestamp, not the sitemap's own lastmod
# (lastmod is a rebuild stamp, not a listing date — see findings.md Addendum 6).
cap = {}
for f in glob.glob(str(ROOT / "raw/lotxml/lotxml_p1_*.xml")):
    ts = re.search(r"_(\d{14})", f).group(1)
    cap[ts[:6]] = datetime.date(int(ts[:4]), int(ts[4:6]), int(ts[6:8]))
cap["202609"] = datetime.date(2026, 9, 8)          # live collector, first full capture

inv = {}
for m, u, ov, comp, us in con.execute(
        "SELECT month,union_lots,overlap_pct,complete,usable FROM inventory_v2"):
    inv[m] = (int(u), float(ov), int(comp), int(us))
inv["202609"] = (145108, 0.11, 1, 1)

rep = {q: v for q, v in con.execute(
    "SELECT fiscal_q,us_inventory_yoy FROM reported_units") if v is not None}
rep["FY2026 Q4"] = -3.4                             # stated on the 2026-09-10 call

QE = []
for y in range(2022, 2028):
    QE += [(datetime.date(y, 7, 31), f"FY{y} Q4"), (datetime.date(y, 10, 31), f"FY{y+1} Q1"),
           (datetime.date(y+1, 1, 31), f"FY{y+1} Q2"), (datetime.date(y+1, 4, 30), f"FY{y+1} Q3")]

def nearest_quarter(d, tol=45):
    b = min(QE, key=lambda x: abs((x[0] - d).days)); off = abs((b[0] - d).days)
    return (b[1], off) if off <= tol else (None, None)

def build(months):
    """YoY pairs 330-400 days apart whose end date sits within 45d of a fiscal quarter end."""
    out = []
    for i, m2 in enumerate(months):
        for m1 in months[:i]:
            gap = (cap[m2] - cap[m1]).days
            if 330 <= gap <= 400:
                q, off = nearest_quarter(cap[m2])
                if q and q in rep:
                    out.append(dict(frm=m1, to=m2, gap=gap, ours=100*(inv[m2][0]/inv[m1][0]-1),
                                    q=q, off=off, rep=rep[q],
                                    ov_base=inv[m1][1], ov_end=inv[m2][1]))
    return out

def fit(pairs):
    X = [p["rep"] for p in pairs]; Y = [p["ours"] for p in pairs]; n = len(X)
    mx, my = st.mean(X), st.mean(Y)
    sxy = sum((a-mx)*(b-my) for a, b in zip(X, Y)); sxx = sum((a-mx)**2 for a in X); syy = sum((b-my)**2 for b in Y)
    r = sxy/(sxx*syy)**.5; beta = sxy/sxx
    return dict(n=n, r=r, beta=beta, alpha=my-beta*mx)

def report(label, months, holdout=None):
    pairs = build(months)
    if len(pairs) < 3:
        print(f"\n=== {label} ===\n  only {len(pairs)} pairs — cannot fit"); return None
    tr = [p for p in pairs if p["q"] != holdout]; te = [p for p in pairs if p["q"] == holdout]
    f = fit(tr); a, b = f["alpha"], f["beta"]
    print(f"\n=== {label} ===")
    print(f"{'base':<8}{'end':<8}{'gap':>5}{'ovl base':>9}{'ours raw':>10}{'quarter':>12}{'reported':>10}{'raw err':>9}{'calib':>9}{'cal err':>9}")
    for p in pairs:
        c = (p["ours"]-a)/b
        print(f"{p['frm']:<8}{p['to']:<8}{p['gap']:>5}{p['ov_base']:>8.2f}%{p['ours']:>+9.2f}%"
              f"{p['q']:>12}{p['rep']:>+9.1f}%{p['ours']-p['rep']:>+9.2f}{c:>+8.2f}%{c-p['rep']:>+9.2f}"
              f"{'   <-- HELD OUT' if p['q']==holdout else ''}")
    print(f"  fit n={f['n']}  r={f['r']:.3f}  R2={f['r']**2:.3f}  beta={b:.2f} (our swing is {b:.2f}x reported)  alpha={a:+.2f}pp")
    print(f"  in-sample MAE: raw {st.mean(abs(p['ours']-p['rep']) for p in tr):.2f}pp  |  calibrated {st.mean(abs((p['ours']-a)/b-p['rep']) for p in tr):.2f}pp")
    for p in te:
        print(f"  OUT-OF-SAMPLE {p['q']}: raw {p['ours']:+.2f}% (err {p['ours']-p['rep']:+.2f}pp)  |  "
              f"calibrated {(p['ours']-a)/b:+.2f}% (err {(p['ours']-a)/b-p['rep']:+.2f}pp)  |  actual {p['rep']:+.1f}%")
    return pairs

complete = sorted(m for m in inv if m in cap and inv[m][2] == 1)
gated    = sorted(m for m in inv if m in cap and inv[m][3] == 1)
print(f"months with all 4 pages captured: {len(complete)}   passing the overlap<=1% gate: {len(gated)}")
print(f"gated: {gated}")

report("A. ALL complete months (union counts, no quality gate)", complete)
pairs = report("B. QUALITY-GATED (cross-page overlap <= 1%)", gated)
report("C. QUALITY-GATED, FY2026 Q4 held out — the only true forward test", gated, holdout="FY2026 Q4")

if pairs:
    with open(ROOT / "data/csv/backtest_inventory_v2.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["base_month", "end_month", "gap_days", "overlap_base_pct", "overlap_end_pct",
                    "ours_yoy_pct", "fiscal_q", "days_off_quarter_end", "reported_yoy_pct", "error_pp"])
        for p in pairs:
            w.writerow([p["frm"], p["to"], p["gap"], p["ov_base"], p["ov_end"],
                        round(p["ours"], 2), p["q"], p["off"], p["rep"], round(p["ours"]-p["rep"], 2)])
    print("\n-> data/csv/backtest_inventory_v2.csv")
