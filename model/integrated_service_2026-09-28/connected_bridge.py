"""Sequential quarterly revenue attribution with exact-age fleet marginals.
Order-dependent contributions, not causal estimates or a Shapley attribution.
"""
import copy,hashlib,json
import engine as m
import history_repair as h

def main():
    d,e,c=m.load();result=m.run(d,e,c);reconciled=h.build(d,c,result)
    active=m.fleet_data(d,c);_,raw0=m.stock(d,[0,0,1,0,0])
    cw={(b,k):e['relative_claim_weights'][k]*e['body_weights'][str(k)][b] for b in range(4) for k in range(6)}
    z=sum(cw.values());correction={key:v/z/raw0[key] for key,v in cw.items()}
    checks=[]
    def check(name,ok):
        assert ok,name
        checks.append(name)
    def fleet_state(p):
        counts={(r['body'],r['age']):sum(x*w for x,w in zip(r['births'],p['weights']))*r['survival']*active['split'][r['body']] for r in active['fleet']}
        ages={a:sum(counts[b,a] for b in range(4)) for a in range(46)}
        total=sum(ages.values())
        return dict(total=total,age={a:v/total for a,v in ages.items()},body={(b,a):counts[b,a]/ages[a] if ages[a] else .25 for b,a in counts})
    states=[fleet_state(p) for p in d['periods']]
    economics={}
    def evaluate(s):
        key=s['repair'],s['value']
        if key not in economics:economics[key]=m.economics(d,e,c,*key)
        eco=economics[key];units=rev=0.
        ancillary=c['title']['adoption']*s['title']*c['title']['net_incremental_fee']*(not c['title']['included_in_seller_fee'])
        ancillary+=c['delivery']['adoption']*s['delivery']*(c['delivery']['gross_external_revenue_per_job']-c['delivery']['fee_waiver_per_job'])
        for r in active['fleet']:
            b,a,k=r['body'],r['age'],r['bucket']
            claims=s['total']*s['age'][a]*s['body'][b,a]*r['relative_claim_weight']*correction[b,k]*s['frequency']
            sold=claims*eco[b,k]['probability']*s['capture']*c['routing_fraction']*c['insurance_consignment_fraction']
            units+=sold;rev+=sold*(eco[b,k]['core_RPU']+ancillary)
        return rev,units,rev/units
    def state(i):
        dr=c['quarter_drivers']
        return dict(**states[i],frequency=dr['reported_claim_frequency'][i],repair=dr['repair_cost'][i],value=dr['vehicle_value'][i],capture=result['quarters'][i]['effective_capture'],title=dr['title_adoption_multiplier'][i],delivery=dr['delivery_adoption_multiplier'][i])
    order=[('total','fleet_size'),('age','age_mix'),('body','body_within_age'),('frequency','combined_claim_frequency'),('repair','repair_cost'),('value','vehicle_value'),('capture','carrier_allocation'),('title','title_adoption'),('delivery','delivery_adoption')]
    detailed=[];summary=[]
    legacy_config=copy.deepcopy(c);legacy_config.update(claims_mode='fleet_exposure_proxy_times_reported_frequency',fleet_body_mode='fixed_split')
    legacy=h.build(d,legacy_config,m.run(d,e,legacy_config))
    for i in range(4,8):
        start=state(i-4);end=state(i);current=copy.deepcopy(start)
        r0,u0,p0=evaluate(start);anchor=d['actuals'][i-4]['us_service']*c['insurance_share_of_us_service_base']
        row=dict(period=result['quarters'][i]['period'],prior_total_service_musd=reconciled[i-4]['legacy_service_musd'],assumed_insurance_base_musd=anchor)
        previous=anchor
        for field,label in order:
            current[field]=end[field];rev,units,rpu=evaluate(current);value=anchor*rev/r0
            delta=value-previous;row[label+'_delta_musd']=delta
            detailed.append(dict(period=row['period'],step=label,insurance_musd=value,incremental_delta_musd=delta,insurance_units_factor=units/u0,insurance_RPU_factor=rpu/p0))
            previous=value
        check(row['period']+' insurance bridge matches integrated engine',m.close(previous,reconciled[i]['insurance_musd']))
        row['nonfiling_delta_musd']=0. # Repairable-only selection leaves sold totals unchanged.
        row['other_us_delta_musd']=reconciled[i]['other_us_musd']-d['actuals'][i-4]['us_service']*(1-c['insurance_share_of_us_service_base'])
        row['international_delta_musd']=reconciled[i]['intl_musd']-d['actuals'][i-4]['intl_service']
        row['forecast_total_service_musd']=reconciled[i]['legacy_service_musd']
        row['prior_architecture_forecast_musd']=legacy[i]['legacy_service_musd']
        row['architecture_revision_musd']=row['forecast_total_service_musd']-row['prior_architecture_forecast_musd']
        delta=sum(v for k,v in row.items() if k.endswith('_delta_musd'))
        check(row['period']+' total service bridge adds up',m.close(row['prior_total_service_musd']+delta,row['forecast_total_service_musd']))
        neutral=copy.deepcopy(end)
        for field in ['frequency','repair','value','capture','title','delivery']:neutral[field]=start[field]
        rn,un,pn=evaluate(neutral)
        row['fleet_only_insurance_delta_musd']=anchor*(rn/r0-1)
        row['fleet_only_units_growth_pct']=100*(un/u0-1)
        row['fleet_only_RPU_growth_pct']=100*(pn/p0-1)
        row['fleet_only_total_service_musd']=row['prior_total_service_musd']+row['fleet_only_insurance_delta_musd']
        check(row['period']+' fleet-only unit RPU identity',m.close(rn/r0,un/u0*pn/p0))
        check(row['period']+' fleet factors reconcile',m.close(row['fleet_only_insurance_delta_musd'],sum(row[x+'_delta_musd'] for x in ['fleet_size','age_mix','body_within_age'])))
        summary.append(row)
    # Independent previously saved vintage candidate is the frozen-economics cross-check.
    import csv
    with (m.HERE/'vintage_body_growth.csv').open() as f:prior=list(csv.DictReader(f))
    if all(all(v==1 for v in c['quarter_drivers'][key]) for key in ['repair_cost','vehicle_value','title_adoption_multiplier','delivery_adoption_multiplier','reported_claim_frequency']):
        for row,old in zip(summary,prior):
            check(row['period']+' prior vintage candidate agreement',m.close(row['fleet_only_insurance_delta_musd'],float(old['vintage_split_service_delta_musd'])))
    m.save_csv('connected_quarterly_bridge.csv',summary);m.save_csv('connected_bridge_steps.csv',detailed)
    paths=[m.OLD,m.ECON,m.BIRTHS,m.HERE/'engine.py',m.HERE/'assumptions.json',m.HERE/'history_repair.py',m.HERE/'connected_bridge.py']
    out={'checks_passed':len(checks),'checks':checks,'H1_fleet_only_delta_musd':sum(r['fleet_only_insurance_delta_musd'] for r in summary[:2]),'source_hashes':{str(p.relative_to(m.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'status':'Sequential order-dependent attribution; provisional legacy services only; no empirical validation claim'}
    (m.HERE/'connected_bridge_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'checks_passed':len(checks),'quarters':summary},indent=2))

if __name__=='__main__':main()
