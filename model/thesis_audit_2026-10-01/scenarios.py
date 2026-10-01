"""Quarterly, common-reference thesis scenarios. No empirical fitting.

The aftermarket closure measures only incremental sourcing effects conditional
on the other drivers. It does not estimate macro supply/price feedback.
"""
import copy
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'model/revenue_architecture_2026-09-28'))
sys.path.insert(0, str(ROOT/'model/aftermarket_bridge_2026-09-29'))
import model as m
import bridge as am


def load():
    reference = json.loads((ROOT/'model/ccc_age_body_2026-09-29/reference_config.json').read_text())
    parameters = json.loads((ROOT/'model/ccc_age_body_2026-09-29/aftermarket_inputs.json').read_text())
    premiums = json.loads((ROOT/'model/premium_scenarios_2026-10-01/assumptions.json').read_text())
    return reference, parameters, premiums


def configure(factors, assumptions):
    c, _, premiums = load()
    d, _, _ = m.old.load()
    if not factors['fleet_mix']:
        c['fleet_period_weights'] = [x['weights'] for x in d['periods'][:4]] * 2
    if factors['market_allocation']:
        c['carrier_mode'] = 'inherited_runoff'
    # The comparison is recovery versus no additional relief, not a repeat of
    # the historical premium increase as a new forecast shock.
    a = copy.deepcopy(premiums['same_as_reference'])
    a['premium'] = assumptions['no_relief_premium_index'] if factors['premium_recovery'] else assumptions['recovery_premium_index']
    c['premium_assumptions'] = a
    c['name'] = '+'.join(k for k, v in factors.items() if v) or 'recovery_comparator'
    c['status'] = 'Illustrative comparison; behavioral magnitudes and recovery path are assumed'
    return c


def apply_changes(c, repairs, prices, p, selection=True, nodes=None):
    changed = copy.deepcopy(c)
    if nodes is not None:
        changed['nodes'] = nodes
    for q in range(4):
        if selection:
            changed['repair'][q+4] *= repairs[q]
            changed['expected_salvage'][q+4] *= 1+p['expected_salvage_pass_through']*prices[q]
        changed['realized_salvage'][q+4] *= 1+prices[q]
    return changed


def run_aftermarket(c, p, oem, recycled):
    """Solve four separate quarterly sourcing equilibria, then price the same pool.

    Locked/responsive claims are disjoint, identical starting populations. The
    response fraction attenuates disposition changes, not the realized-price
    shock. Default sale-equivalent timing is required for this cohort mixture.
    """
    if len(oem) != 4 or len(recycled) != 4:
        raise ValueError('Four quarterly cumulative source-share transfers required')
    if c['sales_timing']['mode'] != 'sale_equivalent':
        raise ValueError('Combined bridge requires sale-equivalent timing')
    if c.get('premium_assumptions') is not None:
        from premium_channels import compile_channels
        c, premium_diagnostics = compile_channels(c, c['premium_assumptions'])
    else:
        c = copy.deepcopy(c); premium_diagnostics = None
    baskets = [am.basket(p, o, r) for o, r in zip(oem, recycled)]
    repairs = [1+b['repair_change'] for b in baskets]
    quick = copy.deepcopy(c); quick['nodes'] = 1
    reference_ops = m.operating(quick)[0][4:]
    response = p['threshold_responsive_fraction']
    def evaluate(prices):
        changed = apply_changes(quick, repairs, prices, p)
        ops = m.operating(changed)[0][4:]
        residuals, feedback = [], []
        for i, (a, z, b, x) in enumerate(zip(reference_ops, ops, baskets, prices)):
            totals = a['totals']+response*(z['totals']-a['totals'])
            supply = totals/a['totals']
            # Existing reportable repairable-claim pool, not a census of repairs.
            filing = c.get('repairable_filing', [1.]*8)[i+4]*(1-c['nonfiling'][i+4])
            jobs_ratio = (a['prefiling_claims']-totals)*filing/(a['claims']-a['totals'])
            jobs = 1+p['repair_job_recapture']*(jobs_ratio-1)
            recycler = p['donor_contribution_exposed_fraction']*p['donor_contribution_to_hammer_bid']*(b['recycled_retention']*jobs-1)
            rebuilder = -b['repair_change']*p['rebuilder_repair_bill_to_hammer_bid']
            scarcity = -p['supply_price_response']*math.log(supply)
            implied = p['recycler_price_transmission_weight']*recycler+(1-p['recycler_price_transmission_weight'])*rebuilder+scarcity
            residuals.append(implied-x)
            feedback.append(dict(quarter=i+1,repair_change=b['repair_change'],price_change=x,
                supply_ratio=supply,repair_jobs_ratio=jobs_ratio,recycler_bid_change=recycler,
                rebuilder_bid_change=rebuilder,scarcity_price_support=scarcity,residual=implied-x))
        return residuals, feedback
    if all(x == 0 for x in oem+recycled):
        prices = [0.]*4
    else:
        lo = [-.8]*4; hi = [.8]*4
        flo, _ = evaluate(lo); fhi, _ = evaluate(hi)
        if any(a*b > 0 for a, b in zip(flo, fhi)):
            raise ValueError('Quarterly sourcing equilibrium not bracketed')
        for _ in range(32):
            mid = [(a+b)/2 for a, b in zip(lo, hi)]
            fm, _ = evaluate(mid)
            for i in range(4):
                if fm[i]*flo[i] > 0:
                    lo[i] = mid[i]; flo[i] = fm[i]
                else:
                    hi[i] = mid[i]
        prices = [(a+b)/2 for a, b in zip(lo, hi)]
    residuals, feedback = evaluate(prices)
    if max(map(abs, residuals)) > 1e-8:
        raise AssertionError('Quarterly equilibrium did not converge')
    responsive = m.run(apply_changes(c, repairs, prices, p))
    locked = m.run(apply_changes(c, repairs, prices, p, selection=False))
    if responsive['base_ledger'] != locked['base_ledger']:
        raise AssertionError('Historical ledger changed between claim populations')
    # Recompute all ratios from additive quantities, never average cohort ratios.
    result = copy.deepcopy(responsive)
    financial = ['insurance_core_musd','title_musd','delivery_musd','other_us_musd','us_service_musd',
                 'intl_service_musd','legacy_service_musd','purchased_musd','legacy_total_musd','modeled_insurance_sales']
    rows = []
    for q, (a, z) in enumerate(zip(responsive['quarters'], locked['quarters'])):
        row = {k:response*a[k]+(1-response)*z[k] for k in financial}
        row.update(period=a['period'],TLF=(response*responsive['operating'][q+4]['totals']+(1-response)*locked['operating'][q+4]['totals']) /
                   (response*responsive['operating'][q+4]['claims']+(1-response)*locked['operating'][q+4]['claims']))
        row['insurance_ASP'] = (response*a['modeled_insurance_sales']*a['insurance_ASP']+(1-response)*z['modeled_insurance_sales']*z['insurance_ASP'])/row['modeled_insurance_sales']
        row['insurance_core_RPU'] = row['insurance_core_musd']*1e6/row['modeled_insurance_sales']
        rows.append(row)
    result['quarters'] = rows
    for q, (a, z) in enumerate(zip(responsive['operating'], locked['operating'])):
        row = {k:response*a[k]+(1-response)*z[k] for k in ['claims','prefiling_claims','totals','assignments','buyer','seller','proceeds']}
        row.update(TLF=row['totals']/row['claims'],TLF_prefiling=row['totals']/row['prefiling_claims'],
            ASP=row['proceeds']/row['assignments'],core_RPU=(row['buyer']+row['seller'])/row['assignments'],
            capture_including_routing=row['assignments']/row['totals'])
        result['operating'][q] = row
    # The inherited cells belong to the responsive branch only; omit rather than
    # mislabel them as the aggregate of the two disjoint populations.
    result.pop('cells', None)
    result['premium_diagnostics'] = premium_diagnostics
    result['aftermarket_feedback'] = feedback
    return result


def annual(r):
    quarters = r['quarters']
    units = sum(q['modeled_insurance_sales'] for q in quarters)
    insurance = sum(sum(q[k] for k in ['insurance_core_musd','title_musd','delivery_musd']) for q in quarters)
    return dict(service_musd=sum(q['legacy_service_musd'] for q in quarters),insurance_musd=insurance,
                modeled_insurance_units=units,insurance_allin_RPU=insurance*1e6/units)


def effects(r, base):
    a = annual(r); z = annual(base)
    out = dict(a,delta_service_musd=a['service_musd']-z['service_musd'],
        unit_change=a['modeled_insurance_units']/z['modeled_insurance_units']-1,
        allin_RPU_change=a['insurance_allin_RPU']/z['insurance_allin_RPU']-1)
    du = a['modeled_insurance_units']-z['modeled_insurance_units']
    dr = a['insurance_allin_RPU']-z['insurance_allin_RPU']
    out.update(units_contribution_musd=du*z['insurance_allin_RPU']/1e6,
               RPU_contribution_musd=z['modeled_insurance_units']*dr/1e6,product_interaction_musd=du*dr/1e6)
    if abs(out['delta_service_musd']-out['units_contribution_musd']-out['RPU_contribution_musd']-out['product_interaction_musd']) > 1e-7:
        raise AssertionError('Revenue identity failed; other branches must share a reference')
    return out
