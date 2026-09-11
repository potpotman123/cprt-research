import sys,json,re,os,html,pathlib,csv,sqlite3
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent)); import prov
ROOT=pathlib.Path(__file__).resolve().parent.parent
B="sec.gov/Archives public EDGAR; descriptive UA w/ contact"
os.makedirs(ROOT/"raw/sec/job5",exist_ok=True)
d=json.load(open(ROOT/"raw/sec/submissions_CIK0001046102.json")); r=d["filings"]["recent"]
jobs=[(r["filingDate"][i],r["accessionNumber"][i]) for i in range(len(r["form"]))
      if r["form"][i]=="8-K" and "2.02" in (r["items"][i] or "")]
print(f"RB Global earnings 8-Ks available: {len(jobs)}")
def txt(b):
    s=b.decode("utf-8","replace")
    s=re.sub(r'(?is)<(script|style).*?</\1>',' ',s); s=re.sub(r'(?s)<[^>]+>',' ',s)
    return re.sub(r'\s+',' ',html.unescape(s))
out=[]
for fd,acc in sorted(jobs,reverse=True)[:10]:
    a=acc.replace("-","")
    s,b=prov.get(f"https://www.sec.gov/Archives/edgar/data/1046102/{a}/index.json","allowed",B,note=f"RBA idx {fd}")
    if s!=200: continue
    ex=[i["name"] for i in json.loads(b)["directory"]["item"]
        if re.search(r'ex.?99',i["name"],re.I) and i["name"].lower().endswith((".htm",".html"))]
    if not ex: continue
    s2,b2=prov.get(f"https://www.sec.gov/Archives/edgar/data/1046102/{a}/{ex[0]}","allowed",B,
                   note=f"RBA earnings {fd}",save_to=f"raw/sec/job5/RBA_{fd}_{ex[0]}")
    if s2!=200: continue
    t=txt(b2)
    # the six-quarter lots-sold table
    m=re.search(r'lots sold by sector for each of the last six fiscal quarters.{0,400}?'
                r'\(in thousands\)((?:\s*\w+ \d+, \d{4}){6})\s*Automotive((?:\s*[\d.]+){6})',t,re.I)
    if m:
        qs=re.findall(r'\w+ \d+, \d{4}',m.group(1)); vals=re.findall(r'[\d.]+',m.group(2))
        for q,v in zip(qs,vals): out.append((fd,q,float(v)))
        print(f"  {fd}: got 6 quarters -> {list(zip(qs,vals))[:2]}...")
    else:
        m2=re.search(r'Automotive\s+([\d.]+)\s+([\d.]+)\s+(\(?\d+\)?)\s*%',t)
        print(f"  {fd}: six-qtr table not matched" + (f"; single-qtr Automotive={m2.group(1)}" if m2 else ""))
# dedupe: latest filing wins per quarter
best={}
for fd,q,v in out:
    if q not in best or fd>best[q][0]: best[q]=(fd,v)
import datetime
def key(q):
    return datetime.datetime.strptime(q,"%B %d, %Y")
print(f"\n=== RB GLOBAL: Automotive lots sold (thousands), quarterly ===")
print(f"  {'quarter end':<18}{'lots (k)':>10}{'YoY':>9}   source filing")
ser=sorted(best.items(),key=lambda x:key(x[0]))
D={q:v for q,(fd,v) in ser}
for q,(fd,v) in ser:
    d0=key(q); prior=None
    for q2,(f2,v2) in ser:
        dd=key(q2)
        if 330<=(d0-dd).days<=400: prior=v2
    yy=f"{(v/prior-1)*100:+.1f}%" if prior else ""
    print(f"  {q:<18}{v:>10.1f}{yy:>9}   {fd}")
con=sqlite3.connect(ROOT/"data/cprt.db",timeout=60)
con.execute("DROP TABLE IF EXISTS rba_automotive_units")
con.execute("CREATE TABLE rba_automotive_units(quarter_end TEXT PRIMARY KEY,lots_thousands REAL,source_filing TEXT)")
con.executemany("INSERT INTO rba_automotive_units VALUES(?,?,?)",[(q,v,fd) for q,(fd,v) in ser])
con.commit()
with open(ROOT/"data/csv/rba_automotive_units.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["quarter_end","lots_thousands","source_filing"]); w.writerows([(q,v,fd) for q,(fd,v) in ser])
print(f"\n{len(ser)} quarters -> data/csv/rba_automotive_units.csv")
