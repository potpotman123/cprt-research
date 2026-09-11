"""Sales cadence, measured as the GAP between a yard's consecutive published sale dates.

Why this works where events/yard failed: the truncated lookahead affects HOW MANY dates
get published, but the interval between two published dates is the yard's actual schedule.
A yard selling Tue+Thu publishes a 2-day gap regardless of how far ahead the generator looks.
"""
import sqlite3,collections,datetime,statistics,csv,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent.parent
con=sqlite3.connect(ROOT/"data/cprt.db")
US=set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split())
def load():
    rows=list(con.execute("SELECT snapshot_ts,yard_id,sale_date,state,location FROM sale_events WHERE sale_date IS NOT NULL"))
    live=[( "20260908120000",r[0],r[1],r[2],r[3]) for r in con.execute(
        "SELECT yard_id,sale_date,state,location FROM sale_events_live WHERE sale_date IS NOT NULL")]
    return rows+live
rows=[r for r in load() if r[3] in US and "test" not in (r[4] or "").lower() and "stage" not in (r[4] or "").lower()]
by=collections.defaultdict(lambda: collections.defaultdict(list))
for ts,yard,sd,st,loc in rows: by[ts[:6]][yard].append(sd)
print(f"{'month':<8}{'yards':>7}{'y>=2dt':>8}{'gaps':>6}{'medGap':>8}{'meanGap':>9}{'wk_rate':>9}{'2x/wk%':>8}")
out=[]
for mo in sorted(by):
    gaps=[]; multi=0
    for yard,dates in by[mo].items():
        ds=sorted(set(datetime.date.fromisoformat(d) for d in dates))
        if len(ds)>=2:
            multi+=1
            for a,b in zip(ds,ds[1:]):
                g=(b-a).days
                if 1<=g<=21: gaps.append(g)
    if not gaps: continue
    med=statistics.median(gaps); mean=statistics.mean(gaps)
    # sales/week implied by the median gap
    wk=7.0/med if med else None
    twice=sum(1 for g in gaps if g<=4)/len(gaps)*100
    print(f"{mo:<8}{len(by[mo]):>7}{multi:>8}{len(gaps):>6}{med:>8.1f}{mean:>9.2f}{wk:>9.2f}{twice:>7.1f}%")
    out.append((mo,len(by[mo]),multi,len(gaps),med,round(mean,3),round(wk,4),round(twice,2)))
con.execute("DROP TABLE IF EXISTS cadence_panel")
con.execute("""CREATE TABLE cadence_panel(month TEXT PRIMARY KEY,yards INT,yards_multi INT,n_gaps INT,
  median_gap REAL,mean_gap REAL,implied_sales_per_week REAL,pct_gap_le4 REAL)""")
con.executemany("INSERT INTO cadence_panel VALUES(?,?,?,?,?,?,?,?)",out); con.commit()
with open(ROOT/"data/csv/cadence_panel.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["month","yards","yards_multi","n_gaps","median_gap","mean_gap","implied_sales_per_week","pct_gap_le4"]); w.writerows(out)
print(f"\n{len(out)} months -> data/csv/cadence_panel.csv")
print("\n=== gap distribution, first vs last snapshot ===")
for mo in (out[0][0], out[-1][0]):
    gg=collections.Counter()
    for yard,dates in by[mo].items():
        ds=sorted(set(datetime.date.fromisoformat(d) for d in dates))
        for a,b in zip(ds,ds[1:]):
            g=(b-a).days
            if 1<=g<=21: gg[g]+=1
    tot=sum(gg.values())
    print(f"  {mo}: "+"  ".join(f"{k}d={v}({v/tot*100:.0f}%)" for k,v in sorted(gg.items()))[:150])
# trend
if len(out)>3:
    ys=[r[6] for r in out]; xs=list(range(len(ys)))
    mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
    sl=sum((a-mx)*(b-my) for a,b in zip(xs,ys))/sum((a-mx)**2 for a in xs)
    print(f"\nimplied sales/week: first={ys[0]:.3f} last={ys[-1]:.3f} change={(ys[-1]/ys[0]-1)*100:+.2f}%")
    print(f"  OLS slope={sl:+.5f}/snapshot over {len(ys)} snapshots")
