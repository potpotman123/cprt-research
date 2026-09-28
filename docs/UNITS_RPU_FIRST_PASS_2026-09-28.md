# First pass: customer activities and revenue perimeter

Read-only source investigation plus this note, 2026-09-28. No new collection, simulation, or workbook changes. Scope remains 100% of service revenue, not purchased-vehicle sales or EPS. Mechanisms will be tested independently, not forced to agree.

## Accounting finding

Source: local raw/sec/10k/cprt_2025-07-31.htm, Revenue Recognition / Service revenues. Parsed locally with Python standard-library HTMLParser; no OCR. This is FY2025 accounting evidence, not verification of any subsequent change or new product contract.

The filing describes auction-related transportation, title, storage, bidding and loading services as not distinct within the contract and recognized with the auction performance obligation. Annual registration access has a separate performance obligation. Consequently operational service uptake can be modeled separately but cannot automatically be recognized when the activity occurs. A title completed in one quarter does not automatically create revenue in that quarter under these disclosed arrangements. Auction-related fees already in all-in RPU cannot be added again as ancillary revenue. New delivery offerings or standalone services require confirmation of their specific accounting before extending the historical policy.

This is a correction in specificity to the research plan: identify service activity first, then map its recognition to the applicable contract; separate activity drivers do not imply separate performance obligations.

## Revenue architecture

1. Forecast insurance claims by carrier and cohort; select economic total losses; apply routing and auction allocation.
2. Forecast assignments and completed auction units with inventory/lag reconciliation.
3. Forecast buyer/seller fees and attached service use for those auctions. Recognize covered bundled services with the auction under the verified historical policy.
4. Add separately recognized services/access only where evidence supports a separate obligation, avoiding overlapping all-in RPU anchors.
5. Repeat with appropriate supply drivers for US non-insurance and international service business; insurance total-loss rules do not apply to all channels.
6. Reconcile all service revenue. Keep purchased vehicles outside scope. Do not assert both absolute units and absolute fees are independently measured merely because their product matches disclosed revenue.

## Evidence and rival explanations

Service track: existing transcripts identify account rollout and service adoption as contributors, but not quantitative saturation. Faster title processing can also accelerate sales. A shift of sales between quarters is not a permanent new supply source. Long-haul operating cost increases do not alone establish service revenue or its margin.

Fleet track: the existing diagnostic README (docs/model_tests_2026-09-27/README.md) reports H1 age composition -$0.885m and conditional body composition +$0.082m versus the legacy mechanical growth baseline. These are not adopted forecasts; they warn that a negative per-claim vehicle comparison is not automatically a negative or material next-two-quarter growth contribution. Re-estimating an old ACV ratio cannot be treated as a sudden future value shock.

## Immediate next bounded checks

- Build period/population-matched US service revenue and fee-unit growth reconciliation; do not use international RPU disclosures as US figures.
- Map Title Express adoption evidence to account cohorts and eligible volumes, leaving fees and remaining opportunity unidentified where not disclosed.
- Use existing deterministic calculations to screen crossover break-even economics before collecting a larger valuation sample.
- Maintain separate contributions for supply, allocation, fee economics, service use and timing, with interactions explicit. If tracks conflict, report the net result and confidence rather than selecting assumptions to force alignment.

Limitation: this pass adds an accounting constraint and audits existing numerical conclusions; it does not yet deliver a new empirical quarterly forecast or prove either investment direction.
