# Evidence and source decisions — 28 September 2026

## Existing sources recovered and used

- JPMorgan September 11 report, file ending `124345098.txt`, Table 3, text lines 275–278: FY27 agency/service revenue $4,061m; principal/purchased revenue $721m; total $4,782m. Quarterly summary lines 358–359: total revenue $1,180m/$1,146m/$1,261m/$1,196m. Quarterly rounded sum is $4,783m, $1m above the annual row; preserve both. Acquisition exclusion appears at lines 37–38. FY27 service growth versus reported FY26 is 2.30%, not a claim about buy-side expectations. These dated forecasts are a named benchmark, not a replacement for CapIQ's eight-contributor total. `evidence.py` extracts the numeric rows and records source hash and lines in `evidence_manifest.json`.
- Existing CapIQ September 28 export: quarterly total revenue only, acquired perimeter unverified. Keep annual sum of quarters $4,860.97m separate from JPM's $4,782m. Their $78.97m difference is not alpha; dates, contributors and assumptions differ. Quarterly JPM service values are unavailable, not derived by imposing annual agency mix on each quarter.
- `raw/transcripts/call_2026-09-10.txt`, lines 216–226: US insurance ASP +3.7% and international service growth/RPU disclosure. The 3.7% future auction-price case is a continuation assumption at fixed selection, not management guidance. International fee-unit growth is derived from exact service-dollar growth divided by 1.035, then hypothetically continued. Its RPU is in reported currency; no second FX factor is applied.
- US noninsurance +0.2% units and +5.9% ASP in the same call include a different perimeter, including principal activity. They were deliberately not inserted as measured growth for other-US consignment service revenue. Other-US +/-5% activity cases are transparent stresses, not data-derived ranges.
- JPM's approximately +5% US Q4 service RPU is retained separately as a soft historical cross-check; the official history row remains unresolved. No analyst estimate was relabeled a company disclosure.
- Saved September 26 fee-grid selection remains the schedule source. Public page text currently mixes $79 and $95 gate sections. That does not establish a dated price cut/increase; no automatic replacement was made.

## Bounded external discovery

Four search queries, strongest primary pages selectively inspected. No bulk download, scraping, OCR, outreach or paid data:

1. `site.lkqcorp.com 2026 second quarter salvage procurement prices salvage vehicles`
2. `site.cccis.com 2026 salvage returns vehicle values repair total loss`
3. `site.boydgroup.com 2026 second quarter total loss repairable claims`
4. `site.copart.com delivery fees waived gate fee automatic delivery`

**LKQ, July 30 2026 release:** North America returned to organic growth; management describes alternative-parts utilization above 40% and improving repairable claims. This supports examining alternative-parts repair economics and contradicts assuming uniformly deteriorating repair demand. It does not measure comparable-job repair-cost deflation, salvage recovery or Copart auction bids. [Official SEC exhibit](https://www.sec.gov/Archives/edgar/data/1065696/000106569626000041/exhibit991.htm), opening operating commentary. No numerical model coefficient adopted.

**Boyd, Q2 2026 release:** management estimates repairable claims flat to down 2%, with limited repair-cost contribution to its growth; it attributes company outperformance substantially to share gains. That supports stabilization and requires separating repairer share gains from industry claims. It does not measure total losses or latent cost for a fixed damage scope. The underlying claims-processing source may overlap other industry datasets, so this is not automatically an independent statistical sample. [Official release](https://boydgroup.com/investor/investor-news/news-details/2026/Boyd-Group-Services-Inc--Reports-Second-Quarter-2026-Results/default.aspx), Outlook. No claims-frequency forecast adopted from repairable-only data.

**CCC workflow leads:** indexed job aids describe anticipated supplements and vendor-supplied anticipated salvage. Full PDF retrieval failed; retain as schema leads, not an available dataset or validated elasticity. URLs: https://help.cccis.com/training/insurance_company/estimating/orientation/JobAids/CCC_ONE_SALVAGE_TVR.pdf and https://help.cccis.com/training/insurance_company/salvage/CCCONESalvageTVR.pdf. The indexed fields motivate distinguishing expected versus realized salvage, but supply no magnitude. No OCR escalation.

**Delivery:** search surfaced Canadian/UK waiver terms and mixed US fee-page content. Cross-jurisdiction terms do not establish a US waiver rate. Existing delivery disclosure search remains the governing limit; product revenue, jobs, adoption and gross/net are not identified. This pass did not reopen the parked delivery collection project.

## Conclusions admitted to the model

New benchmark observations and soft historical controls enter their own tables. The engine receives explicit scenario inputs, not new inferred empirical repair/demand coefficients. Supplier and repairer evidence changes research priorities and counterarguments; it does not justify mapping a selected repair average onto the latent damage distribution. Pre-loss values, marginal total-loss response, service levels and absolute insurance counts remain unresolved.
