"""Read the user-supplied workbook without modifying it; standard library only."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET
import zipfile

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
BODY=[('Car',0,4),('Pickup',2,9),('Utility Vehicle',1,14),('Van',3,19)]
AGES=['Current Yr or Newer Group','1 - 3 Years Old','4 - 6 Years Old','7 Years and Older']

def write_csv(name, rows):
    with (HERE/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('workbook',type=Path);args=ap.parse_args()
    source=args.workbook; digest=hashlib.sha256(source.read_bytes()).hexdigest()
    raw=ROOT/'raw/ccc_direct_2026-09-29';raw.mkdir(parents=True,exist_ok=True)
    archived=raw/source.name
    if archived.exists() and hashlib.sha256(archived.read_bytes()).hexdigest()!=digest:
        raise ValueError('Different source already archived; use a new version')
    shutil.copy2(source,archived)
    with zipfile.ZipFile(source) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            strings=[''.join(el.itertext()) for el in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',NS)]
        wb=ET.fromstring(z.read('xl/workbook.xml'));sheets=wb.find('s:sheets',NS)
        assert len(sheets)==1 and sheets[0].get('name')=='Vehicle Type, Age'
        cells={}
        for c in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//s:sheetData/s:row/s:c',NS):
            if c.find('s:f',NS) is not None:raise ValueError('Unexpected formulas: review cached values before extraction')
            v=c.find('s:v',NS);kind=c.get('t')
            if kind=='inlineStr':value=''.join(c.find('s:is',NS).itertext())
            elif v is None:continue
            elif kind=='s':value=strings[int(v.text)]
            else:value=float(v.text)
            cells[c.get('r')]=value
    assert cells['A1']=='% of Claims Flagged Total Loss'
    assert cells['K1']=='Total Loss Mix by Vehicle Age and Vehicle Type'
    rows=[]; controls=[]; yearly=[]; checks=[]
    for j,y in enumerate(range(2020,2026)):
        left=chr(ord('C')+j);right=chr(ord('M')+j)
        assert int(cells[left+'3'])==int(cells[right+'3'])==y
        subset=[]
        for bi,(name,b,start) in enumerate(BODY):
            assert cells['A'+str(start)]==name
            for a,age in enumerate(AGES):
                tc=left+str(start+a);mc=right+str(5+4*a+bi)
                assert cells['B'+str(start+a)]==age
                assert cells['L'+str(5+4*a+bi)]==name
                rate,mix=cells[tc],cells[mc]
                assert 0<rate<1 and 0<mix<1
                subset.append(dict(year=y,source_body=name,model_body=b,age_group=a,source_age=age,
                    tlf=rate,tl_mix=mix,tlf_cell=tc,tl_mix_cell=mc,sheet='Vehicle Type, Age',source_sha256=digest))
        z=sum(r['tl_mix']/r['tlf'] for r in subset)
        for r in subset:r['derived_claim_weight']=(r['tl_mix']/r['tlf'])/z
        assert abs(sum(r['tl_mix'] for r in subset)-cells[right+'21'])<1e-12
        for bi,(name,b,start) in enumerate(BODY):
            own=[r for r in subset if r['model_body']==b]
            mix=sum(r['tl_mix'] for r in own);weight=sum(r['derived_claim_weight'] for r in own)
            implied=mix/(z*weight);reported=cells[left+str(start+4)]
            assert abs(mix-cells[right+str(27+bi)])<1e-12
            controls.append(dict(year=y,source_body=name,reported_tlf=reported,derived_tlf=implied,
                residual_percentage_points=100*(implied-reported),reported_tl_mix=mix,derived_claim_weight=weight,
                tlf_cell=left+str(start+4),mix_cell=right+str(27+bi)))
        yearly.append(dict(year=y,derived_tlf=1/z,claim_weights_sum=sum(r['derived_claim_weight'] for r in subset),tl_mix_sum=sum(r['tl_mix'] for r in subset)))
        rows+=subset
    write_csv('source_cells.csv',rows);write_csv('source_body_controls.csv',controls);write_csv('annual_derived.csv',yearly)
    previous={ (r['model_body'],r['age_group']):r for r in rows if r['year']==2024}
    within=mix=0.
    for r in [r for r in rows if r['year']==2025]:
        p=previous[r['model_body'],r['age_group']]
        within+=(p['derived_claim_weight']+r['derived_claim_weight'])/2*(r['tlf']-p['tlf'])
        mix+=(p['tlf']+r['tlf'])/2*(r['derived_claim_weight']-p['derived_claim_weight'])
    delta=yearly[-1]['derived_tlf']-yearly[-2]['derived_tlf']
    assert abs(within+mix-delta)<1e-12
    manifest=dict(source_filename=source.name,source_sha256=digest,raw_copy=str(archived.relative_to(ROOT)),
        received='2026-09-29',sheet='Vehicle Type, Age',source_cells=96,
        provenance='User supplied as CCC contact data; workbook has no explanatory footnotes or formula cells.',
        definitions_unknown=['Geography and coverage/loss exclusions','Sample/estimate maturity and revision policy','Whether Van includes commercial vans','Completeness of each year'],
        mapping_status='Car and Pickup direct label mapping; Utility Vehicle to SUV and Van to existing Van/minivan economics are proxies.',
        claim_weight_method='Normalize total_loss_mix / cell_total_loss_frequency, conditional on common population and partition.',
        max_body_tlf_residual_pp=max(abs(r['residual_percentage_points']) for r in controls),
        source_checks={'six_mix_totals_equal_one':True,'24_body_mix_controls_match':True,'96_rates_valid':True},
        decomposition_2024_to_2025=dict(tlf_change_pp=100*delta,within_cell_rate_pp=100*within,composition_pp=100*mix,
            interpretation='Symmetric arithmetic decomposition. Within-cell includes severity and within-7+ aging, not aftermarket causality.'))
    (HERE/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':main()
