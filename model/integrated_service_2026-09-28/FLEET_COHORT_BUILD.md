# Fleet cohorts: explicit activity, age mix and body mix

September 28, 2026. First carrier-neutral cohort build after the historical baseline repair. Existing local data and one small calculation only; no scraping, OCR, optimization or spreadsheet design. Production forecast files and assumptions are unchanged.

## What was built

`fleet_cohort_build.py` generates 1,472 single-age/body/quarter records: ages 0–45, four bodies, eight fiscal quarters. Each record exposes interpolated births, survival, surviving fleet, relative claim propensity, calibration correction and claim contribution. These aggregate into 192 age-bucket/body cells and four forward quarterly revenue bridges.

Outputs:

- `fleet_single_age.csv`: auditable fleet-to-claims arithmetic. Births and surviving vehicles are in thousands; claim mass is a relative index, not physical claims.
- `fleet_selected_cells.csv`: claim shares, TLF, selected total-loss shares, ASP and fees for each economic cell.
- `fleet_quarterly.csv`: total fleet proxy, revised claim-activity index, TLF, conditional ASP/RPU and expected service revenue per claim.
- `fleet_revenue_bridge.csv`: separate activity, age-mix and within-age body-mix effects with capture held unchanged YoY.
- `fleet_cohort_results.json`: source hashes, checks, summary and limitations.

## Structural correction under evaluation

The existing engine scales total claims with total fleet size, then separately changes the age/body distribution of those claims. That does not carry changing claim propensity through to total activity. In this candidate, the same weighted vehicle cohorts determine both total claim activity and the distribution of claims.

For age a, body b and quarter q:

`raw claim exposure[a,b,q] = interpolated cohort births × survival[a,b] × relative claim propensity[a]`.

The latest damage calibration already supplies a CY2025 claim share for each six-age-bucket/four-body cell. Define a fixed cell correction as that target share divided by the corresponding raw CY2025 claim exposure. Multiply each single-age raw contribution by its cell correction, then sum. The CY2025 total is normalized to one.

`claim activity[q] = sum of corrected single-age claim exposures[q]`.

`claim share[cell,q] = corrected claim exposure[cell,q] / claim activity[q]`.

This reproduces the prior engine's normalized claim composition, while changing the total-activity adapter. It does not refit repair, value, TLF or fees. It also does not establish observed coverage or actual claim counts: the age propensity and cell corrections are fitted transfers, not separately measured insurance exposures. Migration across a bucket changes the assigned cell correction; this discontinuity is a modeling limitation, not a measured birthday effect. Annual snapshot interpolation smooths but does not empirically resolve it.

The fixed claim-frequency, routing and capture assumptions cancel in the same-quarter comparison used here. New coverage/frequency evidence would need an explicit additional driver and a clear population definition, rather than reusing fleet growth twice.

## How units and RPU are joined

For each quarter, cohort TLF is the claim-weighted average of cell total-loss probabilities. Conditional ASP and core RPU are weighted by total-loss counts, not fleet counts. The current assumed title/delivery contribution is then held fixed per sale.

`relative sold units = relative claim activity × relative TLF` under unchanged capture/routing/timing.

`insurance revenue ratio = relative sold units × relative all-in RPU`.

To explain the mixture, we first change total claim activity, then age-bucket shares while retaining prior-year body shares within each age bucket, then change body shares within each bucket. This exactly reconciles the final output. Attribution depends on the chosen order; it is not an independently estimated causal decomposition. The age and body factors each contain both selection-volume and conditional-fee effects.

## First result: the present inputs produce little net near-term fleet effect

FY27 H1 versus FY26 H1, USD millions, fixed carrier capture and unchanged ancillary adoption:

| Component | Service-revenue contribution |
|---|---:|
| Change in claim-weighted fleet activity | +1.894 |
| Change in age composition, at prior within-age body mix | +1.279 |
| Change in within-age body mix | −2.883 |
| Net | +0.290 |

The net is about +0.015% of prior H1 legacy service revenue of $1,943.896m. The old total-fleet activity convention produced +$1.635m in the otherwise comparable carrier-neutral calculation. The revised activity convention therefore changes the result, but does not reveal a large thesis by itself.

Quarterly net fleet contributions are approximately +$0.294m, −$0.005m, −$0.399m and −$0.747m for FY27Q1–Q4. These are conditional outputs, not adopted forecasts or consensus deltas. The slight later decline does not establish that fleet aging is about to reverse; multiple modeled effects offset each other.

## Why this still cannot establish the crossover thesis

The source snapshot has historical births for cars and aggregate light trucks. It then assigns **every light-truck vintage** the same split: approximately 72.39% SUV, 19.29% pickup, 8.32% minivan. All three use the same inherited light-truck survival schedule. Therefore:

- Changes in cars versus aggregate light trucks are represented.
- A historical shift from pickups/minivans toward crossovers within light trucks is not represented.
- Crossovers and other SUVs are not distinguished by separate repair/value economics.
- The fixed subtype shares originate in earlier listing-based assumptions; they are not historical new-vehicle sales shares.

This is consequential missing input structure, not a reason to enlarge the assumed negative effect. We cannot infer the economics of a distinct crossover transition from a model that holds its relevant birth mix fixed.

Two additional conventions are explicit: 2026 and 2027 new sales repeat 2025, and fiscal-quarter fleet states interpolate annual calendar-age snapshots. They are not observed monthly registration cohorts. Survival is fitted, not independently estimated for each birth vintage; imports, exports and other fleet movements are not separately reconciled here.

## Next data task and integration boundary

The next useful acquisition is a compact historical birth-mix table, not thousands of auction listings. Minimum fields: year, year basis (calendar sales/model-year production), vehicle classification, domestic-market scope, count or share, source, and status. Seek a coherent annual car/SUV-or-crossover/pickup/van series covering the cohorts now moving through ages 4–12; retain an explicit older-tail assumption if older years are unavailable.

An official production/type series could be a proxy if a consistent sales series is unavailable, but it must not silently be relabeled registrations or spliced into the existing births. First check whether its car/light-truck definition matches ours: a regulatory classification and a consumer body category are not necessarily the same. Validate category totals, avoid double-counting crossovers, and keep the original aggregate birth totals as a reconciliation control. The source's definition—not its label—determines the mapping.

After a small source/definition check, implement vintage-specific body shares, rerun survival and claims with frozen economic assumptions, and compare selected units and fees. Do not refit the damage parameters merely to obtain a larger revenue effect. If a new body classification requires new repair/value mappings, disclose that as a separate assumption before integration.

The current candidate is deliberately parallel to production. Adopting it requires updating the claim-activity interface and regenerating all dependent forecast/attribution files together; do not mix this cohort bridge with the previous carrier bridge as though they share the same activity convention. Source inputs, calculation provenance and all 33 reconciliation checks are retained.
