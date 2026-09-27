"""Read existing local records only; preserve originals and tag scope gaps."""
import csv,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent; ROOT=P.parents[1]
paths=['data/csv/reported_units.csv','data/csv/units_decomp_panel_v2.csv','data/csv/decomposition.csv','data/csv/segment_service_rev_8k.csv','scripts/units_decomp_panel.py','MODEL_BLUEPRINT.md','findings.md']
def rows(p):
    with (ROOT/p).open() as f:return list(csv.DictReader(f))
reported={r['fiscal_q'].replace(' ',''):r for r in rows(paths[0])}
panel=rows(paths[1]); output=[]
for r in panel:
    fq=r['cprt_fq']; rr=reported.get(fq)
    cp=float(r['cprt_us_ins_excat']);pool=float(r['pool__ccc_all_coverage'])
    output.append(dict(fiscal_quarter=fq,calendar_proxy=r['calendar_q'],insurance_units_yoy_pct=r['cprt_us_ins_asrep'],insurance_excat_yoy_pct=r['cprt_us_ins_excat'],excat_status='Panel substitutes as-reported value; no distinct exCAT observation in reported_units.csv' if rr and not rr['us_ins_units_exCAT_yoy'] else 'Transcript-derived repository value; original call not reverified in this pass',claims_proxy_yoy_pct=r['claims__ccc_all_coverage'],claims_status='Annual CY2025 figure repeated each quarter; not quarterly observation' if r['calendar_q'].startswith('2025') else 'Scenario proxy/range; do not equate frequency to count',tlf_relative_change_pct=r['tlf_yoy_rel_pct'],tlf_status=r['tlf_source'],pool_proxy_yoy_pct=pool,additive_gap_pp=cp-pool,exact_relative_residual_pct=100*((1+cp/100)/(1+pool/100)-1),residual_status='Diagnostic only: period, population, timing, claims and TLF errors remain'))
with (P/'historical_insurance_evidence.csv').open('w',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=list(output[0]));wr.writeheader();wr.writerows(output)
freq=-.034;tlf=23.3/22.4-1;proxy=(1+freq)*(1+tlf)-1
checks={'records':len(output),'historical_data_modified':False,'new_network_requests':0,'fq4_frequency_only_pool_proxy_pct':proxy*100,'fq4_assignment_relative_residual_pct_if_exposure_flat':100*(.95/(1+proxy)-1),'fq4_ex_account_relative_residual_pct_if_exposure_flat':100*(1.023/(1+proxy)-1),'prior_year_insurance_unit_weight_implied_by_rounded_q4_growth':(-5.7-.2)/(-7.5-.2),'implied_weight_caveat':'Conditional on US total, insurance and non-insurance growth sharing the identical sold-unit scope. Prior FY25Q4 unit weight, not current share or service revenue weight. Rounding and source verification pending.','cy2025_copart_simple_four_quarter_mean_pct':(2-2-2.1-7.3)/4,'cy2025_copart_month_weighted_growth_approx_pct':(1*2+3*(-2)+3*(-2.1)+3*(-7.3)+2*(-4.8))/12,'calendar_average_caveat':'Neither arithmetic mean is exact annual volume growth without prior-year unit weights; the two stored research approaches conflict.'}
assert len(output)==6
for r in output:
    assert abs((1+r['pool_proxy_yoy_pct']/100)*(1+r['exact_relative_residual_pct']/100)-(1+float(r['insurance_excat_yoy_pct'])/100))<1e-12
checks['multiplicative_reconciliation_passed']=True
manifest={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
(P/'audit_results.json').write_text(json.dumps(checks,indent=2));(P/'input_manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(checks,indent=2))
