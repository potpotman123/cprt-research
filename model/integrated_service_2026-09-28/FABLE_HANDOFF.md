# Fable handoff — integrated analytical model

Read README.md and INPUT_REGISTER.md before presenting outputs. The delivered model is executable Python + JSON/CSV, not a redesigned workbook. Preserve formulas and assumptions if translating it; do not merely paste one forecast case as unexplained hardcodes. Source/model dollars are in millions; dollar-per-vehicle outputs are in dollars.

## Four primary views

1. **RPM Summary:** eight fiscal quarters. For historical periods display reported US/international/legacy service totals from historical_controls.csv; show model reconstruction separately. Forecast periods use quarterly_results.csv us_musd, intl_musd and legacy_service_musd, explicitly labeled provisional. Keep the acquisition overlay separate; post-close consolidated service is unavailable, not zero, until classification is supplied. No EPS or DCF.
2. **Volume Build:** fleet exposure proxy, seasonal proxy, assumed frequency, normalized claim weights, TLF, effective capture and normalized fee sales. Label counts as modeled/normalized, not disclosed. Timing convention is sale-equivalent bypass; do not draw an inventory chart from null balances.
3. **Vehicle Economics:** six frozen cohort parameter rows, four body ratios, repair and value source targets, selected price distributions and fee schedules. Show age constraints and fitted distributions separately from source observations. Supporting cohort_engine.csv has quarterly probabilities/values/fees.
4. **Revenue Bridge:** buyer fees + seller fees + title + delivery gross − fee waivers = insurance services; add other-US = US services; add international = legacy services. Show historical residuals. Display ancillary jobs/prices and equivalent activity × fee branches as assumed, not observed breakdowns.

## Supporting organization

Keep raw controls, posted fees, CCC constraints and provenance separate from cohort/selection, capture and fee/service engines. One assumptions section owns each editable input; do not duplicate different copies across tabs. Color section dividers only, use compact financial tables and preserve the user's previously approved organization.

## Population contracts

- US insurance branch: assumed consignment sale-equivalent vehicles, no purchased-vehicle sales dollars. Title/delivery here apply only to this branch.
- Other US: remaining US service perimeter, including noninsurance service activity; no duplication of the insurance attachments. Equivalent units are not physical sales.
- International: aggregate service branch; explicit fee/activity/FX assumptions, not an independently measured unit census.
- Vehicle ACV: pre-accident value. ACV Auctions: optional acquisition. Keep names distinct.
- Same selected damage states determine total-loss probability, auction price and core fees. RPU is an output, not an independent unexplained growth line.

## Required controls

Legacy branch addition, claims/total-loss weight normalization, fee-sale reconciliation, captured share applied once, source/assumption status, missing-data cells, acquisition close/classification gate, reported-versus-reconstructed history, and one explicit base normalization. Do not force residuals to zero, turn null post-close acquisition service into zero, or treat a calibration target as independent validation.

Do not display a consensus gap until compatible service-revenue estimates are supplied. Do not convert a normalized unit or activity-equivalent into a capacity utilization estimate. Do not annualize a quarterly default as an economic thesis. Preserve the current historical errors in the review view.
