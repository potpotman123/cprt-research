"""Read-only local capture audit. No network, OCR, or source-file mutation."""
import ast, collections as C, csv, hashlib, io, json, pathlib, re, sqlite3, statistics, time
import xml.etree.ElementTree as ET

ROOT = pathlib.Path('/Users/kwu/cprt')
OUT = pathlib.Path(__file__).resolve().parent
US = set('AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC'.split())
# Load only literal dictionaries and the classifier, never the original script's I/O.
src = ROOT/'scripts/experiments/e1_listed_body_share.py'
tree = ast.parse(src.read_text())
names = {'OTHER_MAKES','OTHER_MODELS','PICKUP','VAN','SUV','AMBIG','PASSENGER_MAKES'}
nodes = [n for n in tree.body if (isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets)) or (isinstance(n,ast.FunctionDef) and n.name=='classify')]
ns = {}; exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
classify=ns['classify']

def parse(loc):
    m=re.search(r'/lot/(\d+)/([^?\#]*)',loc)
    if not m: return None
    slug=m[2].lower().strip('/')
    y=re.search(r'(?:^|-)((?:19|20)\d{2})-',slug)
    if not y: return None
    rest=slug[y.end():].split('-'); state=None; yard=None; mm='-'.join(rest)
    for i in range(len(rest)-1,0,-1):
        if rest[i].upper() in US:
            state=rest[i].upper();yard='-'.join(rest[i+1:]);mm='-'.join(rest[:i]);break
    return int(m[1]), (slug[:y.start()].strip('-'),int(y[1]),mm,state,yard)

def metrics(items,year):
    groups=C.defaultdict(list); missing=0; fallback=C.Counter(); invalid=0
    for title,my,mm,state,yard in items:
        cls,key=classify(mm or '')
        if cls=='CAR': fallback[key]+=1
        if not state: missing+=1
        if not my or not (1900<=my<=year+1): invalid+=1;continue
        sal=(title or '').startswith(('salvage','non'))
        for scope in ['all_light']+(['salvage_light'] if sal else [])+(['us_salvage_light'] if sal and state in US else []):
            if cls in {'CAR','PICKUP','SUV','VAN'}: groups[scope].append((cls,my,state,yard))
    out={'unique_lots':len(items),'missing_us_state':missing,'invalid_year':invalid,'car_class_keys':fallback.most_common(15),'scopes':{}}
    for scope,rows in groups.items():
        cnt=C.Counter(x[0] for x in rows);ys=[x[1] for x in rows]
        out['scopes'][scope]={'n':len(rows),'mean_my':statistics.mean(ys),'median_my':statistics.median(ys),'lt_pct':100*(len(rows)-cnt['CAR'])/len(rows),'body_counts':dict(cnt),'states':dict(C.Counter(x[2] or 'UNKNOWN' for x in rows)), 'mean_my_by_body':{b:statistics.mean(x[1] for x in rows if x[0]==b) for b in cnt}}
    return out

def archive(f):
    start=time.perf_counter();raw=f.read_bytes(); cap=re.search(r'p(\d)_(\d{14})',f.name)
    result={'file':f.name,'page':int(cap[1]),'capture':cap[2],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    if not raw: return dict(result,status='empty')
    if b'<urlset' not in raw[:1000]:return dict(result,status='not_sitemap',note='HTML/challenge response; excluded, not zero vehicles')
    # Invalid XML control-character references occur in a few vehicle descriptions.
    # Exclude the complete offending URL record in memory; preserve raw bytes/hash.
    excluded=[]
    def clean_block(m):
        bad=False
        for x in re.finditer(rb'&#(x[0-9a-fA-F]+|[0-9]+);',m[0]):
            n=int(x[1][1:],16) if x[1].startswith(b'x') else int(x[1])
            if not(n in (9,10,13) or 32<=n<=0xD7FF or 0xE000<=n<=0xFFFD or 0x10000<=n<=0x10FFFF):bad=True
        if bad:excluded.append(hashlib.sha256(m[0]).hexdigest());return b''
        return m[0]
    if re.search(rb'&#(?:x[0-9a-fA-F]+|[0-9]+);',raw):
        raw=re.sub(rb'<url\b[^>]*>.*?</url>',clean_block,raw,flags=re.S)
    result['excluded_invalid_xml_records']=len(excluded)
    result['excluded_record_hashes']=excluded
    records={};locs=0;unparsed=0;dups=0;conflicts=0;bad_ids=set()
    try:
        for _,el in ET.iterparse(io.BytesIO(raw),events=('end',)):
            if el.tag.split('}')[-1]=='loc':
                locs+=1;row=parse(el.text or '')
                if row:
                    lid,v=row
                    if lid in records:
                        dups+=1;conflicts+=records[lid]!=v
                        if records[lid]!=v:bad_ids.add(lid)
                    else:records[lid]=v
                else:unparsed+=1
            el.clear()
    except ET.ParseError as exc:
        return dict(result,status='xml_error',error=str(exc),locs_before_error=locs)
    for lid in bad_ids:records.pop(lid,None)
    return dict(result,status='parsed',loc_elements=locs,unparsed_locs=unparsed,duplicate_rows=dups,conflicting_rows=conflicts,excluded_conflicting_ids=len(bad_ids),seconds=time.perf_counter()-start,**metrics(list(records.values()),int(cap[2][:4])))

def table(name):
    with (ROOT/'data/csv'/name).open() as f:return list(csv.DictReader(l for l in f if not l.startswith('#')))

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');args=ap.parse_args()
    started=time.perf_counter();files=sorted((ROOT/'raw/lotxml').glob('*.xml'))
    if not args.full:
        nonempty=[f for f in files if f.stat().st_size]
        files=[nonempty[0],nonempty[len(nonempty)//2],nonempty[-1]]
    results=[archive(f) for f in files]
    payload={'scope':'full archive' if args.full else 'three-file pilot','archive':results,'classifier_sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
    if args.full:
        con=sqlite3.connect('file:/Users/kwu/cprt/data/cprt.db?mode=ro',uri=True); con.execute('BEGIN')
        grouped=C.defaultdict(dict);dup=C.Counter();conf=C.Counter();bad_ids=C.defaultdict(set)
        for ts,lid,title,yr,mm,state,yard in con.execute("SELECT snapshot_utc,lot_id,title_type,year,make_model,state,yard_slug FROM lot_snapshots WHERE snapshot_utc >= '2026-09-24' AND snapshot_utc < '2026-09-27'"):
            value=(title,yr,mm,state,yard)
            if lid in grouped[ts]:
                dup[ts]+=1;conf[ts]+=grouped[ts][lid]!=value
                if grouped[ts][lid]!=value:bad_ids[ts].add(lid)
            else:grouped[ts][lid]=value
        for ts,ids in bad_ids.items():
            for lid in ids:grouped[ts].pop(lid,None)
        payload['live']=[dict(capture=ts,duplicates=dup[ts],conflicts=conf[ts],excluded_conflicting_ids=len(bad_ids[ts]),records_sha256=hashlib.sha256(json.dumps(sorted(rows.items())).encode()).hexdigest(),**metrics(list(rows.values()),2026)) for ts,rows in sorted(grouped.items())]
        con.close()
        p={r['age_bucket']:r for r in table('ccc_tl_share_by_age_2020_2025.csv')};t={r['age_bucket']:r for r in table('ccc_tl_valuation_share_by_age_2020_2025.csv')}
        buckets=[b for b in p if b!='total'];weights={};rates={};levels={}
        for y in ['cy2020','cy2021','cy2022','cy2023','cy2024','cy2025']:
            rates[y]={b:float(p[b][y])/100 for b in buckets}
            raw={b:float(t[b][y])/rates[y][b] for b in buckets};s=sum(raw.values());weights[y]={b:v/s for b,v in raw.items()}
            levels[y]={'reconstructed_pct':100*sum(weights[y][b]*rates[y][b] for b in buckets),'published_pct':float(p['total'][y])}
        decomp=[]
        for a,z in [('cy2020','cy2022'),('cy2022','cy2025'),('cy2024','cy2025')]:
            w0,w1=weights[a],weights[z];p0,p1=rates[a],rates[z]
            mix=sum((w1[b]-w0[b])*p0[b] for b in buckets)*100
            within=sum(w0[b]*(p1[b]-p0[b]) for b in buckets)*100
            interaction=sum((w1[b]-w0[b])*(p1[b]-p0[b]) for b in buckets)*100
            decomp.append({'from':a,'to':z,'mix_base_pp':mix,'within_base_pp':within,'interaction_pp':interaction,'mix_symmetric_pp':mix+interaction/2,'within_symmetric_pp':within+interaction/2,'total_pp':mix+within+interaction})
        payload['ccc']={'levels':levels,'decomposition':decomp,'status':'recomputed from existing transcribed tables; source-chart population compatibility not reverified'}
    payload['elapsed_seconds']=time.perf_counter()-started
    dest=OUT/('results.json' if args.full else 'pilot.json');dest.write_text(json.dumps(payload,indent=2))
    print(json.dumps({'output':str(dest),'files':len(results),'statuses':dict(C.Counter(r['status'] for r in results)),'elapsed_seconds':payload['elapsed_seconds'],'pilot_rows':[r.get('loc_elements') for r in results] if not args.full else None}))
if __name__=='__main__':main()
