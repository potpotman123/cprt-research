"""Rebuild the volume series on TOTAL inventory across all lot.xml pages.

A month is COMPLETE only if we hold pages 1..k where page k is the first page with
fewer than 50,000 entries (or empty). If every page we hold is full at 50,000 and the
next page is missing, the remainder is unknown -> month flagged INCOMPLETE.
"""
import re,glob,csv,sqlite3,collections,statistics,pathlib,datetime
ROOT=pathlib.Path(__file__).resolve().parent.parent
FULL=50000
FULL_TOL=49900   # >=this counts as a FULL page; 49,998/49,999 are parse artifacts, not remainders
US=set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split())
TITLE=("clean-title","salvage","non-repairable","nonrepairable","cert-of-title","bill-of-sale","junk")
rx=re.compile(r'<loc>[^<]*?/lot/(\d+)(?:/([^<?#]*))?</loc>')
files=collections.defaultdict(dict)   # month -> page -> path
for f in sorted(glob.glob(str(ROOT/"raw/lotxml/lotxml_p*.xml"))):
    m=re.search(r'lotxml_p(\d)_(\d{14})',f); pg=int(m.group(1)); ts=m.group(2)
    if pg==0: continue
    mo=ts[:6]
    if pg not in files[mo] or ts<re.search(r'_(\d{14})',files[mo][pg]).group(1):
        files[mo][pg]=f
def scan(path):
    txt=open(path,encoding="utf-8",errors="replace").read()
    ids=[];tt=collections.Counter();st=collections.Counter();yrs=[]
    for mm in rx.finditer(txt):
        ids.append(int(mm.group(1)))
        slug=(mm.group(2) or "").lower().strip("/"); t=None
        for k in TITLE:
            if slug.startswith(k): t=k; slug=slug[len(k):].strip("-"); break
        tt[t or "unknown"]+=1
        ym=re.match(r'(19\d{2}|20\d{2})-(.*)$',slug)
        if ym:
            yrs.append(int(ym.group(1))); parts=ym.group(2).split("-")
            for i in range(len(parts)-1,0,-1):
                if parts[i].upper() in US: st[parts[i].upper()]+=1; break
    return ids,tt,st,yrs
rows=[]
for mo in sorted(files):
    pages=files[mo]
    counts={}; allids=[]; TT=collections.Counter(); ST=collections.Counter(); YR=[]
    for pg in sorted(pages):
        ids,tt,st,yrs=scan(pages[pg])
        counts[pg]=len(ids); allids+=ids; TT+=tt; ST+=st; YR+=yrs
    have=sorted(counts)
    # find first non-full page among contiguous run starting at 1
    k=None; contiguous=True
    for i,pg in enumerate(have,start=1):
        if pg!=i: contiguous=False; break
        if counts[pg]<FULL_TOL: k=pg; break
    total=sum(counts[p] for p in have if p<= (k or max(have)))
    if k is None:
        complete=False; note=f"all held pages full ({','.join(str(p) for p in have)}); remainder unknown"
    elif not contiguous:
        complete=False; note=f"non-contiguous pages held: {have}"
    else:
        complete=True; note=f"last page = {k} ({counts[k]:,})"
    core=[i for i in allids if 1_000_000<=i<200_000_000]
    n=sum(counts.values())
    rows.append(dict(month=mo,pages_held=",".join(map(str,have)),
        page_counts=";".join(f"{p}:{counts[p]}" for p in have),
        total_lots=total if complete else None, complete=int(complete), note=note,
        core_max=max(core) if core else None, core_min=min(core) if core else None,
        pw_n=len([i for i in allids if i>=900_000_000]),
        salvage_pct=round(TT["salvage"]/n*100,2) if n else None,
        clean_pct=round(TT["clean-title"]/n*100,2) if n else None,
        med_veh_year=int(statistics.median(YR)) if YR else None,
        top_state=ST.most_common(1)[0][0] if ST else None,
        scanned_lots=n))
print(f"{'month':<8}{'pages':<12}{'total':>9}{'ok':>4}{'core_max':>12}{'salv%':>7}{'clean%':>7}  note")
for r in rows:
    tot = "{:,}".format(r["total_lots"]) if r["total_lots"] else "-"
    ok  = "Y" if r["complete"] else "n"
    cm  = r["core_max"] or 0
    sv  = r["salvage_pct"] or 0
    cl  = r["clean_pct"] or 0
    print(f"{r['month']:<8}{r['pages_held']:<12}{tot:>9}{ok:>4}{cm:>12,}"
          f"{sv:>6.1f}%{cl:>6.1f}%  {r['note']}")
con=sqlite3.connect(ROOT/"data/cprt.db",timeout=60)
con.execute("DROP TABLE IF EXISTS inventory_panel")
cols=list(rows[0].keys())
con.execute(f"CREATE TABLE inventory_panel({','.join(c+' TEXT' for c in cols)})")
con.executemany(f"INSERT INTO inventory_panel VALUES({','.join(':'+c for c in cols)})",rows); con.commit()
with open(ROOT/"data/csv/inventory_panel.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); w.writerows(rows)
comp=[r for r in rows if r["complete"]]
print(f"\n{len(rows)} months scanned, {len(comp)} COMPLETE -> data/csv/inventory_panel.csv")
