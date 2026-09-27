# Paired ACV / auction proceeds feasibility pilot

Executed 2026-09-26 US Eastern (raw retrieval timestamps are Sep27 UTC). Purpose: establish whether a small public sample can pair pre-accident value and accepted sale proceeds, before scaling or replacing model assumptions. Seven unique candidate VINs inspected; two secondary-corroborated pairs; zero primary-settlement-verified pairs; zero matched cross-body comparison sets. No model coefficients changed.

## Procedure and cost discipline

1. Search 2016 Camry, RAV4 and F150 records displaying both ACV and final bid. This fixes model year for initial feasibility, not mileage, severity or drivetrain. Search-discovered records are a convenience sample and cannot establish a population mean.
2. Open candidate pages; separate numeric fields from AI-generated condition prose. Do not use visual descriptions synthesized by archive AI as verified damage measurements.
3. Search by VIN and compare event histories on a second archive/broker. Match VIN, lot identifier AND sale date. A highest bid is not necessarily an accepted sale. Different sites may use a common feed; agreement is corroboration, not independent ground truth.
4. Record earlier unsuccessful attempts, title history, seller, mileage, damage, run condition and sale channel. Reject zero/missing value fields instead of treating them as actual zero ACV. Record Buy Now separately from competitive auction and timed sale.
5. Try underlying IAA/Copart links for two promising records. IAA search exposed only an iframe; Copart lot was inaccessible. No primary verification claimed.
6. Compute proceeds/ACV only for the two secondary-corroborated records. Do not estimate a body premium from unmatched records. All exclusions remain in the ledger.

Used readable web text plus five direct HTML attempts (two successful). No OCR, image downloads, paid reports, account creation, outreach, or bulk scrape. Raw successful pages and failed request logs are retained. Most web-tool observations are recorded as structured factual transcriptions with URLs in candidate_ledger.json, not misrepresented as raw downloaded snapshots.

## Results

| Record | Reported ACV | Accepted sale reported by archives | Gross recovery | Disposition |
|---|---:|---:|---:|---|
| 2016 Camry LE, VIN ending 557682 | $9,680 | $2,100, Sep14 2026 | 21.69% | Corroborated secondary pair; Buy Now; front/left damage; 188,328 mi |
| 2016 F150 XL, VIN ending D57189 | $8,533 | $3,550, Sep17 2026 | 41.60% | Corroborated secondary pair; side damage; 198,379 mi |

These are not a matched pair. Similar model year and mileage do not remove differences in damage severity, configuration, seller, geography, platform or selling method. The pickup has lower reported ACV here, illustrating why individual vehicles cannot represent category means. Seller net proceeds, settlement invoices and complete crash severity remain unavailable. Gross recovery cannot be substituted directly for the insurer's net salvage fraction without seller costs/fees.

## Errors caught before aggregation

- Camry 4T4BF1FK4GR540574: vin-archive calls $1,850 sold. BidCars history identifies Sep18 $1,850 as not sold, Sep25 $3,225 as sold. Also reconstructed title and a separate 2019 sale. Excluded from clean first-total-loss sample. Do not average attempts or combine 2019 price with 2026 ACV.
- RAV4 2T3DFREVXGW533908: vin-archive calls $6,300 sold. BidCars identifies Aug28 $6,300 as not sold, Sep4 $6,200 as sold. vin-archive supplies ACV $20,352, while BidCars displays 0/0 ACV/ERC. Zero treated as missing; ACV/event pairing quarantined rather than presumed confirmed.
- F150 1FTEW1CF6GFA07312: web/indexed FinalBid page says reserve met yes; saved direct HTML says no, although sold is also displayed. Different versions/rendering possible. Quarantined pending authoritative event history; a reserve miss alone does not prove no subsequent negotiated sale.
- Camry 4T1BF1FK2GU154892: ACV $11,179 agrees; BidCars final price is missing. FinalBid reports timed sale but its final amount was not extracted in this bounded pass. Trim and damage coding differ. No average bid substituted.
- Camry 4T1BF1FK1GU193991: historical Carfast lead supplies a Retail Value, with unresolved event date. Not silently relabeled insurer ACV.

Seven candidates are not a random sample; neither admission rate nor inconsistency frequency estimates archive-wide quality.

## Sources and acquisition status

Every candidate URL is in candidate_ledger.json. Key cross-check pages:
- https://bid.cars/en/lot/0-45593431/2016-Toyota-Camry-4T4BF1FK4GR557682
- https://bid.cars/en/lot/1-65004706/2016-Ford-F-150-1FTMF1C81GKD57189
- https://bid.cars/en/lot/0-46074809/2016-Toyota-Camry-4T4BF1FK4GR540574
- https://bid.cars/en/lot/0-45888997/2016-Toyota-RAV4-2T3DFREVXGW533908
- https://bid.cars/en/lot/0-45886589/2016-Toyota-Camry-4T1BF1FK2GU154892
Primary attempts: https://www.iaai.com/Search?Keyword=45593431 and https://www.copart.com/lot/65004706. Neither yielded a readable primary sale record.

## Decision and next bounded stage

Field feasibility passes in limited form: recoverable paired amounts exist in secondary sources. Readiness to estimate a body premium does not pass. No class ratio or 1.50 replacement produced.

A next small stage should use a predefined platform/date/model-year frame rather than search terms requiring a visible price, retain all records and missingness, and seek common mileage/damage/run-status strata across body classes. First secure crossover records with paired corroboration; the current pilot has none. Keep completed Buy Now sales as a separate sale channel, not discard them silently or mix them with auction-clearing bids. Keep failed attempts for process analysis, but one completed-event observation per VIN/lot/date for proceeds. Complete all events before classifying a relisting.

Before estimating, verify multiple dates/VINs on source snapshots, distinguish source feed agreement from primary settlement confirmation, and calculate coverage for each stratum. A small pilot can estimate feasibility and rough dispersion; it cannot justify a precise adjusted fleet coefficient. Larger collection or paid source acquisition requires a concrete scope/cost proposal to the user first.

ACV in a disposed-vehicle sample remains selected on insurer total-loss decisions. It can support auction-price decomposition but cannot alone identify pre-accident values across all insured accident exposures or repair-versus-total propensity.

## Reproduction and audit

candidate_ledger.json contains fields, dates, source URLs and dispositions. build_ledger.py computes only admitted descriptive recovery fractions, checks VIN uniqueness and the count of admitted pairs, and writes results.json. sources.json logs direct requests and errors; raw/ contains two complete HTML/text captures, including the reserve-field discrepancy. manifest.json hashes saved artifacts. No commercial workbook or prior assumption was overwritten.
