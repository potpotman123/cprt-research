"""Feed vintage body shares through frozen survival, selection and fee economics.
Keep historical level effects separate from same-quarter growth; no refitting.
"""
import copy,csv,hashlib,json,math
import engine as m

BIRTHS=m.ROOT/'docs/historical_body_births_2026-09-28/candidate_body_births.csv'
BODY=['Car','SUV','Pickup','Minivan']

def adapt(d,births):
    out=copy.deepcopy(d);out['split']=[1,1,1,1]
    for r in out['fleet']:
        name='Van' if r['body']==3 else BODY[r['body']]
        r['births']=[births[y-r['age'],name] for y in range(2023,2028)]
    return out

def main():
    d,e,c=m.load()
    with BIRTHS.open() as f:births={(int(r['year']),r['body']):float(r['births_thousands']) for r in csv.DictReader(f)}
    new=adapt(d,births);eco=m.economics(d,e,c,1,1)
    _,raw0=m.stock(d,[0,0,1,0,0])
    cw={(b,k):e['relative_claim_weights'][k]*e['body_weights'][str(k)][b] for b in range(4) for k in range(6)}
    norm=sum(cw.values());cw={key:v/norm for key,v in cw.items()}
    correction={key:cw[key]/raw0[key] for key in cw}
    ancillary=c['title']['adoption']*c['title']['net_incremental_fee']*(not c['title']['included_in_seller_fee'])+c['delivery']['adoption']*(c['delivery']['gross_external_revenue_per_job']-c['delivery']['fee_waiver_per_job'])
    records=[];cells=[];states={};checks=[]
    def check(name,ok):
        if not ok:raise AssertionError(name)
        checks.append(name)
    def state(data,weights):
        fleet,raw=m.stock(data,weights);mass={key:raw[key]*correction[key] for key in raw}
        claims=sum(mass.values());losses=sum(mass[key]*eco[key]['probability'] for key in mass)
        proceeds=sum(mass[key]*eco[key]['probability']*eco[key]['ASP'] for key in mass)
        revenue=sum(mass[key]*eco[key]['probability']*(eco[key]['core_RPU']+ancillary) for key in mass)
        return dict(fleet_thousands=fleet,claim_mass=claims,total_loss_mass=losses,TLF=losses/claims,ASP=proceeds/losses,allin_RPU=revenue/losses,service_mass=revenue),mass
    for case,data in [('fixed_split',d),('vintage_split',new)]:
        states[case]=[]
        for p in d['periods']:
            s,mass=state(data,p['weights']);period=f'FY{p["fy"]}Q{p["q"]}';states[case].append(s)
            records.append(dict(case=case,period=period,**s))
            for (b,k),v in mass.items():
                x=eco[b,k]
                cells.append(dict(case=case,period=period,body=BODY[b],age_bucket=e['cohorts'][k]['age_bucket'],claim_share=v/s['claim_mass'],total_loss_share=v*x['probability']/s['total_loss_mass'],claim_mass=v,total_loss_mass=v*x['probability'],TLF=x['probability'],ASP=x['ASP'],allin_RPU=x['core_RPU']+ancillary,service_mass=v*x['probability']*(x['core_RPU']+ancillary)))
            check(case+period+' units times RPU',m.close(s['total_loss_mass']*s['allin_RPU'],s['service_mass']))
    for i,p in enumerate(d['periods']):
        check(str(i)+' total surviving fleet preserved',m.close(states['fixed_split'][i]['fleet_thousands'],states['vintage_split'][i]['fleet_thousands']))
    # This adapter must reproduce the prior result when subtype birth shares are constant.
    fixedbirths={}
    for r in d['fleet']:
        for j,y in enumerate(range(2023,2028)):
            name='Van' if r['body']==3 else BODY[r['body']]
            fixedbirths[y-r['age'],name]=r['births'][j]*d['split'][r['body']]
    identity=adapt(d,fixedbirths)
    check('Constant-share adapter reproduces original stock and claims',all(m.close(state(identity,p['weights'])[0]['service_mass'],state(d,p['weights'])[0]['service_mass']) for p in d['periods']))
    growth=[]
    for i in range(4,8):
        actual=d['actuals'][i-4];base=actual['us_service']*c['insurance_share_of_us_service_base'];values={}
        for case in states:
            q,b=states[case][i],states[case][i-4]
            units=q['total_loss_mass']/b['total_loss_mass'];rpu=q['allin_RPU']/b['allin_RPU'];ratio=units*rpu
            values[case]=dict(units_growth_pct=(units-1)*100,RPU_growth_pct=(rpu-1)*100,insurance_growth_pct=(ratio-1)*100,service_delta_musd=base*(ratio-1))
            check(case+str(i)+' growth identity',m.close(ratio,q['service_mass']/b['service_mass']))
        growth.append(dict(period=d['periods'][i]['label'],assumed_insurance_base_musd=base,**{case+'_'+key:v for case,x in values.items() for key,v in x.items()},vintage_minus_fixed_musd=values['vintage_split']['service_delta_musd']-values['fixed_split']['service_delta_musd']))
    # Baseline compatibility: age-specific TLF and selected values under frozen economics.
    calibration=[];basecases={case:state(data,[0,0,1,0,0]) for case,data in [('fixed_split',d),('vintage_split',new)]}
    for k in range(6):
        r={'age_bucket':e['cohorts'][k]['age_bucket'],'target_TLF':d['calibration'][k]['target']}
        for case,(s,mass) in basecases.items():
            exposure=sum(mass[b,k] for b in range(4));tl=sum(mass[b,k]*eco[b,k]['probability'] for b in range(4))
            r[case+'_TLF']=tl/exposure
            r[case+'_selected_ACV']=sum(mass[b,k]*eco[b,k]['probability']*eco[b,k]['ACV'] for b in range(4))/tl
        r['vintage_TLF_target_error_pp']=100*(r['vintage_split_TLF']-r['target_TLF']);calibration.append(r)
        check(str(k)+' old TLF calibration reproduced',abs(r['fixed_split_TLF']-r['target_TLF'])<1e-9)
    oldbridge=list(csv.DictReader((m.HERE/'fleet_revenue_bridge.csv').open()))
    check('Fixed case reproduces previous cohort bridge',all(m.close(r['fixed_split_service_delta_musd'],float(old['cohort_delta_musd'])) for r,old in zip(growth,oldbridge)))
    for name,rows in [('vintage_body_quarters.csv',records),('vintage_body_cells.csv',cells),('vintage_body_growth.csv',growth),('vintage_body_calibration.csv',calibration)]:m.save_csv(name,rows)
    summary={key:sum(r[key] for r in growth[:2]) for key in ['fixed_split_service_delta_musd','vintage_split_service_delta_musd','vintage_minus_fixed_musd']}
    paths=[BIRTHS,m.OLD,m.ECON,m.HERE/'assumptions.json',m.HERE/'vintage_body_integration.py']
    out={'H1_carrier_neutral':summary,'CY2025_level_comparison':{case:s for case,(s,_) in basecases.items()},'max_vintage_TLF_calibration_gap_pp':max(abs(r['vintage_TLF_target_error_pp']) for r in calibration),'checks_passed':len(checks),'checks':checks,'source_hashes':{str(p.relative_to(m.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'status':'Integrated candidate comparison; production forecast unchanged; fixed original calibration corrections and cell economics','limitations':['Model-year production shares transferred to existing sales births','SUV combines car/truck regulatory classes; not separate crossover vs traditional SUV','All vans mapped to inherited minivan economics','2025-27 subtype mix held at final 2024','No calibration refit; base-year target drift exposed','No carrier or adoption changes; 90% insurance revenue share assumed']}
    (m.HERE/'vintage_body_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['checks','source_hashes']},indent=2))

if __name__=='__main__':main()
