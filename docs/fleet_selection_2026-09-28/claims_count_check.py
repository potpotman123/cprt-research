"""CCC disclosed count-proxy changes and their compatibility with TLF."""
import hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
source=ROOT/'raw/ccc/crash-course-2026.txt'
cases=[('all_categories',22.3,23.1,-2.9,-9.7),('non_comprehensive',22.9,23.9,-.2,-8)]
results=[]
for label,p0,p1,tl,repair in cases:
    p0/=100;p1/=100;t=1+tl/100;r=1+repair/100
    # Counterfactual identities, valid only for a common, exhaustive claims population.
    total=p0*t+(1-p0)*r
    rate_from_counts=p0*t/total
    claims_from_tl=t*p0/p1
    repair_from_tl=claims_from_tl*(1-p1)/(1-p0)
    tl_from_repair=r*(p1/(1-p1))/(p0/(1-p0))
    assert math.isclose(total*rate_from_counts,p0*t,rel_tol=1e-12)
    results.append(dict(scope=label,reported_tlf_start_pct=p0*100,reported_tlf_end_pct=p1*100,
        reported_valuation_count_change_pct=tl,reported_repairable_volume_change_pct=repair,
        conditional_tlf_from_count_proxies_pct=100*rate_from_counts,
        tlf_gap_pp=100*(rate_from_counts-p1),
        conditional_all_claim_count_change_pct=100*(total-1),
        conditional_repairable_change_from_valuations_and_tlf_pct=100*(repair_from_tl-1),
        conditional_total_loss_count_change_from_repairables_and_tlf_pct=100*(tl_from_repair-1),
        matched_claim_count_break_even_change_pct=100*(p0/p1-1)))
output={'source':str(source.relative_to(ROOT)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'source_locations':'lines 183-184: valuations and TLF; line 264: repairables',
 'period':'CY2025 versus CY2024','status':'Count proxies disclosed; common-population identities fail to reconcile. Do not adopt inferred counts as observed.',
 'results':results}
Path(__file__).with_name('claims_count_results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(results,indent=2))
