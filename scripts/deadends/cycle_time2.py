"""Cycle-time proxy, dt-controlled and page-matched.

Survival is non-exponential, so implied CT is only comparable at matched dt.
Fix: compare the SAME sitemap page across consecutive captures (page 1 is always a
50,000-lot slice), which yields many more pairs incl. 2025-26, then restrict to dt~30d."""
import re,glob,collections,datetime,math,sqlite3,csv,pathlib,statistics
ROOT=pathlib.Path(__file__).resolve().parent.parent.parent
rx=re.compile(r'/lot/(\d+)')
def ids(path):
    s=set()
    for m in rx.finditer(open(path,encoding="utf-8",errors="replace").read()):
        v=int(m.group(1))
        if 1_000_000<=v<200_000_000: s.add(v)
    return s
byp=collections.defaultdict(dict)   # page -> date -> path
for f in glob.glob(str(ROOT/"raw/lotxml/lotxml_p*.xml")):
    m=re.search(r'lotxml_p(\d)_(\d{14})',f); pg=int(m.group(1)); ts=m.group(2)
    if pg==0: continue
    d=datetime.date(int(ts[:4]),int(ts[4:6]),int(ts[6:8]))
    byp[pg][d]=f
rows=[]
for pg in sorted(byp):
    ds=sorted(byp[pg])
    cache={}
    for a,b in zip(ds,ds[1:]):
        dt=(b-a).days
        if not (20<=dt<=45): continue
        if a not in cache: cache[a]=ids(byp[pg][a])
        if b not in cache: cache[b]=ids(byp[pg][b])
        A,B=cache[a],cache[b]
        if len(A)<10000: continue
        ov=len(A&B); su=ov/len(A)
        if not (0<su<1): continue
        ct=-dt/math.log(su)
        rows.append((pg,str(a),str(b),dt,len(A),ov,round(su,4),round(ct,2)))
rows.sort(key=lambda r:r[1])
print(f"{'pg':<3}{'from':<12}{'to':<12}{'dt':>4}{'base':>8}{'surv':>8}{'CT(d)':>8}  norm CT@30d")
for pg,a,b,dt,base,ov,su,ct in rows:
    ct30=-30/math.log(su**(30/dt))
    print(f"{pg:<3}{a:<12}{b:<12}{dt:>4}{base:>8,}{su:>8.3f}{ct:>8.1f}{ct30:>13.1f}")
con=sqlite3.connect(ROOT/"data/cprt.db",timeout=60)
con.execute("DROP TABLE IF EXISTS cycle_time_pagematched")
con.execute("""CREATE TABLE cycle_time_pagematched(page INT,from_date TEXT,to_date TEXT,dt_days INT,
  base_lots INT,survivors INT,survival REAL,implied_ct_days REAL)""")
con.executemany("INSERT INTO cycle_time_pagematched VALUES(?,?,?,?,?,?,?,?)",rows); con.commit()
with open(ROOT/"data/csv/cycle_time_pagematched.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["page","from_date","to_date","dt_days","base_lots","survivors","survival","implied_ct_days"]); w.writerows(rows)
print(f"\n{len(rows)} dt-matched (20-45d) page-matched pairs -> data/csv/cycle_time_pagematched.csv")
byy=collections.defaultdict(list)
for pg,a,b,dt,base,ov,su,ct in rows: byy[a[:4]].append(ct)
print("\n=== implied CT by year (dt 20-45d only, so comparable) ===")
prev=None
for y in sorted(byy):
    m=statistics.mean(byy[y]); sd=statistics.stdev(byy[y]) if len(byy[y])>1 else 0
    ch=f"{(m/prev-1)*100:+.1f}%" if prev else ""
    print(f"  {y}: n={len(byy[y]):<3} mean CT={m:.1f}d  sd={sd:.1f}  {ch}")
    prev=m
print("\n=== dt-sensitivity check (is dt still driving it?) ===")
X=[r[3] for r in rows]; Y=[r[7] for r in rows]; n=len(X)
if n>3:
    mx=sum(X)/n; my=sum(Y)/n
    sxy=sum((a-mx)*(b-my) for a,b in zip(X,Y)); sxx=sum((a-mx)**2 for a in X); syy=sum((b-my)**2 for b in Y)
    r=sxy/(sxx*syy)**.5
    print(f"  corr(dt, implied CT) within the 20-45d band = {r:+.3f}  (want ~0)")
