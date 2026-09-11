import sqlite3,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
Q=["FY2023 Q1","FY2023 Q2","FY2023 Q3","FY2023 Q4","FY2024 Q1","FY2024 Q2","FY2024 Q3","FY2024 Q4",
   "FY2025 Q1","FY2025 Q2","FY2025 Q3","FY2025 Q4","FY2026 Q1","FY2026 Q2","FY2026 Q3"]
# Stephens Exhibit 7, transcribed. None = blank cell.
S={
"us_inventory_yoy":      [-6.3,-3.0, 2.0, 8.0, 1.0, 4.0, 3.0, 6.0, 5.0,-4.0,-11.0,-14.8,-17.0,-8.1,-4.7],
"us_ins_units_yoy":      [None, 9.0, 6.0, 9.0, 9.7, 0.3, 6.8, 6.0,12.0, 9.0,  0.6, -2.1, -9.5,-10.7,-4.2],
"us_ins_asp_yoy":        [ 6.4, 1.0,-1.1, 2.0,-1.7,-5.0,-2.0,-4.0,-1.0, 2.0,  2.0,  5.7,  8.4, 6.0, 4.1],
"global_asp_yoy":        [ 5.0, 0.0,-1.4,-1.0,-5.0,-3.0,-5.0,-1.0, 2.0, 3.0,  5.6,  8.5,  6.0, 4.6, None],
"us_total_units_yoy":    [ 1.3, 4.0, 4.0, 8.0,10.0, 5.0, 9.0, 6.0,11.0, 8.0,  0.0, -1.8, -7.9,-9.5,-4.2],
"global_inventory_yoy":  [-3.6,-1.0, 4.0, 9.5, 3.0, 6.0, 4.0, 7.0, 6.0,-3.0,-10.0,-13.1, -4.6,-7.0,-2.0],
}
# note: global_asp row in Exhibit 7 has 15 values 1Q23..3Q26; shift check below
S["global_asp_yoy"]=[5.0,0.0,-1.4,-1.0,-5.0,-3.0,-5.0,-1.0,2.0,3.0,5.6,8.5,6.0,4.6,None]
con=sqlite3.connect(ROOT/"data/cprt.db")
mine={r[0]:dict(zip(["us_inventory_yoy","us_ins_units_yoy","us_ins_units_exCAT_yoy","us_ins_asp_yoy",
                     "global_asp_yoy","global_ins_units_yoy"],r[1:]))
      for r in con.execute("""SELECT fiscal_q,us_inventory_yoy,us_ins_units_yoy,us_ins_units_exCAT_yoy,
                              us_ins_asp_yoy,global_asp_yoy,global_ins_units_yoy FROM reported_units""")}
print("=== CORROBORATION: my transcript reading vs Stephens Exhibit 7 ===")
for metric in ("us_inventory_yoy","us_ins_units_yoy","us_ins_asp_yoy"):
    ok=diff=absent=0; notes=[]
    print(f"\n--- {metric} ---")
    print(f"{'quarter':<11}{'mine':>8}{'Stephens':>10}   verdict")
    for q,sv in zip(Q,S[metric]):
        mv=mine.get(q,{}).get(metric)
        if mv is None or sv is None:
            absent+=1; v="(one side blank)"
        elif abs(mv-sv)<0.15: ok+=1; v="MATCH"
        elif abs(mv-sv)<=0.6: ok+=1; v=f"match (rounding, {mv-sv:+.1f})"
        else: diff+=1; v=f"*** DIFFERS {mv-sv:+.1f}pp ***"; notes.append((q,mv,sv))
        f=lambda x: "   -  " if x is None else f"{x:>+6.1f}"
        print(f"{q:<11}{f(mv):>8}{f(sv):>10}   {v}")
    print(f"  -> {ok} agree, {diff} differ, {absent} not comparable")
print("\n=== metrics Stephens has that I did not extract ===")
for m in ("us_total_units_yoy","global_inventory_yoy"):
    print(f"  {m}: "+" ".join(("  -  " if v is None else f"{v:+.1f}") for v in S[m]))
con.execute("DROP TABLE IF EXISTS stephens_exhibit7")
cols=list(S)
con.execute(f"CREATE TABLE stephens_exhibit7(fiscal_q TEXT PRIMARY KEY,{','.join(c+' REAL' for c in cols)})")
con.executemany(f"INSERT INTO stephens_exhibit7 VALUES(?,{','.join('?'*len(cols))})",
                [tuple([q]+[S[c][i] for c in cols]) for i,q in enumerate(Q)])
con.commit()
import csv
with open(ROOT/"data/csv/stephens_exhibit7.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["fiscal_q"]+cols)
    for i,q in enumerate(Q): w.writerow([q]+[S[c][i] for c in cols])
print("\n-> table stephens_exhibit7 + data/csv/stephens_exhibit7.csv")
