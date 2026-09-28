"""Small exact bridge: distinguish inherited capture comparisons from new runoff.

Sequential attribution; interaction allocation is order-dependent, not causal.
No calibration, scraping, or change to adopted model inputs.
"""
import json
import engine as m
import history_repair as h

def main():
    d,e,c=m.load();result=m.run(d,e,c);forecast=h.build(d,c,result)
    q4=result['quarters'][3]['effective_capture'];rows=[]
    for i in range(4,8):
        q=result['quarters'][i];b=result['quarters'][i-4];f=forecast[i]
        actual=d['actuals'][i-4];base=actual['us_service']+actual['intl_service']
        running=actual['us_service']*c['insurance_share_of_us_service_base']
        r={'period':q['period'],'prior_legacy_service_musd':base,
           'historical_capture_proxy':b['effective_capture'],'q4_capture_proxy':q4,
           'forecast_capture_proxy':q['effective_capture']}
        factors=[('exposure_frequency',f['exposure_frequency_factor']),
                 ('total_loss_frequency',f['total_loss_factor']),
                 ('insurance_RPU',f['insurance_RPU_factor']),
                 ('inherited_capture_comparison',q4/b['effective_capture']),
                 ('post_q4_capture_change',q['effective_capture']/q4)]
        for name,factor in factors:
            delta=running*(factor-1);running*=factor
            r[name+'_factor']=factor;r[name+'_delta_musd']=delta
        r['other_us_delta_musd']=f['other_us_musd']-actual['us_service']*(1-c['insurance_share_of_us_service_base'])
        r['intl_delta_musd']=f['intl_musd']-actual['intl_service']
        total_delta=sum(v for k,v in r.items() if k.endswith('_delta_musd'))
        r['forecast_legacy_service_musd']=f['legacy_service_musd']
        r['change_musd']=total_delta;r['change_pct']=100*total_delta/base
        r['capture_neutral_service_musd']=base+sum(r[name+'_delta_musd'] for name in ['exposure_frequency','total_loss_frequency','insurance_RPU'])+r['other_us_delta_musd']+r['intl_delta_musd']
        r['q4_capture_frozen_service_musd']=r['forecast_legacy_service_musd']-r['post_q4_capture_change_delta_musd']
        assert m.close(base+total_delta,f['legacy_service_musd'])
        assert m.close(r['inherited_capture_comparison_factor']*r['post_q4_capture_change_factor'],f['capture_factor'])
        assert m.close(running,f['insurance_musd'])
        rows.append(r)
    m.save_csv('driver_attribution.csv',rows)
    summary={key:sum(r[key] for r in rows[:2]) for key in ['prior_legacy_service_musd','forecast_legacy_service_musd','exposure_frequency_delta_musd','total_loss_frequency_delta_musd','insurance_RPU_delta_musd','inherited_capture_comparison_delta_musd','post_q4_capture_change_delta_musd','capture_neutral_service_musd','q4_capture_frozen_service_musd','change_musd']}
    out={'FY27_H1':summary,'checks_passed':12,'method':'Exact sequential bridge: exposure, TLF, RPU, inherited capture comparison, post-Q4 capture; order-dependent interactions',
         'evidence_status':'All capture paths are inherited assumptions; comparison case is not a forecast recommendation',
         'scope':'Legacy service only; no stock-price or consensus conclusion'}
    (m.HERE/'driver_attribution.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
