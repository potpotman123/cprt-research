import sqlite3,datetime,collections,statistics,pathlib,csv
ROOT=pathlib.Path(__file__).resolve().parent.parent
con=sqlite3.connect(ROOT/"data/cprt.db")
rows=con.execute("SELECT lot_id,first_seen FROM lot_first_seen").fetchall()
def dt(ts): return datetime.datetime.strptime(ts,"%Y%m%d%H%M%S")
# clean: keep plausible Copart lot ids (7-9 digits)
clean=[(l,dt(t)) for l,t in rows if 1_000_000<=l<200_000_000]
print(f"raw={len(rows):,}  after ID sanity filter (1M-200M)={len(clean):,}  dropped={len(rows)-len(clean)}")
clean.sort()
ids=[c[0] for c in clean]; ds=[c[1] for c in clean]
def spearman(x,y):
    n=len(x); rx=[0]*n; ry=[0]*n
    for arr,r in ((x,rx),(y,ry)):
        order=sorted(range(n),key=lambda i:arr[i]); i=0
        while i<n:
            j=i
            while j+1<n and arr[order[j+1]]==arr[order[i]]: j+=1
            avg=(i+j)/2+1
            for k in range(i,j+1): r[order[k]]=avg
            i=j+1
    mx=sum(rx)/n; my=sum(ry)/n
    num=sum((a-mx)*(b-my) for a,b in zip(rx,ry))
    den=(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))**.5
    return num/den if den else float('nan')
ep=[d.timestamp() for d in ds]
rho=spearman(ids,ep)
print(f"\nSPEARMAN rho(lot_id, first_seen) = {rho:.4f}   (1.0 = perfectly monotonic clock)")
# bucket by 1M
buck=collections.defaultdict(list)
for l,d in clean: buck[l//1_000_000].append(d)
print(f"\n{'bucket':<12}{'n':>7}{'median first_seen':>21}{'p10':>13}{'p90':>13}{'monotone?':>11}")
prev=None; inversions=[]; tbl=[]
for b in sorted(buck):
    v=sorted(buck[b]); n=len(v)
    if n<15: continue
    med=v[n//2]; p10=v[int(n*.10)]; p90=v[int(n*.90)]
    ok=""
    if prev is not None:
        if med<prev: ok="<-- INVERSION"; inversions.append((b,prev,med))
        else: ok="ok"
    print(f"{b:>3}M-{b+1}M{'':<3}{n:>7}{med.strftime('%Y-%m-%d'):>21}{p10.strftime('%Y-%m-%d'):>13}{p90.strftime('%Y-%m-%d'):>13}{ok:>11}")
    tbl.append((b,n,med.isoformat(),p10.isoformat(),p90.isoformat()))
    prev=med
print(f"\ninversions among populated buckets: {len(inversions)}")
for b,p,m in inversions: print(f"   bucket {b}M: median {m.date()} < previous {p.date()}")
with open(ROOT/"data/csv/lotid_monotonicity.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["bucket_millions","n","median_first_seen","p10","p90"]); w.writerows(tbl)
# dispersion: how tight is each bucket? (clock quality)
spans=[(b,(sorted(v)[int(len(v)*.9)]-sorted(v)[int(len(v)*.1)]).days) for b,v in buck.items() if len(v)>=15]
sp=[s for _,s in spans]
print(f"\nintra-bucket p10-p90 span (days): median={statistics.median(sp):.0f}  mean={statistics.mean(sp):.0f}  min={min(sp)}  max={max(sp)}")
