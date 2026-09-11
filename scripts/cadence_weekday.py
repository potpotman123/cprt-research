"""Window-robust cadence: accumulate each yard's SET OF SELLING WEEKDAYS per year.

A yard selling Tue+Thu reveals both weekdays across several snapshots regardless of how
far ahead any single snapshot looks. |weekday set| = sales per week.
Controls for the fact that more snapshots in a year discover more weekdays.
"""
import sqlite3,collections,datetime,statistics,csv,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
con=sqlite3.connect(ROOT/"data/cprt.db")
US=set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split())
rows=list(con.execute("SELECT snapshot_ts,yard_id,sale_date,state,location FROM sale_events WHERE sale_date IS NOT NULL"))
rows+=[("20260908120000",r[0],r[1],r[2],r[3]) for r in con.execute(
        "SELECT yard_id,sale_date,state,location FROM sale_events_live WHERE sale_date IS NOT NULL")]
rows=[r for r in rows if r[3] in US and not any(k in (r[4] or "").lower() for k in ("test","stage","demo"))]
snaps=sorted({r[0] for r in rows})
year_snaps=collections.defaultdict(list)
for s in snaps: year_snaps[s[:4]].append(s)
print("snapshots per year:", {y:len(v) for y,v in sorted(year_snaps.items())})
# --- control for snapshot count: subsample every year to the SAME number of snapshots ---
K=min(len(v) for v in year_snaps.values())
print(f"subsampling every year to K={K} snapshots (the min) to remove discovery bias\n")
def wkset(snapshot_list):
    d=collections.defaultdict(set)
    for ts,yard,sd,st,loc in rows:
        if ts in snapshot_list:
            d[yard].add(datetime.date.fromisoformat(sd).weekday())
    return d
print(f"{'year':<6}{'snaps':>6}{'yards':>7}{'mean wkdays/yard':>18}{'median':>8}{'>=2 days':>10}{'>=3 days':>10}")
out=[]
for y in sorted(year_snaps):
    sel=year_snaps[y][:K]                      # first K snapshots of the year
    d=wkset(set(sel))
    sizes=[len(v) for v in d.values() if v]
    if not sizes: continue
    m=statistics.mean(sizes); med=statistics.median(sizes)
    ge2=sum(1 for s in sizes if s>=2)/len(sizes)*100
    ge3=sum(1 for s in sizes if s>=3)/len(sizes)*100
    print(f"{y:<6}{len(sel):>6}{len(sizes):>7}{m:>18.3f}{med:>8.1f}{ge2:>9.1f}%{ge3:>9.1f}%")
    out.append((y,len(sel),len(sizes),round(m,4),med,round(ge2,2),round(ge3,2)))
con.execute("DROP TABLE IF EXISTS cadence_weekday")
con.execute("""CREATE TABLE cadence_weekday(year TEXT PRIMARY KEY,snapshots INT,yards INT,
  mean_weekdays REAL,median_weekdays REAL,pct_ge2 REAL,pct_ge3 REAL)""")
con.executemany("INSERT INTO cadence_weekday VALUES(?,?,?,?,?,?,?)",out); con.commit()
with open(ROOT/"data/csv/cadence_weekday.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["year","snapshots","yards","mean_weekdays","median_weekdays","pct_ge2","pct_ge3"]); w.writerows(out)
if len(out)>2:
    a,b=out[0],out[-1]
    print(f"\nmean selling-weekdays per yard: {a[0]}={a[3]:.3f} -> {b[0]}={b[3]:.3f}  ({(b[3]/a[3]-1)*100:+.1f}%)")
print("\n=== sanity: same-K weekday histogram, first vs last year ===")
for y in (out[0][0], out[-1][0]):
    d=wkset(set(year_snaps[y][:K]))
    h=collections.Counter(len(v) for v in d.values() if v)
    tot=sum(h.values())
    print(f"  {y}: "+"  ".join(f"{k}wd={v} ({v/tot*100:.0f}%)" for k,v in sorted(h.items())))
