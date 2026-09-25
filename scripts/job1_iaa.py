#!/usr/bin/env python3
"""JOB 1b — IAA (Insurance Auto Auctions, owned by RB Global) daily sitemap snapshot.

Purpose: a DAILY measure of the duopoly's US listed inventory split.
  Copart lists ~137-147k US lots in lot.xml (Job 1). IAA lists ~103k US vehicles in
  sitemap1-3.xml. Copart share of listed = copart_us / (copart_us + iaa). First
  observed 2026-09-11: 136,803 vs 102,976 -> 57.1%.

What IAA publishes (all under one obfuscated path, discovered from robots.txt):
  sitemap_index.xml            -> 10 children
  sitemap{1,2,3}.xml           -> /vehicledetail/{id}~US    (~103k, the inventory)
  sitemapbranches1.xml         -> /locations/{id}~US        (~201 branches)
  sitemapauctions1.xml         -> /saleslist/{branch}~US/{MMDDYYYY}  (~335 scheduled sales)
  sitemapMake*/VehicleType*    -> SEO landing pages, not fetched

lastmod semantics (observed 2026-09-11): ~98% of vehicle entries carry a lastmod within
the last 4 business days (44k today, 21k/18k/15k the three prior days). So lastmod is a
live touch stamp and the file is a live listing, not an archive. Same ~4-day rebuild
cadence as Copart's lot.xml.

ROBOTS / PROVENANCE
  www.iaai.com/robots.txt (fetched FIRST, every run, saved to raw/):
    Disallow: /MyAuctionCenter/  /Login/*  /Search  /Marketing/Search
    #Sitemap: https://www.iaai.com/Xj9rDOVMEi0hc38S/sitemap_index.xml   <-- COMMENTED OUT
  The sitemap path is NOT in any Disallow. Robots semantics restrict only via Disallow,
  so fetching it is permitted. But the Sitemap directive being commented out means IAA is
  not advertising it. This is recorded verbatim in the provenance log so the user can make
  the judgement call. If the user decides otherwise, remove this job from run_job1.sh.
  We never touch /vehicledetail/ pages themselves (only the sitemap listing them), never
  authenticate, never exceed prov.MIN_INTERVAL between requests, and identify with
  From:/X-Contact: on every request.

Same-day guard (inherits the lesson from Job 1's three iterations): a re-run on the same
UTC day only replaces the stored rows if it captured at least 90% as many vehicles.
Never delete before a successful parse.
"""
import sys, os, re, sqlite3, csv, datetime, pathlib, urllib.parse, collections, glob, time
BIG_PAUSE = int(os.environ.get('IAA_BIG_PAUSE', '90'))   # seconds between the ~6.8 MB vehicle sitemaps: 11 of the first 15 nightly runs lost sitemap3 to the volume throttle
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import prov

# VOLUME THROTTLE (observed 2026-09-11): three full pulls (~45MB) in one morning and IAA began serving
# the "Pardon Our Interruption" interstitial on every request, including the 1.6KB index. It cleared
# for Copart within hours in the analogous case. RULE: run this at most ONCE per day (the LaunchAgent).
# If a run is challenged, do nothing - the same-day guard keeps prior data and tomorrow's run will land.
#   --from-dir DIR : load a snapshot from already-fetched XML files instead of fetching (no requests).
#                    Used 2026-09-11 to load the morning's first pull after the afternoon was throttled.
FROM_DIR = None
if "--from-dir" in sys.argv:
    FROM_DIR = pathlib.Path(sys.argv[sys.argv.index("--from-dir") + 1])

HOST = "https://www.iaai.com"
INDEX = f"{HOST}/Xj9rDOVMEi0hc38S/sitemap_index.xml"
WANT = re.compile(r"/(sitemap\d+|sitemapbranches\d+|sitemapauctions\d+)\.xml$")

NOW = datetime.datetime.now(datetime.timezone.utc)
SNAP = NOW.strftime("%Y-%m-%dT%H:%M:%SZ"); TS = NOW.strftime("%Y%m%d%H%M%S"); TODAY = SNAP[:10]
RAW = ROOT / "raw/iaai/daily" / TS; os.makedirs(RAW, exist_ok=True)

rx_veh = re.compile(r"<loc>https://www\.iaai\.com/vehicledetail/(\d+)~(\w+)</loc>\s*(?:<lastmod>([^<]+)</lastmod>)?", re.S)
rx_br  = re.compile(r"<loc>https://www\.iaai\.com/locations/(\d+)~(\w+)</loc>")
rx_auc = re.compile(r"<loc>https://www\.iaai\.com/saleslist/(\d+)~(\w+)/(\d{8})</loc>")

def db():
    c = sqlite3.connect(ROOT / "data/cprt.db", timeout=120); c.execute("PRAGMA journal_mode=WAL"); return c

con = db()
con.executescript("""
CREATE TABLE IF NOT EXISTS iaa_vehicle_snapshots(snapshot_utc TEXT, vehicle_id INT, country TEXT, lastmod TEXT);
CREATE TABLE IF NOT EXISTS iaa_branch_snapshots(snapshot_utc TEXT, branch_id INT, country TEXT);
CREATE TABLE IF NOT EXISTS iaa_auction_snapshots(snapshot_utc TEXT, branch_id INT, country TEXT, sale_date TEXT);
CREATE TABLE IF NOT EXISTS iaa_run_log(snapshot_utc TEXT, target TEXT, http INT, bytes INT, rows INT, note TEXT);
CREATE TABLE IF NOT EXISTS duopoly_daily(snapshot_utc TEXT PRIMARY KEY, day TEXT, copart_snapshot TEXT,
  copart_us_lots INT, copart_total_lots INT, iaa_vehicles INT, iaa_branches INT, iaa_auctions INT,
  copart_share_pct REAL, iaa_lastmod_4day_pct REAL, note TEXT);
CREATE INDEX IF NOT EXISTS ix_iaa_veh_snap ON iaa_vehicle_snapshots(snapshot_utc);
""")
con.commit(); con.close()

# ---- 1. robots.txt FIRST -------------------------------------------------------------
def _read(p): return open(p, "rb").read()
if FROM_DIR:
    rf = sorted(glob.glob(str(FROM_DIR / "robots*.txt")))
    if not rf: print("--from-dir needs a saved robots*.txt in the directory"); sys.exit(2)
    s, b = 200, _read(rf[0]); print(f"[from-dir] robots from {rf[0]}")
else:
    s, b = prov.get(f"{HOST}/robots.txt", "unknown", "fetching robots.txt first", note="Job1b IAA robots",
                    save_to=f"raw/iaai/daily/{TS}/robots.txt")
if s != 200:
    print(f"robots.txt HTTP {s}; refusing to proceed without robots"); sys.exit(2)
rob = b.decode("utf-8", "replace")
disallow = [ln.split(":", 1)[1].strip() for ln in rob.splitlines() if ln.lower().startswith("disallow:")]
disallow_prefixes = [d.rstrip("*") for d in disallow if d]
sitemap_commented = any(ln.strip().startswith("#") and "sitemap" in ln.lower() for ln in rob.splitlines())
ROBOTS_BASIS = (f"www.iaai.com/robots.txt fetched first-hand {TODAY} (200, {len(b)}b). Disallow: {disallow}. "
                f"Sitemap directive {'COMMENTED OUT' if sitemap_commented else 'active'}; sitemap path is not Disallowed.")
print(ROBOTS_BASIS)
def robots_ok(url):
    p = urllib.parse.urlsplit(url).path
    return not any(p.startswith(x) for x in disallow_prefixes)

# ---- 2. index -----------------------------------------------------------------------
if not robots_ok(INDEX):
    print("REFUSED (robots): index"); sys.exit(2)
if FROM_DIR:
    idx = sorted(glob.glob(str(FROM_DIR / "sitemap_index*.xml")))
    s, b = (200, _read(idx[0])) if idx else (404, b"")
    runlog = [(SNAP, "index", s, len(b), 0, f"from-dir {FROM_DIR}")]
else:
    s, b = prov.get(INDEX, "allowed", ROBOTS_BASIS, note="Job1b IAA sitemap index", save_to=f"raw/iaai/daily/{TS}/sitemap_index.xml")
    runlog = [(SNAP, "index", s, len(b), 0, "")]
if s != 200:
    print(f"index HTTP {s}"); sys.exit(2)
children = [u for u in re.findall(r"<loc>([^<]+)</loc>", b.decode("utf-8", "replace")) if WANT.search(u)]
# SMALL FILES FIRST. Observed 2026-09-11: after ~15MB of sitemap1-3 the 6th request (auctions, 6KB)
# came back as a "Pardon Our Interruption" bot-challenge page with HTTP 200 - a volume-based throttle,
# exactly what Copart's collector showed on 2026-09-09. Same fix: fetch the small endpoints before the big ones.
children.sort(key=lambda u: (0 if "branches" in u or "auctions" in u else 1, u))
print(f"index -> {len(children)} wanted children (small first)")

def is_challenge(body):
    """WAF interstitial served with HTTP 200. Never parse it as data; never try to solve it."""
    h = body[:6000].lower()
    return (b"pardon our interruption" in h or b"incapsula" in h or b"distil" in h
            or b"request unsuccessful" in h or (b"<html" in h and b"<urlset" not in h and b"<sitemapindex" not in h))

# ---- 3. children -------------------------------------------------------------------
veh, br, auc = [], [], []
big_seen = 0
for u in children:
    tag = WANT.search(u).group(1)
    is_veh = bool(re.match(r"sitemap\d", tag))
    if is_veh and big_seen and not FROM_DIR:
        print(f"  pausing {BIG_PAUSE}s before {tag} (spread the volume; IAA throttles bursts)"); time.sleep(BIG_PAUSE)
    if is_veh: big_seen += 1
    if not robots_ok(u):
        print(f"REFUSED (robots): {u}"); prov.log(u, "GET", None, b"", "disallowed", ROBOTS_BASIS, "refused by policy"); continue
    if FROM_DIR:
        fs = sorted(glob.glob(str(FROM_DIR / f"{tag}*.xml")))
        s, b = (200, _read(fs[0])) if fs else (404, b"")
    else:
        s, b = prov.get(u, "allowed", ROBOTS_BASIS, note=f"Job1b IAA {tag}", save_to=f"raw/iaai/daily/{TS}/{tag}.xml")
    n = 0
    if s == 200 and is_challenge(b):
        print(f"  CHALLENGE (WAF interstitial, not parsed)  {tag}"); runlog.append((SNAP, tag, s, len(b), 0, "challenge")); continue
    if s == 200:
        t = b.decode("utf-8", "replace")
        if tag.startswith("sitemapbranches"):
            for m in rx_br.finditer(t): br.append((SNAP, int(m.group(1)), m.group(2))); n += 1
        elif tag.startswith("sitemapauctions"):
            for m in rx_auc.finditer(t):
                d = m.group(3); iso = f"{d[4:8]}-{d[0:2]}-{d[2:4]}"
                auc.append((SNAP, int(m.group(1)), m.group(2), iso)); n += 1
        else:
            for m in rx_veh.finditer(t): veh.append((SNAP, int(m.group(1)), m.group(2), (m.group(3) or "")[:10])); n += 1
    runlog.append((SNAP, tag, s, len(b), n, ""))
    print(f"  {s} {len(b):>9,}b rows={n:<7} {tag}")

veh_failed = sorted(t for (_s, t, _h, _b, n, _n) in runlog if re.match(r"sitemap\d", t) and n == 0)
iaa_complete = 0 if veh_failed else 1
if veh_failed: print(f"  !! IAA INCOMPLETE: {', '.join(veh_failed)} not parsed - vehicle total is partial; share will be NULL")

# dedupe vehicles across the three files (defensive; observed 0 overlap)
seen = set(); veh_u = []
for r in veh:
    if r[1] in seen: continue
    seen.add(r[1]); veh_u.append(r)
lm = collections.Counter(r[3] for r in veh_u if r[3])
recent4 = sum(v for k, v in lm.items() if k and (NOW.date() - datetime.date.fromisoformat(k)).days <= 5)
pct4 = 100 * recent4 / len(veh_u) if veh_u else 0.0
print(f"vehicles={len(veh_u):,} (dup dropped {len(veh)-len(veh_u)})  branches={len(br)}  auctions={len(auc)}  lastmod<=5d: {pct4:.1f}%")

# ---- 4. same-day guard + store -----------------------------------------------------
con = db()
for _col, _typ in (("iaa_complete", "INT"), ("copart_overlap_pct", "REAL"), ("usable", "INT")):
    try: con.execute(f"ALTER TABLE duopoly_daily ADD COLUMN {_col} {_typ}")
    except sqlite3.OperationalError: pass
prev = con.execute("SELECT snapshot_utc, count(*) FROM iaa_vehicle_snapshots WHERE substr(snapshot_utc,1,10)=? GROUP BY 1 ORDER BY 2 DESC LIMIT 1", (TODAY,)).fetchone()
replace = True; note = ""
if not veh_u:
    replace = False; note = "zero vehicles parsed; existing rows kept"
elif prev and len(veh_u) < 0.9 * prev[1]:
    replace = False; note = f"new capture {len(veh_u)} < 90% of existing {prev[1]} ({prev[0]}); kept existing"
if replace:
    for tbl in ("iaa_vehicle_snapshots", "iaa_branch_snapshots", "iaa_auction_snapshots"):
        con.execute(f"DELETE FROM {tbl} WHERE substr(snapshot_utc,1,10)=?", (TODAY,))
    con.executemany("INSERT INTO iaa_vehicle_snapshots VALUES(?,?,?,?)", veh_u)
    con.executemany("INSERT INTO iaa_branch_snapshots VALUES(?,?,?)", br)
    con.executemany("INSERT INTO iaa_auction_snapshots VALUES(?,?,?,?)", auc)
else:
    print("SAME-DAY GUARD:", note)
con.executemany("INSERT INTO iaa_run_log VALUES(?,?,?,?,?,?)", runlog)
if veh_u:
    tt = sum(lm.values()); cum = 0; med = None
    for d, c_ in sorted(lm.items(), reverse=True):
        cum += c_
        if cum >= tt/2: med = d; break
    age = (NOW.date() - datetime.date.fromisoformat(med)).days if med else None
    con.execute("INSERT INTO lastmod_profile(snapshot_utc,target,n,newest,median_lastmod,median_age_days,cluster_days) VALUES(?,?,?,?,?,?,?)",
                (SNAP, "iaa_vehicles", len(veh_u), max(lm) if lm else None, med, age,
                 ",".join(d for d, c_ in sorted(lm.items()) if c_ > tt*0.05)))

# ---- 5. duopoly join with the latest Copart snapshot (same day preferred, else latest) --
cp = con.execute("SELECT snapshot_utc FROM lot_snapshots WHERE substr(snapshot_utc,1,10)=? ORDER BY 1 DESC LIMIT 1", (TODAY,)).fetchone() \
     or con.execute("SELECT max(snapshot_utc) FROM lot_snapshots").fetchone()
cp_snap = cp[0] if cp else None
if cp_snap and veh_u:
    tot = con.execute("SELECT count(DISTINCT lot_id) FROM lot_snapshots WHERE snapshot_utc=?", (cp_snap,)).fetchone()[0]
    us = con.execute("SELECT count(DISTINCT lot_id) FROM lot_snapshots WHERE snapshot_utc=? AND length(state)=2 AND state GLOB '[A-Z][A-Z]'", (cp_snap,)).fetchone()[0]
    cr, cl = con.execute("SELECT count(*), count(DISTINCT lot_id) FROM lot_snapshots WHERE snapshot_utc=?", (cp_snap,)).fetchone()
    ov = round(100.0 * (cr - cl) / cr, 2) if cr else None                      # cross-page overlap = Copart quality gate (<=1% usable)
    share = round(100 * us / (us + len(veh_u)), 2) if iaa_complete else None   # never publish a share off a partial IAA count
    usable = 1 if (iaa_complete and ov is not None and ov <= 1.0) else 0
    notes = []
    if cp_snap[:10] != TODAY: notes.append(f"copart snapshot is from {cp_snap[:10]}")
    if veh_failed: notes.append(f"iaa incomplete: {','.join(veh_failed)} failed")
    if ov is not None and ov > 1.0: notes.append(f"copart overlap {ov}% > 1 (ungated)")
    con.execute("INSERT OR REPLACE INTO duopoly_daily(snapshot_utc,day,copart_snapshot,copart_us_lots,copart_total_lots,iaa_vehicles,iaa_branches,iaa_auctions,"
                "copart_share_pct,iaa_lastmod_4day_pct,note,iaa_complete,copart_overlap_pct,usable) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (SNAP, TODAY, cp_snap, us, tot, len(veh_u), len(set(x[1] for x in br)), len(auc), share, round(pct4, 1), "; ".join(notes), iaa_complete, ov, usable))
    print(f"\nDUOPOLY {TODAY}: Copart US {us:,} (total {tot:,}, overlap {ov}%, snap {cp_snap}) | IAA US {len(veh_u):,}{'' if iaa_complete else ' PARTIAL'} | "
          f"Copart share {('%.1f%%' % share) if share is not None else 'n/a'} | usable={usable}  {'; '.join(notes)}")
con.commit()
rows = con.execute("SELECT * FROM duopoly_daily ORDER BY snapshot_utc").fetchall()
cols = [d[1] for d in con.execute("PRAGMA table_info(duopoly_daily)")]
con.close()
with open(ROOT / "data/csv/duopoly_daily.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(cols); w.writerows(rows)
print(f"-> data/csv/duopoly_daily.csv ({len(rows)} rows)")
sys.exit(0 if veh_u else 1)
