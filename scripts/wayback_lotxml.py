import sys,os,re,time,pathlib,urllib.request,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parent.parent
UA=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
H={"User-Agent":UA,"Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip",
   "From":"kendall_wu@college.harvard.edu"}
SLEEP=5.0
def req(u,t=180):
    r=urllib.request.Request(u,headers=H)
    for a in range(5):
        try:
            with urllib.request.urlopen(r,timeout=t) as x:
                raw=x.read()
                if (x.headers.get("Content-Encoding") or "")=="gzip":
                    import gzip
                    try: raw=gzip.decompress(raw)
                    except Exception: pass
                return x.status,raw
        except Exception as e:
            print(f"    retry{a+1} {type(e).__name__}",flush=True); time.sleep(10*(a+1))
    return -1,b""
os.makedirs(ROOT/"raw/lotxml",exist_ok=True)
TARGETS=["copart.com/lot.xml","copart.com/lot.xml%3Fpage%3D1",
         "copart.com/lot.xml%3Fpage%3D2","copart.com/lot.xml%3Fpage%3D3"]
for tgt in TARGETS:
    u=("https://web.archive.org/cdx/search/cdx?"
       f"url={tgt}&fl=original,timestamp,statuscode&filter=statuscode:200&limit=200")
    s,b=req(u); caps=[]
    for line in b.decode("utf-8","replace").splitlines():
        p=line.split()
        if len(p)>=2 and re.fullmatch(r'\d{14}',p[1]): caps.append((p[0],p[1]))
    print(f"=== {tgt}: {len(caps)} captures ===",flush=True); time.sleep(SLEEP)
    for orig,ts in caps:
        page=re.search(r'page=(\d)',orig); pg=page.group(1) if page else "0"
        out=ROOT/"raw/lotxml"/f"lotxml_p{pg}_{ts}.xml"
        if out.exists() and out.stat().st_size>100_000: continue
        st,body=req(f"https://web.archive.org/web/{ts}id_/{orig}")
        if st==200 and len(body)>100_000:
            out.write_bytes(body)
            print(f"  p{pg} {ts} {len(body):>10,}b  locs~{body.count(b'<loc>'):,}",flush=True)
        else:
            print(f"  p{pg} {ts} st={st} len={len(body)} SKIP",flush=True)
        time.sleep(SLEEP)
print("DONE",flush=True)
