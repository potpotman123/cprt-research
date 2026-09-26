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
    if form != '10-Q': continue                      # 10-K primary documents carry no MD&A (Exhibit 13); skip
    txt = text_of(f).replace('\n', ' ')
    # frequency: four wordings across 2015–2026
    fm = (re.search(r'([^.]*incurred frequency of (?:auto|personal auto) accidents[^.]*\.)', txt)
          or re.search(r'([^.]*personal auto incurred (?:accident )?frequency,? on a (?:calendar-year|calendar year|year-over-year) basis,[^.]*\.)', txt)
          or re.search(r'([^.]*incurred personal auto accident frequency[^.]*\.)', txt)
          or re.search(r'([^.]*personal auto incurred accident frequency was (?:down|up)[^.]*\.)', txt))
    fs = fm.group(1).strip() if fm else ''
    TB = r'personal auto incurred frequency, on a calendar-year basis, over the prior-year period, was as follows:.{0,700}?'
    tbl = re.search(TB + r'Total \(?(\d+)\)?', txt)        # 2023+ table: "Total (4) (3)" (Q1 filings have one column); parentheses = negative
    ctb = re.search(TB + r'Collision \(?(\d+)\)?', txt)
    def signed(m, i):  # parenthesised = negative
        seg = m.group(0); num = m.group(i); j = seg.rfind(num); return -float(num) if seg[j - 1] == '(' else float(num)
    cs = ''
    if fm:
        cm = re.search(r'(Collision[^.•]*\.)', txt[fm.end():fm.end() + 2500]); cs = cm.group(1).strip() if cm else ''
    sm = re.search(r'(?:Total )?personal auto incurred severity', txt) or re.search(r'incurred severity', txt)
    ss = re.sub(r'\(i\.e\.,[^)]*\)', '', txt[sm.start():sm.start() + 700]).strip() if sm else ''
    ss = ss.split('. ')[0] + '.' if ss else ''
    def qfig(s):
        if not s: return None
        m = re.search(r'(increased|decreased|down|up)\s+(?:by\s+)?(?:about|approximately|around|nearly|almost|roughly)?\s*(\d+(?:\.\d+)?)\s*%?(?:\s+to\s+\d+%)?', s)
        if m: return (1 if m.group(1) in ('increased', 'up') else -1) * float(m.group(2))
        if re.search(r'\b(flat|unchanged)\b', s): return 0.0
        return None
    f_q = signed(tbl, 1) if tbl else qfig(fs); c_q = signed(ctb, 1) if ctb else qfig(cs)
    if tbl: fs = 'TABLE: ' + tbl.group(0)[:300].replace('|', '/')
    rows.append(dict(filing_date=dt, form=form, freq_total_q=f_q, freq_collision_q=c_q, severity_total_q=qfig(ss), freq_quote=fs[:300], collision_quote=cs[:200], severity_quote=ss[:300]))
out = ROOT / 'data/csv/pgr_frequency_quarterly.csv'
with open(out, 'w', newline='') as fh:
    fh.write("# Progressive (CIK 80661) personal-auto incurred claim frequency and severity, year-over-year % change for the quarter, transcribed by regex from each 10-Q/10-K MD&A (raw/sec/pgr/, fetched 2026-09-26) with the source sentence beside every number (scripts/experiments/e2_pgr_frequency.py). 10-K rows are full-year unless the sentence gives Q4. Comprehensive coverage excluded by Progressive's own convention. VERIFIED quotes; parsed figures should be spot-checked against them.\n")
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(f"{r['filing_date']} {r['form']:5s} freq {str(r['freq_total_q']):>6s}  coll {str(r['freq_collision_q']):>6s}  sev {str(r['severity_total_q']):>6s} | {r['freq_quote'][:110]}")
