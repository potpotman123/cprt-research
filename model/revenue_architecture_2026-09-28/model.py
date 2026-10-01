"""Quarterly research architecture v2: explicit events, populations and benchmarks.

Reuses the prior cohort/fee evidence; no claim that calibrated levels are observed.
All execution is local, standard-library only. Historical artifacts stay unchanged.
"""
import copy
import csv
import functools
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEGACY = ROOT / 'model/integrated_service_2026-09-28'
sys.path.insert(0, str(LEGACY))
import engine as old


def vector(value):
    return [value] * 8


def forecast(value, historical=1.):
    return [historical] * 4 + [value] * 4


def configuration():
    return {
        'name': 'neutral_allocation_flat_other_reference',
        'status': 'Conditional reference, not an adopted forecast',
        'claims_convention': 'combined_propensity_per_fleet_excluding_incremental_nonfiling',
        'insurance_service_fraction': .9,
        'cohort_anchor_path': None,
        'claims': vector(1.), 'repair': vector(1.), 'value': vector(1.),
        'expected_salvage': vector(1.), 'realized_salvage': vector(1.),
        'routing': vector(1.), 'cat_total_loss_activity': vector(0.),
        'nonfiling': vector(0.),
        'carrier_mode': 'same_quarter_neutral',
        'carrier_claim_weights_by_cell': {},
        'carrier_terms': {},
        'allocation_overrides': {},
        'preferred_buyer_fraction': vector(.5),
        'seller_fee_fraction': vector(.04),
        'seller_fixed_fee': vector(0.),
        'fixed_buyer_fee': vector(110.),
        'buyer_fee_multiplier': vector(1.),
        'schedule_ids': ['sep2026_snapshot'] * 8,
        'schedule_status': 'Historical use of Sep2026 schedule is a proxy, not verified history',
        'sales_timing': {'mode': 'sale_equivalent', 'input_stage': 'sale_equivalent',
                         'kernels': None, 'opening_release': None, 'withdrawal_fraction': 0.,
                         'without_title_kernel': None, 'with_title_kernel': None,
                         'rpu_by_vintage': None, 'opening_rpu': None},
        'title': {'base_adoption': .5, 'base_charge': 50., 'basis': 'sales',
                  'eligible_external': None, 'adoption': vector(.5), 'charge': vector(50.),
                  'waiver': vector(0.), 'bundled': False, 'accounting': 'incremental_fee',
                  'recognition_kernel': [1.], 'opening_release': None,
                  'status': 'Inherited assumption; not observed adoption or contract terms'},
        'delivery': {'base_adoption': .1, 'base_charge': 300., 'basis': 'sales',
                     'eligible_external': None, 'adoption': vector(.1), 'charge': vector(300.),
                     'waiver': vector(0.), 'bundled': False, 'accounting': 'assumed_gross',
                     'recognition_kernel': [1.], 'opening_release': None,
                     'status': 'Inherited assumption; gross/net and product levels unknown'},
        'other_us_units': vector(1.), 'other_us_fee': vector(1.),
        'intl_units': vector(1.), 'intl_rpu': vector(1.), 'intl_fx': vector(1.),
        'intl_rpu_basis': 'reported_currency',
        'purchased_units': vector(1.), 'purchased_asp': vector(1.),
        'acquired_total': [None] * 4, 'acquired_service': [None] * 4,
        'acquisition_first_fiscal_quarter': 2,
        'nodes': 1024,
    }


def validate(c):
    for k in ['claims', 'repair', 'value', 'expected_salvage', 'realized_salvage',
              'routing', 'cat_total_loss_activity', 'nonfiling', 'preferred_buyer_fraction',
              'seller_fee_fraction', 'seller_fixed_fee', 'fixed_buyer_fee',
              'buyer_fee_multiplier', 'other_us_units', 'other_us_fee', 'intl_units',
              'intl_rpu', 'intl_fx', 'purchased_units', 'purchased_asp']:
        a = c[k]
        if len(a) != 8 or any(not isinstance(v, (float, int)) or not math.isfinite(v) or v < 0 for v in a):
            raise ValueError('Invalid eight-quarter driver: '+k)
    for k in ['claims', 'repair', 'value', 'expected_salvage', 'realized_salvage']:
        if min(c[k]) <= 0: raise ValueError(k+' must be positive')
    for k in ['coverage_exposure', 'repairable_filing']:
        v = c.get(k, [1.] * 8)
        if len(v) != 8 or any(not isinstance(x, (float, int)) or not math.isfinite(x) or x <= 0 for x in v):
            raise ValueError('Invalid positive eight-quarter driver: ' + k)
    for k in ['routing', 'nonfiling', 'preferred_buyer_fraction', 'seller_fee_fraction']:
        if max(c[k]) > 1: raise ValueError(k+' out of range')
    if max(c['nonfiling']) >= 1: raise ValueError('Nonfiling must be <1')
    if c['claims_convention'] != 'combined_propensity_per_fleet_excluding_incremental_nonfiling':
        raise ValueError('Do not silently multiply incompatible claims/coverage conventions')
    if c['intl_rpu_basis'] == 'reported_currency' and any(x != 1 for x in c['intl_fx']):
        raise ValueError('Reported-currency RPU already contains FX')
    if c['intl_rpu_basis'] not in ['reported_currency', 'constant_currency']:
        raise ValueError('Unknown RPU/FX convention')
    if c['carrier_mode'] not in ['same_quarter_neutral', 'inherited_runoff']:
        raise ValueError('Unknown allocation convention')
    d, _, _ = old.load()
    names = {x['name'] for x in d['carriers']}
    for key in ['allocation_overrides', 'carrier_terms', 'carrier_terms_by_period']:
        if not set(c.get(key, {})) <= names:
            raise ValueError('Unknown carrier in ' + key)
    for name, values in c['allocation_overrides'].items():
        if len(values) != 8 or any(not math.isfinite(x) or not 0 <= x <= 1 for x in values):
            raise ValueError('Allocation override needs eight fractions: ' + name)
    period_weights = c.get('carrier_claim_weights_by_period')
    if period_weights is not None:
        if c['carrier_claim_weights_by_cell']:
            raise ValueError('Specify either period or static cell carrier weights, not both')
        if len(period_weights) != 8:
            raise ValueError('Carrier claim weights need eight periods')
        for row in period_weights:
            if set(row) != names or any(not math.isfinite(x) or x < 0 for x in row.values()) or abs(sum(row.values())-1) > 1e-8:
                raise ValueError('Carrier claim weights must be finite fractions summing to one')
    allowed_terms = {'repair_factor', 'value_factor', 'preferred_fraction', 'seller_pct', 'seller_fixed'}
    term_rows = list(c['carrier_terms'].values())
    for name, rows in c.get('carrier_terms_by_period', {}).items():
        if len(rows) != 8:
            raise ValueError('Carrier terms need eight periods: ' + name)
        term_rows.extend(rows)
    for terms in term_rows:
        if not set(terms) <= allowed_terms or any(not math.isfinite(x) for x in terms.values()):
            raise ValueError('Unknown or nonfinite carrier term')
    fleet_weights = c.get('fleet_period_weights')
    if fleet_weights is not None:
        if len(fleet_weights) != 8 or any(len(row) != 5 or any(not math.isfinite(x) or x < 0 for x in row) or abs(sum(row)-1) > 1e-8 for row in fleet_weights):
            raise ValueError('Fleet calendar weights require eight normalized five-year rows')
    if len(c['acquired_total'])!=4 or len(c['acquired_service'])!=4:
        raise ValueError('Acquisition requires four quarterly values')
    for q,(total,service) in enumerate(zip(c['acquired_total'],c['acquired_service'])):
        if any(x is not None and (not math.isfinite(x) or x<0) for x in [total,service]):
            raise ValueError('Invalid acquired external revenue')
        if service is not None and (total is None or service>total):
            raise ValueError('Acquired service classification requires compatible total')
        if q+1<c['acquisition_first_fiscal_quarter'] and any(x not in [None,0] for x in [total,service]):
            raise ValueError('No acquired revenue before assumed control transfer')
    if not 0 < c['insurance_service_fraction'] < 1:
        raise ValueError('Base split must be strictly between zero and one')


def flow(arrivals, kernels, opening_release, withdrawal_fraction=0.):
    """One completed sale per arrival at most; unserved mass stays in inventory.

    opening_release contains scheduled opening-backlog exits by future quarter,
    including any beyond the displayed horizon. No opening inventory is invented.
    """
    n = len(arrivals)
    if opening_release is None: raise ValueError('Explicit opening backlog required')
    if len(kernels) != n or not 0 <= withdrawal_fraction <= 1:
        raise ValueError('Invalid flow convention')
    if any(x < 0 or not math.isfinite(x) for x in arrivals + opening_release):
        raise ValueError('Negative/nonfinite flow')
    for k in kernels:
        if not k or any(x < 0 or not math.isfinite(x) for x in k) or sum(k) > 1+1e-12:
            raise ValueError('Sale probabilities must be nonnegative and sum <= 1')
    sales = [opening_release[q] if q < len(opening_release) else 0. for q in range(n)]
    withdrawals = [x*withdrawal_fraction for x in arrivals]
    for t, a in enumerate(arrivals):
        for lag, fraction in enumerate(kernels[t]):
            if t+lag < n: sales[t+lag] += a*(1-withdrawal_fraction)*fraction
    inventory = sum(opening_release)
    ledger = []
    for q in range(n):
        begin = inventory
        inventory += arrivals[q]-sales[q]-withdrawals[q]
        if inventory < -1e-8: raise ValueError('Flow exits exceed inventory')
        ledger.append({'opening': begin, 'arrivals': arrivals[q], 'sales': sales[q],
                       'withdrawals': withdrawals[q], 'closing': inventory})
    return sales, ledger


@functools.lru_cache(maxsize=512)
def cell_economics(b, k, repair, value, expected, realized, preferred, seller_pct,
                   seller_fixed, fixed_buyer, buyer_multiplier, schedule_id, nodes):
    if any(not math.isfinite(x) for x in [repair,value,expected,realized,preferred,seller_pct,seller_fixed,fixed_buyer,buyer_multiplier]) or not isinstance(nodes, int) or nodes < 1:
        raise ValueError('Cell economics must be finite with positive integration nodes')
    if min(repair,value,expected,realized)<=0 or not 0<=preferred<=1 or not 0<=seller_pct<=1 or min(seller_fixed,fixed_buyer,buyer_multiplier)<0:
        raise ValueError('Invalid cell economics or carrier terms')
    d, e, _ = old.load()
    if schedule_id == 'sep2026_snapshot':
        fee_data = d
    else:
        registry = json.loads((HERE/'fee_schedule_registry.json').read_text())
        entry = registry.get(schedule_id)
        if not entry: raise ValueError('Unknown schedule vintage: '+schedule_id)
        if entry.get('status') != 'observed' or not entry.get('source'):
            raise ValueError('New schedule requires observed source provenance')
        with (ROOT/entry['path']).open() as f:
            fee_data = dict(d, fees=list(csv.DictReader(line for line in f if not line.startswith('#'))))
    std, pref, virtual = old.fee_grids(fee_data)
    row = e['cohorts'][k]
    acv = row['car_ACV']*e['value_ratios'][b]*value
    mu = row['log_car_repair_median']+math.log(e['repair_ratios'][b]*repair)
    # Perfect rank relationship is inherited, explicitly unvalidated.
    lo, hi = 1e-12, 1-1e-12
    for _ in range(44):
        u = (lo+hi)/2
        expected_net = acv*(.4-.2*u)*expected*(1-seller_pct)-seller_fixed
        threshold = acv-expected_net
        if threshold <= 0: hi = u
        elif mu+row['sigma']*old.N.inv_cdf(u) < math.log(threshold): lo = u
        else: hi = u
    u = (lo+hi)/2
    buyer = seller = proceeds = 0.
    for j in range(nodes):
        rank = u+(1-u)*(j+.5)/nodes
        price = acv*(.4-.2*rank)*realized
        proceeds += price/nodes
        buyer += ((1-preferred)*old.fee(price,std)+preferred*old.fee(price,pref)+old.fee(price,virtual))*buyer_multiplier/nodes
        seller += (seller_pct*price+seller_fixed)/nodes
    buyer += fixed_buyer
    return {'TLF': 1-u, 'ASP': proceeds, 'buyer': buyer, 'seller': seller, 'core_RPU': buyer+seller}


def timed_core(arrivals, timing, adoption):
    kernels=timing['kernels']
    if kernels is None:
        a,b=timing['without_title_kernel'],timing['with_title_kernel']
        if a is None or b is None: raise ValueError('Provide measured/assumed title timing kernels explicitly')
        n=max(len(a),len(b));a=a+[0.]*(n-len(a));b=b+[0.]*(n-len(b))
        kernels=[[(1-adoption[q])*a[i]+adoption[q]*b[i] for i in range(n)] for q in range(4)]
    sales,ledger=flow(arrivals,kernels,timing['opening_release'],timing['withdrawal_fraction'])
    prices=timing['rpu_by_vintage'];opening_price=timing['opening_rpu']
    if prices is None or opening_price is None: raise ValueError('Timing requires explicit opening/vintage fee economics')
    if len(prices)!=4 or any(len(x)!=4 for x in prices) or len(opening_price)!=4:
        raise ValueError('Timing fee matrix must be four assignment vintages by four sale quarters')
    if any(x<0 or not math.isfinite(x) for row in prices for x in row) or any(x<0 or not math.isfinite(x) for x in opening_price):
        raise ValueError('Invalid vintage fee assumptions')
    opening=timing['opening_release']
    revenue=[(opening[q] if q<len(opening) else 0)*opening_price[q] for q in range(4)]
    for t,qty in enumerate(arrivals):
        for lag,w in enumerate(kernels[t]):
            if t+lag<4: revenue[t+lag]+=qty*(1-timing['withdrawal_fraction'])*w*prices[t][t+lag]
    return sales,ledger,revenue


def operating(c):
    if c.get('premium_assumptions') is not None:
        from premium_channels import compile_channels
        c, _ = compile_channels(c, c['premium_assumptions'])
    validate(c)
    d, e, inherited = old.load()
    active = old.fleet_data(d, inherited)
    _, raw0 = old.stock(d, [0,0,1,0,0])
    cw = {(b,k):e['relative_claim_weights'][k]*e['body_weights'][str(k)][b] for b in range(4) for k in range(6)}
    z = sum(cw.values()); cw = {key:v/z for key,v in cw.items()}
    repair_calibration = {key:1. for key in cw}
    if c.get('cohort_anchor_path'):
        anchor = json.loads((ROOT/c['cohort_anchor_path']).read_text())
        mapped = {(int(r['body']),int(r['age'])):r for r in anchor['cells']}
        if len(anchor['cells']) != 24 or set(mapped) != set(cw):
            raise ValueError('Cohort anchor must contain each of the 24 cells once')
        cw = {key:r['claim_weight'] for key,r in mapped.items()}
        repair_calibration = {key:r['repair_multiplier'] for key,r in mapped.items()}
        if abs(sum(cw.values())-1)>1e-8 or any(not math.isfinite(v) or v<=0 for v in [*cw.values(),*repair_calibration.values()]):
            raise ValueError('Invalid cohort anchor weights or repair calibration')
        # Observed claims weights refer to the active fleet in the anchor year.
        # Using the predecessor fixed-body denominator here would distort them twice.
        if anchor['fleet_reference_weights'] != [0,0,1,0,0]:
            raise ValueError('Unsupported cohort anchor fleet reference')
        _, raw0 = old.stock(active, anchor['fleet_reference_weights'])
    quarters, cells = [], []
    for p, period in enumerate(d['periods']):
        fleet_weights = c['fleet_period_weights'][p] if c.get('fleet_period_weights') is not None else period['weights']
        _, raw = old.stock(active, fleet_weights)
        hist_idx = p if p < 4 else (p-4 if c['carrier_mode']=='same_quarter_neutral' else 3)
        weights = {x['name']:x['weights'][hist_idx] for x in d['carriers']}
        norm = sum(weights.values()); weights = {k:v/norm for k,v in weights.items()}
        if c.get('carrier_claim_weights_by_period') is not None:
            weights = c['carrier_claim_weights_by_period'][p]
        q = dict(claims=0., prefiling_claims=0., totals=0., assignments=0., buyer=0., seller=0., proceeds=0.)
        for (b,k), w in cw.items():
            cl = w*raw[b,k]/raw0[b,k]*c['claims'][p]*c.get('coverage_exposure', [1.] * 8)[p]
            conditional = c['carrier_claim_weights_by_cell'].get(f'{b}:{k}', weights)
            if set(conditional) != set(weights) or any(not math.isfinite(v) or v < 0 for v in conditional.values()) or abs(sum(conditional.values())-1)>1e-8:
                raise ValueError('Carrier weights must span all carriers and sum to one per cell')
            for carrier in d['carriers']:
                name = carrier['name']; terms = dict(c['carrier_terms'].get(name,{}))
                if name in c.get('carrier_terms_by_period', {}):
                    terms.update(c['carrier_terms_by_period'][name][p])
                allocation_index = p if p < 4 else p-4
                if p >= 4 and c['carrier_mode']=='inherited_runoff': allocation_index = p if name=='Progressive' else 3
                alloc = c['allocation_overrides'].get(name, carrier['allocations'])[allocation_index if name not in c['allocation_overrides'] else p]
                if not 0 <= alloc <= 1: raise ValueError('Allocation outside [0,1]')
                ec = cell_economics(b,k,c['repair'][p]*repair_calibration[b,k]*terms.get('repair_factor',1),c['value'][p]*terms.get('value_factor',1),
                    c['expected_salvage'][p],c['realized_salvage'][p],terms.get('preferred_fraction',c['preferred_buyer_fraction'][p]),
                    terms.get('seller_pct',c['seller_fee_fraction'][p]),terms.get('seller_fixed',c['seller_fixed_fee'][p]),
                    c['fixed_buyer_fee'][p],c['buyer_fee_multiplier'][p],c['schedule_ids'][p],c['nodes'])
                claims = cl*conditional[name]; tl = claims*ec['TLF']
                reported = tl+(claims-tl)*(1-c['nonfiling'][p])*c.get('repairable_filing', [1.] * 8)[p]
                units = tl*alloc*c['routing'][p]
                for key, val in [('claims',reported),('prefiling_claims',claims),('totals',tl),('assignments',units),('buyer',units*ec['buyer']),('seller',units*ec['seller']),('proceeds',units*ec['ASP'])]: q[key] += val
                cells.append(dict(period=p,body=b,age=k,carrier=name,claims=reported,prefiling_claims=claims,
                    totals=tl,assignments=units,allocation=alloc,selection_TLF=ec['TLF'],
                    ASP=ec['ASP'],buyer_RPU=ec['buyer'],seller_RPU=ec['seller'],core_RPU=ec['core_RPU']))
        if q['assignments'] <= 0: raise ValueError('No fee units for RPU comparison')
        q.update(core_RPU=(q['buyer']+q['seller'])/q['assignments'],ASP=q['proceeds']/q['assignments'],
                 TLF=q['totals']/q['claims'],TLF_prefiling=q['totals']/q['prefiling_claims'],
                 capture_including_routing=q['assignments']/q['totals'])
        quarters.append(q)
    return quarters, cells


def service_revenue(spec, sales, assignments):
    basis = spec['basis']
    if basis == 'sales': eligible = sales
    elif basis == 'assignments': eligible = assignments
    elif basis == 'external':
        eligible = spec['eligible_external']
        if eligible is None or len(eligible)!=4: raise ValueError('External eligible jobs missing')
    else: raise ValueError('Unknown service eligibility')
    if spec['accounting'] not in ['incremental_fee','assumed_gross','gross','net']:
        raise ValueError('Specify service revenue accounting basis')
    jobs, amounts = [], []
    for q, qty in enumerate(eligible):
        p = q+4; adoption=spec['adoption'][p]; fee=spec['charge'][p]; waiver=spec['waiver'][p]
        if not 0<=adoption<=1 or min(qty,fee,waiver)<0 or waiver>fee:
            raise ValueError('Invalid service volume/charge/waiver')
        jobs.append(qty*adoption)
        amounts.append(qty*adoption*(fee-waiver)*(not spec['bundled']))
    kernel=spec['recognition_kernel']
    opening = spec['opening_release']
    if len(kernel)==1 and kernel==[1.] and opening is None: opening=[]
    recognized, ledger = flow(amounts,[kernel]*4,opening)
    return recognized, jobs, ledger


def run(c):
    premium_diagnostics = None
    if c.get('premium_assumptions') is not None:
        from premium_channels import compile_channels
        c, premium_diagnostics = compile_channels(c, c['premium_assumptions'])
    d, _, _ = old.load()
    ops, cells = operating(c)
    # Components are allocated by explicit assumptions, never called disclosures.
    # Freeze this base decomposition before applying forward driver changes.
    # Historical assumption edits deliberately alter the base and must be labeled.
    # Forward-only changes never enter these first four periods.
    base_ops = ops
    bases, prior_units = [], []
    for p,a in enumerate(d['actuals']):
        title = c['title']['base_adoption']*c['title']['base_charge']*(not c['title']['bundled'])
        delivery = c['delivery']['base_adoption']*c['delivery']['base_charge']*(not c['delivery']['bundled'])
        allin = base_ops[p]['core_RPU']+title+delivery
        insurance = a['us_service']*c['insurance_service_fraction']
        units = insurance*1e6/allin
        prior_units.append(units)
        bases.append(dict(insurance_core=units*base_ops[p]['core_RPU']/1e6,title=units*title/1e6,
            delivery=units*delivery/1e6,other_us=a['us_service']*(1-c['insurance_service_fraction']),intl=a['intl_service']))
        assert abs(sum(bases[-1].values())-a['us_service']-a['intl_service'])<1e-8
    arrivals = [prior_units[q]*ops[q+4]['assignments']/ops[q]['assignments'] for q in range(4)]
    # CAT is an explicit separate volume scenario with common economics by assumption.
    arrivals = [v*(1+c['cat_total_loss_activity'][q+4]) for q,v in enumerate(arrivals)]
    timing = c['sales_timing']
    if timing['mode']=='sale_equivalent':
        sales = arrivals; inventory = None
        core_revenues=[sales[q]*ops[q+4]['core_RPU'] for q in range(4)]
    elif timing['mode']=='assignment_flow':
        if timing['input_stage']!='assignments': raise ValueError('Do not lag a sale-equivalent carrier path again')
        if timing['kernels'] is None and c['title']['basis']!='assignments':
            raise ValueError('Title timing must use assignment-vintage adoption, not completed-sale adoption')
        sales,inventory,core_revenues=timed_core(arrivals,timing,c['title']['adoption'][4:])
    else: raise ValueError('Unknown sales timing mode')
    title,jt,title_flow=service_revenue(c['title'],sales,arrivals)
    delivery,jd,delivery_flow=service_revenue(c['delivery'],sales,arrivals)
    rows=[]
    with (ROOT/'docs/consensus_review_2026-09-28/total_revenue_consensus.csv').open() as f: street=list(csv.DictReader(f))[:4]
    jpm=[1180.,1146.,1261.,1196.]
    for q in range(4):
        p=q+4; a=d['actuals'][q]
        core=core_revenues[q]/1e6
        other=bases[q]['other_us']*c['other_us_units'][p]*c['other_us_fee'][p]
        intl=bases[q]['intl']*c['intl_units'][p]*c['intl_rpu'][p]*c['intl_fx'][p]
        us=core+title[q]/1e6+delivery[q]/1e6+other
        service=us+intl
        purchased=(a['us_vehicle']+a['intl_vehicle'])*c['purchased_units'][p]*c['purchased_asp'][p]
        total=service+purchased
        acq=c['acquired_total'][q]; acqs=c['acquired_service'][q]
        rows.append(dict(period=f'FY2027Q{q+1}',scenario=c['name'],status=c['status'],insurance_core_musd=core,
            title_musd=title[q]/1e6,delivery_musd=delivery[q]/1e6,other_us_musd=other,us_service_musd=us,
            intl_service_musd=intl,legacy_service_musd=service,purchased_musd=purchased,legacy_total_musd=total,
            modeled_insurance_sales=sales[q],insurance_sales_factor=sales[q]/prior_units[q],
            insurance_core_RPU=core_revenues[q]/sales[q] if sales[q] else None,
            insurance_core_RPU_factor=core_revenues[q]/sales[q]/base_ops[q]['core_RPU'] if sales[q] else None,
            insurance_ASP=ops[p]['ASP'] if inventory is None else None,TLF=ops[p]['TLF'],title_jobs=jt[q],delivery_jobs=jd[q],
            capiq_conditional_gap_musd=total-float(street[q]['total_revenue_mean_m']),
            jpm_legacy_total_gap_musd=total-jpm[q],
            consolidated_total_musd=None if acq is None else total+acq,
            consolidated_service_musd=None if acqs is None else service+acqs))
    return dict(quarters=rows,base_ledger=bases,base_modeled_units=prior_units,operating=ops,
                premium_diagnostics=premium_diagnostics,
                cells=cells,inventory=inventory,title_recognition=title_flow,delivery_recognition=delivery_flow,
                limitations=['Absolute units and component split are conditional, not observed',
                    'Carrier total-loss weights transferred to claim weights under common economics; cohort-specific weights unmeasured',
                    'Physical timing requires explicit vintage fee matrix; opening mix and value aging unmeasured',
                    'Physical assignments require explicit re-interpretation of sale-equivalent starting flows',
                    'CAT share/mix not measured; default combined pool, no extra CAT units',
                    'Historical fee vintage and damage-response elasticity remain unvalidated'])


def write_csv(path, rows):
    with path.open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
