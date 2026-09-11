import sqlite3,csv,pathlib,collections,statistics
ROOT=pathlib.Path(__file__).resolve().parent.parent
con=sqlite3.connect(ROOT/"data/cprt.db")
rows=con.execute("SELECT snapshot_ts,yard_id,sale_date,state,city,location FROM sale_events").fetchall()
US=set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split())
def bad(loc,st): 
    l=(loc or "").lower()
    return ("test" in l or "stage" in l or "demo" in l or st not in US)
clean=[r for r in rows if not bad(r[5],r[3])]
print(f"rows: {len(rows):,} -> US operating yards only: {len(clean):,}  (dropped {len(rows)-len(clean):,})")
snaps=sorted({r[0] for r in clean})
print(f"\n{'snapshot':<11}{'US yards':>9}{'dated ev':>9}{'ev/yard':>9}{'states':>7}{'yard chg':>9}")
panel=[]; prev=None
for ts in snaps:
    sub=[r for r in clean if r[0]==ts]
    yards={r[1] for r in sub}; dated=[r for r in sub if r[2]]
    epy=len(dated)/len(yards)
    chg="" if prev is None else f"{len(yards)-prev:+d}"
    print(f"{ts[:8]:<11}{len(yards):>9}{len(dated):>9}{epy:>9.3f}{len({r[3] for r in sub}):>7}{chg:>9}")
    panel.append((ts[:8],len(yards),len(dated),round(epy,4),len({r[3] for r in sub})))
    prev=len(yards)
with open(ROOT/"data/csv/yard_panel_us.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["snapshot","us_yards","dated_events","events_per_yard","states"]); w.writerows(panel)
con.execute("DROP TABLE IF EXISTS yard_panel_us")
con.execute("CREATE TABLE yard_panel_us(snapshot TEXT PRIMARY KEY,us_yards INT,dated_events INT,events_per_yard REAL,states INT)")
con.executemany("INSERT INTO yard_panel_us VALUES(?,?,?,?,?)",panel); con.commit()
first=snaps[0]; last=snaps[-1]
y0={r[1] for r in clean if r[0]==first}; y1={r[1] for r in clean if r[0]==last}
locs={r[1]:r[5] for r in clean}
print(f"\n=== yard roster change {first[:8]} -> {last[:8]} ===")
print(f"ADDED ({len(y1-y0)}): "+", ".join(f"{y}:{locs.get(y)}" for y in sorted(y1-y0)))
print(f"DROPPED ({len(y0-y1)}): "+", ".join(f"{y}:{locs.get(y)}" for y in sorted(y0-y1)))
# trend
ep=[p[3] for p in panel]
n=len(ep); xs=list(range(n)); mx=sum(xs)/n; my=sum(ep)/n
slope=sum((x-mx)*(y-my) for x,y in zip(xs,ep))/sum((x-mx)**2 for x in xs)
print(f"\nevents/yard: first={ep[0]:.3f} last={ep[-1]:.3f} peak={max(ep):.3f} min={min(ep):.3f}")
print(f"  OLS slope per snapshot = {slope:+.5f}  (~{slope*len(ep)/((int(last[:4])-int(first[:4]))+ (int(last[4:6])-int(first[4:6]))/12):+.4f}/yr)")
print(f"  total change {(ep[-1]/ep[0]-1)*100:+.2f}%  over {first[:6]}->{last[:6]}")
# state distribution latest
st=collections.Counter(r[3] for r in clean if r[0]==last)
uy=collections.defaultdict(set)
for r in clean:
    if r[0]==last: uy[r[3]].add(r[1])
print("\n=== yards by state (latest snapshot), top 15 ===")
for s,c in sorted(uy.items(),key=lambda x:-len(x[1]))[:15]: print(f"  {s}: {len(c)} yards")
