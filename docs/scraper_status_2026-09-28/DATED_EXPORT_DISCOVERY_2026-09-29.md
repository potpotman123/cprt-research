# Dated historical access: bounded discovery, September 29, 2026

## Decision
Found a documented dated aggregate route, NOT a validated matched historical dataset. Best low-cost next candidate is Apibara's free authenticated test. No account created, provider contacted, paid service purchased, authenticated data queried, or bulk collection performed. No new price estimate enters the Copart model.

Reviewed preceding YEAR_OVER_YEAR_FEASIBILITY.md and standing instructions. Six search queries across archive operators, direct Copart and structured-data vendors; selectively inspected provider documentation. Provider claims below are not independently verified coverage or accuracy.

## Ranked routes
1. **Apibara:** https://apibara.tech/en/products/vehicle-auction-data-api/endpoints and https://apibara.tech/openapi/v1.json document `/market/sold-prices`: make, model, exact year, damage, auction (copart/iaai), sale_date_from and sale_date_to. Returns retained positive sold-history count/average/min/max. This establishes documented date filtering for aggregates, not row-level dated export. Listed parameters omit mileage, trim, seller, geography and explicit status filtering. Its canonical price description includes final/approval prices; clarify whether aggregates exclude on-approval/uncompleted outcomes. Date boundary inclusivity/timezone, retention consistency and event deduplication unknown. https://apibara.tech/en/pricing advertises 100 requests/month free without card; authenticated entitlement still untested. https://apibara.tech/en/vehicle-auction-dataset distinguishes lifetime indexed from retained records and directs custom data requests to contact. Direct public schema retrieval via Python returned403 once; web reader accessible; no bypass/retries.
2. **API Auctions (apiauctions.io; distinct from auctionsapi.com):** https://apiauctions.io/docs documents `/api/v1/get-cars` paginated make/model/year search with vehicle history; date filters were documented on buy-now search, not this historical enumeration endpoint. Could filter historical rows locally but collection volume unknown. Homepage https://apiauctions.io advertises 10 demo requests/hour with card required; PAYG $0.01/request, minimum top-up$25, auto-refill mentioned. Not recommended to pay without demonstrating the required sampling frame. Linked OpenAPI retrieval failed once. Marketing version2 and detailed version1 docs require reconciliation before coding.
3. **AuctionsAPI (auctionsapi.com):** https://auctionsapi.com/auction-docs has sale_date_from/to, model-year, mileage, damage, platform and status filters, but identifies `/api/cars` as ACTIVE inventory. `/api/archived-lots` is recent archival synchronization, not documented year-old date-window enumeration. VIN/lot history useful for spot checks, insufficient proof of historical sample access. Demo requires key. Do not treat archive removal as completed sale.
4. **Copart direct:** search surfaced https://www.copart.com/content/us/en/buyer/sales/downloadsalesdata, described as scheduled inventory updated every15minutes. Page open failed; search description alone suggests upcoming lots, not historical settled outcomes. Lower priority for this specific question.
5. **BidCars/FinalBid:** no official documented dated export found in bounded searches. Third-party scraper wrappers surfaced but do not independently resolve date selection, price conflicts or access. No claim that export is impossible. Prior browser findings remain.

## Proposed small access test, contingent on free account availability
Cap at12 authenticated requests; no pagination expansion. First check entitlement and filter vocabulary. Request identical September1–28 windows for 2016 Camry in2025 and2017 in2026, Copart only; then same2016 year in2026 as an aging sensitivity. Use remaining requests for known controls71432145,47794676,49409146 (the last has conflicting prices across archives), date/status checks and at most one primary-damage split if sample exists. Store returned responses and exact filters; separate observed from missing and conflicting fields. No photos/OCR. This tests provider consistency and historical coverage, not causal aftermarket substitution.

Stop if dates do not filter as documented, known events are mismatched, old coverage absent, price/status semantics unresolved or row-level controls inaccessible. Aggregate difference is discovery only: mileage, seller, title and damage-severity changes can explain it. Do not transplant a pooled percentage into ASP/RPU. A small row-level dated sample export would be preferable to purchasing broad access or crawling years of records. Requires separate explicit authorization before outreach or paid collection. Model delta remains unestimated.

## Exact discovery queries
- site.bid.cars API auction history export date
- site.finalbid.vin API export auction history date
- site.stat.vin API auction date historical data
- historical Copart auction results API sale date filter export
- site.finalbid.vin "export" "API"
- site.bid.cars "API" "history"
