"""Small source-derived calculations; no refitting of the revenue engine.

The historical discount regressions are descriptive diagnostics. The optional
price sensitivities change a hypothetical basket, not a national price estimate.
"""
import copy
import csv
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = 'https://www.mitchell.com/industry-trends-report/itr-2017-q2-apd/offline/download.pdf'
SERIES = {
    'six_parts_asian': [32.7, 32.3, 32.7, 32.2, 29.7, 30.2, 29.9],
    'six_parts_european': [29.5, 28.2, 28.7, 28.7, 25.0, 25.6, 27.7],
    'six_parts_domestic': [30.9, 29.9, 29.7, 27.1, 24.0, 22.9, 23.3],
    'radiators_domestic': [47.1, 43.6, 40.0, 30.2, 25.6, 23.4, 25.8],
    'bumper_covers_domestic': [29.1, 27.8, 27.9, 25.6, 22.3, 20.8, 20.5],
}


def write_csv(name, rows):
    with (HERE / name).open('w') as f:
        w = csv.DictWriter(f, fieldnames=rows[0], lineterminator='\n')
        w.writeheader(); w.writerows(rows)


def line(values):
    n = len(values); xbar = (n-1)/2; ybar = sum(values)/n
    slope = sum((i-xbar)*(y-ybar) for i,y in enumerate(values))/sum((i-xbar)**2 for i in range(n))
    intercept = ybar-slope*xbar
    ss_res = sum((y-intercept-slope*i)**2 for i,y in enumerate(values))
    ss_tot = sum((y-ybar)**2 for y in values)
    return dict(intercept_pp=intercept, slope_pp_per_year=slope, r_squared=1-ss_res/ss_tot)


def main():
    observations = []; fits = {}
    for name, values in SERIES.items():
        for year, value in zip(range(2010,2017),values):
            observations.append(dict(series=name, year=year, discount_pct_of_oe=value,
                status='Observed published aggregate; rounded to 0.1 percentage point',
                page=10 if name in ['radiators_domestic','bumper_covers_domestic'] else 9,
                source_url=SOURCE))
        fit = line(values); train = line(values[:-1]); prediction = train['intercept_pp']+6*train['slope_pp_per_year']
        fit.update(endpoint_slope_pp_per_year=(values[-1]-values[0])/6,
            diagnostic_2016_prediction_pp=prediction, actual_2016_pp=values[-1],
            trend_absolute_error_pp=abs(values[-1]-prediction),
            flat_2015_absolute_error_pp=abs(values[-1]-values[-2]),
            status='Descriptive 2010-2016 fit; retrospective withheld-year diagnostic, not preregistered validation. No extrapolation to 2026.')
        fits[name] = fit
    write_csv('mitchell_discount_history.csv', observations)
    # Actual application in a repair bill: switching spend share × part discount.
    # The 6% exposure is assumed; discounts are historical observations.
    bill_examples = [{'discount_source':name,'assumed_bill_fraction_switching_from_oe':.06,
        'historical_discount':values[-1]/100,
        'implied_bill_saving':.06*values[-1]/100} for name,values in SERIES.items()]
    write_csv('repair_bill_examples.csv', bill_examples)
    # Approximate historical seal-request growth: 2016 is derived from reported difference.
    capa = dict(seals_2017_observed=9912000, seals_2016_derived=9912000-1600000,
        derived_seal_growth=9912000/(9912000-1600000)-1,
        applications_2016_observed=23721,applications_2017_observed=27053,
        derived_application_growth=27053/23721-1,
        status='Certification supply proxies; neither national utilization nor recycled displacement.')
    # Reuse CCC's saved rounded count table. Ratio requires a common appraisal population.
    am24 = [(3.2-.05)/(13.6+.05),(3.2+.05)/(13.6-.05)]
    am25 = [(3.3-.05)/(13.0+.05),(3.3+.05)/(13.0-.05)]
    ccc = dict(am_physical_share_2024_bounds=am24,am_physical_share_2025_bounds=am25,
        am_physical_share_change_pp_bounds=[100*(am25[0]-am24[1]),100*(am25[1]-am24[0])],
        status='Derived rounding bounds, not confidence intervals; common count-table population and nearest-0.1 rounding assumed. No causal recycled displacement inferred.')
    result = dict(as_of='2026-09-29', historical_discount_fits=fits, ccc_count_rounding_bounds=ccc,
        capa_2017=capa, observations=len(observations),
        full_model_price_sensitivities_status='Historical price ratios applied to an unchanged assumed basket; diagnostic only.')
    # New evidence justifies bounded price-ordering sensitivity, not a new calibration.
    sys.path.insert(0,str(ROOT/'model/aftermarket_bridge_2026-09-29'))
    import bridge
    p0=json.loads((ROOT/'model/aftermarket_bridge_2026-09-29/inputs.json').read_text())
    rows=[]
    for name, price in [('original_assumed_50pct_discount',.5),
                        ('historical_asian_2016_ratio_proxy',.701),
                        ('historical_domestic_2016_ratio_proxy',.767)]:
        p=copy.deepcopy(p0);p['source_relative_prices']['aftermarket']=price
        solution=bridge.solve(p,.04,.015)
        quarters=bridge.forecast_result(p,solution)
        summary=bridge.summarize(name,p,solution,quarters)
        summary.update(aftermarket_price_relative_to_oe=price,
            recycled_price_relative_to_oe_assumed=.6,
            marginal_recycled_to_aftermarket_repair_cost_change=price/.6-1,
            status='Hypothetical basket sensitivity; historical ratios are not measured 2026 national prices. Other behavioral inputs assumed.')
        rows.append(summary)
    write_csv('historical_price_proxy_sensitivity.csv', rows)
    assert len(observations)==35 and all(0<r['discount_pct_of_oe']<100 for r in observations)
    assert abs(rows[0]['FY_delta_vs_reference_musd']+90.655866)<1e-4
    assert all(abs(r['FY_delta_vs_reference_pct']-(r['FY_legacy_service_musd']/(r['FY_legacy_service_musd']-r['FY_delta_vs_reference_musd'])-1))<1e-12 for r in rows)
    assert sum(f['trend_absolute_error_pp']>f['flat_2015_absolute_error_pp'] for f in fits.values())==5
    result['checks']={'35_observations':True,'original_case_reproduced':True,
        'revenue_percent_reconciles':True,'flat_beats_trend_in_five_of_five_series':True}
    result['runtime_inputs_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in [ROOT/'model/aftermarket_bridge_2026-09-29/inputs.json',
                  ROOT/'model/aftermarket_bridge_2026-09-29/bridge.py',
                  ROOT/'model/revenue_architecture_2026-09-28/model.py',
                  ROOT/'model/revenue_architecture_2026-09-28/scenario_configs.json',
                  ROOT/'model/linked_service_revenue_2026-09-28/inputs.json',
                  ROOT/'docs/fleet_selection_2026-09-28/age_constrained_engine_results.json']}
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'fits':fits,'price_sensitivities':rows},indent=2))


if __name__=='__main__':main()
