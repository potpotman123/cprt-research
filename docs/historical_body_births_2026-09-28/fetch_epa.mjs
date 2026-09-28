// Read the existing public EPA table; no browser, OCR or private account.
import fs from 'node:fs/promises';
const app='18c705d2-35a3-4410-9428-0eb9dfd64c4f';
const object='dc3849eb-27da-4539-821e-4a8a1d28fcca';
const ws=new WebSocket(`wss://edap.epa.gov/public/app/${app}`);
let id=0;const pending=new Map();
const timer=setTimeout(()=>{console.error('EPA request timeout');process.exit(1)},30000);
const call=(handle,method,params=[])=>new Promise((resolve,reject)=>{
  pending.set(++id,{resolve,reject});ws.send(JSON.stringify({jsonrpc:'2.0',id,handle,method,params}));
});
ws.onmessage=e=>{const r=JSON.parse(e.data);const p=pending.get(r.id);if(p){pending.delete(r.id);r.error?p.reject(r.error):p.resolve(r.result)}};
ws.onerror=()=>{console.error('EPA connection failed');process.exit(1)};
ws.onopen=async()=>{
  try {
    const a=await call(-1,'OpenDoc',[app]);
    const o=await call(a.qReturn.qHandle,'GetObject',[object]);const handle=o.qReturn.qHandle;
    const {qProp}=await call(handle,'GetProperties');const {qLayout}=await call(handle,'GetLayout');
    const size=qLayout.qHyperCube.qSize;
    if(size.qcy>1000)throw Error('Unexpected table expansion; review before retrieving');
    const data=await call(handle,'GetHyperCubeData',['/qHyperCubeDef',[{qTop:0,qLeft:0,qHeight:size.qcy,qWidth:4}]]);
    const out={retrieved_at:new Date().toISOString(),app_id:app,object_id:object,
      source_url:'https://www.epa.gov/automotive-trends/explore-automotive-trends-data',
      basis_url:'https://www.epa.gov/automotive-trends/about-automotive-trends-data',
      dimensions:qProp.qHyperCubeDef.qDimensions.map(x=>x.qDef.qFieldDefs),
      production_share_expression:qProp.qHyperCubeDef.qMeasures[0].qDef.qDef,
      rows:data.qDataPages.flatMap(x=>x.qMatrix).map(row=>row.map(x=>({text:x.qText,number:Number.isFinite(x.qNum)?x.qNum:null}))) };
    await fs.writeFile(new URL('epa_public_table.json',import.meta.url),JSON.stringify(out,null,2)+'\n');
    console.log(JSON.stringify({rows:out.rows.length,types:[...new Set(out.rows.map(r=>r[1].text))],sample:out.rows.slice(-8)}));
  } catch(e){console.error(e);process.exitCode=1}finally{clearTimeout(timer);ws.close()}
};
