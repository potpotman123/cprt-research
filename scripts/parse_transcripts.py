"""Extract reported unit / inventory / ASP percentages from earnings-call transcripts."""
import re,glob,csv,sqlite3,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
def sgn(word,val):
    return -val if re.search(r'declin|decreas|down|fell|lower|contract',word,re.I) else val
NUM=r'(\d+(?:\.\d+)?)%'
def find(t,pats):
    for p in pats:
        m=re.search(p,t,re.I|re.S)
        if m:
            gs=m.groups()
            word=next((g for g in gs if g and re.search(r'[a-z]{4}',g)),"")
            num=next((g for g in gs if g and re.fullmatch(r'\d+(?:\.\d+)?',g)),None)
            if num is not None: return sgn(word,float(num)), m.group(0)[:190]
    return None,None
M={
"global_ins_units":[
  r'global insurance unit sales (declined|decreased|increased|grew|rose|were up|were down)[^.%]{0,30}?'+NUM,
  r'global insurance units? (?:sales )?(?:volumes? )?(?:were )?(down|up|declined|decreased|increased|grew)[^.%]{0,30}?'+NUM,
  r'(?:on the insurance side,? )?global (?:insurance )?units were (down|up)[^.%]{0,20}?'+NUM],
"global_ins_units_exCAT":[
  r'global insurance unit sales (?:declined|decreased|increased|grew)[^.]{0,40}?or ()'+NUM+r' excluding the effect of catastroph',
  r'global insurance units[^.]{0,60}?or ()'+NUM+r'[^.]{0,30}excluding[^.]{0,30}catastroph'],
"us_ins_units":[
  r'U\.?S\.? insurance unit volume[^.%]{0,40}?(declined|decreased|increased|grew|rose)[^.%]{0,30}?'+NUM,
  r'U\.?S\.? insurance units?[^.%]{0,40}?(declined|decreased|increased|grew|rose|were up|were down)[^.%]{0,30}?'+NUM,
  r'[Ii]nsurance (?:unit )?volumes? (decreased|declined|increased|grew|rose)[^.%]{0,30}?'+NUM],
"us_ins_units_exCAT":[
  r'U\.?S\.? insurance unit volume[^.]{0,60}?or (?:just over |approximately |about )?()'+NUM+r'[^.]{0,40}excluding',
  r'U\.?S\.? insurance unit volume[^.]{0,60}?or (just over|just under|approximately|about) ()'+NUM],
"us_inventory":[
  r'U\.?S\.? inventory was (down|up)[^.%]{0,30}?'+NUM,
  r'U\.?S\.? inventory (declined|decreased|increased|grew|rose)[^.%]{0,30}?'+NUM,
  r'inventory[^.]{0,20}U\.?S\.?[^.]{0,30}(down|up|declined|increased)[^.%]{0,25}?'+NUM],
"global_inventory":[
  r'global inventory was (down|up)[^.%]{0,30}?'+NUM,
  r'global inventory (declined|decreased|increased|grew|rose)[^.%]{0,30}?'+NUM],
"intl_inventory":[
  r'[Ii]nventory in our international segment (increased|decreased|declined|grew|rose)[^.%]{0,30}?'+NUM,
  r'international[^.]{0,25}inventory[^.%]{0,30}?(increased|decreased|declined|grew)[^.%]{0,25}?'+NUM],
"asp_consolidated":[
  r'average selling prices,? which (rose|increased|declined|decreased|fell)[^.%]{0,30}?'+NUM,
  r'average selling prices? (increased|rose|declined|decreased|grew|fell)[^.%]{0,35}?'+NUM],
"us_ins_asp":[
  r'U\.?S\.? insurance ASPs (increased|rose|declined|decreased|grew|fell)[^.%]{0,30}?'+NUM,
  r'[Ii]nsurance ASPs (increased|rose|declined|decreased|grew|fell)[^.%]{0,30}?'+NUM],
"us_total_units":[
  r'[Tt]otal units (declined|decreased|increased|grew|rose)[^.%]{0,30}?'+NUM],
"copart_direct_units":[
  r'Copart direct unit volume (declined|decreased|increased|grew|rose)[^.%]{0,30}?'+NUM],
}
CALL2Q={"2022-09-08":"FY2022 Q4","2022-11-17":"FY2023 Q1","2023-02-21":"FY2023 Q2","2023-05-17":"FY2023 Q3",
 "2023-09-14":"FY2023 Q4","2023-11-16":"FY2024 Q1","2024-02-22":"FY2024 Q2","2024-05-16":"FY2024 Q3",
 "2024-09-04":"FY2024 Q4","2024-11-21":"FY2025 Q1","2025-02-20":"FY2025 Q2","2025-05-22":"FY2025 Q3",
 "2025-09-04":"FY2025 Q4","2025-11-20":"FY2026 Q1","2026-02-19":"FY2026 Q2","2026-05-21":"FY2026 Q3"}
rows=[];ev=[]
for f in sorted(glob.glob(str(ROOT/"raw/transcripts/call_*.txt"))):
    d=re.search(r'call_(\d{4}-\d{2}-\d{2})',f).group(1)
    t=re.sub(r'\s+',' ',open(f).read())
    r={"call_date":d,"fiscal_q":CALL2Q.get(d,"?")}
    for k,pats in M.items():
        v,q=find(t,pats); r[k]=v
        if q: ev.append((d,k,v,q))
    rows.append(r)
cols=["call_date","fiscal_q"]+list(M)
print(f"{'call':<12}{'quarter':<11}"+"".join(f"{k[:11]:>13}" for k in list(M)[:7]))
for r in rows:
    print(f"{r['call_date']:<12}{r['fiscal_q']:<11}"+"".join(
      ("  n/a        " if r[k] is None else f"{r[k]:>+12.1f}%") for k in list(M)[:7]))
print()
print(f"{'call':<12}{'quarter':<11}"+"".join(f"{k[:11]:>13}" for k in list(M)[7:]))
for r in rows:
    print(f"{r['call_date']:<12}{r['fiscal_q']:<11}"+"".join(
      ("  n/a        " if r[k] is None else f"{r[k]:>+12.1f}%") for k in list(M)[7:]))
con=sqlite3.connect(ROOT/"data/cprt.db",timeout=60)
con.execute("DROP TABLE IF EXISTS reported_units")
con.execute(f"CREATE TABLE reported_units(call_date TEXT PRIMARY KEY,fiscal_q TEXT,{','.join(c+' REAL' for c in list(M))})")
con.executemany(f"INSERT INTO reported_units VALUES({','.join(':'+c for c in cols)})",rows); con.commit()
with open(ROOT/"data/csv/reported_units.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); w.writerows(rows)
miss=sum(1 for r in rows for k in M if r[k] is None)
print(f"\n{len(rows)} calls; {miss} missing cells of {len(rows)*len(M)}")
with open(ROOT/"logs/transcript_evidence.txt","w") as fh:
    for d,k,v,q in ev: fh.write(f"{d}\t{k}\t{v}\t{q}\n")
print("evidence quotes -> logs/transcript_evidence.txt (for audit)")
