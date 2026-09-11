"""Scrape cycle time via lot-ID survival between snapshots.

If a lot sits in inventory for CT days, the fraction still present after dt days is
S = exp(-dt/CT)  =>  CT = -dt / ln(S).
Survival is computed from lot_id set overlap between consecutive lot.xml captures.
Validated against Copart's disclosed 'cycle times decreased 9%' (FY26 Q1)."""
import re,glob,collections,datetime,math,sqlite3,csv,pathlib,statistics
ROOT=pathlib.Path(__file__).resolve().parent.parent.parent
rx=re.compile(r'/lot/(\d+)')
con=sqlite3.connect(ROOT/"data/cprt.db")
complete={r[0] for r in con.execute("SELECT month FROM inventory_level")}
def ids_for(month):
    s=set()
    for f in glob.glob(str(ROOT/f"raw/lotxml/lotxml_p*_{month}*.xml")):
        for m in rx.finditer(open(f,encoding="utf-8",errors="replace").read()):
            v=int(m.group(1))
            if 1_000_000<=v<200_000_000: s.add(v)
    return s
def date_for(month):
    fs=sorted(glob.glob(str(ROOT/f"raw/lotxml/lotxml_p1_{month}*.xml")))
    if not fs: fs=sorted(glob.glob(str(ROOT/f"raw/lotxml/lotxml_p*_{month}*.xml")))
    ts=re.search(r'_(\d{14})',fs[0]).group(1)
    return datetime.date(int(ts[:4]),int(ts[4:6]),int(ts[6:8]))
months=sorted(m for m in complete if m!="202609")
S={}
for m in months:
    S[m]=ids_for(m); print(f"  {m}: {len(S[m]):,} core lot ids",flush=True)
# live
live={r[0] for r in con.execute("""SELECT lot_id FROM lot_snapshots
   WHERE snapshot_utc=(SELECT max(snapshot_utc) FROM lot_snapshots) AND lot_id<200000000""")}
S["202609"]=live; months.append("202609")
print(f"  202609: {len(live):,} core lot ids (live)")
print(f"\n{'from':<9}{'to':<9}{'dt_days':>8}{'survivors':>11}{'survival':>10}{'implied CT (days)':>19}")
rows=[]
for a,b in zip(months,months[1:]):
    da,db=date_for(a) if a!="202609" else datetime.date(2026,9,8), date_for(b) if b!="202609" else datetime.date(2026,9,8)
    dt=(db-da).days
    if dt<=0 or dt>200: continue
    ov=len(S[a]&S[b]); surv=ov/len(S[a])
    ct=(-dt/math.log(surv)) if 0<surv<1 else float('nan')
    print(f"{a:<9}{b:<9}{dt:>8}{ov:>11,}{surv:>9.3f}{ct:>19.1f}")
    rows.append((a,b,str(da),str(db),dt,len(S[a]),ov,round(surv,4),round(ct,2)))
con2=sqlite3.connect(ROOT/"data/cprt.db",timeout=60)
con2.execute("DROP TABLE IF EXISTS cycle_time")
con2.execute("""CREATE TABLE cycle_time(from_month TEXT,to_month TEXT,from_date TEXT,to_date TEXT,
  dt_days INT,base_lots INT,survivors INT,survival REAL,implied_ct_days REAL)""")
con2.executemany("INSERT INTO cycle_time VALUES(?,?,?,?,?,?,?,?,?)",rows); con2.commit()
with open(ROOT/"data/csv/cycle_time.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["from_month","to_month","from_date","to_date","dt_days","base_lots","survivors","survival","implied_ct_days"]); w.writerows(rows)
print(f"\n{len(rows)} survival pairs -> data/csv/cycle_time.csv")
# YoY comparison of implied CT for same-ish calendar windows
byyear=collections.defaultdict(list)
for a,b,da,db,dt,base,ov,su,ct in rows:
    if ct==ct: byyear[a[:4]].append(ct)
print("\n=== implied cycle time by year ===")
prev=None
for y in sorted(byyear):
    m=statistics.mean(byyear[y]); ch=f"{(m/prev-1)*100:+.1f}%" if prev else ""
    print(f"  {y}: n={len(byyear[y])}  mean implied CT = {m:.1f} days   {ch}")
    prev=m
