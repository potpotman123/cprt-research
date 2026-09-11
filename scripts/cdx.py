import sys, time, urllib.request, urllib.parse, os
UA="CPRT-Research/1.0 (+academic equity research; contact: kendall_wu@college.harvard.edu)"
def page(params):
    u="https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(params,safe=":*.[]")
    r=urllib.request.Request(u,headers={"User-Agent":UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(r,timeout=180): pass
        except Exception: pass
        try:
            with urllib.request.urlopen(r,timeout=180) as resp: return resp.read().decode("utf-8","replace")
        except Exception as e:
            print(f"   retry {attempt+1}: {e}",flush=True); time.sleep(5)
    return ""
def fetch_all(target, out, extra=None, pagesize=20000, maxpages=40):
    rows=[]; rk=None; n=0
    while n<maxpages:
        n+=1
        p={"url":target,"fl":"original,timestamp,statuscode","filter":"statuscode:200",
           "limit":pagesize,"showResumeKey":"true"}
        if extra: p.update(extra)
        if rk: p["resumeKey"]=rk
        txt=page(p)
        if not txt.strip(): break
        lines=txt.split("\n")
        # resumeKey (if any) is the last non-empty line, preceded by a blank line
        newrk=None
        nonempty=[i for i,l in enumerate(lines) if l.strip()]
        if nonempty:
            last=nonempty[-1]
            if last>0 and not lines[last-1].strip() and " " not in lines[last].strip():
                newrk=lines[last].strip(); lines=lines[:last-1]
        chunk=[l for l in lines if l.strip()]
        rows+=chunk
        print(f"  page {n}: +{len(chunk)} rows, total={len(rows)}, rk={'yes' if newrk else 'none'}",flush=True)
        rk=newrk
        if not rk: break
        time.sleep(2)
    with open(out,"w") as f: f.write("\n".join(rows)+"\n")
    return rows
if __name__=="__main__":
    tgt,out=sys.argv[1],sys.argv[2]
    print(f"=== CDX {tgt} ===")
    rows=fetch_all(tgt,out)
    print(f"TOTAL {len(rows)} rows -> {out}")
