# CapIQ consensus review

28 September 2026. Read-only analysis of user-provided consensus XLSX and S&P methodology. No source or forecast workbook was modified. No assertion that sell-side consensus equals expectations priced into CPRT.

## Findings

The supplied Consensus tab contains consolidated total revenue, not services or geographic service revenue. FY27 revenue has analyst-count labels 8/8 in all four quarters; FY28 revenue has 2/2. FY27 normalized EPS has 8/8, but other measures have different contributor coverage. The export lacks individual contributor dates, company share price, price target and contributor-specific acquisition treatment.

Total revenue FY27Q1–Q4 means ($m): 1183.10, 1166.93, 1286.52, 1224.42. Growth against corresponding supplied FY26 actuals: 2.43%, 4.04%, 4.00%, 6.25%. H1 sum $2350.03m, growth 3.22%. FY27 sum $4860.97m, growth 4.17%. These are sums of quarter means, not separate annual consensus observations. Display-rounded source values limit precision.

Near-term means and medians are similar, but this cannot establish forecast accuracy, independence of contributors, or freshness. Broker detail and update timestamps are needed. Historical final-estimate-versus-actual rows do not substitute for a comparable fixed-horizon point-in-time forecast accuracy study.

## Methodology source

https://www.spglobal.com/market-intelligence/en/solutions/capital-iq-estimates

S&P describes collection of contributor forecasts, standardization and majority-basis inclusion, exclusion of estimates not reflecting significant events or guidance, and presentation of excluded contributors. This is a documented sell-side forecast benchmark, not a direct survey of buy-side expectations. S&P's general quality process does not independently verify each CPRT contributor's dates or acquisition perimeter in this export.

## Model treatment

Retain as a separately labeled external total-revenue benchmark. Do not insert these values into the service-only consensus input. Obtain broker service/purchased splits or granular estimates with appropriate access. Until then, an implied service benchmark would require an explicit assumed purchased-vehicle forecast and must be labeled derived, not reported consensus.

Maintain three distinct concepts: (1) reported analyst consensus, (2) the research operating forecast, (3) price-consistent valuation scenarios. Do not tune consensus to match the share price. A reverse valuation can solve for one or a small number of drivers conditional on held-fixed margins, reinvestment, discount rate, long-term growth and net cash. One price cannot uniquely identify all operating assumptions, and near-term unit/RPU combinations can yield the same revenue.

An analyst fair-value estimate 20% above the share price does not invalidate its operating estimates. The difference may reflect the valuation multiple, discount rate, longer-term assumptions, or timing. It also means that a forecast below sell-side consensus is not by itself a sufficient short case: independently assess value and the dated catalyst relative to the actual share price. No valuation or current-price match was computed in this pass because this export supplies neither share price nor target and a validated valuation model is outside this step.

Reproduce the extracted numeric audit with extract.py. No large collection or OCR required.
