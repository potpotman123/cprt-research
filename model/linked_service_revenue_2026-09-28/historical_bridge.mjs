import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root='/Users/kwu/cprt', dir=root+'/model/linked_service_revenue_2026-09-28', out=root+'/outputs/cprt-historical-20260928';
await fs.mkdir(out,{recursive:true});
const d=JSON.parse(await fs.readFile(dir+'/bridge_inputs.json','utf8'));
const wb=Workbook.create(), b=wb.worksheets.add('Historical Bridge'), s=wb.worksheets.add('Source Data');
const cols=['D','E','F','G'], fmt='#,##0.00;(#,##0.00);"—"';
function v(sh,a,x){sh.getRange(a).values=[[x]];}
function f(sh,a,x){sh.getRange(a).formulas=[[x]];sh.getRange(a).format.font.color=x.includes('!')?'#008000':'#111111';}
function band(sh,r,t){v(sh,'B'+r,t);sh.getRange(`B${r}:H${r}`).format={fill:'#E7EBEF',font:{bold:true},borders:{bottom:{style:'thin',color:'#8A98A5'}}};}
for(const sh of [b,s]){
 sh.showGridLines=false;sh.getRange('A1:J55').format={font:{name:'Arial',size:10},rowHeight:20};
 sh.getRange('A1:A55').format.columnWidth=2;sh.getRange('B1:B55').format.columnWidth=42;sh.getRange('C1:C55').format.columnWidth=3;
 sh.getRange('D1:H55').format.columnWidth=15;sh.getRange('D6:H55').setNumberFormat(fmt);sh.getRange('D6:H55').format.horizontalAlignment='right';
 sh.getRange('B2:H2').format={font:{size:14,bold:true},borders:{bottom:{style:'thin',color:'#243A51'}},rowHeight:26};
 sh.getRange('D5:H5').values=[['FY26 Q1','FY26 Q2','FY26 Q3','FY26 Q4','FY26 total']];
 sh.getRange('B5:H5').format={fill:'#243A51',font:{bold:true,color:'#FFFFFF'}};
}
v(b,'B2','Copart — historical service-revenue bridge');v(s,'B2','Historical observations and provenance');
v(b,'B3','USD millions. Derived contributions are accounting attributions, not causal estimates.');
v(s,'B3','Inputs are observations or labelled broker history. Missing values remain n.a.');
for(const [region,start] of [['us',7],['intl',14]]){
 const rr=d.controls.filter(x=>x.region===region);
 ['Prior-year service revenue','Current-year service revenue','Observed fee-unit growth','Observed fee RPU growth'].forEach((x,i)=>v(s,'B'+(start+i),(region==='us'?'US: ':'International: ')+x));
 for(let i=0;i<4;i++){
  const c=cols[i],x=rr[i];v(s,c+start,+x.prior_service_musd);v(s,c+(start+1),+x.service_musd);
  v(s,c+(start+2),region==='us'?(['n.a.',-.09,-.033,'n.a.'][i]):'n.a.');
  v(s,c+(start+3),x.disclosed_fee_rpu_yoy===''?'n.a.':+x.disclosed_fee_rpu_yoy);
 }
 s.getRange(`D${start+2}:G${start+3}`).setNumberFormat('0.0%');s.getRange(`D${start}:G${start+3}`).format.font.color='#0000FF';
}
band(s,21,'Sources and classification');
const notes=[
 'Service dollars: data/csv/segment_service_rev_8k.csv; FY25/FY26 paired SEC release figures.',
 'US Q1 RPU: call_2025-11-20.txt lines 209–210; +7.5%, company transcript.',
 'US Q2/Q3 fee units: Stephens 20 Aug 2026, Exhibit 7, PDF page 7: -9.0% / -3.3%.',
 'Broker PDF: local supplied report ending 123970131.pdf; period columns verified with text positions.',
 'International RPU: Nov 20 lines 219–220; Feb 19 line 185; May 21 line 184; Sep 10 line 223.',
 'International Q4 fee units: Sep 10 lines 232–235, +11.5%; independent rounded cross-check only.',
 'US Q4 JPM ~5% RPU is an analyst estimate; excluded from the observed bridge.',
 'No absolute unit count or dollar RPU is implied. Each quarter uses its own prior-year revenue.',
 'Derived RPU includes mix, services and FX where relevant; it is not a pure price increase.',
 'Model comparison: linked model validation.json; assumed 90% insurance split, fixed other-US revenue.'
];notes.forEach((x,i)=>{v(s,'B'+(23+i),x);s.getRange(`B${23+i}:H${23+i}`).merge();s.getRange(`B${23+i}:H${23+i}`).format={wrapText:true,rowHeight:30};});
v(s,'B35','Observed international Q4 fee-unit growth');v(s,'G35',.115);s.getRange('G35').setNumberFormat('0.0%');
v(s,'B37','Prototype US service reconstruction');cols.forEach((c,i)=>v(s,c+'37',d.model[i].insurance_m+d.model[i].other_us_m));
for(const [title,start,src] of [['US service revenue',7,7],['International service revenue',24,14]]){
 band(b,start,title);
 const labels=['Prior-year service revenue','Fee-unit growth — used','Fee RPU growth — used','Attribution basis','Volume contribution ($m)','RPU contribution ($m)','Volume × RPU interaction ($m)','Unallocated revenue change ($m)','Reconstructed service revenue','Reported service revenue','Reconciliation difference','Reported revenue change ($m)','Reported revenue growth'];
 labels.forEach((x,i)=>v(b,'B'+(start+1+i),x));
 cols.forEach(c=>{
  const pr=start+1,u=start+2,p=start+3;
  f(b,c+pr,`='Source Data'!${c}${src}`);
  f(b,c+u,`=IF(ISNUMBER('Source Data'!${c}${src+2}),'Source Data'!${c}${src+2},IF(ISNUMBER('Source Data'!${c}${src+3}),('Source Data'!${c}${src+1}/${c}${pr})/(1+'Source Data'!${c}${src+3})-1,"n.a."))`);
  f(b,c+p,`=IF(ISNUMBER('Source Data'!${c}${src+3}),'Source Data'!${c}${src+3},IF(ISNUMBER('Source Data'!${c}${src+2}),('Source Data'!${c}${src+1}/${c}${pr})/(1+'Source Data'!${c}${src+2})-1,"n.a."))`);
  f(b,c+(start+4),`=IF(ISNUMBER('Source Data'!${c}${src+2}),"Broker units",IF(ISNUMBER('Source Data'!${c}${src+3}),"Reported RPU","Unresolved"))`);
  for(const [off,expr] of [[5,`${c}${pr}*${c}${u}`],[6,`${c}${pr}*${c}${p}`],[7,`${c}${pr}*${c}${u}*${c}${p}`]])f(b,c+(start+off),`=IF(AND(ISNUMBER(${c}${u}),ISNUMBER(${c}${p})),${expr},"n.a.")`);
  f(b,c+(start+8),`=IF(ISNUMBER(${c}${u}),0,'Source Data'!${c}${src+1}-${c}${pr})`);
  f(b,c+(start+9),`=${c}${pr}+SUM(${c}${start+5}:${c}${start+8})`);
  f(b,c+(start+10),`='Source Data'!${c}${src+1}`);
  f(b,c+(start+11),`=${c}${start+9}-${c}${start+10}`);
  f(b,c+(start+12),`=${c}${start+10}-${c}${pr}`);
  f(b,c+(start+13),`=${c}${start+10}/${c}${pr}-1`);
 });
 b.getRange(`D${start+2}:G${start+3}`).setNumberFormat('0.00%');b.getRange(`D${start+13}:H${start+13}`).setNumberFormat('0.00%');
 for(const off of [1,5,6,7,8,9,10,11,12])f(b,'H'+(start+off),`=SUM(D${start+off}:G${start+off})`);
 f(b,'H'+(start+13),`=H${start+10}/H${start+1}-1`);
 for(const off of [2,3])v(b,'H'+(start+off),'n.a.');v(b,'H'+(start+4),start===7?'Q4 unresolved':'Derived units');
 b.getRange(`D${start+4}:H${start+4}`).format.font.size=9;
 b.getRange(`B${start+10}:H${start+10}`).format={font:{bold:true},borders:{top:{style:'thin',color:'#243A51'}}};
}
v(b,'B22','US annual attribution is partial: Q4 revenue change remains explicitly unallocated.');
band(b,40,'Model comparison — US service revenue');
v(b,'B41','Prototype reconstruction');v(b,'B42','Reported US revenue');v(b,'B43','Prototype less reported');v(b,'B44','Absolute quarterly errors');
cols.forEach(c=>{f(b,c+'41',`='Source Data'!${c}37`);f(b,c+'42',`=${c}17`);f(b,c+'43',`=${c}41-${c}42`);f(b,c+'44',`=ABS(${c}43)`);});
for(const r of [41,42,43,44])f(b,'H'+r,`=SUM(D${r}:G${r})`);
v(b,'B46','A zero bridge residual is an identity, not independent validation of inferred units or fees.');
v(b,'B47','Volume = prior revenue × unit growth; RPU = prior revenue × RPU growth; interaction kept separate.');
v(b,'B48','RPU attribution does not distinguish fees, seller mix, additional services or foreign exchange.');
for(const r of [3,22,46,47,48]){b.getRange(`B${r}:H${r}`).merge();b.getRange(`B${r}:H${r}`).format={wrapText:true,rowHeight:30};}
s.getRange('B3:H3').merge();s.getRange('B3:H3').format={wrapText:true,rowHeight:30};
wb.recalculate();
// Cheap propagation: input changes must alter inferred RPU while preserving revenue identity.
const before=b.getRange('E10').values[0][0];v(s,'E9',-.08);wb.recalculate();
if(b.getRange('E10').values[0][0]===before)throw Error('RPU propagation failed');
if(Math.abs(b.getRange('E18').values[0][0])>1e-8)throw Error('Revenue reconciliation failed');
v(s,'E9','n.a.');wb.recalculate();if(b.getRange('E12').values[0][0]!=='n.a.')throw Error('Missing unit input concealed');
v(s,'E9',-.09);wb.recalculate();
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:20},maxChars:1500});
await fs.writeFile(out+'/error_scan.json',JSON.stringify(errors));
for(const [sh,end]of [[b,48],[s,37]]){const img=await wb.render({sheetName:sh.name,range:`B2:H${end}`,scale:1.5});await fs.writeFile(out+'/'+sh.name.replaceAll(' ','_')+'.png',new Uint8Array(await img.arrayBuffer()));}
await (await SpreadsheetFile.exportXlsx(wb)).save(out+'/CPRT_Historical_Service_Bridge.xlsx');
console.log(JSON.stringify({output:out+'/CPRT_Historical_Service_Bridge.xlsx',us_rpu:b.getRange('D10:G10').values,us_contributions:b.getRange('H12:H15').values,intl_contributions:b.getRange('H29:H32').values}));
