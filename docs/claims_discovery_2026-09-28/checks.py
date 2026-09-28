"""Bounded source arithmetic; no causal estimates or forecast writes."""
import json, math
from pathlib import Path
P=Path(__file__).resolve().parent
inputs={
 'LexisNexis':{'period':'2022 to 2025, 2026 report landing-page summary','basis':'paid frequency; publisher panel, all vehicle ages','collision_growth':-.164,'PD_growth':-.035,'url':'https://risk.lexisnexis.com/insights-resources/white-paper/auto-insurance-trends-report','locator':'Bodily Injury Costs Dominate Claims Outcomes'},
 'Progressive':{'period':'Calendar 2023, 2024, 2025 YoY','basis':'personal auto incurred frequency; all vehicle ages','collision_growth':[-.07,-.08,-.05],'PD_growth':[0,-.04,-.02],'url':'https://www.progressiveproxy.com/Progressive-2025-Financial-Review.pdf','locator':'PDF page 65 / App.-A-64; frequency table'},
 'Boyd':{'period':'Calendar 2025 quarters YoY','basis':'management estimates of industry repairable claims; Q3 release attributes estimates to claims processing platforms, exact panel not specified','quarter_ranges_pct':{'Q1':[-10,-9],'Q2':[-8,-6],'Q3':[-5,-3],'Q4':[-4,-2]},'urls':['https://boydgroup.com/investor/investor-news/news-details/2025/Boyd-Group-Services-Inc--Reports-Third-Quarter-2025-Results-11-12-2025/default.aspx','https://s25.q4cdn.com/123825503/files/doc_financials/2025/ar/2025-Annual-Report.pdf'],'locators':['Q3 Outlook paragraphs 1-2','Annual Report printed page 3']}}
ln=inputs['LexisNexis'];p=inputs['Progressive']
coll=math.prod(1+x for x in p['collision_growth']);pd=math.prod(1+x for x in p['PD_growth'])
results={'LN_collision_frequency_index_2022_100':100*(1+ln['collision_growth']),'LN_PD_frequency_index_2022_100':100*(1+ln['PD_growth']),'LN_collision_to_PD_frequency_ratio_change_pct':100*((1+ln['collision_growth'])/(1+ln['PD_growth'])-1),'PGR_collision_frequency_index_2022_100':100*coll,'PGR_PD_frequency_index_2022_100':100*pd,'PGR_collision_to_PD_frequency_ratio_change_pct':100*(coll/pd-1),'PGR_2025_only_relative_ratio_change_pct':100*(.95/.98-1),'Boyd_Q1_to_Q4_improvement_in_YoY_rate_pp_range':[5,8]}
assert math.isclose(coll,.81282);assert math.isclose(pd,.9408)
assert results['LN_collision_to_PD_frequency_ratio_change_pct']<0
assert results['PGR_collision_to_PD_frequency_ratio_change_pct']<0
# Endpoints, not a sequential quarter-to-quarter volume calculation.
assert -4-(-9)==5 and -2-(-10)==8
out={'inputs':inputs,'derived':results,'checks_passed':5,'interpretation':'Relative frequency changes are descriptive, not missing-claim shares. Different paid/incurred bases and panels cannot be pooled. Boyd range is change in YoY rate, not sequential volume growth. No 13+ coefficient identified.'}
(P/'small_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(results,indent=2))
