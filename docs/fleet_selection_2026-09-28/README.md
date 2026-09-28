# Resume the fleet and damage-selection foundation

Completed next step: [age versus within-group historical recheck](AGE_VERSUS_WITHIN_BUCKET.md). Existing CCC data support changes within broad age groups as the dominant component of the recent conditional reconstruction; they do not isolate repair inflation or prove a demographic reversal.

28 September 2026. Delivery research is parked at the user's instruction. It remains an explicitly assumed component pending evidence; no additional delivery sourcing, quote collection or adoption calibration is needed now. Spreadsheet construction remains with Fable.

## Question and method

Can the existing fleet roll, combined with the existing joint total-loss/auction-fee engine, produce a meaningful near-term composition effect without assumed service growth?

`check.py` reads only the existing linked-model JSON and its prior validation results. No network, Excel access, scraping or new calibration. It computes four composition worlds for each FY27 quarter: freeze both age and body-within-age mix at FY26Q4; change age only; change body-within-age only; change both. All worlds retain the same forecast total fleet size. Relative claim propensity by exact age remains fixed. Cohort repair/value/recovery assumptions and September fee grid also remain fixed. Carrier allocation is held common, so cancels from each quarter's percentage comparison; no carrier ramp is included in H1 aggregation. Title/delivery dollars are excluded entirely.

This is a statistical decomposition of fleet composition, not a claim that each counterfactual is a feasible physical fleet. Conditional body mix means the body-type proportions among vehicles of each exact age. The order of conditioning matters. Total fleet size and other operating drivers are outside this comparison.

## Results: core US insurance auction revenue only

Percent differences from that quarter's same-size fleet with FY26Q4 composition; not YoY growth, consolidated service growth or a consensus miss.

| Quarter | Units change | Core RPU change | Core revenue change |
|---|---:|---:|---:|
| FY27 Q1 | -0.0136% | -0.0265% | -0.0401% |
| FY27 Q2 | -0.0290% | -0.0528% | -0.0818% |
| FY27 Q3 | -0.0680% | -0.0774% | -0.1454% |
| FY27 Q4 | -0.1143% | -0.1015% | -0.2157% |

H1 combined revenue effect is -0.06091% (about 6.1 basis points), comprising approximately -0.03409% from age and -0.02695% from body-within-age, plus interaction. This is a different model and reference comparison from the older September 27 tests; do not treat changes in sign as a new observed market development.

The original engine's raw units and RPU were reproduced for all eight historical/forecast quarters. Each counterfactual preserves total fleet stock. The full-changing world reconstructs the original calculation, and age/body/interaction effects reconcile. These are implementation checks, not empirical validation. No unsupported absolute-unit normalization was needed and no dollar forecast was adopted.

## What limits this answer

1. **Crossover history is not represented properly.** Car/light-truck births vary by vintage, but light trucks are split into SUV/pickup/minivan using one fixed pool proxy across all vintages. The model therefore cannot claim to have quantified a historical crossover boom separately from pickups. It lacks that input.
2. **Age economics are stepped.** Actual fleet ages roll, but ACV and calibrated damage distributions use six representative ages (0, 2, 5, 8, 11, 17). Every 13+ vehicle shares the same representative age economics. This can obscure within-bucket aging and concentrate effects at boundaries. It does not prove the true effect is larger or smaller.
3. **Calendar changes within age are absent.** Repair costs, ACV and salvage economics for a given age/body cohort are fixed. Mix shifts alone cannot test whether repair inflation or used-value changes move the total-loss threshold in coming quarters.
4. **Claims-age weights are fitted proxies.** Fleet composition is not insured collision-claim composition. Coverage and usage can change with age, so more older cars in operation need not translate one-for-one into more insured claims.
5. **Fee discretization remains.** This diagnostic preserves the original nine severity states to make it reproducible. Earlier fee-band work showed that point prices can produce artificial jumps under price shocks. A future shock test must use consistent within-cohort dispersion and check numerical stability. No artificial price-band catalyst is claimed here.

## Priority decision

The current composition effect alone is too small to support a material six-month thesis. Do not enlarge arbitrary shocks to rescue it. The next high-value work is to establish whether historical total-loss changes arise from age composition or changing economics within the same age group.

Use the existing CCC age tables first: identify which years and populations are actually available; compare fixed-age total-loss probabilities and report missing intervals. If only one year exists, label the test unavailable rather than interpolate an invented history. Then assess whether existing repair/value series share those populations. This can distinguish a stable age effect from a changing repair-versus-value threshold without a new scrape.

Only after that evidence check, revise the computational engine to use smoother age economics while reproducing the observed bucket targets at the original calibration date. Do not refit every forecast shock back to unchanged historical TLF, which would remove the effect being tested. Smooth interpolation is an assumption, not new data. Retain the coarse version as a diagnostic comparison.

Vintage-specific body mix is a separate data question. First inventory existing new-sales registrations/classification sources, especially whether SUVs and crossovers are separable. Avoid applying today's auction or listing composition backward through historical births. A more elaborate body split earns further work only if its attainable effect is material.

## Source status

Input snapshot: `model/linked_service_revenue_2026-09-28/inputs.json`; SHA256 in `results.json`. Existing body repair ratios, retail ACV proxies, survival adjustments, claim-age decay, latent severity calibration and seller terms retain their prior limitations. No source status is upgraded by this test. Existing workbook and main forecast remain unchanged.
