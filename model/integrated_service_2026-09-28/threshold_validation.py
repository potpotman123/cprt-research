"""Expose assumed near-threshold mass; no empirical validation claimed."""
import json,hashlib
import engine as m

def main():
    d,e,c=m.load();active=m.fleet_data(d,c)
    _,raw0=m.stock(d,[0,0,1,0,0])
    w={(b,k):e['relative_claim_weights'][k]*e['body_weights'][str(k)][b] for b in range(4) for k in range(6)}
    z=sum(w.values());correction={key:v/z/raw0[key] for key,v in w.items()}
    baseline=m.economics(d,e,c,1,1);up=m.economics(d,e,c,1.05,1);down=m.economics(d,e,c,.95,1)
    rows=[]
    for key,x in baseline.items():
        b,k=key;u=1-x['probability']
        rows.append(dict(body=['Car','SUV','Pickup','Minivan'][b],age_bucket=e['cohorts'][k]['age_bucket'],sigma=e['cohorts'][k]['sigma'],baseline_TLF=x['probability'],repair_plus5_TLF=up[key]['probability'],repair_minus5_TLF=down[key]['probability'],assumed_claim_mass_crossing_up=up[key]['probability']-x['probability'],assumed_claim_mass_crossing_down=x['probability']-down[key]['probability'],baseline_repair_threshold_usd=x['ACV']*(1-(.4-.2*u)*(1-c['seller_fee_fraction'])),status='Model-implied, not observed near-threshold claim counts'))
        assert down[key]['probability']<x['probability']<up[key]['probability']
    quarterly=[]
    for i in range(4,8):
        _,raw=m.stock(active,d['periods'][i]['weights']);mass={key:v*correction[key] for key,v in raw.items()};z=sum(mass.values())
        p=sum(mass[key]*x['probability'] for key,x in baseline.items())/z
        pu=sum(mass[key]*x['probability'] for key,x in up.items())/z
        pd=sum(mass[key]*x['probability'] for key,x in down.items())/z
        quarterly.append(dict(period=d['periods'][i]['label'],baseline_TLF_pct=100*p,plus5_crossing_share_all_claims_pct=100*(pu-p),plus5_crossing_share_repairables_pct=100*(pu-p)/(1-p),plus5_total_loss_growth_pct=100*(pu/p-1),minus5_total_loss_growth_pct=100*(pd/p-1)))
    m.save_csv('threshold_validation_cells.csv',rows)
    paths=[m.OLD,m.ECON,m.BIRTHS,m.HERE/'assumptions.json',m.HERE/'engine.py',m.HERE/'threshold_validation.py']
    out={'quarterly':quarterly,'checks_passed':24,'source_hashes':{str(p.relative_to(m.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'status':'Assumed threshold density exposed. External response validation not achieved. No forecast change.'}
    (m.HERE/'threshold_validation_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(quarterly,indent=2))

if __name__=='__main__':main()
