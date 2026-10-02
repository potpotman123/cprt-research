"""Thesis 1: D Coverage data tab and E2 block F (physical-damage coverage index, premium burden, forward coverage paths)."""
import csv, collections
from .common import *
def bls_annual(path, series):
    months = collections.defaultdict(list); latest = []
    for line in open(ROOT / path):
        p = line.rstrip('\n').split('\t')
        if len(p) < 4 or p[0].strip() != series: continue
        y, per, val = p[1].strip(), p[2].strip(), p[3].strip()
        if per == 'M13' or not val.replace('.', '').isdigit(): continue
        months[int(y)].append(float(val)); latest.append((int(y), per, float(val)))
    return {y: sum(v) / len(v) for y, v in months.items()}, sorted(latest)
def build(wb, ctx):
    cpi, cpi_m = bls_annual('raw/bls/cu.data.14.USTransportation', 'CUUR0000SETE')
    ahe, ahe_m = bls_annual('raw/bls/ce.data.05b.TotalPrivate.AllEmployeeHoursAndEarnings', 'CES0500000003')
    years = list(range(2017, 2027))
    # ---------------- D Coverage
    ws = wb.create_sheet('D Coverage'); tab_color(ws, 'BFBFBF'); setup(ws, label_w=46, ncols=12)
    title(ws, 'D Coverage — insurance affordability and physical-damage coverage (thesis 1 data)', 'Values only. BLS CPI motor vehicle insurance (CUUR0000SETE) and CES average hourly earnings (CES0500000003) from flat files on disk (raw/bls, fetched 25 Sep 2026); IRC press release 20 Feb 2025 (raw/irc); III analysis of 2023 NAIC data (raw/discovery_2026-10-02); CCC claim volumes from the owner\'s v1 Volume Build (CCC reports).')
    for j, y in enumerate(years): put(ws, f'{L(4+j)}4', y, 'label', b=True)
    put(ws, 'B4', 'Calendar year', 'label', b=True)
    rows = [('CPI motor vehicle insurance, annual average (1982–84 = 100)', [cpi.get(y) for y in years], '0.0', 'VERIFIED — raw/bls/cu.data.14.USTransportation, series CUUR0000SETE, annual = mean of months (2026 = Jan–Aug)'),
            ('   y/y', [None] + [cpi[y] / cpi[y - 1] - 1 if y in cpi and (y - 1) in cpi else None for y in years[1:]], F_PCT, ''),
            ('Average hourly earnings, total private, annual average ($)', [ahe.get(y) for y in years], '0.00', 'VERIFIED — raw/bls/ce.data.05b.TotalPrivate.AllEmployeeHoursAndEarnings, series CES0500000003 (2026 = months to date)'),
            ('Uninsured-motorist rate (share of drivers), IRC', [0.124, None, None, None, None, None, 0.154, None, None, None], F_PCT, 'VERIFIED endpoints — IRC release 20 Feb 2025: 15.4% in 2023, "an increase of 3% over the six years"; 2017 = 15.4 − 3.0 = 12.4% (derived); yearly path not in the release'),
            ('Share of insured drivers buying collision coverage, NAIC via III', [None, None, None, None, 0.76, 0.77, 0.77, None, None, None], F_PCT, 'VERIFIED republication — III Facts + Statistics: 2021 NAIC data 76% (Wayback snapshot 2 Jun 2024, raw/wayback/iii_auto_20240602004547.html); 2022 data 77% (snapshot 27 Sep 2025); 2023 data 77% (live page, raw/discovery_2026-10-02). Comprehensive 80% in all three. NAIC\'s own report refused the fetch (403); pre-2021 pages rate-limited (429), not pursued'),
            ('CCC total claim volume, y/y', [None, None, None, None, None, None, None, -0.077, -0.033, None], F_PCT, 'VERIFIED — owner\'s v1 Volume Build row 10 ("all from CCC reports"); calendar 2024 and 2025'),
            ('CCC claim volume excluding comprehensive, y/y', [None, None, None, None, None, None, None, -0.057, -0.016, None], F_PCT, 'VERIFIED — v1 Volume Build row 11'),
            ('CCC repairable claim volume, y/y', [None, None, None, None, None, None, None, -0.097, None, None], F_PCT, 'VERIFIED — v1 Volume Build row 12')]
    for i, (lab, vals, fmt, note) in enumerate(rows):
        r = 5 + i; label(ws, r, lab, note=note, i=lab.startswith('   '))
        for j, v in enumerate(vals):
            if v is not None: put(ws, f'{L(4+j)}{r}', v, 'input', fmt)
    r = 14; put(ws, f'B{r}', 'CPI motor vehicle insurance, monthly, latest 14 months (NSA)', 'label', b=True)
    for j, (y, per, v) in enumerate(cpi_m[-14:]):
        put(ws, f'{L(4+j)}{r+1}', f'{y}-{per[1:]}', 'label'); put(ws, f'{L(4+j)}{r+2}', v, 'input', '0.0')
        prior = [x for x in cpi_m if x[0] == y - 1 and x[1] == per]
        if prior: put(ws, f'{L(4+j)}{r+3}', v / prior[0][2] - 1, 'input', F_PCT)
    put(ws, f'B{r+2}', 'index', 'label'); put(ws, f'B{r+3}', '   y/y', 'label', i=True)
    put(ws, f'B{r+5}', 'S&P Global Market Intelligence, 2025 US Auto Insurance Market Report (data compiled 3 Dec 2025), as published by Carrier Management 6 Jan 2026 (raw/discovery_2026-10-02/carriermanagement_spgmi_outlook_2026.html and three chart images). S&P\'s own page refused the fetch (403).', 'label', b=True)
    for k, (lab, val, note) in enumerate([('Auto (private + commercial) combined ratio, 2025P', 94.5, 'VERIFIED (republication) — article text'), ('Auto combined ratio, 2026P', 97.1, 'VERIFIED (republication) — article text; "matching 2024"'), ('Auto combined ratio, 2027P', 98.9, 'VERIFIED (republication) — article text; breaches 100 in 2028'),
                                            ('Auto share of total US P&C direct premiums written, 2024A (peak)', 0.412, 'VERIFIED (republication) — chart spgmi_premium_growth_2015_2029.jpg'), ('Auto share of P&C premiums, 2026P / 2027P', 0.4037, 'VERIFIED (republication) — chart: 40.37% 2026P, 40.09% 2027P, 39.90% 2029P: auto premiums grow slower than other lines'),
                                            ('Private auto direct premiums written growth outlook, 2025 (revised)', 0.046, 'VERIFIED (republication) — chart spgmi_premium_outlook_by_line.jpg, read from the bar (about 4.6%)'),
                                            ('S&P on 2026 private auto pricing: "rate decreases matching rate increases and increased advertising spending"', None, 'VERIFIED (republication) — media statement quoted in the article. S&P publishes no 2026–27 premium-growth percentage in the accessible material')]):
        rr = r + 6 + k; label(ws, rr, lab, note=note)
        if val is not None: put(ws, f'D{rr}', val, 'input', F_PCT if val < 1 else '0.0')
    put(ws, f'B{r+14}', 'MoneyGeek lapse study (raw/discovery_2026-10-02/moneygeek_lapse.html): a coverage gap longer than 30 days raises quoted premiums by 22.4% on average across nine insurers; a gap of 30 days or less by 10.6%. Rate-comparison estimate, not a filing.', 'note')
    ctx['cov_years'] = years; ctx['cov_rows'] = {'cpi': 5, 'ahe': 7, 'um': 8, 'coll': 9}
    # ---------------- E2 block F
    e2 = wb['E2 Claims & Totals']; cy = {y: L(4 + j) for j, y in enumerate(years)}
    group(e2, 103, 'F. Coverage & filing (thesis 1): physical-damage coverage index, premium burden, and forward coverage paths')
    put(e2, 'B104', 'Calendar year', 'label', b=True)
    for y in years: put(e2, f'{cy[y]}104', y, 'label', b=True)
    label(e2, 105, 'Uninsured-motorist rate (IRC; endpoints verified, path interpolated)', '%', note='UNVERIFIED path: linear between 2017 and 2023; 2024–26 held at 2023 (IRC notes UM "continues to tick upward")')
    label(e2, 106, 'Share of insured drivers with collision coverage (NAIC via III: 76% 2021, 77% 2022, 77% 2023)', '%', note='2017–2020 held at the 2021 value and 2024–26 at the 2023 value (archive pages before 2024 were rate-limited). Collision take-up did not fall through the premium spike, so the index decline comes from the uninsured leg')
    label(e2, 107, 'Physical-damage coverage index  (1 − uninsured) × collision share, 2025 = 1', 'x', b=True)
    label(e2, 108, 'Premium burden: insurance CPI ÷ average hourly earnings, 2025 = 1', 'x')
    label(e2, 109, '   premium burden y/y', '%', i=True)
    for j, y in enumerate(years):
        c = cy[y]
        if y <= 2017: um = f"='D Coverage'!D8"
        elif y >= 2023: um = f"='D Coverage'!J8"
        else: um = f"='D Coverage'!$D$8+('D Coverage'!$J$8-'D Coverage'!$D$8)*({y}-2017)/6"
        coll = "='D Coverage'!$H$9" if y <= 2021 else ("='D Coverage'!$I$9" if y == 2022 else "='D Coverage'!$J$9")
        put(e2, f'{c}105', um, 'link', F_PCT); put(e2, f'{c}106', coll, 'link', F_PCT)
        put(e2, f'{c}107', f'=(1-{c}105)*{c}106/((1-$L$105)*$L$106)', fmt='0.0000', b=True)
        put(e2, f'{c}108', f"=('D Coverage'!{c}5/'D Coverage'!{c}7)/('D Coverage'!$L$5/'D Coverage'!$L$7)", fmt='0.0000')
        if j: put(e2, f'{c}109', f'={c}108/{cy[years[j-1]]}108-1', fmt=F_PCT, i=True)
    for j, y in enumerate((2027, 2028)):
        c = L(14 + j); put(e2, f'{c}104', y, 'label', b=True); put(e2, f'{c}107', '=$M$107', fmt='0.0000', b=True)
    put(e2, 'P107', 'sticky path shown for 2027–28 (flat); the premium-response and recovery paths are the quarterly ratios in rows 117–118', 'note')
    label(e2, 110, 'Two-point coverage response ε = −ln(C₂₀₂₃ ÷ C₂₀₁₇) ÷ ln(B₂₀₂₃ ÷ B₂₀₁₇)', 'x', note='UNVERIFIED: two observations only; sign and scale indicative. Used solely in the premium-response path below')
    put(e2, 'D110', '=-LN(J107/D107)/LN(J108/D108)', fmt='0.000')
    label(e2, 111, 'Context: CCC total claim volume y/y (2024, 2025) and ex-comprehensive', '%', i=True, note='Coverage explains only part of the claim-volume decline; frequency and non-filing explain the rest')
    put(e2, 'K111', "='D Coverage'!K10", 'link', F_PCT); put(e2, 'L111', "='D Coverage'!L10", 'link', F_PCT); put(e2, 'K112', "='D Coverage'!K11", 'link', F_PCT); put(e2, 'L112', "='D Coverage'!L11", 'link', F_PCT); label(e2, 112, '   ex-comprehensive', '%', i=True)
    group(e2, 114, 'Forward coverage ratios to the same quarter a year earlier, by path  (→ Scenarios units chain)')
    put(e2, 'B115', 'Path', 'label', b=True)
    for fy, q in QUARTERS: put(e2, f'{QCOL[(fy,q)]}115', qlabel(fy, q), 'label', b=True)
    label(e2, E2_COV_STICKY_ROW, 'Sticky (thesis 1): coverage stays at the 2025 level', 'x', b=True, note='The thesis: lapsed physical-damage coverage does not return because price and friction (lapse surcharges) have not improved')
    label(e2, E2_COV_PREMIUM_ROW, 'Premium-response (threshold): no recovery while the burden is at or above its 2023 level; below it, ratio = (B_q ÷ B_{q−4})^(−ε)', 'x', b=True, note='Mechanistic bull path with hysteresis: coverage returns only once premiums relative to pay fall back below the level at which households left (2023 = 0.867)')
    label(e2, 119, 'Premium burden path (2025 = 1): FY27 = 2026 × (1 + premium growth − earnings growth); FY28 steps again', 'x', note='Inputs rows 123–125; selector row 127 chooses the BLS observed trend or the S&P-consistent path')
    label(e2, 120, '   below the 2023 level? (1 = yes)', 'flag', i=True)
    label(e2, E2_COV_RECOVERY_ROW, 'Street-implied recovery: FY27 ratio reverse-solved so case 0 reaches JPM $4,061m; FY28 held', 'x', b=True, note='r = (JPM − case 1 legacy FY27) ÷ case 1 US insurance service FY27 (identity; RPU unchanged)')
    for fy, q in QUARTERS:
        c = QCOL[(fy, q)]
        if fy == 2026: continue
        put(e2, f'{c}{E2_COV_STICKY_ROW}', 1.0, 'formula', '0.0000', b=True)
        prev = '$M$108' if fy == 2027 else f'{QCOL[(fy-1,q)]}119'
        put(e2, f'{c}119', f'={prev}*(1+$D$123-$D$124)' if fy == 2027 else f'={prev}*(1+$D$125-$D$124)', fmt='0.0000')
        put(e2, f'{c}120', f'=IF({c}119<$J$108,1,0)', fmt='0')
        put(e2, f'{c}{E2_COV_PREMIUM_ROW}', f'=IF({c}119>=$J$108,1,({c}119/{prev})^(-$D$110))', fmt='0.0000', b=True)
        put(e2, f'{c}{E2_COV_RECOVERY_ROW}', '=1+$D$126' if fy == 2027 else 1.0, 'formula', '0.0000', b=True)
    section(e2, 122, 'Coverage inputs', ['Value', 'Label'])
    items = [(123, 'Premium growth, FY27 (selected path)', '=IF($F$127=1,$D$128,$D$129)', 'formula', 'selected', 'Row 127 selects: 1 = BLS observed trend (row 128); 2 = S&P-consistent path (rows 129–130)'),
             (124, 'Earnings growth, FY27 and FY28 (CES average hourly earnings, latest year y/y)', f"='D Coverage'!M7/'D Coverage'!L7-1", 'link', 'VERIFIED', 'raw/bls CES0500000003'),
             (125, 'Premium growth, FY28 (selected path)', '=IF($F$127=1,$D$128,$D$130)', 'formula', 'selected', 'BLS trend continued, or the S&P-consistent FY28 step'),
             (126, 'r: Street-implied FY27 coverage recovery (reverse-solved, live)', None, 'formula', 'MEASURED', 'Identity from Scenarios case 1 and the JPM benchmark; recomputes with every input change'),
             (127, 'Premium path selector (click D127 to choose; index in F127): BLS observed trend or S&P-consistent', 1, 'toggle', 'TOGGLE', 'Both paths shown on Key Drivers'),
             (128, 'BLS CPI motor vehicle insurance, latest month y/y (Aug 2026)', "='D Coverage'!Q17", 'link', 'VERIFIED', 'raw/bls CUUR0000SETE'),
             (129, 'S&P-consistent premium growth, FY27', 0.0, 'input', 'ASSUMED', 'S&P (Dec 2025): 2026 private auto pricing with "rate decreases matching rate increases"; no percentage published. Flat is our reading, not an S&P number'),
             (130, 'S&P-consistent premium growth, FY28', 0.03, 'input', 'ASSUMED', 'S&P projects auto combined ratios rising to 98.9 in 2027 and above 100 in 2028, implying renewed rate increases; +3% is our reading of that path, not an S&P number'),
             (131, 'First quarter in which the burden falls below its 2023 level (selected path)', '=IFERROR(INDEX($D$115:$O$115,MATCH(1,$D$120:$O$120,0)),"beyond FQ4 FY28")', 'formula', 'MEASURED', 'Row 120 flags; the date the bull mechanism could start, on the selected path')]
    for row, lab, val, kind, lbl, src in items:
        label(e2, row, lab, note=src)
        if val is not None: put(e2, f'D{row}', val, kind, F_PCT if row != 131 else '@')
        put(e2, f'E{row}', lbl, 'note')
    ctx['cov_r_cell'] = "'E2 Claims & Totals'!$D$126"
    dropdown(e2, 'D127', ['1 · BLS trend', '2 · S&P path'], index_cell='F127', default_index=1, list_col='U', list_row=123, title='Premium-path options (list source for D127)')
