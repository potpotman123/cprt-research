#!/usr/bin/env python3
"""Render an IAA fee-table SVG to PNG (qlmanage), OCR it with macOS Vision (ocr_image.swift), pair each row's price band with its
fee column(s) by y-position, and print CSV-ready rows. Usage: e6_ocr_iaa_table.py <file.svg>"""
import re, subprocess, sys, pathlib, collections
svg = pathlib.Path(sys.argv[1]).resolve(); png = svg.with_suffix('.svg.png')
if not png.exists():
    subprocess.run(['qlmanage', '-t', '-s', '2400', '-o', str(svg.parent), str(svg)], capture_output=True)
out = subprocess.run(['swift', str(pathlib.Path(__file__).parent / 'ocr_image.swift'), str(png)], capture_output=True, text=True)
if out.returncode: sys.exit(out.stderr)
items = []
for line in out.stdout.splitlines():
    y, x, t = line.split('\t', 2); items.append((float(y), float(x), t.strip()))
items.sort(); rows = collections.OrderedDict(); keys = []
for y, x, t in items:                                   # group by y: join a row if within 0.008 of its centre (row pitch is ~0.02)
    k = next((k for k in keys if abs(k - y) < 0.008), None)
    if k is None: k = y; keys.append(k); rows[k] = []
    rows[k].append((x, t))
band = re.compile(r'^\$?([\d,\.]+)\s*(?:[–\-]\s*\$?([\d,\.]+)|\+)$'); fee = re.compile(r'^\$?([\d,\.]+)\s*(%.*)?$|^([\d\.]+)%')
header = None
for k in sorted(rows):
    cells = sorted(rows[k]); texts = [t for _, t in cells]
    if any('Sale Price' in t for t in texts): header = texts; print('# header:', ' | '.join(texts)); continue
    m = band.match(texts[0].replace(' ', ''))
    if not m: print('# skipped:', ' | '.join(texts)); continue
    lo = m.group(1).replace(',', ''); hi = m.group(2).replace(',', '') if m.group(2) else ''
    fees = []
    for t in texts[1:]:
        t2 = t.replace(' ', '')
        pm = re.match(r'^([\d\.]+)%', t2); dm = re.match(r'^\$?([\d,\.]+)$', t2)
        fees.append(('', pm.group(1)) if pm else ((dm.group(1).replace(',', ''), '') if dm else (t, '?')))
    print(lo, hi, *[f"{a}|{b}" for a, b in fees], sep=',')
