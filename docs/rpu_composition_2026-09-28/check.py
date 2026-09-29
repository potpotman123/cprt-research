"""Small, source-traceable named-broker RPU hurdle; no predictive fitting."""
from pathlib import Path
import csv, hashlib, json, re

OUT = Path(__file__).resolve().parent
SOURCES = Path('/Users/kwu/Documents/ChatGPT/HFAC x Citadel/research/cprt_discovery_plan_2026-09-26/sources')
source = next(SOURCES.glob('2026-08-20*123970131.txt'))
lines = source.read_text().splitlines()

def row(prefix, currency=False):
    matches = [(i+1, s) for i, s in enumerate(lines) if i >= 550 and s.startswith(prefix)]
    assert len(matches) == 1, matches
    line, text = matches[0]
    values = re.findall(r'\$([\d,]+\.\d+)' if currency else r'(\(?-?\d+\.\d+\)?%)', text)
    values = [float(v.replace(',', '').replace('%', '').replace('(', '-').replace(')', '')) for v in values]
    return line, values

us_line, us = row('U.S. service revenue ', True)
rpu_line, rpu = row('Implied U.S. rev per unit % change ')
unit_line, units = row('U.S. fee unit growth ')
total_line, totals = row('Total revenue ', True)
assert len(us) == len(totals) == 20
assert len(rpu) == len(units) == 16
base, published, total = us[10:14], us[15:19], totals[15:19]
assert rpu[-4:] == [2., 2., 2., 2.]
assert units[-4:] == [-1., 2., 2., 2.]
# Verify table column assignment and rounded multiplicative identity to <0.05pp.
identity_error_pp = [(published[i]/base[i]/(1+units[-4+i]/100)-1)*100-2 for i in range(4)]
assert max(map(abs, identity_error_pp)) < .05
records = []
for assumed_rpu in [-.02, 0, .01, .02, .03]:
    revised = [v*(1+assumed_rpu)/1.02 for v in published]
    delta = [v-b for v,b in zip(revised,published)]
    records.append(dict(rpu_growth=assumed_rpu, h1_us_service_musd=sum(revised[:2]),
        h1_delta_musd=sum(delta[:2]), h1_total_delta_pct=100*sum(delta[:2])/sum(total[:2]),
        fy_delta_musd=sum(delta), fy_total_delta_pct=100*sum(delta)/totals[-1]))
assert abs(records[3]['h1_delta_musd']) < 1e-9
assert abs(records[0]['h1_delta_musd']-2*records[1]['h1_delta_musd']) < 1e-9
with (OUT/'rpu_hurdles.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=records[0],lineterminator='\n'); writer.writeheader(); writer.writerows(records)
hurdles = {str(miss): .02-miss*sum(total[:2])*1.02/sum(published[:2]) for miss in [.02,.03,.05]}
result = dict(source=str(source), sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    source_date='2026-08-20', table='Supplemental Financial Data, printed page 10; Income Statement, printed page 9',
    locators=dict(us_service=us_line, rpu=rpu_line, fee_units=unit_line, total_revenue=total_line),
    quarterly_us_service_musd=published, quarterly_fee_unit_growth_pct=units[-4:],
    quarterly_rpu_growth_pct=rpu[-4:], h1_total_musd=sum(total[:2]), fy_total_musd=totals[-1],
    rounded_identity_error_pp=identity_error_pp,
    required_rpu_growth_for_h1_total_miss=hurdles,
    caveat='Named pre-results broker, not current consensus. Hold units, all other revenues and accounting fixed. No ACV added. RPU changes are scenarios, not measured service deterioration.',
    checks='Column counts, forecast rates, quarterly revenue identity within rounding, zero shock, linear scaling passed.')
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(scenarios=records,required_rpu_growth=hurdles),indent=2))
