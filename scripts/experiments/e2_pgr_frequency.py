#!/usr/bin/env python3
"""E2 step 1 — Progressive's quarterly personal-auto claim FREQUENCY and SEVERITY changes from its 10-Q/10-K MD&A (raw/sec/pgr/).
Each filing states, for the quarter and year-to-date: "Our incurred frequency of auto accidents ... increased/decreased about X%
for the <n> quarter <year>", a per-coverage bullet list (collision, BI/PD/PIP), and "Total personal auto incurred severity ...
increased about X%". This script extracts the sentences, parses the QUARTER figure (or the fourth quarter from a 10-K if stated,
else the full year), and writes data/csv/pgr_frequency_quarterly.csv with the quote for every number so a reader can check.
"""
import csv, glob, html, os, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
def text_of(f):
    t = open(f, encoding='utf-8', errors='ignore').read()
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S); t = re.sub(r'</(p|div|tr|li|h\d)>', '\n', t); t = re.sub(r'</t[dh]>', ' ', t)
    txt = html.unescape(re.sub(r'<[^>]+>', '', t)); txt = re.sub(r'[ \t\xa0]+', ' ', txt); return re.sub(r'\n\s*\n+', '\n', txt)
def pct_after(s, words=('increased', 'decreased', 'up', 'down', 'flat', 'unchanged')):
    """first (direction, number) in s: 'increased about 2%' -> +2; 'decreased 5%' -> -5; 'flat' -> 0"""
    m = re.search(r'(increased|decreased|rose|fell|up|down)\s+(?:by\s+)?(?:about|approximately|around|nearly|almost|roughly)?\s*(\d+(?:\.\d+)?)\s*%', s)
    if m: return (1 if m.group(1) in ('increased', 'rose', 'up') else -1) * float(m.group(2))
    if re.search(r'\b(flat|unchanged|relatively flat)\b', s): return 0.0
    return None
rows = []
for f in sorted(glob.glob(str(ROOT / 'raw/sec/pgr/*.htm'))):
    base = os.path.basename(f); dt, form = base[:10], base[11:].split('_')[0]
    txt = text_of(f).replace('\n', ' ')
    # frequency sentence
    fm = re.search(r'([^.]*incurred frequency of (?:auto|personal auto) accidents[^.]*\.)', txt) or re.search(r'([^.]*\bauto accident frequency[^.]*\.)', txt) or re.search(r'([^.]*\bfrequency\b[^.]*(?:quarter|three months)[^.]*\.)', txt)
    fs = fm.group(1).strip() if fm else ''
    # per-coverage collision bullet (first "Collision ..." sentence after the frequency sentence)
    cs = ''
    if fm:
        cm = re.search(r'(Collision[^.•]*\.)', txt[fm.end():fm.end() + 2500]); cs = cm.group(1).strip() if cm else ''
    # severity sentence
    sm = re.search(r'(?:Total )?personal auto incurred severity', txt) or re.search(r'incurred severity', txt)
    ss = re.sub(r'\(i\.e\.,[^)]*\)', '', txt[sm.start():sm.start() + 700]).strip() if sm else ''
    ss = ss.split('. ')[0] + '.' if ss else ''
    # quarter figure: prefer the clause mentioning 'quarter'
    def qfig(s):
        if not s: return None
        parts = re.split(r'\band\b|,|;', s)
        for p in parts:
            if 'quarter' in p or 'three months' in p:
                v = pct_after(p)
                if v is not None: return v
        return pct_after(s)
    rows.append(dict(filing_date=dt, form=form, freq_total_q=qfig(fs), freq_collision_q=qfig(cs), severity_total_q=qfig(ss), freq_quote=fs[:300], collision_quote=cs[:200], severity_quote=ss[:300]))
out = ROOT / 'data/csv/pgr_frequency_quarterly.csv'
with open(out, 'w', newline='') as fh:
    fh.write("# Progressive (CIK 80661) personal-auto incurred claim frequency and severity, year-over-year % change for the quarter, transcribed by regex from each 10-Q/10-K MD&A (raw/sec/pgr/, fetched 2026-09-26) with the source sentence beside every number (scripts/experiments/e2_pgr_frequency.py). 10-K rows are full-year unless the sentence gives Q4. Comprehensive coverage excluded by Progressive's own convention. VERIFIED quotes; parsed figures should be spot-checked against them.\n")
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(f"{r['filing_date']} {r['form']:5s} freq {str(r['freq_total_q']):>6s}  coll {str(r['freq_collision_q']):>6s}  sev {str(r['severity_total_q']):>6s} | {r['freq_quote'][:110]}")
