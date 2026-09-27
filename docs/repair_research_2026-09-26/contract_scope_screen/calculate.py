from pathlib import Path
import json,hashlib
p=Path(__file__).parent
price=3850;commission=.04;discount=.20;carrier=621900;new=125000;rpu=950;cost=40e6
concession=price*commission*discount
out={'source_status':'Barclays analyst estimates, not verified contract terms','inputs':dict(price=price,commission=commission,discount=discount,carrier_volume=carrier,incremental_volume_midpoint=new,total_service_RPU=rpu,incremental_cost=cost),'concession_per_affected_vehicle':concession,'new_revenue':new*rpu,'contribution_before_concession':new*rpu-cost,'carrier_base_concession':carrier*concession,'reconstructed_gain_EBITDA':new*rpu-cost-carrier*concession,'incremental_only_concession_gain':new*rpu-cost-new*concession,'alternative_if_table_carrier_base_pre_award_and_new_also_discounted':new*rpu-cost-(carrier+new)*concession,'published_gain_EBITDA':60e6,'lost_volume_midpoint':245000,'lost_contribution':245000*rpu-80e6,'net_two_contracts_reconstructed':new*rpu-cost-carrier*concession-(245000*rpu-80e6),'published_net_two_contracts':-90e6,'break_even_concession_per_table_carrier_unit':(new*rpu-cost)/carrier,'break_even_discount_fraction_of_assumed_seller_commission':(new*rpu-cost)/(carrier*price*commission),'scenario_gain_at_40pct_discount':new*rpu-cost-carrier*price*commission*.40,'RB_reconstructed_gain':245000*850-80e6-1003000*3642*.04*.15,'RB_published_gain':105e6}
assert abs(out['reconstructed_gain_EBITDA']-60e6)<1e6
assert abs(out['RB_reconstructed_gain']-105e6)<2e6
(p/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
