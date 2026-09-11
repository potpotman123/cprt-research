import re,csv,sqlite3,datetime,collections,pathlib,statistics
ROOT=pathlib.Path(__file__).resolve().parent.parent
TITLE=("clean-title","salvage","non-repairable","nonrepairable","cert-of-title","bill-of-sale","junk")
US=set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split())
rx=re.compile(r'/lot/(\d{6,})(?:/([^/?#\s]+))?')
rows=[]
for line in open(ROOT/"raw/cdx/lot_pages_full.txt"):
    p=line.split()
    if len(p)<2: continue
    m=rx.search(p[0])
    if not m: continue
    lot=int(m.group(1)); ts=p[1]
    if not re.fullmatch(r'\d{14}',ts): continue
    slug=(m.group(2) or "")
    if "&" in slug or "%" in slug or "<" in slug: slug=""
    tt=year=make_model=state=city=None
    if slug and slug.lower()!="photos":
        s=slug.lower()
        for t in TITLE:
            if s.startswith(t): tt=t; s=s[len(t):].strip("-"); break
        ym=re.match(r'(19\d{2}|20\d{2})-(.*)$', s)
        if ym:
            year=int(ym.group(1)); rest=ym.group(2)
            parts=rest.split("-")
            # trailing state code (2 letters) then city
            for i in range(len(parts)-1,0,-1):
                if parts[i].upper() in US:
                    state=parts[i].upper(); city="-".join(parts[i+1:]) or None
                    make_model="-".join(parts[:i]); break
            if state is None: make_model=rest
    rows.append((lot,ts,tt,year,make_model,state,city,slug))
print(f"parsed {len(rows):,} lot captures")
con=sqlite3.connect(ROOT/"data/cprt.db")
con.execute("DROP TABLE IF EXISTS lot_anchors")
con.execute("""CREATE TABLE lot_anchors(lot_id INTEGER,capture_ts TEXT,title_type TEXT,
   year INTEGER,make_model TEXT,state TEXT,city TEXT,slug TEXT)""")
con.executemany("INSERT INTO lot_anchors VALUES(?,?,?,?,?,?,?,?)",rows)
con.execute("CREATE INDEX IF NOT EXISTS ix_lot ON lot_anchors(lot_id)")
con.commit()
with open(ROOT/"data/csv/lot_anchors.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["lot_id","capture_ts","title_type","year","make_model","state","city","slug"])
    w.writerows(rows)
# ---- first-seen per lot = upper bound on ID issuance date ----
first={}
for lot,ts,*_ in rows:
    if lot not in first or ts<first[lot]: first[lot]=ts
print(f"distinct lot_ids: {len(first):,}")
con.execute("DROP TABLE IF EXISTS lot_first_seen")
con.execute("CREATE TABLE lot_first_seen(lot_id INTEGER PRIMARY KEY,first_seen TEXT)")
con.executemany("INSERT INTO lot_first_seen VALUES(?,?)",sorted(first.items()))
con.commit(); con.close()
print("\n=== lot_id distribution (millions) ===")
ids=sorted(first)
print(f"  min={min(ids):,}  max={max(ids):,}  n={len(ids):,}")
h=collections.Counter(i//1_000_000 for i in ids)
for b in sorted(h): print(f"   {b:>3}M-{b+1}M : {h[b]:>7,} {'#'*min(60,h[b]//120)}")
