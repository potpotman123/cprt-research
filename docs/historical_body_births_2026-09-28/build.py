"""Keep EPA source shares separate from a provisional sales-cohort mapping."""
import csv,json,re,hashlib,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
raw=json.loads((HERE/'epa_public_table.json').read_text())
source=ROOT/'data/csv/light_vehicle_sales_by_year.csv'
sales={int(r['year']):r for r in csv.DictReader(line for line in source.read_text().splitlines() if not line.startswith('#'))}
types=['Sedan/Wagon','Car SUV','Truck SUV','Pickup','Minivan/Van']
byyear={};source_rows=[]
for r in raw['rows']:
    year=int(re.search(r'\d{4}',r[2]['text']).group());typ=r[1]['text'];value=r[3]['number']
    byyear.setdefault(year,{})[typ]=value
    source_rows.append({'model_year':year,'source_year_label':r[2]['text'],'regulatory_class':r[0]['text'],'vehicle_type':typ,'production_share':value,'source_status':'final' if year<=2024 else 'preliminary label; numeric value unavailable in retrieved table','source_url':raw['source_url']})
shares=[];maxerr=0
for year,values in sorted(byyear.items()):
    if any(values[t] is None for t in types):
        shares.append(dict(model_year=year,sedan_share=None,suv_share=None,pickup_share=None,van_share=None,suv_within_non_sedan=None,pickup_within_non_sedan=None,van_within_non_sedan=None,status='Unavailable; not zero'))
        continue
    err=abs(sum(values[t] for t in types)-1);maxerr=max(maxerr,err)
    assert err<1e-5
    assert abs(values['Sedan/Wagon']+values['Car SUV']-values['All Car'])<1e-5
    assert abs(values['Truck SUV']+values['Pickup']+values['Minivan/Van']-values['All Truck'])<1e-5
    suv=values['Car SUV']+values['Truck SUV'];den=suv+values['Pickup']+values['Minivan/Van']
    shares.append(dict(model_year=year,sedan_share=values['Sedan/Wagon'],suv_share=suv,pickup_share=values['Pickup'],van_share=values['Minivan/Van'],suv_within_non_sedan=suv/den,pickup_within_non_sedan=values['Pickup']/den,van_within_non_sedan=values['Minivan/Van']/den,status='Final EPA model-year US-market production mix; SUV combines both regulatory classes'))
available={r['model_year']:r for r in shares if r['suv_share'] is not None}
oldsplit=[.409/.565,.109/.565,.047/.565];mapped=[]
for year in range(min(sales),2028):
    base=sales[min(year,2025)];car=float(base['cars_k']);lt=float(base['light_trucks_k'])
    if year<1975: split=oldsplit;mixyear=None;mixstatus='Inherited fixed subtype assumption; no EPA year'
    else:
        mixyear=min(year,2024);s=available[mixyear]
        split=[s['suv_within_non_sedan'],s['pickup_within_non_sedan'],s['van_within_non_sedan']]
        mixstatus='Same-numbered MY mix transferred to CY sales (proxy)' if year<=2024 else 'Hold final MY2024 mix; 2025 table unavailable; assumption'
    assert math.isclose(sum(split),1,abs_tol=1e-12)
    counts=[car]+[lt*w for w in split]
    for b,count in zip(['Car','SUV','Pickup','Van'],counts):
        mapped.append(dict(year=year,body=b,births_thousands=count,existing_car_total_thousands=car,existing_lt_total_thousands=lt,mix_source_model_year=mixyear,mix_status=mixstatus,total_status='Existing sales input' if year<=2025 else 'Hold existing 2025 total; assumption',mapping_status='Candidate only: preserve existing car/LT totals; EPA non-sedan subtype shares are a transfer proxy, not observed category sales'))
    assert math.isclose(sum(counts),car+lt,abs_tol=1e-8)
def write(name,rows):
    with (HERE/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
write('epa_source_shares.csv',source_rows);write('body_mix_by_model_year.csv',shares);write('candidate_body_births.csv',mapped)
out={'source_rows':len(source_rows),'final_years':len(available),'range':[min(available),max(available)],'missing_preliminary_years':[r['model_year'] for r in shares if r['suv_share'] is None],'max_share_sum_rounding_error':maxerr,'candidate_birth_rows':len(mapped),'totals_preserved':True,'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,HERE/'epa_public_table.json',HERE/'build.py']},'samples':[available[y] for y in [2000,2005,2010,2015,2020,2024]],'production_integration':False}
(HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
