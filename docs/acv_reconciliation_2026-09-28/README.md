# ACV reconciliation and next model architecture

28 September 2026. Status: architecture decision and small arithmetic bridge, not an adopted forecast or revised Excel deliverable. User authorizes flexible treatment of the skeleton and asks to proceed with architecture; expensive experiments still require prior approval. Existing Excel files are preserved.

## Decision

Keep legacy Copart units/RPU economics intact. Add ACV as a separately forecast acquisition module, consolidated only after control transfers. Keep a legacy-only comparison to analysts that exclude the deal. Value the acquisition separately from legacy salvage until a supported combined cash-flow forecast exists. Do not goal-seek unsupported operating inputs just to make a stock price match.

The skeleton's $1.9bn cash deduction without an identifiable acquired operating asset undervalues the transaction case by construction relative to including that asset. Simply deleting the deduction is a diagnostic, not a complete transaction valuation. The approximately 4% implied growth result is not an independently measured market expectation.

## Evidence actually checked

1. Copart announcement, September 10: $10.50/share, approximately $1.9bn equity consideration, cash financing, expected calendar-year-end 2026 close, independent subsidiary. Expected first-full-year EPS neutrality and FY28 accretion are management statements, not our calculations. https://www.sec.gov/Archives/edgar/data/900075/000119312526388064/d138322dex991.htm
2. ACV Schedule 14D-9, September 17, accession 0001193125-26-393862: local `raw/sec/acv/sc14d9_2026-09-17.txt`, lines 973–1060, independently reread against existing extracted table `data/csv/acv_14d9_projections.csv`. https://www.sec.gov/Archives/edgar/data/1637873/000119312526393862/d136775dsc14d9.htm
3. Existing September 11 broker reports, local searchable extracts in `/Users/kwu/Documents/ChatGPT/HFAC x Citadel/research/cprt_discovery_plan_2026-09-26/sources/`: Barclays file ending 124339246, lines 104–109; JPMorgan ending 124345098, lines 37–40; BNP ending 124357601, lines 280–287. All explicitly exclude ACV. BNP explicitly excludes P&L, balance sheet and cash-flow effects. These are dated broker observations, not proof of the September 28 CapIQ contributor universe. Full licensed reports are not copied into Git.
4. CapIQ export reviewed previously: FY27 total revenue quarter sum $4,860.97m; no contributor-level deal flags or dates. FY28 $5,191.75m from only two contributors. Do not infer acquisition inclusion from low growth alone.

ACV management standalone projections, calendar years, $m:

| Metric | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---:|---:|---:|---:|---:|
| Revenue |857|964|1,116|1,322|1,525|
| Adjusted EBITDA excluding SBC |78|123|187|283|382|
| Adjusted EBIT including SBC |-15|20|73|152|244|
| Source-defined unlevered FCF |unavailable|-97|-69|-8|37|

These are management projections prepared for the sale process, not audited results, consensus or adopted assumptions. Source-defined FCF retains SBC as an economic expense; do not mix it silently with the skeleton's SBC-addback convention. Adjusted EBITDA cannot be inserted into Copart's EBITDA without an adjustment bridge. ACV floorplan receivables, related funding, restricted cash and capitalized software need specific classification before constructing enterprise value or FCF independently.

Corrections to earlier E10 interpretation: $1.9bn divided by EBITDA is equity consideration/EBITDA, not EV/EBITDA without a net-debt adjustment. Negative standalone FCF does not prove value destruction. Calendar-year standalone EBIT versus annual foregone interest does not establish fiscal-year GAAP EPS dilution without closing dates, acquisition accounting, financing, tax and synergies. Preserve E10 as historical work; this note supersedes those stronger conclusions.

## Cheap fiscal-period bridge implemented

`model/linked_service_revenue_2026-09-28/acquisition_bridge.py` reads the existing projections and writes `acquisition_timing.csv` and `calculations.json`. No web scrape, OCR, paid data or simulation. Uses first consolidated months November 2026, January 2027 and April 2027 as timing scenarios. January is a convenient scenario consistent with the announced year-end target, not a confirmed close date.

Monthly amounts equal calendar-year amounts divided by 12. This is provisional timing allocation, not measured seasonality. It must later be replaced with historical calendar-quarter patterns if material. No forward growth beyond disclosed CY2030 is invented.

January 2027 scenario: CPRT FY27Q1 $0, Q2 $80.33m, Q3 $241m, Q4 $241m of acquired revenue; FY27 $562.33m, FY28 $1,052.67m. Q2 is November–January, hence one acquired month. FY28 combines five CY27 months and seven CY28 months. The deal creates a FY28 comparison effect even with unchanged standalone expectations.

If every CapIQ contributor excludes ACV, adding this illustrative FY27 contribution gives $5,423.30m. This is a scope bridge, NOT updated consensus and NOT alpha. Contributor-level confirmation is missing. Never compare acquisition-inclusive model growth with acquisition-exclusive consensus and claim an operating beat. Missing CY26 FCF stays unavailable in the November-close scenario rather than becoming zero.

## Valuation treatment

Use a consistent valuation date and reference share price. The skeleton's $29.95 is a historical reference, not a refreshed quote. First reconcile the July balance sheet to the valuation date; do not mix pre-close cash with post-close cash deductions.

Before close, conditional transaction equity value = legacy operating EV + legacy non-operating net assets + PV(at closing: ACV acquired equity value minus equity consideration minus transaction costs) + PV(net incremental synergies). ACV acquired equity value means ACV operating EV plus eligible cash less debt/other claims; use one consistent convention for its floorplan financing. Costs and cash flows must not appear twice. If using a consolidated operating DCF instead, do not also add a separate ACV value.

After close, use consolidated net cash/debt and operating values; do not subtract consideration again. In a probability-weighted analysis, value close and no-close scenarios separately before weighting; do not probability-weight reported revenue for a single realized scenario. No numerical closing probability is assigned here.

Foregone interest belongs in an EPS or cash-interest schedule, not as a second deduction from unlevered enterprise FCF after purchase consideration has already been included. Similarly, do not add future accumulated operating cash on top of its discounted FCF value. Buybacks affect cash and share count consistently; they are not an additional enterprise-value benefit.

For now, display ACV net value creation as an explicit unresolved variable: PV(acquired equity value minus purchase price, deal costs, plus synergies). A zero net-value-creation reference means asset value equals consideration before costs; it is a calibration convention, not validation of price. Do not grant the acquired asset zero value. Do not extrapolate the public projections to 2036 to reproduce the fairness opinion: the later forecasts used there are undisclosed. The disclosed fairness range is context, not an independently reproduced DCF.

Separate legacy and ACV terminal assumptions. Resolve SBC convention across both businesses. Discount terminal value at the chosen exit date, separately from annual cash-flow midpoints. Reverse solve one named legacy driver at a time with ACV and other valuation assumptions fixed; show which driver was solved. Do not treat one flat consolidated CAGR as evidence about insurer units or RPU.

## Revenue architecture and connections

Keep four main views: RPM Summary; Volume Build; Vehicle Economics; Revenue Bridge. Add one supporting Acquisition Build with its source block; do not spread the acquisition across unrelated tabs. Detailed cohort calculations remain in existing supporting engines. Valuation stays a separate consuming module, not a source of operating assumptions.

1. Source and period layer: every observation has period, region, carrier/body/age where relevant, metric definition, currency, gross/net basis, reported versus proxy versus assumption status, and source. One fiscal calendar maps all inputs. ACV Auctions is labelled by name; pre-loss actual cash value uses `vehicle ACV` to avoid ambiguity.
2. US insurance exposure: carrier insured vehicle-years × claims frequency, with physical-damage coverage included only when exposure is not already covered exposure. Premium share is a proxy, not vehicle share. Preserve carrier-specific ages/body mix where evidence supports it; do not add overlapping frequency or coverage adjustments.
3. Joint damage selection: distribute claims across age/body/damage states. Compare repair cost with vehicle ACV less expected net salvage, subject to legal/operational rules. Use the same selected population to calculate total-loss counts and auction-value distributions. Keep repair severity selection distinct from fleet mix. Higher damage does not automatically mean higher ASP.
4. Routing and allocation: total losses × commercial-auction eligibility × carrier-specific Copart allocation. Friend's share build supplies allocation paths; our exposure and damage engine supplies the weights. Do not apply its already-weighted aggregate share change a second time. Record whether ramps describe assignments or completed sales.
5. Inventory timing: opening inventory + assignments − sold units = ending inventory, by origin cohort when material. Carry cohort economics through the lag, rather than pricing old inventory as new assignments. Separately flag catastrophes; do not use lag assumptions to force a quarterly revenue tie.
6. Legacy RPU: for sold states, expected buyer fee from price brackets and buyer mix + contracted seller economics + service uptake × service price. Different services may have different denominators and recognition timing. Title-handling activity is not automatically same-quarter recognized revenue. Registration and other non-unit fees remain separate. Show mix, posted-price and adoption contributions separately.
7. Other legacy branches: US non-insurance and international get explicit activity × fee schedules; purchased vehicles get units × gross sale price in a separate revenue category. Their coarse assumptions remain visible; do not call activity equivalents measured unit counts. Branches must add to reported historical totals without a forecast residual-growth plug.
8. ACV branch: dealer/commercial auction transactions × net auction fees; transportation transactions × external transport fee; financing activity × yield/fees with separate receivables/funding; assurance activity × fee; subscriptions/data accounts × ARPU. These are proposed driver definitions, not all sourced inputs. Until the pieces are sourced, the management total remains a transparent projection with an unallocated detail line, not invented bottom-up precision. Gate by closing date and distinguish reported presentation from managerial categories.
9. Consolidation: legacy service revenue + eligible acquired service revenue − intercompany service eliminations; purchased-vehicle sales and any differently classified acquired revenue remain separately identified. Total consolidated revenue adds all categories once. ACV gross merchandise value is not revenue. Revenue synergies count only incremental external revenue, not internal transportation billings. Cost synergies do not raise revenue.
10. Comparison and valuation: summary shows legacy organic service growth, acquired contribution, and consolidated revenue on separate rows. Compare each against matching analyst scope. Valuation consumes annual sums and explicit longer-term drivers; it cannot feed back into the revenue engines unless a clearly labelled reverse-solve diagnostic is selected.

## Next implementation order

First fix historical definition/scale: reconcile reported service revenue by geography with modeled units/fees, resolve the current assumed 90% US insurance dollar split and four-quarter residuals. Existing FY26Q4 calibration is not an independent validation; absolute units and fees are not jointly identified by revenue alone.

Second make the carrier integration explicit: common period definitions, exposure weights, claim and total-loss weights, assignment versus sale basis. Freeze an allocation path, then run a small test proving that a carrier mix change affects both units and RPU once.

Third replace illustrative title/delivery inputs with bounded sourced evidence; calibrate residual core/service components transparently. Then improve cohort inventory timing. Test a repair-cost perturbation jointly through totals, selected prices, fees and revenue, rather than separate unrelated volume/RPU shocks.

Fourth promote this acquisition timing bridge into Excel when updating the operating workbook, after service classification is checked. Use broker flags to compare legacy-only projections now; leave aggregate CapIQ scope unresolved until a contributor export confirms it. A targeted export is cheaper and more precise than inferring scope from topline growth.

Finally connect the stable quarterly output to a revised valuation consumer, with separate terminal economics and net acquisition value. Do not publish a new precise price target before this input work. No large collection exercise is necessary for these steps; any proposed large scrape, OCR or paid dataset requires a separate cost/method proposal.

## Acceptance checks

Pre-close acquired revenue is zero; full-year sums match mapped calendar projections; delayed close shifts recognized amounts without changing the standalone source plan; missing CY26 FCF propagates as unavailable; intercompany elimination cannot exceed identified internal revenue; no consideration double count; no lost-interest double count; no goodwill amortization in cash FCF; no blanket legacy margin applied to acquired sales; all forecast revenue branches sum exactly; units/RPU changes reconcile with their interaction; no future growth plug hides historical residuals.

Completed in this pass: source recheck, three broker scope confirmations, fiscal mapping scenarios and small checks, architecture and valuation contract. Not completed: independent ACV fair value, contributor-by-contributor CapIQ mapping, verified close date, or updated Excel. These remain explicit rather than silently assumed.
