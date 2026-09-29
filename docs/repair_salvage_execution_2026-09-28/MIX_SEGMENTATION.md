# Repair operations and replacement sourcing: first segmentation

As of 2026-09-28. Incremental evidence update; no forecast coefficients changed.

## Question and method
Separate (1) repairing an existing component vs replacing it, (2) sourcing a replacement, (3) price and component/vehicle mix. These determine repair costs differently and only recycled demand directly requires donor parts. Reused existing CCC report, inspected three original chart images, followed one new Mitchell/Enlyte primary-source lead. Published tables are cheaper and better defined than scraping individual listings, but do not identify same-component substitution or near-total-loss effects. No paid data, bulk extraction, OCR or agents.

## Observed replacement mix: CCC 2026, Figures 38–39

| Category | 2024 replacement dollars share | 2025 share | Change pp | 2024 parts/appraisal | 2025 parts/appraisal |
|---|---:|---:|---:|---:|---:|
| OEM | 63.5% | 61.7% | -1.8 | 9.5 | 8.8 |
| Aftermarket | 21.0% | 22.7% | +1.7 | 3.2 | 3.3 |
| Recycled | 10.7% | 10.5% | -0.2 | 0.6 | 0.5 |
| Reconditioned | 1.3% | 1.3% | 0.0 | 0.1 | 0.1 |
| Optional OEM (source label OPT OEM/Opt-OE) | 3.5% | 3.8% | +0.3 | 0.3 | 0.3 |
| Published total | 100.0% | 100.0% | 0.0 | 13.6 | 13.0 |

Source: https://www.cccis.com/reports/crash-course-2026 . Figure 38 = percent of total part replacement dollars by part type. Figure 39 = average part counts; surrounding prose specifies non-comprehensive repairable appraisals for total counts. Subgroup table does not independently restate exclusions. Keep these as source-reported aggregates; do not assume paid invoices or all damaged vehicles.

Original images inspected locally: raw/ccc_figure38.webp, raw/ccc_figure39.webp, raw/ccc_figure41.webp in this directory (ignored raw cache). Original HTML/text already at repository raw/ccc/crash-course-2026.*. Image URLs:
- https://cdn.prod.website-files.com/677e7ecbb3dbbe98615cde30/69caddd856f7229d2d89fd7d_Picture38.webp
- https://cdn.prod.website-files.com/677e7ecbb3dbbe98615cde30/69caddd8b5f2b84e5e2535e2_Picture39.webp
- https://cdn.prod.website-files.com/677e7ecbb3dbbe98615cde30/69caddd8993b32e383ef2ee8_Picture41.webp

Checks/derivations: dollar shares sum to 100% both years. Rounded category counts sum to 13.7 in 2024 vs published 13.6; 2025 sums to 13.0. Therefore category count changes sum to -0.7 vs total -0.6: a +0.1 rounding residual, not an economic category. Total count change = 13.0/13.6-1 = -4.41%. Do not give a precise recycled growth rate from 0.6 to 0.5: rounding is material. Do not equate +1.7pp spending share to +1.7pp physical substitution. Secondary reporting encountered conflated 2024 OEM 63.5% with 2025; primary chart resolves 2025 to 61.7%.

## Repair vs replace: separate measurement

Primary Enlyte/Mitchell, Ryan Mandell, 2026-06-01:
https://www.enlyte.com/insights/article/industry-trends/navigating-complexity-collision-claims

Reports percentage of parts repaired 14.8% in 2024 to 15.5% in 2025 (+0.7pp), first increase in more than a decade. Article does not fully document operation eligibility, geography, sample size, or sample stability. Admit as reported historical statistic, not a cohort-specific probability. Same article reports OEM price inflation 4.21% and aftermarket 3.89% in 2025; these are not matched-component discount levels or proof that whole repair bills fell.

CCC Figure 41/prose: repair labor share of total labor dollars fell 0.3pp. Age groups are current/newer, 1–3, 4–6, 7+. Chart labels are whole-percent rounded; use prose for aggregate 0.3pp. Labor-dollar shares and repaired-part counts measure different things. More low-dollar repairs could raise repaired-part frequency while expensive replacement operations increase labor-dollar weight. Different vendor samples are another explanation. We cannot identify which explanation dominates from these aggregates.

Revision to previous qualitative interpretation: a claim of uniformly increasing replacement instead of repairing is not supported across current measures. PartsTrader technician-shortage discussion is a possible mechanism; Mitchell's measured repaired-part share moved the other way in 2025. Mitchell and PartsTrader share Enlyte ownership; don't count their narratives as fully independent confirmation. CCC is a separate estimator dataset, but insurers/shops may overlap.

## Model interpretation and competing explanations

Observed: aftermarket intensity rose; recycled intensity fell; total replacement counts fell. This contradicts automatically mapping alternative-parts adoption to a positive recycler demand/salvage-price coefficient.

Still unidentifiable from these aggregates:
- Same-component sourcing substitution vs vehicle age, impact type, severity and component mix.
- Fewer replacements from repairing more vs severe candidates leaving repairable sample as total losses vs reporting/coverage or estimate-process changes.
- Fixed-basket repair cost savings vs inflation and expensive-component mix. A larger aftermarket share can coexist with rising bills.
- Donor bid effect: repair-job volume × recycled pieces/job × resale value/recovery costs/inventory matters; neither share nor pieces/job alone identifies total demand. Exporter/rebuilder demand and salvage supply can offset recycler weakness.

Use in model now: historical observation/validation layer, separate operation/source/price dimensions. Keep causal repair and salvage shocks as assumptions; no point estimate for revenue delta follows. Existing -3% repair/+3% salvage scenario is not validated by these data.

Next discriminating test: fixed vehicle-age × component × impact cohorts, estimating repaired share and OEM/aftermarket/recycled count shares together; pair with repair-job volume and recycler volumes/inventory if obtainable from existing sources. Without matched data, use explicit alternative mechanisms rather than fitting a substitution coefficient to national averages. Stop before paid extracts or large collection.

## Discovery and access record
Queries (bounded initial pass):
1. site.mitchell.com 2026 parts utilization OEM aftermarket recycled repair replace percentage
2. site.cccis.com 2026 "parts" "OEM" "share"
3. site.partstrader.com 2026 "repair" "ratio" replacement
4. site.enlyte.com "2026" "parts repaired"
5. site.mitchell.com "2026" "parts" "utilization" "2025"

Secondary lead: https://www.autobodynews.com/news/enlytes-2026-trends-report-tracks-climbing-calibration-costs-uneven-parts-inflation-and-a-repair-rate-reversal . Its report link led to Enlyte homepage; followed June 2 press release → 2026 report → Auto Physical Damage → collision article above. Verified repaired-part statistic in primary article; no need to retrieve gated full report. Secondary reused-parts story was not admitted over primary CCC chart. No failed bulk collection repeated.
