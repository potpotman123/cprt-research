import sys,os,re,time,pathlib,urllib.request,urllib.parse,sqlite3,csv,collections,datetime
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
ROOT=pathlib.Path(__file__).resolve().parent.parent
UA="CPRT-Research/1.0 (+academic equity research; contact: kendall_wu@college.harvard.edu)"
SLEEP=5.0
def req(u,timeout=120):
    r=urllib.request.Request(u,headers={"User-Agent":UA})
    for a in range(5):
        try:
            with urllib.request.urlopen(r,timeout=timeout) as resp: return resp.status,resp.read()
        except Exception as e:
            print(f"    retry{a+1} {type(e).__name__}",flush=True); time.sleep(10*(a+1))
    return -1,b""
def cdx(target):
    u=("https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(
        {"url":target,"fl":"original,timestamp,statuscode","filter":"statuscode:200","limit":500},safe=":*.?=&"))
    s,b=req(u); rows=[]
    for line in b.decode("utf-8","replace").splitlines():
        p=line.split()
        if len(p)>=2 and re.fullmatch(r'\d{14}',p[1]): rows.append((p[0],p[1]))
    return rows
TARGETS=["copart.com/sale-list-results.xml","copart.com/CMS/en/content/location.xml"]
os.makedirs(ROOT/"raw/wayback",exist_ok=True)
allrows=[]
for tgt in TARGETS:
    caps=cdx(tgt); print(f"=== {tgt}: {len(caps)} captures (status 200) ===",flush=True); time.sleep(SLEEP)
    for orig,ts in caps:
        name=re.sub(r'[^A-Za-z0-9]+','_',tgt)+f"_{ts}.xml"
        out=ROOT/"raw/wayback"/name
        if out.exists() and out.stat().st_size>500:
            allrows.append((tgt,ts,str(out))); continue
        u=f"https://web.archive.org/web/{ts}id_/{orig}"
        s,b=req(u)
        if s==200 and len(b)>500:
            out.write_bytes(b); allrows.append((tgt,ts,str(out)))
            print(f"  {ts}  {len(b):>9,}b  ok",flush=True)
        else:
            print(f"  {ts}  status={s} len={len(b)}  SKIP",flush=True)
        time.sleep(SLEEP)
print(f"\nDOWNLOADED {len(allrows)} snapshots")
