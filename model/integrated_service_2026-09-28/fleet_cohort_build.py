"""Carrier-neutral cohort build from existing annual sales and fitted propensities.
No new evidence, parameter fit or production forecast overwrite.
"""
import csv,json,hashlib
import engine as m

def main():
    d,e,c=m.load();eco=m.economics(d,e,c,1,1)
    stock0,raw0=m.stock(d,[0,0,1,0,0])
    cw={(b,k):e['relative_claim_weights'][k]*e['body_weights'][str(k)][b] for b in range(4) for k in range(6)}
    total=sum(cw.values());cw={key:v/total for key,v in cw.items()}
    # Cell correction reproduces the existing calibration while retaining single-age R(a).
    correction={key:cw[key]/raw0[key] for key in cw}
    detail=[];cells=[];quarters=[];states=[];checks=0
    ancillary=c['title']['adoption']*c['title']['net_incremental_fee']*(not c['title']['included_in_seller_fee'])+c['delivery']['adoption']*(c['delivery']['gross_external_revenue_per_job']-c['delivery']['fee_waiver_per_job'])
    def metrics(weights):
        tl=sum(weights[key]*eco[key]['probability'] for key in weights)
        asp=sum(weights[key]*eco[key]['probability']*eco[key]['ASP'] for key in weights)/tl
        core=sum(weights[key]*eco[key]['probability']*eco[key]['core_RPU'] for key in weights)/tl
        return {'TLF':tl,'ASP':asp,'core_RPU':core,'allin_RPU':core+ancillary,'service_per_claim':tl*(core+ancillary)}
    for p in d['periods']:
        period=f'FY{p["fy"]}Q{p["q"]}';fleet,raw=m.stock(d,p['weights'])
        masses={key:raw[key]*correction[key] for key in raw};mass=sum(masses.values())
        weights={key:v/mass for key,v in masses.items()};states.append((mass,weights))
        for r in d['fleet']:
            key=r['body'],r['bucket'];birth=sum(v*w for v,w in zip(r['births'],p['weights']))*d['split'][r['body']]
            surviving=birth*r['survival'];claim=surviving*r['relative_claim_weight']*correction[key]
            detail.append(dict(period=period,body=['Car','SUV','Pickup','Minivan'][r['body']],age=r['age'],age_bucket=e['cohorts'][r['bucket']]['age_bucket'],blended_births_thousands=birth,survival=r['survival'],fleet_thousands=surviving,relative_claim_weight=r['relative_claim_weight'],cell_calibration_correction=correction[key],claim_mass_relative_to_CY2025=claim,claim_share=claim/mass,status='Annual sales cohort interpolation; fitted survival/claim propensity; fixed LT subtype split'))
        met=metrics(weights)
        for key,w in weights.items():
            b,k=key;x=eco[key]
            cells.append(dict(period=period,body=['Car','SUV','Pickup','Minivan'][b],age_bucket=e['cohorts'][k]['age_bucket'],claim_mass=masses[key],claim_share=w,TLF=x['probability'],total_loss_share=w*x['probability']/met['TLF'],ASP=x['ASP'],core_RPU=x['core_RPU'],allin_RPU=x['core_RPU']+ancillary))
        quarters.append(dict(period=period,fleet_thousands=fleet,old_fleet_activity_index=fleet/stock0,cohort_claim_activity_index=mass,**met))
        rr=[r for r in detail if r['period']==period]
        assert m.close(sum(r['fleet_thousands'] for r in rr),fleet)
        assert m.close(sum(r['claim_mass_relative_to_CY2025'] for r in rr),mass)
        assert m.close(sum(r['claim_share'] for r in rr),1)
        checks+=3
    bridges=[]
    for i in range(4,8):
        mass,w=states[i];oldmass,oldw=states[i-4];q=quarters[i];b=quarters[i-4]
        age={k:sum(w[bb,k] for bb in range(4)) for k in range(6)}
        oldage={k:sum(oldw[bb,k] for bb in range(4)) for k in range(6)}
        # Age changes first; within-age body composition second. Fixed cell economics.
        ageonly={(bb,k):age[k]*oldw[bb,k]/oldage[k] for bb in range(4) for k in range(6)}
        mid=metrics(ageonly);base=metrics(oldw);end=metrics(w)
        actual=d['actuals'][i-4];insurance=actual['us_service']*c['insurance_share_of_us_service_base']
        activity=mass/oldmass;agefactor=mid['service_per_claim']/base['service_per_claim'];bodyfactor=end['service_per_claim']/mid['service_per_claim']
        volume=activity*end['TLF']/base['TLF'];rpu=end['allin_RPU']/base['allin_RPU']
        activitydelta=insurance*(activity-1);agedelta=insurance*activity*(agefactor-1);bodydelta=insurance*activity*agefactor*(bodyfactor-1)
        totaldelta=insurance*(volume*rpu-1)
        oldactivity=q['old_fleet_activity_index']/b['old_fleet_activity_index']
        bridges.append(dict(period=q['period'],prior_legacy_service_musd=actual['us_service']+actual['intl_service'],assumed_insurance_base_musd=insurance,old_activity_factor=oldactivity,cohort_activity_factor=activity,age_composition_revenue_factor=agefactor,within_age_body_revenue_factor=bodyfactor,insurance_units_factor=volume,insurance_RPU_factor=rpu,activity_delta_musd=activitydelta,age_mix_delta_musd=agedelta,within_age_body_delta_musd=bodydelta,cohort_delta_musd=totaldelta,old_activity_convention_delta_musd=insurance*(oldactivity*end['service_per_claim']/base['service_per_claim']-1),status='Capture neutral; fixed economics and ancillary adoption; no measured crossover subtype trend'))
        assert m.close(activitydelta+agedelta+bodydelta,totaldelta)
        assert m.close(activity*agefactor*bodyfactor,volume*rpu)
        checks+=2
    assert m.close(sum(cw.values()),1);checks+=1
    for name,rows in [('fleet_single_age.csv',detail),('fleet_selected_cells.csv',cells),('fleet_quarterly.csv',quarters),('fleet_revenue_bridge.csv',bridges)]:m.save_csv(name,rows)
    fields=['activity_delta_musd','age_mix_delta_musd','within_age_body_delta_musd','cohort_delta_musd','old_activity_convention_delta_musd']
    summary={key:sum(r[key] for r in bridges[:2]) for key in fields}
    paths=[m.OLD,m.ECON,m.HERE/'assumptions.json',m.HERE/'fleet_cohort_build.py']
    out={'checks_passed':checks,'single_age_rows':len(detail),'selected_cell_rows':len(cells),'FY27_H1_carrier_neutral':summary,'sources':{str(p.relative_to(m.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'status':'Candidate cohort-activity adapter; not adopted forecast; no new source validation','interaction_order':'Activity, age composition, within-age body composition','limitations':['Fixed LT subtype shares across all vintages','2026/2027 sales repeat 2025','Quarterly interpolation of annual-age snapshots, not observed monthly registrations','Fitted claim propensities and age-cell correction, not measured covered exposures','Fixed repair/value/fee economics and ancillary adoption','No catastrophe, carrier or lag change','Dollar translation assumes 90% insurance share and persistent same-quarter base']}
    (m.HERE/'fleet_cohort_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
