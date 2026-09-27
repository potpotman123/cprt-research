"""Small local reconciliation and report; no workbook or source mutations."""
import csv, hashlib, json, pathlib, statistics as st
HERE=pathlib.Path(__file__).resolve().parent; ROOT=pathlib.Path('/Users/kwu/cprt')
r=json.loads((HERE/'results.json').read_text())
def read(name):
    with (ROOT/'data/csv'/name).open() as f:return list(csv.DictReader(l for l in f if not l.startswith('#')))
historical=[]
for year in ['2022','2023','2024','2025','2026']:
    rows=[x['scopes']['us_salvage_light'] for x in r['archive'] if x['status']=='parsed' and x['page']==1 and x['capture'].startswith(year)]
    historical.append({'year':year,'captures':len(rows),'lt_pct':st.mean(x['lt_pct'] for x in rows),'suv_pct':st.mean(x['body_counts'].get('SUV',0)/x['n']*100 for x in rows),'pickup_pct':st.mean(x['body_counts'].get('PICKUP',0)/x['n']*100 for x in rows),'mean_model_year':st.mean(x['mean_my'] for x in rows)})
# Independent source-chart check found one transcription difference; preserve original CSV.
p={x['age_bucket']:x for x in read('ccc_tl_share_by_age_2020_2025.csv')}
t={x['age_bucket']:x for x in read('ccc_tl_valuation_share_by_age_2020_2025.csv')}
p['10-12']['cy2020']='31.8'
def dist(y):
    pp={b:float(x[y])/100 for b,x in p.items() if b!='total'}
    w={b:float(t[b][y])/pp[b] for b in pp};s=sum(w.values())
    return {b:v/s for b,v in w.items()},pp
ccc=[]
for a,b in [('cy2020','cy2022'),('cy2022','cy2025'),('cy2024','cy2025')]:
    w0,p0=dist(a);w1,p1=dist(b)
    mix=100*sum((w1[k]-w0[k])*p0[k] for k in p0)
    within=100*sum(w0[k]*(p1[k]-p0[k]) for k in p0)
    inter=100*sum((w1[k]-w0[k])*(p1[k]-p0[k]) for k in p0)
    ccc.append({'period':a[2:]+'–'+b[2:],'base_mix_pp':mix,'symmetric_mix_pp':mix+inter/2,'symmetric_within_pp':within+inter/2,'total_pp':mix+within+inter})
fee=[x for x in read('copart_fee_grid_2026-09.csv') if all(x[k]==v for k,v in {'page':'non-licensed','title_group':'non-clean','vehicle_class':'standard','payment_method':'secured','fee_type':'buyer_fee'}.items())]
def f(price):
    hits=[x for x in fee if float(x['band_low_usd'])<=price<=float(x['band_high_usd'] or 'inf')]
    assert len(hits)==1
    x=hits[0];assert x['fee_usd'],'This screen intentionally uses fixed dollar bands only'
    return float(x['fee_usd'])
fees=[]
for price in (2000,4000,8000):
    a,b=f(price),f(price*1.5)
    fees.append({'car_price_assumed':price,'suv_price_assumed':price*1.5,'car_buyer_fee':a,'suv_buyer_fee':b,'fee_gain_pct':100*(b/a-1),'break_even_sale_probability_ratio':a/b})
sources=[]
for name,pop,status in [('copart_fee_grid_2026-09.csv','One documented buyer category; not actual buyer mix','Previously transcribed schedule; used as read, not freshly verified online'),('ccc_tl_share_by_age_2020_2025.csv','CCC all-loss claim count by age, with source methodology disclaimer','Visually checked; local analytical override 31.6 to 31.8 for CY2020 age 10–12'),('ccc_tl_valuation_share_by_age_2020_2025.csv','CCC share of total-loss valuations by age','Visually checked against stored chart; compatibility with claim-count population remains a limitation')]:
    path=ROOT/'data/csv'/name;sources.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'population':pop,'status':status})
summary={'historical_page1':historical,'ccc_chart_corrected':ccc,'fee_bounds':fees,'input_register':sources,'source_correction':{'field':'10–12 years, CY2020 total-loss share','stored':31.6,'chart':31.8,'source_csv_modified':False}}
(HERE/'summary.json').write_text(json.dumps(summary,indent=2))
hist='\n'.join(f"| {x['year']}{' (January only)' if x['year']=='2026' else ''} | {x['captures']} | {x['lt_pct']:.1f}% | {x['suv_pct']:.1f}% | {x['pickup_pct']:.1f}% | {x['mean_model_year']:.2f} |" for x in historical)
ct='\n'.join(f"| {x['period']} | {x['base_mix_pp']:+.3f} | {x['symmetric_mix_pp']:+.3f} | {x['total_pp']:+.3f} |" for x in ccc)
ft='\n'.join(f"| ${x['car_price_assumed']:,.0f} → ${x['suv_price_assumed']:,.0f} | ${x['car_buyer_fee']:,.0f} → ${x['suv_buyer_fee']:,.0f} | {x['fee_gain_pct']:.1f}% | {x['break_even_sale_probability_ratio']*100:.1f}% |" for x in fees)
report=f'''# CPRT: first local research pass

September 26, 2026. Executed the initial local listing audit, age-decomposition reconciliation, and a buyer-fee break-even screen. No network requests, paid data, OCR or source-workbook changes. Two existing CCC chart images were visually inspected. Existing uncommitted repository data updates were left untouched.

## What this pass establishes

1. The saved archive can be processed cheaply. Ordinary XML parsing and a narrow treatment of invalid records recover 95 usable sitemap files from 100 saved files.
2. The increase in SUVs/crossovers remains visible in a same-page historical comparison. It is not solely a consequence of combining different archive pages within a month. This does not establish representative sold-vehicle composition or body-specific total-loss probability.
3. The small 2024–2025 claims-age-mix contribution survives recomputation and an alternative decomposition convention. Source-population mismatches still limit precision.
4. The saved buyer-fee schedule provides a concrete economic reason why higher sale prices may fail to offset fewer transactions. Actual cohort prices and probabilities remain unmeasured.

## Acquisition and parsing results

The input comprised 100 existing archive files totaling 553.1 MB and three recent database snapshots. The three-file pilot took 0.52 seconds. The final archive/database audit took {r['elapsed_seconds']:.2f} seconds of local wall time. These are execution times, not total research effort or credit usage.

- 90 XML files parsed initially.
- Five more contained an invalid `&#26;` reference, each inside one URL record. The parser excluded those five complete records in memory, saved their hashes, and parsed the remainder. Original files were preserved. It did not substitute a guessed vehicle description.
- Four files are HTML/challenge responses, not sitemaps. They are unavailable observations, not zero inventory.
- One file is empty.
- The resulting files contained 4,166,708 URL elements after those five exclusions. These are repeated source observations, not unique vehicles over time.
- 6,366 URL elements did not match the required lot-ID/model-year structure and were excluded from the composition calculation. That is approximately 0.153% overall, with higher rates in some individual pages. Their composition is unresolved.
- Each historical file remains a separate observation. The trend below uses page 1 only, with equal weight per capture within the year; it is not a complete or randomly sampled annual series. Page ordering and source coverage can still change.
- Duplicate IDs within captures are removed. IDs with conflicting attributes are excluded. The live captures contained 16, 1 and 1 conflicting IDs, respectively.

The September 25 and September 26 database captures have identical hashes of the selected deduplicated vehicle records. They are not independent evidence of a daily operating change. This could reflect an unchanged or stale source; this pass does not identify why it repeated.

## Vehicle-composition result

Population: listings with a recognized US state, a salvage/nonrepairable title label and a classified car/SUV/pickup/van body. Salvage-title is not proof of insurer consignment. All classifications reuse the existing rules; the classifier's fallback-to-car behavior still needs validation. No claim-level or sale-outcome data were added.

| Year | Page-1 captures | Light trucks | SUVs/crossovers | Pickups | Mean model year |
|---|---:|---:|---:|---:|---:|
{hist}

The light-truck increase from 2022 to 2025 is about 8 percentage points in this comparison. SUVs account for approximately 7 points; pickups account for approximately 1 point. This supports retaining separate SUV/crossover and pickup assumptions in the model.

The September 25 live capture has a light-truck share of 56.93% in the filtered US salvage light-vehicle sample, after duplicate/conflict handling. It combines available pages and is therefore not directly identical in coverage to the historical page-1 comparison.

Mean model year rises along with observation year. That is evidence of newer manufacturing cohorts in the listing pool, not by itself evidence that the pool is becoming older, or that salvage ASP rises by a particular amount. Listing dwell times, consignor mix and source coverage can influence these statistics.

## Aging reconciliation and source correction

I visually checked the two stored CCC chart images against the extracted tables. Figure 19 shows 31.8% for the 10–12-year group in CY2020; the stored CSV says 31.6%. The analysis below uses a local override to 31.8%, recorded in the input register. The source CSV and workbooks have not been changed.

The base-period decomposition values changes in age weights at initial totaling rates. The symmetric version assigns half the interaction to each component. Neither makes the decomposition causal.

| Period | Age-mix effect, base-period method (pp) | Age-mix effect, symmetric method (pp) | Reconstructed TLF change (pp) |
|---|---:|---:|---:|
{ct}

For 2024–2025, the symmetric age-mix contribution is approximately 0.027 percentage points out of a 0.710-point reconstructed increase: about 4%. Most of this accounting increase occurs within the age groups. This does not prove that repair inflation caused the remainder: damage, body, carrier composition and aging within broad buckets can contribute.

The reconstruction uses total-loss valuation shares and claim-count totaling rates as if their populations are compatible. Their published totals do not reconcile exactly, especially early in the series, and CCC states an age-methodology limitation. The chart check confirms the labels, not population identity. Therefore the precise historical attribution remains qualified; the tables should not be used as proof that fleet aging is permanently over.

## Buyer-fee break-even: a conditional economic test

Use the stored September 2026 fee table for non-licensed buyers, non-clean titles, standard vehicles and secured payments. For illustration only, assume an SUV sells for 50% more than a car. These are not measured cohort sale prices. Include only the buyer fee; seller fees, ancillary charges and costs are excluded.

Expected buyer-fee revenue per comparable exposure is sale probability multiplied by buyer fee. Therefore the break-even relative sale probability is car fee divided by SUV fee. If claim frequency is identical, this could be interpreted as a relative totaling probability; otherwise it combines the different stages of the supply funnel.

| Assumed auction prices | Posted buyer fees | Buyer-fee increase | SUV sale probability needed relative to car |
|---|---:|---:|---:|
{ft}

In the $4,000/$6,000 example, 50% more auction value produces only 13.8% more buyer-fee revenue per transaction. If the higher-value cohort generates more than approximately 12.1% fewer sales per comparable exposure, expected buyer-fee revenue is lower. This is an exact calculation for that saved schedule and scenario, not an estimate of the actual cohort effect.

The result supports the proposed mechanism but does not validate the existing -0.24% revenue forecast. We still need defensible relative repair costs, expected recoveries, exposure/frequency and actual sale-price distributions. A single buyer category and price pair cannot establish total service revenue or profit.

## Capacity feasibility: initial local field audit

The inspected listing table has capture time, lot ID, title label, model year, make/model, state, yard, sitemap modification time and URL. It does not have verified physical arrival, completed sale, pickup, usable spaces or developed acreage. The existing yard summary contains yard/event counts rather than those capacity measures. Company facility-cost totals do not identify local spare capacity.

Consequently this pass does not estimate utilization, dwell time or CapEx. An appropriate next capacity step is a bounded source check for a few facilities' operational capacity and capabilities. More of the same listing rows would not fill the missing physical timestamps. Other repository tables have not all been ruled out by this initial field audit.

## What should happen next

The next demographic step is to audit consequential vehicle classifications and test the existing revenue conclusion against alternative repair-cost and recovery relationships. Start with algebra and existing tables. The observed SUV mix trend warrants that work, but it does not validate the fitted totaling differential.

For capacity, seek source-supported developed/usable capacity or operational clocks before expanding collection. There is no basis yet for a national site scrape or a detailed queue simulation.

This pass is complete. Larger provider acquisition, OCR campaigns or historical sale-event collection remain outside this pass and require a separate scope/cost proposal. The user has already authorized ordinary cheap continuation; another approval is not required merely to do a bounded local check.

## Reproducibility and evidence

The adjacent `results.json` holds per-file hashes, timestamps, parsing exclusions, composition summaries, recent snapshot hashes and the original-table CCC reconciliation. `summary.json` holds the local source correction, exact values underlying this report, fee scenarios and the source register. `audit.py` and `summarize.py` reproduce the work without network access or source-file mutation. Existing licensed files remain local.
'''
(HERE/'first_pass_findings.md').write_text(report)
print(json.dumps({'report':str(HERE/'first_pass_findings.md'),'corrected_ccc':ccc,'fees':fees},indent=2))
