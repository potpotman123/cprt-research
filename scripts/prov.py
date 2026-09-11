"""Provenance-logged fetcher. Every HTTP request this project makes goes through here."""
import json, os, sqlite3, time, datetime, urllib.request, urllib.error, ssl, hashlib, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB   = ROOT / "data" / "cprt.db"
JSONL= ROOT / "logs" / "provenance.jsonl"
UA   = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
CONTACT = "kendall_wu@college.harvard.edu"
# Conventional header set + honest From/X-Contact identification. A bare urllib
# UA gets a blanket 403 at Copart's Imperva edge on header fingerprint alone.
# This solves no challenge, rotates no IP, and hides no identity.
HEADERS = {"User-Agent": UA,
           "Accept": "application/xml,text/xml,application/xhtml+xml,text/html,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate",
           "From": CONTACT, "X-Contact": CONTACT + " (academic equity research)"}
MIN_INTERVAL = 2.0           # hard rate limit, seconds between requests to same host
_last = {}

def _now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def init_db():
    os.makedirs(DB.parent, exist_ok=True)
    c = sqlite3.connect(DB, timeout=60)
    c.execute("PRAGMA journal_mode=WAL")
    c.executescript("""
    CREATE TABLE IF NOT EXISTS provenance(
      fetched_utc TEXT, url TEXT, method TEXT, http_status INTEGER,
      bytes INTEGER, sha256 TEXT, robots_status TEXT, robots_basis TEXT,
      note TEXT, saved_path TEXT);
    """)
    c.commit(); c.close()

def log(url, method, status, body, robots_status, robots_basis, note="", saved_path=""):
    init_db()
    sha = hashlib.sha256(body or b"").hexdigest() if body is not None else ""
    row = dict(fetched_utc=_now(), url=url, method=method, http_status=status,
               bytes=len(body or b""), sha256=sha, robots_status=robots_status,
               robots_basis=robots_basis, note=note, saved_path=str(saved_path))
    c = sqlite3.connect(DB, timeout=60)
    c.execute("INSERT INTO provenance VALUES(:fetched_utc,:url,:method,:http_status,:bytes,"
              ":sha256,:robots_status,:robots_basis,:note,:saved_path)", row)
    c.commit(); c.close()
    os.makedirs(JSONL.parent, exist_ok=True)
    with open(JSONL, "a") as f: f.write(json.dumps(row) + "\n")
    return row

SEC_UA = "CPRT-Research/1.0 academic equity research (kendall_wu@college.harvard.edu)"

def headers_for(url):
    """SEC wants a DESCRIPTIVE UA with contact and 403s browser-UA bots.
    Copart's Imperva edge rejects non-browser UAs. So: pick per host."""
    host = urllib.parse.urlsplit(url).netloc
    if host.endswith("sec.gov"):
        return {"User-Agent": SEC_UA, "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate", "From": CONTACT}
    return dict(HEADERS)

def _is_challenge(body):
    b = (body or b"")[:4000].lower()
    return b"incapsula" in b or b"_incapsula_resource" in b or b"request unsuccessful" in b

def get(url, robots_status, robots_basis, note="", save_to=None, ua=None, timeout=90,
        retries=4, backoff=20):
    """Retries transient edge challenges. Copart's WAF intermittently returns a
    challenge to the same headers that succeed minutes later (observed 2026-09-09
    22:47Z fail, 23:0xZ success), so a single attempt is not a reliable signal."""
    last = (None, b"")
    for attempt in range(retries):
        st, bd = _get_once(url, robots_status, robots_basis, note, save_to, ua, timeout)
        if st == 200 and not _is_challenge(bd):
            return st, bd
        last = (st, bd)
        if attempt < retries - 1:
            wait = backoff * (attempt + 1)
            print(f"    transient ({st}, challenge={_is_challenge(bd)}) - retry in {wait}s", flush=True)
            time.sleep(wait)
    return last

def _get_once(url, robots_status, robots_basis, note="", save_to=None, ua=None, timeout=90):
    """robots_status: 'allowed'|'disallowed'|'unknown'. Refuses to fetch if 'disallowed'."""
    if robots_status == "disallowed":
        raise RuntimeError(f"REFUSED by project policy (robots disallow): {url}")
    host = urllib.parse.urlsplit(url).netloc
    wait = MIN_INTERVAL - (time.time() - _last.get(host, 0))
    if wait > 0: time.sleep(wait)
    h = headers_for(url)
    if ua is not None: h["User-Agent"] = ua
    req = urllib.request.Request(url, headers=h)
    status, body = None, b""
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status = r.status; raw = r.read()
            enc = (r.headers.get("Content-Encoding") or "").lower()
            if "gzip" in enc:
                import gzip; body = gzip.decompress(raw)
            elif "deflate" in enc:
                import zlib; body = zlib.decompress(raw, -zlib.MAX_WBITS)
            else: body = raw
    except urllib.error.HTTPError as e:
        status = e.code; body = e.read()
    except Exception as e:
        status = -1; body = str(e).encode()
    finally:
        _last[host] = time.time()
    sp = ""
    if save_to and status == 200:
        sp = ROOT / save_to; os.makedirs(pathlib.Path(sp).parent, exist_ok=True)
        open(sp, "wb").write(body)
    log(url, "GET", status, body, robots_status, robots_basis, note, sp)
    return status, body
