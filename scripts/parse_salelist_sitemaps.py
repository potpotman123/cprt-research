import re,glob,sqlite3,csv,pathlib,collections,datetime,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parent.parent
rx=re.compile(r'/saleListResult/(\d+)(?:/(\d{4}-\d{2}-\d{2}))?\?location=([^&<]+)&(?:amp;)?saleDate=([^<&]+)')
rows=[]
for f in sorted(glob.glob(str(ROOT/"raw/wayback/copart_com_sale_list_results_xml_*.xml"))):
    ts=re.search(r'_(\d{14})\.xml$',f).group(1)
    snap=datetime.datetime.strptime(ts,"%Y%m%d%H%M%S").strftime("%Y-%m-%dT%H:%M:%SZ")
    txt=open(f,encoding="utf-8",errors="replace").read()
    seen=set()
    for m in rx.finditer(txt):
        yard=int(m.group(1)); sd=m.group(2); loc=urllib.parse.unquote(m.group(3)).strip()
        epoch=m.group(4)
        st,city=(loc.split(" - ",1)+[None])[:2] if " - " in loc else (None,loc)
        key=(yard,sd,loc)
        if key in seen: continue
        seen.add(key)
        rows.append((snap,ts,yard,sd,st,city,loc,None if epoch=="Future" else int(epoch)))
print(f"parsed {len(rows):,} rows from {len(set(r[1] for r in rows))} snapshots")
con=sqlite3.connect(ROOT/"data/cprt.db")
con.execute("DROP TABLE IF EXISTS sale_events")
con.execute("""CREATE TABLE sale_events(snapshot_utc TEXT,snapshot_ts TEXT,yard_id INT,
  sale_date TEXT,state TEXT,city TEXT,location TEXT,sale_epoch_ms INT)""")
con.executemany("INSERT INTO sale_events VALUES(?,?,?,?,?,?,?,?)",rows)
con.execute("CREATE INDEX IF NOT EXISTS ix_se ON sale_events(snapshot_ts,yard_id)")
con.commit()
with open(ROOT/"data/csv/sale_events.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["snapshot_utc","snapshot_ts","yard_id","sale_date","state","city","location","sale_epoch_ms"]); w.writerows(rows)
print(f"\n{'snapshot':<12}{'yards':>7}{'dated_events':>14}{'events/yard':>13}{'states':>8}")
panel=[]
for ts in sorted(set(r[1] for r in rows)):
    sub=[r for r in rows if r[1]==ts]
    yards={r[2] for r in sub}; dated=[r for r in sub if r[3]]
    states={r[4] for r in sub if r[4]}
    epy=len(dated)/len(yards) if yards else 0
    print(f"{ts[:8]:<12}{len(yards):>7}{len(dated):>14}{epy:>13.2f}{len(states):>8}")
    panel.append((ts[:8],len(yards),len(dated),round(epy,3),len(states)))
with open(ROOT/"data/csv/yard_panel.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["snapshot","yards","dated_sale_events","events_per_yard","states"]); w.writerows(panel)
con.execute("DROP TABLE IF EXISTS yard_panel")
con.execute("CREATE TABLE yard_panel(snapshot TEXT PRIMARY KEY,yards INT,dated_sale_events INT,events_per_yard REAL,states INT)")
con.executemany("INSERT INTO yard_panel VALUES(?,?,?,?,?)",panel); con.commit()
print("\n=== yard roster: first/last seen (top 12 by id) ===")
fs=collections.defaultdict(lambda:[None,None,None])
for snap,ts,yard,sd,st,city,loc,ep in rows:
    e=fs[yard]
    if e[0] is None or ts<e[0]: e[0]=ts
    if e[1] is None or ts>e[1]: e[1]=ts
    e[2]=loc
for y in sorted(fs)[:12]: print(f"  yard {y:<6} {fs[y][2]:<28} first={fs[y][0][:8]} last={fs[y][1][:8]}")
print(f"\ntotal distinct yards ever seen: {len(fs)}")
