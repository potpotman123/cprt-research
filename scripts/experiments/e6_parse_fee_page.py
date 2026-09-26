#!/usr/bin/env python3
"""E6 — parse a saved Copart fee-page text dump (get_page_text output from the owner-driven browser session) into
data/csv/copart_fee_grid_2026-09.csv rows. Usage: e6_parse_fee_page.py <dump.txt> <page> <title_group> <vehicle_class> [read_date]
Tables recognised: 'Secured Payment Methods' / 'Unsecured Payment Methods' buyer-fee bands; Virtual Bid 'Pre-Bid' / 'Live Bid'; Gate Fee $.
Idempotent per (page,title,vehicle): existing rows for that key are replaced."""
import csv, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent; OUT = ROOT / 'data/csv/copart_fee_grid_2026-09.csv'
dump, page, title, vcls = sys.argv[1:5]; date = sys.argv[5] if len(sys.argv) > 5 else '2026-09-26'
txt = open(dump, encoding='utf-8').read()
band = re.compile(r'^\$([\d,\.]+)\s*(?:-\s*\$?([\d,\.]+)|\+)\s+(?:\$([\d,\.]+)|([\d\.]+)%|(FREE))\s*$', re.M)
def bands(section_start, section_end):
    i = txt.find(section_start); j = txt.find(section_end, i + 1) if section_end else len(txt)
    assert i >= 0, section_start
    seg = txt[i:j if j > 0 else len(txt)]
    rows = []
    for m in band.finditer(seg):
        lo = float(m.group(1).replace(',', '')); hi = float(m.group(2).replace(',', '')) if m.group(2) else ''
        fee = 0.0 if m.group(5) else (float(m.group(3).replace(',', '')) if m.group(3) else ''); pct = float(m.group(4)) if m.group(4) else ''
        rows.append((lo, hi, fee, pct))
    return rows
new = []
for pm, s, e in (('secured', 'Secured Payment Methods', 'Unsecured Payment Methods'), ('unsecured', 'Unsecured Payment Methods', 'Gate Fee')):
    for lo, hi, fee, pct in bands(s, e): new.append([date, page, title, vcls, 'buyer_fee', pm, lo, hi, fee, pct])
for bt, s, e in (('pre_bid', 'Pre-Bid', 'Live Bid'), ('live_bid', 'Live Bid', 'Title Shipping')):
    for lo, hi, fee, pct in bands(s, e): new.append([date, page, title, vcls, 'virtual_bid_' + bt, 'any', lo, hi, fee, pct])
g = re.search(r'A \$([\d\.]+) Gate Fee', txt)
if g: new.append([date, page, title, vcls, 'gate_fee', 'any', 0, '', float(g.group(1)), ''])
hdr = ("# Copart US buyer fee schedule, read 2026-09-26 from copart.com fee pages in a human-driven browser session (raw/fees/live_2026-09/README.txt). "
       "One row per price band per (member page, title group, vehicle class, payment method). fee_usd is a fixed dollar fee; fee_pct applies to the final bid where fee_usd is blank; "
       "virtual-bid and gate-fee rows are keyed to the page/title selection they were displayed under. VERIFIED (page text dumps on disk).\n")
cols = ['read_date', 'page', 'title_group', 'vehicle_class', 'fee_type', 'payment_method', 'band_low_usd', 'band_high_usd', 'fee_usd', 'fee_pct']
old = []
if OUT.exists():
    old = [r for r in csv.DictReader(l for l in open(OUT) if not l.startswith('#')) if not (r['page'] == page and r['title_group'] == title and r['vehicle_class'] == vcls)]
with open(OUT, 'w', newline='') as f:
    f.write(hdr); w = csv.writer(f); w.writerow(cols)
    for r in old: w.writerow([r[c] for c in cols])
    for r in new: w.writerow(r)
print(f"{page}/{title}/{vcls}: {len(new)} rows written ({sum(1 for r in new if r[4]=='buyer_fee')} buyer-fee bands, gate ${g.group(1) if g else '?'}); file now {len(old)+len(new)} rows")
