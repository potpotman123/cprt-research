from pathlib import Path
import urllib.request,hashlib,json,datetime,sys
root=Path(__file__).parent
for name,url in zip(sys.argv[1::2],sys.argv[2::2]):
 rec={'url':url,'file':name,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'CPRT-Research/1.0 academic research'}),timeout=40) as r:
   data=r.read(); rec.update(status=r.status,bytes=len(data),sha256=hashlib.sha256(data).hexdigest());(root/'raw'/name).write_bytes(data)
 except Exception as e: rec['error']=str(e)
 with (root/'sources.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
 print(rec)
