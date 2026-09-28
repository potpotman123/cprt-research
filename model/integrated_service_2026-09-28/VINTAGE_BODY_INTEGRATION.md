# Vintage-specific body shares fed through the fleet and fee engines

September 28, 2026. Executed `vintage_body_integration.py` using the acquired EPA-share candidate birth table and existing economic parameters. No new scrape, OCR, optimization, calibration refit or Excel authoring.

## Integration performed

For each age and calendar snapshot, select births for the corresponding vintage and body. Car births stay unchanged; SUVs, pickups and vans now have vintage-specific counts instead of a common historical split. Set the adapter's separate split multiplier to one so subtype proportions are not applied twice. Apply the same inherited survival schedules, relative claims-by-age function and fixed CY2025 cell corrections as before.

Aggregate the resulting claim masses by the six age buckets and four body types. Apply the **same frozen** cell total-loss probabilities, selected auction prices and buyer/seller fees in both cases. Include the existing constant ancillary revenue per sold unit. Compare each FY27 quarter with its own FY26 quarter, with carrier capture, timing and ancillary adoption unchanged.

This is a genuine run through the linked quantity/fee calculation, not a change to an assumed aggregate service-growth rate. The production headline forecast remains unchanged because source mapping and base calibration compatibility are not yet resolved. The candidate and fixed-split results are separately exported and reproducible.

## Quarterly results

These are fleet-only changes in the modeled US insurance branch, with other-US and international dollars held unchanged. Percentage columns are growth in that insurance branch, not consolidated growth or a consensus gap. Dollar conversion uses the existing assumed 90% US insurance revenue share.

| FY27 quarter | Sold units YoY | All-in RPU YoY | Insurance services YoY | Legacy service contribution, $m |
|---|---:|---:|---:|---:|
| Q1 | +0.0631% | −0.0813% | −0.0182% | −0.140 |
| Q2 | +0.0306% | −0.0852% | −0.0547% | −0.403 |
| Q3 | −0.0243% | −0.0785% | −0.1028% | −0.828 |
| Q4 | −0.0860% | −0.0686% | −0.1545% | −1.137 |

H1 fleet contribution changes from **+$0.290m under the fixed split to −$0.544m under vintage-specific shares**, a **−$0.833m revision**. Against the prior H1 legacy service denominator of $1,943.896m, the new net contribution is about **−0.028%** and the revision is about **−0.043%**. These are model outputs; displayed precision aids reconciliation, not a claim of estimation precision.

The observed history improves the model's cohort inputs, but does not turn this default composition mechanism into a large six-month thesis. In this run, small unit gains in the first two quarters are more than offset by small RPU declines. Later, both effects are negative. Other macro drivers—repair inflation, within-age vehicle value changes, coverage/claim frequency and ancillary penetration—were held fixed; their economic effects have not been tested by this comparison.

## Historical levels versus forecast growth

Replacing historical subtype shares changes the **level** of the CY2025 modeled auction population as well as its subsequent evolution:

| CY2025 diagnostic | Fixed split | Vintage-specific split |
|---|---:|---:|
| Surviving fleet, millions | 292.832 | 292.832 |
| Relative claim activity | 1.000 | 1.000 |
| Aggregate modeled TLF | 22.8838% | 22.8495% |
| Selected ASP, dollars | 3,040.99 | 3,057.21 |
| All-in insurance RPU, dollars | 906.51 | 908.76 |

The higher base RPU is not an incremental annual growth assumption. Our forecast ratios compare updated FY27 economics with updated FY26 economics; both periods contain the historical-data revision. Applying only the new future mix against the old historical mix would conflate a level correction with a forecast change.

## Calibration compatibility is exposed, not repaired by fitting

The old CY2025 body mix was used in the existing age-specific damage/value calibration. With original correction factors and cell economics frozen, the updated mix no longer exactly reproduces those targets. The largest six-bucket TLF deviation is **0.0741 percentage points**. Current-year selected vehicle ACV moves from $40,187 to $40,341; ages 1–3 from $30,259 to $30,460; ages 4–6 from $20,328 to $20,527. Older-bucket values also shift, recorded in the output.

We have not refitted parameters, reapportioned claim shares or hidden these discrepancies in an aggregate offset. The old car/LT totals, common LT survival schedules and common within-age raw claim propensities preserve total fleet and, in this setup, total claim activity. What changes is the body composition of selected losses and fees. This means the comparison isolates the intended subtype effect without importing a carrier loss or extra fleet-growth shock.

## Data and modeling limits retained

1. EPA model-year production shares are transferred onto existing sales-based birth totals. This is a candidate mapping, not observed subtype registrations.
2. Both regulatory SUV categories are combined. It does not distinguish unibody crossovers from traditional SUVs.
3. Vans use the model's existing minivan economics. No new van repair/valuation calibration was acquired.
4. Subtype mix for 2025–2027 holds final 2024 mix because retrieved preliminary 2025 shares are null. New sales totals for 2026–2027 still hold 2025 levels.
5. All same-age vehicles in a body group share the existing economics; the model does not represent within-SUV model/platform changes.
6. The quarterly roll interpolates annual snapshots. The analysis does not observe precise registration, accident or auction-sale timing.
7. Current fee schedules and assumed buyer/seller terms remain fixed; no historical fee reconstruction or carrier-specific economics is introduced.

These caveats do not justify choosing assumptions that make the result bigger. The evidence supports upgrading the historical inputs while retaining a modest current composition-only effect. A materially different thesis would require a distinct, evidenced change in economics or exposures, not relabeling this small effect.

## Outputs and verification

- `vintage_body_quarters.csv`: eight quarters per case, activity, TLF, ASP, RPU and expected fee revenue.
- `vintage_body_cells.csv`: 384 case/quarter/body/age records connecting claims to selected losses and fees.
- `vintage_body_growth.csv`: side-by-side quarterly unit/RPU/revenue changes and dollar revision.
- `vintage_body_calibration.csv`: age-target deviations and selected-value comparison.
- `vintage_body_results.json`: summary, source hashes, assumptions and 40 passed checks.

Checks include reproducing the original cohort bridge, a constant-share adapter round-trip, preserving total surviving fleet, all quarter units-times-RPU identities, growth reconciliation and old calibration targets. These verify implementation, not predictive validity. No primary inputs or existing headline forecast files were overwritten.
