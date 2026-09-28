"""Bounded historical falsification and proxy transmission, not a FY27 forecast."""
import csv,hashlib,json,math
from statistics import mean
import engine as m

def main():
    d,e,c=m.load();N=m.N;grids=m.fee_grids(d);nodes=c['fee_integration_nodes']
    weights={(b,k):e['relative_claim_weights'][k]*e['body_weights'][str(k)][b] for b in range(4) for k in range(6)}
    z=sum(weights.values());weights={key:v/z for key,v in weights.items()}
    cp=m.ROOT/'data/csv/cprt_cpi_three_series.csv'
    with cp.open() as f:series={r['date']:r for r in csv.DictReader(f)}
    fields=['CUUR0000SETD','CUUR0000SETA02']
    def ratio(year,months):
        good=[mo for mo in months if all(series.get(f'{y}-{mo:02}',{}).get(key) for y in [year-1,year] for key in fields)]
        if not good:raise ValueError('No compatible observed months')
        return {key:mean(float(series[f'{year}-{mo:02}'][key]) for mo in good)/mean(float(series[f'{year-1}-{mo:02}'][key]) for mo in good) for key in fields},good
    hist,hmonths=ratio(2025,range(1,13));recent,rmonths=ratio(2026,[4,5,6]);assert rmonths==[4,5,6]
    ratespath=m.ROOT/'data/csv/ccc_tl_share_by_age_2020_2025.csv'
    with ratespath.open() as f:rates={r['age_bucket']:r for r in csv.DictReader(l for l in f if not l.startswith('#'))}
    ccc=[.996,1.019,1.023,1.01,1.01,1.01] # Reported repairable means; deliberately unvalidated latent-cost transfer.
    def evaluate(repair,value,salvage=1):
        cells=[];age=[];repaired={k:[0.,0.] for k in range(6)}
        for (b,k),w in weights.items():
            row=e['cohorts'][k];acv=row['car_ACV']*e['value_ratios'][b]*(value[k] if isinstance(value,list) else value)
            mu=row['log_car_repair_median']+math.log(e['repair_ratios'][b]*repair[k]);sigma=row['sigma']
            lo,hi=1e-12,1-1e-12
            for _ in range(44):
                u=(lo+hi)/2;threshold=acv*(1-salvage*(.4-.2*u)*(1-c['seller_fee_fraction']))
                if threshold<=0:raise ValueError('Invalid net salvage threshold')
                if mu+sigma*N.inv_cdf(u)<math.log(threshold):lo=u
                else:hi=u
            u=(lo+hi)/2;p=1-u;buyer=0
            for j in range(nodes):
                rank=u+p*(j+.5)/nodes;price=acv*salvage*(.4-.2*rank)
                buyer+=((1-c['preferred_buyer_fraction'])*m.fee(price,grids[0])+c['preferred_buyer_fraction']*m.fee(price,grids[1])+m.fee(price,grids[2])+c['gate_environment_fee'])/nodes
            asp=acv*salvage*(.3-.1*u);rpu=buyer+c['seller_fee_fraction']*asp
            cells.append(dict(body=b,age=k,weight=w,TLF=p,ASP=asp,core_RPU=rpu))
            repaired[k][0]+=w*u
            repaired[k][1]+=w*math.exp(mu+sigma*sigma/2)*N.cdf(N.inv_cdf(u)-sigma)
        for k in range(6):
            part=[r for r in cells if r['age']==k];total=sum(r['weight'] for r in part)
            age.append(dict(age_bucket=e['cohorts'][k]['age_bucket'],TLF=sum(r['weight']*r['TLF'] for r in part)/total,repairable_mean=repaired[k][1]/repaired[k][0]))
        units=sum(r['weight']*r['TLF'] for r in cells);rev=sum(r['weight']*r['TLF']*r['core_RPU'] for r in cells)
        return dict(TLF=units,core_RPU=rev/units,core_revenue_per_reference_claim=rev,ASP=sum(r['weight']*r['TLF']*r['ASP'] for r in cells)/units),age
    base,baseages=evaluate([1]*6,1)
    scenarios={
        'CY2024_backcast_broad_CPI':([1/hist[fields[0]]]*6,1/hist[fields[1]],1),
        'CY2024_backcast_CCC_repairable_mean_proxy':([1/x for x in ccc],1/hist[fields[1]],1),
        'CY2024_backcast_7plus_CCC_joint_proxy':([1,1,1,1/1.01,1/1.01,1/1.01],[1,1,1,1/.995,1/.995,1/.995],1),
        'CY2026Q2_broad_CPI_transmission_only':([recent[fields[0]]]*6,recent[fields[1]],1),
        'salvage_recovery_plus_1pct_unobserved_diagnostic':([1]*6,1,1.01)}
    outcomes={};agechecks=[];count=0
    for name,(repair,value,salvage) in scenarios.items():
        result,ages=evaluate(repair,value,salvage)
        old,new=(result,base) if 'backcast' in name else (base,result)
        change={key:100*(new[key]/old[key]-1) for key in ['TLF','core_RPU','core_revenue_per_reference_claim','ASP']}
        change['TLF_change_pp']=100*(new['TLF']-old['TLF'])
        assert m.close((1+change['TLF']/100)*(1+change['core_RPU']/100),1+change['core_revenue_per_reference_claim']/100);count+=1
        outcomes[name]={'direction':'2024 proxy to calibrated 2025' if 'backcast' in name else 'Apply observed broad-index ratios or hypothetical salvage shock to fixed calibration; not dated forecast','change_pct':change,'repair_multipliers':repair,'vehicle_value_multiplier':value,'salvage_multiplier':salvage,'model_result':result}
        if 'backcast' in name:
            for a,b in zip(ages,baseages):
                if '7plus' in name and a['age_bucket'] in [x['age_bucket'] for x in baseages[:3]]:continue
                target=float(rates[a['age_bucket']]['cy2024'])/100
                agechecks.append(dict(case=name,age_bucket=a['age_bucket'],reported_2024_TLF=target,model_2024_TLF=a['TLF'],residual_2024_pp=100*(a['TLF']-target),reported_2025_TLF=b['TLF'],reported_change_pp=100*(b['TLF']-target),modeled_change_pp=100*(b['TLF']-a['TLF']),model_repairable_mean_growth_pct=100*(b['repairable_mean']/a['repairable_mean']-1)))
    filing=[]
    for k,a in enumerate(baseages):
        rr=rates[a['age_bucket']];p0=float(rr['cy2024'])/100;p1=float(rr['cy2025'])/100
        removal=1-p0/p1
        filing.append(dict(age_bucket=a['age_bucket'],TLF_2024=p0,TLF_2025=p1,required_fraction_of_initial_claims_removed=removal if removal>=0 else None,required_fraction_of_initial_repairables_removed=removal/(1-p0) if removal>=0 else None,total_loss_count_change=0 if removal>=0 else None,status='Pure small-repairable removal can reproduce rate arithmetically; not an observed filing estimate' if removal>=0 else 'Pure removal cannot explain a falling TLF'))
        if removal>=0:assert m.close(p0/(1-removal),p1);count+=1
    # Native model equivalence and equal repair/value scale invariance.
    native=m.economics(d,e,c,1,1)
    assert m.close(base['TLF'],sum(weights[key]*native[key]['probability'] for key in weights));count+=1
    assert m.close(base['core_RPU'],sum(weights[key]*native[key]['probability']*native[key]['core_RPU'] for key in weights)/base['TLF']);count+=1
    scaled,_=evaluate([1.05]*6,1.05);assert m.close(scaled['TLF'],base['TLF']);count+=1
    for name,rows in [('within_age_backcast.csv',agechecks),('within_age_filing_alternative.csv',filing)]:m.save_csv(name,rows)
    paths=[cp,ratespath,m.ECON,m.HERE/'assumptions.json',m.HERE/'within_age_economics.py',m.ROOT/'raw/ccc/crash-course-2026.txt',m.ROOT/'docs/fleet_selection_2026-09-28/ccc_2026_figure22.webp']
    out={'status':'Proxy falsification and transmission only; no forecast adoption or causal fit','weights':'Fixed CY2025 calibration age/body claims; vintage mix and carrier changes excluded to isolate within-group economics','baseline':base,'CPI_2025_vs_2024_matched_months':{'months':hmonths,'ratios':hist,'note':'Annual comparison uses only matched months; not full-year growth if any month missing'},'CPI_2026Q2_vs_2025Q2':{'months':rmonths,'ratios':recent},'CCC_repairable_mean_growth_by_age':ccc,'CCC_source':'raw/ccc/crash-course-2026.txt line 277; repairable-only, not constant-damage latent repair costs','CCC_older_value_proxy':{'ratio':.995,'source':'Saved CCC annual Figure22 footnote visually checked: 7+ adjusted valuations -0.5% CY2025 versus 2024, noncomprehensive','limitation':'Selected total-loss values, not unconditional matched vehicle values; applied equally within 7+ by assumption; younger cohorts held fixed in this diagnostic only'},'salvage_evidence':'No compatible within-age recovery history identified in current inputs; isolated 1% shock is explicitly hypothetical. Copart aggregate ASP is a selected outcome, not an exogenous recovery driver.','cases':outcomes,'checks_passed':count,'sources':{str(p.relative_to(m.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    (m.HERE/'within_age_economics_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['sources']},indent=2))

if __name__=='__main__':main()
