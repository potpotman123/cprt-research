import re,glob,csv,sqlite3,collections,statistics,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
US=set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split())
TITLE=("clean-title","salvage","non-repairable","nonrepairable","cert-of-title","bill-of-sale","junk")
rx=re.compile(r'<loc>[^<]*?/lot/(\d+)(?:/([^<?#]*))?</loc>')
rows=[]
for f in sorted(glob.glob(str(ROOT/"raw/lotxml/lotxml_p*.xml"))):
    m=re.search(r'lotxml_p(\d)_(\d{14})',f); pg=int(m.group(1)); ts=m.group(2)
    txt=open(f,encoding="utf-8",errors="replace").read()
    ids=[]; tt=collections.Counter(); st=collections.Counter(); yrs=[]
    for mm in rx.finditer(txt):
        lid=int(mm.group(1)); ids.append(lid)
        slug=(mm.group(2) or "").lower().strip("/")
        t=None
        for k in TITLE:
            if slug.startswith(k): t=k; slug=slug[len(k):].strip("-"); break
        tt[t or "unknown"]+=1
        ym=re.match(r'(19\d{2}|20\d{2})-(.*)$',slug)
        if ym:
            yrs.append(int(ym.group(1))); parts=ym.group(2).split("-")
            for i in range(len(parts)-1,0,-1):
                if parts[i].upper() in US: st[parts[i].upper()]+=1; break
    if not ids: continue
    core=[i for i in ids if 1_000_000<=i<200_000_000]
    rows.append(dict(page=pg,ts=ts,month=ts[:6],n=len(ids),
        min_id=min(ids),max_id=max(ids),
        core_n=len(core),core_min=min(core) if core else None,core_max=max(core) if core else None,
        pw_n=len([i for i in ids if i>=900_000_000]),
        salvage=tt["salvage"],clean=tt["clean-title"],unknown=tt["unknown"],
        med_veh_year=int(statistics.median(yrs)) if yrs else None,
        top_state=st.most_common(1)[0][0] if st else None))
rows.sort(key=lambda r:(r["page"],r["ts"]))
print(f"{'pg':<3}{'month':<8}{'n':>7}{'core_min':>11}{'core_max':>11}{'PW':>6}{'salv%':>7}{'clean%':>7}{'medYr':>6}")
for r in rows:
    tot=r["n"]
    print(f"{r['page']:<3}{r['month']:<8}{r['n']:>7,}{(r['core_min'] or 0):>11,}{(r['core_max'] or 0):>11,}"
          f"{r['pw_n']:>6,}{r['salvage']/tot*100:>6.1f}%{r['clean']/tot*100:>6.1f}%{str(r['med_veh_year'] or ''):>6}")
con=sqlite3.connect(ROOT/"data/cprt.db",timeout=60)
con.execute("DROP TABLE IF EXISTS lotxml_panel")
cols=list(rows[0].keys())
con.execute(f"CREATE TABLE lotxml_panel({','.join(c+(' INT' if c not in ('top_state','month','ts') else ' TEXT') for c in cols)})")
con.executemany(f"INSERT INTO lotxml_panel VALUES({','.join(':'+c for c in cols)})",rows); con.commit()
with open(ROOT/"data/csv/lotxml_panel.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); w.writerows(rows)
print(f"\n{len(rows)} captures -> data/csv/lotxml_panel.csv")
# issuance-rate estimate from core_max drift on page-1 series
p1=[r for r in rows if r["page"]==1 and r["core_max"]]
if len(p1)>2:
    print("\n=== core_max drift (page 1) = ID issuance clock test ===")
    prev=None
    for r in p1:
        d="" if prev is None else f"{r['core_max']-prev:+,}"
        print(f"  {r['month']}  core_max={r['core_max']:>12,}  delta={d:>12}")
        prev=r["core_max"]
