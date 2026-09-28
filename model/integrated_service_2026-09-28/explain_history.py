"""Exact mechanical reconstruction-error bridge; not causal residual fitting."""
import csv,json,math
from pathlib import Path
P=Path(__file__).parent
with (P/'quarterly_results.csv').open() as f: rows=list(csv.DictReader(f))
with (P/'historical_controls.csv').open() as f: controls={r['period']:r for r in csv.DictReader(f)}
cfg=json.loads((P/'assumptions.json').read_text());q4=rows[3]
def v(r,k):return float(r[k])
results=[]
for r in rows[:4]:
    actual_us=v(r,'reported_us_musd');actual_int=v(r,'reported_intl_musd');actual=actual_us+actual_int
    season=v(r,'seasonality_proxy');base_us=v(q4,'us_musd')*season
    ins=v(q4,'insurance_musd')*season
    factors=[('fleet_exposure_proxy', (v(r,'claims_raw')/season)/v(q4,'claims_raw')),
             ('cohort_TLF',v(r,'TLF')/v(q4,'TLF')),
             ('carrier_capture',v(r,'effective_capture')/v(q4,'effective_capture')),
             ('insurance_RPU',v(r,'insurance_allin_RPU')/v(q4,'insurance_allin_RPU'))]
    previous=ins;bridge={'Q4_anchor_times_FY25_seasonal_proxy_less_actual':base_us-actual_us}
    for name,factor in factors:
        following=previous*factor;bridge[name]=following-previous;previous=following
    residual=v(r,'us_residual_musd')
    assert math.isclose(sum(bridge.values()),residual,abs_tol=1e-7)
    total_error=residual+v(r,'intl_residual_musd')
    implied_other=actual_us-v(r,'insurance_musd')
    results.append({'period':r['period'],'actual_us_service_musd':actual_us,'modeled_us_service_musd':v(r,'us_musd'),
      'US_error_musd':residual,'US_error_pct':100*residual/actual_us,
      'actual_total_service_musd':actual,'modeled_total_service_musd':v(r,'legacy_service_musd'),
      'total_service_error_musd':total_error,'total_service_error_pct':100*total_error/actual,
      'reported_total_company_revenue_musd':actual+v(controls[r['period']],'excluded_purchased_vehicle_revenue_musd'),
      'US_error_bridge_musd':bridge,'bridge_factors':dict(factors),
      'international_error_musd':v(r,'intl_residual_musd'),
      'diagnostic_implied_other_US_if_insurance_unchanged_musd':implied_other,
      'diagnostic_required_insurance_activity_change_pct_if_other_US_and_RPU_unchanged':100*((actual_us-v(r,'other_us_musd'))/v(r,'insurance_musd')-1),
      'warning':'Sequential arithmetic attribution, order-dependent interaction allocation; not inferred real-world causality. Q4 calibrated.'})
out={'bridge_order':['Q4 seasonal proxy','fleet exposure','cohort TLF','capture','RPU'],'results':results,
 'decision':'No assumptions changed or residual adjustments adopted. Investigate time-shape and historical capture convention before retuning damage economics.'}
(P/'historical_error_explanation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(results,indent=2))

# Small standard plot; separates US denominator from total service denominator.
from PIL import Image,ImageDraw,ImageFont
im=Image.new('RGB',(1700,720),'white');draw=ImageDraw.Draw(im)
def font(size):
    p=Path('/System/Library/Fonts/Supplemental/Arial.ttf')
    return ImageFont.truetype(str(p),size) if p.exists() else ImageFont.load_default(size=size)
draw.text((50,25),'FY2026: historical reconstruction versus reported revenue',font=font(34),fill='#243A51')
for x,color,label in [(50,'#243A51','Reported'),(260,'#d58a36','Model reconstruction')]:
    draw.rectangle((x,87,x+24,111),fill=color);draw.text((x+34,83),label,font=font(24),fill='#243A51')
for left,ak,mk,title in [(95,'actual_us_service_musd','modeled_us_service_musd','US service revenue'),(930,'actual_total_service_musd','modeled_total_service_musd','Total service revenue')]:
    draw.text((left,145),title,font=font(28),fill='#243A51')
    for tick in [0,250,500,750,1000,1250]:
        y=610-tick*.32
        draw.line((left,y,left+660,y),fill='#dce2e7',width=1)
        draw.text((left-12,y),str(tick),anchor='rm',font=font(19),fill='#526272')
    for i,r in enumerate(results):
        center=left+90+i*158;a=r[ak];b=r[mk]
        draw.rectangle((center-48,610-a*.32,center-5,610),fill='#243A51')
        draw.rectangle((center+5,610-b*.32,center+48,610),fill='#d58a36')
        y=610-max(a,b)*.32-63
        label='Calibrated' if i==3 else f'+${b-a:.1f}m\n+{100*(b/a-1):.1f}%'
        draw.multiline_text((center,y),label,anchor='ma',align='center',font=font(22),fill='#243A51',spacing=3)
        draw.text((center,625),f'Q{i+1}',anchor='ma',font=font(23),fill='#243A51')
draw.text((50,675),'USD millions. Q4 matches by construction; these are not out-of-sample forecasts.',font=font(22),fill='#526272')
im.save(P/'historical_errors.png')
