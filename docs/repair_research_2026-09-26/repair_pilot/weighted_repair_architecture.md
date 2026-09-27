# Weighted repair-cost baseline: architecture and first source

2026-09-26. Bounded research: ten search queries; public indexed primary-source report text; no OCR, paid access or large collection. Direct PDF request returned 403. No forecast workbook changes.

## Recommended approach

Start with a weighted component/operation index, not a simulation of every crash. Keep two outputs: a common-mix price index that compares the same work across body types; and an own-mix index that allows each body type to have different component damage/replacement frequencies. Their difference distinguishes price/repairability from observed damage mix. Keep pickups separate from crossovers/SUVs.

For component j and body b, define involvement probability q, replacement probability conditional on involvement r, expected quantity conditional on replacement m, replacement cost K, and repair cost H. A first-order average is sum_j q[b,j] * (r[b,j]*m[b,j]*K[b,j] + (1-r[b,j])*H[b,j]) plus separately allocated common operations. K includes parts, labor and paint; price sourcing mixes OEM, aftermarket and recycled parts using observed shares when available. Shared disassembly, paint setup and scans must not be charged independently to every component. Correlation is not needed just to add expected costs, but matters for total-loss tail probabilities; correlated bundle costs and overlaps must still be handled.

A common-mix comparison uses the same q/r/m across bodies and changes prices/hours. An own-mix comparison uses each body's q/r/m. No measured SUV/pickup/car-specific weights have yet been located. Do not fabricate these from ranks, dealer catalog breadth or auction stock.

## First usable frequency source

Mitchell Q3 2015 Industry Trends Report, feature by Greg Horn, reports a subset of three million repairable estimates from insurers, bodyshops and independent appraisers. The historical pooled table includes involvement and conditional replacement rates. Examples: bumper cover 68%/72%; fender 37%/59%; hood 24%/56%; headlamp 29%/95%. Multiplication gives indicative replacement involvement of 49.0%, 21.8%, 13.4%, and 27.6%, respectively. Categories overlap and must not be normalized to sum to 100%; these are not segment-specific unit quantities. Original observation-window/geography and deduplication details remain incompletely verified. Treat as a historical seed, not current calibration.

Source: https://device.report/m/5694a4bab9268932b8a1959beafb692ec37c21ce3c2aba84371219a3e5b41083.pdf

## Executed arithmetic demonstration

Apply common historical fender replacement involvement 0.37*0.59 and hood replacement involvement 0.24*0.56 to the six-price catalog study's fender/hood prices. Assume one part per replacement event for demonstration only. The result is recorded in repair_frequency_seed.json. This is a two-component index, not expected total claim cost. Fender side/multiplicity, other components, repair rather than replacement, labor, parts sourcing and selection are missing. It should not be inserted into the 1.18 full-cost sign-reversal sensitivity.

## Scope versus Copart total-loss inference

The baseline can compare expected repairable costs without building a complete crash simulator. It cannot independently estimate total-loss frequency: repairable estimates exclude many expensive cases that were totaled, and average cost does not identify the probability of exceeding ACV minus expected net salvage. Retain broad damage-severity bins only when an all-claim or defensible pre-decision source supports their weights. Until then, show a range of threshold-crossing scenarios rather than claim a calibrated body-specific total-loss rate.

Next data targets are: modern component involvement and repair/replace frequencies by body and age; complete operation costs for a small common basket; OEM/aftermarket/recycled shares; all-claim estimates or total-loss probabilities by comparable age/value/damage. Current public data support only the provisional common-mix index. Existing catalog prices cover two panels and insulation, so no complete ten-component cost index is claimed.
