"""Small published-series compatibility screen, not a claims forecast."""
import json,math
from pathlib import Path

rows=[]
for name,p0,p1,repair_growth,valuation_growth,claims_growth in [
    ('all_coverages',.223,.231,-.097,-.029,-.077),
    ('non_comprehensive',.229,.239,-.08,-.002,-.057)]:
    # Only valid as empirical reconstruction IF populations/panels match.
    implied_t=(1+claims_growth)*p1/p0-1
    implied_r=(1+claims_growth)*(1-p1)/(1-p0)-1
    combined=p0*(1+valuation_growth)+(1-p0)*(1+repair_growth)
    hypothetical_p=p0*(1+valuation_growth)/combined
    assert math.isclose(p0*(1+implied_t)+(1-p0)*(1+implied_r),1+claims_growth)
    rows.append(dict(scope=name,p0=p0,p1=p1,reported_claim_growth=claims_growth,
        reported_repairable_growth=repair_growth,reported_valuation_growth=valuation_growth,
        same_population_implied_total_loss_growth=implied_t,
        same_population_implied_repairable_growth=implied_r,
        implied_minus_reported_repairable_pp=100*(implied_r-repair_growth),
        hypothetical_combined_claim_growth=combined-1,
        hypothetical_combined_TLF=hypothetical_p,
        hypothetical_TLF_gap_pp=100*(hypothetical_p-p1)))
out={'rows':rows,'status':'Compatibility diagnostic only; valuation counts are not confirmed flagged-total-loss counts. No nonfiling estimate or forecast input.',
     'sources':{'annual':'https://www.cccis.com/reports/crash-course-2026',
                'recap':'https://www.cccis.com/news-and-insights/posts/crash-course-2026-webinar-recap'},
     'accessed':'2026-09-28','baseline_TLF':'Derived from published 2025 level less stated percentage-point increase'}
Path(__file__).with_name('count_compatibility_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(rows,indent=2))
