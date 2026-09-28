"""Economic invariants, population gates and independent saved-output checks."""
import copy
import csv
import json
import math
import model as m


def main():
    passed=[]
    def check(name, condition):
        if not condition: raise AssertionError(name)
        passed.append(name)
    def close(a,b): return math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7)
    def rejects(name,fn):
        try: fn()
        except ValueError: passed.append(name);return
        raise AssertionError(name)
    c=m.configuration();r=m.run(c)
    with (m.LEGACY/'connected_quarterly_bridge.csv').open() as f: saved=list(csv.DictReader(f))
    for i in range(4):
        check(f'Q{i+1} saved neutral parity',close(r['quarters'][i]['legacy_service_musd'],float(saved[i]['fleet_only_total_service_musd'])))
    cr=copy.deepcopy(c);cr['carrier_mode']='inherited_runoff';rr=m.run(cr)
    with (m.LEGACY/'reconciled_quarterly_service.csv').open() as f: old=list(csv.DictReader(f))[4:]
    check('Inherited allocation reproduces original dollars',all(close(a['legacy_service_musd'],float(b['legacy_service_musd'])) for a,b in zip(rr['quarters'],old)))
    cp=copy.deepcopy(c);cp['realized_salvage']=m.forecast(1.05);rp=m.run(cp)
    check('Realized-price-only change preserves units',all(close(a['modeled_insurance_sales'],b['modeled_insurance_sales']) for a,b in zip(r['quarters'],rp['quarters'])))
    check('Higher realized prices raise core fees',all(b['insurance_core_RPU']>a['insurance_core_RPU'] for a,b in zip(r['quarters'],rp['quarters'])))
    ce=copy.deepcopy(c);ce['expected_salvage']=m.forecast(1.03);re=m.run(ce)
    check('Expected salvage affects total-loss selection',all(b['modeled_insurance_sales']>a['modeled_insurance_sales'] for a,b in zip(r['quarters'],re['quarters'])))
    cv=copy.deepcopy(c);cv['repair']=m.forecast(1.05);cv['value']=m.forecast(1.05);rv=m.run(cv)
    check('Equal repair/value scaling preserves totals',all(close(a['totals'],b['totals']) for a,b in zip(r['operating'],rv['operating'])))
    cn=copy.deepcopy(c);cn['nonfiling']=m.forecast(.1,0);rn=m.run(cn)
    check('Repairable nonfiling preserves revenue',all(close(a['legacy_service_musd'],b['legacy_service_musd']) for a,b in zip(r['quarters'],rn['quarters'])))
    check('Repairable nonfiling raises TLF',all(b['TLF']>a['TLF'] for a,b in zip(r['quarters'],rn['quarters'])))
    ci=copy.deepcopy(c);ci['insurance_service_fraction']=.8;ri=m.run(ci)
    check('Alternative split preserves historical dollars',all(close(sum(a.values()),sum(b.values())) for a,b in zip(r['base_ledger'],ri['base_ledger'])))
    check('Alternative split changes inferred units',all(not close(a,b) for a,b in zip(r['base_modeled_units'],ri['base_modeled_units'])))
    cc=copy.deepcopy(c);cc['allocation_overrides']['Progressive']=[.25,.25,.159090909,.068181818]+[.95]*4
    rc=m.run(cc)
    check('Common carrier economics: allocation leaves RPU invariant',all(close(a['insurance_core_RPU'],b['insurance_core_RPU']) for a,b in zip(r['quarters'],rc['quarters'])))
    ch=copy.deepcopy(c);ch['carrier_terms']={'Progressive':{'value_factor':1.3}};rh=m.run(ch)
    ch['allocation_overrides']=cc['allocation_overrides'];rh2=m.run(ch)
    check('Heterogeneous carrier economics: allocation now changes RPU',any(not close(a['insurance_core_RPU'],b['insurance_core_RPU']) for a,b in zip(rh['quarters'],rh2['quarters'])))
    ct=copy.deepcopy(c);ct['title']['adoption']=m.forecast(.6,.5);rt=m.run(ct)
    check('Service-only adoption preserves auction units',all(close(a['modeled_insurance_sales'],b['modeled_insurance_sales']) for a,b in zip(r['quarters'],rt['quarters'])))
    check('Service-only adoption increases title revenue',all(b['title_musd']>a['title_musd'] for a,b in zip(r['quarters'],rt['quarters'])))
    check('Forecast changes preserve historical ledger',r['base_ledger']==rt['base_ledger'])
    # Hand-calculated synthetic conservation example: no company data implied.
    sold,ledger=m.flow([100,100,0,0],[[.5,.5]]*4,[20,0,0,0])
    check('Inventory example independently calculated',sold==[70,100,50,0] and ledger[-1]['closing']==0)
    check('Every inventory quarter conserves vehicles',all(close(x['opening']+x['arrivals']-x['sales']-x['withdrawals'],x['closing']) for x in ledger))
    rejects('Reject missing opening inventory',lambda:m.flow([100],[[1]],None))
    rejects('Reject duplicate sale probability',lambda:m.flow([100],[[.7,.7]],[]))
    t=copy.deepcopy(c['sales_timing']);t.update(mode='assignment_flow',input_stage='assignments',without_title_kernel=[.5,.5],with_title_kernel=[1.],opening_release=[0,0,0,0],rpu_by_vintage=[[10]*4 for _ in range(4)],opening_rpu=[10]*4)
    s0,l0,v0=m.timed_core([100,100,0,0],t,[0]*4)
    s1,l1,v1=m.timed_core([100,100,0,0],t,[1]*4)
    check('Title timing acceleration changes quarterly sales',s0==[50,100,50,0] and s1==[100,100,0,0])
    check('Title acceleration does not create lifetime units or fees',sum(s0)==sum(s1)==200 and sum(v0)==sum(v1)==2000)
    timing=copy.deepcopy(c);timing['sales_timing']=t;timing['title']['basis']='assignments'
    tr=m.run(timing)
    check('Full forecast integrates timing and title events',tr['inventory'] is not None and all(x['insurance_ASP'] is None for x in tr['quarters']))
    bad=copy.deepcopy(timing);bad['sales_timing']['input_stage']='sale_equivalent'
    rejects('Reject double-lagging sale-equivalent allocation',lambda:m.run(bad))
    bad=copy.deepcopy(timing);bad['sales_timing']['opening_rpu']=None
    rejects('Reject unpriced opening backlog',lambda:m.run(bad))
    service=copy.deepcopy(c['delivery']);service.update(basis='external',eligible_external=[100,200,0,0],recognition_kernel=[0,1.],opening_release=[0]*4)
    rev,jobs,rl=m.service_revenue(service,[1]*4,[1]*4)
    check('External jobs recognized independently of auctions',jobs==[10,20,0,0] and rev==[0,3000,6000,0])
    service['waiver']=[100]*8;rvw,_,_=m.service_revenue(service,[1]*4,[1]*4)
    check('Fee waiver reduces incremental service revenue',rvw==[0,2000,4000,0])
    service['bundled']=True;rvb,_,_=m.service_revenue(service,[1]*4,[1]*4)
    check('Bundled service not double counted',sum(rvb)==0)
    bad=copy.deepcopy(c);bad['intl_fx']=m.forecast(1.02)
    rejects('Reject duplicate FX in reported-currency RPU',lambda:m.run(bad))
    bad=copy.deepcopy(c);bad['schedule_ids'][4]='unknown'
    rejects('Reject unknown fee vintage',lambda:m.run(bad))
    for x in r['quarters']:
        check(x['period']+' exclusive ledger',close(x['legacy_service_musd'],sum(x[k] for k in ['insurance_core_musd','title_musd','delivery_musd','other_us_musd','intl_service_musd'])))
        check(x['period']+' core unit RPU identity',close(x['modeled_insurance_sales']*x['insurance_core_RPU']/1e6,x['insurance_core_musd']))
    check('Unknown acquired scope stays null',all(x['consolidated_total_musd'] is None and x['consolidated_service_musd'] is None for x in r['quarters']))
    bad=copy.deepcopy(c);bad['acquired_total'][0]=10
    rejects('Reject pre-control acquired revenue',lambda:m.run(bad))
    bad=copy.deepcopy(c);bad['acquired_service'][1]=10
    rejects('Reject service without acquired total/classification',lambda:m.run(bad))
    # Every output control has a limited interpretation; no fit is called validation.
    (m.HERE/'tests.json').write_text(json.dumps({'passed':len(passed),'checks':passed,'status':'Structural and arithmetic checks, not predictive validation'},indent=2)+'\n')
    print(json.dumps({'passed':len(passed)}))


if __name__=='__main__':main()
