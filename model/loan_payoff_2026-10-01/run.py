"""Offline, hypothetical loan-payoff sensitivity. No coefficients are calibrated."""
from pathlib import Path
import copy, csv, hashlib, json, sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'model/revenue_architecture_2026-09-28'))
import model as m

def save_csv(name, rows):
    with (HERE/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def shifted(year, month, term):
    n=year*12+month-1+term
    return f'{n//12:04d}-{n%12+1:02d}'
def annual(r):return sum(q['legacy_service_musd'] for q in r['quarters'])

def main():
    refpath=ROOT/'model/ccc_age_body_2026-09-29/reference_config.json'
    before=hashlib.sha256(refpath.read_bytes()).hexdigest()
    ref=json.loads(refpath.read_text());base=m.run(ref)
    calendar=[dict(origination_year=y,assumed_term_months=t,earliest_scheduled_maturity=shifted(y,1,t),latest_scheduled_maturity=shifted(y,12,t),status='Calendar arithmetic only; no origination weights or survival estimate') for y in [2020,2021,2022] for t in [60,70,72,84]]
    save_csv('maturity_calendar.csv',calendar)
    # e is exposure to the payoff cohort, weighted by baseline prospective Copart
    # insurance total-loss units, not by all cars, loans or reported claims.
    # d is EXCESS coverage attrition over that already embedded in the reference.
    # r is fraction of otherwise-lost insurance units still arriving by another route.
    # Net l=e*d*(1-r), used as a UNIFORM claims multiplier solely for sensitivity.
    # Engine has no explicit alternate-route revenue: r nets units before the shock;
    # routed-back units are assumed to earn baseline-equivalent revenue.
    specs=[('reference',0,0,0,0),('repairable_nonfiling_only',0,0,0,.10),
           ('coverage_example',.10,.20,.25,0),('coverage_plus_nonfiling',.10,.20,.25,.10),
           ('severe_coverage_example',.20,.40,.25,0)]
    rows=[];configs={};results={}
    for name,e,d,r,f in specs:
        assert all(0<=x<=1 for x in [e,d,r,f])
        loss=e*d*(1-r);c=copy.deepcopy(ref)
        c['name']=name;c['status']='HYPOTHETICAL payoff sensitivity; not admitted forecast'
        c['claims'][4:]=[v*(1-loss) for v in ref['claims'][4:]]
        c['nonfiling'][4:]=[f]*4
        result=m.run(c);configs[name]=c;results[name]=result
        assert result['base_ledger']==base['base_ledger']
        assert result['base_modeled_units']==base['base_modeled_units']
        for q,b in zip(result['quarters'],base['quarters']):
            assert abs(q['modeled_insurance_sales']/b['modeled_insurance_sales']-(1-loss))<1e-10
            expected=b['TLF']/(1-f*(1-b['TLF']))
            assert abs(q['TLF']-expected)<1e-10
        rows.append(dict(scenario=name,exposed_unit_weight=e,excess_coverage_drop=d,alternate_route_recapture=r,repairable_nonfiling=f,net_unit_loss=loss,legacy_service_musd=annual(result),delta_vs_reference_musd=annual(result)-annual(base),q1_reported_tlf=result['quarters'][0]['TLF'],status='HYPOTHETICAL; flat effect all four FY27 quarters, no maturity timing inferred'))
    assert abs(annual(results['reference'])-annual(results['repairable_nonfiling_only']))<1e-8
    assert abs(annual(results['coverage_example'])-annual(results['coverage_plus_nonfiling']))<1e-8
    # Compare to prior reverse stress only as an operating magnitude hurdle.
    # Different mechanisms, and its 0/half/full/full ramp is NOT inferred here.
    with (ROOT/'model/reverse_short_2026-09-30/hurdles.csv').open() as f:
        target=next(x for x in csv.DictReader(f) if float(x['target_miss_pct'])==3)
    loss=float(target['terminal_unit_shortfall_pct'])/100
    hurdle=[dict(exposed_unit_weight=e,alternate_route_recapture=r,required_excess_coverage_drop=loss/(e*(1-r)),feasible_probability=loss/(e*(1-r))<=1,terminal_unit_loss_target=loss,status='Reverse-solved hurdle only; NOT evidence or annual timing forecast') for e in [.05,.10,.20] for r in [0,.25]]
    save_csv('scenarios.csv',rows);save_csv('hurdles.csv',hurdle)
    (HERE/'scenario_configs.json').write_text(json.dumps(configs,indent=2)+'\n')
    rate=.06/12;n=72;principal=40000;payment=principal*rate/(1-(1+rate)**(-n));balance=principal
    for _ in range(n):balance=balance*(1+rate)-payment
    assert abs(balance)<1e-7
    assert before==hashlib.sha256(refpath.read_bytes()).hexdigest()
    checks=dict(status='PASS',reference_sha256=before,reference_service_musd=annual(base),history_unchanged=True,uniform_unit_multiplier_checked=True,nonfiling_identity_checked=True,nonfiling_revenue_invariant=True,forecast_admission=False,catalyst_verified=False,amortization_example=dict(status='ILLUSTRATIVE fixed-rate fully amortizing loan; no fees/arrears/balloon',principal=principal,apr=.06,term_months=n,monthly_payment=payment,first_month_interest=principal*rate,first_month_principal=payment-principal*rate,ending_balance=balance))
    (HERE/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps({'checks':checks,'scenarios':rows,'hurdles':hurdle},indent=2))
if __name__=='__main__':main()
