"""Bounded structural versus forecast-shock screen. No adopted input changes."""
import hashlib,json,math
import engine as m
import history_repair as h

def main():
    d,e,c=m.load();active=m.fleet_data(d,c);base=m.run(d,e,c)
    _,raw0=m.stock(d,[0,0,1,0,0])
    weights={(b,k):e['relative_claim_weights'][k]*e['body_weights'][str(k)][b] for b in range(4) for k in range(6)}
    z=sum(weights.values());correction={key:w/z/raw0[key] for key,w in weights.items()}
    masses=[]
    for p in d['periods']:
        _,raw=m.stock(active,p['weights']);masses.append({key:v*correction[key] for key,v in raw.items()})
    grids=m.fee_grids(d);cache={};checks=[]
    def check(name,ok):
        assert ok,name
        checks.append(name)
    def economics(repair=1.,value=1.,recovery=1.,scope='SUV_pickup'):
        key=repair,value,recovery,scope
        if key in cache:return cache[key]
        out={}
        for b,k in weights:
            affected=scope=='all' or b in (1,2)
            rr,vv,ss=(repair,value,recovery) if affected else (1.,1.,1.)
            row=e['cohorts'][k];acv=row['car_ACV']*e['value_ratios'][b]*vv
            mu=row['log_car_repair_median']+math.log(e['repair_ratios'][b]*rr)
            lo,hi=1e-12,1-1e-12
            for _ in range(44):
                u=(lo+hi)/2;threshold=acv*(1-ss*(.4-.2*u)*(1-c['seller_fee_fraction']))
                if mu+row['sigma']*m.N.inv_cdf(u)<math.log(threshold):lo=u
                else:hi=u
            u=(lo+hi)/2;p=1-u;buyer=0.
            for j in range(c['fee_integration_nodes']):
                rank=u+p*(j+.5)/c['fee_integration_nodes'];price=acv*ss*(.4-.2*rank)
                buyer+=((1-c['preferred_buyer_fraction'])*m.fee(price,grids[0])+c['preferred_buyer_fraction']*m.fee(price,grids[1])+m.fee(price,grids[2])+c['gate_environment_fee'])/c['fee_integration_nodes']
            asp=acv*ss*(.3-.1*u)
            ancillary=c['title']['adoption']*c['title']['net_incremental_fee']*(not c['title']['included_in_seller_fee'])+c['delivery']['adoption']*(c['delivery']['gross_external_revenue_per_job']-c['delivery']['fee_waiver_per_job'])
            out[b,k]={'p':p,'rpu':buyer+c['seller_fee_fraction']*asp+ancillary,'asp':asp}
        cache[key]=out;return out
    baseline=economics();engine_eco=m.economics(d,e,c,1,1)
    check('Baseline recovery economics reproduce engine probabilities',all(m.close(x['p'],engine_eco[key]['probability']) for key,x in baseline.items()))
    equal=economics(repair=1.05,value=1.05,scope='all')
    check('Equal repair and value scaling preserves total-loss probabilities',all(m.close(x['p'],baseline[key]['p']) for key,x in equal.items()))
    higher=economics(recovery=1.2)
    check('Higher recovery increases affected total-loss probabilities',all(higher[b,k]['p']>baseline[b,k]['p'] for b,k in weights if b in (1,2)))
    check('Body-specific recovery leaves other probabilities unchanged',all(m.close(higher[b,k]['p'],baseline[b,k]['p']) for b,k in weights if b not in (1,2)))
    def stats(i,eco):
        units=sum(masses[i][key]*x['p'] for key,x in eco.items())
        revenue=sum(masses[i][key]*x['p']*x['rpu'] for key,x in eco.items())
        return units,revenue/units,revenue
    cases=[dict(name='baseline',mode='structural',repair=1.,value=1.,recovery=1.,scope='SUV_pickup')]
    for mode in ['structural','forecast_only']:
        for variable,levels in [('repair',[.9,1.1]),('value',[.9,1.1]),('recovery',[.8,1.2])]:
            for level in levels:
                case=dict(name=f'{mode}_{variable}_{level}',mode=mode,repair=1.,value=1.,recovery=1.,scope='SUV_pickup');case[variable]=level;cases.append(case)
    for variable in ['repair','value']:
        for level in [.95,1.05]:
            case=dict(name=f'all_forecast_{variable}_{level}',mode='forecast_only',repair=1.,value=1.,recovery=1.,scope='all');case[variable]=level;cases.append(case)
    rows=[];summaries=[];history=h.build(d,c,base)
    for case in cases:
        altered=economics(**{k:case[k] for k in ['repair','value','recovery','scope']});prior=altered if case['mode']=='structural' else baseline
        for i in range(4,8):
            u0,p0,r0=stats(i-4,prior);u1,p1,r1=stats(i,altered)
            anchor=d['actuals'][i-4]['us_service']*c['insurance_share_of_us_service_base']
            total0=d['actuals'][i-4]['us_service']+d['actuals'][i-4]['intl_service']
            cap=base['quarters'][i]['effective_capture']/base['quarters'][i-4]['effective_capture']
            neutral=anchor*(r1/r0-1);carrier=anchor*r1/r0*(cap-1)
            check(case['name']+str(i)+' unit RPU identity',m.close(r1/r0,u1/u0*p1/p0))
            rows.append(dict(case=case['name'],mode=case['mode'],scope=case['scope'],period=d['periods'][i]['label'],repair_multiplier=case['repair'],value_multiplier=case['value'],recovery_multiplier=case['recovery'],neutral_delta_musd=neutral,carrier_increment_musd=carrier,neutral_service_musd=total0+neutral,inherited_carrier_service_musd=total0+neutral+carrier,neutral_units_growth_pct=100*(u1/u0-1),neutral_RPU_growth_pct=100*(p1/p0-1)))
            if case['name']=='baseline':check('Baseline headline '+str(i),m.close(total0+neutral+carrier,history[i]['legacy_service_musd']))
        selected=rows[-4:-2]
        summaries.append(dict(**case,H1_neutral_delta_musd=sum(x['neutral_delta_musd'] for x in selected),H1_carrier_increment_musd=sum(x['carrier_increment_musd'] for x in selected)))
    base_delta=summaries[0]['H1_neutral_delta_musd'];denom=sum(d['actuals'][i]['us_service']+d['actuals'][i]['intl_service'] for i in range(2))
    for row in summaries:
        row['H1_change_vs_baseline_musd']=row['H1_neutral_delta_musd']-base_delta
        row['H1_change_vs_baseline_pct_of_service']=100*row['H1_change_vs_baseline_musd']/denom
    m.save_csv('materiality_quarters.csv',rows);m.save_csv('materiality_summary.csv',summaries)
    paths=[m.OLD,m.ECON,m.BIRTHS,m.HERE/'assumptions.json',m.HERE/'engine.py',m.HERE/'materiality_screen.py']
    out={'case_count':len(cases),'checks_passed':len(checks),'checks':checks,'H1_prior_service_musd':denom,'source_hashes':{str(p.relative_to(m.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'status':'Hypothetical one-factor screen, not confidence bounds. Structural cases alter both periods without refitting historical targets. Forecast cases are unverified time shocks. No forecast overwrite.'}
    (m.HERE/'materiality_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'checks_passed':len(checks),'case_count':len(cases),'summary':summaries},indent=2))

if __name__=='__main__':main()
