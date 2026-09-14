#!/usr/bin/env python3
"""BLUEPRINT — one worked model tab, built the way every tab should be built.

Mechanism A: fleet cohort roll -> baseline total-loss frequency (demographics only).
  baseline TLF(year) = SUM_cohorts[ sales(MY) * S(age) * R(age) * P(age) ] / SUM_cohorts[ sales(MY) * S(age) * R(age) ]
Layout pattern (same on every tab): title+description+sources / INPUTS (blue) / CALCULATION / OUTPUT / CHECKS.
Two parameters are CALIBRATED to stated anchors (yellow): survival centre -> S&P avg fleet age 12.7 (2025);
propensity multiplier -> CCC 2019 TLF 19.2%. Everything else is a blue input with a note.

Output: model/blueprint_A_CohortRoll.xlsx   (recalculate with the xlsx skill's recalc.py before reading values)
"""
import csv, collections, math, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as L
ROOT = pathlib.Path(__file__).resolve().parent.parent

# ---------- data ----------
by = collections.defaultdict(float)
for r in csv.DictReader(open(ROOT / 'data/csv/fred_TOTALNSA.csv')):
    v = r.get('TOTALNSA') or r.get('value')
    if v and v != '.': by[int(r[list(r)[0]][:4])] += float(v) / 1000
MY = list(range(1995, 2033)); FUT = 16.5
sales = {y: (round(by[y], 2) if y <= 2025 else FUT) for y in MY}
YEARS = list(range(2018, 2033)); AGES = list(range(0, 36))
R = {a: (1.0 if a <= 5 else 0.9 if a <= 9 else 0.75 if a <= 12 else 0.55 if a <= 16 else 0.40) for a in AGES}
Praw = {a: {0: 10, 1: 11, 2: 12, 3: 13.5, 4: 15, 5: 17, 6: 19, 7: 22, 8: 25, 9: 28, 10: 31, 11: 35, 12: 39, 13: 43, 14: 45, 15: 47}.get(a, 48.0) for a in AGES}
actual = {2018: 18.5, 2019: 19.2, 2020: 20.6, 2021: 19.7, 2022: 18.8, 2023: 20.2, 2024: 22.3, 2025: 23.1}
SCALE = 4.0
def S(a, c): return 1 / (1 + math.exp((a - c) / SCALE))
def model(year, c, mult):
    fw = cw = tw = agesum = 0
    for my in MY:
        a = year - my
        if a < 0 or a > 35: continue
        f = sales[my] * S(a, c); cwt = f * R[a]; t = cwt * Praw[a] * mult / 100
        fw += f; cw += cwt; tw += t; agesum += a * f
    return 100 * tw / cw, agesum / fw
lo, hi = 10, 30
for _ in range(60):
    c = (lo + hi) / 2
    if model(2025, c, 1)[1] > 12.7: hi = c
    else: lo = c
CENTER = round((lo + hi) / 2, 3)
lo, hi = 0.2, 2.0
for _ in range(60):
    m = (lo + hi) / 2
    if model(2019, CENTER, m)[0] > 19.2: hi = m
    else: lo = m
MULT = round((lo + hi) / 2, 4)
print(f"calibrated: survival centre={CENTER}, propensity mult={MULT}")

# ---------- workbook ----------
wb = Workbook(); ws = wb.active; ws.title = "A_CohortRoll"
def F(**k):
    k.setdefault("name", "Arial"); k.setdefault("size", 10); return Font(**k)
BLUE = F(color="0000FF"); BLK = F(); BOLD = F(bold=True); TITLE = F(bold=True, size=13); HDR = F(bold=True, color="FFFFFF")
NOTE = F(italic=True, color="595959")
YEL = PatternFill("solid", fgColor="FFFF00"); GREYH = PatternFill("solid", fgColor="404040"); LIGHT = PatternFill("solid", fgColor="F2F2F2")
def put(cell, val, font=BLK, fmt=None, fill=None, wrap=False):
    c = ws[cell]; c.value = val; c.font = font
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap: c.alignment = Alignment(wrap_text=True, vertical="top")
    return c
def hdr(row, c1, c2, text):
    ws.merge_cells(start_row=row, start_column=c1, end_row=row, end_column=c2)
    put(f"{L(c1)}{row}", text, HDR, fill=GREYH)

put("A1", "BLUEPRINT TAB — Mechanism A: Fleet cohort roll → baseline total-loss frequency", TITLE)
put("A2", "Every model year is a cohort of known size that ages through brackets with different totaling propensities. Baseline TLF(year) = Σ_cohorts [sales × survival(age) × claim-freq(age) × TL-propensity(age)] ÷ Σ [sales × survival × claim-freq]. This tab answers one question: how much of the TLF rise is DEMOGRAPHICS, versus everything else (repair-cost cycle, technology, the 2025 denominator artifact)?", BLK, wrap=True)
ws.merge_cells("A2:R2"); ws.row_dimensions[2].height = 44
put("A3", "Sources: cohort sizes = FRED TOTALNSA (light-vehicle sales, NSA, summed by calendar year) data/csv/fred_TOTALNSA.csv · TL-propensity anchors = CCC Crash Course (≈10% current MY; 45.3% at 13+ yrs; 70% of total losses are 7+ yrs) · avg fleet age 12.7 = S&P Global Mobility 2025 · actual TLF = CCC all-loss, data/csv/ccc_tlf_annual.csv.   Colour: BLUE = input · BLACK = formula · YELLOW = calibrated to a stated anchor.", BLK, wrap=True)
ws.merge_cells("A3:R3"); ws.row_dimensions[3].height = 44

hdr(5, 1, 6, "INPUTS  (one assumption per cell; source or note to the right)")
rows = [("Future model-year sales, 2026–2032 (M / yr)", FUT, "0.0", "ASSUMED — 2023–25 ran 16.0–16.7M"),
        ("Survival curve centre (age at 50% survival, yrs)", CENTER, "0.000", "CALIBRATED so 2025 avg fleet age = S&P 12.7 (C12). Logistic S(a)=1/(1+EXP((a−centre)/scale))"),
        ("Survival curve scale (yrs)", SCALE, "0.0", "ASSUMED shape parameter"),
        ("TL-propensity level multiplier", MULT, "0.0000", "CALIBRATED so 2019 baseline = CCC 19.2% (C10:C11). Curve SHAPE is the input; LEVEL is calibrated"),
        ("Anchor year", 2019, "0", "pre-COVID, pre-rate-shock"),
        ("Anchor TLF, CCC all-loss (%)", 19.2, "0.0", "CCC Crash Course; ccc_tlf_annual.csv"),
        ("Check target: avg fleet age 2025 (yrs)", 12.7, "0.0", "S&P Global Mobility, 2025"),
        ("Check target: share of total losses from vehicles 7+ yrs", 0.70, "0%", "CCC Crash Course")]
for i, (lab, val, fmt, note) in enumerate(rows):
    r = 6 + i; put(f"B{r}", lab); put(f"C{r}", val, BLUE, fmt, fill=(YEL if "CALIBRATED" in note else None)); put(f"D{r}", note, NOTE)

hdr(15, 1, 6, "AGE CURVES  (rows = vehicle age 0–35)")
for j, h in enumerate(["Age (yrs)", "Survival S(a)", "Rel. insured-claim freq R(a)", "TL propensity, raw P(a) %", "P(a) calibrated %"]):
    put(f"{L(1+j)}16", h, BOLD, fill=LIGHT)
A0 = 17
for k, a in enumerate(AGES):
    r = A0 + k
    put(f"A{r}", a, BLK, "0"); put(f"B{r}", f"=1/(1+EXP((A{r}-$C$7)/$C$8))", BLK, "0.000")
    put(f"C{r}", R[a], BLUE, "0.00"); put(f"D{r}", Praw[a], BLUE, "0.0"); put(f"E{r}", f"=D{r}*$C$9", BLK, "0.00")
A1_ = A0 + len(AGES) - 1
put(f"G{A0}", "R(a): older cars are driven less and are often liability-only, so they generate fewer INSURED physical-damage claims. ASSUMED step function — flex it.", NOTE, wrap=True); ws.merge_cells(f"G{A0}:L{A0+2}")
put(f"G{A0+4}", "P(a): probability a CLAIM on an age-a vehicle is a total loss. Anchors ≈10% (age 0) and ≈45% (13+) from CCC; points between are interpolated (ASSUMED). Held FIXED over time — so any TLF rise this tab does NOT produce is technology / cycle / measurement, not demographics.", NOTE, wrap=True); ws.merge_cells(f"G{A0+4}:L{A0+8}")

C0 = A1_ + 4; hdr(C0 - 1, 1, 6, "COHORT SIZES  (rows = model year)")
for j, h in enumerate(["Model year", "Sales (M)", "Source"]): put(f"{L(1+j)}{C0}", h, BOLD, fill=LIGHT)
CR0 = C0 + 1
for k, my in enumerate(MY):
    r = CR0 + k; put(f"A{r}", my, BLK, "0")
    if my <= 2025: put(f"B{r}", sales[my], BLUE, "0.00"); put(f"C{r}", "FRED TOTALNSA", NOTE)
    else: put(f"B{r}", "=$C$6", BLK, "0.00"); put(f"C{r}", "= input C6", NOTE)
CR1 = CR0 + len(MY) - 1

def matrix(top, title, formula):
    hdr(top, 1, 18, title)
    put(f"A{top+1}", "Model year", BOLD, fill=LIGHT); put(f"B{top+1}", "Sales (M)", BOLD, fill=LIGHT)
    for j, y in enumerate(YEARS): put(f"{L(4+j)}{top+1}", y, BOLD, "0", fill=LIGHT)
    r0 = top + 2
    for k, my in enumerate(MY):
        r = r0 + k; put(f"A{r}", f"=A{CR0+k}", BLK, "0"); put(f"B{r}", f"=B{CR0+k}", BLK, "0.00")
        for j, _ in enumerate(YEARS):
            col = L(4 + j); put(f"{col}{r}", formula(col, r, top + 1, r0, k), BLK, "0.000")
    return r0, r0 + len(MY) - 1
M1 = CR1 + 4
m1a, m1b = matrix(M1, "MATRIX 1 — Fleet weight = sales(MY) × S(age),   age = calendar year − model year",
    lambda col, r, hr, r0, k: f"=IF(OR({col}${hr}-$A{r}<0,{col}${hr}-$A{r}>35),0,$B{r}*INDEX($B${A0}:$B${A1_},{col}${hr}-$A{r}+1))")
M2 = m1b + 3
m2a, m2b = matrix(M2, "MATRIX 2 — Insured-claim weight = fleet weight × R(age)",
    lambda col, r, hr, r0, k: f"=IF(OR({col}${hr}-$A{r}<0,{col}${hr}-$A{r}>35),0,{col}{m1a+k}*INDEX($C${A0}:$C${A1_},{col}${hr}-$A{r}+1))")
M3 = m2b + 3
m3a, m3b = matrix(M3, "MATRIX 3 — Total-loss weight = claim weight × P_calibrated(age) / 100",
    lambda col, r, hr, r0, k: f"=IF(OR({col}${hr}-$A{r}<0,{col}${hr}-$A{r}>35),0,{col}{m2a+k}*INDEX($E${A0}:$E${A1_},{col}${hr}-$A{r}+1)/100)")

O = m3b + 3; hdr(O, 1, 18, "OUTPUT  (the cells other tabs reference)")
put(f"A{O+1}", "Calendar year", BOLD, fill=LIGHT)
for j, y in enumerate(YEARS): put(f"{L(4+j)}{O+1}", y, BOLD, "0", fill=LIGHT)
labels = [("Fleet on road (M)", "0.0"), ("Insured-claim weight (M)", "0.0"), ("Total-loss weight (M)", "0.00"),
          ("BASELINE TLF — demographics only (%)", "0.00"), ("Δ baseline TLF YoY (pp)", "+0.00;-0.00;0.00"),
          ("Avg fleet age (yrs)", "0.00"), ("7–12-yr cohort size (M)", "0.0"), ("Share of TL weight from age ≥7", "0.0%"),
          ("ACTUAL TLF, CCC all-loss (%)", "0.0"), ("RESIDUAL = actual − baseline (pp)  → technology + repair-cost cycle + denominator artifact", "+0.00;-0.00;0.00")]
for i, (lab, fmt) in enumerate(labels): put(f"A{O+2+i}", lab, BOLD if i in (3, 9) else BLK)
for j, y in enumerate(YEARS):
    c = L(4 + j); h = O + 1
    put(f"{c}{O+2}", f"=SUM({c}{m1a}:{c}{m1b})", BLK, "0.0")
    put(f"{c}{O+3}", f"=SUM({c}{m2a}:{c}{m2b})", BLK, "0.0")
    put(f"{c}{O+4}", f"=SUM({c}{m3a}:{c}{m3b})", BLK, "0.00")
    put(f"{c}{O+5}", f"=IF({c}{O+3}=0,0,{c}{O+4}/{c}{O+3}*100)", BOLD, "0.00", fill=LIGHT)
    put(f"{c}{O+6}", (f"={c}{O+5}-{L(3+j)}{O+5}" if j > 0 else None), BLK, "+0.00;-0.00;0.00")
    put(f"{c}{O+7}", f"=SUMPRODUCT(({c}${h}-$A${m1a}:$A${m1b})*{c}{m1a}:{c}{m1b})/{c}{O+2}", BLK, "0.00")
    put(f"{c}{O+8}", f"=SUMPRODUCT(($A${CR0}:$A${CR1}>={c}${h}-12)*($A${CR0}:$A${CR1}<={c}${h}-7)*$B${CR0}:$B${CR1})", BLK, "0.0")
    put(f"{c}{O+9}", f"=SUMPRODUCT(($A${m3a}:$A${m3b}<={c}${h}-7)*{c}{m3a}:{c}{m3b})/{c}{O+4}", BLK, "0.0%")
    if y in actual: put(f"{c}{O+10}", actual[y], BLUE, "0.0")
    put(f"{c}{O+11}", (f"={c}{O+10}-{c}{O+5}" if y in actual else None), BOLD, "+0.00;-0.00;0.00")

K = O + 14; hdr(K, 1, 6, "CHECKS  (every tab has these; a FAIL means stop and look before building the next tab)")
yr = f"$D${O+1}:$R${O+1}"
chk = [("Anchor: baseline TLF in anchor year = CCC anchor (±0.3pp)", f'=IF(ABS(INDEX($D${O+5}:$R${O+5},MATCH($C$10,{yr},0))-$C$11)<0.3,"OK","FAIL")'),
       ("Avg fleet age 2025 within 1 yr of S&P 12.7", f'=IF(ABS(INDEX($D${O+7}:$R${O+7},MATCH(2025,{yr},0))-$C$12)<1,"OK","FAIL")'),
       ("Share of TLs from 7+ yr vehicles within 10pp of CCC 70%", f'=IF(ABS(INDEX($D${O+9}:$R${O+9},MATCH(2025,{yr},0))-$C$13)<0.10,"OK","FAIL")'),
       ("Age-curve rows = 36 (0–35)", f'=IF(COUNT($A${A0}:$A${A1_})=36,"OK","FAIL")'),
       ("Informational: demographic drift, avg Δbaseline 2019→2028 (pp / yr)", f"=(INDEX($D${O+5}:$R${O+5},MATCH(2028,{yr},0))-INDEX($D${O+5}:$R${O+5},MATCH(2019,{yr},0)))/9"),
       ("Informational: intercept of the CCC spread regression (pp / yr), for comparison", 0.599)]
for i, (lab, f) in enumerate(chk):
    r = K + 1 + i; put(f"B{r}", lab); put(f"E{r}", f, BOLD if i < 4 else BLK, ("+0.000" if i >= 4 else None), fill=(LIGHT if i < 4 else None))
put(f"B{K+8}", "READ-OUT: if the demographic drift (row above) is far below the regression intercept (0.6pp / yr), the fleet-cohort story explains only a small part of the secular TLF rise; the rest is technology (P(a) shifting up over time) and the repair-cost cycle. That is the finding this tab exists to make — and it is honest even though it is smaller than the popular version.", F(italic=True), wrap=True)
ws.merge_cells(f"B{K+8}:L{K+10}"); ws.row_dimensions[K+8].height = 30

ws.column_dimensions["A"].width = 14; ws.column_dimensions["B"].width = 46; ws.column_dimensions["C"].width = 13
for col in "DEFGHIJKLMNOPQR": ws.column_dimensions[col].width = 9.5
ws.freeze_panes = "B5"
out = ROOT / "model/blueprint_A_CohortRoll.xlsx"; out.parent.mkdir(exist_ok=True); wb.save(out)
print(f"wrote {out}   (output block starts row {O}, checks row {K})")
