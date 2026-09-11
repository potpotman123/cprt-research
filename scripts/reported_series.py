"""Reported metrics hand-verified from earnings-call transcripts (quotes in
logs/transcript_quotes.md). Values transcribed by reading, NOT regex, because
regex mis-attributed sentences. 'over/nearly/about/approximately N%' -> N."""
import sqlite3,csv,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
# fiscal_q, call_date, us_inventory, us_ins_units, us_ins_units_exCAT, us_ins_asp, global_asp, global_ins_units
R=[
("FY2022 Q4","2022-09-08",  -9.6, None, None,  9.2,  8.3, None),
("FY2023 Q1","2022-11-17",  -6.3, None, None,  6.4,  5.0, None),
("FY2023 Q2","2023-02-21",  -3.0,  9.0, None,  1.0,  0.0, None),
("FY2023 Q3","2023-05-17",   2.0,  6.0, None, -1.0, -1.0, None),
("FY2023 Q4","2023-09-14",   8.0,  9.0, None,  2.0,  2.0, None),
("FY2024 Q1","2023-11-16",   1.0,  9.7, None, -1.7, -1.0, None),
("FY2024 Q2","2024-02-22",   4.0,  0.3,  9.2, -5.0, -5.0, None),
("FY2024 Q3","2024-05-16",   3.0,  6.8, None, -2.0, -3.0, None),
("FY2024 Q4","2024-09-04",   6.0,  6.0, None, -4.0, -5.0, None),
("FY2025 Q1","2024-11-21",   5.0, 12.0,  9.0, -1.0, -1.0, None),
("FY2025 Q2","2025-02-20",  -4.0,  9.0,  2.0,  2.0,  2.0, None),
("FY2025 Q3","2025-05-22", -11.0, -1.0, -2.0,  2.0,  3.0, None),
("FY2025 Q4","2025-09-04", -14.8, -2.1, None,  5.7,  5.6, -1.9),
("FY2026 Q1","2025-11-20", -17.0, -9.5, -7.3,  8.4,  8.5, None),
("FY2026 Q2","2026-02-19",  -8.1,-10.7, -4.8,  6.0,  6.0, -8.0),
("FY2026 Q3","2026-05-21",  -4.7, -4.2, -3.1,  4.1,  4.6, -2.7),
]
cols=["fiscal_q","call_date","us_inventory_yoy","us_ins_units_yoy","us_ins_units_exCAT_yoy",
      "us_ins_asp_yoy","global_asp_yoy","global_ins_units_yoy"]
con=sqlite3.connect(ROOT/"data/cprt.db",timeout=60)
con.execute("DROP TABLE IF EXISTS reported_units")
con.execute(f"CREATE TABLE reported_units(fiscal_q TEXT PRIMARY KEY,call_date TEXT,{','.join(c+' REAL' for c in cols[2:])})")
con.executemany(f"INSERT INTO reported_units VALUES({','.join('?'*len(cols))})",R); con.commit()
with open(ROOT/"data/csv/reported_units.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(cols); w.writerows(R)
print(f"{'quarter':<11}{'US inv':>9}{'US ins u':>10}{'exCAT':>8}{'US ins ASP':>12}{'glob ASP':>10}")
for r in R:
    f=lambda x,w: ("     -   "[:w] if x is None else f"{x:>+{w}.1f}")
    print(f"{r[0]:<11}{f(r[2],9)}{f(r[3],10)}{f(r[4],8)}{f(r[5],12)}{f(r[6],10)}")
print(f"\n{len(R)} quarters -> data/csv/reported_units.csv")
print("\n=== BASIS RECONCILIATION (spec's open question) ===")
print("  Spec's third-party FY26 series -7.3% / -4.8% / -3.1% (Q1/Q2/Q3):")
for q in ("FY2026 Q1","FY2026 Q2","FY2026 Q3"):
    row=[x for x in R if x[0]==q][0]
    print(f"    {q}: as-reported US ins units {row[3]:+.1f}%   ex-CAT {row[4]:+.1f}%   global as-rep "
          f"{('n/a' if row[7] is None else f'{row[7]:+.1f}%')}")
print("  => the third-party series is US INSURANCE UNITS EXCLUDING CAT. Exact match, 3 of 3.")
print("  => -4.2% (Q3) is US insurance units AS-REPORTED (incl. CAT comp).")
print("  => -2.7% (Q3) is GLOBAL insurance units AS-REPORTED.")
print("  No conflict: three different bases, all disclosed on the same calls.")
