import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const out='/Users/kwu/cprt/outputs/cprt-delivery-20260928';await fs.mkdir(out,{recursive:true});
const w=Workbook.create(),b=w.worksheets.add('Delivery Build'),a=w.worksheets.add('Inputs');
function v(s,c,x){s.getRange(c).values=[[x]];}
function f(s,c,x){s.getRange(c).formulas=[[x]];}
function note(s,r,x){v(s,'B'+r,x);s.getRange(`B${r}:G${r}`).merge();s.getRange(`B${r}:G${r}`).format={wrapText:true,rowHeight:32};}
for(const s of [b,a]){s.showGridLines=false;s.getRange('A1:G48').format={font:{name:'Arial',size:10},rowHeight:20};s.getRange('A1:A48').format.columnWidth=2;s.getRange('B1:B48').format.columnWidth=49;s.getRange('C1:G48').format.columnWidth=16;s.getRange('C5:G48').setNumberFormat('#,##0.00;(#,##0.00);"—"');s.getRange('C5:G48').format.horizontalAlignment='right';s.getRange('B2:G2').format={font:{bold:true,size:14},rowHeight:25,borders:{bottom:{style:'thin',color:'#243A51'}}};}
v(a,'B2','Delivery assumptions and source observations');v(b,'B2','Copart delivery — adoption scenario build');
note(b,3,'Illustrative operating cases, not adopted forecasts. Revenue levels require an assumed starting base.');
const inputs=[
 [5,'Active case: 1 continuation / 2 slower / 3 flat',1],
 [7,'FY26Q3 delivery cost increase, YoY ($m)',15],
 [8,'FY26Q4 delivery cost increase, YoY ($m)',17],
 [10,'Cost increase attributable to completed jobs',1],
 [11,'Constant delivery gross margin — assumed',.2],
 [12,'FY25Q4 delivery jobs — illustrative base',50000],
 [13,'Revenue per completed delivery ($) — assumed',300],
 [14,'Eligible quarterly transactions — assumed',1000000],
 [16,'Continuation: adoption increase per quarter',.01],
 [17,'Slower: adoption increase per quarter',.0025],
 [18,'Flat: adoption increase per quarter',0],
 [20,'Eligible transactions, sequential growth',0],
 [21,'Revenue per delivery, sequential growth',0],
 [23,'FY26Q1 delivery revenue ($m) — unavailable','n.a.'],
 [24,'FY26Q2 delivery revenue ($m) — unavailable','n.a.']];
for(const[r,l,x]of inputs){v(a,'B'+r,l);v(a,'C'+r,x);a.getRange('C'+r).format={font:{color:'#0000FF'},fill:r===7||r===8?'#E8EEF2':'#FFF2CC'};}
for(const r of [10,11,16,17,18,20,21])a.getRange('C'+r).setNumberFormat('0.00%');a.getRange('C5').setNumberFormat('0');
a.getRange('C5').dataValidation={rule:{type:'list',values:['1','2','3']}};
note(a,27,'Only C7:C8 are reported cost increases. Other numeric inputs are illustrative assumptions, not measured adoption, prices or volumes.');
note(a,29,'Source: call_2026-05-21.txt lines 471–477 ($15m); call_2026-09-10.txt lines 522–528 ($17m), existing repository transcripts.');
note(a,31,'Cost-to-revenue conversion requires stable margins and costs matched to incremental completed jobs. Positive product margin alone is insufficient.');
note(a,33,'Eligible transactions mean the potential delivery customer pool, not insurance-only units. Default one million is a scaling assumption.');
note(a,35,'Gross revenue and same-quarter recognition are working conventions requiring contract/accounting confirmation. No ACV revenue included.');
note(a,37,'Holding job price and eligible transactions constant isolates adoption. The cases are not evidence that adoption will slow.');
v(b,'B5','Active case');f(b,'C5','=CHOOSE(Inputs!C5,"Continuation","Slower","Flat")');
v(b,'B7','Historical constraint — FY26Q4');
const hist=[
 [8,'Assumed FY25Q4 delivery revenue ($m)','=Inputs!C12*Inputs!C13/1000000'],
 [9,'Conditional YoY delivery revenue increase ($m)','=Inputs!C8*Inputs!C10/(1-Inputs!C11)'],
 [10,'Conditional FY26Q4 delivery revenue ($m)','=SUM(C8:C9)'],
 [11,'Implied FY26Q4 delivery jobs','=C10*1000000/Inputs!C13'],
 [12,'Implied FY26Q4 adoption','=C11/Inputs!C14'],
 [14,'Q3 conditional YoY revenue increase ($m)','=Inputs!C7*Inputs!C10/(1-Inputs!C11)']];
for(const[r,l,x]of hist){v(b,'B'+r,l);f(b,'C'+r,x);}b.getRange('C12').setNumberFormat('0.00%');
b.getRange('C17:F17').values=[['FY27 Q1','FY27 Q2','FY27 Q3','FY27 Q4']];b.getRange('B17:F17').format={fill:'#243A51',font:{bold:true,color:'#FFFFFF'}};
const labels={18:'Eligible transactions',19:'Beginning adoption',20:'Active quarterly adoption increase',21:'Ending adoption',22:'Average adoption during quarter',23:'Completed delivery jobs',24:'Revenue per delivery ($)',25:'Delivery revenue ($m)',27:'Volume and adoption at unchanged price ($m)',28:'Price contribution ($m)',29:'Revenue identity check',31:'Comparable prior-year delivery revenue ($m)',32:'Delivery revenue change, YoY ($m)'};
for(const[r,l]of Object.entries(labels))v(b,'B'+r,l);
for(const[c,i]of ['C','D','E','F'].map((c,i)=>[c,i])){
 const prev=String.fromCharCode(c.charCodeAt(0)-1);
 f(b,c+'18',i===0?'=Inputs!C14*(1+Inputs!C20)':`=${prev}18*(1+Inputs!$C$20)`);
 f(b,c+'19',i===0?'=$C$12':`=${prev}21`);
 f(b,c+'20','=CHOOSE(Inputs!$C$5,Inputs!$C$16,Inputs!$C$17,Inputs!$C$18)');
 f(b,c+'21',`=MIN(1,MAX(0,${c}19+${c}20))`);f(b,c+'22',`=AVERAGE(${c}19,${c}21)`);
 f(b,c+'23',`=${c}18*${c}22`);f(b,c+'24',i===0?'=Inputs!C13*(1+Inputs!C21)':`=${prev}24*(1+Inputs!$C$21)`);
 f(b,c+'25',`=${c}23*${c}24/1000000`);f(b,c+'27',`=${c}23*Inputs!$C$13/1000000`);
 f(b,c+'28',`=${c}23*(${c}24-Inputs!$C$13)/1000000`);f(b,c+'29',`=SUM(${c}27:${c}28)-${c}25`);
 f(b,c+'31',i===0?'=Inputs!C23':i===1?'=Inputs!C24':i===2?'="n.a."':'=$C$10');
 f(b,c+'32',`=IF(ISNUMBER(${c}31),${c}25-${c}31,"n.a.")`);
}b.getRange('C19:F22').setNumberFormat('0.00%');b.getRange('C18:F18').setNumberFormat('#,##0');b.getRange('C23:F23').setNumberFormat('#,##0');
v(b,'B35','H1 delivery revenue ($m)');f(b,'C35','=SUM(C25:D25)');
note(b,37,'Adoption begins at the calibrated Q4 average as an assumed opening proxy; actual quarter-end adoption is unknown.');
note(b,39,'The Q3 cost disclosure constrains YoY growth only. It does not identify Q3 absolute revenue or H1 prior-year revenue.');
note(b,41,'Integrate by replacing the existing delivery allowance, not adding this schedule on top. Other service revenue remains separate.');
note(b,43,'Do not recalibrate the starting base when changing forward adoption. Missing YoY history stays unavailable.');
const cases=[];for(let k=1;k<=3;k++){v(a,'C5',k);w.recalculate();cases.push({case:k,quarter_revenue:b.getRange('C25:F25').values[0],h1:b.getRange('C35').values[0][0]});}
v(a,'C5',1);w.recalculate();const histBase=b.getRange('C10').values[0][0];
if(cases[0].h1<=cases[1].h1||cases[1].h1<=cases[2].h1)throw Error('Case propagation failed');
v(a,'C16',0);w.recalculate();if(Math.abs(b.getRange('C35').values[0][0]-cases[2].h1)>1e-8)throw Error('Flat adoption check failed');
if(b.getRange('C10').values[0][0]!==histBase)throw Error('Historical anchor changed');v(a,'C16',.01);w.recalculate();
await fs.writeFile(out+'/case_checks.json',JSON.stringify({cases,limitations:'Illustrative, not forecast; no independent baseline level'},null,2));
for(const sh of [b,a]){const img=await w.render({sheetName:sh.name,range:`B2:G${sh===b?43:37}`,scale:1.5});await fs.writeFile(out+'/'+sh.name.replace(' ','_')+'.png',new Uint8Array(await img.arrayBuffer()));}
await(await SpreadsheetFile.exportXlsx(w)).save(out+'/CPRT_Delivery_Adoption.xlsx');console.log(JSON.stringify(cases));
