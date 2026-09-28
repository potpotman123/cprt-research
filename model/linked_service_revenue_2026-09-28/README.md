# Linked service-revenue model: first working research version

**Current completion status:** see [architecture audit](../../docs/ARCHITECTURE_COMPLETION_AUDIT_2026-09-28.md). This remains the original prototype; the newer age-constrained repair engine and proposed simplified carrier path are separate components. Complete integration and revenue-perimeter checks before thesis-delta tests. The implementation/default descriptions below describe this prototype, not adopted forecasts.

Created 28 September 2026. User authorized data sourcing and implementation, retaining approval for expensive collection and analysis. Work here uses local source records and a small deterministic engine; no listing scrape, OCR, paid acquisition, or provider outreach. Browser connection to CapIQ found an expired session; user prefers attaching exports. No CapIQ estimates were obtained or inserted.

## Deliverable and scope

Workbook: `outputs/cprt-linked-20260928/CPRT_Linked_Service_Revenue.xlsx` in the repository. Four main tabs: RPM Summary, Volume Build, Vehicle Economics, Revenue Bridge. Supporting engines and source tabs follow them. The prior approved workbook is preserved unchanged.

Eight fiscal quarters, FY26Q1–FY27Q4. FY26 service dollars are reported; operating history is a modeled reconstruction. Forecast quarters are a conditional working case, not adopted estimates. Purchased-vehicle sales, acquisitions, EPS and valuation are excluded. Missing comparable consensus is displayed as unavailable.

## What is actually implemented

- Age/body fleet roll: 184 age/body rows with legacy birth and survival inputs, weighted into 24 age/body cohorts per quarter. Future births hold CY2025 levels. Light-truck subtype split uses a listed-pool proxy and is held constant across vintages; this is not a measured crossover birth-cohort history.
- Joint damage selection: nine severity intervals per cohort, 1,728 cohort/quarter/severity rows. Total-loss probabilities and selected salvage values use the same states. CCC CY2025 bucket targets set latent log-repair medians once. Gross recovery falls with severity by assumption. Calibration is not validation of the latent distribution.
- Carrier allocation: ten carriers, eight quarters, taken from the friend's Base engine. No additional Progressive haircut. Claim weights initially use its auto-share proxies with neutral relative-claim factors. All carriers initially share the same age/body economics; carrier-specific seller rates influence weighted fees, with aggregate seller economics used for the totaling decision as an approximation.
- Core RPU: selected auction prices passed through standard/preferred posted fee schedules, plus seller-rate assumptions. No blanket RPU-growth intercept.
- Services: title and delivery usage times their prices, separate from core RPU. Their inputs are illustrative because management does not disclose the needed decomposition. No adoption slowdown is imposed.
- Units: claims to total losses to eligible auctions to allocation, then opening inventory/assignments/completed sales/closing inventory. Neutral 100% quarter conversion prevents a second assumed lag on an allocation ramp that may already describe sales. Changing timing away from neutral still applies current-period economics to the sold mix; vintage-specific inventory fees remain a limitation.
- Revenue: modeled insurance units times RPU, plus other-US and international activity-times-fee schedules. These latter branches are deliberately coarse, with flat activity and fee defaults. Their activity equivalents are not actual auction-unit measurements.
- Exact unit/RPU/interaction attribution of insurance revenue changes relative to FY26Q4.

## What must not be claimed

This workbook eliminates the old total-service-growth input from the forecast mechanics, but does not empirically identify every operating driver. The coarse activity assumptions for other US and international services are still assumptions, not a developed thesis.

The single FY26Q4 normalization matches an assumed 90% US insurance share of reported US service revenue. The other 10% is a residual starting perimeter. Service prices of $50/title, $300/delivery and adoption of 50%/10% are illustrative, not sourced estimates. Changing these baseline assumptions changes the inferred unit scale. Reported revenue cannot identify absolute units and absolute fees simultaneously. International $750 and other-US $500 activity-equivalent fees only define a transparent scale; they are not measured realized RPUs.

The 1.128 SUV and 1.493 pickup value ratios are from the small older-vehicle retail proxy check, not matched insurer ACV. Van ratio 1.00 is assumed. These differ from the unvalidated legacy uniform 1.50 light-truck ratio. A correction to a longstanding value estimate is not a forecast-period catalyst.

The reconstruction misses earlier FY26 US quarters by approximately +$10.2m, +$44.0m and -$56.1m. The base quarter ties by construction. Historical fee schedules, claims changes, seasonality, catastrophe composition and service adoption remain unresolved. This is not a passing historical backtest, and the current FY27 totals must not be presented as an investment forecast.

## Source discipline and next data

`evidence_register.csv` and the workbook Evidence tab distinguish reported inputs, proxies, fitted quantities, assumptions and missing inputs. `inputs.json` records source snapshot hashes. Source Data, Fee Data and Evidence are values-only; builds do not read checks. Source-file extraction via openpyxl is read-only; workbook authoring/export uses Artifact Tool.

Next requested CapIQ export: CPRT FY27 quarterly consensus, fiscal period end dates, USD units, as-of date and contributor counts, preferably service revenue and US/international service breakdowns. Broker-level estimates are useful. Total company revenue cannot be relabeled service revenue; retain purchased vehicles and acquisition perimeter differences. If only total revenue is available, it is context until a supported bridge exists.

Next AlphaSense documents: targeted title-volume/account-rollout disclosure, delivery adoption and revenue evidence, and original carrier-allocation source passages. Searchable PDFs or structured exports are preferable to screenshots. Avoid requesting the whole library.

## Verification and reproduction

1. `prepare.py`: local source extraction and fixed baseline calibration, no network.
2. `build.mjs`: live formulas, source/assumption labels, bounded input propagation checks, renders all 12 sheets, exports one workbook.
3. `validate.py`: reads exported cached results and independently reconstructs fleet exposures, 1,728 damage states, fees, carrier allocations and quarterly revenue. Confirms no Excel error cells or external workbook links and values-only data tabs.

Input tests change forecast title adoption, repair-cost level and sale conversion, then restore defaults. Reported history stays unchanged. Engine: Artifact Tool plus independent Python reconstruction; native desktop Excel behavior has not been separately tested.

No conclusion has been forced to align the two thesis directions. The next research objective is to replace the consequential assumptions and explain the historical residuals before asserting a consensus gap.
