"""State-level inventory from lot.xml slugs, per complete month.
Tests Yipit's claim (via Stephens 2026-08-20) of inventory BUILDS in NC, NY, UT, WA, HI."""
import re,glob,collections,sqlite3,csv,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
US=set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split())
TITLE=("clean-title","salvage","non-repairable","nonrepairable","cert-of-title","bill-of-sale","junk")
rx=re.compile(r'<loc>[^<]*?/lot/(\d+)(?:/([^<?#]*))?</loc>')
con=sqlite3.connect(ROOT/"data/cprt.db")
complete={r[0] for r in con.execute("SELECT month FROM inventory_level")}
def states_for(month):
    cnt=collections.Counter(); n=0
    for f in glob.glob(str(ROOT/f"raw/lotxml/lotxml_p*_{month}*.xml")):
        for m in rx.finditer(open(f,encoding="utf-8",errors="replace").read()):
            slug=(m.group(2) or "").lower().strip("/"); n+=1
            for k in TITLE:
                if slug.startswith(k): slug=slug[len(k):].strip("-"); break
            ym=re.match(r'(19\d{2}|20\d{2})-(.*)$',slug)
            if not ym: continue
            parts=ym.group(2).split("-")
            for i in range(len(parts)-1,0,-1):
                if parts[i].upper() in US: cnt[parts[i].upper()]+=1; break
    return cnt,n
panel={}
for mo in sorted(complete):
    if mo=="202609": continue
    c_,n=states_for(mo); panel[mo]=c_
    print(f"  {mo}: {n:,} lots scanned, {sum(c_.values()):,} state-attributed, {len(c_)} states",flush=True)
# live snapshot from DB
live=collections.Counter()
for st,k in con.execute("""SELECT state,count(*) FROM lot_snapshots
     WHERE snapshot_utc=(SELECT max(snapshot_utc) FROM lot_snapshots) AND state IS NOT NULL GROUP BY 1"""):
    if st in US: live[st]=k
panel["202609"]=live
print(f"  202609: {sum(live.values()):,} state-attributed (live), {len(live)} states")
rows=[]
for mo,c_ in panel.items():
    for st,k in c_.items(): rows.append((mo,st,k))
con2=sqlite3.connect(ROOT/"data/cprt.db",timeout=60)
con2.execute("DROP TABLE IF EXISTS state_panel")
con2.execute("CREATE TABLE state_panel(month TEXT,state TEXT,lots INT)")
con2.executemany("INSERT INTO state_panel VALUES(?,?,?)",rows); con2.commit()
with open(ROOT/"data/csv/state_panel.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["month","state","lots"]); w.writerows(rows)
print(f"\n{len(rows)} state-month rows -> data/csv/state_panel.csv")
# ---- the test: Sep 2025 -> Sep 2026 by state ----
A,B=panel.get("202509"),panel.get("202609")
if A and B:
    ta,tb=sum(A.values()),sum(B.values())
    print(f"\n=== STATE-LEVEL YoY, Sep-2025 -> Sep-2026 (totals {ta:,} -> {tb:,}, {(tb/ta-1)*100:+.1f}%) ===")
    YIPIT={"NC","NY","UT","WA","HI"}
    res=[]
    for st in sorted(set(A)|set(B)):
        a,b=A.get(st,0),B.get(st,0)
        if a<150: continue
        res.append((st,a,b,(b/a-1)*100,(b/tb)-(a/ta)))
    res.sort(key=lambda x:-x[3])
    print(f"{'st':<4}{'Sep25':>8}{'Sep26':>8}{'YoY':>9}{'share chg(bp)':>15}   Yipit-flagged?")
    for st,a,b,y,sh in res:
        print(f"{st:<4}{a:>8,}{b:>8,}{y:>+8.1f}%{sh*10000:>+14.0f}   {'<<< YIPIT' if st in YIPIT else ''}")
    print("\n=== VERDICT on the Yipit 5 ===")
    d={x[0]:x for x in res}
    for st in sorted(YIPIT):
        if st in d:
            _,a,b,y,sh=d[st]
            print(f"  {st}: {a:,} -> {b:,}  YoY {y:+.1f}%  share {sh*10000:+.0f}bp  "
                  f"{'BUILD confirmed' if y>0 else 'no build (declined)'}"
                  f"{'  [outperforms national]' if y>(tb/ta-1)*100 else ''}")
        else: print(f"  {st}: base too small to test")
