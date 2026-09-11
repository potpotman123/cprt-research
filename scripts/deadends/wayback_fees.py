import sys,os,re,time,pathlib,urllib.request,urllib.parse,collections
ROOT=pathlib.Path(__file__).resolve().parent.parent.parent
UA="CPRT-Research/1.0 (+academic equity research; contact: kendall_wu@college.harvard.edu)"
def req(u,t=120):
    r=urllib.request.Request(u,headers={"User-Agent":UA})
    for a in range(4):
        try:
            with urllib.request.urlopen(r,timeout=t) as x: return x.status,x.read()
        except Exception as e: print(f"   retry{a+1} {type(e).__name__}",flush=True); time.sleep(8*(a+1))
    return -1,b""
os.makedirs(ROOT/"raw/fees",exist_ok=True)
# collapse to one capture per (url, yyyymm) so we sample the fee schedule over time
targets=["copart.com/content/us/en/premier-member-fees","copart.com/Content/US/EN/Basic-Member-Fees",
         "copart.com/content/us/en/member-fees-us-licensed"]
for tgt in targets:
    u=("https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(
       {"url":tgt,"fl":"original,timestamp,statuscode","filter":"statuscode:200","limit":400},safe=":*.?=&"))
    s,b=req(u); caps=[]
    for line in b.decode("utf-8","replace").splitlines():
        p=line.split()
        if len(p)>=2 and re.fullmatch(r'\d{14}',p[1]): caps.append((p[0],p[1]))
    bymon={}
    for o,ts in caps: bymon.setdefault(ts[:6],(o,ts))
    print(f"=== {tgt}: {len(caps)} caps -> {len(bymon)} months ===",flush=True)
    time.sleep(4)
    for mon,(o,ts) in sorted(bymon.items()):
        name=re.sub(r'[^A-Za-z0-9]+','_',tgt)+f"_{ts}.html"
        out=ROOT/"raw/fees"/name
        if out.exists() and out.stat().st_size>2000: continue
        st,body=req(f"https://web.archive.org/web/{ts}id_/{o}")
        if st==200 and len(body)>2000:
            out.write_bytes(body); print(f"  {mon} {ts} {len(body):>8,}b ok",flush=True)
        else: print(f"  {mon} {ts} st={st} len={len(body)} skip",flush=True)
        time.sleep(5)
print("DONE",flush=True)
