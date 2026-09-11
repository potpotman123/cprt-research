"""Structural nowcast: do public monthly macro series predict Copart's ASP and units?

Inputs (FRED, monthly, no API key, decades of history):
  CUSR0000SETA02      CPI: Used Cars & Trucks   -> ASP driver
  TRFVOLUSM227NFWA    Vehicle Miles Traveled    -> accident-frequency / assignment driver
Targets (from Copart's own calls, via reported_units + stephens_exhibit7):
  us_ins_asp_yoy, global_asp_yoy, us_total_units_yoy, us_ins_units_yoy
"""
import sys,csv,io,sqlite3,datetime,statistics,math,pathlib,urllib.request
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent)); import prov
ROOT=pathlib.Path(__file__).resolve().parent.parent
B="fred.stlouisfed.org public CSV endpoint; no key required; robots permits /graph/"
SER={"cpi_used_cars":"CUSR0000SETA02","vmt":"TRFVOLUSM227NFWA"}
data={}
for name,sid in SER.items():
    # fetched with curl to raw/fred/ (prov's header set hangs on FRED); provenance logged manually
    rows=list(csv.reader(open(ROOT/f"raw/fred/{sid}.csv")))
    prov.log(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}","GET",200,
             open(ROOT/f"raw/fred/{sid}.csv","rb").read(),"allowed",B,
             f"Job5 nowcast {name} (curl)",f"raw/fred/{sid}.csv")
    hdr=rows[0]; d={}
    for r in rows[1:]:
        if len(r)<2 or not r[1].strip() or r[1]=='.': continue
        d[r[0][:7]]=float(r[1])
    data[name]=d
    print(f"  {name} ({sid}): {len(d)} monthly obs, {min(d)} .. {max(d)}")
# Copart fiscal quarters -> the 3 calendar months they cover
FQ={"FY2023 Q1":("2022-08","2022-09","2022-10"),"FY2023 Q2":("2022-11","2022-12","2023-01"),
    "FY2023 Q3":("2023-02","2023-03","2023-04"),"FY2023 Q4":("2023-05","2023-06","2023-07"),
    "FY2024 Q1":("2023-08","2023-09","2023-10"),"FY2024 Q2":("2023-11","2023-12","2024-01"),
    "FY2024 Q3":("2024-02","2024-03","2024-04"),"FY2024 Q4":("2024-05","2024-06","2024-07"),
    "FY2025 Q1":("2024-08","2024-09","2024-10"),"FY2025 Q2":("2024-11","2024-12","2025-01"),
    "FY2025 Q3":("2025-02","2025-03","2025-04"),"FY2025 Q4":("2025-05","2025-06","2025-07"),
    "FY2026 Q1":("2025-08","2025-09","2025-10"),"FY2026 Q2":("2025-11","2025-12","2026-01"),
    "FY2026 Q3":("2026-02","2026-03","2026-04"),"FY2026 Q4":("2026-05","2026-06","2026-07")}
def qavg(d,months):
    v=[d[m] for m in months if m in d]
    return statistics.mean(v) if len(v)==len(months) else None
def qyoy(d,fq):
    m=FQ[fq]; cur=qavg(d,m)
    py=tuple(f"{int(x[:4])-1}{x[4:]}" for x in m); pri=qavg(d,py)
    return ((cur/pri-1)*100) if (cur and pri) else None
con=sqlite3.connect(ROOT/"data/cprt.db")
rep={r[0]:r for r in con.execute("SELECT fiscal_q,us_ins_asp_yoy,us_ins_units_yoy FROM reported_units")}
st={r[0]:r for r in con.execute("SELECT fiscal_q,us_total_units_yoy,global_asp_yoy FROM stephens_exhibit7")}
print(f"\n{'quarter':<11}{'CPI used YoY':>14}{'VMT YoY':>10}{'CPRT ins ASP':>14}{'CPRT glob ASP':>15}{'CPRT US units':>15}")
rows=[]
for fq in FQ:
    c=qyoy(data["cpi_used_cars"],fq); v=qyoy(data["vmt"],fq)
    a=rep.get(fq,(None,None,None))[1]; ga=st.get(fq,(None,None,None))[2]; u=st.get(fq,(None,None,None))[1]
    f=lambda x,w: (" "*w if x is None else f"{x:>+{w-1}.1f}%")
    print(f"{fq:<11}{f(c,14)}{f(v,10)}{f(a,14)}{f(ga,15)}{f(u,15)}")
    rows.append((fq,c,v,a,ga,u))
def reg(pairs,lab):
    P=[(x,y) for x,y in pairs if x is not None and y is not None]
    n=len(P)
    if n<5: print(f"  {lab}: n={n} too few"); return
    X=[p[0] for p in P]; Y=[p[1] for p in P]
    mx=sum(X)/n; my=sum(Y)/n
    sxy=sum((a-mx)*(b-my) for a,b in zip(X,Y)); sxx=sum((a-mx)**2 for a in X); syy=sum((b-my)**2 for b in Y)
    r=sxy/(sxx*syy)**.5; beta=sxy/sxx; alpha=my-beta*mx
    resid=[y-(alpha+beta*x) for x,y in zip(X,Y)]
    se=math.sqrt(sum(e*e for e in resid)/(n-2)/sxx)
    print(f"  {lab:<44} n={n:<3} r={r:+.3f} R2={r*r:.3f} beta={beta:+.3f} (se {se:.3f}) rmse={statistics.stdev(resid):.2f}pp")
    return alpha,beta,r
print("\n=== DOES CPI USED CARS PREDICT COPART ASP? ===")
f1=reg([(r[1],r[3]) for r in rows],"CPI used cars -> CPRT US insurance ASP")
reg([(r[1],r[4]) for r in rows],"CPI used cars -> CPRT global ASP")
print("\n=== DOES VMT PREDICT COPART UNITS? ===")
reg([(r[2],r[5]) for r in rows],"VMT -> CPRT US total units")
reg([(r[2],r[3]) for r in rows],"VMT -> CPRT US insurance ASP (control)")
print("\n=== LAGGED: CPI/VMT one quarter EARLIER -> Copart this quarter ===")
ks=list(FQ)
reg([(rows[i-1][1],rows[i][3]) for i in range(1,len(rows))],"CPI(t-1) -> ASP(t)")
reg([(rows[i-1][2],rows[i][5]) for i in range(1,len(rows))],"VMT(t-1) -> US units(t)")
