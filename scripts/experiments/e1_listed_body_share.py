#!/usr/bin/env python3
"""E1 step 1 — light-truck share of Copart's LISTED pool by capture month, 2022-08 → 2026-09, from the lot slugs.

Why: the fleet roll (scripts/age_curves.py, asp_vintage_effect.csv) says light trucks were 57% of modelled total losses in
2024, rising ~1.7pp/yr. Nothing in that number came from Copart. The listed pool's make/model slugs are a free reality
check: if the listed light-truck share is far from the roll's, the roll's body split is wrong and E1 stops there.

Classification: make/model tokens → CAR | LT (pickup ≤10,000 lb GVWR, SUV/crossover, van) | OTHER (medium/heavy trucks,
motorcycles, RVs, trailers, equipment, boats, unrecognised). Ward's/EPA convention: crossovers are light trucks; F-350 /
3500-series and up are class 3+ and go to OTHER. Ambiguous crossovers (Outback, Soul, Niro, EV6, Crosstrek, Kicks) are
tagged AMBIG and reported both ways as a band. Share = LT / (CAR + LT), i.e. of classified light vehicles.

Sources: raw/lotxml/*.xml (Internet Archive captures, union across pages within a capture month), data/cprt.db
lot_snapshots (nightly live captures; union within night). No network. Output: data/csv/listed_body_share_monthly.csv
"""
import csv, glob, os, pathlib, re, sqlite3, sys, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'data/csv/listed_body_share_monthly.csv'

# ---- lookup tables (make, model-first-token[, second token]) ---------------------------------------------------------
OTHER_MAKES = {'freightliner','kenworth','peterbilt','international','hino','isuzu','mack','western','harley','kawasaki',
  'suzuki','yamaha','ducati','triumph','indian','polaris','can','sea','forest','keystone','jayco','grand','gulf','utility',
  'great','big','club','john','ditch','thomas','bluebird','ic','others','carry','erie','highland','24','kubota','bobcat',
  'caterpillar','cat','case','wabash','hyundai-translead','trail','load','pj','pace','cargo','haulmark','sun','coachmen',
  'thor','winnebago','fleetwood','tiffin','newmar','airstream','heartland','dutchmen','crossroads','cruiser','palomino',
  'starcraft','skyline','honda-motorcycle','bmw-motorcycle','ktm','aprilia','vespa','husqvarna','sea-doo','yamaha-boat',
  'bayliner','sea-ray','tracker','lund','ranger-boats','skeeter','mastercraft','malibu-boats','bennington','godfrey',
  'freightlin','navistar','sterling','ottawa','capacity','volvo-truck','gillig','new-flyer','blue','collins','starcraft-bus',
  'elkhart','supreme','morgan','rvision','felling','doolittle','lamar','maxx','kaufman','cronkhite','anderson','sure','texas',
  'iron','diamond','wells','interstate','american','continental','fontaine','east','mac','landoll','talbert','kalyn','trailmobile',
  'stoughton','vanguard','manac','strick','dorsey','reitnouer','transcraft','xl','witzco','eager','trail-king','towmaster',
  'homemade','shopmade','asv','takeuchi','genie','jlg','skyjack','toro','exmark','scag','hustler','gravely','ariens','cub',
  'craftsman','troy','husky','generac','miller','lincoln-electric','multiquip','wacker','ingersoll','atlas','doosan','sullair',
  'kioti','mahindra','ls','branson','yanmar','new-holland','massey','deere','kenworth-truck','peterbilt-truck','tesla-semi',
  'workhorse','nikola','blue-bird','unknown','unk','not','no'}
# models that are OTHER regardless of make (class 3+ trucks, chassis, buses, motorcycles)
OTHER_MODELS = {'f350','f450','f550','f650','f750','f59','f53','e450','e350','3500','4500','5500','npr','nqr','nrr','frr',
  'cascadia','m2','business','chassis','columbia','t680','t800','t880','w900','579','389','379','4300','4400','7400','4000',
  'lt625','mv607','durastar','prostar','lonestar','workstar','195','258','268','338','conventional','vnl','vnr','vhd','vn',
  'davidson','zx636','zx6r','zx10r','ninja','gsx','gsxr','r1','r6','mt07','mt09','fz','cbr','cb','crf','grom','rebel',
  'motorcycle','rzr','sportsman','general','outlander-atv','commander','maverick-x3','defender','am','doo','river','cougar',
  'springdale','hideout','coleman','jay','design','stream','dane','tex','car','deere','witch','saf','minotour','vision',
  'corporation','1','4','frame','pcs','industries','ridge','on','vs2ra','trailer','semi','cutaway','stripped','motorhome',
  'rv','bus','ambulance','fire','sweeper','wrecker','rollback','dump','mixer','refuse','tractor','step','box','utility-van',
  'express-cutaway','savana-cutaway','sprinter-3500','sprinter-4500','promaster-3500'}
PICKUP = {('ford','f150'),('ford','f'),('ford','f250'),('ford','ranger'),('ford','maverick'),('ford','lightning'),
  ('chevrolet','silverado'),('chevrolet','colorado'),('chevrolet','s'),('chevrolet','s10'),('chevrolet','avalanche'),('chevrolet','c'),('chevrolet','k'),
  ('gmc','sierra'),('gmc','canyon'),('gmc','sonoma'),('ram','1500'),('ram','2500'),('ram','ram'),('dodge','ram'),('dodge','dakota'),
  ('toyota','tacoma'),('toyota','tundra'),('toyota','pickup'),('toyota','t100'),('nissan','frontier'),('nissan','titan'),
  ('honda','ridgeline'),('jeep','gladiator'),('jeep','comanche'),('rivian','r1t'),('tesla','cybertruck'),('hyundai','santa-cruz'),
  ('ford','f100'),('mazda','b'),('mitsubishi','raider'),('lincoln','mark-lt'),('cadillac','escalade-ext'),('gmc','hummer')}
VAN = {('ford','transit'),('ford','econoline'),('ford','e150'),('ford','e250'),('ford','e'),('ram','promaster'),('dodge','grand'),
  ('dodge','caravan'),('chrysler','pacifica'),('chrysler','town'),('chrysler','voyager'),('honda','odyssey'),('toyota','sienna'),
  ('kia','sedona'),('kia','carnival'),('nissan','quest'),('nissan','nv200'),('nissan','nv'),('chevrolet','express'),('gmc','savana'),
  ('chevrolet','city'),('chevrolet','uplander'),('chevrolet','venture'),('chevrolet','astro'),('gmc','safari'),('mercedes','benz-sprinter'),
  ('mercedes','benz-metris'),('ford','freestar'),('ford','windstar'),('mazda','mpv'),('mazda','5'),('volkswagen','routan'),('pontiac','montana'),
  ('buick','terraza'),('saturn','relay'),('oldsmobile','silhouette'),('mercury','villager'),('mercury','monterey')}
SUV = {('toyota','rav4'),('toyota','highlander'),('toyota','4runner'),('toyota','sequoia'),('toyota','venza'),('toyota','land'),
  ('toyota','fj'),('toyota','c'),('toyota','grand'),('toyota','corolla-cross'),('toyota','bz4x'),('toyota','crown-signia'),
  ('honda','cr'),('honda','hr'),('honda','pilot'),('honda','passport'),('honda','element'),('honda','prologue'),
  ('ford','escape'),('ford','explorer'),('ford','edge'),('ford','expedition'),('ford','bronco'),('ford','ecosport'),('ford','flex'),
  ('ford','mustang-mach'),('ford','excursion'),('ford','freestyle'),('ford','taurus-x'),
  ('chevrolet','equinox'),('chevrolet','traverse'),('chevrolet','trax'),('chevrolet','tahoe'),('chevrolet','suburban'),('chevrolet','blazer'),
  ('chevrolet','trailblazer'),('chevrolet','captiva'),('chevrolet','hhr'),('chevrolet','bolt-euv'),('chevrolet','gmt'),
  ('gmc','terrain'),('gmc','acadia'),('gmc','yukon'),('gmc','envoy'),('gmc','jimmy'),
  ('nissan','rogue'),('nissan','pathfinder'),('nissan','murano'),('nissan','kicks'),('nissan','armada'),('nissan','xterra'),('nissan','juke'),('nissan','ariya'),
  ('hyundai','santa'),('hyundai','tucson'),('hyundai','kona'),('hyundai','venue'),('hyundai','palisade'),('hyundai','ioniq-5'),('hyundai','nexo'),
  ('kia','sorento'),('kia','sportage'),('kia','telluride'),('kia','seltos'),('kia','soul'),('kia','niro'),('kia','ev6'),('kia','ev9'),('kia','borrego'),
  ('jeep','grand'),('jeep','cherokee'),('jeep','wrangler'),('jeep','compass'),('jeep','renegade'),('jeep','patriot'),('jeep','liberty'),
  ('jeep','wagoneer'),('jeep','commander'),
  ('subaru','outback'),('subaru','forester'),('subaru','crosstrek'),('subaru','ascent'),('subaru','xv'),('subaru','tribeca'),('subaru','solterra'),
  ('mazda','cx'),('mazda','tribute'),('mitsubishi','outlander'),('mitsubishi','eclipse-cross'),('mitsubishi','montero'),('mitsubishi','endeavor'),
  ('volkswagen','tiguan'),('volkswagen','atlas'),('volkswagen','taos'),('volkswagen','touareg'),('volkswagen','id'),
  ('dodge','durango'),('dodge','journey'),('dodge','nitro'),('dodge','hornet'),
  ('lexus','rx'),('lexus','nx'),('lexus','gx'),('lexus','lx'),('lexus','ux'),('lexus','tx'),('lexus','rz'),
  ('bmw','x1'),('bmw','x2'),('bmw','x3'),('bmw','x4'),('bmw','x5'),('bmw','x6'),('bmw','x7'),('bmw','ix'),
  ('audi','q3'),('audi','q5'),('audi','q7'),('audi','q8'),('audi','sq5'),('audi','sq7'),('audi','e'),('audi','q4'),
  ('mercedes','benz-gl'),('mercedes','benz-ml'),('mercedes','benz-gle'),('mercedes','benz-glc'),('mercedes','benz-gla'),('mercedes','benz-glb'),
  ('mercedes','benz-gls'),('mercedes','benz-glk'),('mercedes','benz-g'),('mercedes','benz-eqb'),('mercedes','benz-eqe-suv'),('mercedes','benz-eqs-suv'),('mercedes','benz-r'),
  ('volvo','xc90'),('volvo','xc60'),('volvo','xc40'),('volvo','xc70'),('volvo','ex30'),('volvo','ex90'),
  ('cadillac','escalade'),('cadillac','srx'),('cadillac','xt5'),('cadillac','xt4'),('cadillac','xt6'),('cadillac','lyriq'),
  ('buick','encore'),('buick','enclave'),('buick','envision'),('buick','envista'),('buick','rendezvous'),('buick','rainier'),
  ('infiniti','qx60'),('infiniti','qx50'),('infiniti','qx80'),('infiniti','qx56'),('infiniti','qx30'),('infiniti','qx70'),('infiniti','fx35'),
  ('infiniti','fx45'),('infiniti','fx37'),('infiniti','jx35'),('infiniti','qx4'),
  ('acura','mdx'),('acura','rdx'),('acura','zdx'),('lincoln','mkx'),('lincoln','mkc'),('lincoln','navigator'),('lincoln','nautilus'),
  ('lincoln','aviator'),('lincoln','corsair'),('lincoln','mkt'),
  ('porsche','cayenne'),('porsche','macan'),('jaguar','f-pace'),('jaguar','e-pace'),('jaguar','i'),('land','rover'),('alfa','romeo-stelvio'),
  ('maserati','levante'),('maserati','grecale'),('genesis','gv70'),('genesis','gv80'),('genesis','gv60'),('tesla','model-x'),('tesla','model-y'),
  ('hummer','h2'),('hummer','h3'),('saturn','vue'),('saturn','outlook'),('pontiac','torrent'),('pontiac','aztek'),('mercury','mountaineer'),
  ('mercury','mariner'),('fiat','500x'),('fiat','500l'),('mini','countryman'),('mini','paceman'),('rivian','r1s'),('isuzu','rodeo'),('isuzu','trooper'),
  ('suzuki','grand'),('suzuki','xl7'),('oldsmobile','bravada'),('chrysler','aspen'),('vinfast','vf8'),('vinfast','vf9'),('lucid','gravity'),
  ('scion','xb'),('toyota','matrix'),('pontiac','vibe')}
# ambiguous crossovers: EPA classes them as station wagons (cars) in some years; Ward's/BEA as light trucks
AMBIG = {('subaru','outback'),('kia','soul'),('kia','niro'),('kia','ev6'),('subaru','crosstrek'),('subaru','xv'),('nissan','kicks'),
  ('chevrolet','hhr'),('scion','xb'),('toyota','matrix'),('pontiac','vibe'),('honda','element'),('audi','e'),('volkswagen','id'),('hyundai','ioniq-5')}
PASSENGER_MAKES = {'toyota','honda','ford','chevrolet','chev','chevy','nissan','hyundai','kia','jeep','ram','dodge','gmc','subaru','mazda','mitsubishi',
  'volkswagen','lexus','bmw','audi','mercedes','volvo','cadillac','buick','infiniti','acura','lincoln','porsche','jaguar','land','alfa',
  'maserati','genesis','tesla','hummer','saturn','pontiac','mercury','fiat','mini','rivian','chrysler','scion','lucid','vinfast','oldsmobile',
  'plymouth','saab','smart','bentley','rolls','ferrari','lamborghini','aston','lotus','mclaren','fisker','polestar','geo','eagle','isuzu','suzuki','daewoo'}

def classify(mm):
    """mm = make_model slug tokens joined by '-', e.g. 'ford-f150-supercrew', 'mercedes-benz-glc-300', 'tesla-model-y'."""
    t = mm.split('-')
    if len(t) < 1 or not t[0]: return 'UNK', ''
    mk = t[0]
    if mk in ('chev', 'chevy'): mk = 'chevrolet'
    if mk in OTHER_MAKES: return 'OTHER', mk
    md = t[1] if len(t) > 1 else ''
    md2 = '-'.join(t[1:3]) if len(t) > 2 else md   # 'benz-glc', 'model-y', 'f-pace', 'santa-cruz'
    if md in OTHER_MODELS: return 'OTHER', mk + '-' + md
    if mk == 'mercedes':
        for k in (md2, ) :
            for pre in ('benz-sprinter', 'benz-metris'):
                if k.startswith(pre): return 'VAN', mk + '-' + pre
            for pre in ('benz-gl', 'benz-ml', 'benz-g', 'benz-r', 'benz-eqb'):
                if k.startswith(pre) and not k.startswith('benz-glass'): return 'SUV', mk + '-' + pre
        if md2 in ('benz-sprinter',): return 'VAN', md2
        return ('CAR', mk + '-' + md2) if mk in PASSENGER_MAKES else ('OTHER', mk)
    if mk in ('isuzu',) and md in ('npr', 'nqr', 'nrr', 'frr', 'ftr'): return 'OTHER', mk + '-' + md
    for key in ((mk, md2), (mk, md)):  # noqa
        if key in PICKUP: return 'PICKUP', '-'.join(key)
        if key in VAN: return 'VAN', '-'.join(key)
        if key in SUV: return 'SUV', '-'.join(key)
    if mk == 'ford' and md == 'mustang' and len(t) > 2 and t[2] == 'mach': return 'SUV', 'ford-mustang-mach'
    if mk == 'tesla' and md == 'model': return ('SUV' if md2 in ('model-x', 'model-y') else 'CAR'), md2
    if mk == 'jaguar' and md == 'f': return ('SUV' if md2 == 'f-pace' else 'CAR'), md2
    if mk == 'alfa': return ('SUV' if 'stelvio' in mm else 'CAR'), md2
    if mk == 'mitsubishi' and md == 'eclipse': return ('SUV' if md2 == 'eclipse-cross' else 'CAR'), md2
    if mk == 'toyota' and md == 'corolla': return ('SUV' if md2 == 'corolla-cross' else 'CAR'), md2
    if mk == 'hyundai' and md == 'santa': return ('PICKUP' if md2 == 'santa-cruz' else 'SUV'), md2
    if mk == 'hyundai' and md == 'ioniq': return ('SUV' if md2 == 'ioniq-5' else 'CAR'), md2
    if mk in PASSENGER_MAKES: return 'CAR', mk + '-' + md
    return 'UNK', mk

LT = {'PICKUP', 'SUV', 'VAN'}
rx = re.compile(r'/lot/(\d+)/([^<?#"]*)')
def parse_slug(slug):
    """'salvage-2015-ford-f150-supercrew-tx-houston' → (title, year, make_model_tokens)"""
    sl = slug.lower().strip('/')
    m = re.search(r'(?:^|-)((?:19|20)\d\d)-', sl)
    if not m: return None
    title = sl[:m.start()].strip('-'); rest = sl[m.end():]
    return title, int(m.group(1)), rest

def tally(iter_lots):
    c = collections.Counter(); amb = collections.Counter(); seen = set(); years = []; ex = collections.Counter()
    for lot_id, title, year, mm in iter_lots:
        if lot_id in seen: continue
        seen.add(lot_id)
        cls, key = classify(mm)
        sal = 'salvage' if title.startswith('salvage') or title.startswith('non') else ('clean' if title.startswith('clean') else 'other')
        c[(cls, sal)] += 1
        mk = tuple(mm.split('-')[:2])
        if mk in AMBIG or (mk[0], '-'.join(mm.split('-')[1:3])) in AMBIG: amb[sal] += 1
        if cls in LT or cls == 'CAR': years.append((year, cls in LT))
        if cls == 'UNK': ex[key] += 1
    return c, amb, years, ex

def stats(c, amb, years):
    def sh(sal):
        car = sum(v for (cl, s), v in c.items() if cl == 'CAR' and (sal is None or s == sal))
        lt = sum(v for (cl, s), v in c.items() if cl in LT and (sal is None or s == sal))
        a = amb[sal] if sal else sum(amb.values())
        n = car + lt
        return (lt / n * 100 if n else None, (lt - a) / n * 100 if n else None, n)
    tot = sum(c.values())
    other = sum(v for (cl, s), v in c.items() if cl == 'OTHER'); unk = sum(v for (cl, s), v in c.items() if cl == 'UNK')
    pick = sum(v for (cl, s), v in c.items() if cl == 'PICKUP'); suv = sum(v for (cl, s), v in c.items() if cl == 'SUV'); van = sum(v for (cl, s), v in c.items() if cl == 'VAN')
    allsh, allsh_lo, n_all = sh(None); salsh, salsh_lo, n_sal = sh('salvage'); clsh, clsh_lo, n_cl = sh('clean')
    ly = [y for y, lt in years if lt]; cy = [y for y, lt in years if not lt]
    import statistics as st
    R = lambda x: round(x, 2) if x is not None else None
    return dict(lots=tot, light_classified=n_all, other=other, unclassified=unk, pickup=pick, suv=suv, van=van,
                lt_share_all=R(allsh), lt_share_all_exambig=R(allsh_lo), lt_share_salvage=R(salsh),
                lt_share_salvage_exambig=R(salsh_lo), lt_share_clean=R(clsh),
                n_salvage=n_sal, n_clean=n_cl, median_my_lt=int(st.median(ly)) if ly else None, median_my_car=int(st.median(cy)) if cy else None)

rows = []; unk_total = collections.Counter()
# ---- archived captures, grouped by capture month, union of pages
files = collections.defaultdict(list)
for f in glob.glob(str(ROOT / 'raw/lotxml/lotxml_p*_*.xml')):
    m = re.search(r'lotxml_p(\d)_(\d{6})', f); files[m.group(2)].append(f)
for month in sorted(files):
    def it():
        for f in files[month]:
            txt = open(f, encoding='utf-8', errors='ignore').read()
            for m in rx.finditer(txt):
                p = parse_slug(m.group(2))
                if p: yield int(m.group(1)), p[0], p[1], p[2]
    c, amb, years, ex = tally(it()); unk_total.update(ex)
    rows.append(dict(month=month, source='archive', pages=len(files[month]), **stats(c, amb, years)))
# ---- live nightly captures
con = sqlite3.connect(ROOT / 'data/cprt.db')
for (night,) in con.execute("SELECT DISTINCT substr(snapshot_utc,1,10) FROM lot_snapshots ORDER BY 1"):
    def it2():
        for lot_id, title, year, mm in con.execute("SELECT lot_id,title_type,year,make_model FROM lot_snapshots WHERE substr(snapshot_utc,1,10)=?", (night,)):
            yield lot_id, (title or ''), (year or 0), (mm or '')
    c, amb, years, ex = tally(it2()); unk_total.update(ex)
    rows.append(dict(month=night.replace('-', '')[:8], source='live', pages='', **stats(c, amb, years)))

hdr = ("# E1 step 1 (scripts/experiments/e1_listed_body_share.py): light-truck share of Copart's LISTED pool by capture, from lot slugs; "
       "LT = pickup (<=10,000 lb) + SUV/crossover + van on Ward's/EPA convention; share = LT/(CAR+LT); *_exambig treats ambiguous crossovers "
       "(Outback, Soul, Niro, EV6, Crosstrek, Kicks, HHR, Element...) as cars. Archive rows = Internet Archive captures (union of pages, "
       "may be out of sync -> use as level check only); live rows = nightly lot_snapshots. Listed pool, not total losses; includes clean-title. No network.\n")
with open(OUT, 'w', newline='') as f:
    f.write(hdr); w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(f"{'capture':9s} {'src':7s} {'lots':>7s} {'lightcls':>8s} {'other':>6s} {'unk':>5s} {'LT%all':>7s} {'exAmb':>6s} {'LT%salv':>7s} {'LT%clean':>8s} {'medMY LT/car':>12s}")
for r in rows:
    g = lambda v: f"{v:7.1f}" if v is not None else "      -"
    print(f"{r['month']:9s} {r['source']:7s} {r['lots']:7d} {r['light_classified']:8d} {r['other']:6d} {r['unclassified']:5d} {g(r['lt_share_all'])} {g(r['lt_share_all_exambig'])} "
          f"{g(r['lt_share_salvage'])} {g(r['lt_share_clean'])} {str(r['median_my_lt']):>5s}/{str(r['median_my_car']):<5s}")
print("\nTop unclassified make tokens (check these are not light vehicles):")
for k, v in unk_total.most_common(25): print(f"  {k:20s} {v}")
