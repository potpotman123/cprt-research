import re,html,glob,csv,sqlite3,pathlib,collections
ROOT=pathlib.Path(__file__).resolve().parent.parent
def text(p):
    s=open(p,encoding='utf-8',errors='replace').read()
    s=re.sub(r'(?is)<(script|style).*?</\1>',' ',s)
    s=re.sub(r'(?s)<[^>]+>',' ',s); s=html.unescape(s)
    return re.sub(r'[\s ]+',' ',s)
def num(x): return float(x.replace(",","").replace("$","").strip())
land=collections.defaultdict(dict); dep=collections.defaultdict(dict); amort=collections.defaultdict(dict)
for f in sorted(glob.glob(str(ROOT/"raw/sec/10k/cprt_*.htm"))):
    fy=int(re.search(r'cprt_(\d{4})',f).group(1)); t=text(f)
    m=re.search(r'Property and equipment,? net consisted of the following:?\s*(.{0,1400})',t)
    if not m: print(f"FY{fy}: PP&E table NOT FOUND"); continue
    seg=m.group(1)
    yrs=re.match(r'.*?July 31,?\s*(?:\(In thousands\)\s*)?(\d{4})\s*(\d{4})',seg,re.S)
    if not yrs:
        yrs=re.search(r'(\d{4})\s+(\d{4})',seg)
    y1,y2=(int(yrs.group(1)),int(yrs.group(2))) if yrs else (fy,fy-1)
    lm=re.search(r'Land\s*\$?\s*([\d,]+)\s*\$?\s*([\d,]+)',seg)
    if lm:
        land[y1][fy]=num(lm.group(1))/1000.0; land[y2][fy]=num(lm.group(2))/1000.0
    dm=re.search(r'Depreciation expense on property and equipment was \$?\s*([\d.]+) million,?\s*\$?\s*([\d.]+) million,? and \$?\s*([\d.]+) million for the years ended July 31,?\s*(\d{4}),?\s*(\d{4}),? and \$?\s*(\d{4})',t)
    if dm:
        for i,yy in enumerate((int(dm.group(4)),int(dm.group(5)),int(dm.group(6)))):
            dep[yy][fy]=float(dm.group(i+1))
    am=re.search(r'Amortization expense of software was \$?\s*([\d.]+) million,?\s*\$?\s*([\d.]+) million,? and \$?\s*([\d.]+) million for the years ended July 31,?\s*(\d{4}),?\s*(\d{4}) and (\d{4})',t)
    if am:
        for i,yy in enumerate((int(am.group(4)),int(am.group(5)),int(am.group(6)))):
            amort[yy][fy]=float(am.group(i+1))
    print(f"FY{fy}: cols {y1}/{y2}  land={land[y1].get(fy)} / {land[y2].get(fy)}  dep={'y' if dm else 'n'} amort={'y' if am else 'n'}")
def pick(d,y):
    if y not in d or not d[y]: return None
    return d[y][max(d[y])]          # most recent filing's value
con=sqlite3.connect(ROOT/"data/cprt.db")
sec=dict((r[0],r) for r in con.execute("SELECT fy,total_revenue,operating_income,d_and_a,capex FROM sec_annual"))
out=[]
print(f"\n{'FY':<5}{'Land($M)':>10}{'dLand':>9}{'Capex':>9}{'NonLand':>9}{'D&A(xbrl)':>11}{'Dep+Amort':>11}{'NL-D&A':>9}{'EBIT':>9}{'OwnerErn':>10}")
for fy in range(2016,2026):
    L=pick(land,fy); Lp=pick(land,fy-1)
    dL=(L-Lp) if (L is not None and Lp is not None) else None
    row=sec.get(fy); capex=row[4] /1e6 if row and row[4] else None
    da=row[3]/1e6 if row and row[3] else None
    ebit=row[2]/1e6 if row and row[2] else None
    dp=pick(dep,fy); am=pick(amort,fy)
    dpam=(dp+am) if (dp is not None and am is not None) else None
    nonland=(capex-dL) if (capex is not None and dL is not None) else None
    diff=(nonland-da) if (nonland is not None and da is not None) else None
    oe=(ebit+da-nonland) if None not in (ebit,da,nonland) else None
    f=lambda x,w=9,p=1: (" "*w if x is None else f"{x:>{w},.{p}f}")
    print(f"{fy:<5}{f(L,10)}{f(dL)}{f(capex)}{f(nonland)}{f(da,11)}{f(dpam,11)}{f(diff)}{f(ebit)}{f(oe,10)}")
    out.append(dict(fy=fy,land=L,d_land=dL,capex=capex,nonland_capex=nonland,
                    da_xbrl=da,dep_plus_amort=dpam,nonland_minus_da=diff,ebit=ebit,owner_earnings=oe))
con.execute("DROP TABLE IF EXISTS owner_earnings")
con.execute("""CREATE TABLE owner_earnings(fy INT PRIMARY KEY,land REAL,d_land REAL,capex REAL,
  nonland_capex REAL,da_xbrl REAL,dep_plus_amort REAL,nonland_minus_da REAL,ebit REAL,owner_earnings REAL)""")
con.executemany("INSERT INTO owner_earnings VALUES(:fy,:land,:d_land,:capex,:nonland_capex,:da_xbrl,:dep_plus_amort,:nonland_minus_da,:ebit,:owner_earnings)",out)
con.commit()
with open(ROOT/"data/csv/owner_earnings.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print("\nland series cross-filing consistency (same FY seen in multiple 10-Ks):")
for y in sorted(land):
    if len(land[y])>1 and 2015<=y<=2025:
        vals={k:round(v,1) for k,v in sorted(land[y].items())}
        agree = len(set(vals.values()))==1
        print(f"  FY{y}: {vals}  {'AGREE' if agree else '<-- DISAGREE'}")
