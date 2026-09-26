#!/usr/bin/env python3
"""Append OCR'd IAA table rows to data/csv/iaa_fee_grid_2026-09.csv. Usage: e6_iaa_ocr_to_csv.py <svg> <page> <tier> <fee_type[,fee_type2]>
Multi-column tables (internet fees) map column i to the i-th fee_type. Replaces existing rows with the same (page,tier,fee_types)."""
import csv, subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent; OUT = ROOT / 'data/csv/iaa_fee_grid_2026-09.csv'
svg, page, tier, ftypes = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(',')
out = subprocess.run([str(ROOT / '.venv/bin/python'), str(ROOT / 'scripts/experiments/e6_ocr_iaa_table.py'), svg], capture_output=True, text=True).stdout
new = []
for l in out.splitlines():
    if l.startswith('#'): continue
    parts = l.split(','); lo, hi = parts[0], parts[1]
    for i, cell in enumerate(parts[2:]):
        usd, pct = cell.split('|'); new.append(['2026-09-26', page, tier, ftypes[i], float(lo), float(hi) if hi else '', float(usd) if usd else '', float(pct) if pct else ''])
hdr = open(OUT).readline(); rows = [r for r in csv.DictReader(l for l in open(OUT) if not l.startswith('#')) if not (r['page'] == page and r['tier'] == tier and r['fee_type'] in ftypes)]
cols = ['read_date', 'page', 'tier', 'fee_type', 'band_low_usd', 'band_high_usd', 'fee_usd', 'fee_pct']
with open(OUT, 'w', newline='') as f:
    f.write(hdr); w = csv.writer(f); w.writerow(cols)
    for r in rows: w.writerow([r[c] for c in cols])
    w.writerows(new)
print(f"{page}/{tier}/{ftypes}: {len(new)} rows; file {len(rows)+len(new)} rows")
