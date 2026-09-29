# Repair economics and salvage demand: prior-work inventory and next plan

**Executed bounded follow-through:** [evidence, offset calculations and quarterly timing results](repair_salvage_execution_2026-09-28/README.md). New provider schemas did not clear the accepted-sale/claims-threshold gates; no expensive collection or empirical forecast coefficient was adopted.

28 September 2026. User requested an end-to-end plan and explicitly required checking prior work first. This pass reviewed relevant research indexes, methods/results and source audits; it did not reread every raw document, collect new evidence or run new experiments. No new forecast is adopted.

## What exists and how it constrains the plan

| Existing work | Reuse | Remaining limitation / avoid repeating |
|---|---|---|
| [Repair source map](repair_research_2026-09-26/repair_pilot/repair_cost_source_map.md) | Already maps 14 source families, including repairers, OEMs, specialist services, suppliers, public fleets and regulators | No need to rediscover the same generic list; test a specific missing field |
| [Repair pilot index](repair_research_2026-09-26/README.md), controlled AAA scenarios, matched older-model parts, alternative-parts checks | Operation definitions and scope/sourcing comparisons | Price/finish/date/vendor differences can reverse a body premium; estimates/list prices are not allowed or paid repair bills |
| [Frequency feasibility](repair_research_2026-09-26/repair_frequency_feasibility/README.md) and historical Mitchell weights | Age/body/impact organization; documented population distinctions | CRSS crashes are not insurer operations; overlapping marginal part incidences are not mutually exclusive bundles |
| [Historical repair distributions](repair_research_2026-09-26/repair_cost_reference/README.md) | Preserved histograms and modern benchmark checks | New-sedan repairable-only distributions cannot identify latent costs of already-totaled vehicles |
| [Value/recovery audit](repair_research_2026-09-26/value_recovery_audit/README.md) and [auction pilot](repair_research_2026-09-26/auction_recovery_pilot/README.md) | Known candidate records and rejection reasons | Seven VIN candidates, two secondary-corroborated pairs, no primary-settlement-verified pair; local listing DB lacks ACV and accepted proceeds. Do not scale that convenience sample or reuse highest bids as sales |
| [Age-constrained engine](fleet_selection_2026-09-28/AGE_CONSTRAINED_ENGINE.md) | Selected age values, repaired means and age TLF constraints | Targets now used in calibration are not independent validation; mixed populations, older-age shape and damage/recovery dependence remain assumptions |
| [Age decomposition](fleet_selection_2026-09-28/AGE_VERSUS_WITHIN_BUCKET.md) and [claims check](claims_discovery_2026-09-28/COUNT_COMPATIBILITY.md) | Within-age change and denominator diagnostics | Age mix does not explain all rate change; published claims/valuation series do not reconcile as one population |
| [Revised architecture](../model/revenue_architecture_2026-09-28/README.md) and [RPU downside tests](rpu_downside_test_2026-09-28/README.md) | Separate expected/realized salvage, units/fees, services and timing; numerical scenario machinery | Structural coverage is not empirical identification; the repair-response derivative and physical timing remain unmeasured |
| [Supplier/repairer evidence](../model/revenue_architecture_2026-09-28/EVIDENCE_UPDATE.md) | Existing LKQ/Boyd disclosures provide concrete source leads | Alternative-parts utilization/repairer growth are not fixed-scope cost deflation or salvage-bid measurements |

## Precise target

For comparable vehicle and damage cohorts, measure changes in (C) insurer-expected complete repair cost, (V) pre-loss value, (S_e) expected net salvage recovery, and (S_r) realized gross auction proceeds. Match period, estimate version, geography, coverage and disposition. Define the simplified economic decision margin D=C−V+S_e; larger D makes totaling more attractive, holding other decision criteria fixed. This is an economic screen, not a universal legal settlement rule. Record applicable threshold/workflow constraints and other decision costs before using it as a disposition classifier.

Two missing objects have different evidence requirements: changing repair and recovery dollars determine ΔD; the population of claims near D=0 determines how many switch. Auction-only samples can help measure S_r but cannot supply the missing repaired claims or identify the switching population.

## Stage 1 — Resolve field availability, not more generic facts

Do one bounded discovery pass (initially 4–6 targeted queries) from the existing map. Prioritize:

1. Insurer/estimating workflow reports: anticipated salvage, anticipated supplements, repair-to-total conversion and threshold bins. Start with saved CCC/ Mitchell documentation leads and check actual export/report fields. Best potential direct link; access unconfirmed.
2. Repairer/parts procurement: original and revised estimate, part-source substitutions, labor/calibration lines, approved final scope, quote/order dates. Start with saved sources; target PartsTrader/OEC, repair groups or public fleet collision packets only where an identifiable field exists. A fleet record can demonstrate a mechanism but not insurer-wide prevalence.
3. Dismantler economics: donor acquisition cost, realized parts revenue, sell-through, inventory aging, dismantling/freight costs and procurement volume. Start with LKQ and recycler/trade disclosures. Separate recycled collision parts from aftermarket products; company mix and purchasing changes may contaminate averages.
4. Rebuilder/exporter economics: destination resale receipts, local repair expense, freight/duties, exchange rates, eligibility restrictions and purchase bids. Prefer dated operational/customs/port sources; classify salvage/whole-car and destination where possible. Export volumes alone cannot identify willingness to pay.
5. Auction channels: accepted proceeds, reserve/no-sale status, relistings, sale date, vehicle specifications and condition. Revisit old sources only if a specific new field/access route changes the earlier feasibility result.

Illustrative query vocabulary: `anticipated salvage repair total threshold report`; `collision repair alternative parts quoted accepted cost trend`; `recycled parts salvage vehicle acquisition cost sell through`; `salvage rebuild landed cost export bids`. Actual queries and results must be logged when executed; these are planned, not completed searches.

Public structured tables/text layers first, small relevant excerpts from licensed documents second; no bulk OCR or speculative full-library search. Output one field-access table recording availability, source independence, population, date, missingness and use status. If no new usable field appears, stop that route. No external outreach without explicit authorization.

## Stage 2 — Build comparable changes with a small pilot

Choose at most two cohorts already represented in the saved work (e.g. Camry and RAV4 of compatible model years), adding a pickup only if its data availability is comparable. Choose damage/operation strata based on accessible records, not which show the largest effect. Examine roughly 10–20 documents/records as a feasibility pilot, retaining every attempted record and exclusion; this is not a representative sample or an elasticity estimate.

Repair panel fields: model/year/equipment, damage scope, estimate date/region/stage, parts source and price, quantity, operation/hours/rate, calibration, supplements, approval/payment status and disposition. Separate identical-operation inflation, sourcing substitution and scope changes. If historical identical items are unavailable, do not call cross-sectional alternatives a time trend. Include quotes/estimates for cases later totaled where available; final paid repairs alone are selected.

Auction panel fields: VIN/lot/event identifiers, model/year/mileage/trim, damage/run status, title, seller channel, listing and sale dates, attempts/no-sales, accepted gross proceeds, fees and separately sourced pre-loss value. Sample by date/cohort rather than search terms requiring visible prices. Keep unmatched and missing-price records; repeated VINs follow one event history. Do not treat relisting as another sold unit. Matching observable condition only reduces, not eliminates, damage/selection bias.

This pilot tests schema and comparability. Broad regressions or a bulk scrape before this stage would add precision to potentially misdefined variables. If an accessible aggregate report already supplies comparable fixed-cohort outcomes, prefer it to individual records.

## Stage 3 — Test mechanisms jointly

For matched cohorts, calculate ΔD=ΔC−ΔV+ΔS_e in dollars. A hypothetical $300 repair saving offset by $300 greater net salvage leaves D unchanged at fixed V. Meanwhile higher S_r can still raise fees. This directly tests the recycling loop: cheaper substitute parts can reduce repair cost, while demand for recycled parts may support donor-auction bids. New aftermarket supply need not have the same donor-demand effect.

Distinguish competing explanations: genuine fixed-scope repair relief; expensive jobs exiting the repaired population; weaker salvage demand; better parts sell-through supporting bids; richer sold-vehicle mix; changed auction supply/reserves. Require separate measurement of expected versus realized recovery and preserve any update lag. Scrap metals are a separate low-value buyer channel; their index must not reprice rebuildable crossovers indiscriminately.

For each candidate cause specify disconfirming observations. Examples: parts prices fall but labor/supplements erase the saving; procurement costs fall only because cheaper donors were purchased; reported ASP changes disappear after cohort matching; bids weaken but reserves rise and sold-only ASP remains high. No causal coefficient comes from aggregate correlation alone.

## Stage 4 — Constrain switching mass

First seek existing aggregate counts by cost gap/repair-to-value band with repaired and totaled dispositions and consistent expected salvage. These can be cheaper and more informative than thousands of detailed invoices. If access to paired pre-disposition records exists, calculate D consistently and count claims close enough to the measured ΔD to switch, accounting for incomplete estimates and rule overrides. Include current total losses as well as repairs; supplier/auction samples alone cannot identify this.

If direct bands are unavailable, a narrow historical holdout with compatible joint C/V/S measures and cohort outcomes can challenge the engine. It cannot establish causation if coverage, damage, carrier or reporting mix shifts simultaneously. Keep current derivative explicitly assumed if the evidence cannot constrain it; do not rerun the old exact calibration and rename it validation. If only directional inputs are defensible, report directional or bounded outcomes rather than a precise unit forecast.

## Stage 5 — Translate into quarterly Copart revenue and test expectations

Freeze historical calibration. Run reference, repair-only, salvage-only and joint cases with the same exposure/carrier/service assumptions. Preserve interactions rather than adding isolated percentages. Expected recovery changes selection; realized proceeds feed the posted buyer-fee bands and seller terms on that selected population. Do not apply an ASP shock twice through both mix and an aggregate overlay.

Map decision dates to assignments and completed sales using observed lags if obtainable. Otherwise show explicit timing cases; no default instant unit effect presented as evidence. Label FY27Q1 versus later-quarter effects. Separate insurance from all-US and purchased/ACV business. Produce quarter-specific units, selected ASP, core RPU, service contribution and service revenue, then compare like-for-like named forecasts. Forecast divergence is not automatically a stock-price return.

## Combined rationale and spending gate

The sequence first asks whether a mechanism exists, then whether it is changing, then whether enough claims can switch, and finally whether it reaches earnings within the pitch horizon. Do not optimize public-listing collection if the decisive missing observation is a pre-disposition claims histogram. Do not keep refining repair baskets if matched prices show negligible changes. Conversely, strong realized-price evidence may support an RPU forecast even while the unit response stays bounded.

Only the inventory and plan were completed in this turn. Next authorized routine scope is a bounded field-availability pass; large record collection, extensive fitting, paid access or OCR requires a separate proposal describing schema, sample frame, expected information gain, uncertainty in cost, cheaper alternatives and stopping rule. No precise token estimate is asserted. The deliverable is an evidence ledger and model-admission decision, not another large narrative report.
