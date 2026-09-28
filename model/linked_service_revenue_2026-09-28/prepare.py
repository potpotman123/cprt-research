"""Bounded existing-file extraction; no network or spreadsheet authoring."""
import json, math, hashlib, csv
from pathlib import Path
from statistics import NormalDist
import openpyxl

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).parent
oldpath=ROOT/'model/service_revenue_2026-09-27/model_inputs.json'
d=json.loads(oldpath.read_text())
sharepath=Path('/Users/kwu/Library/Messages/Attachments/53/03/CDE4DBC0-6774-4ABD-860B-E12504CAF220/CPRT_share_sidebuild.xlsx')
w=openpyxl.load_workbook(sharepath,data_only=True,read_only=True)
s=w.worksheets[0]
carriers=[]
for i in range(10):
    carriers.append({'name':s.cell(108+i,1).value,'weights':[s.cell(108+i,c).value for c in range(4,12)],'allocations':[s.cell(130+i,c).value for c in range(4,12)],'weight_cells':f'D{108+i}:K{108+i}','allocation_cells':f'D{130+i}:K{130+i}'})
w.close()
sales={int(r['year']):[float(r['cars_k']),float(r['light_trucks_k'])] for r in d['sales']}
sales[2026]=sales[2025];sales[2027]=sales[2025]
split=[1,.409/.565,.109/.565,.047/.565]
def surv(a,b):
    z=a/([1.270,1.099,1.099,1.099][b])
    if z>=31:return 0
    lo=int(z);key='survival_cars' if b==0 else 'survival_light_trucks'
    return float(d['survival'][lo][key])+(z-lo)*(float(d['survival'][lo+1][key])-float(d['survival'][lo][key]))
def bucket(a):return 0 if a==0 else 1 if a<=3 else 2 if a<=6 else 3 if a<=9 else 4 if a<=12 else 5
fleet=[]
for b in range(4):
 for a in range(46):
    fleet.append({'body':b,'age':a,'bucket':bucket(a),'survival':surv(a,b),'relative_claim_weight':(.5 if a==0 else 1)*math.exp(-.09027*max(a-6,0)),'births':[sales[y-a][int(b>0)] for y in range(2023,2028)]})
# Fixed historical calibration: joint severity/recovery model, not measured latent costs.
sigma=d['repair']['inherited_sigma']; repair=[d['repair']['body_average_cost_usd'][b]/3682 for b in ['Car','SUV','Pickup','Minivan']]
values=[1,1.128,1.493,1.0];ages=[0,2,5,8,11,17];N=NormalDist()
def probability(mu,b,k):
    acv=10000*math.exp(-.1*(ages[k]-10))*values[b]
    p=0
    for j in range(9):
        low=j/9; high=(j+1)/9; recovery=.3+.2*(.5-(j+.5)/9)
        threshold=acv*(1-recovery*(1-.04))
        cut=N.cdf((math.log(threshold)-mu-math.log(repair[b]))/sigma)
        p+=max(0,high-max(low,cut))
    return p
calibration=[]
for k in range(6):
    weights=[sum(r['births'][2]*r['survival']*split[b]*r['relative_claim_weight'] for r in fleet if r['body']==b and r['bucket']==k) for b in range(4)]
    target=float(d['ccc'][k]['cy2025'])/100
    lo,hi=0,15
    for _ in range(70):
        mid=(lo+hi)/2
        got=sum(weights[b]*probability(mid,b,k) for b in range(4))/sum(weights)
        if got<target:lo=mid
        else:hi=mid
    mu=(lo+hi)/2
    calibration.append({'age_bucket':d['ccc'][k]['age_bucket'],'representative_age':ages[k],'target':target,'log_repair_median':mu,'reproduced':sum(weights[b]*probability(mu,b,k) for b in range(4))/sum(weights)})
evidence=[
 ['E01','US / international service revenue','Reported','FY25–FY26 fiscal quarters','SEC earnings releases; segment_service_rev_8k.csv','No insurance revenue split disclosed here','Use as historical controls'],
 ['E02','Carrier weights','Proxy','FY26–FY27','Friend workbook Base engine rows 108–117','Auto premium/share proxy; not measured claim weights','Replace with compatible exposure and frequency evidence'],
 ['E03','Carrier allocation','Assumed path','FY26–FY27','Friend workbook Base engine rows 130–139','Probability-weighted estimates; original quotes not reverified','No separate aggregate share haircut'],
 ['E04','Fleet births and survival','Source + fitted transfer','1970–2027','Legacy input snapshot / ORNL / FRED','2026–27 births flat; historical LT split held constant','Need cohort-specific crossover births'],
 ['E05','Relative claims by age','Fitted assumption','All modeled periods','Legacy age decay 0.09027','Not insured exposure or claim frequency','Absolute scale calibrated once'],
 ['E06','Total-loss age targets','Reported with population caveat','CY2025','CCC Crash Course Figure 19','Annual age targets; not carrier-specific','Latent damage calibration fitted once'],
 ['E07','Body repair ratios','Assumption-driven estimate','2026 working case','AAA + CRSS + CCC working repair analysis','Modern scenarios transferred to older claims','Retain scope and population limitations'],
 ['E08','SUV / pickup value ratios','Retail proxy assumption','2016 model-year panel','value_recovery_audit/README.md','1.128 and 1.493 not matched insurer ACV','Base scenario, not measured premiums'],
 ['E09','Severity and salvage relationship','Assumed','All modeled periods','9 severity intervals; recovery 30% +/- 10pp','Not observed damaged-vehicle recovery curve','Do not claim validated damage selection'],
 ['E10','Buyer fee grid','Observed snapshot','2026-09-26','copart_fee_grid_2026-09.csv','Standard/preferred mix assumed; not historical grids','Historical reconstruction uses current schedule'],
 ['E11','Seller fee rate','Analyst assumption','All modeled periods','Barclays illustration uses 4%','Not executed carrier terms','Rates separately editable by carrier'],
 ['E12','Title service adoption and price','Illustrative assumption','All modeled periods','Usage 50%; fee $50; not disclosed','Management confirms contribution, not the decomposition','Flat future use; no presumed saturation'],
 ['E13','Delivery uptake and price','Illustrative assumption','All modeled periods','Usage 10%; revenue $300; not disclosed','Not inferred from transport costs','Flat future use; new product scope unverified'],
 ['E14','US insurance revenue weight','Assumed','FY26Q4','90% retained legacy working assumption','Not the global 81% insurance unit disclosure','Material allocation uncertainty'],
 ['E15','Other-US service activity','Coarse assumed build','FY26Q4–FY27','Noninsurance + referral + other service residual','Activity-equivalent counts, not reported sold units','Separate actual channels when measured'],
 ['E16','International service activity','Coarse assumed build','FY26Q4–FY27','Country mix combined; unit/fee/FX controls','No imported US fee grid','Requires country fee and activity evidence'],
 ['E17','Recognition timing','Reported historical policy','FY2025 10-K','Revenue Recognition / Service revenues','Auction-related services recognized at auction; access separate','Check new product/standalone arrangements'],
 ['E18','Sale timing','Neutral assumption','All modeled periods','Same-quarter conversion 100% initially','Friend ramp may already describe sales; timing unverified','No second lag until scope resolved'],
 ['E19','Direct-buy referral fees','Management disclosure','FY26Q1 call lines 183–190','Referral fee replaces some owned-vehicle processing','Fees can arise without Copart inventory/sold units','Other-US activity branch, not insurer units'],
 ['E20','Consensus service forecast','Missing','FY27 quarters','No comparable dated consensus series loaded','Never substitute our old revenue growth baseline','Comparison remains unavailable']]
payload={'periods':d['periods'][4:],'actuals':d['actuals'][4:],'prior_actuals':d['actuals'][:4],'carriers':carriers,'fleet':fleet,'split':split,'repair_ratios':repair,'value_ratios':values,'sigma':sigma,'calibration':calibration,'fees':d['fees'],'sales':d['sales'],'survival':d['survival'],'evidence':evidence,'source_paths':d['source_paths'],'manifests':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [oldpath,sharepath]],'share_source':str(sharepath)}
(OUT/'inputs.json').write_text(json.dumps(payload,indent=2))
with (OUT/'evidence_register.csv').open('w') as f:
    wr=csv.writer(f);wr.writerow(['id','input','status','period','source','limitation','treatment']);wr.writerows(evidence)
print(json.dumps({'cohorts':24,'damage_rows':24*9*8,'carriers':10,'periods':8,'calibration_max_error':max(abs(x['target']-x['reproduced']) for x in calibration),'source_files':len(payload['manifests'])}))
