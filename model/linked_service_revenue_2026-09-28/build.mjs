import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const dir=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(dir,'../..'),out=path.join(root,'outputs/cprt-linked-20260928');
await fs.mkdir(out,{recursive:true});
const d=JSON.parse(await fs.readFile(path.join(dir,'inputs.json'),'utf8'));
const wb=Workbook.create(),names=['RPM Summary','Volume Build','Vehicle Economics','Revenue Bridge','Assumptions','Fleet Engine','Damage Engine','Carrier Engine','Source Data','Fee Data','Evidence','Checks'];
const ss=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));
const body=['Car','SUV / crossover','Pickup','Van'],cols=['D','E','F','G','H','I','J','K'];
const num='#,##0.0;(#,##0.0);"-"',pct='0.0%;(0.0%);"-"',integer='#,##0;(#,##0);"-"';
const col=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
function V(n,a,v){ss[n].getRange(a).values=[[v]];}
function F(n,a,f){ss[n].getRange(a).formulas=[[f]];ss[n].getRange(a).format.font.color=n==='RPM Summary'?'#111111':f.includes('!')?'#008000':'#111111';}
function R(n,a,v){ss[n].getRange(a).values=v;}
function input(n,a,v,fmt=num){V(n,a,v);ss[n].getRange(a).format={font:{color:'#0000FF'},fill:'#FFF4D6'};ss[n].getRange(a).setNumberFormat(fmt);}
function base(n,title,last=50,end='K'){
 let s=ss[n];s.showGridLines=false;s.getRange(`A1:${end}${last}`).format={font:{name:'Arial',size:10},rowHeight:19,verticalAlignment:'center'};
 s.getRange(`A1:B${last}`).format.columnWidth=2;s.getRange(`C1:C${last}`).format.columnWidth=43;s.getRange(`D1:${end}${last}`).format.columnWidth=14;
 s.getRange(`D6:${end}${last}`).setNumberFormat(num);V(n,'C2',title);s.getRange(`C2:${end}2`).format={font:{bold:true,size:14},rowHeight:24,borders:{bottom:{style:'thin',color:'#243A51'}}};
 s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(3);
}
function note(n,r,text,end='K'){V(n,`C${r}`,text);ss[n].getRange(`C${r}:${end}${r}`).merge();ss[n].getRange(`C${r}:${end}${r}`).format={wrapText:true,rowHeight:30,font:{size:10,color:'#555555'}};}
function header(n,r,values,start=2){let a=ss[n].getRangeByIndexes(r-1,start,1,values.length);a.values=[values];a.format={fill:'#243A51',font:{bold:true,color:'#FFFFFF'},rowHeight:30,wrapText:true};}
function section(n,r,label){V(n,`C${r}`,label);ss[n].getRange(`C${r}:K${r}`).format={fill:'#E7EBEF',font:{bold:true},borders:{top:{style:'thin',color:'#A4ACB4'},bottom:{style:'thin',color:'#A4ACB4'}}};}
function total(n,r){ss[n].getRange(`C${r}:K${r}`).format={font:{bold:true},borders:{top:{style:'thin',color:'#243A51'},bottom:{style:'double',color:'#243A51'}}};}
function periods(n){header(n,5,['Fiscal quarter',...d.periods.map(p=>`Q${p.q}:${String(p.fy).slice(2)}${p.fy===2026?'A':'E'}`)]);}
function label(n,r,text){V(n,`C${r}`,text);}
function row(n,r,text,fs,format=num){label(n,r,text);fs.forEach((f,i)=>F(n,cols[i]+r,f));ss[n].getRange(`D${r}:K${r}`).setNumberFormat(format);}

base('Source Data','Source records and extracted inputs',338,'N');periods('Source Data');
for(let i=0;i<4;i++){V('Source Data',cols[i]+'8',d.actuals[i].us_service);V('Source Data',cols[i]+'9',d.actuals[i].intl_service);V('Source Data',cols[i]+'10',d.actuals[i].us_service+d.actuals[i].intl_service);V('Source Data',cols[i]+'12',d.prior_actuals[i].us_service);V('Source Data',cols[i]+'13',d.prior_actuals[i].intl_service);}
[['8','US service revenue ($m)'],['9','International services ($m)'],['10','Total service revenue ($m)'],['12','Prior-year US services ($m)'],['13','Prior-year international ($m)']].forEach(([r,l])=>label('Source Data',r,l));
header('Source Data',16,['Period','2023 weight','2024 weight','2025 weight','2026 weight','2027 weight']);R('Source Data','C17:H24',d.periods.map(p=>[p.label,...p.weights]));ss['Source Data'].getRange('D17:H24').setNumberFormat(pct);
header('Source Data',28,['Body ID','Age','Age bucket','2023 births','2024 births','2025 births','2026 births','2027 births']);
R('Source Data','C29:J212',d.fleet.map(r=>[r.body,r.age,r.bucket,...r.births]));
header('Source Data',28,['Age','Car survival','LT survival'],11);R('Source Data','L29:N60',d.survival.map(r=>[+r.age,+r.survival_cars,+r.survival_light_trucks]));ss['Source Data'].getRange('M29:N60').setNumberFormat(pct);
header('Source Data',216,['Age bucket','Representative age','CCC target','Fitted log repair median','Calibration result']);R('Source Data','C217:G222',d.calibration.map(r=>[r.age_bucket,r.representative_age,r.target,r.log_repair_median,r.reproduced]));ss['Source Data'].getRange('E217:E222').setNumberFormat(pct);ss['Source Data'].getRange('G217:G222').setNumberFormat(pct);
note('Source Data',225,'Births come from the existing ORNL/FRED snapshot. CY2026–27 births hold CY2025 levels. Historical body splits are assumptions.');
note('Source Data',227,'CCC targets: CY2025 age buckets. Log repair medians fitted once using baseline values and recovery; not observed claims costs.');
note('Source Data',229,'Service dollars: data/csv/segment_service_rev_8k.csv and FY2026 releases in raw/sec/8k. Units are $millions.');
note('Source Data',231,'Carrier rows: supplied share workbook, Base engine rows 108–117 and 130–139, columns D:K. Estimates, not observed exposure.');
header('Source Data',249,['Period ID','Carrier','Auto-share proxy','Copart allocation']);R('Source Data','C250:F329',d.periods.flatMap((p,i)=>d.carriers.map(c=>[i,c.name,c.weights[i],c.allocations[i]])));ss['Source Data'].getRange('E250:F329').setNumberFormat(pct);

base('Fee Data','Buyer fee schedules — September 2026',68,'M');
const grid=t=>d.fees.filter(r=>r.page===(t==='std'?'non-licensed':'licensed-high-volume')&&r.title_group==='non-clean'&&r.vehicle_class==='standard'&&r.fee_type==='buyer_fee'&&r.payment_method==='secured');
let standard=grid('std'),preferred=grid('pref');
if(!preferred.length){const pages=[...new Set(d.fees.map(r=>r.page))];preferred=d.fees.filter(r=>/high/.test(r.page)&&r.title_group==='non-clean'&&r.vehicle_class==='standard'&&r.fee_type==='buyer_fee'&&r.payment_method==='secured');if(!preferred.length)throw Error('Preferred fee page missing: '+pages);}
const virtual=d.fees.filter(r=>r.page==='non-licensed'&&r.title_group==='non-clean'&&r.vehicle_class==='standard'&&r.fee_type==='virtual_bid_pre_bid');
header('Fee Data',5,['Bid lower','Standard fixed','Standard rate','Preferred fixed','Preferred rate']);
if(standard.length!==preferred.length)throw Error('Fee bands differ; explicit join needed');
R('Fee Data',`C6:G${5+standard.length}`,standard.map((r,i)=>{if(r.band_low_usd!==preferred[i].band_low_usd)throw Error('Misaligned bands');return [+r.band_low_usd,+(r.fee_usd||0),+(r.fee_pct||0)/100,+(preferred[i].fee_usd||0),+(preferred[i].fee_pct||0)/100]}));
ss['Fee Data'].getRange(`E6:E${5+standard.length}`).setNumberFormat(pct);ss['Fee Data'].getRange(`G6:G${5+standard.length}`).setNumberFormat(pct);
header('Fee Data',5,['Prebid lower','Prebid fee'],8);R('Fee Data',`I6:J${5+virtual.length}`,virtual.map(r=>[+r.band_low_usd,+r.fee_usd]));V('Fee Data','I20','Gate');V('Fee Data','J20',95);V('Fee Data','I21','Environment');V('Fee Data','J21',15);
note('Fee Data',57,'Source: data/csv/copart_fee_grid_2026-09.csv. Non-clean title, standard vehicle, secured payment, prebid.');
note('Fee Data',59,'Schedule mix is assumed. Clean titles, heavy vehicles and unsecured payments require separate inputs if material.');

base('Assumptions','Research assumptions — editable, not adopted forecasts',88);periods('Assumptions');
const globals=[[7,'US insurance share of service dollars',.9,'E14'],[8,'Car ACV at age 10 ($)',10000,'E08'],[9,'Annual age depreciation rate',.1,'E08'],[10,'Log repair dispersion',d.sigma,'E09'],[11,'Midpoint gross salvage / ACV',.3,'E09'],[12,'Recovery slope across severity',.2,'E09'],[13,'Auction routing fraction',1,'Embedded routing assumption'],[14,'Preferred buyer-fee share',.5,'E10'],[15,'Title-service fee ($)',50,'E12'],[16,'Delivery revenue per job ($)',300,'E13'],[17,'Other-US revenue per activity ($)',500,'E15'],[18,'International revenue per activity ($)',750,'E16'],[19,'Car survival stretch',1.270,'E04'],[20,'LT survival stretch',1.099,'E04'],[21,'Age claim-weight decay',.09027,'E05']];
for(const[r,l,v,e]of globals){label('Assumptions',r,l);input('Assumptions','D'+r,v,[7,9,11,12,13,14].includes(r)?pct:num);V('Assumptions','F'+r,e);}
note('Assumptions',23,'Amber inputs are working assumptions. No saturation, repair inflation, price inflation or claims decline is imposed by default.');
note('Assumptions',25,'Insurance dollar share and service prices set the calibrated level. Absolute modeled units are not independently observed.');
const per=[[30,'Claim-frequency multiplier',1],[31,'Coverage / filing multiplier',1],[32,'Within-quarter sale conversion',1],[33,'Title use among eligible sold units',.5],[34,'Delivery use among sold units',.1],[35,'Repair-cost level',1],[36,'Pre-loss-value level',1],[37,'Buyer-fee schedule multiplier',1],[38,'Title-service price multiplier',1],[39,'Delivery-price multiplier',1],[40,'Other-US activity multiplier',1],[41,'Other-US fee multiplier',1],[42,'International activity multiplier',1],[43,'International fee multiplier',1],[44,'International FX multiplier',1],[45,'Additional CAT claim fraction',0]];
section('Assumptions',28,'Quarterly operating drivers');for(const[r,l,v]of per){label('Assumptions',r,l);cols.forEach(c=>input('Assumptions',c+r,v,[32,33,34,45].includes(r)?pct:num));}
note('Assumptions',48,'Other-US activity includes noninsurance auctions, referrals and other services. International is aggregated. Flat levels are neutral placeholders.');
note('Assumptions',50,'Timing starts at 100% within-quarter conversion to avoid imposing a second lag on the friend’s potentially sale-based allocation ramps.');
header('Assumptions',54,['Body','Repair / car','Value / car','LT split','Exposure adjustment']);
for(let b=0;b<4;b++){V('Assumptions','C'+(55+b),body[b]);[d.repair_ratios[b],d.value_ratios[b],d.split[b],1].forEach((v,j)=>input('Assumptions',col(3+j)+(55+b),v,j===2?pct:num));}
note('Assumptions',60,'SUV 1.128x and pickup 1.493x values are small-panel retail proxies; van 1.00x is assumed. None is matched insurer ACV.');
header('Assumptions',64,['Carrier','Seller rate','Title-use factor','Claim-weight factor']);
d.carriers.forEach((c,i)=>{V('Assumptions','C'+(65+i),c.name);input('Assumptions','D'+(65+i),.04,pct);input('Assumptions','E'+(65+i),1);input('Assumptions','F'+(65+i),1);});
note('Assumptions',77,'Seller rates use an analyst illustration, not contracts. Carrier title-use factors are neutral, not measured adoption.');
header('Assumptions',80,['Comparison: total services ($m)',...d.periods.map(p=>p.label)]);cols.forEach(c=>V('Assumptions',c+'81','n.a.'));note('Assumptions',83,'No compatible current consensus series loaded. Enter sourced quarterly service-revenue estimates to enable the comparison.');

base('Fleet Engine','Fleet and relative claim exposure',252,'AD');
header('Fleet Engine',5,['Body ID','Age','Bucket ID','Relative claims','Survival',...['2023 stock','2024 stock','2025 stock','2026 stock','2027 stock'],...d.periods.map(p=>p.label)]);
for(let i=0;i<184;i++){
 const r=6+i,src=29+i,b=d.fleet[i].body,ar=55+b;
 F('Fleet Engine','C'+r,`='Source Data'!C${src}`);F('Fleet Engine','D'+r,`='Source Data'!D${src}`);F('Fleet Engine','E'+r,`='Source Data'!E${src}`);
 F('Fleet Engine','F'+r,`=IF(D${r}=0,0.5,1)*EXP(-'Assumptions'!$D$21*MAX(D${r}-6,0))`);
 const z=`D${r}/'Assumptions'!$D$${b===0?19:20}`,sc=b===0?'M':'N';
 F('Fleet Engine','G'+r,`=IF(${z}>=31,0,INDEX('Source Data'!$${sc}$29:$${sc}$60,INT(${z})+1)+(${z}-INT(${z}))*(INDEX('Source Data'!$${sc}$29:$${sc}$60,MIN(32,INT(${z})+2))-INDEX('Source Data'!$${sc}$29:$${sc}$60,INT(${z})+1)))`);
 for(let y=0;y<5;y++)F('Fleet Engine',col(7+y)+r,`='Source Data'!${col(5+y)}${src}*G${r}*'Assumptions'!$F$${ar}*'Assumptions'!$G$${ar}`);
 for(let p=0;p<8;p++){F('Fleet Engine',col(12+p)+r,`=SUMPRODUCT(H${r}:L${r},'Source Data'!D${17+p}:H${17+p})`);F('Fleet Engine',col(22+p)+r,`=${col(12+p)}${r}*F${r}`);}
}
header('Fleet Engine',193,['Body ID','Bucket ID','Representative age',...d.periods.map(p=>p.label)]);
for(let b=0;b<4;b++)for(let k=0;k<6;k++){let r=194+b*6+k;V('Fleet Engine','C'+r,b);V('Fleet Engine','D'+r,k);F('Fleet Engine','E'+r,`='Source Data'!D${217+k}`);for(let p=0;p<8;p++)F('Fleet Engine',col(5+p)+r,`=SUMIFS(${col(22+p)}$6:${col(22+p)}$189,$C$6:$C$189,C${r},$E$6:$E$189,D${r})`);}
note('Fleet Engine',221,'Stocks are in thousands; weighted claim exposure is a relative quantity. A single base-period calibration supplies the claims scale.','M');
note('Fleet Engine',223,'Historical LT splits use a listed-pool proxy for all vintages. Carrier-specific age/body mixes are not measured and remain identical.','M');
ss['Fleet Engine'].getRange('C1:E252').format.columnWidth=12;ss['Fleet Engine'].getRange('F1:AD252').format.columnWidth=13;

base('Carrier Engine','Carrier weights and Copart allocation',115,'N');header('Carrier Engine',5,['Period ID','Carrier','Auto share','Claim factor','Raw weight','Claim share','Copart alloc','Assigned share','Seller rate','Title-use factor']);
for(let p=0;p<8;p++)for(let i=0;i<10;i++){
 let r=6+p*10+i,sr=250+p*10+i,ar=65+i,lo=6+p*10,hi=lo+9;
 F('Carrier Engine','C'+r,`='Source Data'!C${sr}`);F('Carrier Engine','D'+r,`='Source Data'!D${sr}`);F('Carrier Engine','E'+r,`='Source Data'!E${sr}`);F('Carrier Engine','F'+r,`='Assumptions'!F${ar}`);F('Carrier Engine','G'+r,`=E${r}*F${r}`);F('Carrier Engine','H'+r,`=G${r}/SUM(G${lo}:G${hi})`);F('Carrier Engine','I'+r,`='Source Data'!F${sr}`);F('Carrier Engine','J'+r,`=H${r}*I${r}`);F('Carrier Engine','K'+r,`='Assumptions'!D${ar}`);F('Carrier Engine','L'+r,`=MIN(1,'Assumptions'!${cols[p]}33*'Assumptions'!E${ar})`);
}
header('Carrier Engine',90,['Period','Copart share','Seller rate / sold','Title use / sold','Claim-share sum']);
for(let p=0;p<8;p++){let r=91+p,lo=6+p*10,hi=lo+9;V('Carrier Engine','C'+r,d.periods[p].label);F('Carrier Engine','D'+r,`=SUM(J${lo}:J${hi})`);F('Carrier Engine','E'+r,`=SUMPRODUCT(J${lo}:J${hi},K${lo}:K${hi})/D${r}`);F('Carrier Engine','F'+r,`=SUMPRODUCT(J${lo}:J${hi},L${lo}:L${hi})/D${r}`);F('Carrier Engine','G'+r,`=SUM(H${lo}:H${hi})`);}
ss['Carrier Engine'].getRange('E6:L85').setNumberFormat(pct);ss['Carrier Engine'].getRange('D91:G98').setNumberFormat(pct);ss['Carrier Engine'].getRange('C1:C115').format.columnWidth=17;ss['Carrier Engine'].getRange('D1:D115').format.columnWidth=36;
note('Carrier Engine',101,'Allocation paths imported as editable source estimates. No extra Progressive or aggregate-share adjustment is applied.','N');
note('Carrier Engine',103,'Common damage/age mix across carriers is an explicit temporary assumption; claim factors adjust weights, not observed intensity.','N');

base('Damage Engine','Joint total-loss selection and auction fees',1740,'W');
header('Damage Engine',5,['Period ID','Cohort ID','Body ID','Bucket','Severity low','Severity high','Recovery / ACV','Pre-loss value','Log repair median','Net loss threshold','Repair CDF cutoff','TL probability mass','Auction price','Standard buyer','Preferred buyer','Buyer blend','Seller fee','Core fee','Relative TL units','Core fee weight','Auction value weight']);
const lastfee=5+standard.length,lastvirtual=5+virtual.length;
for(let p=0;p<8;p++)for(let c=0;c<24;c++)for(let j=0;j<9;j++){
 const r=6+p*216+c*9+j,b=Math.floor(c/6),k=c%6,a=cols[p],ar=55+b,fr=194+c;
 R('Damage Engine',`C${r}:H${r}`,[[p,c,b,k,j/9,(j+1)/9]]);
 F('Damage Engine','I'+r,`='Assumptions'!$D$11+'Assumptions'!$D$12*(0.5-(G${r}+H${r})/2)`);
 F('Damage Engine','J'+r,`='Assumptions'!$D$8*EXP(-'Assumptions'!$D$9*('Fleet Engine'!E${fr}-10))*'Assumptions'!E${ar}*'Assumptions'!${a}36`);
 F('Damage Engine','K'+r,`='Source Data'!F${217+k}+LN('Assumptions'!D${ar})+LN('Assumptions'!${a}35)`);
 F('Damage Engine','L'+r,`=J${r}*(1-I${r}*(1-'Carrier Engine'!E${91+p}))`);
 F('Damage Engine','M'+r,`=NORM.S.DIST((LN(L${r})-K${r})/'Assumptions'!$D$10,TRUE)`);
 F('Damage Engine','N'+r,`=MAX(0,H${r}-MAX(G${r},M${r}))`);
 F('Damage Engine','O'+r,`=J${r}*I${r}`);
 const vb=`VLOOKUP(O${r},'Fee Data'!$I$6:$J$${lastvirtual},2,TRUE)+'Fee Data'!$J$20+'Fee Data'!$J$21`;
 F('Damage Engine','P'+r,`=(VLOOKUP(O${r},'Fee Data'!$C$6:$G$${lastfee},2,TRUE)+O${r}*VLOOKUP(O${r},'Fee Data'!$C$6:$G$${lastfee},3,TRUE)+${vb})*'Assumptions'!${a}37`);
 F('Damage Engine','Q'+r,`=(VLOOKUP(O${r},'Fee Data'!$C$6:$G$${lastfee},4,TRUE)+O${r}*VLOOKUP(O${r},'Fee Data'!$C$6:$G$${lastfee},5,TRUE)+${vb})*'Assumptions'!${a}37`);
 F('Damage Engine','R'+r,`=P${r}*(1-'Assumptions'!$D$14)+Q${r}*'Assumptions'!$D$14`);F('Damage Engine','S'+r,`=O${r}*'Carrier Engine'!E${91+p}`);F('Damage Engine','T'+r,`=R${r}+S${r}`);
 F('Damage Engine','U'+r,`=N${r}*'Fleet Engine'!${col(5+p)}${fr}`);F('Damage Engine','V'+r,`=U${r}*T${r}`);F('Damage Engine','W'+r,`=U${r}*O${r}`);
}
ss['Damage Engine'].getRange('C1:H1740').format.columnWidth=11;ss['Damage Engine'].getRange('I1:W1740').format.columnWidth=16;ss['Damage Engine'].getRange('G6:I1733').setNumberFormat(pct);ss['Damage Engine'].getRange('M6:N1733').setNumberFormat(pct);ss['Damage Engine'].getRange('C1:W5').format.rowHeight=38;

base('Vehicle Economics','Service revenue per insurance auction vehicle',51);periods('Vehicle Economics');note('Vehicle Economics',3,'RPU and ASP are outputs of the selected auction population. Service prices and adoption remain illustrative.');
row('Vehicle Economics',8,'Modeled total-loss probability',cols.map((c,p)=>`=SUM('Damage Engine'!U${6+p*216}:U${221+p*216})/SUM('Fleet Engine'!${col(5+p)}194:${col(5+p)}217)`),pct);
row('Vehicle Economics',9,'Selected auction ASP ($)',cols.map((c,p)=>`=SUM('Damage Engine'!W${6+p*216}:W${221+p*216})/SUM('Damage Engine'!U${6+p*216}:U${221+p*216})`));
row('Vehicle Economics',11,'Core auction RPU ($)',cols.map((c,p)=>`=SUM('Damage Engine'!V${6+p*216}:V${221+p*216})/SUM('Damage Engine'!U${6+p*216}:U${221+p*216})`));
row('Vehicle Economics',12,'Seller fee within core RPU',cols.map((c,p)=>`=${c}9*'Carrier Engine'!E${91+p}`));row('Vehicle Economics',13,'Buyer fee within core RPU',cols.map(c=>`=${c}11-${c}12`));
section('Vehicle Economics',15,'Attached services');
row('Vehicle Economics',16,'Title service use / sold vehicles',cols.map((c,p)=>`='Carrier Engine'!F${91+p}`),pct);row('Vehicle Economics',17,'Revenue per title job ($)',cols.map(c=>`='Assumptions'!$D$15*'Assumptions'!${c}38`));row('Vehicle Economics',18,'Title contribution to RPU ($)',cols.map(c=>`=${c}16*${c}17`));
row('Vehicle Economics',20,'Delivery use / sold vehicles',cols.map(c=>`='Assumptions'!${c}34`),pct);row('Vehicle Economics',21,'Revenue per delivery ($)',cols.map(c=>`='Assumptions'!$D$16*'Assumptions'!${c}39`));row('Vehicle Economics',22,'All-in insurance service RPU ($)',cols.map(c=>`=SUM(${c}11,${c}18,${c}20*${c}21)`));total('Vehicle Economics',22);
row('Vehicle Economics',24,'Delivery contribution to RPU ($)',cols.map(c=>`=${c}20*${c}21`));
section('Vehicle Economics',27,'Change from FY26Q4 baseline ($ / unit)');row('Vehicle Economics',28,'Core auction change',cols.map(c=>`=${c}11-$G$11`));row('Vehicle Economics',29,'Title contribution change',cols.map(c=>`=${c}18-$G$18`));row('Vehicle Economics',30,'Delivery contribution change',cols.map(c=>`=${c}24-$G$24`));row('Vehicle Economics',31,'Total RPU change',cols.map(c=>`=SUM(${c}28:${c}30)`));total('Vehicle Economics',31);
note('Vehicle Economics',34,'Title and delivery are modeled as attached auction revenue here. New or standalone product accounting still needs verification.');
note('Vehicle Economics',36,'Same-quarter fee mix is applied to completed units. With nonzero carryover, prior-cohort fee attribution is an approximation.');
note('Vehicle Economics',38,'No generic RPU-growth assumption. No historical +4pp regression intercept is carried into the forecast.');

base('Volume Build','U.S. insurance claims → Copart sales',48);periods('Volume Build');note('Volume Build',3,'Modeled quantities are calibrated to FY26Q4 insurance service dollars; they are not disclosed unit levels.');
row('Volume Build',8,'Relative claim exposure (000s)',cols.map((c,p)=>`=SUM('Fleet Engine'!${col(5+p)}194:${col(5+p)}217)`));
row('Volume Build',9,'Claims scale per exposure weight',cols.map(c=>`='Source Data'!$G$8*1000000*'Assumptions'!$D$7/($G$30*'Vehicle Economics'!$G$22)`));
row('Volume Build',10,'Claim-frequency multiplier',cols.map(c=>`='Assumptions'!${c}30`));row('Volume Build',11,'Coverage / filing multiplier',cols.map(c=>`='Assumptions'!${c}31`));
row('Volume Build',12,'Claim vehicles (calibrated)',cols.map(c=>`=${c}8*${c}9*${c}10*${c}11*(1+'Assumptions'!${c}45)`),integer);
row('Volume Build',14,'Total-loss probability',cols.map(c=>`='Vehicle Economics'!${c}8`),pct);row('Volume Build',15,'Total-loss vehicles',cols.map(c=>`=${c}12*${c}14`),integer);row('Volume Build',16,'Auction routing',cols.map(c=>`='Assumptions'!$D$13`),pct);row('Volume Build',17,'Eligible auction vehicles',cols.map(c=>`=${c}15*${c}16`),integer);row('Volume Build',18,'Copart allocation',cols.map((c,p)=>`='Carrier Engine'!D${91+p}`),pct);row('Volume Build',19,'Copart assignments (modeled)',cols.map(c=>`=${c}17*${c}18`),integer);
row('Volume Build',21,'Opening inventory (modeled)',cols.map((c,p)=>p?`=${cols[p-1]}24`:'=0'),integer);row('Volume Build',22,'Quarterly sale conversion',cols.map(c=>`='Assumptions'!${c}32`),pct);row('Volume Build',23,'Completed insurance sales',cols.map(c=>`=(${c}21+${c}19)*${c}22`),integer);row('Volume Build',24,'Closing inventory (modeled)',cols.map(c=>`=SUM(${c}21,${c}19)-${c}23`),integer);total('Volume Build',23);
section('Volume Build',26,'Historical normalization calculation');row('Volume Build',28,'Assignments before scale',cols.map(c=>`=${c}8*${c}10*${c}11*(1+'Assumptions'!${c}45)*${c}14*${c}16*${c}18`));row('Volume Build',29,'Opening inventory before scale',cols.map((c,p)=>p?`=${cols[p-1]}31`:'=0'));row('Volume Build',30,'Sales before scale',cols.map(c=>`=SUM(${c}28:${c}29)*${c}22`));row('Volume Build',31,'Closing inventory before scale',cols.map(c=>`=SUM(${c}28:${c}29)-${c}30`));
note('Volume Build',34,'One normalization at FY26Q4. Earlier-quarter misses remain visible; there are no quarterly revenue-calibration plugs.');note('Volume Build',36,'Opening FY26Q1 inventory is zero in the neutral timing convention. Changing historical timing requires a supported opening balance.');note('Volume Build',38,'Claims scale combines unmeasured coverage and claim frequency. This is not an independent absolute insured-fleet forecast.');

base('Revenue Bridge','Quarterly service revenue from operating drivers',53);periods('Revenue Bridge');note('Revenue Bridge',3,'$millions unless stated. Other-US and international use coarse activity × fee builds; no service-growth plug.');
row('Revenue Bridge',8,'Insurance completed units',cols.map(c=>`='Volume Build'!${c}23`),integer);row('Revenue Bridge',9,'Insurance service RPU ($)',cols.map(c=>`='Vehicle Economics'!${c}22`));row('Revenue Bridge',10,'US insurance service revenue',cols.map(c=>`=${c}8*${c}9/1000000`));
row('Revenue Bridge',12,'Other-US billable activity equivalents',cols.map(c=>`='Source Data'!$G$8*1000000*(1-'Assumptions'!$D$7)/'Assumptions'!$D$17*'Assumptions'!${c}40`),integer);row('Revenue Bridge',13,'Revenue per other-US activity ($)',cols.map(c=>`='Assumptions'!$D$17*'Assumptions'!${c}41`));row('Revenue Bridge',14,'Other-US service revenue',cols.map(c=>`=${c}12*${c}13/1000000`));row('Revenue Bridge',15,'Total US service revenue',cols.map(c=>`=SUM(${c}10,${c}14)`));total('Revenue Bridge',15);
row('Revenue Bridge',17,'International activity equivalents',cols.map(c=>`='Source Data'!$G$9*1000000/'Assumptions'!$D$18*'Assumptions'!${c}42`),integer);row('Revenue Bridge',18,'Revenue per activity ($ before FX)',cols.map(c=>`='Assumptions'!$D$18*'Assumptions'!${c}43`));row('Revenue Bridge',19,'International service revenue',cols.map(c=>`=${c}17*${c}18*'Assumptions'!${c}44/1000000`));row('Revenue Bridge',21,'Total modeled service revenue',cols.map(c=>`=SUM(${c}15,${c}19)`));total('Revenue Bridge',21);
section('Revenue Bridge',24,'Historical reconstruction — not a backtest');for(let p=0;p<4;p++){F('Revenue Bridge',cols[p]+'25',`=${cols[p]}15-'Source Data'!${cols[p]}8`);F('Revenue Bridge',cols[p]+'26',`=${cols[p]}19-'Source Data'!${cols[p]}9`);}label('Revenue Bridge',25,'US modeled less reported ($m)');label('Revenue Bridge',26,'International less reported ($m)');
section('Revenue Bridge',29,'Insurance revenue change vs FY26Q4 ($m)');row('Revenue Bridge',30,'Completed-unit contribution',cols.map(c=>`=(${c}8-$G$8)*$G$9/1000000`));row('Revenue Bridge',31,'RPU contribution',cols.map(c=>`=$G$8*(${c}9-$G$9)/1000000`));row('Revenue Bridge',32,'Unit × RPU interaction',cols.map(c=>`=(${c}8-$G$8)*(${c}9-$G$9)/1000000`));row('Revenue Bridge',33,'Total insurance revenue change',cols.map(c=>`=SUM(${c}30:${c}32)`));total('Revenue Bridge',33);
note('Revenue Bridge',37,'Other-US includes referral/access/other unseparated services; equivalent activity counts are not reported auction units.');note('Revenue Bridge',39,'No acquisition contribution is included. Seasonality, CAT changes and other activity growth require supported explicit inputs.');note('Revenue Bridge',41,'This prototype covers the dollar perimeter but does not independently identify every revenue component.');

base('RPM Summary','Copart — linked units and service revenue',46);periods('RPM Summary');note('RPM Summary',3,'Research prototype. FY26 reported dollars; FY27 conditional operating case. No EPS, DCF or purchased-vehicle sales.');
row('RPM Summary',8,'US insurance services — estimated ($m)',cols.map((c,p)=>p<3?'="n.a."':`='Revenue Bridge'!${c}10`));row('RPM Summary',9,'Other-US services — estimated ($m)',cols.map((c,p)=>p<3?'="n.a."':`='Revenue Bridge'!${c}14`));
row('RPM Summary',10,'US service revenue ($m)',cols.map((c,p)=>p<4?`='Source Data'!${c}8`:`='Revenue Bridge'!${c}15`));row('RPM Summary',11,'International services ($m)',cols.map((c,p)=>p<4?`='Source Data'!${c}9`:`='Revenue Bridge'!${c}19`));row('RPM Summary',12,'Total service revenue ($m)',cols.map(c=>`=SUM(${c}10:${c}11)`));total('RPM Summary',12);
row('RPM Summary',14,'Total service revenue YoY',cols.map((c,p)=>p<4?`=${c}12/SUM('Source Data'!${c}12:${c}13)-1`:`=${c}12/${cols[p-4]}12-1`),pct);
section('RPM Summary',17,'Insurance operating outputs — modeled in all periods');row('RPM Summary',18,'Completed units',cols.map(c=>`='Volume Build'!${c}23`),integer);row('RPM Summary',19,'Auction ASP ($)',cols.map(c=>`='Vehicle Economics'!${c}9`));row('RPM Summary',20,'Core auction RPU ($)',cols.map(c=>`='Vehicle Economics'!${c}11`));row('RPM Summary',21,'Additional-service RPU ($)',cols.map(c=>`='Vehicle Economics'!${c}18+'Vehicle Economics'!${c}24`));row('RPM Summary',22,'All-in service RPU ($)',cols.map(c=>`='Vehicle Economics'!${c}22`));row('RPM Summary',23,'Copart allocation',cols.map(c=>`='Volume Build'!${c}18`),pct);
section('RPM Summary',26,'External forecast comparison');row('RPM Summary',27,'Comparable service forecast ($m)',cols.map(c=>`='Assumptions'!${c}81`));row('RPM Summary',28,'Difference vs external forecast',cols.map(c=>`=IF(ISNUMBER(${c}27),${c}12-${c}27,"n.a.")`));
note('RPM Summary',31,'FY26Q4 insurance/other split is assumed. Earlier splits are unavailable here; the Revenue Bridge shows the full historical reconstruction and its residuals.');note('RPM Summary',33,'Current case does not assert service saturation or a validated crossover disadvantage. All amber driver assumptions remain reviewable.');note('RPM Summary',35,'Main unresolved inputs: claim levels, insurance dollar share, matched values/recovery, service prices/adoption, and carrier weights.');
header('RPM Summary',38,['Six-month view','H1 FY27']);F('RPM Summary','D39','=SUM(H12:I12)');label('RPM Summary',39,'Total service revenue ($m)');F('RPM Summary','D40','=D39/SUM(D12:E12)-1');label('RPM Summary',40,'YoY growth');ss['RPM Summary'].getRange('D40').setNumberFormat(pct);

base('Evidence','Input provenance and unresolved measurements',26,'I');header('Evidence',5,['ID','Input','Status','Period / population','Source','Limitation','Treatment']);R('Evidence','C6:I25',d.evidence);ss['Evidence'].getRange('C1:C26').format.columnWidth=8;ss['Evidence'].getRange('D1:I26').format.columnWidth=30;ss['Evidence'].getRange('C6:I25').format={wrapText:true,rowHeight:68};

base('Checks','Reconciliations and scope checks',30);periods('Checks');
row('Checks',8,'Inventory conservation (units)',cols.map(c=>`=SUM('Volume Build'!${c}21,'Volume Build'!${c}19)-SUM('Volume Build'!${c}23:'Volume Build'!${c}24)`));
row('Checks',9,'Normalized carrier weights less one',cols.map((c,p)=>`='Carrier Engine'!G${91+p}-1`));
row('Checks',10,'Insurance revenue identity ($m)',cols.map(c=>`='Revenue Bridge'!${c}10-'Volume Build'!${c}23*'Vehicle Economics'!${c}22/1000000`));
row('Checks',11,'Insurance change bridge ($m)',cols.map(c=>`='Revenue Bridge'!${c}33-('Revenue Bridge'!${c}10-'Revenue Bridge'!$G$10)`));
row('Checks',12,'RPU component bridge ($)',cols.map(c=>`='Vehicle Economics'!${c}31-('Vehicle Economics'!${c}22-'Vehicle Economics'!$G$22)`));
label('Checks',14,'FY26Q4 US calibration residual');F('Checks','G14',"='Revenue Bridge'!G15-'Source Data'!G8");
row('Checks',16,'Model less reported US ($m)',cols.map((c,p)=>p<4?`='Revenue Bridge'!${c}25`:'="n.a."'));
note('Checks',19,'Earlier historical residuals are not forced to zero. This is a reconstruction with present-day fee assumptions, not an out-of-sample validation.');
ss['Checks'].getRange('D8:K14').setNumberFormat('0.0000;(0.0000);0.0000');ss['Checks'].getRange('D8:K14').conditionalFormats.add('cellIs',{operator:'notBetween',formula:[-0.00001,0.00001],format:{fill:'#FFE2E2',font:{color:'#A00000',bold:true}}});
ss['Checks'].getRange('D8:K16').format.font.color='#111111';
ss['Checks'].getRange('D16:K16').format.horizontalAlignment='right';
ss['RPM Summary'].getRange('D8:K9').format.horizontalAlignment='right';
ss['RPM Summary'].getRange('D27:K28').format.horizontalAlignment='right';
ss['Fleet Engine'].getRange('C6:E189').setNumberFormat('0');ss['Fleet Engine'].getRange('C194:E217').setNumberFormat('0');
ss['Damage Engine'].getRange('C6:F1733').setNumberFormat('0');
ss['RPM Summary'].tabColor='#243A51';ss['Assumptions'].tabColor='#9EAAB5';ss['Source Data'].tabColor='#CDBDA5';
wb.recalculate();
const before=ss['RPM Summary'].getRange('H12:I12').values;
const actualBefore=ss['RPM Summary'].getRange('D10:G12').values;
ss['Assumptions'].getRange('H33').values=[[.6]];wb.recalculate();const adoption=ss['RPM Summary'].getRange('H12:I12').values;
ss['Assumptions'].getRange('H33').values=[[.5]];
ss['Assumptions'].getRange('H35').values=[[1.05]];wb.recalculate();const repair=ss['RPM Summary'].getRange('H12:I12').values;
ss['Assumptions'].getRange('H35').values=[[1]];
ss['Assumptions'].getRange('H32').values=[[.9]];wb.recalculate();const timing=ss['RPM Summary'].getRange('H18:I18').values;
ss['Assumptions'].getRange('H32').values=[[1]];wb.recalculate();
const tests={before,adoption,repair,timing,restored:ss['RPM Summary'].getRange('H12:I12').values,actualsUnchanged:JSON.stringify(actualBefore)===JSON.stringify(ss['RPM Summary'].getRange('D10:G12').values)};
if(JSON.stringify(tests.before)!==JSON.stringify(tests.restored)||!tests.actualsUnchanged||JSON.stringify(before)===JSON.stringify(adoption)||JSON.stringify(before)===JSON.stringify(repair))throw Error('Input propagation failed '+JSON.stringify(tests));
await fs.writeFile(path.join(dir,'propagation_tests.json'),JSON.stringify(tests,null,2));
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},summary:'Formula error scan'});
await fs.writeFile(path.join(dir,'error_scan.json'),errors.ndjson);
console.log((await wb.inspect({kind:'table',range:'RPM Summary!C8:K14',include:'values',tableMaxRows:7,tableMaxCols:9,maxChars:2500})).ndjson);
for(const n of names){const range=n==='Damage Engine'?'C5:W12':n==='Fleet Engine'?'C193:M201':n==='Carrier Engine'?'C90:G98':n==='Evidence'?'C5:I10':n==='Source Data'?'C5:K13':n==='Fee Data'?'C5:J15':n==='Assumptions'?'C28:K45':'C5:K24';const png=await wb.render({sheetName:n,range,scale:1,format:'png'});await fs.writeFile(path.join(out,n.replaceAll(' ','_')+'.png'),new Uint8Array(await png.arrayBuffer()));}
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(out,'CPRT_Linked_Service_Revenue.xlsx'));
console.log(JSON.stringify({output:path.join(out,'CPRT_Linked_Service_Revenue.xlsx'),tests,errorScan:errors.ndjson}));
