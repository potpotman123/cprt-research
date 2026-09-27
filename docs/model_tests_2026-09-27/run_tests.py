"""Bounded local model diagnostics. No downloads, workbook changes or fitted new evidence."""
import contextlib, io, json, math, runpy, hashlib
from pathlib import Path
from statistics import NormalDist
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
with contextlib.redirect_stdout(io.StringIO()):
    v=runpy.run_path(str(ROOT/'model/service_revenue_2026-09-27/validate_live.py'))
d=v['d']; cdf=v['cdf']; bucket=v['bucket']; buyer=v['buyer']; sales=v['sales']; repairs=v['repairs']; sigma=d['repair']['inherited_sigma']
bodies=range(4); ages=range(46); years=range(2023,2028)
base=dict(us_growth=v['ug'],intl_growth=v['ig'],insured=.9,acv=[1,1.5,1.5,1.5],repair=repairs,salvage=.3,seller=.04,sigma=sigma,car_stretch=1.270,lt_stretch=1.099,decay=.09027,car_value=10000,price_decay=.1,birth_growth=0.)
def bridge(pot,par):
    growth=[None]*4+[pot[j]/pot[j-4]-1 for j in range(4,12)]
    ans=[]
    for j in range(4):
        old=d['actuals'][4+j];B=old['us_service']*(1+par['us_growth'])
        adjustment=B/(1+par['insured']*growth[7])*par['insured']*(growth[8+j]-growth[7])
        intl=old['intl_service']*(1+par['intl_growth'])
        ans.append(dict(total=B+adjustment+intl,adjustment=adjustment,growth=growth[8+j]))
    return ans
def model(par):
    stock={}
    for y in years:
        for b in bodies:
            for a in ages:
                z=a/(par['car_stretch'] if b==0 else par['lt_stretch']);lo=math.floor(z)
                key='survival_cars' if b==0 else 'survival_light_trucks'
                surv=0 if z>=31 else float(d['survival'][lo][key])+(z-lo)*(float(d['survival'][lo+1][key])-float(d['survival'][lo][key]))
                birth=sales[y-a][0] if b==0 else sales[y-a][1]*v['split'][b-1]
                if y-a>2025:birth*=(1+par['birth_growth'])**(y-a-2025)
                stock[y,b,a]=birth*surv
    claim=lambda a:(.5 if a==0 else 1)*math.exp(-par['decay']*max(a-6,0))
    offset=[math.log((par['acv'][b]/par['acv'][0])/(par['repair'][b]/par['repair'][0]))/par['sigma'] for b in bodies]
    prob={}
    for k in range(6):
        wt=[sum(stock[2025,b,a]*claim(a) for a in ages if bucket(a)==k) for b in bodies];lo,hi=-8,8
        for _ in range(60):
            z=(lo+hi)/2;avg=sum(w*cdf(z-offset[b]) for b,w in enumerate(wt))/sum(wt)
            if avg<float(d['ccc'][k]['cy2025'])/100:lo=z
            else:hi=z
        for b in bodies:prob[k,b]=cdf(z-offset[b])
    fee={};unit={};econ={}
    for b in bodies:
        for a in ages:
            bid=par['car_value']*math.exp(-par['price_decay']*(a-10))*par['acv'][b]*par['salvage']
            fee[b,a]=sum(w*buyer(bid*m) for w,m in zip([.25,.5,.25],[.5,1,1.5]))+par['seller']*bid
            unit[b,a]=claim(a)*prob[bucket(a),b];econ[b,a]=unit[b,a]*fee[b,a]
    q=[{(b,a):sum(stock[y,b,a]*wt for y,wt in zip(years,period['weights'])) for b in bodies for a in ages} for period in d['periods']]
    pot=[sum(s[k]*econ[k] for k in econ) for s in q]
    return dict(forecast=bridge(pot,par),q=q,econ=econ,unit=unit,fee=fee,pot=pot,prob=prob)
ref=model(base)
for j,r in enumerate(ref['forecast']):assert abs(r['total']-v['forecasts'][j]['total_service_m'])<1e-7
h1=lambda m:sum(r['total'] for r in m['forecast'][:2])
cases=[]
def test(name,param,low,high,definition):
    for side,x in [('low',low),('high',high)]:
        p={**base,param:x};m=model(p)
        cases.append(dict(driver=name,case=side,setting=x,definition=definition,h1_delta_m=h1(m)-h1(ref),quarter_delta_m=[r['total']-s['total'] for r,s in zip(m['forecast'],ref['forecast'])]))
test('US baseline growth','us_growth',base['us_growth']-.01,base['us_growth']+.01,'Minus/plus 1 percentage point in all forecast quarters; no historical change')
test('International baseline growth','intl_growth',base['intl_growth']-.01,base['intl_growth']+.01,'Minus/plus 1 percentage point in all forecast quarters')
test('SUV pre-loss value ratio','acv',[1,1.2,1.5,1.5],[1,1.8,1.5,1.5],'SUV/car 1.20x or 1.80x versus 1.50x; historical and forecast economics recalibrated')
test('All LT repair costs','repair',[repairs[0]]+[x*.9 for x in repairs[1:]],[repairs[0]]+[x*1.1 for x in repairs[1:]],'All non-car costs minus/plus 10%; CCC buckets recalibrated')
test('Gross salvage recovery','salvage',.25,.35,'25%/35% across all bodies versus 30%; common threshold change absorbed in age calibration')
test('Insured service exposure','insured',.8,1.,'80%/100% versus assumed 90%')
test('Latent repair dispersion','sigma',sigma*.8,sigma*1.2,'Minus/plus 20%; CCC buckets recalibrated')
test('LT survival stretch','lt_stretch',1.099*.95,1.099*1.05,'Minus/plus 5%; hypothetical structural refit, not a six-month mortality shock')
test('Claim age decay','decay',.09027*.8,.09027*1.2,'Minus/plus 20%; hypothetical structural refit')
test('Age-10 car value','car_value',8000,12000,'Minus/plus 20%; all body dollar values scale, same historical/forecast fee convention')
test('Future vehicle births','birth_growth',-.1,.1,'CY26 and CY27 births compound -10%/+10% annually from CY25; historical cohorts fixed')
test('Seller fee rate','seller',.02,.06,'2%/6% versus 4%, applied to modeled history and forecast; no repricing event')
# Exact joint factorization fleet N * P(age) * P(body|age). Freeze at Q4FY26.
anchor=ref['q'][7];N0=sum(anchor.values());age0={a:sum(anchor[b,a] for b in bodies)/N0 for a in ages}
cond0={(b,a):anchor[b,a]/sum(anchor[k,a] for k in bodies) if sum(anchor[k,a] for k in bodies) else 0 for b in bodies for a in ages}
worlds={}
for age_live,body_live in [(False,False),(True,False),(False,True),(True,True)]:
    pots=[];units=[]
    for q in ref['q']:
        N=sum(q.values());aa={a:sum(q[b,a] for b in bodies)/N for a in ages}
        cc={(b,a):q[b,a]/sum(q[k,a] for k in bodies) if sum(q[k,a] for k in bodies) else cond0[b,a] for b in bodies for a in ages}
        cell={(b,a):N*(aa[a] if age_live else age0[a])*(cc[b,a] if body_live else cond0[b,a]) for b in bodies for a in ages}
        pots.append(sum(cell[k]*ref['econ'][k] for k in cell));units.append(sum(cell[k]*ref['unit'][k] for k in cell))
    name=f'age_{int(age_live)}_body_{int(body_live)}'
    worlds[name]=dict(forecast=bridge(pots,base),unit_yoy=[units[j]/units[j-4]-1 for j in range(8,12)],rpu_yoy=[(pots[j]/units[j])/(pots[j-4]/units[j-4])-1 for j in range(8,12)])
for j in range(4):assert abs(worlds['age_1_body_1']['forecast'][j]['total']-ref['forecast'][j]['total'])<1e-7
parts=[]
for j in range(4):
    adj={k:w['forecast'][j]['adjustment'] for k,w in worlds.items()}
    size=adj['age_0_body_0'];age=adj['age_1_body_0']-size;body=adj['age_0_body_1']-size
    interaction=adj['age_1_body_1']-size-age-body
    assert abs(size+age+body+interaction-ref['forecast'][j]['adjustment'])<1e-8
    parts.append(dict(quarter=d['periods'][8+j]['label'],fleet_size_m=size,age_m=age,body_given_age_m=body,interaction_m=interaction,total_m=ref['forecast'][j]['adjustment']))
# Mechanical stress: a new forecast-period within-cohort TLF shift; not an existing workbook input.
shock=[]
for pp in [-.01,.01]:
    pots=[]
    for j,q in enumerate(ref['q']):
        pots.append(sum(q[b,a]*v['exposure'](a)*max(0,min(1,ref['prob'][bucket(a),b]+(pp if j>=8 else 0)))*ref['fee'][b,a] for b in bodies for a in ages))
    rr=bridge(pots,base);shock.append(dict(tlf_shift_pp=pp*100,h1_delta_m=sum(r['total'] for r in rr[:2])-h1(ref)))
# Distinguish new forecast-period economics from refitting permanent assumptions.
timing=[]
for ratio in [1.2,1.8]:
    new_econ=dict(ref['econ'])
    for a in ages:
        z=NormalDist().inv_cdf(ref['prob'][bucket(a),0])
        p=cdf(z-math.log(ratio/(repairs[1]/repairs[0]))/sigma)
        bid=10000*math.exp(-.1*(a-10))*ratio*.3
        fee=sum(w*buyer(bid*m) for w,m in zip([.25,.5,.25],[.5,1,1.5]))+.04*bid
        new_econ[1,a]=v['exposure'](a)*p*fee
    pots=[sum(q[k]*(new_econ[k] if j>=8 else ref['econ'][k]) for k in q) for j,q in enumerate(ref['q'])]
    rr=bridge(pots,base)
    timing.append(dict(suv_value_ratio=ratio,h1_delta_m=sum(r['total'] for r in rr[:2])-h1(ref),meaning='SUV pre-loss value changes only in forecast; car severity calibration fixed; constant recovery fraction; no insurer or demand response'))
# Toy damage selection at age 10. Calibrate latent car repair distribution once to baseline car P.
# No claim this unobserved lognormal is an empirical repair distribution.
nd=NormalDist();target=ref['prob'][4,0];mu=math.log(10000*(1-.3*(1-.04)))+sigma*nd.inv_cdf(target)
selection=[]
for n in [2001,8001]:
    for slope in [0.,.2,.4]:
        for suv_value in [1.2,1.5]:
            outputs=[]
            for b,value_ratio in [(0,1.),(1,suv_value)]:
                count=rev=recovery=cost=0.
                for i in range(n):
                    u=(i+.5)/n;repair=math.exp(mu+sigma*nd.inv_cdf(u))*repairs[b]/repairs[0]
                    recover=.3+slope*(.5-u);acv=10000*value_ratio;bid=acv*recover
                    if repair>acv-bid*(1-.04):
                        count+=1;recovery+=recover;cost+=repair
                        rev+=sum(w*buyer(bid*m) for w,m in zip([.25,.5,.25],[.5,1,1.5]))+.04*bid
                outputs.append(dict(tlf=count/n,mean_recovery_given_total=recovery/count,rpu=rev/count,revenue_per_claim=rev/n))
            selection.append(dict(nodes=n,recovery_slope=slope,suv_value_ratio=suv_value,car=outputs[0],suv=outputs[1],suv_car_revenue_ratio=outputs[1]['revenue_per_claim']/outputs[0]['revenue_per_claim']))
for a in selection[:6]:
    b=next(x for x in selection[6:] if x['recovery_slope']==a['recovery_slope'] and x['suv_value_ratio']==a['suv_value_ratio'])
    assert abs(a['suv_car_revenue_ratio']-b['suv_car_revenue_ratio'])<.003
result=dict(baseline=ref['forecast'],h1_service_m=h1(ref),sensitivities=cases,attribution=parts,counterfactual_worlds=worlds,new_tlf_shock=shock,forecast_only_value_tests=timing,selection=selection,input_sha256=hashlib.sha256((ROOT/'model/service_revenue_2026-09-27/model_inputs.json').read_bytes()).hexdigest())
(P/'results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:result[k] for k in ['h1_service_m','attribution','new_tlf_shock']},indent=2))
print('Sensitivity H1 $m:',[(x['driver'],x['case'],round(x['h1_delta_m'],4)) for x in cases])
print('Selection ratios:',[(x['recovery_slope'],x['suv_value_ratio'],round(x['suv_car_revenue_ratio'],4)) for x in selection if x['nodes']==8001])
print('Forecast-only value changes:',timing)
