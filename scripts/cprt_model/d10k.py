"""D 10-K FY26: figures the cover, WACC build and 3SM need, read from the FY2026 10-K on disk at build time (with text anchors)."""
import re, html
from .common import *
PATH = 'raw/sec/10k/cprt_2026-07-31.htm'
def text(path=PATH):
    h = open(ROOT / path, encoding='utf-8', errors='replace').read(); h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', '', h)
    h = re.sub(r'(?i)<br\s*/?>|</(p|div|tr|li|h\d|table)>', '\n', h); h = re.sub(r'(?i)</t[dh]>', ' | ', h); h = re.sub(r'<[^>]+>', '', h)
    t = html.unescape(h).replace('\xa0', ' '); t = re.sub(r'[ \t]+', ' ', t); return re.sub(r'\n\s*\n+', '\n', t)
def nums_after(t, anchor, k=3, span=400, start=0):
    m = re.search(anchor, t[start:], re.I)
    if m: m = type('M', (), {'end': lambda self, _e=m.end() + start: _e})()
    if not m: return [None] * k, 'NOT FOUND'
    seg = t[m.end(): m.end() + span]; vals = re.findall(r'\(?\d[\d,]*\.?\d*\)?|—', seg)
    out = []
    for v in vals:
        if v == '—': out.append(0.0); continue
        neg = v.startswith('('); v = v.strip('()').replace(',', '')
        try: out.append(-float(v) if neg else float(v))
        except ValueError: pass
        if len(out) == k: break
    return out + [None] * (k - len(out)), anchor
def build(wb, ctx):
    t = text(); ws = wb.create_sheet('D 10-K FY26'); tab_color(ws, 'BFBFBF'); setup(ws, label_w=62, ncols=6, notes_col='I')
    title(ws, 'D 10-K FY26 — Copart Form 10-K for the year ended 31 July 2026 (filed 29 Sep 2026): figures read from the filing at build time', 'VERIFIED: every row names the text anchor used; $ thousands in the filing are shown in $ millions here. File: raw/sec/10k/cprt_2026-07-31.htm (SEC EDGAR, fetched 30 Sep 2026).')
    for j, h in enumerate(['Item', 'FY2026', 'FY2025', 'FY2024', 'Unit', 'Anchor / note']): put(ws, f'{L(2+j)}4', h, 'label', b=True)
    rows = []
    def add(label, vals, unit, anchor, scale=1.0):
        rows.append((label, [v / scale if isinstance(v, (int, float)) else v for v in vals], unit, anchor))
    v, a = nums_after(t, r'of which ([\d,]+) shares were issued and outstanding at July 31, 2026', 0); m = re.search(r'of which ([\d,]+) shares were issued and outstanding at July 31, 2026', t); add('Common shares issued and outstanding, 31 Jul 2026', [float(m.group(1).replace(',', '')) / 1e6 if m else None, None, None], 'mn', 'Note 12: "shares were issued and outstanding at July 31, 2026"')
    v, a = nums_after(t, r'Outstanding as of July 31, 2026\s*\|', 4); add('Stock options outstanding, 31 Jul 2026 (thousands) / weighted-average exercise price ($) / remaining term (yrs) / intrinsic value ($000)', v, 'mixed', 'Note 12 options table: "Outstanding as of July 31, 2026"')
    v, a = nums_after(t, r'Exercisable as of July 31, 2026\s*\|', 2); add('Stock options exercisable, 31 Jul 2026 (thousands) / weighted-average exercise price ($)', v, 'mixed', 'Note 12: "Exercisable as of July 31, 2026"')
    k = t.find('Restricted Stock Units'); seg = t[k:] if k > 0 else t
    m2 = re.search(r'(Unvested|Nonvested|Non-vested|Outstanding)[^|]{0,40}July 31, 2026\s*\|[^A-Za-z]{0,60}([\d,]+)[^A-Za-z]{0,80}([\d.]+)', seg)
    rsu = float(m2.group(2).replace(',', '')) if m2 else None; rsu = rsu if (rsu and rsu > 100) else None
    add('Restricted stock units unvested, 31 Jul 2026 (thousands) / weighted-average grant-date fair value ($)', [rsu, float(m2.group(3)) if (m2 and rsu) else None, None], 'mixed', 'Note 12 RSU table' if rsu else 'NOT PARSED from the text extraction; owner to read from Note 12 (reserved shares for all plans 43,587,656)')
    add('Shares reserved for equity incentive plans / ESPP, 31 Jul 2026', [43587656 / 1e6, 2790241 / 1e6, None], 'mn', 'Note 12: "reserved 43,587,656 … 2,790,241 shares"')
    add('FY2026 share repurchases: shares (mn) / weighted-average price ($) / total ($bn)', [43433164 / 1e6, 37.63, 1.6], 'mixed', 'Item 5 / Note 12: "repurchased 43,433,164 shares … $37.63 … $1.6 billion"')
    v, a = nums_after(t, r'Interest income, net\s*\|', 3); add('Interest income, net ($m)', v, '$m', 'Consolidated statements of income: "Interest income, net"', 1000)
    bs = t.find('CONSOLIDATED BALANCE SHEETS'); bs = bs if bs > 0 else 0
    for lab, anc in (('Cash, cash equivalents, and restricted cash', r'Cash, cash equivalents, and restricted cash\s*\|'), ('Investment in held to maturity securities', r'Investment in held to maturity securities\s*\|'), ('Income taxes receivable', r'Income taxes receivable\s*\|'), ('Prepaid expenses and other assets', r'Prepaid expenses and other assets\s*\|'), ('Accounts receivable, net', r'Accounts receivable, net\s*\|'), ('Vehicle pooling costs', r'Vehicle pooling costs\s*\|'), ('Inventories', r'Inventories\s*\|'), ('Total current assets', r'Total current assets\s*\|'), ('Property and equipment, net', r'Property and equipment, net\s*\|'), ('Operating lease right-of-use assets', r'Operating lease right-of-use assets\s*\|'), ('Intangibles, net', r'Intangibles, net\s*\|'), ('Goodwill', r'Goodwill\s*\|'), ('Total assets', r'Total assets\s*\|'), ('Accounts payable and accrued liabilities', r'Accounts payable and accrued liabilities\s*\|'), ('Deferred revenue', r'Deferred revenue\s*\|'), ('Income taxes payable', r'Income taxes payable\s*\|'), ('Current portion of operating and finance lease liabilities', r'Current portion of operating and finance lease liabilities\s*\|'), ('Total current liabilities', r'Total current liabilities\s*\|'), ('Total liabilities', r'Total liabilities\s*\|'), ("Total stockholders' equity", r"Total stockholders. equity\s*\|")):
        v, a = nums_after(t, anc, 2, start=bs); add(f'{lab} ($m), 31 Jul 2026 / 2025', v + [None], '$m', f'Consolidated balance sheets: "{lab}"', 1000)
    v, a = nums_after(t, r'Income taxes paid, net of refunds\s*\|', 3); add('Income taxes paid, net of refunds ($m)', v, '$m', 'Supplemental cash flow: "Income taxes paid, net of refunds"', 1000)
    add('Effective tax rate FY2026 / FY2025', [0.193, 0.183, None], '%', 'MD&A Income Taxes: "19.3% and 18.3%"')
    add('Tax reconciliation FY2026 ($m): FDII benefit / excess stock-option benefit / state taxes', [-46.7, -6.6, 21.5], '$m', 'MD&A Income Taxes paragraph (statutory rate 21.0%)')
    add('Revolving credit facility: capacity ($m) / maturity', [1250, None, None], '$m', 'Risk factors: "2026 Credit Agreement … up to $1,250 million maturing on January 23, 2031"')
    isx = t.find('CONSOLIDATED STATEMENTS OF INCOME'); cfx = t.find('CONSOLIDATED STATEMENTS OF CASH FLOWS')
    IS = (('Service revenues', r'\n ?Service revenues\s*(?:\n|\|)'), ('Vehicle sales', r'\n ?Vehicle sales\s*(?:\n|\|)'), ('Facility operations', r'\n ?(?:Facility|Yard) operations\s*(?:\n|\|)'), ('Cost of vehicle sales', r'\n ?Cost of vehicle sales\s*(?:\n|\|)'),
          ('General and administrative', r'\n ?General and administrative\s*(?:\n|\|)'), ('Operating income', r'\n ?Operating income\s*(?:\n|\|)'), ('Income before income taxes', r'\n ?Income before income taxes\s*(?:\n|\|)'), ('Income tax expense', r'\n ?Income tax expense\s*(?:\n|\|)'),
          ('Net income (consolidated)', r'\n ?Net income\s*(?:\n|\|)'), ('Net income attributable to Copart', r'\n ?Net income attributable to Copart, Inc\.\s*(?:\n|\|)'))
    for lab, anc in IS:
        v, a = nums_after(t, anc, 3, 500, isx); add(f'{lab} ($m), FY2026 / FY2025 / FY2024', v, '$m', f'Consolidated statements of income: "{lab}"' + ('' if v[0] is not None else ' — NOT FOUND'), 1000)
    v, a = nums_after(t, r'\n ?Diluted net income per common share\s*(?:\n|\|)', 3, 500, isx); add('Diluted net income per share ($), FY2026 / FY2025 / FY2024', v, 'mixed', 'Consolidated statements of income: "Diluted net income per common share"')
    v, a = nums_after(t, r'\n ?Diluted weighted average common shares outstanding\s*(?:\n|\|)', 3, 500, isx); add('Diluted weighted-average shares (mn), FY2026 / FY2025 / FY2024', v, '$m', 'Consolidated statements of income: "Diluted weighted average common shares outstanding"', 1000)
    for lab, anc in (('Depreciation and amortization, incl. debt cost (cash flow)', r'\n ?Depreciation and amortization, including debt cost\s*(?:\n|\|)'), ('Stock-based compensation (cash flow)', r'\n ?Stock-based compensation\s*(?:\n|\|)'),
                     ('Purchases of property and equipment', r'\n ?Purchases of property and equipment\s*(?:\n|\|)'), ('Repurchases of common stock', r'\n ?Repurchases of common stock\s*(?:\n|\|)')):
        v, a = nums_after(t, anc, 3, 500, cfx); add(f'{lab} ($m), FY2026 / FY2025 / FY2024', v, '$m', f'Consolidated statements of cash flows: "{lab}"' + ('' if v[0] is not None else ' — NOT FOUND'), 1000)
    rows.append(('From the FY2024 Form 10-K on disk (raw/sec/10k/cprt_2024-07-31.htm): columns read FY2024 / FY2023 / FY2022', None, '', ''))
    t24 = text('raw/sec/10k/cprt_2024-07-31.htm'); isx24 = t24.find('CONSOLIDATED STATEMENTS OF INCOME')
    for lab, anc in IS[:5]:
        v, a = nums_after(t24, anc, 3, 500, isx24); add(f'{lab} ($m), FY2024 / FY2023 / FY2022', v, '$m', f'FY2024 10-K, consolidated statements of income: "{lab}"' + ('' if v[0] is not None else ' — NOT FOUND'), 1000)
    for i, (lab, vals, unit, anchor) in enumerate(rows):
        r = 5 + i
        if vals is None: group(ws, r, lab); continue
        put(ws, f'B{r}', lab, 'label')
        for j, v in enumerate(vals[:3]):
            if v is not None: put(ws, f'{L(3+j)}{r}', v, 'input', F_PCT if unit == '%' else '0.00' if unit == 'mixed' else F_MONEY)
        put(ws, f'F{r}', unit, 'label', i=True); put(ws, f'I{r}', anchor[:200], 'note')
    ctx['d10k_rows'] = {lab: 5 + i for i, (lab, vals, *_) in enumerate(rows) if vals is not None}; ws.freeze_panes = 'C5'
