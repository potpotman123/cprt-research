import re,html,glob,csv,sqlite3,pathlib,collections
ROOT=pathlib.Path(__file__).resolve().parent.parent
def text(p):
    s=open(p,encoding='utf-8',errors='replace').read()
    s=re.sub(r'(?is)<(script|style).*?</\1>',' ',s); s=re.sub(r'(?s)<[^>]+>',' ',s)
    return re.sub(r'[\s ]+',' ',html.unescape(s))
LINES=[("land",r'Land'),
       ("buildings",r'Buildings and (?:leasehold )?improvements'),
       ("transport",r'Transportation and other equipment'),
       ("office",r'Office furniture and equipment'),
       ("software",r'(?:Internal-use s|S)oftware')]
comp=collections.defaultdict(lambda: collections.defaultdict(dict))
for f in sorted(glob.glob(str(ROOT/"raw/sec/10k/cprt_*.htm"))):
    fy=int(re.search(r'cprt_(\d{4})',f).group(1)); t=text(f)
    m=re.search(r'Property and equipment,? net consisted of the following:?\s*(.{0,1600})',t)
    if not m: continue
    seg=m.group(1)
    ys=re.search(r'(20\d{2})\s+(20\d{2})',seg)
    y1,y2=(int(ys.group(1)),int(ys.group(2))) if ys else (fy,fy-1)
    for key,pat in LINES:
        mm=re.search(pat+r'\s*\$?\s*\(?([\d,]+)\)?\s*\$?\s*\(?([\d,]+)\)?',seg)
        if mm:
            comp[key][y1][fy]=float(mm.group(1).replace(",",""))/1000.0
            comp[key][y2][fy]=float(mm.group(2).replace(",",""))/1000.0
def pick(k,y):
    d=comp[k].get(y)
    return d[max(d)] if d else None
con=sqlite3.connect(ROOT/"data/cprt.db")
sec={r[0]:r for r in con.execute("SELECT fy,total_revenue,operating_income,d_and_a,capex FROM sec_annual")}
print(f"{'FY':<5}{'dLand':>8}{'dBldg':>8}{'dTrans':>8}{'dOffice':>8}{'dSoft':>8}{'SUMd':>9}{'Capex':>9}{'D&A':>8}{'Growth':>8}{'Maint':>8}{'M-D&A':>8}")
out=[]
for fy in range(2016,2026):
    g={k:(pick(k,fy),pick(k,fy-1)) for k,_ in LINES}
    d={k:(a-b) if None not in (a,b) else None for k,(a,b) in g.items()}
    row=sec.get(fy); capex=row[4]/1e6 if row and row[4] else None
    da=row[3]/1e6 if row and row[3] else None; ebit=row[2]/1e6 if row and row[2] else None
    vals=[d[k] for k,_ in LINES]
    sumd=sum(v for v in vals if v is not None) if all(v is not None for v in vals) else None
    growth=(d["land"]+d["buildings"]) if None not in (d["land"],d["buildings"]) else None
    maint=(capex-growth) if None not in (capex,growth) else None
    mda=(maint-da) if None not in (maint,da) else None
    f=lambda x,w=8: (" "*w if x is None else f"{x:>{w},.1f}")
    print(f"{fy:<5}{f(d['land'])}{f(d['buildings'])}{f(d['transport'])}{f(d['office'])}{f(d['software'])}"
          f"{f(sumd,9)}{f(capex,9)}{f(da)}{f(growth)}{f(maint)}{f(mda)}")
    out.append(dict(fy=fy,d_land=d['land'],d_buildings=d['buildings'],d_transport=d['transport'],
        d_office=d['office'],d_software=d['software'],sum_delta_gross=sumd,capex=capex,da=da,
        growth_capex=growth,maint_capex=maint,maint_minus_da=mda,ebit=ebit,
        owner_earnings=(ebit+da-maint) if None not in (ebit,da,maint) else None))
con.execute("DROP TABLE IF EXISTS capex_decomp")
cols=list(out[0].keys())
con.execute(f"CREATE TABLE capex_decomp(fy INT PRIMARY KEY,{','.join(c+' REAL' for c in cols[1:])})")
con.executemany(f"INSERT INTO capex_decomp VALUES({','.join(':'+c for c in cols)})",out)
con.commit()
with open(ROOT/"data/csv/capex_decomp.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); w.writerows(out)
print("\n=== maint_capex / D&A ratio ===")
for r in out:
    if r["maint_capex"] and r["da"]:
        print(f"  FY{r['fy']}: maint={r['maint_capex']:>7,.1f}  D&A={r['da']:>6,.1f}  ratio={r['maint_capex']/r['da']:.2f}  OE={r['owner_earnings']:>8,.1f}")
