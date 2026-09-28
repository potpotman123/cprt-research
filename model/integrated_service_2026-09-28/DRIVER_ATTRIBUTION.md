# What currently drives the forecast, after the historical repair

Bounded local check, September 28, 2026. Existing inputs only; no new source acquisition, fitted assumptions, Excel work or scenario search. Run `driver_attribution.py` using the model's Python runtime. Outputs: `driver_attribution.csv` and `driver_attribution.json`.

## Finding

The present default is principally an inherited carrier-allocation scenario, not a quantified fleet-selection or service-adoption thesis. This was true qualitatively before the baseline repair; the revised same-quarter bridge now makes the dollar attribution explicit.

FY27 H1 means quarters ending October 2026 and January 2027. Prior-year legacy service revenue is $1,943.896m. The provisional output is $1,845.563m, a $98.333m decline, approximately 5.06%. This is not a consensus gap or adopted investment forecast.

| Sequential bridge from prior-year service revenue | Change, USD m |
|---|---:|
| Fleet exposure proxy and assumed claim frequency | +3.241 |
| Cohort-weighted total-loss frequency | −0.521 |
| Modeled insurance RPU | −1.084 |
| Prior-year capture versus FY26Q4 capture | −91.173 |
| Further capture change after FY26Q4 | −8.795 |
| Other US / international, current flat drivers | 0.000 |
| Total | −98.333 |

Effects are applied in the displayed order. Interaction attribution depends on that order; this is exact mechanical reconciliation, not empirical causal attribution. The RPU line includes modeled mixture effects and constant ancillary assumptions; it is not pure core-auction pricing evidence.

## Why a year-over-year decline is not necessarily a new customer loss

The comparison-quarter capture proxy exceeds the modeled FY26Q4 endpoint. Even if capture stops falling after Q4, early FY27 quarters still compare with higher assumed capture a year earlier. We separate:

`forecast capture / prior-year capture = (FY26Q4 capture / prior-year capture) × (forecast capture / FY26Q4 capture)`.

The first term is the inherited comparison effect. It includes changes in the historical carrier mix and allocations, not only Progressive. The second term reflects the simplified forward scenario: fixed Q4 carrier weights and other allocations, with only Progressive changing further.

In the inherited input snapshot, Progressive's modeled allocation to Copart is 25% in FY26Q1/Q2, about 15.91% in Q3, 6.82% in Q4, and 5% in FY27. These are source-model assumptions, not newly verified customer allocations. The forward 5% assumption is then constant, so it would be wrong to describe the model as forecasting fresh Progressive deterioration in every quarter.

Historical capture was not independently established by the previous unit reconciliation. The earlier carrier audit found mismatched claims populations and a Q4 path calibrated to the observed print. These limitations remain; this arithmetic does not fix them.

## Comparison views now available

| FY27 H1 view | Legacy service revenue, USD m | Interpretation |
|---|---:|---|
| Current inherited forward path | 1,845.563 | Existing provisional output; unchanged |
| Freeze capture at FY26Q4 | 1,854.358 | Remove only further assumed capture losses; prior-year comparison remains |
| Capture unchanged versus matching prior-year quarter | 1,945.531 | Diagnostic isolation of non-capture modeled changes |

The last case is not a recommended share forecast. It assumes away the carrier comparison to expose what the other model components currently contribute. Neither comparison is a statistical confidence bound. The aggregate capture proxy assumes common cohort economics across carriers, so these cases do not capture carrier-specific ASP/RPU shifts.

## Consequence for architecture and research ownership

Keep the current capture path explicit rather than quietly replacing it with a favorable case. The historical allocation uncertainty belongs in the baseline assumptions, not in the claimed evidence for the differentiated theses. Maintain this attribution view alongside the revenue summary.

The teammate's ancillary research will replace or constrain adoption and fee inputs. Our main-model work should next establish the actual cohort changes entering the fleet engine: age mix, body mix and covered-claim exposure, with historical observations separated from flat future birth assumptions. Then compare the selected sold population and fees on the same exposure base. A default run with flat repair/value/adoption drivers is not a forecast that those forces are economically absent.

Do not extrapolate the roughly +$1.635m non-capture H1 contribution into a claim that the fleet thesis is immaterial. It is conditional on existing cohort paths, fixed body economic relationships, flat claim-frequency drivers and no new ancillary-adoption forecast. Conversely, do not use the approximately $100m capture drag as evidence that the fleet/adoption theses are material. Those mechanisms have separate ownership and must retain separate attribution.

## Verification

Twelve assertions verify four quarterly dollar reconciliations, capture-ratio factorization, and insurance branch reconstruction. The calculation reads but does not modify production assumptions, historical controls, economics, or forecast CSVs. Recomputing the capture comparisons is cheap; no broad sensitivity grid was run. This test establishes what the current model assumes, not what will happen.
