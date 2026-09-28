"""Incremental nonfiling identity and integration tests; no forecast adoption."""
import copy,json
import engine as m
import history_repair as h

def main():
    d,e,c=m.load();base=m.run(d,e,c);checks=[]
    def check(name,ok):
        assert ok,name
        checks.append(name)
    config=copy.deepcopy(c)
    config['incremental_repairable_nonfiling'][4:]=[.1,.2,.05,.15]
    scenario=m.run(d,e,config)
    check('Forecast nonfiling leaves history unchanged',base['quarters'][:4]==scenario['quarters'][:4])
    check('Normalization unchanged',m.close(base['claim_scale'],scenario['claim_scale']))
    for a,b in zip(base['quarters'][4:],scenario['quarters'][4:]):
        label=b['period']
        check(label+' claims decline and TLF rises',b['claims_raw']<a['claims_raw'] and b['TLF']>a['TLF'])
        check(label+' paired identity',m.close(b['claims_raw']*b['TLF'],a['total_losses_raw']))
        for key in ['total_losses_raw','normalized_fee_sales','ASP','core_RPU','insurance_allin_RPU','insurance_musd','legacy_service_musd']:
            check(label+' invariant '+key,m.close(a[key],b[key]))
        rows=[r for r in scenario['cohorts'] if r['period']==label]
        check(label+' selected claim weights reconcile',m.close(sum(r['reported_claim_weight'] for r in rows),1))
        check(label+' cohort claims reconcile',m.close(sum(r['claim_equivalent_raw'] for r in rows),b['claims_raw']))
        check(label+' cohort TLF aggregation',m.close(sum(r['reported_claim_weight']*r['TLF'] for r in rows),b['TLF']))
    for a,b in zip(h.build(d,c,base)[4:],h.build(d,config,scenario)[4:]):
        for key in ['insurance_units_factor','insurance_musd','legacy_service_musd']:
            check(b['period']+' same-quarter bridge '+key,m.close(a[key],b[key]))
    # Economic changes can affect totals; adding repairable-only nonfiling must not.
    repair=copy.deepcopy(c);repair['quarter_drivers']['repair_cost'][4]=1.02
    repair_filter=copy.deepcopy(repair);repair_filter['incremental_repairable_nonfiling'][4]=.1
    a=m.run(d,e,repair)['quarters'][4];b=m.run(d,e,repair_filter)['quarters'][4]
    check('Repair changes totals',not m.close(a['total_losses_raw'],base['quarters'][4]['total_losses_raw']))
    check('Nonfiling preserves economically changed revenue',m.close(a['insurance_musd'],b['insurance_musd']))
    for value in [-.01,1,float('nan'),None]:
        bad=copy.deepcopy(c);bad['incremental_repairable_nonfiling'][4]=value
        try:m.run(d,e,bad)
        except ValueError:check('Invalid fraction rejected '+str(value),True)
        else:raise AssertionError('Invalid fraction accepted')
    bad=copy.deepcopy(c);bad['claims_frequency_convention']='observed_frequency_already_includes_nonfiling'
    try:m.run(d,e,bad)
    except ValueError:check('Incompatible frequency convention rejected',True)
    else:raise AssertionError('Invalid convention accepted')
    out={'checks_passed':len(checks),'checks':checks,'status':'Synthetic integration checks; no estimated nonfiling rates or forecast changes',
         'example_FY27Q1':{k:scenario['quarters'][4][k] for k in ['baseline_TLF','TLF','incremental_repairable_nonfiling']}}
    (m.HERE/'nonfiling_checks_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'checks_passed':len(checks),'example_FY27Q1':out['example_FY27Q1']}))

if __name__=='__main__':main()
