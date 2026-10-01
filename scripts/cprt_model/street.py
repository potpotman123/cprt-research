"""Street: named-broker FY27 assumptions from the verified extraction (30 Sep workflow), not-disclosed preserved."""
import json
from .common import *
FIELDS = [('report_date', 'Report date'), ('rating_and_target', 'Rating / target'), ('fy27_service_revenue_musd', 'FY27E service revenue ($M)'), ('fy27_purchased_revenue_musd', 'FY27E purchased-vehicle revenue ($M)'),
          ('fy27_total_revenue_musd', 'FY27E total revenue ($M)'), ('fy28_total_revenue_musd', 'FY28E total revenue ($M)'), ('lost_account_named_carrier', 'Lost account: carrier named?'), ('us_insurance_units_assumption', 'US insurance units / assignments'),
          ('us_insurance_asp_assumption', 'US insurance ASP'), ('fee_or_service_rpu_assumption', 'Fee / service RPU'), ('international_assumption', 'International'), ('acv_scope', 'ACV scope'), ('aftermarket_tlf_commentary', 'Aftermarket / total-loss commentary'), ('corrections_made', 'Verifier corrections made')]
def build(wb, ctx):
    ws = wb.create_sheet('Street'); tab_color(ws, NAVY); setup(ws, label_w=34, ncols=9, notes_col='N')
    title(ws, 'Street — named-broker FY27 assumptions (licensed reports held locally; figures and paraphrases only)', 'Source: 15 extractions, each re-verified against the cited lines (workflow 30 Sep 2026; raw/workflow_2026-09-30_expectations_discovery.json). "Not disclosed" is recorded, never inferred from a total. No licensed text is reproduced.')
    p = ROOT / 'raw/workflow_2026-09-30_expectations_discovery.json'
    try:
        d = json.load(open(p)); res = d.get('result', d); res = json.loads(res) if isinstance(res, str) else res; ex = [e for e in res.get('expectations', []) if e]
    except Exception as err:
        put(ws, 'B4', f'Extraction file not readable: {err}', 'note'); return
    ex = [e for e in ex if 'transcripts' not in e.get('source_file', '')]
    ws.column_dimensions['B'].width = 34
    for j, e in enumerate(ex):
        c = L(4 + j); ws.column_dimensions[c].width = 30; put(ws, f'{c}4', (e.get('broker') or '').split('(')[0].strip()[:28], 'label', b=True); ws[f'{c}4'].alignment = Alignment(wrap_text=True, vertical='top')
    for i, (k, lab) in enumerate(FIELDS):
        r = 5 + i; label(ws, r, lab, b=k.startswith('fy27_service'))
        for j, e in enumerate(ex):
            v = e.get(k); c = L(4 + j)
            if v is None or v == '': v = 'not disclosed'
            if isinstance(v, (int, float)): put(ws, f'{c}{r}', v, 'input', F_MONEY if 'musd' in k else '0')
            else: cell = put(ws, f'{c}{r}', str(v)[:260], 'label'); cell.alignment = Alignment(wrap_text=True, vertical='top'); cell.font = font(sz=9)
        ws.row_dimensions[r].height = 15 if k in ('report_date', 'corrections_made') or 'musd' in k else 75
    r = 5 + len(FIELDS) + 1; S = ctx['sel_rows']; label(ws, r, 'Model FY27E legacy service revenue, selected case', '$M', b=True); put(ws, f'D{r}', f"=Scenarios!{ACOL[2027]}{S['legacy']}", 'link', F_MONEY, b=True)
    label(ws, r + 1, 'Δ model − broker FY27E service revenue (where disclosed)', '$M', b=True)
    for j, e in enumerate(ex):
        c = L(4 + j); put(ws, f'{c}{r+1}', f'=IF(ISNUMBER({c}7),$D${r}-{c}7,"n/a")', fmt=F_MONEY, b=True)
    put(ws, f'B{r+3}', 'Full field set (quarterly tables, contract events, catalysts) is in the JSON; this tab shows the forecast-relevant rows only.', 'note')
    ws.freeze_panes = 'D5'
