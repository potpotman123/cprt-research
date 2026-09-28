# Architecture and evidence audit — 28 September 2026

## Decision

The current model is a connected, historically anchored research prototype, not a completed absolute bottom-up forecast. Maintain existing outputs as provisional; do not promote the carrier-driven consensus gap into demonstrated alpha. No operating assumptions changed in this audit. New `consensus_hurdle.py` / `consensus_hurdles.csv` provide a separate conditional benchmark, not an extra growth plug in the engine.

## Where the chain works and where it breaks

| Stage | Current implementation | Missing identification / consequence | Smallest useful next step |
|---|---|---|---|
| Consensus scope | CapIQ total revenue, eight FY27 contributors | Service split and ACV acquisition inclusion unknown | Map dated contributor models where available; keep acquisition and purchased-sales bridges explicit |
| Exposure by age/body | Historical sales, production-share proxy, fitted survival | Births are not registrations; SUVs pooled; future mix held flat | Retain detail but do not claim measured crossover composition; identify observed fleet controls before adding cohorts |
| Claims | Cohort mass times calibrated claiming propensity | Absolute insured exposure and frequency not independently observed; combined coverage/driving effect | Separate observed counts from frequency, matching coverage and periods; do not multiply a second coverage adjustment into the fitted composite |
| Total-loss selection | Repair/value distributions, threshold, salvage recovery | Near-threshold density assumed; aggregate TLF fit does not validate marginal elasticity | Keep repair/value responses as scenarios until independent evidence constrains selection; no new large fitting exercise |
| Copart allocation | Inherited historical path, Progressive-only future runoff | Quote-derived scenario; calibration to historical print not independent validation | Use common allocation across thesis comparisons and report runoff separately |
| Sale timing | Sale-equivalent convention, annual interpolation | No physical assignment-to-sale inventory engine | Preserve convention; do not apply another lag to the inherited allocation; use observed timing only if available |
| Core RPU | Selected ASP distribution through fee brackets, seller percentage, buyer-mix assumptions | Historical fee vintages, payer/fee mix and value changes not measured sufficiently | Match observed ASP and fee-RPU periods, then isolate what schedule arithmetic can and cannot explain |
| Ancillary RPU | Assumed adoption times fee, attached to sale | Adoption/realized fee/gross-net/timing unavailable; flat forward multipliers | Record historical unexplained RPU as unallocated, never label it adoption automatically; pursue quantified disclosures narrowly |
| Other US/international | Historical dollar anchors, flat activity/fee factors | Flat is not an evidence-based forecast | Explicit separate branch scenarios; avoid forcing all consensus growth into US insurance |
| Dollar scale | 90% US service insurance split plus reported quarterly anchors | No independently measured insurance units/RPU levels; raw Q2 reconstruction misses by $99.5m | Preserve failed reconstruction; identify level anchors or explicitly accept a relative-index model |

## Required architecture distinction

1. Observations: actual quarterly service dollars, compatible unit/RPU growth disclosures, fleet inputs, dated fee schedules, and consensus totals. Every metric retains its own population.
2. Operating hypotheses: explicit changes in cohort activity, selection, values, fees and service adoption. Unidentified coefficients remain assumptions. Carrier scenario is separately selectable.
3. Forecast: insurance units × insurance RPU, plus other US service and international service. Purchased sales and ACV acquisition are separate scope bridges. Physical service-event timing may differ from auction-sale timing; an average per-sale allocation is not proof of recognition timing.
4. Benchmark: consensus total minus explicit non-insurance/purchased/acquired components produces a conditional insurance revenue target. It does not reveal unique Street unit or RPU assumptions.
5. Attribution: compare hypothesis on/off under identical remaining assumptions, then compare the complete forecast with consensus. Sequential waterfall effects are order-dependent; do not sum individually shocked deltas when interactions are present. Revenue divergence alone is not stock alpha.

Absolute units are not mathematically necessary to forecast growth from a reliable historical revenue anchor and independently supported unit/RPU ratios. They are necessary if claiming an independently reconstructed absolute units × fee build. The present engine has not achieved the latter; preserve the user's original goal and disclose this distinction rather than calling calibration completion.

## Bounded diagnostic completed

The hurdle calculation holds purchased-vehicle sales flat, conditionally treats CapIQ as excluding ACV Auctions, and varies US-insurance share of US service (80/90/100%), other-service growth (0/5%), and insurance-unit growth (-5/0/+5%). These are illustrative cases, not estimated confidence bounds. Q1, Q2 and H1 identities all reproduce their revenue targets (54 checks). H1 uses a uniform unit-growth and RPU-growth assumption over the two quarters; it is not a measured aggregate unit count.

Central convention: 90% insurance fraction and flat other branches. To reach CapIQ H1 $2,350.03m, insurance revenue must grow 4.8641%. Required insurance RPU growth is 10.3832% with units -5%; 4.8641% with units flat; -0.1295% with units +5%. These are requirements under assumptions, not inferred consensus views. Every 1 percentage point of insurance RPU growth at flat units changes H1 revenue by $15.075m under this scale convention. The equation is RPU factor = (consensus - purchased sales - other service) / (prior insurance service × assumed unit factor).

Sources: `../linked_service_revenue_2026-09-28/inputs.json` actuals; `../../docs/consensus_review_2026-09-28/total_revenue_consensus.csv`; `assumptions.json`, `engine.py`, `history_repair.py`, `CONNECTED_ARCHITECTURE.md`, and `../../docs/carrier_test_2026-09-28/README.md`. No new external evidence collected; no probability claims or operating forecasts adopted.

## Next work in priority order

First reuse the historical operating bridge and RPU evidence to build a matched-period table: service growth, compatible fee-unit growth, derived fee RPU, insurance ASP where separately disclosed, schedule vintage, ancillary disclosures, and unallocated residual. All-US fee RPU cannot validate insurance-only RPU without a mix bridge. This inexpensive inventory can reveal whether the supposed RPU thesis is an actual measured deceleration or simply a flat default.

Second reconcile the consensus perimeter and establish explicit scenarios for other service branches. Third add only evidence-supported quarter-specific changes to the RPU and claims engines, leaving unavailable inputs visible. Assess the joint units/RPU gap against the conditional hurdle and under alternative carrier scenarios. Do not pick repair sensitivities or allocation assumptions to manufacture a target downside. Stop before bulk listings/OCR or extensive fitting and seek approval with a concrete information-gain case.
