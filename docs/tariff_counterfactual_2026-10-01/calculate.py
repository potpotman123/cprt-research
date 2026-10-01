"""Static, hypothetical tariff removal; no estimated substitution elasticity."""
from pathlib import Path
import csv,json,math
P=Path(__file__).resolve().parent

def share(s,relative_price_factor,epsilon):
    odds=s/(1-s)*relative_price_factor**(-epsilon)
    return odds/(1+odds)
def run_case(name,t0=.15,t1=0,r=.30,passing=.5,epsilon=2,exposed=1,competitor_cut=0):
    # P(t)=P_without_tariff + passing * customs_value * t.
    # r=customs_value/P_without_tariff. Dollar margins fixed; all hypothetical.
    price_factor=(1+passing*r*t1)/(1+passing*r*t0)
    relative=price_factor/(1-competitor_cut)
    s=.25
    affected=share(s,relative,epsilon)
    final=(1-exposed)*s+exposed*affected
    return dict(case=name,initial_tariff=t0,remaining_tariff=t1,customs_value_over_untaxed_delivered_price=r,tariff_dollar_pass_through=passing,odds_elasticity=epsilon,affected_market_fraction=exposed,competitor_price_cut=competitor_cut,aftermarket_price_cut=1-price_factor,relative_price_factor=relative,initial_physical_share=s,counterfactual_physical_share=final,share_gain_pp=100*(final-s),relative_quantity_gain_fixed_market=final/s-1,status='HYPOTHETICAL static counterfactual, not forecast or fitted elasticity')
def save(name,rows):
    with (P/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
    grid=[run_case(f'pass{p:g}_elasticity{e:g}',passing=p,epsilon=e) for p in [0,.25,.5,1] for e in [1,2,4]]
    alternatives=[run_case('central_illustration'),run_case('half_market_affected',exposed=.5),run_case('competitors_also_cut_1pct',competitor_cut=.01),run_case('competitors_also_cut_3pct',competitor_cut=.03),run_case('retain_assumed_2p5pct_base_duty',t1=.025),run_case('higher_customs_ratio_60pct',r=.6),run_case('25_to_15pct_historical_step',t0=.25,t1=.15),run_case('25pct_to_zero_stress',t0=.25),run_case('zero_price_pass_through',passing=0)]
    for row in grid+alternatives:
        assert 0<row['counterfactual_physical_share']<1
        if row['competitor_price_cut']==0:assert row['share_gain_pp']>=-1e-12
    assert run_case('zero',t0=0)['share_gain_pp']==0
    assert run_case('noexposure',exposed=0)['share_gain_pp']==0
    assert abs(run_case('equal cuts',competitor_cut=run_case('x')['aftermarket_price_cut'])['share_gain_pp'])<1e-10
    for e in [1,2,4]:
        gains=[r['share_gain_pp'] for r in grid if r['odds_elasticity']==e]
        assert gains==sorted(gains)
    assert alternatives[3]['share_gain_pp']<0
    x=alternatives[0]['aftermarket_price_cut'];dollar_share=.227*(1-x)/(1-.227*x)
    hurdles=[]
    for passing in [.5,1]:
        factor=1-run_case('hurdle',passing=passing)['aftermarket_price_cut']
        e=math.log((.30/.70)/(.25/.75))/-math.log(factor)
        assert abs(share(.25,factor,e)-.30)<1e-12
        hurdles.append(dict(target_physical_share_gain_pp=5,tariff_dollar_pass_through=passing,required_odds_elasticity=e,status='Reverse solved assumption, not measured'))
    save('sensitivity_grid.csv',grid);save('alternative_cases.csv',alternatives);save('five_point_hurdle.csv',hurdles)
    out=dict(status='PASS',forecast_admission=False,central_illustration=alternatives[0],fixed_quantity_dollar_share_example=dict(initial=.227,counterfactual=dollar_share,note='Separate spending identity, holding quantities and other prices fixed'),source_numeric_example=dict(untaxed_delivered_price=200,customs_value=60,tariff=.15,tax_dollars=9,full_pass_taxed_price=209,full_pass_removal_price_cut=9/209),limitations=['No causal adoption elasticity','No current customs-value/import weights','No mapped China tariff rate','No timing or policy-repeal forecast','OEM/recycled prices and eligibility can change','Physical share gain is not annual growth or revenue impact'],hurdles=hurdles)
    (P/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'central':alternatives[0],'alternatives':[(r['case'],r['share_gain_pp']) for r in alternatives],'hurdles':hurdles,'checks':'PASS'},indent=2))
if __name__=='__main__':main()
