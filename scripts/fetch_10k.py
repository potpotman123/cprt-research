import sys, json, pathlib, os
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent)); import prov
ROOT=pathlib.Path(__file__).resolve().parent.parent
d=json.load(open(ROOT/"raw/sec/submissions_CIK0000900075.json")); r=d["filings"]["recent"]
BASIS="www.sec.gov/robots.txt allows /Archives/; SEC public EDGAR full-text archive; descriptive UA w/ contact required by SEC fair-access policy"
targets=[]
for i in range(len(r["form"])):
    if r["form"][i]=="10-K" and r["reportDate"][i][:4] >= "2016":
        acc=r["accessionNumber"][i].replace("-","")
        targets.append((r["reportDate"][i], f"https://www.sec.gov/Archives/edgar/data/900075/{acc}/{r['primaryDocument'][i]}"))
os.makedirs(ROOT/"raw/sec/10k",exist_ok=True)
for rd,u in sorted(targets):
    out=f"raw/sec/10k/cprt_{rd}.htm"
    if (ROOT/out).exists(): print(f"  have {rd}"); continue
    s,b=prov.get(u,"allowed",BASIS,note=f"Job4 10-K FY{rd[:4]} primary doc",save_to=out)
    print(f"  {s} {len(b)/1e6:.2f}MB  FY{rd[:4]}  {u.rsplit('/',1)[1]}",flush=True)
