import sys,json,re,html,pathlib,os
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent)); import prov
ROOT=pathlib.Path(__file__).resolve().parent.parent
BASIS="sec.gov/Archives public EDGAR; descriptive UA w/ contact per SEC fair-access policy"
d=json.load(open(ROOT/"raw/sec/submissions_CIK0000900075.json")); r=d["filings"]["recent"]
os.makedirs(ROOT/"raw/sec/8k",exist_ok=True)
jobs=[]
for i in range(len(r["form"])):
    if r["form"][i]=="8-K" and "2.02" in (r["items"][i] or "") and r["filingDate"][i]>="2021-08-01":
        jobs.append((r["filingDate"][i], r["accessionNumber"][i]))
print(f"earnings 8-Ks (item 2.02) to fetch: {len(jobs)}")
for fd,acc in sorted(jobs):
    a=acc.replace("-","")
    idx=f"https://www.sec.gov/Archives/edgar/data/900075/{a}/index.json"
    s,b=prov.get(idx,"allowed",BASIS,note=f"8-K index {fd}")
    if s!=200: print(f"  {fd} index http={s}"); continue
    items=json.loads(b)["directory"]["item"]
    ex=[it["name"] for it in items if re.search(r'ex.?99',it["name"],re.I) and it["name"].lower().endswith((".htm",".html",".txt"))]
    if not ex: print(f"  {fd} no EX-99 found: {[it['name'] for it in items][:6]}"); continue
    name=ex[0]
    out=f"raw/sec/8k/er_{fd}_{name}"
    if (ROOT/out).exists(): print(f"  have {fd}"); continue
    s2,b2=prov.get(f"https://www.sec.gov/Archives/edgar/data/900075/{a}/{name}","allowed",BASIS,
                   note=f"Q earnings release {fd}",save_to=out)
    print(f"  {fd}  {s2}  {len(b2)/1000:.0f}kb  {name}",flush=True)
