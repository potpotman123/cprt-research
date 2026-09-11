"""Inventory level v2 — fixes two bugs found 2026-09-09.

BUG 1: pages OVERLAP when they are out of sync (one rebuilt, another not), because the
       pagination boundary moves. Summing page counts overcounts by up to 14.8%.
       FIX: take the UNION of lot URLs across pages, not the sum.

BUG 2: when pages are out of sync you are mixing two vintages of Copart's list - a fresh
       page 1 alongside a stale page 2. Neither sum nor union is then meaningful.
       FIX: overlap % is a QUALITY METRIC. Only trust snapshots where overlap ~ 0,
       i.e. all pages rebuilt from the same underlying list.
"""
import re,glob,collections,sqlite3,csv,pathlib,datetime,statistics
ROOT=pathlib.Path(__file__).resolve().parent.parent
rx=re.compile(r'<loc>([^<]*/lot/\d+[^<]*)</loc>')
FULL_TOL=49900; OVERLAP_MAX=1.0     # percent
con=sqlite3.connect(ROOT/"data/cprt.db")
def pages_for_month(mo):
    P={}
    for f in glob.glob(str(ROOT/f"raw/lotxml/lotxml_p*_{mo}*.xml")):
        pg=int(re.search(r'_p(\d)_',f).group(1))
        if pg==0: continue
        s=set(rx.findall(open(f,encoding="utf-8",errors="replace").read()))
        if s: P[pg]=s
    return P
months=sorted({re.search(r'_p\d_(\d{6})',f).group(1) for f in glob.glob(str(ROOT/"raw/lotxml/lotxml_p*.xml"))})
rows=[]
for mo in months:
    P=pages_for_month(mo)
    if not P: continue
    have=sorted(P)
    counts={p:len(P[p]) for p in have}
    # contiguous from page 1, find first non-full page
    k=None; contig=True
    for i,pg in enumerate(have,1):
        if pg!=i: contig=False; break
        if counts[pg]<FULL_TOL: k=pg; break
    s=sum(counts.values()); u=len(set().union(*P.values()))
    ovp=(s-u)/s*100 if s else 0
    complete = bool(contig and k is not None)
    usable   = complete and ovp<=OVERLAP_MAX
    rows.append(dict(month=mo,pages=",".join(map(str,have)),sum_pages=s,union_lots=u,
                     overlap_pct=round(ovp,2),complete=int(complete),usable=int(usable),
                     last_page=k,last_page_n=counts.get(k)))
print(f"{'month':<9}{'union':>9}{'ovlap':>8}{'cmplt':>7}{'USABLE':>8}  note")
for r in rows:
    note="" if r["usable"] else ("pages out of sync" if r["complete"] else "page set incomplete")
    print(f"{r['month']:<9}{r['union_lots']:>9,}{r['overlap_pct']:>7.1f}%{'Y' if r['complete'] else '-':>7}"
          f"{'YES' if r['usable'] else '-':>8}  {note}")
u=[r for r in rows if r["usable"]]
print(f"\n{len(u)} usable of {len(rows)} months (was 15 under the old sum-based rule)")
con2=sqlite3.connect(ROOT/"data/cprt.db",timeout=60)
con2.execute("DROP TABLE IF EXISTS inventory_v2")
cols=list(rows[0].keys())
con2.execute(f"CREATE TABLE inventory_v2({','.join(c+' TEXT' for c in cols)})")
con2.executemany(f"INSERT INTO inventory_v2 VALUES({','.join(':'+c for c in cols)})",rows)
con2.commit()
with open(ROOT/"data/csv/inventory_v2.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
print(f"-> data/csv/inventory_v2.csv")
