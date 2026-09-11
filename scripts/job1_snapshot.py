#!/usr/bin/env python3
"""JOB 1 - daily sitemap snapshot. Robots-enforced, rate-limited, WAF-aware.

Run daily. Appends one row per lot per snapshot + full sale-event roster.
Exits 2 (loud) if Copart's WAF blocks us, so cron mail shows a real failure
instead of silently recording zero rows.
"""
import sys,os,re,time,sqlite3,csv,datetime,pathlib,urllib.parse
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent)); import prov
ROOT=pathlib.Path(__file__).resolve().parent.parent

# Parsed from raw/sitemaps/robots.copart.com.txt, fetched first-hand 2026-09-08.
DISALLOW_PREFIXES=['/public/data/', '/paymentsDue/', '/paymentHistory/', '/myBids/', '/lotsWon/', '/lotsLost', '/driverseat/', '/dashboard/', '/dashboard', '/downloadSalesData', '/memberFees', '/messagesettings', '/accountInformation/accountSetting', '/accountinformation/contactinfo', '/hireabroker', '/es/hireabroker', '/ar/hireabroker', '/ru/hireabroker', '/pl/hireabroker', '/fr-CA/hireabroker', '/lotSearchResults/', '/es/lotSearchResults/', '/ar/lotSearchResults/', '/ru/lotSearchResults/', '/pl/lotSearchResults/', '/fr-CA/lotSearchResults/']
ALLOW_EXACT=['/lotSearchResults$', '/es/lotSearchResults$', '/ar/lotSearchResults$', '/ru/lotSearchResults$', '/pl/lotSearchResults$', '/fr-CA/lotSearchResults$']
ROBOTS_BASIS=("www.copart.com/robots.txt fetched first-hand 2026-09-08 (200, 1272b, "
              "saved raw/sitemaps/robots.copart.com.txt). None of the Job-1 sitemap "
              "targets appear in its Disallow list; all are named as Sitemap: targets "
              "in copart-sitemaps.com/robots.txt.")
# Order matters: the small endpoints go FIRST. On 2026-09-09 location.xml and
# models-list.xml came back as Incapsula challenges when fetched AFTER ~20MB of
# lot.xml, suggesting a volume-based throttle rather than an endpoint block.
# DAILY targets only. location.xml and models-list.xml were removed 2026-09-09:
# neither had a parser (both logged rows=0 every run), both change rarely, and being
# fetched last after ~20MB of lot.xml they were the two that drew Incapsula challenges.
# Re-add them behind a weekly flag if/when a parser exists.
TARGETS=[("https://www.copart.com/sale-list-results.xml","salelist"),
         ("https://www.copart.com/lot.xml?page=1","lot1"),
         ("https://www.copart.com/lot.xml?page=2","lot2"),
         ("https://www.copart.com/lot.xml?page=3","lot3"),
         ("https://www.copart.com/lot.xml?page=4","lot4")]
def robots_ok(url):
    p=urllib.parse.urlsplit(url).path
    for a in ALLOW_EXACT:                       # "Allow: /x$" beats a broader Disallow
        if a.endswith("$") and p==a[:-1]: return True
    return not any(p.startswith(x) for x in DISALLOW_PREFIXES)
def is_waf(body):
    b=body[:4000].lower()
    return b"incapsula" in b or b"_incapsula_resource" in b or b"request unsuccessful" in b
NOW=datetime.datetime.now(datetime.timezone.utc)
SNAP=NOW.strftime("%Y-%m-%dT%H:%M:%SZ"); TS=NOW.strftime("%Y%m%d%H%M%S")
RAW=ROOT/"raw/daily"/TS; os.makedirs(RAW,exist_ok=True)
def _db(): 
    c=sqlite3.connect(ROOT/"data/cprt.db", timeout=120)
    c.execute("PRAGMA journal_mode=WAL"); return c
con=_db()
con.executescript("""
CREATE TABLE IF NOT EXISTS lot_snapshots(snapshot_utc TEXT,lot_id INT,title_type TEXT,year INT,
  make_model TEXT,state TEXT,yard_slug TEXT,lastmod TEXT,loc TEXT);
CREATE TABLE IF NOT EXISTS sale_events_live(snapshot_utc TEXT,yard_id INT,sale_date TEXT,
  state TEXT,city TEXT,location TEXT,sale_epoch_ms INT);
CREATE TABLE IF NOT EXISTS run_log(snapshot_utc TEXT,target TEXT,http INT,bytes INT,rows INT,note TEXT);
CREATE TABLE IF NOT EXISTS lastmod_profile(snapshot_utc TEXT,target TEXT,n INT,newest TEXT,
  median_lastmod TEXT,median_age_days INT,cluster_days TEXT);
""")
con.commit(); con.close()   # release lock during network phase
runlog=[]
lmprof=[]
US=set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split())
TITLE=("clean-title","salvage","non-repairable","nonrepairable","cert-of-title","bill-of-sale","junk")
rx_lot=re.compile(r'<url>\s*<loc>([^<]*?/lot/(\d+)(?:/([^<?#]*))?)</loc>(?:\s*<lastmod>([^<]*)</lastmod>)?',re.S)
rx_sale=re.compile(r'/saleListResult/(\d+)(?:/(\d{4}-\d{2}-\d{2}))?\?location=([^&<]+)&(?:amp;)?saleDate=([^<&]+)')
blocked=[]; lot_rows=[]; sale_rows=[]
for url,tag in TARGETS:
    if not robots_ok(url):
        print(f"REFUSED (robots): {url}"); prov.log(url,"GET",None,b"","disallowed",ROBOTS_BASIS,"refused by policy"); continue
    s,b=prov.get(url,"allowed",ROBOTS_BASIS,note=f"Job1 daily {tag}",
                 save_to=f"raw/daily/{TS}/{tag}.xml")
    n=0
    if s==200 and not is_waf(b):
        txt=b.decode("utf-8","replace")
        if tag.startswith("lot"):
            for m in rx_lot.finditer(txt):
                loc,lid,slug,lastmod=m.group(1),int(m.group(2)),(m.group(3) or ""),(m.group(4) or "")
                tt=year=mm=st=None; yard=None
                sl=slug.lower().strip("/")
                for t in TITLE:
                    if sl.startswith(t): tt=t; sl=sl[len(t):].strip("-"); break
                ym=re.match(r'(19\d{2}|20\d{2})-(.*)$',sl)
                if ym:
                    year=int(ym.group(1)); parts=ym.group(2).split("-")
                    for i in range(len(parts)-1,0,-1):
                        if parts[i].upper() in US:
                            st=parts[i].upper(); yard="-".join(parts[i+1:]) or None
                            mm="-".join(parts[:i]); break
                    if st is None: mm=ym.group(2)
                lot_rows.append((SNAP,lid,tt,year,mm,st,yard,lastmod,loc)); n+=1
        elif tag=="salelist":
            seen=set()
            for m in rx_sale.finditer(txt):
                yard=int(m.group(1)); sd=m.group(2)
                loc=urllib.parse.unquote(m.group(3)).strip(); ep=m.group(4)
                st,city=(loc.split(" - ",1)) if " - " in loc else (None,loc)
                k=(yard,sd,loc)
                if k in seen: continue
                seen.add(k)
                sale_rows.append((SNAP,yard,sd,st,city,loc,None if ep=="Future" else int(ep))); n+=1
    else:
        why = "WAF/Incapsula" if is_waf(b) else f"http {s}, {len(b)}b, unparseable"
        blocked.append((url,s,why)); print(f"  BLOCKED [{why}]  {url}")
    runlog.append((SNAP,tag,s,len(b),n,"waf" if is_waf(b) else ""))
    if tag.startswith("lot") and s==200 and n>0:
        import collections as _c
        lm=_c.Counter(x for x in re.findall(r"<lastmod>([^<]*)</lastmod>",b.decode("utf-8","replace")))
        lm=_c.Counter({k.strip()[:10]:v for k,v in lm.items() if k.strip()})
        if lm:
            tt=sum(lm.values()); cum=0; med=None
            for d,c_ in sorted(lm.items(),reverse=True):
                cum+=c_
                if cum>=tt/2: med=d; break
            age=(NOW.date()-datetime.date.fromisoformat(med)).days if med else None
            clus=",".join(d for d,c_ in sorted(lm.items()) if c_>tt*0.05)
            lmprof.append((SNAP,tag,tt,max(lm),med,age,clus))
    print(f"  {s} {len(b):>9,}b rows={n:<6} {url}")
con=_db()
# same-day guard: a re-run on the same UTC date REPLACES that date's rows,
# so a manual run plus the LaunchAgent firing cannot double-count the day.
# BUGFIX 2026-09-09: the guard used to delete the day's rows unconditionally, BEFORE
# inserting. A later failed run (zero rows fetched) therefore DESTROYED the good data
# from an earlier successful run the same day - which is exactly what happened to the
# 2026-09-09 snapshot. Only replace when we actually have something to replace it with.
# BUGFIX 2026-09-10 (third iteration of this guard):
#   v1 deleted the day's rows unconditionally BEFORE inserting -> a later failed run
#      destroyed an earlier good one (lost 2026-09-09).
#   v2 made deletion conditional on having rows -> but a WORSE capture still silently
#      replaced a better one (tonight's 11.5%-overlap run clobbered the morning's 0.1%).
#   v3: only replace when the new capture is at least as IN-SYNC as the one already stored.
#      Cross-page overlap is the quality metric; lower is better.
_today=SNAP[:10]
def _overlap_of(rows):
    if not rows: return 100.0
    ids={r[1] for r in rows}
    return (len(rows)-len(ids))/len(rows)*100
_new_ov=_overlap_of(lot_rows)
_prev=con.execute("""SELECT snapshot_utc,count(*),count(DISTINCT lot_id) FROM lot_snapshots
                     WHERE substr(snapshot_utc,1,10)=? GROUP BY 1 ORDER BY 1 DESC LIMIT 1""",
                  (_today,)).fetchone()
_replace=True
if _prev and _prev[1]:
    _prev_ov=(_prev[1]-_prev[2])/_prev[1]*100
    if _new_ov > _prev_ov + 0.5:
        _replace=False
        print(f"\n  KEEPING existing {_today} capture: stored overlap {_prev_ov:.1f}% "
              f"beats this run's {_new_ov:.1f}%. New rows discarded.")
    else:
        print(f"\n  replacing {_today}: stored {_prev_ov:.1f}% -> new {_new_ov:.1f}% overlap")
if _replace and lot_rows:
    con.execute("DELETE FROM lot_snapshots  WHERE substr(snapshot_utc,1,10)=?",(_today,))
if _replace and sale_rows:
    con.execute("DELETE FROM sale_events_live WHERE substr(snapshot_utc,1,10)=?",(_today,))
if not _replace:
    lot_rows=[]; sale_rows=[]
con.executemany("INSERT INTO run_log VALUES(?,?,?,?,?,?)",runlog)
con.executemany("INSERT INTO lastmod_profile VALUES(?,?,?,?,?,?,?)",lmprof)
con.executemany("INSERT INTO lot_snapshots VALUES(?,?,?,?,?,?,?,?,?)",lot_rows)
con.executemany("INSERT INTO sale_events_live VALUES(?,?,?,?,?,?,?)",sale_rows)
con.commit()
for name,rws,hdr in [("lot_snapshots",lot_rows,["snapshot_utc","lot_id","title_type","year","make_model","state","yard_slug","lastmod","loc"]),
                     ("sale_events_live",sale_rows,["snapshot_utc","yard_id","sale_date","state","city","location","sale_epoch_ms"])]:
    p=ROOT/f"data/csv/{name}.csv"; new=not p.exists()
    with open(p,"a",newline="") as fh:
        w=csv.writer(fh)
        if new: w.writerow(hdr)
        w.writerows(rws)
# ---- cross-page overlap gate: are the pages in sync? ----
# Pages are meant to be disjoint slices of one list. When one rebuilds and another
# does not, the pagination boundary moves and lots appear on TWO pages. Overlap is
# therefore a direct measure of how out-of-sync the file is. Overlap >5% means you
# are mixing two vintages of Copart's list; the snapshot is not comparable.
try:
    _pg={}
    for _t in ("lot1","lot2","lot3","lot4"):
        _f=RAW/f"{_t}.xml"
        if _f.exists() and _f.stat().st_size>10000:
            _pg[_t]=set(re.findall(r"<loc>([^<]*/lot/\d+[^<]*)</loc>",_f.read_text(errors="replace")))
    if len(_pg)>1:
        _s=sum(len(v) for v in _pg.values()); _u=len(set().union(*_pg.values()))
        _ov=(_s-_u)/_s*100
        print(f"\n  cross-page overlap: {_ov:.1f}%  (sum {_s:,} vs union {_u:,})")
        print(f"  DISTINCT lots (use this, not the sum): {_u:,}")
        if _ov>5.0:
            print(f"  !! PAGES OUT OF SYNC ({_ov:.1f}% overlap). Snapshot NOT comparable "
                  f"to others - exclude from level/flow series.")
except Exception as _e:
    print("  (overlap check failed:",_e,")")

# ---- staleness gate: did ANY page refresh recently? ----
# Each fetch is a mosaic of entries aged 0-30+d. If no page has >5% of entries
# stamped today/yesterday, we caught the file before its daily rebuild landed and
# this snapshot is a near-duplicate of the previous one - flag it, do not compare.
stale=None
if lmprof:
    fresh=[(tag,age) for (_,tag,n,newest,med,age,clus) in lmprof if age is not None]
    if fresh:
        stale = min(a for _,a in fresh) > 3
        print(f"\n  page freshness (median entry age): "
              + "  ".join(f"{tag}={age}d" for tag,age in fresh))
        if stale:
            print("  !! STALE FETCH: no page rebuilt in >3d. Do not use for flow analysis.")

# ---------------- profile printout ----------------
print(f"\n{'='*64}\nJOB 1 PROFILE  {SNAP}\n{'='*64}")
if blocked:
    print(f"!! WAF BLOCKED {len(blocked)}/{len(TARGETS)} targets - snapshot INCOMPLETE")
    for u,s,why in blocked: print(f"   http={s:<5} [{why}]  {u}")
if lot_rows:
    ids=[r[1] for r in lot_rows]; ids.sort()
    print(f"lots: {len(lot_rows):,}  distinct={len(set(ids)):,}  min={min(ids):,}  max={max(ids):,}")
    gaps=[(b-a) for a,b in zip(ids,ids[1:]) if b>a]
    if gaps:
        gaps.sort(); import statistics
        print(f"  id gap: median={statistics.median(gaps):,.0f} p90={gaps[int(len(gaps)*.9)]:,} max={max(gaps):,}")
    tt={}; stt={}
    for r in lot_rows:
        tt[r[2] or "unknown"]=tt.get(r[2] or "unknown",0)+1
        stt[r[5] or "?"]=stt.get(r[5] or "?",0)+1
    tot=len(lot_rows)
    print("  title mix: "+"  ".join(f"{k}={v} ({v/tot*100:.1f}%)" for k,v in sorted(tt.items(),key=lambda x:-x[1])))
    print("  top states: "+"  ".join(f"{k}={v}" for k,v in sorted(stt.items(),key=lambda x:-x[1])[:12]))
if lot_rows:
    ids_set={r[1] for r in lot_rows}
    dup=len(lot_rows)-len(ids_set)
    print(f"  duplicate rows: {dup:,} ({dup/len(lot_rows)*100:.1f}%)   distinct lots: {len(ids_set):,}")
    prev=con.execute("""SELECT snapshot_utc FROM lot_snapshots WHERE snapshot_utc<?
                        ORDER BY snapshot_utc DESC LIMIT 1""",(SNAP,)).fetchone()
    if prev:
        P={r[0] for r in con.execute("SELECT lot_id FROM lot_snapshots WHERE snapshot_utc=?",(prev[0],))}
        if P:
            surv=len(P&ids_set)/len(P)
            print(f"  vs {prev[0][:10]}: survived {surv*100:.1f}%  departed {len(P-ids_set):,}  arrived {len(ids_set-P):,}")
            if surv<0.90:
                print(f"  !! WARNING: {(1-surv)*100:.0f}% one-day churn is too fast to be sales "
                      f"(~7%/day max). lot.xml is likely a ROTATING SAMPLE, not a census.")
if sale_rows:
    yards={r[1] for r in sale_rows}; dated=[r for r in sale_rows if r[2]]
    print(f"yards: {len(yards)}   dated sale events: {len(dated):,}   events/yard: {len(dated)/max(1,len(yards)):.2f}")
    st={}
    for r in sale_rows: st[r[3] or "?"]=st.get(r[3] or "?",0)+1
    print("  top states by sale entries: "+"  ".join(f"{k}={v}" for k,v in sorted(st.items(),key=lambda x:-x[1])[:12]))
con.close()
if not lot_rows and not sale_rows:
    print("\nFATAL: zero rows captured from all %d targets." % len(TARGETS))
    print("Copart's edge (Imperva/Incapsula) is blocking this network's egress IP.")
    print("Run this collector from a network Copart does not block. Nothing else in it needs to change.")
    sys.exit(2)
if blocked:
    print("\nWARNING: %d/%d targets failed - snapshot is PARTIAL." % (len(blocked),len(TARGETS)))
    sys.exit(1)
