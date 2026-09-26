#!/usr/bin/env python3
"""Build docs/walkthrough.html — the model walk-through page (how the units identity was reached, the evidence charts,
the theses the build supports). Charts are inline SVG generated from data/csv; no external libraries.
Usage: ./.venv/bin/python scripts/build_walkthrough_page.py"""
import csv, math, pathlib, re, html as H
ROOT = pathlib.Path(__file__).resolve().parent.parent; D = ROOT / 'data/csv'
def rd(f): return [r for r in csv.DictReader(l for l in open(D / f) if not l.startswith('#'))]
W, HT, ML, MR, MT, MB = 720, 380, 60, 20, 26, 48
def nice_ticks(lo, hi, n=5):
    span = hi - lo or 1; raw = span / n; mag = 10 ** math.floor(math.log10(raw)); step = min((m for m in (1, 2, 2.5, 5, 10) if m * mag >= raw), key=lambda m: m) * mag
    t0 = math.floor(lo / step) * step; ticks = []; t = t0
    while t <= hi + 1e-9: ticks.append(round(t, 10)); t += step
    return ticks
def fmt(v, unit=''):
    s = f"{v:,.0f}" if abs(v) >= 100 or float(v).is_integer() else (f"{v:.1f}" if abs(v) >= 1 else f"{v:.2f}")
    return s + unit
class Chart:
    def __init__(self, xlo, xhi, ylo, yhi, xlabel, ylabel, xunit='', yunit='', height=HT):
        self.h = height; self.xs = nice_ticks(xlo, xhi); self.ys = nice_ticks(ylo, yhi)
        self.xlo, self.xhi, self.ylo, self.yhi = self.xs[0], self.xs[-1], self.ys[0], self.ys[-1]
        self.parts = []; self.xlabel, self.ylabel, self.xunit, self.yunit = xlabel, ylabel, xunit, yunit
    def X(self, v): return ML + (v - self.xlo) / (self.xhi - self.xlo) * (W - ML - MR)
    def Y(self, v): return MT + (self.yhi - v) / (self.yhi - self.ylo) * (self.h - MT - MB)
    def frame(self):
        g = []
        for t in self.ys: g.append(f'<line x1="{ML}" x2="{W-MR}" y1="{self.Y(t):.1f}" y2="{self.Y(t):.1f}" class="grid"/><text x="{ML-8}" y="{self.Y(t)+4:.1f}" class="tick" text-anchor="end">{fmt(t, self.yunit)}</text>')
        for t in self.xs: g.append(f'<text x="{self.X(t):.1f}" y="{self.h-MB+18}" class="tick" text-anchor="middle">{fmt(t, self.xunit)}</text>')
        if self.ylo < 0 < self.yhi: g.append(f'<line x1="{ML}" x2="{W-MR}" y1="{self.Y(0):.1f}" y2="{self.Y(0):.1f}" class="zero"/>')
        g.append(f'<text x="{(ML+W-MR)/2:.0f}" y="{self.h-8}" class="axis" text-anchor="middle">{H.escape(self.xlabel)}</text>')
        g.append(f'<text transform="translate(14 {(MT+self.h-MB)/2:.0f}) rotate(-90)" class="axis" text-anchor="middle">{H.escape(self.ylabel)}</text>')
        return "".join(g)
    def svg(self, title):
        return f'<svg viewBox="0 0 {W} {self.h}" role="img" aria-label="{H.escape(title)}" class="chart">{self.frame()}{"".join(self.parts)}</svg>'
def table(rows, cols):
    return '<details><summary>Data</summary><div class="tbl"><table><thead><tr>' + "".join(f'<th>{H.escape(c)}</th>' for c in cols) + '</tr></thead><tbody>' + "".join('<tr>' + "".join(f'<td>{H.escape(str(v))}</td>' for v in r) + '</tr>' for r in rows) + '</tbody></table></div></details>'

# ---------------------------------------------------------------- data
tlf = {r['quarter']: float(r['all_loss_categories_pct']) for r in rd('ccc_tlf_quarterly.csv')}
spread = {r['quarter']: float(r['spread_pp']) for r in rd('totaling_spread_quarterly.csv') if r['months'] == '3'}
cal = {r['variant']: r for r in rd('tlf_calibration.csv')}['all_loss_categories']; a_t, b_t = float(cal['intercept_pp']), float(cal['beta'])
def lagq(q):
    y, n = int(q[:4]), int(q[5]) - 1
    return f"{y-1}Q4" if n == 0 else f"{y}Q{n}"
pairs = [(spread[lagq(q)], tlf[q] - tlf[f"{int(q[:4])-1}{q[4:]}"], q) for q in sorted(tlf) if f"{int(q[:4])-1}{q[4:]}" in tlf and lagq(q) in spread]
oos = (spread['2026Q1'], 0.9, '2026Q2 (mgmt-cited, out of sample)')
panel = rd('units_decomp_panel_v2.csv')
rv = rd('recovery_divergence_quarterly.csv')
ac = rd('age_curves.csv')
# fleet roll paths (same construction as scripts/age_curves.py, k drift 1.194 by 2024, sales held at 2025 after)
S = {int(r['age']): (float(r['survival_cars']), float(r['survival_light_trucks'])) for r in rd('ornl_tedb40_survival_by_age.csv')}
SL = {int(r['year']): (float(r['cars_k']), float(r['light_trucks_k'])) for r in rd('light_vehicle_sales_by_year.csv')}
for y in range(2026, 2031): SL.setdefault(y, SL[2025])
hdr = " ".join(l for l in open(D / 'age_curves.csv') if l.startswith('#'))
lam = float(re.search(r"exp\(-([\d.]+)\*max", hdr).group(1)); pm = re.search(r"P\(a\) = ([\d.]+) \+ \(([\d.]+)-[\d.]+\)/\(1\+exp\(-\(a-([\d.]+)\)/([\d.]+)\)\)", hdr); pmin, pmax, pc, ps = map(float, pm.groups())
Rf = lambda a: (0.5 if a == 0 else 1) * math.exp(-lam * max(a - 6, 0)); Pf = lambda a: pmin + (pmax - pmin) / (1 + math.exp(-(a - pc) / ps))
def Sk(i, a, k):
    x = a / k
    if x >= 31: return 0.0
    j = int(x); f = x - j; return S[j][i] + f * (S[min(j + 1, 31)][i] - S[j][i])
def kmult(t): return 1.0 if t <= 2013 else (1.194 if t >= 2024 else 1 + 0.194 * (t - 2013) / 11)
roll = []
for t in range(2016, 2031):
    kc, kl = 1.064 * kmult(t), 0.921 * kmult(t); tc = tl = cc = cl = 0.0
    for a in range(0, 46):
        my = t - a
        if my not in SL: continue
        c_ = SL[my][0] * Sk(0, a, kc); l_ = SL[my][1] * Sk(1, a, kl)
        cc += c_ * Rf(a); cl += l_ * Rf(a); tc += c_ * Rf(a) * Pf(a); tl += l_ * Rf(a) * Pf(a)
    roll.append(dict(year=t, tlf=(tc + tl) / (cc + cl), lt_share_tl=tl / (tc + tl)))
for i in range(1, len(roll)): roll[i]['drift'] = (roll[i]['tlf'] - roll[i-1]['tlf']) * 100

# ---------------------------------------------------------------- chart 1: spread -> dTLF
xs = [p[0] for p in pairs] + [oos[0]]; ys = [p[1] for p in pairs] + [oos[1]]
c1 = Chart(min(xs) - 2, max(xs) + 2, min(ys) - 0.5, max(ys) + 0.5, 'Totaling spread one quarter earlier: repair CPI minus used-car CPI, YoY (pp)', 'Change in total-loss frequency, YoY (pp)')
c1.parts.append(f'<line x1="{c1.X(c1.xlo):.1f}" y1="{c1.Y(a_t+b_t*c1.xlo):.1f}" x2="{c1.X(c1.xhi):.1f}" y2="{c1.Y(a_t+b_t*c1.xhi):.1f}" class="fit"/>')
for x, y, q in pairs: c1.parts.append(f'<circle cx="{c1.X(x):.1f}" cy="{c1.Y(y):.1f}" r="4.5" class="s1"><title>{q}: spread {x:+.1f}pp → ΔTLF {y:+.1f}pp</title></circle>')
c1.parts.append(f'<circle cx="{c1.X(oos[0]):.1f}" cy="{c1.Y(oos[1]):.1f}" r="6" class="s2 ring"><title>{oos[2]}: spread {oos[0]:+.1f}pp → actual +0.9pp, predicted {a_t+b_t*oos[0]:+.2f}pp</title></circle>')
c1.parts.append(f'<text x="{c1.X(oos[0])-12:.1f}" y="{c1.Y(oos[1])+22:.1f}" class="lbl" text-anchor="end">2Q26 live test: predicted {a_t+b_t*oos[0]:+.2f}, actual +0.90 →</text>')
c1.parts.append(f'<text x="{ML+8}" y="{MT+14}" class="lbl">ΔTLF = {a_t:.3f} + {b_t:.4f} × spread(t−1)   n={len(pairs)}, R² {float(cal["r2"]):.2f}</text>')
svg1 = c1.svg('Spread versus total-loss frequency change') + table([(q, f"{x:+.2f}", f"{y:+.2f}") for x, y, q in pairs] + [('2026Q2 (OOS)', f"{oos[0]:+.2f}", '+0.90')], ['quarter t', 'spread(t−1), pp', 'ΔTLF(t), pp'])

# ---------------------------------------------------------------- chart 2: six-quarter decomposition (stacked bars + actual marker)
rows2 = [(r['cprt_fq'], float(r['claims__ccc_all_coverage']), float(r['tlf_yoy_rel_pct']), float(r['residual__ccc_all_coverage']), float(r['cprt_us_ins_excat'])) for r in panel]
lo = min(min(0, c + min(0, t) + min(0, s)) for _, c, t, s, _ in rows2) - 1; hi = max(max(0, max(0, c) + max(0, t) + max(0, s)) for _, c, t, s, _ in rows2) + 1
c2 = Chart(0, len(rows2), lo, hi, 'Copart fiscal quarter', 'YoY, % or pp'); c2.xs = []
bw = (W - ML - MR) / len(rows2); gap = 2
for i, (fq, cl_, tf, res, act) in enumerate(rows2):
    x0 = ML + i * bw + bw * 0.22; wbar = bw * 0.56; pos = neg = 0.0
    for val, cls, name in ((cl_, 's1', 'industry claims'), (tf, 's3', 'total-loss rate'), (res, 's4', 'residual = Copart share term')):
        if val >= 0: y1, y0 = c2.Y(pos + val), c2.Y(pos); pos += val
        else: y1, y0 = c2.Y(neg), c2.Y(neg + val); neg += val
        c2.parts.append(f'<rect x="{x0:.1f}" y="{y1+gap/2:.1f}" width="{wbar:.1f}" height="{max(0, y0-y1-gap):.1f}" rx="2" class="{cls}"><title>{fq} {name}: {val:+.1f}</title></rect>')
    c2.parts.append(f'<line x1="{x0-4:.1f}" x2="{x0+wbar+4:.1f}" y1="{c2.Y(act):.1f}" y2="{c2.Y(act):.1f}" class="marker"><title>{fq} Copart US insurance units ex-CAT: {act:+.1f}%</title></line>')
    c2.parts.append(f'<text x="{x0+wbar/2:.1f}" y="{c2.h-MB+18}" class="tick" text-anchor="middle">{fq}</text>')
legend2 = '<div class="legend"><span><i class="sw s1"></i>industry claims</span><span><i class="sw s3"></i>total-loss rate</span><span><i class="sw s4"></i>residual = share term</span><span><i class="sw mk"></i>Copart US insurance units, ex-CAT (actual)</span></div>'
svg2 = c2.svg('Units decomposition by quarter') + legend2 + table([(fq, f"{cl_:+.1f}", f"{tf:+.1f}", f"{res:+.1f}", f"{act:+.1f}") for fq, cl_, tf, res, act in rows2], ['quarter', 'claims %', 'TL rate %', 'residual pp', 'Copart actual %'])

# ---------------------------------------------------------------- chart 3: ASP vs used-car CPI
pts3 = [(float(r['used_car_cpi_yoy']), float(r['us_ins_asp_yoy']), r['fiscal_q']) for r in rv]
c3 = Chart(min(p[0] for p in pts3) - 2, max(p[0] for p in pts3) + 2, min(p[1] for p in pts3) - 2, max(p[1] for p in pts3) + 2, 'Used-car CPI, YoY (%)', 'Copart US insurance ASP, YoY (%)')
c3.parts.append(f'<line x1="{c3.X(c3.xlo):.1f}" y1="{c3.Y(3.34+0.602*c3.xlo):.1f}" x2="{c3.X(c3.xhi):.1f}" y2="{c3.Y(3.34+0.602*c3.xhi):.1f}" class="fit"/>')
c3.parts.append(f'<line x1="{c3.X(c3.xlo):.1f}" y1="{c3.Y(c3.xlo):.1f}" x2="{c3.X(c3.xhi):.1f}" y2="{c3.Y(c3.xhi):.1f}" class="ref"/>')
c3.parts.append(f'<text x="{c3.X(c3.xhi)-4:.1f}" y="{c3.Y(c3.xhi)+14:.1f}" class="lbl muted" text-anchor="end">1-for-1 pass-through (what a price-taker would show)</text>')
for x, y, q in pts3: c3.parts.append(f'<circle cx="{c3.X(x):.1f}" cy="{c3.Y(y):.1f}" r="4.5" class="s1"><title>{q}: CPI {x:+.1f}% → ASP {y:+.1f}%</title></circle>')
c3.parts.append(f'<text x="{ML+8}" y="{MT+14}" class="lbl">ASP = 3.3 + 0.60 × CPI   n={len(pts3)}: salvage prices run ~3pp/yr above used-car values</text>')
svg3 = c3.svg('Copart ASP versus used-car CPI') + table([(q, f"{x:+.1f}", f"{y:+.1f}") for x, y, q in pts3], ['fiscal quarter', 'used-car CPI %', 'US insurance ASP %'])

# ---------------------------------------------------------------- chart 4a: light-truck share of the total-loss pool; 4b: demographic drift
c4 = Chart(2016, 2030, 0.45, 0.72, 'Calendar year (sales held at 2025 level after 2025)', 'Light-truck share of modelled total losses', yunit='')
c4.ys = [0.45, 0.50, 0.55, 0.60, 0.65, 0.70]; c4.ylo, c4.yhi = 0.45, 0.72
pts = " ".join(f"{c4.X(r['year']):.1f},{c4.Y(r['lt_share_tl']):.1f}" for r in roll)
c4.parts.append(f'<polyline points="{pts}" class="line s1"/>')
for r in roll: c4.parts.append(f'<circle cx="{c4.X(r["year"]):.1f}" cy="{c4.Y(r["lt_share_tl"]):.1f}" r="3.5" class="s1"><title>{r["year"]}: {r["lt_share_tl"]:.1%}</title></circle>')
c4.parts.append(f'<line x1="{c4.X(2025.5):.1f}" x2="{c4.X(2025.5):.1f}" y1="{MT}" y2="{c4.h-MB}" class="ref"/><text x="{c4.X(2025.5)+6:.1f}" y="{MT+14}" class="lbl muted">projection →</text>')
for r in roll:
    if r['year'] in (2019, 2024, 2027, 2030): c4.parts.append(f'<text x="{c4.X(r["year"]):.1f}" y="{c4.Y(r["lt_share_tl"])-10:.1f}" class="lbl" text-anchor="middle">{r["lt_share_tl"]:.0%}</text>')
c4.parts = [p.replace('>0.4<', '>45%<') for p in c4.parts]
frame_fix = lambda s: re.sub(r'class="tick" text-anchor="end">(0\.\d+)<', lambda m: f'class="tick" text-anchor="end">{float(m.group(1)):.0%}<', s)
svg4a = frame_fix(c4.svg('Light-truck share of the modelled total-loss pool')) + table([(r['year'], f"{r['lt_share_tl']:.1%}") for r in roll], ['year', 'light-truck share of total losses'])
dr = [r for r in roll if 'drift' in r and r['year'] >= 2019]
c5 = Chart(0, len(dr), min(min(r['drift'] for r in dr) - 0.05, -0.05), max(r['drift'] for r in dr) + 0.05, 'Calendar year', 'Demographic change in baseline TLF, pp per year'); c5.xs = []
bw = (W - ML - MR) / len(dr)
for i, r in enumerate(dr):
    x0 = ML + i * bw + bw * 0.25; y1, y0 = (c5.Y(r['drift']), c5.Y(0)) if r['drift'] >= 0 else (c5.Y(0), c5.Y(r['drift']))
    c5.parts.append(f'<rect x="{x0:.1f}" y="{y1:.1f}" width="{bw*0.5:.1f}" height="{max(0.5, y0-y1):.1f}" rx="2" class="{"s1" if r["year"] <= 2025 else "s1 proj"}"><title>{r["year"]}: {r["drift"]:+.3f}pp</title></rect>')
    c5.parts.append(f'<text x="{x0+bw*0.25:.1f}" y="{c5.h-MB+18}" class="tick" text-anchor="middle">{r["year"]}</text>')
    c5.parts.append(f'<text x="{x0+bw*0.25:.1f}" y="{(y1-6) if r["drift"]>=0 else (y0+12):.1f}" class="lbl" text-anchor="middle">{r["drift"]:+.2f}</text>')
svg4b = c5.svg('Demographic contribution to total-loss frequency by year') + table([(r['year'], f"{r['drift']:+.3f}") for r in dr], ['year', 'drift, pp'])

# ---------------------------------------------------------------- chart 6: R and P by age
ages = [r for r in ac if int(r['age']) <= 30]
c6 = Chart(0, 30, 0, 1.1, 'Vehicle age (years)', 'Index (R) or share (P)')
for key, cls, name in (('R', 's1', 'R(age): claims per vehicle, relative'), ('P', 's2', 'P(age): share of claims declared total loss')):
    pts = " ".join(f"{c6.X(int(r['age'])):.1f},{c6.Y(float(r[key])):.1f}" for r in ages)
    c6.parts.append(f'<polyline points="{pts}" class="line {cls}"/>')
    for r in ages:
        c6.parts.append(f'<circle cx="{c6.X(int(r["age"])):.1f}" cy="{c6.Y(float(r[key])):.1f}" r="3" class="{cls}"><title>{name}, age {r["age"]}: {float(r[key]):.3f}</title></circle>')
c6.parts.append(f'<text x="{c6.X(12):.1f}" y="{c6.Y(float([r for r in ages if r["age"]=="12"][0]["R"]))-12:.1f}" class="lbl">R: flat to age 6, then −8.6%/yr (fitted)</text>')
c6.parts.append(f'<text x="{c6.X(14):.1f}" y="{c6.Y(float([r for r in ages if r["age"]=="14"][0]["P"]))+18:.1f}" class="lbl">P: 8% new → 10% ≤3 yrs → 20% at 7 → 43% at 17 (fitted)</text>')
legend6 = '<div class="legend"><span><i class="sw s1"></i>R(age), claims per vehicle relative to ages 1–6</span><span><i class="sw s2"></i>P(age), total-loss share of claims</span></div>'
svg6 = c6.svg('Fitted claim-frequency and total-loss curves by vehicle age') + legend6 + table([(r['age'], r['R'], r['P']) for r in ages], ['age', 'R', 'P'])

# ---------------------------------------------------------------- page
CSS = """
<style>
:root{--bg:#f6f5f1;--surface:#fcfbf8;--ink:#171a1f;--ink2:#4e545e;--ink3:#7a808a;--rule:#d9d6cc;--accent:#1f4f8f;--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--grid:#e7e4db;--fit:#171a1f}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--bg:#14161a;--surface:#1b1e24;--ink:#f1efe9;--ink2:#b9bcc4;--ink3:#868c98;--rule:#2d323b;--accent:#7fb0ef;--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--grid:#262a32;--fit:#f1efe9}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#14161a;--surface:#1b1e24;--ink:#f1efe9;--ink2:#b9bcc4;--ink3:#868c98;--rule:#2d323b;--accent:#7fb0ef;--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--grid:#262a32;--fit:#f1efe9}
body{background:var(--bg);color:var(--ink);font-family:"Source Sans 3","Source Sans Pro",system-ui,sans-serif;font-size:17px;line-height:1.55;padding-inline:20px;padding-block:32px 64px}
.wrap{max-width:820px;margin:0 auto}
h1,h2,h3{font-family:"EB Garamond",Garamond,Georgia,serif;font-weight:500;text-wrap:balance;letter-spacing:-.005em}
h1{font-size:2.4rem;line-height:1.1;margin:0 0 .4rem}h2{font-size:1.65rem;margin:2.6rem 0 .8rem;padding-top:1.2rem;border-top:1px solid var(--rule)}h3{font-size:1.2rem;margin:1.6rem 0 .4rem}
.eyebrow{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3);margin-bottom:.6rem}
.lede{font-size:1.15rem;color:var(--ink2);max-width:66ch}
p{max-width:66ch}li{max-width:66ch;margin-bottom:.5rem}
figure{margin:1.4rem 0 2rem;background:var(--surface);border:1px solid var(--rule);border-radius:6px;padding:14px 14px 10px}
figcaption{font-size:.9rem;color:var(--ink2);margin:.6rem 4px 0;max-width:none}
svg.chart{width:100%;height:auto;display:block;font-family:"Source Sans 3",system-ui,sans-serif}
.grid{stroke:var(--grid);stroke-width:1}.zero{stroke:var(--ink3);stroke-width:1}.tick{fill:var(--ink2);font-size:12px;font-variant-numeric:tabular-nums}.axis{fill:var(--ink2);font-size:12.5px}
.lbl{fill:var(--ink);font-size:12.5px}.muted{fill:var(--ink3)}.fit{stroke:var(--fit);stroke-width:1.6;stroke-dasharray:5 4}.ref{stroke:var(--ink3);stroke-width:1;stroke-dasharray:2 4}
circle.s1{fill:var(--s1)}circle.s2{fill:var(--s2)}rect.s1{fill:var(--s1)}rect.s3{fill:var(--s3)}rect.s4{fill:var(--s4)}rect.proj{opacity:.55}
.line{fill:none;stroke-width:2}.line.s1{stroke:var(--s1)}.line.s2{stroke:var(--s2)}.ring{stroke:var(--surface);stroke-width:2}.marker{stroke:var(--ink);stroke-width:2.5}
.legend{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:.85rem;color:var(--ink2);margin:.5rem 4px 0}.sw{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-2px}.sw.s1{background:var(--s1)}.sw.s2{background:var(--s2)}.sw.s3{background:var(--s3)}.sw.s4{background:var(--s4)}.sw.mk{background:var(--ink);height:3px;vertical-align:3px}
details{margin-top:.5rem;font-size:.85rem}summary{cursor:pointer;color:var(--accent)}.tbl{overflow-x:auto}table{border-collapse:collapse;font-variant-numeric:tabular-nums;margin-top:.4rem}th,td{padding:3px 10px;border-bottom:1px solid var(--rule);text-align:right}th:first-child,td:first-child{text-align:left}
.chain{display:grid;gap:10px;margin:1rem 0 1.6rem}.step{display:grid;grid-template-columns:2.2rem 1fr;gap:10px;align-items:start}.step b{font-family:"EB Garamond",Garamond,serif;font-size:1.3rem;color:var(--accent);line-height:1.2}
.tag{display:inline-block;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;padding:1px 7px;border-radius:3px;border:1px solid var(--rule);color:var(--ink2);margin-left:6px;vertical-align:2px}
.theses li{margin-bottom:1rem}.theses b{color:var(--ink)}
.status{width:100%;max-width:none}.status td:first-child{text-align:left}
code{font-family:ui-monospace,Menlo,monospace;font-size:.86em;background:var(--surface);border:1px solid var(--rule);border-radius:3px;padding:0 4px}
footer{margin-top:3rem;font-size:.85rem;color:var(--ink3)}
@media (max-width:480px){body{font-size:16px}h1{font-size:1.9rem}}
</style>"""
page = f"""<title>Copart Model Map</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500&family=Source+Sans+3:wght@400;600&display=swap">
{CSS}
<div class="wrap">
<div class="eyebrow">Copart, Inc. · NASDAQ: CPRT · research build, September 2026</div>
<h1>How the units model was reached, and what it says</h1>
<p class="lede">Copart never discloses how many cars it sells. Everything below is the chain of reasoning that got from that gap to a testable model of supply, the evidence behind each link, and the handful of claims the build can actually support.</p>

<h2>1. Why an identity and not a regression</h2>
<p>The first instinct was to regress Copart's unit growth on things that move with it. That fails for two reasons that shaped everything after. Copart reports only six to eight comparable quarters of unit growth, which is not enough to fit anything. And a regression on Copart's own history says nothing about <em>why</em> units move, so a judge can accept every number and keep their own view. The build instead writes down what a Copart unit physically is and lets each piece come from its own, larger dataset.</p>
<div class="chain">
<div class="step"><b>1</b><div>A Copart insurance unit is an insured car that crashed, was declared a total loss, and was assigned to Copart rather than IAA. So, as growth rates: <code>(1 + Δunits) = (1 + Δclaims) × (1 + Δtotal-loss rate) × (1 + Δshare)</code>. Nothing is estimated here. It is bookkeeping.<span class="tag">identity</span></div></div>
<div class="step"><b>2</b><div>Industry claim counts come from CCC and the ISS Fast Track headlines. They are exogenous to Copart and published quarterly. This is the first term.<span class="tag">measured</span></div></div>
<div class="step"><b>3</b><div>The total-loss rate is the share of claims an insurer writes off instead of repairing. An adjuster totals a car when repair cost outruns its value, so the driver should be repair-cost inflation relative to used-car values. CCC publishes the rate quarterly for the whole industry, 27 usable quarters, so the sensitivity can be calibrated on industry data rather than Copart's six quarters. That is the one regression in the units model, and its slope has a mechanism behind it before it was fitted.<span class="tag">calibrated</span></div></div>
<div class="step"><b>4</b><div>Share is whatever is left once claims and the total-loss rate are removed from Copart's growth. Solving for it rather than assuming it is what surfaced the Progressive account, and management's own sentence confirmed the size.<span class="tag">residual</span></div></div>
<div class="step"><b>5</b><div>The total-loss regression leaves about 0.6 points a year of drift that the price spread does not explain. The obvious candidate was an ageing fleet, so a cohort model was built from EPA survival schedules and CCC's claim-mix statistics to size it. It explains a quarter of the drift and, importantly, almost none of it going forward.<span class="tag">fitted, tested</span></div></div>
<div class="step"><b>6</b><div>Revenue per unit got the same treatment on the price side: Copart's realised price against used-car values, then fees against price. Both fitted numbers now have named drivers under investigation rather than being constants.<span class="tag">in progress</span></div></div>
</div>
<pre class="mermaid">
flowchart LR
  A[Industry claims<br/>CCC, Fast Track] --> U
  B[Total-loss rate<br/>= 0.60 + 0.08 × spread] --> U
  C[Share residual<br/>Progressive, mix] --> U
  D[Repair CPI − used-car CPI<br/>BLS] --> B
  E[Fleet ageing<br/>EPA survival × CCC mix] -. +0.16pp/yr past, ~0 forward .-> B
  U[US insurance units] --> R[Revenue = units × RPU]
  F[Used-car CPI] --> G[ASP = 3.3 + 0.60 × CPI]
  G --> H[Service RPU = 4.1 + 0.51 × ASP]
  H --> R
</pre>

<h2>2. The evidence behind each link</h2>
<h3>The total-loss rate follows the repair-versus-value spread</h3>
<figure>{svg1}<figcaption>Each point is one CCC quarter, 2019Q1 to 2025Q3. The orange point is a management-cited CCC figure that appeared after the fit and is not in any public edition: the model said +1.28, the actual was +0.90. The intercept, about 0.6 points a year, is the part the spread does not explain.</figcaption></figure>
<h3>The FY26 unit decline was one account, not share erosion</h3>
<figure>{svg2}<figcaption>Copart's US insurance units decomposed into the industry claims term, the total-loss-rate term and the residual, six quarters. The residual sits near zero through 2025 and steps down in FY26 by roughly the size of the Progressive account management described. Claims and total-loss terms are CCC data; the residual is solved, not assumed.</figcaption></figure>
<h3>Copart's realised price is not a used-car price pass-through</h3>
<figure>{svg3}<figcaption>Seventeen fiscal quarters of Copart's US insurance selling price against used-car CPI. The slope is 0.6, not 1, and the intercept is about 3 points a year. Two drivers of that intercept are now identified: each year the typical totaled car is one model year newer, and light trucks are taking over the pool.</figcaption></figure>
<h3>The fleet roll: trucks are taking over the total-loss pool</h3>
<figure>{svg4a}<figcaption>Light-truck share of the modelled total-loss pool, from new-vehicle sales by model year, the EPA survival schedules for cars and light trucks, and the fitted age curves. Trucks were half of new sales for the 2010 to 2013 model years and 83% in 2025; those cohorts only now reach the ages at which cars get totaled.</figcaption></figure>
<figure>{svg4b}<figcaption>What fleet ageing alone does to total-loss frequency each year, with R and P frozen and only the fleet changing. It averaged +0.16 points a year over 2019 to 2025 and is roughly zero from 2026, so it is not a near-term catalyst. Bars after 2025 assume sales held at the 2025 level.</figcaption></figure>
<h3>The two curves that turn a fleet into total losses are fitted, not measured</h3>
<figure>{svg6}<figcaption>R is claims per vehicle by age, relative to ages 1 to 6; P is the share of those claims declared a total loss. Neither exists as public data by single year of age. Five parameters were chosen so the model reproduces eight CCC statistics about its 2024 claims, then frozen and checked against 2019, 2020 and 2025. Bucket values are stable under every survival assumption tried; the single-year shape between anchors is the functional form.</figcaption></figure>

<h2>3. What the build supports, stated as theses</h2>
<p>Each of these comes from a mechanism in the model, not from the model being finer-grained than someone else's. Each names the disagreement with the usual view and the observable that would settle it.</p>
<ol class="theses">
<li><b>Total-loss frequency is a price ratio, and the ratio just re-widened.</b> The spread between repair inflation and used-car values collapsed from +15.7 to +2.3 points through 2025, which is what starved Copart of supply, and has recovered to +8.3. On the calibrated slope that adds roughly half a point a year to the total-loss rate versus a year ago, with a one-quarter lag. The usual view treats total-loss frequency as a structural uptrend; the data say it is cyclical, and 2025's headline rise was mostly small claims disappearing from the denominator as deductibles rose.</li>
<li><b>Copart's price line has demographic drivers that a pass-through model cannot see.</b> The typical totaled car gets one model year newer every year and the pool is shifting to trucks at about 1.7 points a year through 2030. Both push realised prices above used-car values without any change in demand. Combined with fees that move about half with price plus a 4-point fee-and-mix intercept, revenue per unit has a floor near 4.5 to 5.5% against a Street assumption closer to 3%.</li>
<li><b>The unit decline is one account, and lapping is arithmetic.</b> Ex-Progressive, Copart's units ran at or above the industry total-loss pool in every window tested. The account left between April and July 2026, so it laps in FY27Q4. FY27 units should track consensus; the variant view is that FY28 grows 5 to 7% with no share recovery required.</li>
<li><b>Operating leverage is asymmetric and visible in physical units.</b> Cars per weekly sale event fell from about 700 to 490 while sale events rose, and US facility cost per unit rose 6.6% in a year when international's rose 1.2% because its units grew. The sale-event capacity is already in place, so unit recovery from theses 1 and 3 drops through at a high incremental margin. The bear case is the same mechanism run the other way and already fired in Q4.</li>
<li><b>The "ageing fleet" bull case is right about the past and wrong about the next two years, and the build can show it.</b> Demographics added about 0.16 points a year to the total-loss rate over 2019 to 2025 and add roughly nothing in 2026 and 2027. Every deck that leans on an older fleet is describing a tailwind that has already been spent. For the next twelve months the supply story is thesis 1 alone.</li>
</ol>
<p>Supporting exhibit rather than thesis: Copart holds about 57% of the duopoly's listed US inventory on nights when both sitemaps are complete, measured daily. The stated kill condition is a share below 55% by mid-October.</p>

<h2>4. What is measured, fitted and assumed</h2>
<table class="status"><thead><tr><th>Number</th><th>Status</th><th>Where it comes from</th></tr></thead><tbody>
<tr><td>Industry claims, total-loss frequency, CPI series</td><td>measured</td><td>CCC report pages, BLS flat files</td></tr>
<tr><td>Copart unit, inventory and price growth</td><td>hand-transcribed</td><td>earnings calls; 15 of 15 cells match a sell-side exhibit</td></tr>
<tr><td>ΔTLF slope 0.08 and intercept 0.6</td><td>fitted on 27 industry quarters</td><td>one live out-of-sample hit; intercept unexplained</td></tr>
<tr><td>ASP slope 0.60, intercept 3.3; RPU slope 0.51, intercept 4.1</td><td>fitted on 17 quarters, effective n about 6</td><td>drivers of the intercepts under investigation</td></tr>
<tr><td>Survival by age</td><td>measured shape, calibrated scale</td><td>EPA schedule; stretch fitted to the 2013 census and 2024 counts</td></tr>
<tr><td>R(age), P(age)</td><td>fitted</td><td>eight CCC 2024 statistics; tested on 2019, 2020, 2025</td></tr>
<tr><td>289M vehicles in operation anchor</td><td>unverified</td><td>recalled; Experian's 292M on disk gives the same result</td></tr>
</tbody></table>
<footer>Built from the committed data in <code>data/csv/</code> by <code>scripts/build_walkthrough_page.py</code>. Method notes: <code>HANDOFF.md</code>, <code>docs/AGE_CURVES.md</code>, <code>findings.md</code> Addenda 14–20.</footer>
</div>"""
out = ROOT / 'docs/walkthrough.html'; out.write_text(page, encoding='utf-8'); print(f"-> {out.relative_to(ROOT)}  {len(page):,} bytes")
