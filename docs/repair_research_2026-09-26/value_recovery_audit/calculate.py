from pathlib import Path
import csv,json,statistics,hashlib,datetime
p=Path(__file__).parent
# Manual transcription of live KBB national Fair Purchase Price tables, accessed 2026-09-26.
# Include all listed nonhybrid sedan trims for Camry, all sedan trims for Accord,
# all nonhybrid RAV4 trims, all CR-V trims and all SuperCrew F150 trims/bed lengths.
# These are equal-trim descriptive checks, NOT fleet-weighted class estimates.
panels={
'Camry':('Car','https://www.kbb.com/toyota/camry/2016/',{'LE':13500,'SE':13100,'SE Special Edition':13550,'XSE':14550,'XLE':14200}),
'Accord':('Car','https://www.kbb.com/honda/accord/2016/',{'LX Sedan':12900,'Sport Sedan':13650,'EX Sedan':13750,'EX-L Sedan':13200,'Touring Sedan':14550}),
'RAV4':('Crossover','https://www.kbb.com/toyota/rav4/2016/',{'LE':15400,'XLE':15650,'SE':16250,'Limited':16550}),
'CR-V':('Crossover','https://www.kbb.com/honda/cr-v/2016/',{'LX':13500,'SE':14400,'EX':14700,'EX-L':15600,'Touring':16500}),
'F150 SuperCrew':('Pickup','https://www.kbb.com/ford/f150-supercrew-cab/2016/',{'XL 6.5':14350,'XL 5.5':16150,'XLT 5.5':18150,'XLT 6.5':19400,'King Ranch 6.5':21100,'Platinum 6.5':22500,'Lariat 6.5':21200,'Lariat 5.5':21300,'King Ranch 5.5':23600,'Platinum 5.5':24000,'Limited 5.5':23100})}
rows=[];stats={}
for name,(body,url,vals) in panels.items():
 for trim,value in vals.items():rows.append(dict(model_year=2016,model=name,body=body,trim=trim,fair_purchase_price_usd=value,url=url,access_date='2026-09-26',status='published retail proxy; not insurer ACV or salvage proceeds'))
 stats[name]={'mean':statistics.mean(vals.values()),'median':statistics.median(vals.values()),'n_trims':len(vals)}
car=statistics.mean(stats[m]['mean'] for m in ('Camry','Accord'))
crossover=statistics.mean(stats[m]['mean'] for m in ('RAV4','CR-V'))
for name in stats:stats[name]['ratio_to_two_sedan_mean']=stats[name]['mean']/car
with (p/'kbb_2016_panel.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
historical={'Sedan':(7351.28,10.46),'SUV':(9329.23,10.12),'Pickup':(9879.70,12.03),'Van':(5837.79,11.15)}
out={'status':'AUDIT CHECKS; NO NEW VALIDATED FLEET-WIDE OR AUCTION RATIO','kbb_models':stats,'equal_model_sedan_mean':car,'equal_model_crossover_mean':crossover,'crossover_ratio':crossover/car,'pickup_ratio':stats['F150 SuperCrew']['mean']/car,'historical_2013Q3':{k:{'ACV':v[0],'average_age':v[1],'ratio_to_sedan':v[0]/historical['Sedan'][0]} for k,v in historical.items()},'mechanical_example_NOT_DATA':{'ACV_ratio':1.5,'car_gross_and_net_recovery_fraction_assumed':.3,'LT_gross_and_net_recovery_fraction_assumed':.4,'auction_price_ratio':1.5*.4/.3,'economic_threshold_ratio':1.5*(1-.4)/(1-.3)}}
(p/'results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
manifest={str(x.relative_to(p)):hashlib.sha256(x.read_bytes()).hexdigest() for x in p.rglob('*') if x.is_file() and x.name!='manifest.json'}
(p/'manifest.json').write_text(json.dumps(manifest,indent=2))
