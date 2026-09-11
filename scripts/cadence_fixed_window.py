"""Sales per week, measured in a FIXED 7-day window from each snapshot date.

Every snapshot's lookahead is >=18 days (verified), so a 7-day window is FULLY observed
in all 26 snapshots. That makes the count directly comparable across time and immune to
the shortening publication window that confounded mean-gap and events/yard.
"""
import sqlite3,collections,datetime,statistics,csv,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
con=sqlite3.connect(ROOT/"data/cprt.db")
US=set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split())
rows=list(con.execute("SELECT snapshot_ts,yard_id,sale_date,state,location FROM sale_events WHERE sale_date IS NOT NULL"))
rows+=[("20260908120000",r[0],r[1],r[2],r[3]) for r in con.execute(
        "SELECT yard_id,sale_date,state,location FROM sale_events_live WHERE sale_date IS NOT NULL")]
rows=[r for r in rows if r[3] in US and not any(k in (r[4] or "").lower() for k in ("test","stage","demo"))]
by=collections.defaultdict(list)
for ts,y,sd,st,loc in rows: by[ts].append((y,datetime.date.fromisoformat(sd)))
W=7
print(f"fixed window = {W} days from snapshot date\n")
print(f"{'snapshot':<11}{'yards':>7}{'sales in wk':>13}{'sales/yard/wk':>15}{'%yards 0':>10}{'%yards>=2':>11}")
out=[]
for ts in sorted(by):
    snap=datetime.date(int(ts[:4]),int(ts[4:6]),int(ts[6:8]))
    hi=snap+datetime.timedelta(days=W)
    per=collections.defaultdict(set)
    yards=set()
    for y,d in by[ts]:
        yards.add(y)
        if snap<=d<hi: per[y].add(d)
    n_sales=sum(len(v) for v in per.values())
    spw=n_sales/len(yards)
    z=sum(1 for y in yards if len(per.get(y,()))==0)/len(yards)*100
    g2=sum(1 for y in yards if len(per.get(y,()))>=2)/len(yards)*100
    print(f"{ts[:8]:<11}{len(yards):>7}{n_sales:>13}{spw:>15.4f}{z:>9.1f}%{g2:>10.1f}%")
    out.append((ts[:8],len(yards),n_sales,round(spw,5),round(z,2),round(g2,2)))
con.execute("DROP TABLE IF EXISTS cadence_fixed")
con.execute("""CREATE TABLE cadence_fixed(snapshot TEXT PRIMARY KEY,yards INT,sales_in_window INT,
  sales_per_yard_per_week REAL,pct_yards_zero REAL,pct_yards_ge2 REAL)""")
con.executemany("INSERT INTO cadence_fixed VALUES(?,?,?,?,?,?)",out); con.commit()
with open(ROOT/"data/csv/cadence_fixed.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["snapshot","yards","sales_in_window","sales_per_yard_per_week","pct_yards_zero","pct_yards_ge2"]); w.writerows(out)
ys=[r[3] for r in out]; xs=list(range(len(ys)))
mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
sl=sum((a-mx)*(b-my) for a,b in zip(xs,ys))/sum((a-mx)**2 for a in xs)
ssr=sum((b-(my+sl*(a-mx)))**2 for a,b in zip(xs,ys)); sst=sum((b-my)**2 for b in ys)
print(f"\nsales/yard/week: first={ys[0]:.4f}  last={ys[-1]:.4f}  change={(ys[-1]/ys[0]-1)*100:+.2f}%")
print(f"  OLS slope={sl:+.5f}/snapshot   R^2={1-ssr/sst:.4f}")
print(f"  min={min(ys):.4f} max={max(ys):.4f} mean={statistics.mean(ys):.4f} stdev={statistics.stdev(ys):.4f}")
# total US sale capacity = yards x sales/yard/week
print(f"\n=== TOTAL weekly US sale events (yards x cadence) ===")
for r in out: print(f"  {r[0]}: {r[1]:>4} yards x {r[3]:.3f} = {r[2]:>4} sale events/week")
print(f"\n  total sale events/week: {out[0][2]} ({out[0][0]}) -> {out[-1][2]} ({out[-1][0]})  {(out[-1][2]/out[0][2]-1)*100:+.2f}%")
