"""Economic invariants for interfaces added by the thesis audit."""
import copy
import json
import math
import scenarios as s


def main():
    checks=[]
    def check(name,condition):
        if not condition:raise AssertionError(name)
        checks.append(name)
    def close(a,b):return math.isclose(a,b,rel_tol=1e-8,abs_tol=1e-7)
    def rejects(name,fn):
        try:fn()
        except ValueError:checks.append(name);return
        raise AssertionError(name)
    c,p,premiums=s.load(); ref=s.m.run(c); d,_,_=s.m.old.load()
    optional=copy.deepcopy(c);optional.update(fleet_period_weights=None,carrier_claim_weights_by_period=None)
    check('Null optional period controls preserve the reference',close(s.annual(s.m.run(optional))['service_musd'],s.annual(ref)['service_musd']))
    # Frozen claim pool, identical economics and same-quarter allocation: units
    # must equal their inferred prior-year level, despite differing fee dollars.
    frozen=copy.deepcopy(c);frozen['fleet_period_weights']=[x['weights'] for x in d['periods'][:4]]*2
    fr=s.m.run(frozen)
    check('Frozen fleet produces unchanged inferred units',all(close(q['modeled_insurance_sales'],u) for q,u in zip(fr['quarters'],fr['base_modeled_units'])))
    check('Fleet override preserves historical ledger',fr['base_ledger']==ref['base_ledger'])
    # Period carrier weights reproduce normalized historical data, then change
    # only forward exposure. A policy premium-share proxy cannot be silently
    # combined with a different static cell-weight denominator.
    cc=copy.deepcopy(c)
    cc['carrier_claim_weights_by_period']=[]
    for q in range(8):
        weights={x['name']:x['weights'][q%4] for x in d['carriers']};z=sum(weights.values())
        cc['carrier_claim_weights_by_period'].append({k:v/z for k,v in weights.items()})
    check('Explicit quarter weights preserve original result',close(s.annual(s.m.run(cc))['service_musd'],s.annual(ref)['service_musd']))
    cc['carrier_claim_weights_by_period'][4:] = [dict.fromkeys(cc['carrier_claim_weights_by_period'][0],0.) for _ in range(4)]
    for q in cc['carrier_claim_weights_by_period'][4:]:q['Progressive']=1.
    changed=s.m.run(cc)
    check('Quarter carrier weights change units without rewriting history',changed['base_ledger']==ref['base_ledger'] and not close(s.annual(changed)['modeled_insurance_units'],s.annual(ref)['modeled_insurance_units']))
    terms=copy.deepcopy(c);terms['carrier_terms_by_period']={'Progressive':[{} for _ in range(4)]+[{'seller_pct':.03} for _ in range(4)]}
    tr=s.m.run(terms)
    check('Dated carrier concession preserves historical normalization',tr['base_ledger']==ref['base_ledger'])
    check('Dated carrier concession changes seller economics',not close(s.annual(tr)['service_musd'],s.annual(ref)['service_musd']))
    for key,values in [('allocation_overrides',{'Typo':[.5]*8}),('allocation_overrides',{'Progressive':[.5]*4}),('carrier_terms_by_period',{'Progressive':[{}]*4}),('fleet_period_weights',[[0,0,0,0,0]]*8)]:
        bad=copy.deepcopy(c);bad[key]=values
        rejects('Invalid '+key+' '+str(len(checks)),lambda:s.m.run(bad))
    bad=copy.deepcopy(cc);bad['carrier_claim_weights_by_cell']={'0:0':cc['carrier_claim_weights_by_period'][0]}
    rejects('Ambiguous cell and period weights rejected',lambda:s.m.run(bad))
    bad=copy.deepcopy(cc);bad['carrier_claim_weights_by_period'][0]['Progressive']=float('nan')
    rejects('Nonfinite carrier weight rejected',lambda:s.m.run(bad))
    prem=copy.deepcopy(c);prem['premium_assumptions']=premiums['premiums_10pct_above_reference']
    direct=s.m.operating(prem)[0];full=s.m.run(prem)['operating']
    check('Direct operating interface applies premium channels',all(close(a['totals'],b['totals']) for a,b in zip(direct,full)) and direct[4]['totals']<ref['operating'][4]['totals'])
    zero=s.run_aftermarket(prem,p,[0.]*4,[0.]*4)
    check('Zero sourcing preserves combined premium model',close(s.annual(zero)['service_musd'],s.annual(s.m.run(prem))['service_musd']))
    no_switch=s.run_aftermarket(c,dict(p,threshold_responsive_fraction=0.),[.01,.02,.03,.04],[.00375,.0075,.01125,.015])
    check('Zero disposition response preserves total-loss units',all(close(a['modeled_insurance_sales'],b['modeled_insurance_sales']) for a,b in zip(no_switch['quarters'],ref['quarters'])))
    normal=s.run_aftermarket(c,p,[.01,.02,.03,.04],[.00375,.0075,.01125,.015])
    check('Quarterly sourcing converges',max(abs(x['residual']) for x in normal['aftermarket_feedback'])<1e-8)
    check('Quarterly sourcing respects adoption ramp',abs(normal['aftermarket_feedback'][0]['price_change'])<abs(normal['aftermarket_feedback'][3]['price_change']))
    check('Sourcing preserves historical ledger',normal['base_ledger']==ref['base_ledger'])
    check('Reported TLF reconstructed from additive totals',all(close(q['TLF'],o['totals']/o['claims']) for q,o in zip(normal['quarters'],normal['operating'][4:])))
    # Independent permutation calculation, distinct from weighted subset formula.
    import csv,itertools
    with (s.HERE/'scenario_summary.csv').open() as f:rows={int(x['mask']):float(x['service_musd']) for x in csv.DictReader(f)}
    permutation=[0.]*4
    for order in itertools.permutations(range(4)):
        old=0
        for i in order:
            new=old | (1 << i);permutation[i]+=(rows[new]-rows[old])/24;old=new
    output=json.loads((s.HERE/'results.json').read_text())
    check('All 24 orderings independently reconcile factor attribution',all(close(a,b['service_contribution_musd']) for a,b in zip(permutation,output['factor_attribution'])))
    check('Four contributions sum to total shortfall',close(sum(permutation),rows[15]-rows[0]))
    check('Repairable nonfiling has zero revenue effect',abs(output['diagnostics']['10pct_repairable_nonfiling_only']['delta_service_musd'])<1e-8)
    check('Expected recovery and repair inflation increase totals',output['diagnostics']['expected_salvage_plus5pct']['unit_change']>0 and output['diagnostics']['repair_plus5pct']['unit_change']>0)
    (s.HERE/'checks.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'scope':'Arithmetic and economic invariants only; does not validate behavioral response magnitudes'},indent=2)+'\n')
    print(json.dumps({'passed':len(checks)}))

if __name__=='__main__':main()
