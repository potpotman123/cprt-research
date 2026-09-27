from pathlib import Path
import urllib.request,hashlib,json,datetime,concurrent.futures
from html.parser import HTMLParser
p=Path(__file__).parent
urls={
'camry_rear':'https://vin-archive.net/lot/4t4bf1fk4gr540574-toyota-camry-2016',
'rav4_rear':'https://vin-archive.net/lot/2t3dfrevxgw533908-toyota-rav4-2016',
'f150_front':'https://finalbid.vin/en/ford/f-150/2016/iaai-45136422-1FTEW1CF6GFA07312',
'f150_side':'https://finalbid.vin/en/ford/f-150/2016/copart-65004706-1FTMF1C81GKD57189',
'camry_carfast':'https://carfast.express/en/auction/lots/111042860129-toyota-camry-2016-vin-4t1bf1fk1gu193991'}
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.out=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip and s.strip():self.out.append(s.strip())
def fetch(kv):
 k,u=kv;r=dict(key=k,url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as f:b=f.read();r['status']=f.status
  (p/'raw'/f'{k}.html').write_bytes(b);r['sha256']=hashlib.sha256(b).hexdigest();r['bytes']=len(b)
  t=Text();t.feed(b.decode('utf-8',errors='replace'));(p/'raw'/f'{k}.txt').write_text('\n'.join(t.out))
 except Exception as e:r['error']=str(e)
 return r
rs=list(concurrent.futures.ThreadPoolExecutor(max_workers=3).map(fetch,urls.items()))
(p/'sources.json').write_text(json.dumps(rs,indent=2));print(json.dumps(rs,indent=2))
