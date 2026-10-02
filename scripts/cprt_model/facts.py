"""D Facts: every verified or measured datum that an engine tab uses as a number, in one data tab with source, date and file.
Engine tabs link to these cells (green) instead of typing the values. ctx['F'](key) returns the cell reference."""
from .common import *
FACTS = [  # key, label, value, unit, evidence label, source, date, file or URL
 ('cprt_us_ins_asp_yoy_fq4fy26', 'Copart US insurance ASP, y/y, FQ4 FY26', 0.037, '%', 'VERIFIED', 'Copart FQ4 FY26 earnings call (CFO remarks)', '2026-09-10', 'raw/transcripts/call_2026-09-10.txt lines 216–226; SEC-filed exhibit'),
 ('manheim_yoy_fq4fy26', 'Manheim Used Vehicle Value Index, y/y, FQ4 FY26 as cited by Copart', 0.028, '%', 'VERIFIED', 'Copart FQ4 FY26 call', '2026-09-10', 'raw/transcripts/call_2026-09-10.txt'),
 ('cprt_gm_fq4fy26', 'Copart gross margin, FQ4 FY26', 0.418, '%', 'VERIFIED', 'Copart FQ4 FY26 call', '2026-09-10', 'raw/transcripts/call_2026-09-10.txt ~line 176'),
 ('cprt_gm_fq4fy25', 'Copart gross margin, FQ4 FY25 (memo figure)', 0.453, '%', 'UNVERIFIED', 'Memo draft; to confirm from the FQ4 FY25 8-K exhibit', '2026-10-01', 'raw/sec/8k/er_2025-09-04_cprt07312025ex99-1.htm (not yet read for this figure)'),
 ('cprt_us_ins_units_yoy_fq4fy26', 'Copart US insurance units sold, y/y, FQ4 FY26', -0.075, '%', 'VERIFIED', 'Copart FQ4 FY26 call and 8-K', '2026-09-10', 'raw/sec/8k/er_2026-09-10_cprt-ex99_1.htm'),
 ('cprt_facilities_fy26', 'Copart operating facilities, FY2026 10-K', 286, 'count', 'VERIFIED', 'Copart FY2026 10-K Item 2', '2026-09-29', 'raw/sec/10k/cprt_2026-07-31.htm'),
 ('cprt_ins_share_vehicles_fy26', 'Share of vehicles processed from insurance sellers, FY26 (81% FY25, 81% FY24)', 0.79, '%', 'VERIFIED', 'Copart FY2026 10-K, Sales', '2026-09-29', 'raw/sec/10k/cprt_2026-07-31.htm'),
 ('cprt_customer_threshold', 'Copart: no customer above this share of revenue', 0.10, '%', 'VERIFIED', 'Copart FY2026 10-K', '2026-09-29', 'raw/sec/10k/cprt_2026-07-31.htm'),
 ('rba_acres_total', 'RB Global operating acreage, owned 6,143 + leased 8,660, 31 Dec 2025', 14803, 'acres', 'VERIFIED', 'RB Global FY2025 10-K, Properties table', '2026-02-25', 'raw/sec/rba/10k_2025-12-31.htm'),
 ('rba_locations', 'RB Global operating locations, 31 Dec 2025', 333, 'count', 'VERIFIED', 'RB Global FY2025 10-K, Properties table', '2026-02-25', 'raw/sec/rba/10k_2025-12-31.htm'),
 ('rba_cat_option_acres', 'RB Global option acreage for catastrophe response (more than)', 1800, 'acres', 'VERIFIED', 'RB Global FY2025 10-K', '2026-02-25', 'raw/sec/rba/10k_2025-12-31.htm'),
 ('rba_top3_supplier_share', 'RB Global revenue from its three largest vehicle suppliers, FY2025', 0.23, '%', 'VERIFIED', 'RB Global FY2025 10-K, risk factors', '2026-02-25', 'raw/sec/rba/10k_2025-12-31.htm'),
 ('rba_auto_lots_yoy_q2_2026', 'RB Global automotive lots sold, y/y, Q2 2026 (658.8k vs 595.9k)', 0.11, '%', 'VERIFIED', 'RB Global Q2 2026 10-Q', '2026-08-04', 'raw/sec/rba/10q_2026-06-30.htm'),
 ('rba_gtv_per_lot_q2_2026', 'RB Global automotive GTV per lot, Q2 2026 ($2,448.7m ÷ 658.8k)', 3717, '$', 'MEASURED', 'Computed from the Q2 2026 10-Q', '2026-08-04', 'raw/sec/rba/10q_2026-06-30.htm'),
 ('rba_take_rate_q2_2026', 'RB Global service revenue take rate, Q2 2026 (21.1% a year earlier)', 0.200, '%', 'VERIFIED', 'RB Global Q2 2026 earnings release', '2026-08-04', 'raw/sec/rba/8k_2026-08-04_ex99_1.htm'),
 ('rba_sieger_year', 'RB Global director Michael Sieger (three decades at Progressive) appointed', 2023, 'year', 'VERIFIED', 'RB Global 2026 proxy statement', '2026-03-19', 'raw/sec/rba/def14a_2026.htm'),
 ('share_yoy_fq4fy26', 'Copart share of the insured total-loss pool, y/y, FQ4 FY26 (reconstruction)', -0.06508, '%', 'MEASURED', 'Carrier compatibility test from the inherited share build', '2026-09-28', 'docs/carrier_test_2026-09-28/results.json'),
 ('duopoly_listed_share', 'Copart share of Copart + IAA listed US inventory, mean of 4 clean nights 11–27 Sep 2026', 0.572, '%', 'MEASURED', 'Nightly sitemap collector', '2026-09-27', 'data/csv/duopoly_daily.csv (usable = 1)'),
 ('ccc_am_dollar_share_2025', 'Aftermarket share of replacement-part dollars, 2025 (21.0% in 2024)', 0.227, '%', 'VERIFIED', 'CCC Crash Course 2026', '2026-03', 'docs/bidmate_adoption_2026-09-29; https://www.cccis.com/reports/crash-course-2026'),
 ('ccc_am_dollar_share_2024', 'Aftermarket share of replacement-part dollars, 2024', 0.210, '%', 'VERIFIED', 'CCC Crash Course 2026', '2026-03', 'same'),
 ('ccc_rec_dollar_share_2025', 'Recycled share of replacement-part dollars, 2025 (10.7% in 2024)', 0.105, '%', 'VERIFIED', 'CCC Crash Course 2026', '2026-03', 'same'),
 ('ccc_rec_dollar_share_2024', 'Recycled share of replacement-part dollars, 2024', 0.107, '%', 'VERIFIED', 'CCC Crash Course 2026', '2026-03', 'same'),
 ('ccc_oem_dollar_share_2025', 'OEM share of replacement-part dollars, 2025 (1 − AM − recycled)', 0.668, '%', 'MEASURED', 'Derived from the two CCC shares', '2026-03', 'same'),
 ('ccc_parts_share_of_bill_low', 'Parts as a share of the repair bill, CCC, by vehicle age (low end)', 0.36, '%', 'VERIFIED', 'CCC Crash Course 2026', '2026-03', 'docs/aftermarket_parameter_audit_2026-09-29'),
 ('ccc_parts_share_of_bill_high', 'Parts as a share of the repair bill, CCC, by vehicle age (high end)', 0.44, '%', 'VERIFIED', 'CCC Crash Course 2026', '2026-03', 'docs/aftermarket_parameter_audit_2026-09-29'),
 ('mitchell_am_discount_2016_mean', 'Aftermarket discount to OEM, 2016, mean of domestic 23.3%, Asian 29.9%, European 27.7%', 0.27, '%', 'VERIFIED (historical)', 'Mitchell Industry Trends Report Q2 2017, pp. 8–10', '2017-06', 'docs/aftermarket_transition_evidence_2026-09-29/mitchell_discount_history.csv; raw cache'),
 ('maplev_am_price_ratio_2026', 'Aftermarket list price relative to OEM, 259 matched Tesla part numbers (vendor catalogue, Canada)', 0.50, 'x', 'VERIFIED (narrow)', 'MapleV catalogue comparison', '2026-09', 'https://maplev.ca/guides/tesla-collision-part-prices-canada/'),
 ('partstrader_oem_inflation', 'New OEM part price inflation, April 2025 – March 2026 (PartsTrader Collision Parts Price Index)', 0.043, '%', 'VERIFIED (republication)', 'PartsTrader, Spring 2026 Collision Industry Report, via its own site and Repairer Driven News 8 May 2026', '2026-05-08', 'raw/discovery_2026-10-02/partstrader_beyond_tariffs.html; rdn_partstrader_2026-05.html'),
 ('partstrader_am_inflation', 'Aftermarket part price inflation over the same period ("under 1%", "essentially flat" despite tariffs)', 0.01, '%', 'VERIFIED (republication; upper bound)', 'PartsTrader, same report', '2026-05-08', 'same'),
 ('partstrader_recycled_pricing', 'Recycled parts are priced as a percentage of the new OE part they replace and "track closely behind" OEM inflation (1 = yes)', 1, 'flag', 'VERIFIED (republication)', 'PartsTrader, same report', '2026-05-08', 'same'),
 ('partstrader_delivery_days_am', 'Median delivery days, aftermarket parts, Jan–Mar 2026 (OEM 6.9 all-parts median; recycled 3.4–3.8)', 3.0, 'days', 'VERIFIED (republication)', 'PartsTrader, same report', '2026-05-08', 'same'),
 ('engine_asp0', 'Engine modeled selected-vehicle price at the FY26 anchor', 3040.99, '$', 'ENGINE', 'Age-constrained selection engine, baseline_core.ASP', '2026-09-28', 'docs/fleet_selection_2026-09-28/age_constrained_engine_results.json'),
 ('engine_core_rpu0', 'Engine core RPU at the anchor (buyer fees + seller commission + fixed fees)', 851.51, '$', 'ENGINE', 'baseline_core.core_RPU', '2026-09-28', 'docs/fleet_selection_2026-09-28/age_constrained_engine_results.json'),
 ('engine_value_plus5_asp', 'Engine +5% value test: ASP change', 0.040401548, '%', 'ENGINE', 'scenario_changes value_plus_5pct.ASP', '2026-09-28', 'same'),
 ('engine_value_plus5_rpu', 'Engine +5% value test: core RPU change', 0.017859212, '%', 'ENGINE', 'scenario_changes value_plus_5pct.core_RPU', '2026-09-28', 'same'),
 ('experian_vio_2024', 'Vehicles in operation, US, 2024 (thousands)', 292000, '000s', 'UNVERIFIED', 'Experian Automotive figure recorded on disk; file to be cited', '2026-09', 'see PROVENANCE www.experian.com entry'),
 ('sp_fleet_share_7plus_2024', 'Share of US light vehicles aged 7+ years, 2024', 0.66, '%', 'UNVERIFIED', 'Recalled S&P Global Mobility release; not on disk', '2024', 'docs/AGE_CURVES.md §2.4'),
 ('barclays_seller_commission', 'Seller commission rate in Barclays\' contract illustration', 0.04, '%', 'UNVERIFIED (licensed)', 'Barclays, U.S. Auto Retail: CPRT vs RBA, Figure 1', '2026-08-25', 'licensed report held locally; docs/repair_research_2026-09-26/contract_scope_screen'),
 ('barclays_concession', 'Concession on a contested account, share of commission (Barclays illustration)', 0.20, '%', 'UNVERIFIED (licensed)', 'Barclays Figure 1', '2026-08-25', 'same'),
 ('jpm_fy27_service', 'JPMorgan FY27 legacy service revenue, ex-ACV ($m)', 4061, '$M', 'VERIFIED (licensed)', 'JPMorgan, Copart F4Q review, Table 3', '2026-09-11', 'licensed report held locally; model/revenue_architecture_2026-09-28/evidence_manifest.json'),
 ('expert_pgr_alloc_copart', 'Progressive allocation to Copart after the move (expert estimate; IAA 95%)', 0.05, '%', 'UNVERIFIED (expert)', 'Expert calls summarised in the owner\'s share-loss build', '2026-05', '~/Downloads/CPRT_share_loss_build.xlsx Contract_Calendar'),
 ('expert_cycle_days_cprt', 'Average days on lot, Copart (expert estimate)', 52, 'days', 'UNVERIFIED (expert)', 'Former SVP GEICO (Sep 2026), former VP GEICO (Feb 2025)', '2026-09', 'memo draft; expert transcripts held by the owner'),
 ('expert_cycle_days_iaa', 'Average days on lot, IAA (expert estimate)', 50, 'days', 'UNVERIFIED (expert)', 'same', '2026-09', 'same'),
 ('expert_prob_sf', 'Probability State Farm shifts volume away from Copart in FY27', 0.45, '%', 'UNVERIFIED (expert rubric)', 'Share build probability rubric U7', '2026-09-27', 'docs/FABLE_SHARE_BUILD_REVIEW_2026-09-27.md'),
 ('expert_prob_other', 'Probability regional carriers (Erie, AAA, AmFam) shift volume away', 0.45, '%', 'UNVERIFIED (expert rubric)', 'Share build Events row 15', '2026-09-27', 'same'),
 ('expert_prob_geico', 'Probability of a GEICO allocation win for Copart', 0.60, '%', 'UNVERIFIED (expert rubric)', 'Share build U5', '2026-09-27', 'same'),
 ('precedent_move_pts', 'Typical carrier allocation move in historical precedents (points, phased over four quarters)', 0.05, 'pts', 'UNVERIFIED (expert)', 'Share build historical-precedents tab (10–20 point moves; 5 used per event)', '2026-09-27', 'same; tab not re-read in this environment'),
]
def build(wb, ctx):
    ws = wb.create_sheet('D Facts'); tab_color(ws, 'BFBFBF'); setup(ws, label_w=72, ncols=6, notes_col='J')
    title(ws, 'D Facts — every verified, measured or second-hand datum the engines use as a number', 'One row per fact: value, unit, evidence label, source, date, file or URL. Engine tabs link here (green); nothing on an engine tab retypes these values.')
    for j, h in enumerate(['Fact', 'Key', 'Value', 'Unit', 'Label', 'Source', 'Date', 'File / URL']): put(ws, f'{L(2+j)}4', h, 'label', b=True)
    ws.column_dimensions['C'].width = 28; ws.column_dimensions['G'].width = 24; ws.column_dimensions['H'].width = 46; ws.column_dimensions['I'].width = 12; ws.column_dimensions['J'].width = 70
    refs = {}
    for i, (key, lab, val, unit, lbl, src, date, path) in enumerate(FACTS):
        r = 5 + i; put(ws, f'B{r}', lab, 'label'); put(ws, f'C{r}', key, 'note')
        fmt = F_PCT if unit in ('%', 'pts') else F_USD if unit == '$' else F_INT if unit in ('000s', 'acres', 'count', 'days', '$M') else '0' if unit == 'year' else '0.000'
        put(ws, f'D{r}', val, 'input', fmt); put(ws, f'E{r}', unit, 'label', i=True); put(ws, f'F{r}', lbl, 'note'); put(ws, f'G{r}', lbl, 'note'); put(ws, f'H{r}', src, 'note'); put(ws, f'I{r}', date, 'note'); put(ws, f'J{r}', path, 'note')
        refs[key] = f"'D Facts'!$D${r}"
    ctx['F'] = lambda key: '=' + refs[key]; ctx['fact_refs'] = refs; ws.freeze_panes = 'D5'
