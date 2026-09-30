"""Source substitution -> donor economics -> inherited selection/fees.

All new behavioral parameters are assumptions. The equilibrium below is a
transparent reduced-form scenario closure, not an estimated auction model.
"""
import copy
import csv
import functools
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ARCH = ROOT / 'model/revenue_architecture_2026-09-28'
sys.path.insert(0, str(ARCH))
import model as m


def jpm_service():
    return float(json.loads((ARCH/'evidence_manifest.json').read_text())['jpm_fy27_service_musd'])


def reference(anchor_path=None):
    c = json.loads((ARCH/'scenario_configs.json').read_text())
    # Saved scenarios are a mapping; do not independently rebuild the reference.
    out = copy.deepcopy(c['price_3p7_intl_continuation'])
    if anchor_path: out['cohort_anchor_path'] = anchor_path
    return out


def basket(p, oem_shift, recycled_shift):
    q = p['source_quantity_shares']; v = p['source_relative_prices']
    if any(not math.isfinite(x) or x < 0 for x in [oem_shift, recycled_shift]):
        raise ValueError('Source transfers must be finite and nonnegative')
    if abs(sum(q.values())-1) > 1e-10 or min(q.values()) < 0 or q['recycled'] <= 0:
        raise ValueError('Invalid initial physical source shares')
    if oem_shift > q['oem'] or recycled_shift > q['recycled']:
        raise ValueError('Transfer exceeds available source quantity')
    for key in ['eligible_parts_bill_share', 'donor_contribution_exposed_fraction',
                'recycler_price_transmission_weight', 'repair_job_recapture',
                'expected_salvage_pass_through', 'threshold_responsive_fraction']:
        if not 0 <= p[key] <= 1: raise ValueError('Invalid fraction: '+key)
    for key in ['donor_contribution_to_hammer_bid', 'rebuilder_repair_bill_to_hammer_bid', 'supply_price_response']:
        if not math.isfinite(p[key]) or p[key] < 0: raise ValueError('Invalid response: '+key)
    if any(not math.isfinite(x) or x <= 0 for x in v.values()): raise ValueError('Invalid prices')
    after = dict(oem=q['oem']-oem_shift, aftermarket=q['aftermarket']+oem_shift+recycled_shift,
                 recycled=q['recycled']-recycled_shift)
    before_cost = sum(q[k]*v[k] for k in q)
    after_cost = sum(after[k]*v[k] for k in q)
    change = p['eligible_parts_bill_share']*(after_cost/before_cost-1)
    return dict(repair_change=change, recycled_retention=after['recycled']/q['recycled'],
                after_quantity_shares=after)


@functools.lru_cache(maxsize=128)
def engine_run(repair, expected, realized, nodes=1024, insurance_fraction=.9, anchor_path=None):
    c = reference(anchor_path)
    for key, factor in [('repair',repair),('expected_salvage',expected),('realized_salvage',realized)]:
        c[key]=[v if i<4 else v*factor for i,v in enumerate(c[key])]
    c.update(nodes=nodes,insurance_service_fraction=insurance_fraction)
    return m.run(c)


def population_state(repair, expected, response, anchor_path=None):
    # Assignments/TLF do not depend on price-integration nodes; solve cheaply.
    ref = engine_run(1., 1., 1., 1, anchor_path=anchor_path)
    changed = engine_run(repair, expected, 1., 1, anchor_path=anchor_path)
    out = []
    for a, b in zip(ref['operating'][4:], changed['operating'][4:]):
        totals = a['totals']+response*(b['totals']-a['totals'])
        out.append(dict(supply_ratio=totals/a['totals'],
                        repair_jobs_ratio=(a['claims']-totals)/(a['claims']-a['totals'])))
    return out


def solve(p, oem_shift, recycled_shift):
    b = basket(p, oem_shift, recycled_shift)
    repair = 1+b['repair_change']; w = p['recycler_price_transmission_weight']
    def evaluate(x):
        states = population_state(repair, 1+p['expected_salvage_pass_through']*x,
                                  p['threshold_responsive_fraction'], p.get('cohort_anchor_path'))
        rows = []
        for s in states:
            jobs = 1+p['repair_job_recapture']*(s['repair_jobs_ratio']-1)
            recycler = p['donor_contribution_exposed_fraction']*p['donor_contribution_to_hammer_bid']*(b['recycled_retention']*jobs-1)
            rebuilder = -b['repair_change']*p['rebuilder_repair_bill_to_hammer_bid']
            scarcity = -p['supply_price_response']*math.log(s['supply_ratio'])
            rows.append(dict(**s, recycled_demand_ratio=b['recycled_retention']*jobs,
                             recycler_bid_change=recycler, rebuilder_bid_change=rebuilder,
                             scarcity_price_support=scarcity,
                             implied_price_change=w*recycler+(1-w)*rebuilder+scarcity))
        # Equal-quarter average is explicit: no measured seasonal exposure weights.
        return sum(r['implied_price_change'] for r in rows)/4-x, rows
    lo, hi = -.8, .8
    flo, _ = evaluate(lo); fhi, _ = evaluate(hi)
    if flo*fhi > 0: raise ValueError('No bounded equilibrium in +/-80% price interval')
    for _ in range(32):
        mid = (lo+hi)/2; fm, _ = evaluate(mid)
        if fm*flo > 0: lo, flo = mid, fm
        else: hi = mid
    x = (lo+hi)/2; residual, rows = evaluate(x)
    if abs(residual) > 1e-8: raise AssertionError('Price closure did not converge')
    return dict(**b, price_change=x, expected_salvage_change=p['expected_salvage_pass_through']*x,
                equilibrium_residual=residual, feedback=rows)


def forecast_result(p, solution, insurance_fraction=.9):
    repair = 1+solution['repair_change']; price = 1+solution['price_change']
    expected = 1+solution['expected_salvage_change']; f = p['threshold_responsive_fraction']
    anchor = p.get('cohort_anchor_path')
    changed = engine_run(repair, expected, price, insurance_fraction=insurance_fraction, anchor_path=anchor)
    locked = engine_run(1., 1., price, insurance_fraction=insurance_fraction, anchor_path=anchor)
    ref = engine_run(1., 1., 1., insurance_fraction=insurance_fraction, anchor_path=anchor)
    if changed['base_ledger'] != ref['base_ledger'] or locked['base_ledger'] != ref['base_ledger']:
        raise AssertionError('Forward shock changed historical ledger')
    rows = []
    for i, (a, z, r) in enumerate(zip(changed['quarters'], locked['quarters'], ref['quarters'])):
        # A mixture of disjoint identical claim populations, not an arbitrary fee blend.
        mix = lambda key: f*a[key]+(1-f)*z[key]
        u = mix('modeled_insurance_sales'); u0 = r['modeled_insurance_sales']
        insurance = sum(mix(k) for k in ['insurance_core_musd','title_musd','delivery_musd'])
        insurance0 = sum(r[k] for k in ['insurance_core_musd','title_musd','delivery_musd'])
        rpu = insurance*1e6/u; rpu0 = insurance0*1e6/u0
        service = mix('legacy_service_musd')
        asp = (f*a['modeled_insurance_sales']*a['insurance_ASP']+(1-f)*z['modeled_insurance_sales']*z['insurance_ASP'])/u
        u_effect = (u-u0)*rpu0/1e6; r_effect = u0*(rpu-rpu0)/1e6
        interaction = (u-u0)*(rpu-rpu0)/1e6
        if abs(service-r['legacy_service_musd']-u_effect-r_effect-interaction)>1e-7:
            raise AssertionError('Unit/fee bridge does not reconcile')
        prior_units = ref['base_modeled_units'][i]
        prior_insurance = sum(ref['base_ledger'][i][k] for k in ['insurance_core','title','delivery'])
        rows.append(dict(period=a['period'],legacy_service_musd=service,
            legacy_total_musd=mix('legacy_total_musd'), insurance_units=u,
            insurance_unit_delta_vs_reference=u/u0-1, insurance_units_yoy=u/prior_units-1,
            insurance_allin_RPU=rpu, insurance_RPU_delta_vs_reference=rpu/rpu0-1,
            insurance_RPU_yoy=rpu/(prior_insurance*1e6/prior_units)-1,
            selected_ASP_delta_vs_reference=asp/r['insurance_ASP']-1,
            delta_service_vs_reference_musd=service-r['legacy_service_musd'],
            units_contribution_musd=u_effect, RPU_contribution_musd=r_effect,
            product_interaction_musd=interaction,
            title_musd=mix('title_musd'), delivery_musd=mix('delivery_musd'),
            insurance_core_musd=mix('insurance_core_musd'),
            other_us_musd=mix('other_us_musd'), intl_service_musd=mix('intl_service_musd')))
    return rows


def summarize(name, p, solution, rows):
    ref = engine_run(1.,1.,1.,anchor_path=p.get('cohort_anchor_path'))['quarters']; fy = sum(q['legacy_service_musd'] for q in rows)
    fy0 = sum(q['legacy_service_musd'] for q in ref)
    units = sum(q['insurance_units'] for q in rows); u0 = sum(q['modeled_insurance_sales'] for q in ref)
    ir = lambda qs: sum(sum(q[k] for k in ['insurance_core_musd','title_musd','delivery_musd']) for q in qs)
    return dict(scenario=name, repair_change=solution['repair_change'],
        auction_price_change_at_fixed_selection=solution['price_change'],
        expected_salvage_change=solution['expected_salvage_change'],
        FY_insurance_unit_delta=units/u0-1,
        FY_insurance_allin_RPU_delta=(ir(rows)/units)/(ir(ref)/u0)-1,
        FY_legacy_service_musd=fy, FY_delta_vs_reference_musd=fy-fy0,
        FY_delta_vs_reference_pct=fy/fy0-1, FY_gap_to_dated_JPM_service_musd=fy-jpm_service(),
        FY_gap_to_dated_JPM_service_pct=fy/jpm_service()-1,
        H1_delta_vs_reference_musd=sum(q['delta_service_vs_reference_musd'] for q in rows[:2]),
        threshold_responsive_fraction=p['threshold_responsive_fraction'],
        status='Conditional scenario; not an empirically identified forecast')


def write_csv(name, rows):
    with (HERE/name).open('w') as f:
        w = csv.DictWriter(f, fieldnames=rows[0], lineterminator='\n'); w.writeheader(); w.writerows(rows)


def main():
    p = json.loads((HERE/'inputs.json').read_text())
    results = {}; summaries = []; quarters = []; solutions = {}
    cases = [(x['name'],p,x['oem_to_aftermarket'],x['recycled_to_aftermarket']) for x in p['cases']]
    variants = [
        ('larger_shift_half_switching',{'threshold_responsive_fraction':.5}),
        ('larger_shift_no_switching',{'threshold_responsive_fraction':0.}),
        ('larger_shift_no_scarcity',{'supply_price_response':0.}),
        ('larger_shift_stronger_scarcity',{'supply_price_response':.5}),
        ('larger_shift_weak_recycler_transmission',{'recycler_price_transmission_weight':.1}),
        ('larger_shift_no_expected_update',{'expected_salvage_pass_through':0.}),
        ('larger_shift_no_repair_recapture',{'repair_job_recapture':0.})]
    cases += [(name,dict(p,**changes),.04,.015) for name,changes in variants]
    cases += [('oem_substitution_only',p,.04,0.)]
    for name, params, o, recycled in cases:
        s = solve(params,o,recycled); rows = forecast_result(params,s)
        solutions[name] = dict(oem_to_aftermarket=o,recycled_to_aftermarket=recycled,parameters=params,solution=s)
        results[name]=rows; summaries.append(summarize(name,params,s,rows))
        quarters.extend(dict(scenario=name,**q) for q in rows)
        print(name, round(summaries[-1]['FY_delta_vs_reference_musd'],2), flush=True)
    write_csv('scenario_summary.csv',summaries); write_csv('quarterly_results.csv',quarters)
    (HERE/'scenario_details.json').write_text(json.dumps(solutions,indent=2)+'\n')

    # A materiality hurdle is a required assumption, not a coefficient fit to data.
    target = .97*jpm_service(); lo,hi=0.,p['source_quantity_shares']['recycled']
    def fy(recycled):
        s=solve(p,.04,recycled); rows=forecast_result(p,s)
        return sum(q['legacy_service_musd'] for q in rows),s,rows
    if not fy(lo)[0] > target > fy(hi)[0]: raise AssertionError('Materiality target not bracketed')
    for _ in range(11):
        mid=(lo+hi)/2
        if fy(mid)[0]>target:lo=mid
        else:hi=mid
    level,s,rows=fy((lo+hi)/2)
    hurdle=dict(target='3% below dated JPM FY27 ex-ACV service revenue',target_service_musd=target,
        oem_to_aftermarket=.04,recycled_to_aftermarket=(lo+hi)/2,
        recycled_quantity_displacement=((lo+hi)/2)/p['source_quantity_shares']['recycled'],
        source_shift_bracket=[lo,hi],solution=s,summary=summarize('materiality_hurdle',p,s,rows))
    (HERE/'materiality_hurdle.json').write_text(json.dumps(hurdle,indent=2)+'\n')

    # Compact grid separates inherited switching response from parts assumptions.
    grid=[]
    for repair in [0.,-.005,-.01,-.02]:
        for price in [0.,-.01,-.03,-.05]:
            s=dict(repair_change=repair,price_change=price,expected_salvage_change=price)
            rows=forecast_result(p,s)
            grid.append(summarize(f'repair_{repair}_price_{price}',p,s,rows))
    write_csv('direct_shock_grid.csv',grid)

    # Incremental one-quarter delay, leaving current prices in the current quarter.
    # Use modeled same-quarter RPU for delayed quantities; no physical backlog claim.
    delayed=[]; base=engine_run(1.,1.,1.)['quarters']
    qrows=results['larger_shift'];du=[q['insurance_units']-r['modeled_insurance_sales'] for q,r in zip(qrows,base)]
    for same in [1.,.5,0.]:
        shifted=[same*du[i]+(1-same)*(du[i-1] if i else 0.) for i in range(4)]
        terminal=(1-same)*du[-1]
        assert abs(sum(shifted)+terminal-sum(du))<1e-7
        for i,q in enumerate(qrows):
            service=q['legacy_service_musd']+(shifted[i]-du[i])*q['insurance_allin_RPU']/1e6
            delayed.append(dict(same_quarter_fraction=same,period=q['period'],
                delta_service_vs_reference_musd=service-base[i]['legacy_service_musd'],
                deferred_unit_delta_beyond_FY=terminal if i==3 else 0.))
    write_csv('incremental_timing.csv',delayed)
    # The inherited base allocation is not observed; expose its dollar leverage.
    s=solutions['larger_shift']['solution']; alt=forecast_result(p,s,insurance_fraction=.8)
    ar=engine_run(1.,1.,1.,insurance_fraction=.8)['quarters']
    allocation=dict(insurance_fraction=.8,FY_delta_vs_own_reference_musd=sum(q['legacy_service_musd']-r['legacy_service_musd'] for q,r in zip(alt,ar)))
    (HERE/'allocation_sensitivity.json').write_text(json.dumps(allocation,indent=2)+'\n')
    paths=[HERE/'bridge.py',HERE/'inputs.json',ARCH/'model.py',ARCH/'scenario_configs.json',
           ARCH/'manifest.json',ARCH/'evidence_manifest.json',m.LEGACY/'engine.py',
           ROOT/'docs/repair_salvage_execution_2026-09-28/MIX_SEGMENTATION.md',
           m.old.OLD,m.old.ECON,m.old.BIRTHS,m.LEGACY/'assumptions.json']
    manifest=dict(as_of='2026-09-29',status=p['status'],
        source_hashes={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths},
        reference_service_musd=sum(q['legacy_service_musd'] for q in base),
        benchmark='JPM 2026-09-11 $4061m FY27 service, explicitly excluding ACV; latest local JPM source found, not asserted current consensus',
        checks='See checks.json; arithmetic/structural checks do not independently validate causal magnitudes')
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(hurdle['summary'],indent=2))


if __name__=='__main__': main()
