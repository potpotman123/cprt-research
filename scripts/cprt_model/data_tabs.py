"""Data tabs (values only, grey tabs): D Reported, D CCC, D Fleet, D Fees, D Carriers, D Engine. Plus Cover and dividers."""
import json, datetime, pathlib
from .common import *
def build(wb, ctx):
    inputs = json.load(open(ROOT / 'model/linked_service_revenue_2026-09-28/inputs.json'))
    # ---------------- D Reported
    ws = wb.create_sheet('D Reported'); tab_color(ws, 'BFBFBF'); setup(ws, label_w=30, ncols=12)
    title(ws, 'D Reported — Copart reported quarterly series (8-K exhibits and calls)', 'Values only. $ millions unless stated. Sources: raw/sec/8k/er_*.htm (VERIFIED); call transcripts for growth rates (VERIFIED, licensed).')
    rows = []
    for r in read_csv('data/csv/quarterly_pl.csv'):
        if not r.get('quarter_end'): continue
        qe = datetime.datetime.strptime(r['quarter_end'], '%B %d, %Y').date(); fy = qe.year + (1 if qe.month > 7 else 0); q = {10: 1, 1: 2, 4: 3, 7: 4}[qe.month]
        rows.append([f'FY{fy} Q{q}', qe.isoformat(), num(r['service_rev_m']), num(r['vehicle_sales_m']), num(r['total_rev_m']), num(r['service_yoy_pct']), num(r['total_yoy_pct'])])
    r = write_table(ws, 4, 2, ['Fiscal quarter', 'Quarter end', 'Service revenue', 'Vehicle sales', 'Total revenue', 'Service y/y %', 'Total y/y %'], rows, fmt_by_col={2: F_MONEY, 3: F_MONEY, 4: F_MONEY, 5: '0.0', 6: '0.0'})
    ws.cell(r + 1, 2, 'Geography split, service and vehicle revenue by quarter (8-K segment tables)').font = font(b=True)
    geo = [[f"FY{a['fy']} Q{a['q']}", a['end'], a['us_service'], a['intl_service'], a['us_vehicle'], a['intl_vehicle'], pathlib.Path(a['source']).name] for a in inputs['prior_actuals'] + inputs['actuals']]
    r = write_table(ws, r + 2, 2, ['Fiscal quarter', 'Quarter end', 'US service', 'Intl service', 'US vehicle', 'Intl vehicle', 'Source exhibit'], geo, fmt_by_col={2: F_MONEY, 3: F_MONEY, 4: F_MONEY, 5: F_MONEY})
    ctx['geo_rows'] = {(int(g[0][2:6]), int(g[0][-1])): r0 for g, r0 in zip(geo, range(r - len(geo), r))}
    ws.cell(r + 1, 2, 'Disclosed growth rates by quarter (calls; per cent)').font = font(b=True)
    ru = [[x['fiscal_q'], x['call_date'], num(x['us_inventory_yoy']), num(x['us_ins_units_yoy']), num(x['us_ins_units_exCAT_yoy']), num(x['us_ins_asp_yoy']), num(x['global_asp_yoy']), num(x['global_ins_units_yoy'])] for x in read_csv('data/csv/reported_units.csv')]
    r = write_table(ws, r + 2, 2, ['Fiscal quarter', 'Call date', 'US inventory y/y', 'US ins. units y/y', 'US ins. units ex-CAT y/y', 'US ins. ASP y/y', 'Global ASP y/y', 'Global ins. units y/y'], ru)
    ws.cell(r + 1, 2, 'FY2026 10-K (filed 2026-09-29): insurers supplied 79% of vehicles processed (81% FY25, 81% FY24); 286 operating facilities; no customer >10% of revenue. VERIFIED raw/sec/10k/cprt_2026-07-31.htm').font = font(C_NOTE, i=True, sz=10)
    # ---------------- D CCC
    ws = wb.create_sheet('D CCC'); tab_color(ws, 'BFBFBF'); setup(ws, label_w=12, ncols=12)
    title(ws, 'D CCC — total-loss frequency and total-loss mix by vehicle type and age, 2020–2025', 'Owner-supplied CCC workbook (Data for Harvard Research, Daniella Biblin, 9.29.2026; SHA-256 2a127900…). VERIFIED cells; geography and coverage of the sample not stated by the source.')
    cells = read_csv('model/ccc_age_body_2026-09-29/source_cells.csv')
    rows = [[int(c['year']), c['source_body'], int(c['age_group']), c['source_age'], float(c['tlf']), float(c['tl_mix']), c['tlf_cell'], c['tl_mix_cell']] for c in cells]
    ctx['ccc_r0'] = 5; r = write_table(ws, 4, 2, ['Year', 'Body', 'Age group', 'Age label', 'TLF', 'TL mix', 'TLF cell', 'Mix cell'], rows, fmt_by_col={4: F_PCT2, 5: F_PCT2}); ctx['ccc_r1'] = r - 1
    ws.cell(r + 1, 2, 'Annual all-loss total-loss frequency (CCC Crash Course; data/csv/ccc_tlf_annual.csv)').font = font(b=True)
    ann = [[int(a[list(a.keys())[0]]), num(list(a.values())[1]), num(list(a.values())[2])] for a in read_csv('data/csv/ccc_tlf_annual.csv')]
    write_table(ws, r + 2, 2, ['Year', 'TLF all loss %', 'TLF ex-comp %'], ann)
    # ---------------- D Fleet
    ws = wb.create_sheet('D Fleet'); tab_color(ws, 'BFBFBF'); setup(ws, label_w=10, ncols=12)
    title(ws, 'D Fleet — new-vehicle births by body (thousands) and EPA survival schedules', "Births: Ward's via ORNL TEDB Ed.40 Table 3.6 (1970–2021) and FRED TOTALNSA/LTRUCKNSA (2022–25), VERIFIED; light-truck split into SUV/pickup/minivan from EPA model-year composition (ASSUMED proxy; docs/historical_body_births_2026-09-28). Survival: ORNL Table 3.15 (EPA), VERIFIED.")
    bb = {}
    for r_ in read_csv('docs/historical_body_births_2026-09-28/candidate_body_births.csv'):
        if r_['year'] == 'year': continue
        bb.setdefault(int(r_['year']), {})[r_['body']] = float(r_['births_thousands'])
    if 2028 not in bb and 2027 in bb: bb[2028] = dict(bb[2027])   # hold 2027 (ASSUMED, build): the births file ends at 2027
    years = sorted(bb); rows = [[y, bb[y].get('Car'), bb[y].get('SUV'), bb[y].get('Pickup'), bb[y].get('Van'), sum(bb[y].values())] for y in years]
    r = write_table(ws, 4, 2, ['Year', 'Car', 'SUV', 'Pickup', 'Van', 'Total'], rows, fmt_by_col={1: F_MONEY, 2: F_MONEY, 3: F_MONEY, 4: F_MONEY, 5: F_MONEY})
    ctx['births'] = (5, r - 1)   # rows holding years in column B, bodies in C..F
    surv = [[int(float(s['age'])), float(s['survival_cars']), float(s['survival_light_trucks'])] for s in read_csv('data/csv/ornl_tedb40_survival_by_age.csv')]
    write_table(ws, 4, 9, ['Age', 'S cars', 'S light trucks'], surv, fmt_by_col={1: '0.000', 2: '0.000'}); ctx['surv'] = (5, 4 + len(surv))
    ws.cell(r + 1, 2, 'Births 2026–2027 hold the final model-year mix and the existing 2025 total (candidate_body_births.csv, ASSUMED); 2028 repeats 2027 (ASSUMED, added at build because the file ends at 2027). Survival beyond the table is zero (age_curves.py convention).').font = font(C_NOTE, i=True, sz=10)
    # ---------------- D Fees
    ws = wb.create_sheet('D Fees'); tab_color(ws, 'BFBFBF'); setup(ws, label_w=14, ncols=12)
    title(ws, 'D Fees — Copart posted buyer fee schedule, read 26 Sep 2026', 'VERIFIED page text (owner-driven browser reads; raw/fees/live_2026-09/). One dated snapshot; its use for history is a proxy. IAA grid and fixed fees alongside.')
    fg = read_csv('data/csv/copart_fee_grid_2026-09.csv'); keys = list(fg[0].keys())
    r = write_table(ws, 4, 2, keys, [[num(x[k]) for k in keys] for x in fg]); ctx['fee_rows'] = (5, r - 1); ctx['fee_keys'] = keys
    ff = read_csv('data/csv/copart_fixed_fees_2026-09.csv'); k2 = list(ff[0].keys())
    ws.cell(r + 1, 2, 'Copart fixed and conditional fees').font = font(b=True); r = write_table(ws, r + 2, 2, k2, [[num(x[k]) for k in k2] for x in ff])
    fi = read_csv('data/csv/iaa_fixed_fees_2026-09.csv'); k3 = list(fi[0].keys())
    ws.cell(r + 1, 2, 'IAA fixed fees (reference; $105 service fee effective 2026-10-01)').font = font(b=True); write_table(ws, r + 2, 2, k3, [[num(x[k]) for k in k3] for x in fi])
    # ---------------- D Carriers
    ws = wb.create_sheet('D Carriers'); tab_color(ws, 'BFBFBF'); setup(ws, label_w=34, ncols=12)
    title(ws, 'D Carriers — inherited carrier weights and Copart allocation paths (share build, 27 Sep 2026)', 'UNVERIFIED: weights are auto premium shares (AM Best/NAIC, mixed years) with salvage intensity 1.0; allocations are expert-call / quote-bank estimates. No Copart disclosure identifies any carrier. Progressive path fitted to the FQ4 FY26 print.')
    per = [p['label'] for p in inputs['periods']]
    rows = [[c['name']] + [round(w, 5) for w in c['weights']] for c in inputs['carriers']]
    r = write_table(ws, 4, 2, ['Carrier weight'] + per, rows, fmt_by_col={i: '0.0000' for i in range(1, 9)}); ctx['carrier_w'] = (5, r - 1)
    rows = [[c['name']] + [round(a, 5) for a in c['allocations']] for c in inputs['carriers']]
    ws.cell(r + 1, 2, 'Copart allocation by carrier (share of that carrier\'s total losses assigned to Copart)').font = font(b=True)
    r = write_table(ws, r + 2, 2, ['Allocation'] + per, rows, fmt_by_col={i: '0.000' for i in range(1, 9)}); ctx['carrier_a'] = (r - len(rows), r - 1)
    ctx['carriers'] = [c['name'] for c in inputs['carriers']]
    ws.cell(r + 1, 2, 'Public anchors: FQ4 FY26 call (US insurance units −7.5%; assignments +2.3% excluding one customer) VERIFIED; listed-inventory split Copart 57.2% of the duopoly, 4 clean nights 11–27 Sep 2026, MEASURED (data/csv/duopoly_daily.csv).').font = font(C_NOTE, i=True, sz=10)
    # ---------------- D Engine
    ws = wb.create_sheet('D Engine'); tab_color(ws, 'BFBFBF'); setup(ws, label_w=44, ncols=12)
    title(ws, 'D Engine — Python engine outputs pasted as values (purple)', 'ENGINE: model/thesis_audit_2026-10-01 (16-subset common-reference scenarios, 1 Oct 2026) and model/ccc_age_body_2026-09-29 (CCC reference and aftermarket cases, 29 Sep 2026). Reproduce with the run.py in each folder.')
    ss = read_csv('model/thesis_audit_2026-10-01/scenario_summary.csv'); k = list(ss[0].keys())
    r = write_table(ws, 4, 2, k, [[num(x[c]) for c in k] for x in ss], kind='engine', fmt_by_col={2: F_MONEY, 3: F_MONEY, 4: F_INT, 5: F_USD}); ctx['eng_ss'] = (5, r - 1)
    fa = read_csv('model/thesis_audit_2026-10-01/factor_attribution.csv'); k = list(fa[0].keys())
    ws.cell(r + 1, 2, 'Four-driver attribution (Shapley, diagnostic)').font = font(b=True); r = write_table(ws, r + 2, 2, k, [[num(x[c]) for c in k] for x in fa], kind='engine')
    qr = read_csv('model/thesis_audit_2026-10-01/quarterly_results.csv'); k = list(qr[0].keys())
    ws.cell(r + 1, 2, 'Quarterly results, all 16 subsets (mask bits: 1 market allocation, 2 premium recovery, 4 aftermarket, 8 fleet mix)').font = font(b=True)
    r = write_table(ws, r + 2, 2, k, [[num(x[c]) for c in k] for x in qr], kind='engine', fmt_by_col={3: F_MONEY, 4: F_INT, 5: F_PCT2, 6: F_USD}); ctx['eng_q'] = (r - len(qr), r - 1)
    cs = read_csv('model/ccc_age_body_2026-09-29/scenario_summary.csv'); k = list(cs[0].keys())
    ws.cell(r + 1, 2, 'CCC family scenario summary (29 Sep): reference $4,093.08m; larger shift $4,002.41m').font = font(b=True); r = write_table(ws, r + 2, 2, k, [[num(x[c]) for c in k] for x in cs], kind='engine'); ctx['eng_ccc_ss'] = (r - len(cs), r - 1)
    cq = read_csv('model/ccc_age_body_2026-09-29/quarterly_results.csv'); k = list(cq[0].keys())[:12]
    ws.cell(r + 1, 2, 'CCC family quarterly results (first 12 columns)').font = font(b=True); r = write_table(ws, r + 2, 2, k, [[num(x[c]) for c in k] for x in cq], kind='engine'); ctx['ccc_q'] = (r - len(cq), r - 1)
    cal = read_csv('model/ccc_age_body_2026-09-29/calibration_cells.csv'); k = list(cal[0].keys())
    ws.cell(r + 1, 2, 'CCC 2025 cell calibration: observed vs calibrated TLF, repair multiplier, derived claim weight, observed TL mix').font = font(b=True)
    r = write_table(ws, r + 2, 2, k, [[num(x[c]) for c in k] for x in cal], kind='engine', fmt_by_col={2: F_PCT2, 3: F_PCT2, 4: F_PCT2, 5: '0.000', 6: '0.0000', 7: '0.0000'}); ctx['cal_rows'] = (r - len(cal), r - 1)
