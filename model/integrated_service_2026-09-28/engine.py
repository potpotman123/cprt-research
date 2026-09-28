"""Integrated service-revenue research model; standard library, no Excel/network."""
import bisect,calendar,csv,hashlib,json,math
from pathlib import Path
from statistics import NormalDist

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];N=NormalDist()
OLD=ROOT/'model/linked_service_revenue_2026-09-28/inputs.json'
ECON=ROOT/'docs/fleet_selection_2026-09-28/age_constrained_engine_results.json'
ACQ=ROOT/'data/csv/acv_14d9_projections.csv'
def load():return json.loads(OLD.read_text()),json.loads(ECON.read_text()),json.loads((HERE/'assumptions.json').read_text())
def close(a,b):return math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7)
def validate_config(c):
    if c['timing_mode']!='sale_equivalent_no_additional_lag':raise ValueError('Physical inventory requires assignment-based capture, opening cohorts and exits; not silently enabled.')
    if c['claims_mode']!='fleet_exposure_proxy_times_reported_frequency':raise ValueError('Unsupported claims convention')
    for key,vals in c['quarter_drivers'].items():
        if len(vals)!=8 or any(v is None or not math.isfinite(v) or v<=0 for v in vals):raise ValueError('Missing/invalid driver: '+key)
    for key in ['insurance_share_of_us_service_base','routing_fraction','insurance_consignment_fraction','preferred_buyer_fraction','seller_fee_fraction']:
        if not 0<=c[key]<=1:raise ValueError(key)
    for product in ['title','delivery']:
        for m in c['quarter_drivers'][product+'_adoption_multiplier']:
            if not 0<=c[product]['adoption']*m<=1:raise ValueError(product+' adoption')
    if c['fee_integration_nodes']<16:raise ValueError('Insufficient fee integration')

def cutoff(mu,acv,sigma,seller):
    lo,hi=1e-12,1-1e-12
    for _ in range(44):
        u=(lo+hi)/2;threshold=acv*(1-(.4-.2*u)*(1-seller))
        if mu+sigma*N.inv_cdf(u)<math.log(threshold):lo=u
        else:hi=u
    return (lo+hi)/2

def fee_grids(d):
    def g(kind,preferred=False):
        return sorted([r for r in d['fees'] if (('high' in r['page']) if preferred else r['page']=='non-licensed') and r['title_group']=='non-clean' and r['vehicle_class']=='standard' and r['fee_type']==kind and (kind!='buyer_fee' or r['payment_method']=='secured')],key=lambda r:float(r['band_low_usd']))
    grids=[g('buyer_fee'),g('buyer_fee',True),g('virtual_bid_pre_bid')]
    if not all(grids):raise ValueError('Missing fee schedule')
    return grids
def fee(price,grid):
    i=bisect.bisect_right([float(r['band_low_usd']) for r in grid],price)-1
    if i<0:raise ValueError('Price below fee schedule')
    r=grid[i];return float(r['fee_usd'] or 0)+price*float(r['fee_pct'] or 0)/100

def economics(d,e,c,repair,value):
    std,pref,virtual=fee_grids(d);out={}
    for k,row in enumerate(e['cohorts']):
        for b in range(4):
            acv=row['car_ACV']*e['value_ratios'][b]*value
            mu=row['log_car_repair_median']+math.log(e['repair_ratios'][b]*repair)
            u=cutoff(mu,acv,row['sigma'],c['seller_fee_fraction']);prob=1-u
            buyer=0.;nodes=c['fee_integration_nodes']
            for j in range(nodes):
                rank=u+prob*(j+.5)/nodes;price=acv*(.4-.2*rank)
                buyer+=((1-c['preferred_buyer_fraction'])*fee(price,std)+c['preferred_buyer_fraction']*fee(price,pref)+fee(price,virtual)+c['gate_environment_fee'])/nodes
            asp=acv*(.3-.1*u);seller=c['seller_fee_fraction']*asp
            out[b,k]={'probability':prob,'ACV':acv,'ASP':asp,'buyer_RPU':buyer,'seller_RPU':seller,'core_RPU':buyer+seller}
    return out

def stock(d,weights):
    fleet=0.;raw={(b,k):0. for b in range(4) for k in range(6)}
    for r in d['fleet']:
        qty=sum(v*w for v,w in zip(r['births'],weights))*r['survival']*d['split'][r['body']]
        fleet+=qty;raw[r['body'],r['bucket']]+=qty*r['relative_claim_weight']
    return fleet,raw

def run(d,e,c):
    validate_config(c);drivers=c['quarter_drivers'];base=c['base_period_index'];historical=[]
    stock0,raw0=stock(d,[0,0,1,0,0])
    cw0={(b,k):e['relative_claim_weights'][k]*e['body_weights'][str(k)][b] for b in range(4) for k in range(6)}
    norm=sum(cw0.values());cw0={key:v/norm for key,v in cw0.items()}
    seasonal_us=[r['us_service']/d['prior_actuals'][3]['us_service'] for r in d['prior_actuals']]
    seasonal_int=[r['intl_service']/d['prior_actuals'][3]['intl_service'] for r in d['prior_actuals']]
    cache={};quarters=[];cohort_rows=[];carrier_rows=[]
    for p,period in enumerate(d['periods']):
        fy,q=period['fy'],period['q'];fq=f'FY{fy}Q{q}';sf,raw=stock(d,period['weights'])
        adjusted={key:cw0[key]*raw[key]/raw0[key] for key in cw0}
        z=sum(adjusted.values());weights={key:v/z for key,v in adjusted.items()}
        assert close(sum(weights.values()),1)
        # Scale is applied later once; fleet totals and composition are separate.
        claims=sf/stock0*seasonal_us[q-1]*drivers['reported_claim_frequency'][p]
        key=(drivers['repair_cost'][p],drivers['vehicle_value'][p])
        if key not in cache:cache[key]=economics(d,e,c,*key)
        eco=cache[key];carrier_total=sum(x['weights'][p if p<4 else base] for x in d['carriers'])
        capture=0.
        for x in d['carriers']:
            wi=x['weights'][p if p<4 else base]/carrier_total
            allocation=x['allocations'][p if p<4 or x['name']=='Progressive' else base]
            capture+=wi*allocation
            carrier_rows.append({'period':fq,'carrier':x['name'],'total_loss_weight_proxy':wi,'allocation':allocation,'capture_contribution':wi*allocation,'status':'Historical inherited path' if p<4 else 'PGR path only; other Q4 weights/allocations fixed'})
        sold=core=buyer=seller=proceeds=losses=0.
        for (b,k),weight in weights.items():
            x=eco[b,k];tl=claims*weight*x['probability'];units=tl*c['routing_fraction']*capture*c['insurance_consignment_fraction']
            losses+=tl;sold+=units;core+=units*x['core_RPU'];buyer+=units*x['buyer_RPU'];seller+=units*x['seller_RPU'];proceeds+=units*x['ASP']
            cohort_rows.append({'period':fq,'body':b,'age_bucket':e['cohorts'][k]['age_bucket'],'claim_weight':weight,'claim_equivalent_raw':claims*weight,'TLF':x['probability'],'total_losses_raw':tl,'fee_sales_raw':units,'selected_ACV':x['ACV'],'ASP':x['ASP'],'buyer_RPU':x['buyer_RPU'],'seller_RPU':x['seller_RPU'],'core_revenue_raw':units*x['core_RPU']})
        title_jobs=sold*c['title']['adoption']*drivers['title_adoption_multiplier'][p]
        title=title_jobs*c['title']['net_incremental_fee']*(not c['title']['included_in_seller_fee'])
        delivery_jobs=sold*c['delivery']['adoption']*drivers['delivery_adoption_multiplier'][p]
        delivery_gross=delivery_jobs*c['delivery']['gross_external_revenue_per_job']
        waiver=delivery_jobs*c['delivery']['fee_waiver_per_job']
        quarters.append({'period':fq,'end':period['end'],'claims_raw':claims,'total_losses_raw':losses,'fee_sales_raw':sold,'effective_capture':capture,'TLF':losses/claims,'ASP':proceeds/sold,'core_RPU':core/sold,'title_jobs_raw':title_jobs,'delivery_jobs_raw':delivery_jobs,'buyer_raw':buyer,'seller_raw':seller,'title_raw':title,'delivery_gross_raw':delivery_gross,'delivery_waiver_raw':waiver,'insurance_raw':core+title+delivery_gross-waiver,'seasonality_proxy':seasonal_us[q-1]})
    insurance_base=d['actuals'][base]['us_service']*1e6*c['insurance_share_of_us_service_base']
    scale=insurance_base/quarters[base]['insurance_raw']
    otherbase=d['actuals'][base]['us_service']*1e6*(1-c['insurance_share_of_us_service_base'])
    intlbase=d['actuals'][base]['intl_service']*1e6
    for p,r in enumerate(quarters):
        q=d['periods'][p]['q'];fy=d['periods'][p]['fy']
        r['normalized_fee_sales']=r['fee_sales_raw']*scale
        r['normalized_claims']=r['claims_raw']*scale
        r['normalized_title_jobs']=r['title_jobs_raw']*scale;r['normalized_delivery_jobs']=r['delivery_jobs_raw']*scale
        for key in ['buyer','seller','title','delivery_gross','delivery_waiver','insurance']:r[key+'_musd']=r[key+'_raw']*scale/1e6
        r['insurance_allin_RPU']=r['insurance_musd']*1e6/r['normalized_fee_sales']
        r['other_us_activity_equivalent']=otherbase/c['other_us_revenue_per_activity_equivalent']*seasonal_us[q-1]*drivers['other_us_activity'][p]
        r['other_us_musd']=r['other_us_activity_equivalent']*c['other_us_revenue_per_activity_equivalent']*drivers['other_us_fee'][p]/1e6
        r['intl_activity_equivalent']=intlbase/c['intl_revenue_per_activity_equivalent']*seasonal_int[q-1]*drivers['intl_activity'][p]
        r['intl_musd']=r['intl_activity_equivalent']*c['intl_revenue_per_activity_equivalent']*drivers['intl_fee'][p]*drivers['intl_fx'][p]/1e6
        r['us_musd']=r['insurance_musd']+r['other_us_musd'];r['legacy_service_musd']=r['us_musd']+r['intl_musd']
        r['reported_us_musd']=d['actuals'][p]['us_service'] if p<4 else None
        r['reported_intl_musd']=d['actuals'][p]['intl_service'] if p<4 else None
        r['us_residual_musd']=r['us_musd']-r['reported_us_musd'] if p<4 else None
        r['intl_residual_musd']=r['intl_musd']-r['reported_intl_musd'] if p<4 else None
        r['presentation_status']='Historical reconstruction, not reported operating units' if p<4 else 'Provisional assumption-driven projection'
        r['physical_opening_inventory']=None;r['physical_ending_inventory']=None
        r['acquired_service_musd']=None;r['consolidated_service_musd']=None
        assert close(r['insurance_musd'],r['buyer_musd']+r['seller_musd']+r['title_musd']+r['delivery_gross_musd']-r['delivery_waiver_musd'])
        assert close(r['normalized_fee_sales']*r['insurance_allin_RPU']/1e6,r['insurance_musd'])
        assert close(r['legacy_service_musd'],r['us_musd']+r['intl_musd'])
    assert close(quarters[base]['us_musd'],d['actuals'][base]['us_service'])
    assert close(quarters[base]['intl_musd'],d['actuals'][base]['intl_service'])
    return {'quarters':quarters,'cohorts':cohort_rows,'carriers':carrier_rows,'claim_scale':scale,'historical_age_claim_weights':cw0}

def acquisition_rows(d,c):
    with ACQ.open() as f: projections={int(r['fiscal_year'][:4]):float(r['revenue_musd']) for r in csv.DictReader(l for l in f if not l.startswith('#'))}
    start=c['acquisition']['first_consolidated_month_assumption'];fraction=c['acquisition']['classified_service_fraction'];elim=c['acquisition']['intercompany_eliminations_musd'];rows=[]
    if fraction is not None and not 0<=fraction<=1:raise ValueError('Acquired service fraction')
    for p in d['periods']:
        first=(p['fy']-1)*12+7+(p['q']-1)*3;months=[divmod(first+i,12) for i in range(3)]
        active=[(y,m+1) for y,m in months if f'{y}-{m+1:02}' >= start]
        revenue=sum(projections[y]/12 for y,m in active)
        service=0. if not active else None if fraction is None or elim is None else revenue*fraction-elim
        if service is not None and (service<0 or service>revenue):raise ValueError('Invalid acquired service bridge')
        rows.append({'period':f'FY{p["fy"]}Q{p["q"]}','active_months':len(active),'management_total_revenue_musd':revenue,'classified_service_musd':service,'status':'Timing assumption; management total not service revenue; classification/eliminations gate'})
    return rows

def save_csv(name,rows):
    with (HERE/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
    d,e,c=load();result=run(d,e,c);acq=acquisition_rows(d,c)
    for r,a in zip(result['quarters'],acq):
        r['acquired_service_musd']=a['classified_service_musd']
        r['consolidated_service_musd']=None if a['classified_service_musd'] is None else r['legacy_service_musd']+a['classified_service_musd']
    save_csv('quarterly_results.csv',result['quarters']);save_csv('cohort_engine.csv',result['cohorts']);save_csv('carrier_allocation.csv',result['carriers']);save_csv('acquisition_gate.csv',acq)
    controls=[]
    for rows in [d['prior_actuals'],d['actuals']]:
        for r in rows:
            controls.append({'period':f'FY{r["fy"]}Q{r["q"]}','end':r['end'],'us_service_musd':r['us_service'],'intl_service_musd':r['intl_service'],'legacy_service_musd':r['us_service']+r['intl_service'],'excluded_purchased_vehicle_revenue_musd':r['us_vehicle']+r['intl_vehicle'],'source':r['source'],'status':'Reported dollar control; insurance split not disclosed here'})
    save_csv('historical_controls.csv',controls)
    paths=[OLD,ECON,HERE/'assumptions.json',ACQ,HERE/'engine.py']
    manifest={'version':c['version'],'scope':c['scope'],'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'normalization':{'period':'FY26Q4','claim_scale':result['claim_scale'],'observed_absolute_units':False},'unresolved':['Claims/population compatibility','Coverage and true exposure','Service base decomposition','Within-old-age values and salvage recovery','Carrier path not observed assignment share','Acquired service classification'], 'structural_status':'Legacy model connected with explicit assumptions; no predictive validation claimed.'}
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'quarters':len(result['quarters']),'cohort_rows':len(result['cohorts']),'legacy_complete':True,'postclose_consolidated_available':False,'historical_us_residuals':[r['us_residual_musd'] for r in result['quarters'][:4]]}))
if __name__=='__main__':main()
