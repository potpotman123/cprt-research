"""Independent checks on active revenue inputs and saved calibration. No refit."""
import csv
import hashlib
import html
import json
import math
import re
import sys
import io
import subprocess
from collections import defaultdict
from pathlib import Path
from statistics import NormalDist

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ARCH=ROOT/'model/revenue_architecture_2026-09-28'
sys.path.insert(0,str(ARCH));import model as m


def rows(path):
    with path.open() as f:return list(csv.DictReader(x for x in f if not x.startswith('#')))


def main():
    d,e,c=m.old.load();checks=[];details={};sources=set()
    def check(name,ok,detail=None):
        if not ok:raise AssertionError(name)
        checks.append(name)
        if detail is not None:details[name]=detail
    def near(a,b,tol=1e-7):return abs(a-b)<tol
    # Parse primary HTML independently of the original source-extraction scripts.
    matched=[]
    for q,source in enumerate(d['source_paths']):
        p=Path(source);sources.add(p)
        parsed=[]
        for row in re.findall(r'<tr\b[^>]*>.*?</tr>',p.read_text(),re.S|re.I):
            txt=' '.join(html.unescape(re.sub('<[^>]+>',' ',row)).split())
            nums=[int(x.replace(',',''))/1000 for x in re.findall(r'\b\d{1,3}(?:,\d{3})+\b',txt)]
            parsed.append((txt,nums))
        for label,fields in [('Service revenues',('us_service','intl_service')),('Vehicle sales',('us_vehicle','intl_vehicle'))]:
            candidates=[v for text,v in parsed if text.startswith(label) and len(v)==6]
            expected=[d['actuals'][q][fields[0]],d['actuals'][q][fields[1]],sum(d['actuals'][q][k] for k in fields),
                      d['prior_actuals'][q][fields[0]],d['prior_actuals'][q][fields[1]],sum(d['prior_actuals'][q][k] for k in fields)]
            check(f'Q{q+1} primary filing {label}',any(all(near(a,b) for a,b in zip(v,expected)) for v in candidates))
            matched.extend(dict(period=f'FY{year}Q{q+1}',field=k,value_musd=d[ds][q][k],source=str(p.relative_to(ROOT)))
                           for year,ds in [(2026,'actuals'),(2025,'prior_actuals')] for k in fields)
    with (HERE/'financial_controls_checked.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=matched[0]);w.writeheader();w.writerows(matched)
    check('32 quarterly geography/revenue controls checked',len(matched)==32)
    check('FY26 service sum equals annual release',near(sum(x['us_service']+x['intl_service'] for x in d['actuals']),3969.520))
    check('FY25 service sum equals annual release',near(sum(x['us_service']+x['intl_service'] for x in d['prior_actuals']),3968.662))
    check('Quarter weights normalized',all(near(sum(x['weights']),1) and min(x['weights'])>=0 for x in d['periods']))
    check('Eight fiscal dates and four forecast comparisons',len(d['periods'])==8 and all(d['periods'][i+4]['fy']==d['periods'][i]['fy']+1 and d['periods'][i+4]['q']==d['periods'][i]['q'] for i in range(4)))

    agecsv=ROOT/'data/csv/ccc_tl_share_by_age_2020_2025.csv';sources.add(agecsv)
    targets={r['age_bucket']:float(r['cy2025'])/100 for r in rows(agecsv)}
    check('All six TLF targets match source CSV',all(near(r['target'],targets[r['age_bucket']]) for r in d['calibration']))
    # Recompute moments from SAVED parameters; do not import the fitting script.
    n=NormalDist();fit=[]
    for k,row in enumerate(e['cohorts']):
        tl=cost=value=0.
        for b in range(4):
            weight=e['body_weights'][str(k)][b];acv=row['car_ACV']*e['value_ratios'][b]
            mu=row['log_car_repair_median']+math.log(e['repair_ratios'][b]);sigma=row['sigma']
            lo,hi=1e-12,1-1e-12
            for _ in range(60):
                u=(lo+hi)/2
                if math.exp(mu+sigma*n.inv_cdf(u))<acv*(.616+.192*u):lo=u
                else:hi=u
            u=(lo+hi)/2
            tl+=weight*(1-u);value+=weight*(1-u)*acv
            cost+=weight*math.exp(mu+.5*sigma*sigma)*n.cdf(n.inv_cdf(u)-sigma)
        fit.append(dict(TLF=tl,selected_value=value/tl,repairable_mean=cost/(1-tl)))
    check('Saved parameters reproduce six TLFs',max(abs(fit[k]['TLF']-d['calibration'][k]['target']) for k in range(6))<1e-8)
    h=json.loads((ROOT/'docs/fleet_selection_2026-09-28/age_value_holdout_results.json').read_text())
    vals=[x['selected_value'] for x in fit[:3]]+[sum(e['TLmix'][k]*fit[k]['selected_value'] for k in range(3,6))/sum(e['TLmix'][3:])]
    check('Saved parameters reproduce four selected-value targets',max(abs(a-b) for a,b in zip(vals,h['observed_values']))<.01,vals)
    means=[]
    for group in [range(3),range(3,6)]:
        weights=[e['relative_claim_weights'][k]*(1-fit[k]['TLF']) for k in group]
        means.append(sum(w*fit[k]['repairable_mean'] for w,k in zip(weights,group))/sum(weights))
    check('Saved parameters reproduce two repaired-mean targets',max(abs(a-b) for a,b in zip(means,[5721,3682]))<.01,means)
    text=(ROOT/'raw/ccc/crash-course-2026.txt').read_text()
    check('Repair target source text includes 5721 and 2039 gap','$5,721' in text and '$2,039' in text)
    details['calibration_caveat']='Twelve in-sample targets; mixed coverage/periods. Reproduction does not validate local switching density.'

    birth=m.old.BIRTHS;sources.add(birth);byyear=defaultdict(list)
    for r in rows(birth):byyear[int(r['year'])].append(r)
    check('58 four-body birth years complete',set(byyear)==set(range(1970,2028)) and all(len(x)==4 for x in byyear.values()))
    check('Birth mapping preserves old totals',all(near(sum(float(r['births_thousands']) for r in rs),float(rs[0]['existing_car_total_thousands'])+float(rs[0]['existing_lt_total_thousands'])) for rs in byyear.values()))
    check('184 age/body fleet cells unique',len(d['fleet'])==184 and len({(r['body'],r['age']) for r in d['fleet']})==184)
    check('Survival and relative claim weights valid',all(0<=r['survival']<=1 and r['relative_claim_weight']>0 for r in d['fleet']))
    check('Carrier weights and allocation fractions valid',all(len(x['weights'])==len(x['allocations'])==8 and all(v>=0 for v in x['weights']) and all(0<=v<=1 for v in x['allocations']) for x in d['carriers']))
    for entry in d['manifests']:
        p=Path(entry['path']);sources.add(p)
        check('Saved extraction source hash: '+p.name,p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'])

    fees=ROOT/'data/csv/copart_fee_grid_2026-09.csv';sources.add(fees)
    check('Embedded fee grid equals saved CSV',rows(fees)==d['fees'],{'rows':len(d['fees'])})
    for i,g in enumerate(m.old.fee_grids(d)):
        check('Selected fee grid '+str(i)+' lower bounds unique',len({float(r['band_low_usd']) for r in g})==len(g))
        check('Selected fee grid '+str(i)+' ordered and no cent gaps',all(near(float(a['band_high_usd'])+.01,float(b['band_low_usd'])) for a,b in zip(g,g[1:])))
    paths=[m.old.OLD,m.old.ECON,birth,m.LEGACY/'assumptions.json',ARCH/'scenario_configs.json',ARCH/'model.py',m.LEGACY/'engine.py',fees]
    sources.update(paths)
    # Manifest integrity for active model snapshots only; archives may intentionally differ.
    for p,key in [(ARCH/'manifest.json','sources'),(ROOT/'model/aftermarket_bridge_2026-09-29/manifest.json','source_hashes')]:
        z=json.loads(p.read_text());check('Active manifest '+p.parent.name,all((ROOT/k).exists() and hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in z[key].items()))
    bm=json.loads((ARCH/'evidence_manifest.json').read_text());jpm=Path(bm['jpm_source']);sources.add(jpm)
    check('Named JPM extraction source hash',jpm.exists() and hashlib.sha256(jpm.read_bytes()).hexdigest()==bm['jpm_sha256'])
    check('Annual benchmark identity and rounding retained',near(bm['jpm_fy27_service_musd']+bm['jpm_fy27_purchased_musd'],bm['jpm_fy27_total_musd']) and near(bm['rounding_difference_musd'],1))
    # Already-rerun source outputs must be byte-identical apart from fingerprints.
    before=json.loads((HERE/'before_hashes.json').read_text())['files']
    outputs=['model/revenue_architecture_2026-09-28/quarterly_scenarios.csv','model/revenue_architecture_2026-09-28/scenario_summary.csv',
             'model/aftermarket_bridge_2026-09-29/quarterly_results.csv','model/aftermarket_bridge_2026-09-29/scenario_summary.csv',
             'model/aftermarket_bridge_2026-09-29/direct_shock_grid.csv','model/aftermarket_bridge_2026-09-29/materiality_hurdle.json']
    check('Four aftermarket output files reproduce byte for byte',all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==before[k] for k in outputs[2:]))
    # Original core files used a different floating-point evaluation environment.
    # Compare numbers and text fields, preserving the observed residual explicitly.
    revision=json.loads((HERE/'before_hashes.json').read_text())['base_commit'];maxdiff=0.
    for k in outputs[:2]:
        oldtext=subprocess.check_output(['git','show',revision+':'+k],cwd=ROOT,text=True)
        check('Pre-audit core snapshot equals recorded Git source '+Path(k).name,hashlib.sha256(oldtext.encode()).hexdigest()==before[k])
        aa=list(csv.DictReader(io.StringIO(oldtext)));bb=rows(ROOT/k)
        check('Core output rows/columns unchanged '+Path(k).name,len(aa)==len(bb) and aa[0].keys()==bb[0].keys())
        for a,b in zip(aa,bb):
            for key in a:
                if a[key]==b[key]:continue
                try:x,y=float(a[key]),float(b[key])
                except ValueError:raise AssertionError('Changed text: '+key)
                maxdiff=max(maxdiff,abs(x-y))
                if not math.isclose(x,y,rel_tol=1e-10,abs_tol=1e-7):raise AssertionError('Changed result: '+key)
    check('All core scenario values reproduce within numerical tolerance',True,{'largest_absolute_numeric_difference':maxdiff,'note':'Includes both units and USD-million fields; no material difference'})
    details['primary_sources_visual_review']=['CCC 2026 Figure 19: six CY2025 TLF labels','CCC Q4 2025 Figure 6: four selected values and age mix']
    details['scope_limit']='All live input families traced; no exhaustive re-verification of every upstream raw observation or archived experiment. Carrier workbook hash, not independent formula recomputation. No new independent causal validation.'
    manifest=[]
    for p in sorted(sources):
        try:name=str(p.relative_to(ROOT))
        except ValueError:name=str(p)
        manifest.append(dict(path=name,exists=p.exists(),sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None))
    result=dict(as_of='2026-09-29',scope='Revenue only',passed=len(checks),checks=checks,details=details)
    (HERE/'audit_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'source_hashes.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
