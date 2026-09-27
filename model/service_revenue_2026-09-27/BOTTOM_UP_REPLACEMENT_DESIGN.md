# Replace the revenue-growth baseline with operating drivers

27 September 2026. User requests that 100% of projected service revenue arise from explicit operating drivers, with damage selection integrated into the model. This document supersedes the mechanical US/international service-growth carry-forward as the intended forecast architecture. It does not assert the replacement is already implemented or fully populated. Preserve the approved four main reading tabs and allow Fable to handle visual design.

## 1. Existing identity and its limits

MODEL_BLUEPRINT.md section 4 and HANDOFF.md section E use insurance units = claims × total-loss rate × Copart share. The product of the three growth factors is exact only for consistently defined populations and periods, constant routing/conversion assumptions and matched unit events. Assignments and completed sales are different events. Historical share solved as the residual also absorbs errors in claims, TLF, timing and scope; it is not independent proof of competitive share.

Use unique claim vehicles with a consistent loss/coverage denominator. Collision, comprehensive, theft and catastrophe populations must not overlap. Accident counts alone omit some insurable loss sources and are not equivalent to filed claims. Never multiply claims by another accident or filing factor already included in their definition.

## 2. Insurance operating chain

For geography, carrier or carrier group, vehicle age/body cohort, loss type and quarter:

1. **Claim vehicles:** compatible insured exposure × claim frequency. Fleet exposure, mileage, coverage and filing behavior can explain frequency, but must not be multiplied again if the measured frequency already incorporates them. The existing fitted age-claim weights are relative allocation weights, not absolute claim probabilities. If total market claims are the anchor, normalize the cohort weights to that total.
2. **Total-loss vehicles:** claim vehicles × probability of totaling conditional on the cohort and loss type.
3. **Copart assignments:** total losses × eligible auction-routing fraction × Copart allocation among that eligible population. Owner retention and non-auction dispositions must be explicit or documented as embedded in the chosen allocation definition, never counted twice.
4. **Completed units:** opening inventory + assignments - ending inventory - returns/withdrawals/other non-sale exits. Use an assignment-to-sale lag distribution, including pre-forecast assignments, when supported; do not equate every assignment to a sale in the same quarter. Inventory is a conservation check, not a second volume addition.
5. **Revenue:** completed units × expected seller and buyer transaction fees, plus separately modeled services recognized on other events if required by the company's accounting and source definitions. Map transportation, storage and other charges to their proper activity and recognition basis; do not add them again when already included in an all-in RPU anchor.

Carrier growth changes market claim weights. Carrier allocation changes Copart's fraction of those losses. Model contract wins/losses as allocation paths, not additive units on top of a share path already including them. Derive aggregate share after summing the carrier groups. A lapped loss removes a comparison drag; it does not restore lost assignments.

## 3. Joint damage selection and fees

For each cohort, use a finite set of explicit damage states with claim probabilities. Each state has complete repair cost, pre-loss value and salvage proceeds. Apply an economic totaling rule repair cost > pre-loss value - seller net salvage, with a documented override for statutory/operational rules where evidence supports it. The rule is an approximation, not a universal description of insurer decisions.

Compute BOTH total-loss probability and expected service fees from the same selected states. Auction fees are conditional on totaling, routing to Copart and sale. Model any residual price dispersion consistently with the existing bid-node convention; distinguish it from damage-related salvage dispersion to avoid double counting. Within a sold-unit construction:

`insurance transaction revenue = sum(claim vehicles × damage-state probability × total-loss decision × routing × allocation × sale-timing weight × transaction fees)`.

The earlier toy recovery slope is a scenario assumption, not a measured coefficient. Baseline calibration is frozen before forecasting new repair/value/recovery changes; do not refit a forecast shock back to the historical TLF target. Unobserved severity costs and frequencies remain labeled assumptions.

## 4. Cover the complete service revenue perimeter

Use mutually exclusive rows for US insurance, US non-insurance, international insurance and international non-insurance, refined only where data support the split. Non-insurance streams need their own supply/consignment, allocation/conversion and fee drivers; insurer TLF must not be applied to dealer or fleet consignments. International builds require their own loss/supply, unit and local-currency fee drivers plus FX. Do not import US fee schedules or age relationships without an explicit transfer assumption.

Country and seller-category detail can begin with coarse groups. All groups still require quantities and fees rather than a total service-growth input. Purchased-vehicle sales are outside this deliverable. Geography, channel, purchase/consignment and acquisition perimeter must reconcile without overlap. Any acquisition contribution requires a separate dated scope decision; do not silently include it.

## 5. Historical anchor and identifiability

The repository does not establish independently observed absolute claim, company-unit and realized-fee levels for every required slice. Multiplying modeled shares and fees does not resolve that gap. One reported revenue observation cannot identify both unknown unit levels and unknown RPU or multiple category revenue weights.

Create an input register with disclosed, independently estimated, fitted and assumed status. Prefer compatible observed units/fees where available. Where absolute levels are unavailable, a historical quantity normalization or segment revenue anchor may be estimated and disclosed, constrained by additional evidence. Freeze it before the forecast. A base-period dollar anchor is not an assumed future revenue growth rate, but it is not a claim to have independently measured every level either.

Historical actuals tie to an explicit reconciliation schedule. Do not force all historical quarters to fit using changing calibration plugs. An unexplained residual remains visible and blocks a claim that the model has fully explained 100% of reported services. Before finalizing, either identify its economic source and project it through activity/fees or clearly retain it as an unmodeled limitation. Never hide it in RPU drift or other-services growth.

## 6. Preserve presentation, change computational ownership

- **RPM Summary:** quarterly service dollars by geography/channel, historical reconciliation and forecast totals. No top-level growth input.
- **Volume Build:** claims, TLF, eligible losses, allocation, assignments and completed sales; separate non-insurance volume drivers.
- **Vehicle Economics:** damage selection, values, recovery, conditional fee distributions, seller terms and buyer fee schedules.
- **Revenue Bridge:** units × fees by revenue stream, other service activity × price where applicable, local currency/FX, total reported-service reconciliation and driver attribution.

Supporting calculation/data tabs own detailed cohorts, carrier groups, damage states, calibration and source records. Do not remove the existing model until the replacement reconciles; keep it as an explicitly superseded comparison, not a forecast input.

## 7. Bounded implementation sequence

1. Inventory existing repo inputs for reported service dollars, unit indicators, carrier allocation, fee schedules, lag evidence and non-insurance/international composition. No new bulk collection. Produce a coverage/missing-data map before estimating levels.
2. Reconcile historical geography/channel definitions and select a defensible base-period anchor, documenting what is identified versus assumed. Avoid optimizing a target share price or a desired short result.
3. Implement the claims → damage selection → routing/allocation → sold units → fees engine for US insurance. Use explicit scenario inputs for missing evidence and compare with the validated legacy mechanics.
4. Add remaining service streams and historical reconciliation, then remove service-growth carry-forward inputs. Retain a visible unresolved bridge if evidence is incomplete; do not claim 100% attribution prematurely.
5. Test conservation of units, category sums, fee inclusions, same-population TLF denominators, no double-counting carrier effects, FX/perimeter and forecast input propagation. Backtest an earlier-to-later period without using later information in baseline calibration.

All forecasts should respond directly to operating inputs. Consensus is an external comparison for identifying a variant view, never the mechanism that generates our forecast. Large scraping/OCR/paid-data work requires the user's separate cost-and-method approval.
