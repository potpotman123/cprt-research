"""E3 Carriers (thesis A): carrier weights x Copart allocation paths -> aggregate share; seller terms."""
from .common import *
def build(wb, ctx):
    ws = wb.create_sheet('E3 Carriers'); tab_color(ws, '7030A0'); setup(ws)
    std_header(ws, 'Copart share S(q) = Σ_i w_i × a_i(q);  units chain uses S(q) ÷ S(q−4).  Known Progressive runoff is always on; thesis A adds events and drift via toggles.  Appendix A, Eq. 7.', 'E3 Carriers — carrier weights, Copart allocation paths and seller terms (thesis A)')
    section(ws, 5, 'A. Carrier weights: share of the insured total-loss pool (frozen at FQ4 FY26)', quarter_labels())
    names = ctx['carriers']; w0, w1 = ctx['carrier_w']; a0, a1 = ctx['carrier_a']
    PCOL = {(2026, 1): 'C', (2026, 2): 'D', (2026, 3): 'E', (2026, 4): 'F', (2027, 1): 'G', (2027, 2): 'H', (2027, 3): 'I', (2027, 4): 'J'}   # D Carriers period columns
    for i, n in enumerate(names):
        r = 6 + i; label(ws, r, n, 'share', note='D Carriers (UNVERIFIED premium-share proxy; frozen per carrier test 28 Sep)' if i == 0 else '')
        for fy, q in QUARTERS: put(ws, f'{QCOL[(fy,q)]}{r}', f"='D Carriers'!$F${w0+i}", 'link', '0.0000')
    label(ws, 16, '   check: weights sum to one', '', i=True)
    for fy, q in QUARTERS: put(ws, f'{QCOL[(fy,q)]}16', f'=SUM({QCOL[(fy,q)]}6:{QCOL[(fy,q)]}15)', fmt='0.0000', i=True)
    group(ws, 18, 'B. Copart allocation by carrier — base: FY26 inherited reconstruction; from FQ1 FY27 Progressive follows its runoff path and every other carrier is frozen at FQ4 FY26')
    toggle_row = {'GEICO': 66, 'State Farm': 67, 'Other (Erie, AAA, AmFam, regionals)': 68}
    for i, n in enumerate(names):
        r = 19 + i; label(ws, r, n, 'share', note='Progressive: inherited runoff (FITTED to the FQ4 FY26 print), then flat' if n == 'Progressive' else '')
        for fy, q in QUARTERS:
            c = QCOL[(fy, q)]; src = PCOL.get((fy, q), 'J'); inherited = f"'D Carriers'!${src}${a0+i}"; frozen = f"'D Carriers'!$F${a0+i}"
            if fy == 2026 or n == 'Progressive': f = f'={inherited}'
            else: f = f'={frozen}'
            put(ws, f'{c}{r}', f, 'link', '0.000')
    group(ws, 30, 'C. Allocation with thesis-A additions — events switch a carrier to its inherited event path; drift subtracts points per quarter from FQ1 FY27')
    for i, n in enumerate(names):
        r = 31 + i; label(ws, r, n, 'share')
        for fy, q in QUARTERS:
            c = QCOL[(fy, q)]; src = PCOL.get((fy, q), 'J'); inherited = f"'D Carriers'!${src}${a0+i}"; base = f'{c}{19+i}'
            nq = max(0, (fy - 2027) * 4 + q) if fy >= 2027 else 0
            if fy == 2026: f = f'={base}'
            elif n == 'Progressive': f = f'=MAX(0,{base}-$D$70*{nq}*$D$64)'
            elif n in toggle_row: f = f'=MAX(0,IF($D${toggle_row[n]}*$D$64=1,{inherited},{base})-$D$69*{nq}*$D$64)'
            else: f = f'=MAX(0,{base}-$D$69*{nq}*$D$64)'
            put(ws, f'{c}{r}', f, fmt='0.000')
    group(ws, 42, 'D. Aggregate Copart share of the insured total-loss pool')
    label(ws, 43, 'Share, base (known runoff only)', '%', b=True); label(ws, 44, 'Share, with thesis-A additions', '%', b=True)
    label(ws, 45, 'Reference: Copart share of duopoly listed US inventory, 4 clean nights 11–27 Sep 2026', '%', i=True, note='MEASURED, data/csv/duopoly_daily.csv usable=1; listed inventory, not assignments. Mean 57.2%, range 56.8–57.6%')
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        put(ws, f'{c}43', f'=SUMPRODUCT({c}6:{c}15,{c}19:{c}28)', fmt=F_PCT, b=True); put(ws, f'{c}44', f'=SUMPRODUCT({c}6:{c}15,{c}31:{c}40)', fmt=F_PCT, b=True)
    put(ws, f'{QCOL[(2026,4)]}45', ctx['F']('duopoly_listed_share'), 'link', F_PCT)
    annual_avg(ws, 43); annual_avg(ws, 44)
    label(ws, E3_SR_BASE_ROW, 'Share ratio to same quarter a year earlier, base  (→ Scenarios)', 'x', b=True)
    label(ws, E3_SR_A_ROW, 'Share ratio to same quarter a year earlier, thesis A  (→ Scenarios)', 'x', b=True)
    for fy, q in QUARTERS:
        if fy > 2026:
            c, p = QCOL[(fy, q)], QCOL[(fy - 1, q)]
            put(ws, f'{c}{E3_SR_BASE_ROW}', f'={c}43/{p}43', fmt='0.0000', b=True); put(ws, f'{c}{E3_SR_A_ROW}', f'={c}44/{p}43', fmt='0.0000', b=True)
    group(ws, 51, 'E. Seller terms (commission as a share of the vehicle\'s sale price)')
    label(ws, 52, 'Base seller commission rate', '%', note='UNVERIFIED analyst assumption (Barclays 25 Aug 2026 Figure 1 uses 4%); not a contract term')
    label(ws, 53, 'Concession on a contested account (share of the commission)', '%', note='UNVERIFIED (Barclays illustration, 20%)')
    label(ws, 54, 'Share of Copart insurance volume on concession terms (thesis A)', '%', note='ASSUMED; 0 in base')
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        put(ws, f'{c}52', '=$D$71', 'link', F_PCT); put(ws, f'{c}53', '=$D$72', 'link', F_PCT); put(ws, f'{c}54', f'=IF({fy}>=2027,$D$73*$D$64,0)', fmt=F_PCT)
    label(ws, E3_SELLER_BASE_ROW, 'Effective seller commission rate, base  (→ E5)', '%', b=True); label(ws, E3_SELLER_A_ROW, 'Effective seller commission rate, thesis A  (→ E5)', '%', b=True)
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]; put(ws, f'{c}{E3_SELLER_BASE_ROW}', f'={c}52', fmt=F_PCT2, b=True); put(ws, f'{c}{E3_SELLER_A_ROW}', f'={c}52*(1-{c}53*{c}54)', fmt=F_PCT2, b=True)
    put(ws, 'B58', 'Feeds →  Scenarios (share ratios rows 48–49); E5 Prices & Fees (seller rates rows 55–56)', 'note')
    section(ws, 63, 'Inputs and toggles', ['Value', 'Label'])
    items = [(64, 'Thesis A master toggle (1 = additions on; Scenarios reads both states, so leave at 1)', 1, 'toggle', 'TOGGLE', 'Structural switch; Scenarios selects base or thesis-A rows itself'),
             (66, 'GEICO allocation event (inherited: allocation 0.83 → 0.90, a gain for Copart)', 0, 'toggle', 'ASSUMED', 'Share build U5: 60% judgmental probability; off by default in the bear variant'),
             (67, 'State Farm adverse event (inherited: 0.50 → 0.4775 by FQ4 FY27)', 1, 'toggle', 'ASSUMED', 'Share build U7: 45% judgmental; shown as realised case, not probability-weighted'),
             (68, 'Other-carrier drift event (inherited: 0.50 → 0.4775)', 1, 'toggle', 'ASSUMED', 'Share build Events row 15; regional anecdote on a 24% bucket'),
             (69, 'Additional allocation drift, non-Progressive carriers (points per quarter from FQ1 FY27)', 0.0, 'input', 'ASSUMED', 'No evidence; 0 by default. Use only as a labelled stress'),
             (70, 'Additional Progressive decline (points per quarter from FQ1 FY27)', 0.0, 'input', 'ASSUMED', 'The inherited path already reaches 5%'),
             (71, 'Base seller commission rate', ctx['F']('barclays_seller_commission'), 'link', 'UNVERIFIED', 'Barclays 25 Aug 2026 Figure 1 (licensed, local)'),
             (72, 'Concession, share of commission', ctx['F']('barclays_concession'), 'link', 'UNVERIFIED', 'Barclays 25 Aug 2026 Figure 1'),
             (73, 'Share of volume on concession terms when thesis A is on', 0.0, 'input', 'ASSUMED', 'Set in Scenarios; 0 means no retained-account repricing')]
    for row, lab, val, kind, lbl, src in items:
        label(ws, row, lab, note=src); put(ws, f'D{row}', val, kind, '0.000' if (isinstance(val, float) or kind == 'link') else '0'); put(ws, f'E{row}', lbl, 'note')

    # ---- F. probability-weighted moves (memo basis) and G. parity evidence
    group(ws, 76, 'F. Probability-weighted carrier moves (memo basis): expected move = size × probability; the inherited D Carriers paths are these expected moves')
    for j, h in enumerate(['Move (pts)', 'Probability', 'Expected (pts)', 'Path check (pts)', 'Start', 'Ramp (qtrs)']): put(ws, f'{L(4+j)}76', h, 'label', b=True)
    F = ctx['F']
    moves = [(77, 'State Farm — adverse shift to IAA', '=-' + F('precedent_move_pts')[1:], F('expert_prob_sf'), 0, 'FQ3 FY27', 2, 'UNVERIFIED (expert, dated): share build U7 = 45%; Downloads build: RFP out since ~2025, Illinois pilot of ~500 cars to IAA (experts Jan–Aug 2026); sizing from historical 10–20 pt moves over four quarters (share-build precedents, not yet re-read)'),
             (78, 'Other (Erie, AAA, AmFam, regionals) — adverse drift', '=-' + F('precedent_move_pts')[1:], F('expert_prob_other'), 9, 'FQ1 FY27', 4, 'UNVERIFIED (expert, dated): share build Events row 15; YipitData shows IAA additions high in Pennsylvania where Erie is #3; regional anecdote applied to a 24% bucket'),
             (79, 'GEICO — win for Copart (0.83 → 0.95 if realised)', 0.12, F('expert_prob_geico'), 2, 'FQ4 FY26', 3, 'UNVERIFIED (expert, dated): share build U5 = 60%; expert (Jul 2025) put the GEICO RFP 1–2 years out. Off in the bear variant by default'),
             (80, 'Progressive — realised loss (0.25 → 0.05)', -0.20, 1.00, 1, 'FQ3 FY26', 2.2, 'FITTED to the FQ4 FY26 print (carrier test); IAA agreement in principle Feb 2026, executed May 2026, all 50 states (Downloads build, UNVERIFIED expert); Copart call: assignments +2.3% ex one customer (VERIFIED)')]
    for r, lab, size, prob, idx, start, ramp, note in moves:
        label(ws, r, lab, note=note); put(ws, f'D{r}', size, 'link' if isinstance(size, str) else 'input', '0.000'); put(ws, f'E{r}', prob, 'link' if isinstance(prob, str) else 'toggle', F_PCT); put(ws, f'F{r}', f'=D{r}*E{r}', fmt='0.0000')
        put(ws, f'G{r}', f"='D Carriers'!$J${a0+idx}-'D Carriers'!$C${a0+idx}", 'link', '0.0000'); put(ws, f'H{r}', start, 'label'); put(ws, f'I{r}', ramp, 'input', '0.0')
    label(ws, 82, 'Derived: the Progressive move\'s effect on FQ4 FY26 revenue (replaces the memo\'s asserted 5.2%)', b=True)
    label(ws, 83, '   Copart share y/y FQ4 FY26 (carrier test) × insurance share of US service × US share of global service = % of global service revenue; × service share of total = % of total revenue', '%', i=True, note='MEASURED chain: −6.508% share y/y (docs/carrier_test_2026-09-28/results.json, reconstructed, not disclosed) × E5 insurance share × 8-K FY26 US service ÷ global service × service ÷ total revenue')
    g = ctx['geo_rows']; us = '+'.join(f"'D Reported'!$D${g[(2026,q)]}" for q in (1, 2, 3, 4)); intl = '+'.join(f"'D Reported'!$E${g[(2026,q)]}" for q in (1, 2, 3, 4)); veh = '+'.join(f"'D Reported'!$F${g[(2026,q)]}+'D Reported'!$G${g[(2026,q)]}" for q in (1, 2, 3, 4))
    put(ws, 'C83', F('share_yoy_fq4fy26'), 'link', F_PCT2); put(ws, 'D83', f"=C83*'E5 Prices & Fees'!$D$39*({us})/({us}+{intl})", fmt=F_PCT2, b=True); put(ws, 'E83', f"=D83*({us}+{intl})/({us}+{intl}+{veh})", fmt=F_PCT2, b=True); put(ws, 'F83', '← % of service revenue; % of total revenue', 'note')
    group(ws, 85, 'G. Parity evidence (documentation for thesis 3; Copart value, IAA / RB Global value, label, source in Notes)')
    for j, h in enumerate(['Copart', 'IAA / RB Global', 'Label']): put(ws, f'{L(4+j)}85', h, 'label', b=True)
    ev = [(86, 'Operating acreage (owned + leased)', None, F('rba_acres_total'), 'VERIFIED (IAA) / NOT FOUND (Copart)', 'RB Global FY2025 10-K properties table: 6,143 owned + 8,660 leased acres, 333 locations (US 250 locations, 4,431 + 7,769 acres). Copart discloses no acreage in the FY25 or FY26 10-K or any of 17 calls; the memo\'s 19.1k acres needs a citation'),
          (87, 'Operating locations', F('cprt_facilities_fy26'), F('rba_locations'), 'VERIFIED', 'Copart FY2026 10-K Item 2 (281 in FY25); RB Global FY2025 10-K'),
          (88, 'Catastrophe option acreage', None, F('rba_cat_option_acres'), 'VERIFIED (IAA)', 'RB Global FY2025 10-K: agreements to lease and use >1,800 acres in catastrophes; Copart describes CAT capacity qualitatively'),
          (89, 'Average days on lot (cycle time)', F('expert_cycle_days_cprt'), F('expert_cycle_days_iaa'), 'UNVERIFIED', 'Expert calls: former SVP GEICO (Sep 2026), former VP GEICO (Feb 2025) as cited in the memo; no filing measures this'),
          (90, 'Gross margin, FQ4 FY26 (Copart) vs FQ4 FY25', F('cprt_gm_fq4fy26'), F('cprt_gm_fq4fy25'), 'VERIFIED / UNVERIFIED', 'Copart FQ4 FY26 call: 41.8% (VERIFIED, transcript line ~176); 45.3% FQ4 FY25 per memo, to be confirmed from raw/sec/8k/er_2025-09-04'),
          (91, 'Seller contract terms', None, None, 'VERIFIED', 'RB Global 10-K: insurance-supplier agreements cancellable by either party on 30–90 days\' notice. Copart FY2026 10-K (new sentence): certain seller arrangements are non-exclusive and may be terminated or modified on limited notice or without cause'),
          (92, 'Supplier concentration', F('cprt_customer_threshold'), F('rba_top3_supplier_share'), 'VERIFIED', 'Copart 10-K: no customer >10% of revenue (shown as the 10% threshold). RB Global 10-K: top three vehicle suppliers ≈ 23% of FY2025 consolidated revenue'),
          (93, 'Progressive link to RB Global board', None, F('rba_sieger_year'), 'VERIFIED', 'RB Global 2026 proxy: director Michael Sieger, appointed 2023, three decades at Progressive (a former executive, not a Progressive representative)'),
          (94, 'Automotive volume growth, latest quarter', F('cprt_us_ins_units_yoy_fq4fy26'), F('rba_auto_lots_yoy_q2_2026'), 'VERIFIED', 'Copart FQ4 FY26 US insurance units −7.5% (call); RB Global Q2 2026 automotive lots +11% (10-Q), GTV per lot ≈ $3,717 (+2.5%), seller revenue −1% from automotive price incentives'),
          (95, 'Progressive allocation Copart : IAA', F('expert_pgr_alloc_copart'), '=1-' + F('expert_pgr_alloc_copart')[1:], 'UNVERIFIED', 'Expert calls (Downloads build Contract_Calendar); Copart has never named the carrier'),
          (96, 'Dated contract items (expert, UNVERIFIED)', None, None, 'UNVERIFIED', 'State Farm RFP since ~2025 and Illinois pilot; GEICO RFP window 2026–27 (Jul 2025); Liberty Mutual standard 3-year master agreements (Jul 2025); Erie/regionals shifting (YipitData); RB Global Q2 2026 call paraphrase on contracts coming up over three years — all from ~/Downloads/CPRT_share_loss_build.xlsx')]
    for r, lab, cp, ia, lbl, note in ev:
        label(ws, r, lab, note=note)
        for col, v in (('D', cp), ('E', ia)):
            if v is not None: put(ws, f'{col}{r}', v, 'link' if isinstance(v, str) else 'input', F_PCT if r in (90, 92, 94, 95) else F_INT)
        put(ws, f'F{r}', lbl, 'note')
    ws.freeze_panes = 'D6'
