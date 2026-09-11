import sys,os,re,time,pathlib,urllib.request
ROOT=pathlib.Path(__file__).resolve().parent.parent
UA=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
H={"User-Agent":UA,"Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip",
   "From":"kendall_wu@college.harvard.edu"}
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
            print(f"    retry{a+1} {type(e).__name__}",flush=True); time.sleep(12*(a+1))
    return -1,b""
for pg in (4,5,6):
    u=("https://web.archive.org/cdx/search/cdx?"
       f"url=copart.com/lot.xml%3Fpage%3D{pg}&fl=original,timestamp,statuscode&filter=statuscode:200&limit=200")
    s,b=req(u); caps=[]
    for line in b.decode("utf-8","replace").splitlines():
        p=line.split()
        if len(p)>=2 and re.fullmatch(r'\d{14}',p[1]): caps.append((p[0],p[1]))
    print(f"=== page {pg}: {len(caps)} captures ===",flush=True); time.sleep(5)
    if not caps: continue
    for orig,ts in caps:
        out=ROOT/"raw/lotxml"/f"lotxml_p{pg}_{ts}.xml"
        if out.exists(): continue
        st,body=req(f"https://web.archive.org/web/{ts}id_/{orig}")
        # keep even small/empty bodies - an EMPTY page 4 is the signal that inventory shrank
        out.write_bytes(body if st==200 else b"")
        print(f"  p{pg} {ts} st={st} {len(body):>10,}b locs={body.count(b'<loc>'):,}",flush=True)
        time.sleep(5)
print("DONE",flush=True)
