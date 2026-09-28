"""Reported history and same-quarter driver bridge; no fitted quarterly residuals.

The original absolute reconstruction remains a separate, failed diagnostic.
Revenue anchors do not identify absolute operating units or branch shares.
"""
import hashlib,json
import engine as m


def operating_bridge(d):
    rows=[]
    for geography,field in [('US','us_service'),('International','intl_service')]:
        for i,(prior,current) in enumerate(zip(d['prior_actuals'],d['actuals'])):
            a,b=prior[field],current[field]
            units=rpu=None
            if geography=='International':
                rpu=[.081,.076,.105,.035][i]
                source='raw/transcripts/call_'+['2025-11-20','2026-02-19','2026-05-21','2026-09-10'][i]+'.txt'
                measured='RPU'; inferred='Fee-unit growth, revenue identity; rounded input'
            elif i==0:
                rpu=.075;source='raw/transcripts/call_2025-11-20.txt'
                measured='RPU';inferred='Fee-unit growth, revenue identity; rounded input'
            elif i in (1,2):
                units={1:-.09,2:-.033}[i]
                source='Stephens 20 Aug 2026, Exhibit 7, PDF p7; docs/legacy_foundation_2026-09-28/HISTORICAL_BRIDGE.md'
                measured='Broker-compiled fee-unit growth';inferred='RPU growth, revenue identity; rounded input'
            else:
                source='No compatible fee-unit/RPU split available'
                measured='Neither';inferred='Neither'
            if rpu is not None:units=b/a/(1+rpu)-1
            elif units is not None:rpu=b/a/(1+units)-1
            known=units is not None
            volume=a*units if known else None
            price=a*rpu if known else None
            interaction=a*units*rpu if known else None
            unallocated=0 if known else b-a
            rows.append(dict(period=f'FY{current["fy"]}Q{current["q"]}',geography=geography,
                prior_service_musd=a,reported_service_musd=b,service_growth=b/a-1,
                fee_unit_growth=units,fee_RPU_growth=rpu,volume_change_musd=volume,
                RPU_change_musd=price,interaction_musd=interaction,unallocated_change_musd=unallocated,
                directly_sourced_metric=measured,identity_derived_metric=inferred,source=source,
                population='All geography fee-service activity; NOT insurance-only units',
                validation='Accounting identity only; absolute unit levels and historical seasonality not identified'))
    return rows


def build(d,c,result):
    rows=[];share=c['insurance_share_of_us_service_base']
    for i,raw in enumerate(result['quarters']):
        row=dict(period=raw['period'],reported_us_musd=None,reported_intl_musd=None,
            assumed_insurance_base_musd=None,assumed_other_us_base_musd=None,
            exposure_frequency_factor=None,total_loss_factor=None,capture_factor=None,
            insurance_units_factor=None,insurance_RPU_factor=None,
            insurance_anchor_to_raw_base_ratio=None,other_us_anchor_to_raw_base_ratio=None,intl_anchor_to_raw_base_ratio=None,
            insurance_musd=None,other_us_musd=None,intl_musd=None,us_musd=None,legacy_service_musd=None,
            original_reconstruction_service_musd=raw['legacy_service_musd'],
            original_reconstruction_error_musd=None,status='')
        if i<4:
            a=d['actuals'][i]
            row.update(reported_us_musd=a['us_service'],reported_intl_musd=a['intl_service'],
                us_musd=a['us_service'],intl_musd=a['intl_service'],
                legacy_service_musd=a['us_service']+a['intl_service'],
                original_reconstruction_error_musd=raw['legacy_service_musd']-a['us_service']-a['intl_service'],
                status='Reported dollars; historical insurance split and absolute units unavailable; not a successful reconstruction')
        else:
            base=result['quarters'][i-4];a=d['actuals'][i-4]
            # The same-quarter revenue seasonal proxy and common Q4 scale cancel.
            exposure=raw['claims_raw']/base['claims_raw']
            tlf=raw['TLF']/base['TLF'];capture=raw['effective_capture']/base['effective_capture']
            units=exposure*tlf*capture
            rpu=raw['insurance_allin_RPU']/base['insurance_allin_RPU']
            ins=a['us_service']*share*units*rpu
            other=a['us_service']*(1-share)*raw['other_us_musd']/base['other_us_musd']
            intl=a['intl_service']*raw['intl_musd']/base['intl_musd']
            row.update(assumed_insurance_base_musd=a['us_service']*share,
                assumed_other_us_base_musd=a['us_service']*(1-share),
                exposure_frequency_factor=exposure,total_loss_factor=tlf,capture_factor=capture,
                insurance_units_factor=units,insurance_RPU_factor=rpu,
                insurance_anchor_to_raw_base_ratio=a['us_service']*share/base['insurance_musd'],
                other_us_anchor_to_raw_base_ratio=a['us_service']*(1-share)/base['other_us_musd'],
                intl_anchor_to_raw_base_ratio=a['intl_service']/base['intl_musd'],
                insurance_musd=ins,other_us_musd=other,intl_musd=intl,us_musd=ins+other,
                legacy_service_musd=ins+other+intl,
                status='Same-quarter reported revenue anchor times provisional driver ratios; not independently validated')
        rows.append(row)
    return rows


def main():
    d,e,c=m.load();result=m.run(d,e,c)
    rows=build(d,c,result);bridge=operating_bridge(d)
    m.save_csv('reconciled_quarterly_service.csv',rows)
    m.save_csv('historical_operating_bridge.csv',bridge)
    paths=[m.OLD,m.ECON,m.HERE/'assumptions.json',m.HERE/'engine.py',m.HERE/'history_repair.py',m.ROOT/'docs/legacy_foundation_2026-09-28/HISTORICAL_BRIDGE.md']
    (m.HERE/'history_repair_manifest.json').write_text(json.dumps({
        'version':'same-quarter-driver-bridge-v2',
        'source_hashes':{str(p.relative_to(m.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        'status':'Historical accounting controls repaired; causal reconstruction remains unresolved',
        'assumption':'Same-quarter reported revenue is the base; unmodeled historical level differences persist proportionately for one year',
        'historical_insurance_share':c['insurance_share_of_us_service_base'],
        'insurance_share_status':'Same 90% assumption transferred to each historical quarter; not disclosed',
        'absolute_unit_levels_identified':False,'predictive_validation_passed':False,
        'acquisition':'Excluded from revised legacy table; existing acquisition_gate.csv remains separate'
    },indent=2)+'\n')
    print(json.dumps({'forecast_service_musd':[r['legacy_service_musd'] for r in rows[4:]],
        'historical_reconstruction_errors_preserved':[r['original_reconstruction_error_musd'] for r in rows[:4]]}))

if __name__=='__main__':main()
