"""Lot-ID issuance clock, REDONE.

v1 used max(lot_id) as the frontier. That was wrong: max sits in a sparse legacy tail
(>86M, median consecutive gap 4,100) not the dense working region (46-68M, median gap 80).
v2 uses robust high-percentile estimators of the DENSE region, and only in-sync captures
(cross-page overlap <=5%) so pagination artifacts do not contaminate the ID set.
"""
import re,glob,sqlite3,datetime,statistics,csv,pathlib,math
ROOT=pathlib.Path(__file__).resolve().parent.parent
rx=re.compile(r'/lot/(\d+)')
con=sqlite3.connect(ROOT/"data/cprt.db")
ok={m for m,ov,c in con.execute("SELECT month,overlap_pct,complete FROM inventory_v2") if c=='1' and float(ov)<=5.0}
def ids_for(mo):
    s=set()
    for f in glob.glob(str(ROOT/f"raw/lotxml/lotxml_p*_{mo}*.xml")):
        for m in rx.finditer(open(f,encoding="utf-8",errors="replace").read()):
            v=int(m.group(1))
            if 1_000_000<=v<100_000_000: s.add(v)
    return sorted(s)
def date_for(mo):
    fs=sorted(glob.glob(str(ROOT/f"raw/lotxml/lotxml_p1_{mo}*.xml"))) or sorted(glob.glob(str(ROOT/f"raw/lotxml/lotxml_p*_{mo}*.xml")))
    ts=re.search(r'_(\d{14})',fs[0]).group(1)
    return datetime.date(int(ts[:4]),int(ts[4:6]),int(ts[6:8]))
rows=[]
for mo in sorted(ok):
    ids=ids_for(mo)
    if len(ids)<10000: continue
    n=len(ids)
    est={"max":ids[-1],
         "p999":ids[int(n*0.999)-1],
         "p99":ids[int(n*0.99)-1],
         "p95":ids[int(n*0.95)-1],
         "p90":ids[int(n*0.90)-1]}
    rows.append((mo,date_for(mo),n,est))
# add today's live snapshot
live=sorted({r[0] for r in con.execute("""SELECT lot_id FROM lot_snapshots
   WHERE snapshot_utc=(SELECT max(snapshot_utc) FROM lot_snapshots) AND lot_id<100000000""")})
if live:
    n=len(live)
    rows.append(("202609L",datetime.date(2026,9,9),n,
       {"max":live[-1],"p999":live[int(n*0.999)-1],"p99":live[int(n*0.99)-1],
        "p95":live[int(n*0.95)-1],"p90":live[int(n*0.90)-1]}))
print(f"{'month':<9}{'date':<12}{'n':>8}" + "".join(f"{k:>13}" for k in ("max","p999","p99","p95","p90")))
for mo,d,n,e in rows:
    print(f"{mo:<9}{str(d):<12}{n:>8,}" + "".join(f"{e[k]:>13,}" for k in ("max","p999","p99","p95","p90")))
def reg(xs,ys):
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    sxy=sum((a-mx)*(b-my) for a,b in zip(xs,ys)); sxx=sum((a-mx)**2 for a in xs); syy=sum((b-my)**2 for b in ys)
    b=sxy/sxx; a=my-b*mx; r=sxy/(sxx*syy)**.5
    return a,b,r
t0=rows[0][1]
print(f"\n=== which estimator is the cleanest clock? (regress on days since {t0}) ===")
print(f"  {'estimator':<10}{'slope IDs/day':>15}{'IDs/yr':>13}{'r':>9}{'R2':>8}{'monotone steps':>16}")
best=None
for k in ("max","p999","p99","p95","p90"):
    xs=[(d-t0).days for _,d,_,_ in rows]; ys=[e[k] for _,_,_,e in rows]
    a,b,r=reg(xs,ys)
    mono=sum(1 for u,v in zip(ys,ys[1:]) if v>=u)
    print(f"  {k:<10}{b:>15,.0f}{b*365:>13,.0f}{r:>+9.4f}{r*r:>8.4f}{f'{mono}/{len(ys)-1}':>16}")
    if best is None or r*r>best[1]: best=(k,r*r,b)
print(f"\n  cleanest: {best[0]}  (R2={best[1]:.4f}, {best[2]*365:,.0f} IDs/yr)")
con2=sqlite3.connect(ROOT/"data/cprt.db",timeout=60)
con2.execute("DROP TABLE IF EXISTS id_clock_v2")
con2.execute("""CREATE TABLE id_clock_v2(month TEXT,capture_date TEXT,n_ids INT,
  max_id INT,p999 INT,p99 INT,p95 INT,p90 INT)""")
con2.executemany("INSERT INTO id_clock_v2 VALUES(?,?,?,?,?,?,?,?)",
  [(mo,str(d),n,e["max"],e["p999"],e["p99"],e["p95"],e["p90"]) for mo,d,n,e in rows])
con2.commit()
with open(ROOT/"data/csv/id_clock_v2.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["month","capture_date","n_ids","max_id","p999","p99","p95","p90"])
    w.writerows([(mo,str(d),n,e["max"],e["p999"],e["p99"],e["p95"],e["p90"]) for mo,d,n,e in rows])
print(f"\n{len(rows)} captures -> data/csv/id_clock_v2.csv")
