"""Backtest: does sitemap-derived total inventory track Copart's reported volume?

Reported comparables (from earnings calls / third-party, NOT in EDGAR filings):
  Q3 FY26 (qtr ended 2026-04-30): US inventory -4.7%, US insurance units -4.2%,
                                  global insurance units -2.7%
  FY26 insurance units YoY (third party): Q1 -7.3%, Q2 -4.8%, Q3 -3.1%
Copart fiscal quarters end Oct 31 / Jan 31 / Apr 30 / Jul 31.
"""
import sqlite3,csv,datetime,pathlib,statistics
ROOT=pathlib.Path(__file__).resolve().parent.parent
con=sqlite3.connect(ROOT/"data/cprt.db")
rows=[dict(zip([c[0] for c in con.execute("SELECT * FROM inventory_panel LIMIT 1").description],r))
      for r in con.execute("SELECT * FROM inventory_panel ORDER BY month")]
def tot(r): return int(r["total_lots"]) if r["total_lots"] not in (None,"","None") else None
series=[(r["month"],tot(r)) for r in rows if tot(r)]
# append today's live total
live=con.execute("SELECT count(*) FROM lot_snapshots WHERE snapshot_utc=(SELECT max(snapshot_utc) FROM lot_snapshots)").fetchone()[0]
series.append(("202609",live))
print("=== TOTAL INVENTORY LEVEL (all lot.xml pages summed) ===")
print(f"{'month':<9}{'total lots':>12}{'MoM':>10}{'YoY':>10}")
d={m:v for m,v in series}
for m,v in series:
    y=str(int(m[:4])-1)+m[4:]
    prev=[x for x in series if x[0]<m]
    mom=f"{(v/prev[-1][1]-1)*100:+.2f}%" if prev else ""
    yoy=f"{(v/d[y]-1)*100:+.2f}%" if y in d else ""
    print(f"{m:<9}{v:>12,}{mom:>10}{yoy:>10}")
print("\n=== BACKTEST vs reported ===")
REPORTED={"202604":{"us_inventory":-4.7,"us_ins_units":-4.2,"global_ins_units":-2.7,"tp_units":-3.1},
          "202601":{"tp_units":-4.8},"202510":{"tp_units":-7.3}}
hit=0;tot_n=0
for m,rep in sorted(REPORTED.items()):
    y=str(int(m[:4])-1)+m[4:]
    if m in d and y in d:
        obs=(d[m]/d[y]-1)*100
        for k,v in rep.items():
            tot_n+=1; err=obs-v
            flag="MATCH" if abs(err)<2.0 else "miss"
            if flag=="MATCH": hit+=1
            print(f"  {m}  observed inv YoY={obs:+.2f}%   reported {k}={v:+.2f}%   err={err:+.2f}pp  {flag}")
    else:
        print(f"  {m}  NO COMPARABLE: need complete months for {m} and {y} (have {m in d}/{y in d})")
if tot_n: print(f"\n  {hit}/{tot_n} within 2pp")
else: print("\n  BACKTEST NOT RUNNABLE - insufficient complete month pairs.")
with open(ROOT/"data/csv/inventory_level.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["month","total_lots"]); w.writerows(series)
print(f"\n{len(series)} usable months -> data/csv/inventory_level.csv")
