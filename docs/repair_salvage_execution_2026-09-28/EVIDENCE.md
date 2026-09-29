# Prior work, bounded discovery and field admission

28 September 2026. Eight search queries followed by selective source inspection. No agents, paid access, external outreach, OCR, bulk record collection or Excel edits. Existing source results were reused; sources below that repeat old evidence are labelled accordingly. Website descriptions and commentary are not underlying transaction datasets.

## Prior-work inventory

| Question | Existing work | Established status | Action in this pass |
|---|---|---|---|
| Body repair premium | repair_research_2026-09-26/repair_pilot source map, matched/alternative parts and scope studies | Available but scope/vendor/date sensitive; not a universal premium | Reuse; seek temporal/source-specific price evidence |
| Repair-frequency weights | repair_frequency_feasibility and repair_cost_reference | Crash proxies/historical repairable estimates; wrong population for full latent damage | No repeated frequency extraction |
| Recovery price paired with value | value_recovery_audit and auction_recovery_pilot | Seven candidates, two secondary pairs, no primary settlement validation | Test schema of newly discovered providers before collecting more |
| Age economics and switching sensitivity | AGE_CONSTRAINED_ENGINE and JOINT_REPAIR_VALUE_CALIBRATION | Calibrated historical levels; derivative unvalidated | Freeze historical fit; test dollar offsets only |
| Claims/TLF identification | claims_discovery SEARCH_LEDGER, COUNT_COMPATIBILITY, QUARTERLY_PAIR_SEARCH | Populations fail exact reconciliation; small-claim nonfiling not identified | No new coefficient from aggregate series |
| Price-to-fee mapping | auction_price_test and rpu_downside_test | Conditional arithmetic; schedule/distribution assumptions | Reuse existing engine |
| Current supplier evidence | model/revenue_architecture EVIDENCE_UPDATE | Prior LKQ/Boyd operating commentary, no fixed-scope cost coefficient | Use as background, not call it new discovery |
| Full revenue comparisons | model/revenue_architecture and rpu_composition | Dated named benchmarks; CapIQ acquisition scope unknown | Keep same reference assumptions and explicit perimeters |

## Searches actually executed

1. `site.lkqcorp.com "2026" "salvage" "procurement"`
2. `site.partstrader.com "2026" "price" report collision`
3. `site.cccis.com "total loss" "threshold" "2026"`
4. `"repair to value" "distribution" insurance total loss salvage`
5. `site.iaai.com "2026" "Market Value" "export"`
6. `site.partstrader.com "Spring 2026" report`
7. `site.iaai.com "2026" "salvage" "export" report demand`
8. `"total loss" "repair cost" "distribution" "salvage" insurer report histogram`

Queries7–8 refined two low-yield routes after the initial pass: exporter evidence and a threshold distribution. They still did not produce the required direct measurements. Stop rather than broadening those loops. Trade articles were leads to PartsTrader, not independent confirmation. No legal-threshold table from secondary search results was adopted.

## Source/field ledger

**S1 — New: PartsTrader, February11,2026, [Why Parts Inflation Looks So Uneven](https://www.partstrader.com/why-parts-inflation-looks-so-uneven/), methodology and discussion paragraphs.** Describes a defined basket of high-volume parts for three-year-old high-volume models, rather than a changing monthly vehicle average. Reports OEM/recycled inflation outpacing aftermarket and suggests competition/inventory effects. Useful directional evidence against broad parts-price deflation. Full weights, continuous numerical series, matched older cohorts, and quote/order/payment conventions are not supplied in the inspected article. Commercial provider commentary; causal explanations for FX and inventory are hypotheses, not independently estimated coefficients. Admit source-specific price direction and methodology, not a percentage change in total repair cost.

**S2 — New: PartsTrader, May21,2026, [Technician shortage and parts replacement](https://www.partstrader.com/is-the-autobody-technician-shortage-leading-to-more-parts-replacement/), operational discussion.** Describes skill/cycle-time constraints and materials/equipment making replacement more likely. Adds an alternative explanation: stable unit-part prices can coexist with more replacement operations. No measured repair/replace trend for matched cohorts supplied. Same author/provider as S1, so not independent empirical corroboration. Labor statistics and tariff claims were not separately verified and are not used as inputs.

**S3 — New source, inaccessible contents: [PartsTrader Spring2026 report](https://www.partstrader.com/trends-report/), May1 listing.** Linked public FlowPaper viewer loaded, but web text contained only title. Viewer-configured PDF and one page-data asset returned404; no chart or numeric coefficient admitted. Did not escalate to browser/OCR. The secondary article's 4.3% number is not adopted. Saved viewer HTML and acquisition hash identify the attempted document.

**S4 — Newly inspected operational detail: [LKQ2025 10-K](https://www.sec.gov/Archives/edgar/data/1065696/000106569626000012/lkq-20251231.htm), North America business pp5–6, salvage supply risk and market-risk section.** LKQ describes setting bids using inventory, historical demand and recent selling prices, and competing with rebuilders/exporters. This supports tracing parts demand and competing buyer economics to donor bids, but no matched acquisition-cost time series was located in the reviewed passages. Scrap/precious-metal exposures have different movements and lags; do not apply a scrap index to all salvage. Admit mechanism/schema, not elasticity or a Copart price forecast.

**S5 — Reused: [LKQ Q2 release](https://www.sec.gov/Archives/edgar/data/1065696/000106569626000041/exhibit991.htm), July30,2026, opening commentary.** Previously recorded alternative-parts utilization and repairable-activity improvement remain directional. Do not use utilization above40% as a measured aftermarket unit share for our fixed repair basket: recycled/new/price-matched definitions and denominator differ. No new model input from rereading it.

**S6 — New field audit: [VinAssessment auction schema](https://vinassessment.com/data/auction-data), displayed sample record and dataset description.** Public sample VIN3KPA24AD7PE615699/lot72326955 includes estimated repair cost1626, estimated retail value16875 and observation date2026-01-31; later retail asks are not completed salvage proceeds. Accepted auction price, insurer expected net salvage, payment status, claim decision version and repaired-claim comparison group are absent from that example. Vendor provenance not independently authenticated. One displayed sample inspected, no package/license requested. Reject for recovery calibration and switching-mass measurement; possible future listing-schema lead only.

**S7 — New field audit: [Rebrowser IAA dataset](https://github.com/rebrowser/iaai-dataset), README field table.** Public documentation exposes ready-for-sale status, scheduled auction date, buy-now/minimum-bid and estimated repair fields; several useful fields are marked premium. No accepted final-sale field shown in the inspected table. No rows downloaded, no premium access attempted. Reject at schema stage: additional listing rows would not supply realized proceeds or rejected repair claims. Do not call advertised completeness percentages independent quality checks.

**S8 — Reused, still unavailable: [CCC Salvage TVR job aid](https://help.cccis.com/training/insurance_company/estimating/orientation/JobAids/CCC_ONE_SALVAGE_TVR.pdf).** Prior indexed anticipated-salvage/supplement lead; this pass's one check returned403. No repeated retries or extraction. Workflow capability is not access to claims observations. No threshold histogram obtained.

**S9 — Reused: [CCC Q2 2025 report](https://www.cccis.com/reports/crash-course-2025/q2), TCOR discussion.** Search surfaced the already-known distinction between reported repair averages, total-loss selection and age mix. It does not supply a joint C/V/S distribution. No new extraction/calibration.

## Access and feasibility decisions

PartsTrader/VinAssessment content was readable through the web tool; separate direct-HTTP snapshot attempts returned403 and were not retried. Native requests library was unavailable, so the public viewer was retrieved with standard-library HTTP; its PDF and one explicitly configured page-data path returned404. Raw acquisition.jsonl contains successful byte-level snapshots only; this paragraph and access_attempts.csv preserve failures.

The feasibility gate stopped before the proposed10–20 record collection. Two new provider schemas and one displayed sample lacked essential fields. More records from those schemas would not cure the problem. No publicly usable fixed-cohort temporal repair panel or paired claims-threshold table emerged. This is a bounded negative finding, not proof such data do not exist.

Export, public-fleet, regulatory and specialist routes were considered from the prior source map. The export query did not yield a usable direct series; no specific public-fleet/specialist lead warranted further collection in this pass. No claim is made to have exhaustively searched every family. All new admission decisions are directional/schema-level; zero new empirical forecast coefficients were adopted.
