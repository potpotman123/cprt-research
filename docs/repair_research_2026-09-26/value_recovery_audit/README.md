# Audit of the 1.50 value and auction-price assumptions

Date: 2026-09-26. Bounded research: local source/code audit, five-model current valuation check, one historical PDF extraction, and targeted public-source searches. No bulk listing collection, OCR, paid data, or model/workbook overwrite.

## Verdict

Neither 1.50 input is validated for the target population. The auction assumption means light trucks sell for **50% more than cars**, not that salvage recovers 50% of ACV. Both inputs descend from the same pre-loss value proxy, so they are not independent evidence. The prior -0.1601 percentage-point service-revenue contribution is an assumption-conditional calculation, not an empirically established effect or reliable sign forecast.

## Provenance of the old numbers

`/Users/kwu/cprt/reports/E8_body_value_ratio.md` and `scripts/experiments/e8_body_value_ratio.py` construct current new-vehicle prices with assumed segment weights: LT $49,408/car $30,657 = 1.61. Five-year retained-value fractions give LT 57.2% versus a 58.2% all-vehicle proxy for cars. The product is about 1.58. The report then chooses 1.50 for the older salvage pool; this is a judgment adjustment, not a measured age-10 result. The report itself labels the level assumed.

Original issues: assumed size/trim mixes; all-vehicle retention substituted for car-only; five-year depreciation extrapolated to a roughly ten-year-old pool; current-new-price/older-vintage mismatch; listed-pool weights used outside their population. Workbook formula checks establish arithmetic integrity, not empirical accuracy.

The pinned source in `../body_mix_working_case/prior_model_source.py.txt` explicitly identifies its 1.50 vehicle-value ratio as E8. It places the ratio in the total-loss propensity offset and also in the auction-price mix formula. The threshold calculation assumes the same proportional economic totaling threshold across bodies. E8 explicitly acknowledges transferring pre-loss values to salvage without body-specific recovery data.

## New check 1: actual older-vehicle valuation tables

Source population: KBB national dealer Fair Purchase Price estimates for 2016 model-year vehicles in typical condition, retrieved 2026-09-26. These are retail proxies, not insurer ACV, auction proceeds, or matched VIN valuations. The page's 2019 editorial-review date is not the pricing date; pricing text says values update weekly. Source URLs and all transcribed inputs are in `kbb_2016_panel.csv`.

Selection: two mainstream midsize sedan/compact crossover brand pairs (Toyota Camry/RAV4 and Honda Accord/CR-V), plus F150 SuperCrew as a pickup check. This is a convenience panel for falsifying an indiscriminate 1.50 assumption, not a random or population-weighted estimator. Chevrolet Silverado was attempted but its pricing table repeatedly failed retrieval, so it is excluded explicitly. No van or large-SUV inference is justified.

Aggregation: include all nonhybrid sedan trims on Camry's table; sedan-only Accord trims; nonhybrid RAV4 trims; all CR-V trims; all F150 SuperCrew trims/bed lengths. Equal weights within each model, then equal weights between the two sedan and two crossover models. This avoids selecting only the cheapest or most expensive trim, but does NOT approximate observed trim sales; the F150 panel contains substantial luxury-trim representation. Mileage, drivetrain and exact condition are not held constant.

| Model / grouping | Mean USD | Relative to two-sedan mean |
|---|---:|---:|
| Camry | 13,780 | 1.006 |
| Accord | 13,610 | 0.994 |
| Two-sedan reference | 13,695 | 1.000 |
| RAV4 | 15,962.50 | 1.166 |
| CR-V | 14,940 | 1.091 |
| Two-crossover reference | 15,451.25 | 1.128 |
| F150 SuperCrew | 20,440.91 | 1.493 |

Finding: a 50% premium can resemble this pickup check while badly overstating these crossovers' retail-value premiums. Neither 1.128 nor 1.493 is adopted as a fleet-wide ACV or salvage-price parameter. The existing report `E1_step1_listed_body_share.md` finds the listed-pool shift is concentrated in SUVs/crossovers, with pickups roughly flat; therefore confusing pickups with all light trucks is particularly consequential.

## New check 2: historical insurer total-loss ACV

Manheim 2014 Used Car Market Report, printed page 39 / PDF page 40, reproduces Mitchell Industry Trends Report Q4 2013 data. Source PDF and extracted text saved under raw/. Latest displayed quarter is Q3 2013:

| Body | Total-loss ACV | Ratio to sedan | Mean vehicle age |
|---|---:|---:|---:|
| Sedan | 7,351.28 | 1.000 | 10.46 |
| SUV | 9,329.23 | 1.269 | 10.12 |
| Pickup | 9,879.70 | 1.344 | 12.03 |
| Van | 5,837.79 | 0.794 | 11.15 |

This is a more relevant measurement concept than new-car ATP, but old, selected on total-loss status, and not matched on age or model mix. It cannot replace a current same-age exposure-value parameter. It provides a second check against assuming every light-truck category is worth 50% more and shows why vans need their own treatment. It contains ACV, not category-level auction proceeds. The initially located Manheim 2016 PDF could not be downloaded (zero bytes); no figures were taken from that failed file.

PDF URL: https://appliedantitrust.com/13_merger_review/2_settlements_ftc/hertz/5_comm/Manheim%202014%20UCMR.pdf

## Auction recovery is still unmeasured

Read-only inspection of `/Users/kwu/cprt/data/cprt.db` lot_anchors and lot_snapshots found identifiers, year, make/model, title and location fields, but no ACV or final sale proceeds. Listing composition alone cannot calibrate auction-price premiums. Targeted public-source searches did not produce a current matched body-level recovery table. This is a bounded negative search result, not a claim no such data exist.

Let V be pre-accident value, g be hammer price/V, and n be net seller salvage proceeds/V. In the simplified economic decision framework:

- auction-price ratio = (V_LT/V_car) * (g_LT/g_car)
- economic repair threshold ratio = (V_LT/V_car) * (1-n_LT)/(1-n_car)

The former affects fee-bearing auction value; the latter affects whether repair is economically preferable to total loss. Net proceeds and gross auction price must not be equated when fees/costs differ. Actual claims decisions can also reflect legal thresholds, anticipated supplements and other costs.

Mechanical example ONLY, ignoring gross/net differences: ACV ratio 1.50, car recovery 30%, LT recovery 40% imply an auction-price ratio 2.00 but threshold ratio 1.286. Thus a stronger salvage market can simultaneously increase proceeds and make totaling economical at a lower repair bill. No 30%/40% estimate is asserted.

## Model consequence and next measurement

Keep ACV and recovery separate by age and body (at minimum car, crossover/SUV, pickup, van). Do not propagate a single new panel average across all cohorts. Preserve the old model as a labeled historical working case; withdraw empirical confidence in its net-revenue sign.

Next bounded acquisition should seek a small set of accessible, completed auction records with BOTH reported ACV and unambiguous accepted sale prices, not live/highest bids. Start with the model/year cohorts above; record sale date, mileage, damage, run condition, title and seller. Test field availability first. A failed sale or missing accepted-price label is not a zero-price sale. Deduplicate relistings by VIN; retain damage/age controls and flag missingness. Dealer retail checks help benchmark ACV but cannot supply recovery.

Before a bulk scrape or a paid provider purchase, review demonstrated field availability, expected sample coverage, retrieval cost and selection bias with the user. For the exposure-value leg, derive model/year weights from the existing listing data only as a disposal-pool proxy; use insured exposure weights if estimating total-loss propensity. Avoid treating auction-selected ACVs as an unbiased exposure distribution.

## Reproduction

`calculate.py` reconstructs the descriptive checks from the explicit transcriptions and writes `results.json`. Source provenance, exclusions, exact populations and limitations are above; `manifest.json` hashes saved artifacts. No OCR was needed. No current auction ratio or new population-wide point estimate was validated in this pass.
