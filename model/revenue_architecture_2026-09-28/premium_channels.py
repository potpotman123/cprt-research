"""Optional premium/affordability scenarios relative to an explicit reference.
Probabilities and behavioral slopes are assumptions unless separately evidenced.
"""
import copy
import math

def _prob(base, shock):
    logodds=math.log(base/(1-base))-shock
    return 1/(1+math.exp(-logodds)) if logodds>=0 else math.exp(logodds)/(1+math.exp(logodds))

def compile_channels(config, a):
    c=copy.deepcopy(config)
    def vector(name):
        v=a[name]
        if len(v)!=4 or any(not isinstance(x,(float,int)) or not math.isfinite(x) or x<=0 for x in v):
            raise ValueError('Expected four positive finite values: '+name)
        return v
    names=['premium','income','vehicle_value','deductible']
    actual={k:vector(k) for k in names};reference={k:vector('reference_'+k) for k in names}
    probabilities=[a['baseline_coverage_probability'],a['baseline_repairable_filing_probability']]
    if any(not math.isfinite(x) or not 0<x<1 for x in probabilities):raise ValueError('Baseline probabilities must be between zero and one')
    exposure=a['affected_baseline_claim_fraction'];speed=a['quarterly_adjustment_fraction']
    if not math.isfinite(exposure) or not 0<=exposure<=1 or not math.isfinite(speed) or not 0<=speed<=1:raise ValueError('Exposure/adjustment must lie in [0,1]')
    slopes=[a[k] for k in ['coverage_income_slope','coverage_value_slope','coverage_payoff_slope','filing_income_slope','filing_deductible_slope']]
    if any(not math.isfinite(x) or x<0 for x in slopes):raise ValueError('Behavior slopes must be finite and nonnegative')
    payoff=a['excess_lien_free_fraction']
    if len(payoff)!=4 or any(not math.isfinite(x) or not -1<=x<=1 for x in payoff):raise ValueError('Payoff deviation must lie in [-1,1]')
    if any(x!=0 for x in c['nonfiling'][4:]):raise ValueError('Premium filing and incremental nonfiling cannot be stacked')
    if any(x!=1 for x in c['claims'][4:]) and not a.get('claims_excludes_premium_channels',False):
        raise ValueError('Existing claims trend may already include premiums; explicitly separate residual first')
    for k in ['coverage_exposure','repairable_filing']:
        if any(x!=1 for x in c.get(k,[1.]*8)):raise ValueError('Do not overwrite an existing coverage/filing shock')
        c[k]=[1.]*8
    cs=fs=0.;rows=[]
    for q in range(4):
        pi=math.log(actual['premium'][q])-math.log(actual['income'][q])-math.log(reference['premium'][q])+math.log(reference['income'][q])
        pv=math.log(actual['premium'][q])-math.log(actual['vehicle_value'][q])-math.log(reference['premium'][q])+math.log(reference['vehicle_value'][q])
        di=math.log(actual['deductible'][q])-math.log(actual['income'][q])-math.log(reference['deductible'][q])+math.log(reference['income'][q])
        ct=a['coverage_income_slope']*pi+a['coverage_value_slope']*pv+a['coverage_payoff_slope']*payoff[q]
        ft=a['filing_income_slope']*pi+a['filing_deductible_slope']*di
        cs+=(ct-cs)*speed;fs+=(ft-fs)*speed
        cp=_prob(probabilities[0],cs);fp=_prob(probabilities[1],fs)
        cm=(1-exposure)+exposure*cp/probabilities[0]
        if cm<=0:raise ValueError('Scenario eliminates all covered exposure')
        # Filing is conditional on the surviving coverage-weighted claims pool.
        fm=((1-exposure)+exposure*(cp/probabilities[0])*(fp/probabilities[1]))/cm
        if cm<=0 or fm<=0:raise ValueError('Scenario eliminates all coverage or filing; outside engine domain')
        c['coverage_exposure'][q+4]=cm;c['repairable_filing'][q+4]=fm
        rows.append(dict(quarter=q+1,premium_income_log_deviation=pi,premium_value_log_deviation=pv,deductible_income_log_deviation=di,coverage_probability=cp,repairable_filing_probability=fp,coverage_multiplier=cm,repairable_filing_multiplier=fm))
    c.pop('premium_assumptions',None)
    return c,dict(status='Conditional behavioral sensitivity; not an estimated causal forecast',forecast_admission=False,quarters=rows)
