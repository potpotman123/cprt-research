#!/usr/bin/env python3
"""Logged, robots-checked fetch (CLI). Wraps scripts/prov.py so every request this project makes is
robots-checked first, rate-limited per host across processes, logged to logs/provenance.jsonl and
data/cprt.db, and saved to disk. Added 2026-09-30 for the catalyst-search session.

Usage:
  python3 scripts/fetch_logged.py URL --save raw/dir/file.ext --note "why" [--retries 2] [--refresh-robots]
Exit codes: 0 fetched (HTTP 200, no challenge); 2 refused (robots disallow); 3 challenge/interstitial; 1 other.
Prints one JSON line: url, host, robots, robots_basis, crawl_delay, status, bytes, challenge, saved, result.
"""
import sys, json, time, argparse, pathlib, urllib.parse, urllib.robotparser
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import prov

ROBOTS_DIR = prov.ROOT / "raw" / "robots"


def robots_check(url, note, refresh=False):
    sp = urllib.parse.urlsplit(url)
    host = sp.netloc
    robots_url = f"{sp.scheme}://{host}/robots.txt"
    cache = ROBOTS_DIR / f"{host}.txt"
    if cache.exists() and cache.stat().st_size > 0 and not refresh:
        body, status = cache.read_bytes(), 200
        basis = f"cached {cache.relative_to(prov.ROOT)}"
    else:
        status, body = prov.get(robots_url, "allowed", "robots.txt is the policy file itself",
                                note=f"robots.txt for: {note}", save_to=str(cache.relative_to(prov.ROOT)), retries=1)
        basis = f"fetched {robots_url} -> HTTP {status}"
    if status == 404:
        return "allowed", basis + " (no robots.txt)", None
    if status != 200 or prov._is_challenge(body):
        return "unknown", basis + " (robots.txt unreadable; flagged, not a violation)", None
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(body.decode("utf-8", "replace").splitlines())
    ua = prov.headers_for(url)["User-Agent"]
    ok = rp.can_fetch(ua, url) and rp.can_fetch("*", url)
    delay = rp.crawl_delay(ua) or rp.crawl_delay("*")
    return ("allowed" if ok else "disallowed"), basis + f"; can_fetch={ok}", delay


def wait_for_host(host, delay):
    """Cross-process per-host spacing: max(prov.MIN_INTERVAL, robots Crawl-delay)."""
    gap = max(prov.MIN_INTERVAL, float(delay or 0))
    stamp = ROBOTS_DIR / f".last_{host}"
    try:
        last = float(stamp.read_text())
    except Exception:
        last = 0.0
    w = gap - (time.time() - last)
    if w > 0:
        time.sleep(w)
    stamp.write_text(str(time.time()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--save", required=True, help="path relative to repo root")
    ap.add_argument("--note", required=True)
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--refresh-robots", action="store_true")
    a = ap.parse_args()
    host = urllib.parse.urlsplit(a.url).netloc
    ROBOTS_DIR.mkdir(parents=True, exist_ok=True)
    wait_for_host(host, None)
    rstatus, rbasis, delay = robots_check(a.url, a.note, a.refresh_robots)
    out = {"url": a.url, "host": host, "robots": rstatus, "robots_basis": rbasis, "crawl_delay": delay}
    if rstatus == "disallowed":
        out.update(status=None, bytes=0, challenge=False, saved="", result="REFUSED robots disallow")
        print(json.dumps(out))
        return 2
    wait_for_host(host, delay)
    st, body = prov.get(a.url, rstatus, rbasis, note=a.note, save_to=a.save, retries=a.retries, backoff=10)
    ch = prov._is_challenge(body)
    ok = (st == 200 and not ch)
    out.update(status=st, bytes=len(body or b""), challenge=ch, saved=str(prov.ROOT / a.save) if ok else "",
               result="OK" if ok else ("CHALLENGE" if ch else f"HTTP {st}"))
    print(json.dumps(out))
    return 0 if ok else (3 if ch else 1)


if __name__ == "__main__":
    sys.exit(main())
