# Materiality screen: fleet turnover versus changing economics

28 September2026. Existing data only;17 one-factor cases, no fit, no scraping and no forecast changes. `materiality_summary.csv` gives first-half results; `materiality_quarters.csv` gives all four forecast quarters with and without inherited carrier allocation. Computation takes seconds; no empirical probability is attached to scenarios.

## Method and rationale

Keep observed revenue anchors, fleet paths, fitted claim corrections, fees and adoption unchanged. Alter SUV/pickup repair or ACV ratios by ±10% relative, or multiply their salvage-recovery curve by0.8/1.2. Cars and vans are unchanged. These are deliberately broad analyst-selected diagnostic ranges, not evidence-based confidence intervals or equally sized economic shocks. Recovery changes feed BOTH the totaling threshold and auction proceeds, avoiding an artificial price-only test.

Structural cases change the parameter in both comparison periods; they ask whether uncertain vehicle economics change the impact of fleet turnover. Forecast-only cases change it in FY27 only; they ask what an actual change over time could do. No historical recalibration is performed: structural cases may cease to match historical calibration targets and are not admissible alternative fitted forecasts. The same-quarter revenue anchor remains fixed, so permanent level effects mostly cancel in structural growth comparisons.

Four additional forecast-only cases move repair or ACV5% across all bodies. They distinguish broad economic sensitivity from a truck-specific mechanism. Symmetric endpoints prevent selecting only bearish outcomes. No joint scenario search or optimization is warranted at this screening stage.

## Results

Prior-year H1 total service revenue is$1943.896m. Carrier-neutral baseline fleet effect is-$0.544m.

| Structural assumption varied, both periods | H1 fleet-effect range, $m |
|---|---:|
| SUV/pickup repair ratio ±10% | -6.126 to +4.206 |
| SUV/pickup ACV ratio ±10% | -4.094 to +3.047 |
| SUV/pickup recovery curve ±20% | -6.958 to +5.579 |

Across these cases, the fleet effect remains roughly -0.36% to +0.29% of the H1 total service base. This is a bounded screen, not proof that every possible specification has a small effect.

Forecast-only changes are much larger. Relative to the unchanged-economics baseline, all-body repair costs -5%/+5% change H1 service by-$106.198m/+$105.876m; all-body ACV -5%/+5% changes it by+$72.710m/-$70.923m. SUV/pickup recovery -20%/+20% changes it by-$150.376m/+$166.235m. These are latent cost/value/recovery changes, not changes in selected average repair bills or observed auction ASP. The assumed damage distribution around the threshold drives the size. Correlated repair/value changes can offset: equal scaling preserves model TLF, although fees can still change with auction prices.

The baseline inherited carrier increment is-$99.823m, reported separately. Scenario carrier increments vary because capture changes act on the altered available units and revenue. Do not add the baseline carrier dollar effect unchanged to every scenario. Allocation is still unvalidated; carrier-neutral diagnostics are not an assertion that actual allocation will be flat.

## Decision and next evidence task

Deprioritize further fleet subtype detail as the main route to a large six-month thesis. Retain the cohort build as the composition foundation. This screen does not justify adopting a forecast shock or changing the direction of the pitch.

Next priority is economic response validation: matched age/body/damage observations of repair estimates, pre-loss ACV and salvage offers around the repair-versus-total threshold. First inventory the existing repair/ACV work and its failed historical tests; identify whether we can obtain an independent within-cohort change rather than reuse selected means as latent inputs. Explicit competitors are genuine cost/value change, claim-filing selection, and changing damage severity. A matched pair or a disclosed threshold distribution is preferable to another broad aggregate index. Do not collect thousands of listings: auction-only data omit the repaired comparison group.

If compatible evidence remains unavailable after a bounded feasibility pass, retain these as sensitivities and prioritize ancillary adoption's incremental revenue versus sell-side expectations. No reason exists to keep refining a static repair premium merely because the dynamic model is sensitive.

Validation:76 checks, including baseline headline reproduction, units×RPU reconciliation, equal repair/value scaling, and consistent recovery effects. Results and hashes in `materiality_results.json`. These establish arithmetic consistency, not empirical elasticities.
