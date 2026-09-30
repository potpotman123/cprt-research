"""Independent basket arithmetic, saved-baseline parity and economic limits."""
import copy
import csv
import json
import math
import bridge as b


def main():
    p=json.loads((b.HERE/'inputs.json').read_text()); checks=[]
    def check(name,truth):
        if not truth: raise AssertionError(name)
        checks.append(name)
    def close(x,y): return math.isclose(x,y,rel_tol=1e-8,abs_tol=1e-7)
    def rejects(name,fn):
        try: fn()
        except ValueError: checks.append(name);return
        raise AssertionError(name)
    # Independent dollar basket: 65 OEM at $100, 25 AM at $50, 10 R at $60.
    # Transfer 4 OEM and 1.5 recycled units to AM: $8,350 -> $8,135.
    s=b.basket(p,.04,.015)
    check('Hand-calculated $8350 -> $8135 basket',close(s['repair_change'],.4*(8135/8350-1)))
    check('Physical quantities conserve to one',close(sum(s['after_quantity_shares'].values()),1.))
    check('1.5 of 10 recycled units displaced, not 1.5% of demand',close(s['recycled_retention'],.85))
    check('No source shift means no repair change',b.basket(p,0.,0.)['repair_change']==0.)
    rejects('Cannot substitute more recycled parts than exist',lambda:b.basket(p,0.,.11))
    rejects('Negative substitution rejected',lambda:b.basket(p,-.01,0.))
    expensive=copy.deepcopy(p);expensive['source_relative_prices']['aftermarket']=.7
    check('Aftermarket dearer than recycled can increase costs',b.basket(expensive,0.,.01)['repair_change']>0.)
    baseline=b.engine_run(1.,1.,1.)
    saved=list(csv.DictReader((b.ARCH/'quarterly_scenarios.csv').open()))
    saved=[x for x in saved if x['scenario']=='price_3p7_intl_continuation']
    check('Four saved reference quarters found',len(saved)==4)
    check('Unchanged engine reproduces saved reference',all(close(q['legacy_service_musd'],float(r['legacy_service_musd'])) for q,r in zip(baseline['quarters'],saved)))
    null=b.solve(p,0.,0.)
    check('No shock yields zero equilibrium price change',abs(null['price_change'])<1e-8)
    details=json.loads((b.HERE/'scenario_details.json').read_text())
    summary={r['scenario']:r for r in csv.DictReader((b.HERE/'scenario_summary.csv').open())}
    rows=list(csv.DictReader((b.HERE/'quarterly_results.csv').open()))
    for name in ['small_shift','larger_shift','large_stress']:
        sol=details[name]['solution']
        check(name+' price closure',abs(sol['equilibrium_residual'])<1e-8)
        check(name+' converted totals increase repaired claims',all(x['repair_jobs_ratio']>1 for x in sol['feedback']))
        check(name+' lower donor supply supports prices',all(x['scarcity_price_support']>0 for x in sol['feedback']))
    check('No switching preserves assignment volume',abs(float(summary['larger_shift_no_switching']['FY_insurance_unit_delta']))<1e-9)
    check('Stronger scarcity attenuates downside',float(summary['larger_shift_stronger_scarcity']['FY_delta_vs_reference_musd'])>float(summary['larger_shift_no_scarcity']['FY_delta_vs_reference_musd']))
    check('Repair demand recapture attenuates downside',float(summary['larger_shift']['FY_delta_vs_reference_musd'])>float(summary['larger_shift_no_repair_recapture']['FY_delta_vs_reference_musd']))
    check('OEM-only substitution supports auction bids in this case',float(summary['oem_substitution_only']['auction_price_change_at_fixed_selection'])>0)
    check('Weaker recycler influence can give positive RPU',float(summary['larger_shift_weak_recycler_transmission']['FY_insurance_allin_RPU_delta'])>0)
    for r in rows:
        total=sum(float(r[k]) for k in ['insurance_core_musd','title_musd','delivery_musd','other_us_musd','intl_service_musd'])
        if not close(total,float(r['legacy_service_musd'])): raise AssertionError('Ledger mismatch')
        attrib=sum(float(r[k]) for k in ['units_contribution_musd','RPU_contribution_musd','product_interaction_musd'])
        if not close(attrib,float(r['delta_service_vs_reference_musd'])): raise AssertionError('Attribution mismatch')
    check('All scenario component ledgers and unit/RPU/product bridges reconcile',True)
    hurdle=json.loads((b.HERE/'materiality_hurdle.json').read_text())
    check('Materiality hurdle reaches target to $0.2m',abs(hurdle['summary']['FY_legacy_service_musd']-hurdle['target_service_musd'])<.2)
    check('Hurdle transfer is feasible within assumed basket',0<hurdle['recycled_to_aftermarket']<p['source_quantity_shares']['recycled'])
    # Rounded source data bound; deliberately never enters causal model inputs.
    check('Share loss is offset by 1.90476% parts-spending growth',close((1+.019047619047619)*.105/.107,1.))
    out=dict(passed=len(checks),checks=checks,status='Arithmetic/structural checks only; no empirical validation of response coefficients')
    (b.HERE/'checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
