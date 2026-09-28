# Historical body-type mix: fill the missing subtype history

Completed September 28, 2026. Scope: reuse existing aggregate vehicle-sales history and retrieve only missing vintage-specific body shares. No auction listing scrape, OCR, paid data, parameter fit or Excel authoring.

## Existing workbook checked first

The user supplied `CPRT_Intermediate (1).xlsx` from the Messages temporary attachment path recorded in `workbook_inventory.json`. It is a useful repository of the earlier work. Its README dates the build to September 15 and identifies committed CSVs as the source.

The `Data_Sales` table contains cars, aggregate light trucks and heavy trucks. All **168 historical values** checked (56 years, 1970–2025, three categories) match `data/csv/light_vehicle_sales_by_year.csv` exactly. The workbook also contains survival, fleet, age curves, claims, financial and insurer data; these were inventoried rather than rebuilt. No SUV/pickup/van birth-history table was identified, and a text scan across all sheets found no subtype terms. The workbook was read only. Cached formula outputs were not validated or adopted.

One labeling issue matters: the workbook calls the sales rows “model year,” but its source note explicitly describes calendar-year aggregation of FRED sales. Do not treat that header as proof the series is model-year registrations. The existing age roll uses these sales as birth proxies.

## New source and extraction

Primary source: [EPA 2025 Automotive Trends public data](https://www.epa.gov/automotive-trends/explore-automotive-trends-data). [EPA's definitions](https://www.epa.gov/automotive-trends/about-automotive-trends-data) identify the population as production delivered for sale in the United States by model year, with 1975–2024 final and 2025 preliminary.

The publicly exposed summary table contains 408 rows: 51 model-year labels × eight categories, including aggregate control rows. `fetch_epa.mjs` reads that existing table's first four columns through its public Qlik interface. It uses the source object's own expression restricted to manufacturer `All`; no summing manufacturers or counting aggregate categories twice. There is no account login or browser automation. A small object-path retrieval error was corrected before acquisition; only the successful numeric output feeds the build.

`epa_public_table.json` preserves numeric values, display text, model-year labels, source URLs, table identity, expression and retrieval timestamp. Numeric values are more precise than the displayed three decimals. `epa_source_shares.csv` preserves all source rows. **The eight preliminary-2025 rows have null production shares in this retrieval.** They remain unavailable, not zeros or estimates. Thus the usable acquired history is **50 final years, 1975–2024**.

## Classification: body type is not regulatory class

EPA's five mutually exclusive types are Sedan/Wagon, Car SUV, Truck SUV, Pickup and Minivan/Van. [EPA explains](https://www.epa.gov/automotive-trends/highlights-automotive-trends-report) that car/truck SUV assignment reflects regulatory criteria, including drive configuration and weight. It is **not** a crossover/unibody versus traditional/body-on-frame classification.

For our four-body research model, the candidate mapping is:

| EPA category | Proposed research body | Limitation |
|---|---|---|
| Sedan/Wagon | Car | Preserve source definition, including cars not colloquially called sedans |
| Car SUV + Truck SUV | SUV | No separate crossover/traditional-SUV identification |
| Pickup | Pickup | Source light-duty coverage may differ from earlier broad sales categories |
| Minivan/Van | Van | Existing model economics are named Minivan; applying them to all vans requires an explicit transfer assumption |

Do not append Car SUV to a regulatory-car total and also put it in SUV. The source's `All Car`, `All Truck` and `All` rows are controls, not additional vehicle bodies.

## What the history shows

Shares of all source light-duty production delivered for US sale, percent; both SUV regulatory types combined:

| Model year | Sedan/Wagon | SUV | Pickup | Minivan/Van |
|---|---:|---:|---:|---:|
| 2000 | 55.07 | 18.97 | 15.76 | 10.20 |
| 2005 | 50.51 | 25.70 | 14.47 | 9.32 |
| 2010 | 54.52 | 28.97 | 11.48 | 5.03 |
| 2015 | 47.19 | 38.22 | 10.67 | 3.91 |
| 2020 | 30.94 | 51.73 | 14.40 | 2.93 |
| 2024 | 23.68 | 60.24 | 14.07 | 2.01 |

The older fixed model assigned SUVs 72.39% of every light-truck birth cohort. In this EPA series, SUVs are approximately 63.70% of non-sedan production in 2010, 72.39% in 2015, 74.91% in 2020 and 78.92% in 2024. Thus the old assumption resembles one vintage, not a history. These denominators differ from regulatory light trucks; the comparison motivates a better mapping, not a claim that the categories are identical.

## Candidate adapter: preserve old totals, label the transfer

`body_mix_by_model_year.csv` contains observed source shares and calculated shares within SUV + Pickup + Van. It does not contain observed calendar-year category sales.

`candidate_body_births.csv` applies those conditional subtype shares to the **existing** light-truck total for the same numbered year, leaving existing car totals unchanged:

`candidate SUV births[y] = existing light-truck births[y] × EPA SUV share[y] / (EPA SUV + Pickup + Van shares[y])`.

Pickup and Van follow the same rule. Every year's existing total, and the car-versus-light-truck allocation, is preserved. This is a hybrid transfer proxy: model-year production composition applied to existing sales-based birth totals. It is **not new observed subtype sales**, and preserving the aggregate does not validate the population mapping.

Boundary rules are explicit:

- 1975–2024: same-numbered model-year mix transferred to the existing sales year.
- 1970–1974: retain the earlier fixed subtype assumptions; no invented EPA history.
- 2025–2027: hold final 2024 subtype mix because the retrieved 2025 shares are unavailable. This is an assumption. Existing 2025 sales totals are reused; 2026–2027 retain the prior model's flat-2025 sales assumption.

The source series alone does not resolve whether every vehicle classified as a car or light truck in the earlier sales data maps to our chosen body categories. A full alternative allocation of all existing light-vehicle births using EPA's four shares could be explored separately, but it would change the car/LT split and survival mapping. Do not silently substitute that alternative.

## Model integration gate

This delivery closes the **data availability** gap for vintage-specific broad subtype shares, subject to the source-to-model transfer. It does not close the crossover-versus-traditional-SUV gap. No production model inputs or forecast outputs were changed.

For a subsequent bounded integration comparison, replace the fixed subtype split at the birth-vintage level, retain source and modeled birth tables separately, and inspect survival-adjusted counts by age/body before applying damage economics. The current model uses a generic light-truck survival curve and proxy minivan economics; neither becomes source-backed merely because birth shares improve.

Changing the base-period body composition also changes the relationship to the existing damage calibration. Do not quietly refit vehicle values or claim weights to erase that change. First report the baseline compatibility difference and decide explicitly whether fixed calibration corrections or reanchored claim composition are appropriate. Do not read a level difference between alternative datasets as a year-over-year revenue effect.

## Checks and reproduction

`build.py` verifies five source-body shares sum to one within rounding (maximum error 0.000001), reconciles Car and Truck regulatory subtotals, ensures conditional subtype shares sum to one, and preserves every year's existing sales total. Raw 2025 nulls remain visible. Workbook audit compares source values, not computed forecast results.

Files:

- `fetch_epa.mjs`: optional public-source refresh, using bundled Node with native WebSocket.
- `epa_public_table.json`, `epa_source_shares.csv`: preserved source data and definitions.
- `build.py`: local reproducible mapping; no network.
- `body_mix_by_model_year.csv`, `candidate_body_births.csv`: source summary versus modeled candidate.
- `results.json`: source hashes, range, checks and samples.
- `audit_workbook.py`, `workbook_inventory.json`: read-only attached-workbook inventory and exact source comparison. The temporary workbook path may not exist on a teammate's machine; the acquired body-share build runs independently of it.

Existing `light_vehicle_sales_by_year.csv` and archived listing-mix research remain authoritative for their own populations. They were neither replaced nor reacquired.
