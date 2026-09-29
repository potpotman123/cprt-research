# One-year archive feasibility — 2026-09-28

## Outcome
Historical record access passes: a September2025 Copart event is readable and a reported price is available on a second archive. Reproducible date-window enumeration, matched cohort construction and price validation remain unpassed. No year-over-year price calculation or model input. Do not confuse this access test with a completed matched-price study.

## Scope and selection
Reused SALE_OUTCOME_FEASIBILITY.md rather than repeat its conflicts. Target September1–28 in2025 and2026, US Copart Camry, fixed-model-year2016 and an alternative equal nominal age comparison (2016 in2025 vs2017 in2026). Exact build/registration age unavailable. Same generation alone does not fix trim, mileage, damage or title. Bounded six search queries, archive landing/filter inspection, two new Copart event candidates; earlier2026 records retained. Search-found convenience records, not a probability sample. No silently replacing hidden observations with visible prices.

## New records
2025 control: lot71432145 VIN4T1BF1FK6GU532664,2016 Camry LE,66,220 miles,Detroit, certificate of title(MI), September19,2025. BidCars history says Sold/Insurance company but price hidden. Stat.vin reports same date/lot/VIN,Sold,$7100,Allstate,front end,run&drive. Numerical price is SINGLE-SOURCE, sold date is corroborated; not settlement-verified.
- https://bid.cars/en/lot/1-71432145/2016-Toyota-Camry-4T1BF1FK6GU532664
- https://stat.vin/cars/4T1BF1FK6GU532664

Equal nominal age candidate2026: lot63999876 VIN4T1BF1FK6HU671677,2017 Camry SE,122,613 miles,Atlanta West,GA salvage title,September1,2026,Sold/Insurance company in BidCars. Search snippet displayed$2050; opened record hides amount. Do NOT admit cached snippet as verified price. Stat.vin VIN URL inaccessible once; no retry. Mileage,trim,geography,title already mismatch2025candidate, independent of missing price; no paired estimate.
- https://bid.cars/en/lot/1-63999876/2017-Toyota-Camry-4T1BF1FK6HU671677
- https://stat.vin/cars/4T1BF1FK6HU671677 (access failed)

Fixed2016 candidates from prior check:47794676 Sept14,2026,174571miles,Fairburn,SE,side/rear,$950 single-source with corroborated sold date;49409146 Sept18,351593miles,noninsurance,price conflict2750/3200. Neither is comparable to low-mileage2025LE. Full URLs and exclusions remain SALE_OUTCOME_FEASIBILITY.md. Zero matched pairs admitted. Lower visible values on these very different vehicles do not establish market decline.

## Archive controls
BidCars archive link opens:
https://bid.cars/en/search/archived/results?auction-type=All&make=All&model=All&search-type=filters&status=All&type=Automobile&year-from=1900&year-to=2027
Readable page exposes auction-date sorting, model-year range, auction platform, mileage, start-code and damage/loss filters. No functioning custom sale-date interval or stable dated result enumeration was verified with text access. Model year is not sale year. No claim that browser UI lacks a date control; only this access route is unverified. No broad pagination or browser automation launched.

https://finalbid.vin/en/toyota/camry/2016 exposes Prev/Next pagination, aggregate date range May21,2019–Oct1,2026,15,560 advertised auctions,14,846 recorded bids,median2800,mean3033,71%Copart/29%IAAI at inspection. These are site-reported pooled figures, not measured coverage or a usable YoY index. Date range extends beyond current audit date; don't assume all aggregate entries are completed as of cutoff. Landing page content counts changed between retrievals; do not use counts as independent accuracy validation. No date-range filter verified. One direct HTTP attempt403; web text readable; no retries or bypass.

## Queries
1. site.bid.cars "2016 Toyota Camry" "2025-09" "Sold"
2. site.finalbid.vin/en/toyota/camry/2016 "Sep" "2025"
3. "4T1BF1FK6GU532664" "price"
4. site.bid.cars "2016 Toyota Camry" "2025-09" "$" "Sold" -532664
5. site.bid.cars "2017 Toyota Camry" "2026-09" "Sold"
6. "2016" "Camry" "Copart" "Sep" "2025" "finalbid.vin" (no results)
Alternative Carfast paginated search lead spans mixed models/platforms/dates, not a predefined date population; not expanded. New IAA hits excluded from Copart comparison. Sources can share feeds, agreement is not independent ground truth. All observations above are web text transcriptions, no raw downloaded snapshots claimed.

## Decision
No need to wait a year for our own scraper: historical reconstruction is possible in principle. Next bottleneck is a single interactive/archive-export access check to establish date-window enumeration and hidden-price access conditions. Then propose a modest matched pilot with fixed date/platform/model-age/mileage/damage/seller frame and retained missing/conflicting records, requiring adequate overlap in both years. Do not spend on large collection until that gate passes. Primary invoices would improve field validation but absence of invoices does not by itself preclude an explicitly secondary-source directional indicator; it requires cross-source/conflict/missingness robustness instead. No paid access, signup, outreach, OCR or bulk scrape performed.

## Interactive follow-up — September 28, 2026

Browser UI check completed; date-window enumeration gate remains unpassed. This supersedes the proposed interactive next step above. No matched return or forecast input created.

- **BidCars:** loaded archive with Toyota/Camry/2016–2016/Copart chips selected. Year, odometer, start-code, loss-type and other vehicle controls visible. Auction-date ascending/descending available under Sort By; clicked ascending. No custom sale-date interval found in inspected controls. Filtered result said “Unfortunately, nothing was found.” Then clicked native footer Archived link, removing all restrictive filters (all makes/models/platforms; 1900–2027); loaded broad archive also returned nothing. This session cannot enumerate even the unrestricted archive. This is an access/search-path limitation, not evidence of zero historical sales. Individual records were readable in the preceding test. One early year-button attempt timed out during initial loading; refreshed DOM rather than repeated clicks.
- **FinalBid:** model/year page loaded visible lot cards with prices, mileage, damage, location and dates. Header Auction archive opened https://finalbid.vin/en/archive; inspected full rendered DOM and available controls. VIN/lot search and Next pagination present; no custom sale-date, mileage-range or combined damage/model/year filter found. FAQ explicitly directs users to make/model/model-year pooled summaries. Separate Browse by damage/state/loss links exist, but their intersection with model/year/date was not verified. Archive displayed some September 29 records as sold on September 28; scheduled dates, timezone effects or status timing could explain this, so do not treat displayed dates automatically as completed-sale timestamps. Landing page also contains buy-now labels. Prices/statuses require lot-level checks.
- **Design:** model year is not age or sale year. Equal nominal age comparison shifts model year forward one year (2016 in September 2025 vs 2017 in September 2026). This still requires generation/trim, mileage, title, geography, seller and damage comparability. Exact age cannot be inferred from model year alone. Damage category does not measure severity. Keeping 2016 fixed instead ages the cohort and estimates a different comparison.
- **Stop:** no deep pagination, authentication, purchase, endpoint guessing, hidden-state extraction or bulk collection. Current UI does not establish a cheap reproducible date-window sample. A documented dated export/search facility is preferable to hand-browsing hundreds of pages or search-engine convenience sampling; availability remains unknown. Existing pages remain useful for selected-lot verification only, not a representative YoY bid index.

Screenshots of inspected broad archive pages: [BidCars](bidcars_interactive_archive.png), [FinalBid](finalbid_interactive_archive.png). These preserve page state, not primary settlement evidence. Prior lot-price conflict and missing-price exclusions remain in force.
