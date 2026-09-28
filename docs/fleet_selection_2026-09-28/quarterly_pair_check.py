"""Conditional count/TLF thresholds; illustrative TLF levels are not estimates."""
import json
from pathlib import Path

cases = []
for label, growth in [('all_categories', -.033), ('non_comprehensive', -.016)]:
    factor = 1 + growth
    required = 1 / factor - 1
    assert abs(factor * (1 + required) - 1) < 1e-12
    cases.append({'scope': label, 'reported_Q1_2026_claim_volume_yoy_pct': 100 * growth,
                  'required_relative_TLF_increase_for_flat_TL_count_pct': 100 * required})
examples = []
for end_tlf in [.24, .245, .25]:
    tl_factor = .984 * end_tlf / .24
    examples.append({'assumed_prior_TLF_pct': 24, 'assumed_current_TLF_pct': end_tlf * 100,
                     'conditional_TL_count_change_pct': 100 * (tl_factor - 1)})
out = {'source': 'https://www.cccis.com/news-and-insights/posts/crash-course-2026-webinar-recap',
       'published': '2026-05-20', 'accessed': '2026-09-28',
       'qualification': 'Requires claim counts and TLF for the same population and period. No matching quarterly TLF/count pair established. Claim-volume definition in recap not fully specified.',
       'break_even': cases,
       'illustrative_noncomp_examples_NOT_forecasts': examples}
Path(__file__).with_name('quarterly_pair_results.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
