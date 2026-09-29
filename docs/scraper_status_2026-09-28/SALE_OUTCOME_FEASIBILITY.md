# Sale-outcome feasibility — 2026-09-28

## Decision
Public event histories exist and can join to our lot IDs. This pilot does NOT pass a reliable price-panel gate: zero newly corroborated numerical sale prices from three preselected local lots; zero primary settlement records. Two lots have secondary sold-event records, one has conflicting prices, one price is hidden on the corroborating source, one was not found. No monthly ASP estimate, buyer-type conclusion, model change or collection expansion.

## Frame and prior work
Reused auction_recovery_pilot/README.md and candidate_ledger.json, plus repair_salvage_execution EVIDENCE provider failures. Earlier seven-VIN study already established isolated secondary outcomes; this follow-up tests joining independently selected local records, not rediscovering those as new.
Read-only SQLite selection: earliest snapshot, year=2016, make_model prefix toyota-camry or toyota-rav4, ordered lot_id ascending, LIMIT3. Selected 45798066,47794676,49409146, all Camrys. Deterministic convenience sample, not random; inventory/low-ID selection favors persistent listings. No inference about population coverage from n=3.

## Record ledger (web text observed; no settlement proof)
- 45798066, 2016 Camry SE, Denver South, clean-title in local metadata. Exact-lot search returned no relevant outcome. Primary https://www.copart.com/lot/45798066/clean-title-2016-toyota-camry-se-co-denver-south returned internal error via web tool. Missing outcome, not unsold or zero price.
- 47794676, VIN4T1BF1FK5GU161657, 2016 Camry SE, Fairburn. Cararam reports sold September14,2026 $950, reserve met yes. BidCars agrees VIN/lot/date/sold status but hides final bid (******/Hidden); history seller classified Insurance company while header seller No information. Thus status/date corroborated, $950 SINGLE-SOURCE only. ACV and repair fields not needed for price feasibility; don't substitute page's Avg final bid or calculator defaults for actual amount.
  https://cararam.com/en/toyota/camry/2016/copart-47794676-4T1BF1FK5GU161657
  https://bid.cars/en/lot/1-47794676/2016-Toyota-Camry-4T1BF1FK5GU161657
- 49409146, VIN4T1BF1FK8GU528826, local/BidCars XSE vs FinalBid SE. BidCars reports sold September18,2026 $2750, noninsurance seller. FinalBid same event $3200, Sold, reserve met No. $450 discrepancy (16.36% of2750); no reason established (could be different stages/negotiation, error, update or field interpretation). Quarantine; do not average or choose preferred source. Copart original page returned internal error; no primary adjudication.
  https://bid.cars/en/lot/1-49409146/2016-Toyota-Camry-4T1BF1FK8GU528826
  https://finalbid.vin/en/toyota/camry/2016/copart-49409146-4T1BF1FK8GU528826
  https://www.copart.com/lot/49409146/salvage-2016-toyota-camry-xse-ga-atlanta-west
  BidCars earlier attempts: Aug28 $2200 not sold; Sep1 $2200 not sold; Sep4 $1500 not sold; Sep11 $2600 not sold; Sep15 $2600 not sold. FinalBid lists Sep2/Sep16 instead of Sep1/Sep15 for two attempts and describes approval status. Date mismatch unresolved; possibly convention, not proven. Repeated bids are not multiple realized sales or a market time series.

Positive control reused, not counted among new3: https://bid.cars/en/lot/1-65004706/2016-Ford-F-150-1FTMF1C81GKD57189 still displays Sep17,2026 $3550 Sold Insurance company, agreeing with prior ledger. Existing secondary corroboration retained; no new primary confirmation.

## Search and access
Five queries: Copart sold auction history final bid September 2026 Toyota Camry bid.cars; Copart auction historical data API sold not sold final bid date bidfax stat.vin; Copart "45798066"; Copart "47794676"; Copart "49409146". Followed strongest exact-ID pages above. Other broad archive claims not proof. Two primary attempts failed once each; no retries/bypass/account/paid report, OCR, images or bulk download. Web observations transcribed here, not raw HTML snapshots. Site clocks/related future listings not used to redefine sample dates.

## What is feasible next, and stopping rule
Schema/linkage pass in limited form; accepted-price verification and unbiased coverage fail. Auction-archive Sold is a secondary report of an outcome, not proof of paid settlement or insurer net proceeds. Providers may share underlying feeds; agreement alone is not independent validation. Need documented field semantics and a small primary invoice/result comparison before large historical backfill. An invoice/authorized broker export could resolve high bid vs accepted negotiated price; no such access established. Do not buy reports or contact providers without authorization.

A later pilot could separate reported-sold/date coverage from price availability, explicitly retain conflict/hidden/missing records and stratify insurance vs noninsurance. Only after quality clears should we propose a bounded fixed-date/model/damage panel for price change. More scraped pages alone cannot fix price definitions; pause scale-up here. No automatic changes to nightly scraper.
