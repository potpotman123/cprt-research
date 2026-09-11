"""Backtest sitemap-derived inventory YoY against REPORTED US inventory YoY."""
import sqlite3,datetime,csv,pathlib,statistics
ROOT=pathlib.Path(__file__).resolve().parent.parent
con=sqlite3.connect(ROOT/"data/cprt.db")
inv={}
for m,t in con.execute("SELECT month,total_lots FROM inventory_level"): inv[m]=int(t)
# actual capture dates for each complete month
import re,glob,collections
cap={}
for f in glob.glob(str(ROOT/"raw/lotxml/lotxml_p1_*.xml")):
    ts=re.search(r'_(\d{14})',f).group(1)
    if ts[:6] in inv: cap[ts[:6]]=datetime.date(int(ts[:4]),int(ts[4:6]),int(ts[6:8]))
cap["202609"]=datetime.date(2026,9,8)
rep={r[0]:(r[1],r[2]) for r in con.execute("SELECT fiscal_q,call_date,us_inventory_yoy FROM reported_units")}
QE=[]  # quarter ends -> fiscal quarter
for y in range(2022,2028):
    QE+= [(datetime.date(y,7,31),f"FY{y} Q4"),(datetime.date(y,10,31),f"FY{y+1} Q1"),
          (datetime.date(y+1,1,31),f"FY{y+1} Q2"),(datetime.date(y+1,4,30),f"FY{y+1} Q3")]
def nearest_q(d,tol=45):
    best=min(QE,key=lambda x:abs((x[0]-d).days))
    return (best[1],best[0],abs((best[0]-d).days)) if abs((best[0]-d).days)<=tol else (None,None,None)
months=sorted(inv)
pairs=[]
for i,m2 in enumerate(months):
    d2=cap[m2]
    for m1 in months[:i]:
        d1=cap[m1]; gap=(d2-d1).days
        if 330<=gap<=400:
            yoy=(inv[m2]/inv[m1]-1)*100
            q,qd,off=nearest_q(d2)
            pairs.append((m1,m2,d1,d2,gap,yoy,q,off))
print(f"{'from':<9}{'to':<9}{'gap_d':>6}{'ours YoY':>10}{'-> quarter':>12}{'off_d':>7}{'reported':>10}{'error_pp':>10}")
X=[];Y=[];tbl=[]
for m1,m2,d1,d2,gap,yoy,q,off in pairs:
    r=rep.get(q,(None,None))[1] if q else None
    e=(yoy-r) if r is not None else None
    print(f"{m1:<9}{m2:<9}{gap:>6}{yoy:>+9.2f}%{(q or '-'):>12}{(off if off is not None else -1):>7}"
          f"{('   n/r  ' if r is None else f'{r:>+9.1f}%')}{('' if e is None else f'{e:>+10.2f}')}")
    if r is not None: X.append(r);Y.append(yoy);tbl.append((m1,m2,q,round(yoy,2),r,round(e,2)))
n=len(X)
mx=sum(X)/n; my=sum(Y)/n
sxy=sum((a-mx)*(b-my) for a,b in zip(X,Y)); sxx=sum((a-mx)**2 for a in X); syy=sum((b-my)**2 for b in Y)
r=sxy/(sxx*syy)**.5; beta=sxy/sxx; alpha=my-beta*mx
print(f"\n=== REGRESSION  ours = a + b * reported   (n={n}) ===")
print(f"  Pearson r = {r:.4f}    R^2 = {r*r:.4f}")
print(f"  beta (amplitude) = {beta:.3f}   -> our series is {beta:.2f}x the reported swing")
print(f"  alpha = {alpha:+.2f}pp")
print(f"  mean abs error (raw) = {statistics.mean(abs(y-x) for x,y in zip(X,Y)):.2f}pp")
cal=[(y-alpha)/beta for y in Y]
print(f"  mean abs error (calibrated: (ours-a)/b) = {statistics.mean(abs(c-x) for c,x in zip(cal,X)):.2f}pp")
print(f"\n{'quarter':<11}{'ours raw':>10}{'calibrated':>12}{'reported':>10}{'cal err':>9}")
for (m1,m2,q,yoy,rr,e),c in zip(tbl,cal):
    print(f"{q:<11}{yoy:>+9.2f}%{c:>+11.2f}%{rr:>+9.1f}%{c-rr:>+9.2f}")
# live prediction
live=[p for p in pairs if p[1]=="202609"]
if live:
    m1,m2,d1,d2,gap,yoy,q,off = live[0]
    pred=(yoy-alpha)/beta
    print(f"\n=== LIVE PREDICTION ===")
    print(f"  our {m1} -> {m2} ({d1} -> {d2}, {gap}d): {yoy:+.2f}% raw")
    print(f"  nearest quarter-end: {q} (snapshot is {off}d past it)")
    print(f"  CALIBRATED forecast for {q} reported US inventory YoY: {pred:+.1f}%")
    print(f"  (Q4 FY26 reports 2026-09-10. Reported FY26 Q1..Q3 were -17.0 / -8.1 / -4.7.)")
con.execute("DROP TABLE IF EXISTS backtest_pairs")
con.execute("""CREATE TABLE backtest_pairs(from_month TEXT,to_month TEXT,fiscal_q TEXT,
  ours_yoy REAL,reported_yoy REAL,error_pp REAL)""")
con.executemany("INSERT INTO backtest_pairs VALUES(?,?,?,?,?,?)",tbl); con.commit()
with open(ROOT/"data/csv/backtest_pairs.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["from_month","to_month","fiscal_q","ours_yoy","reported_yoy","error_pp"]); w.writerows(tbl)
