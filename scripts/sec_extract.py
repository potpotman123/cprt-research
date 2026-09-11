import json, sqlite3, datetime, collections, csv, pathlib, os
ROOT=pathlib.Path(__file__).resolve().parent.parent
d=json.load(open(ROOT/"raw/sec/companyfacts_CIK0000900075.json"))
FACTS=d["facts"]
def annual(tag, ns="us-gaap", unit="USD"):
    """Return {fy: (val, start, end, form, accn)} for FY-annual periods (FYE Jul 31)."""
    node=FACTS.get(ns,{}).get(tag)
    if not node: return {}
    out={}
    for u,rows in node["units"].items():
        if u!=unit: continue
        for r in rows:
            end=r.get("end"); start=r.get("start")
            if r.get("form") not in ("10-K","10-K/A"): continue
            if not end: continue
            ed=datetime.date.fromisoformat(end)
            if start:  # flow: require ~annual duration ending in Jul/Aug
                sd=datetime.date.fromisoformat(start); days=(ed-sd).days
                if not (330<=days<=400): continue
                if ed.month not in (7,8): continue
            else:      # stock: balance date must be FYE
                if ed.month not in (7,8): continue
            fy=ed.year
            prev=out.get(fy)
            # prefer original 10-K, latest filed
            if prev is None or (r.get("filed","") > prev[5]):
                out[fy]=(r["val"], start, end, r.get("form"), r.get("accn"), r.get("filed",""))
    return {k:v for k,v in sorted(out.items())}
TAGS={
 "total_revenue":        ["Revenues","RevenueFromContractWithCustomerIncludingAssessedTax","SalesRevenueNet"],
 "service_revenue":      ["SalesRevenueServicesNet"],
 "purchased_veh_revenue":["SalesRevenueGoodsNet"],
 "operating_income":     ["OperatingIncomeLoss"],
 "d_and_a":              ["DepreciationDepletionAndAmortization","DepreciationAmortizationAndAccretionNet","Depreciation"],
 "capex":                ["PaymentsToAcquirePropertyPlantAndEquipment","PaymentsToAcquireProductiveAssets"],
 "cash":                 ["CashAndCashEquivalentsAtCarryingValue"],
 "net_income":           ["NetIncomeLoss"],
}
series={}
for name,cands in TAGS.items():
    merged={}; used=collections.OrderedDict()
    for tag in cands:
        a=annual(tag)
        for fy,v in a.items():
            if fy not in merged: merged[fy]=v; used[fy]=tag
    series[name]={fy:merged[fy] for fy in sorted(merged)}
    series[name+"__tag"]=dict(used)
sh=annual("CommonStockSharesOutstanding",unit="shares")
if not sh: sh=annual("WeightedAverageNumberOfDilutedSharesOutstanding",unit="shares")
series["shares_out"]=sh; series["shares_out__tag"]={k:"CommonStockSharesOutstanding/DilutedWAvg" for k in sh}

years=list(range(2016,2027))
hdr=["fy","total_revenue","service_revenue","purchased_veh_revenue","operating_income","d_and_a","capex","cash","net_income","shares_out"]
os.makedirs(ROOT/"data/csv",exist_ok=True)
rows=[]
for fy in years:
    row={"fy":fy}
    for k in hdr[1:]:
        v=series.get(k,{}).get(fy)
        row[k]=v[0] if v else None
    rows.append(row)
with open(ROOT/"data/csv/sec_annual.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=hdr); w.writeheader(); w.writerows(rows)
con=sqlite3.connect(ROOT/"data/cprt.db")
con.execute("DROP TABLE IF EXISTS sec_annual")
con.execute(f"CREATE TABLE sec_annual(fy INTEGER PRIMARY KEY,{','.join(c+' REAL' for c in hdr[1:])})")
con.executemany(f"INSERT INTO sec_annual VALUES({','.join('?'*len(hdr))})",
                [tuple(r[c] for c in hdr) for r in rows])
con.commit()
def M(x): return "" if x is None else f"{x/1e6:,.1f}"
def SH(x): return "" if x is None else f"{x/1e6:,.1f}"
print(f"{'FY':<6}{'Rev':>11}{'Svc':>11}{'Purch':>10}{'EBIT':>11}{'D&A':>9}{'Capex':>10}{'Cash':>11}{'Shrs(m)':>10}")
for r in rows:
    print(f"{r['fy']:<6}{M(r['total_revenue']):>11}{M(r['service_revenue']):>11}"
          f"{M(r['purchased_veh_revenue']):>10}{M(r['operating_income']):>11}{M(r['d_and_a']):>9}"
          f"{M(r['capex']):>10}{M(r['cash']):>11}{SH(r['shares_out']):>10}")
print()
for k in ("total_revenue","service_revenue","purchased_veh_revenue","d_and_a","capex"):
    print(f"tag[{k}]:", series[k+"__tag"])
