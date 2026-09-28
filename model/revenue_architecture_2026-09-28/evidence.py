"""Targeted extraction of existing reports and immutable historical controls."""
import csv
import hashlib
import json
from pathlib import Path
import model as m

SOURCE_DIR=Path('/Users/kwu/Documents/ChatGPT/HFAC x Citadel/research/cprt_discovery_plan_2026-09-26/sources')


def build():
    jpm=next(SOURCE_DIR.glob('2026-09-11*124345098.txt'))
    lines=jpm.read_text().splitlines()
    table_start=next(i for i,s in enumerate(lines) if s.startswith('Table 3: CPRT Summary Model'))
    def row(prefix):
        found=[(i+1,s) for i,s in enumerate(lines) if table_start < i < table_start+30 and s.startswith(prefix)]
        if len(found)!=1: raise ValueError('Ambiguous broker row '+prefix)
        n,s=found[0]
        return [float(x.replace(',','')) for x in s[len(prefix):].split()],n
    agency,al=row('Agency revenue ')
    principal,pl=row('Principal revenue ')
    total,tl=row('Total revenues ')
    header=next(i for i,s in enumerate(lines) if s.startswith('Income Statement - Quarterly'))
    qline=next(i for i in range(header+1,header+6) if lines[i].startswith('Revenue '))
    quarter=[float(x.replace(',','')) for x in lines[qline].split()[1:]]
    assert len(agency)==len(principal)==len(total)==14 and len(quarter)==4
    assert 'estimates do not reflect' in '\n'.join(lines[35:42])
    assert abs(sum(quarter)-total[-2])<=2 # Printed quarterly/annual rounding.
    d,_,_=m.old.load()
    with (m.ROOT/'docs/consensus_review_2026-09-28/total_revenue_consensus.csv').open() as f: capiq=list(csv.DictReader(f))[:4]
    perimeter=[]
    for q in range(4):
        a=d['actuals'][q]
        perimeter.append(dict(period=f'FY2027Q{q+1}',prior_service_musd=a['us_service']+a['intl_service'],
            prior_purchased_musd=a['us_vehicle']+a['intl_vehicle'],capiq_total_musd=float(capiq[q]['total_revenue_mean_m']),
            capiq_service_musd=None,capiq_acquisition_scope='unverified',capiq_asof='2026-09-28',
            jpm_total_musd=quarter[q],jpm_service_musd=None,jpm_acquisition_scope='excludes ACV',jpm_asof='2026-09-11'))
    perimeter.append(dict(period='FY2027',prior_service_musd=sum(x['us_service']+x['intl_service'] for x in d['actuals']),
        prior_purchased_musd=sum(x['us_vehicle']+x['intl_vehicle'] for x in d['actuals']),
        capiq_total_musd=sum(float(x['total_revenue_mean_m']) for x in capiq),capiq_service_musd=None,
        capiq_acquisition_scope='unverified',capiq_asof='2026-09-28',jpm_total_musd=total[-2],jpm_service_musd=agency[-2],
        jpm_acquisition_scope='excludes ACV',jpm_asof='2026-09-11'))
    m.write_csv(m.HERE/'benchmark_perimeter.csv',perimeter)
    with (m.LEGACY/'historical_operating_bridge.csv').open() as f: history=list(csv.DictReader(f))
    # Preserve official/identity-derived history; add broker evidence as a separate row.
    history.append(dict(period='FY2026Q4',geography='US',prior_service_musd=d['prior_actuals'][3]['us_service'],
        reported_service_musd=d['actuals'][3]['us_service'],service_growth=None,fee_unit_growth=None,fee_RPU_growth=.05,
        volume_change_musd=None,RPU_change_musd=None,interaction_musd=None,unallocated_change_musd=None,
        directly_sourced_metric='JPM estimate of reported quarter RPU, approximately 5%',identity_derived_metric='None',
        source=f'{jpm}:43',population='All-US service RPU; broker estimate',validation='Soft cross-check only, not company disclosure'))
    m.write_csv(m.HERE/'historical_metric_controls.csv',history)
    manifest=dict(jpm_source=str(jpm),jpm_sha256=hashlib.sha256(jpm.read_bytes()).hexdigest(),
        jpm_agency_row=al,jpm_principal_row=pl,jpm_total_row=tl,jpm_quarter_row=qline+1,
        jpm_fy27_service_musd=agency[-2],jpm_fy27_purchased_musd=principal[-2],jpm_fy27_total_musd=total[-2],
        jpm_quarter_sum_musd=sum(quarter),rounding_difference_musd=sum(quarter)-total[-2],
        service_growth_vs_reported_FY26=agency[-2]/perimeter[-1]['prior_service_musd']-1,
        capiq_minus_jpm_fy27_musd=perimeter[-1]['capiq_total_musd']-total[-2],
        quarterly_jpm_service='Not disclosed in extracted summary; do not allocate annual agency forecast as observed quarters',
        absolute_insurance_units_identified=False,insurance_service_fraction_identified=False,
        title_delivery_levels_identified=False,
        independent_equations='Observed US service total alone cannot identify core insurance, other core, title and delivery levels',
        external_research='See EVIDENCE_UPDATE.md for bounded primary-source pass and disconfirming observations')
    (m.HERE/'evidence_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


if __name__=='__main__': print(json.dumps(build(),indent=2))
