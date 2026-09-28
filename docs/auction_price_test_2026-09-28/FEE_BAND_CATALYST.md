# Candidate catalyst: auction prices crossing buyer-fee thresholds

28 September 2026. Explicitly requested by the user as a pitch candidate, conditional on modeling/evidence. Status: plausible mechanism; aggregate concentration and dated catalyst not established. It may be bullish when prices cross upward or bearish when expected crossings fail / reverse. No direction is selected to suit the pitch.

## Candidate pitch

Copart earns a staircase of buyer fees rather than a constant percentage of vehicle value. If a material pool of auction sales moves across particular fee thresholds, fee revenue can change disproportionately to the movement in average vehicle prices. The differentiated forecast would identify which vehicles sit near which thresholds, why their prices should move during our investment horizon, and how many incremental fee dollars those crossings generate versus analyst expectations.

Distinguish crossing an unchanged fee band from Copart raising the fee schedule. These are different mechanisms. A posted staircase alone is not a catalyst: a catalyst requires a dated price/mix driver, a population of affected sales and a material deviation from expectations. Falling fee yield as price rises is not declining fee dollars.

## Cheap experiment completed

`catalyst_test.py` uses the existing fee grids and exact distribution arithmetic. Reference assumptions: non-clean standard vehicles, secured payment, half standard/half preferred buyers, lognormal median $3,500 and log sigma0.8. Seller fee4% and fixed services$55 remain illustrative. The resulting $1,083.39 reference RPU differs from the fleet-engine RPU because the assumed distribution differs; neither is a measured realized level.

For each threshold t and proportional price increase g, crossing mass is Pr[t/(1+g) <= old price < t]. Multiply by the buyer-fee jump at t to obtain its mean-fee contribution. Percentage-fee slopes above thresholds are recorded separately as the continuous contribution. No random simulation or listing collection.

| Uniform price increase | Mean buyer-fee increase | Buyer-fee growth |
|---|---:|---:|
| 1% | $3.32 | 0.397% |
| 3% | $9.90 | 1.185% |
| 5% | $16.41 | 1.964% |

These are smooth aggregate responses despite transaction-level steps. For a 3% increase, the largest reference contribution is the $3,500 threshold: assumed crossing mass1.474% × $50 jump = $0.737 per sale across the entire population. A 3% uniform price rise crosses that threshold only for old sale prices around $3,398–$3,500. This interval is a model calculation, not observed sales concentration. Other large contributions occur at $3,000, $4,000, $2,500 and $6,000. Full results in threshold_crossings.csv.

To obtain a 1% increase in the illustrative $1,083.39 RPU solely from a $50 fee jump at one threshold, approximately 21.7% of sales would have to cross it. That is much higher than the reference distribution's1.47% crossing that threshold under a3% price change. This stress arithmetic isolates one threshold; many thresholds can contribute together, and seller fees also respond. It is not a universal hurdle or a forecast.

## Important prototype issue found

The existing damage engine places each age/body/severity group at a single representative auction price. When a price change moves that representative price across a fee boundary, the entire group's weight jumps at once. That may manufacture an apparent catalyst if real transactions are dispersed.

Read the216 existing FY26Q4 price/weight states and held their weights fixed. Tested the same price shock with no within-state dispersion and then a uniform price range around each state. The range is a numerical robustness assumption, not new evidence about actual dispersion.

For a5% price increase, buyer-fee growth was:

| Within-state price spread | Buyer-fee growth |
|---|---:|
| Single representative price | 2.703% |
| Uniform +/-2.5% | 2.276% |
| Uniform +/-5% | 1.935% |
| Uniform +/-10% | 1.907% |

At a3% price increase the corresponding responses are much closer:1.169%,1.258%,1.139%,1.149%. Hence the issue is local threshold sensitivity, not evidence that the entire model is unusable. Do not choose dispersion to create or suppress the desired thesis.

## Implementation decision

Keep the real fee steps. For the next engine revision, integrate buyer fees over within-cohort prices rather than charge every vehicle the fee at one representative price. Keep dispersed and discrete results as a numerical robustness comparison until empirical dispersion is available. A handful of exact band integrals is computationally cheap. Do not change total-loss unit weights while testing pure price pass-through; joint selection is a separate test.

No Excel engine changes were made in this pass. The smoothed test is not adopted as an empirically calibrated replacement distribution. Its role is to show which prior precision was artificial.

## Evidence required to promote the catalyst

1. Sold-vehicle clearing prices near the relevant bands, with date, sale result, title, buyer-fee eligibility where observable and duplicate handling. Current bids, reserve prices and unsold relists are not realized auction prices.
2. A reason those specific prices should cross during the next one or two quarters: a supported market-price forecast, known mix shift, or a dated schedule change. An average ASP growth assumption alone does not locate concentration.
3. A held-out period / stable subgroup check showing concentrations are persistent rather than artifacts of bid increments or a sample definition. Posted fees can themselves influence bids; fixed prices under fee changes are not an equilibrium model.
4. Multiply incremental fee dollars by compatible affected sold units and compare with consensus's existing RPU assumptions. Never multiply an insurance-only effect by every global unit.

First inspect the schema/coverage of existing repository sale records without bulk collection. If they contain only live bids or listing inventory, do not launch a large scrape. Ask for a small targeted provider/AlphaSense export if available; any expensive collection still needs user approval and an end-to-end proposal. No provider access is assumed.

## Provenance and verification

Fee inputs and source hashes are recorded by run.py. catalyst_results.json stores assumptions, per-threshold stress calculations and node tests. Existing workbook read only; no licensed reports copied. The exact expectation test from run.py still passes. Within-state averaging integrates each linear fee segment exactly. Original prototype and forecast remain unchanged. Findings are about fee arithmetic and numerical robustness, not verified market timing or investment advice.
