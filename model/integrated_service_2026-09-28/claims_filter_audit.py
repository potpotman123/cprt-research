"""Bounded identity checks using existing cells; no forecast writes or fitting."""
import hashlib,json
import engine as m

def main():
    d,e,c=m.load()
    _,raw=m.stock(d,[0,0,1,0,0])
    target={(b,k):e['relative_claim_weights'][k]*e['body_weights'][str(k)][b]
            for b in range(4) for k in range(6)}
    z=sum(target.values());target={key:v/z for key,v in target.items()}
    correction={key:target[key]/raw[key] for key in raw}
    eco=m.economics(d,e,c,1,1)
    claims=sum(raw[key]*correction[key] for key in raw)
    totals=sum(target[key]*eco[key]['probability'] for key in target)
    checks=[]
    assert m.close(claims,1);checks.append('CY2025 corrected claim mass equals one')
    # Hypothetical: remove 10% of repairable claims, no total-loss claims.
    repairables=claims-totals
    after_claims=totals+.9*repairables
    after_tlf=totals/after_claims
    assert m.close(after_claims*after_tlf,totals)
    checks.append('Matched filing denominator and TLF preserve total-loss count')
    wrong_filing=after_claims*(totals/claims)
    assert wrong_filing<totals;checks.append('Holding TLF fixed falsely loses totals under repairable-only nonfiling')
    # Hypothetical uniform loss of covered claim exposure, not empirical coverage.
    once=.9*totals;twice=.9*.9*totals
    assert m.close(once/totals,.9) and m.close(twice/totals,.81)
    checks.append('Same exposure shock applied twice produces 19%, rather than 10%, loss')
    # Baseline corrections absorb any positive cell multiplier if refitted.
    factors={key:.65+.03*key[1] for key in raw}
    revised_raw={key:raw[key]*factors[key] for key in raw}
    revised_correction={key:target[key]/revised_raw[key] for key in raw}
    for key in raw:
        assert m.close(revised_raw[key]*revised_correction[key],target[key])
    checks.append('Refitted cell corrections absorb baseline coverage multipliers; no identification')
    assert all(v==1 for v in c['quarter_drivers']['reported_claim_frequency'])
    checks.append('Production frequency multipliers are flat assumptions')
    paths=[m.OLD,m.ECON,m.HERE/'assumptions.json',m.HERE/'engine.py',
           m.HERE/'fleet_cohort_build.py',m.HERE/'vintage_body_integration.py',
           m.HERE/'joint_claim_selection.py',m.HERE/'claims_filter_audit.py']
    out={'checks':checks,'checks_passed':len(checks),
         'synthetic_cases_not_forecasts':{
             'baseline_relative_claim_mass':claims,'baseline_model_TLF':totals/claims,
             'remove_10pct_repairables_claim_factor':after_claims/claims,
             'remove_10pct_repairables_TLF':after_tlf,
             'correct_total_loss_factor':after_claims*after_tlf/totals,
             'incorrect_fixed_TLF_total_loss_factor':wrong_filing/totals,
             'uniform_exposure_shock_once':once/totals,'same_shock_twice':twice/totals},
         'source_hashes':{str(p.relative_to(m.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
         'status':'Identity audit, not empirical validation. No forecast input changed.'}
    (m.HERE/'claims_filter_audit_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='source_hashes'},indent=2))

if __name__=='__main__':main()
