# Revised Copart architecture: implementation and thesis triage

**29 September pitch audit:** [PM review of both competition theses and the 12-month catalyst](../../docs/pitch_audit_2026-09-29/README.md). Retain the scenario architecture; a combined forecast and catalyst-backed short remain unvalidated. The review flags adoption timing, dated carrier terms, benchmark materiality and the required evidence before adopting a pitch case.

**CCC data update:** [New age/body calibration and connected revenue scenarios](../ccc_age_body_2026-09-29/README.md) incorporate the user-supplied September 29 workbook. Original scenarios below remain the prior comparison; do not mix their reference with the new outputs.

**29 September follow-up:** [Aftermarket source-to-revenue bridge](../aftermarket_bridge_2026-09-29/README.md) adds explicit OEM/recycled substitution, donor economics, competing bids, feedback and a materiality hurdle. Existing history and scenarios are unchanged. Material joint downside is conditional; new causal coefficients remain unvalidated.

**Revenue-only audit and Fable handoff:** [Audit](../../docs/model_audit_2026-09-29/AUDIT.md) and [implementation contract](../../docs/model_audit_2026-09-29/FABLE_HANDOFF.md). Reproduce with `python3 model/revenue_architecture_2026-09-28/run.py --reuse-saved-evidence` when the licensed source report is unavailable. This preserves the dated benchmark; it does not refresh evidence.

28 September 2026. Working analytical successor to the integrated prototype. No Excel design, legacy-output overwrite, paid collection or expensive fitting. **Most of the structural defects identified in the audit now have executable implementations and guards. The evidence gaps are not all solved, and there is still no independently validated point forecast.**

## What changed

| Audit requirement | Implemented result | Remaining limitation |
|---|---|---|
| Consistent historical/consensus scope | `benchmark_perimeter.csv`, sourced history and independently extracted JPM quarterly totals plus annual service forecast | CapIQ contributor acquisition treatment and quarterly service split unavailable |
| Complete base revenue ledger | Insurance core, title, delivery, other-US and international sum to reported history; alternate splits expose non-identification | Component amounts and absolute insurance units still conditional; a fit is not observed disaggregation |
| Compatible claims and selection | Existing cohort calibration retained; explicit combined claims convention, paired nonfiling, routing and CAT scenario inputs | Near-threshold response and coverage/filing separation unmeasured; CAT common-economics scenario is coarse |
| Carrier effects on economics | Carrier terms and conditional carrier-by-cohort weights feed selection, prices and fees; tests confirm allocation can now change RPU when economics differ | New carrier distributions/contracts not observed; default remains common economics and quote-model runoff is a separate case |
| Expected versus realized salvage | Independent drivers allow decision-stage response and sale-price-only effects; joint scenarios rerun selection and prices consistently | Damage/recovery rank relationship and its derivative remain assumed |
| Sale timing and backlog | Conservation-based flows, withdrawals, explicit opening backlog, title/no-title delay kernels, and assignment-vintage fee matrix | Defaults stay sale-equivalent; measured opening inventory/lag/vintage prices absent. Missing inputs reject physical timing rather than inventing them |
| Fee vintages and buyer/seller mix | Per-quarter schedule selection, registered source provenance, buyer mix, seller terms and fixed fees | Only one verified selected schedule snapshot; its historical application remains a proxy, not verified dated history |
| Independent service activities | Sale/assignment/external eligibility, adoption, prices, waivers, bundling and separate recognition delays; title adoption can affect timing when explicit kernels are supplied | Undisclosed product levels/fees; gross/net supplied explicitly, not resolved by the engine |
| Other branches and acquisition | Explicit activity/fee/FX scenarios; currency double-count guard; acquired-service/total classification and pre-control gates | Extrapolations are assumptions, other-US fee population remains incomplete, ACV scope not settled |
| Thesis attribution | 15 complete quarterly cases, named benchmark comparisons, uniform-driver hurdles and four-case interaction | Scenarios are not probability distributions or investment forecasts |

### How the level problem is handled

Historical total revenue is observed; internal component allocation is not. The ledger starts with the inherited insurance share and core/title/delivery fee assumptions, shows the implied components and counts, and separately runs an 80% insurance-share case. Both allocations reconcile; neither is called measured. The 80/90% cases are illustrative assumptions, not confidence bounds. A forward adoption/price change does not recalibrate historical units. Changing the historical split explicitly creates a new base case.

Other-US and international now use relative activity/fee factors rather than presenting arbitrary $500/$750 activity equivalents as physical units. All comparison outputs identify legacy services, purchased revenue and the unknown acquisition overlay separately. The original failed absolute historical reconstruction is preserved in the old directory; the new ledger has not independently cured that empirical failure.

### How timing is handled

The default uses the inherited sale-equivalent convention. Physical assignment mode requires explicit opening releases, sale probabilities, and fee economics for opening and incoming vintages. Title adoption can mix separately supplied title/no-title delay distributions. A synthetic hand-calculated test verifies that acceleration changes quarterly sales but not lifetime sales or fees. Those test inputs are not company estimates. Do not confuse unsold backlog with sold cars awaiting pickup.

Service-event recognition has its own inventory of unrecognized event revenue. Separate jobs can generate revenue even when current auction sales differ. Title/delivery prices remain contract assumptions; selecting `net` requires entering the actual net revenue charge, not merely changing a label. Services bundled in core seller fees cannot add a second charge.

## What the repaired comparisons show

JPM September 11 explicitly excludes ACV and forecasts FY27 service revenue of **$4,061m**, about **2.30% growth**, alongside $721m purchased sales and $4,782m total revenue. Its quarterly totals sum to $4,783m because of rounding. CapIQ September 28 quarter means sum to $4,860.97m and have an unverified acquisition perimeter. See `EVIDENCE_UPDATE.md` for exact source rows and limitations.

The following are conditional cases, with allocation held neutral year-over-year, purchased revenue flat, other-US activity/fees flat, and title/delivery adoption and pricing unchanged unless stated. International continuation carries forward Q4's derived fee-unit growth and 3.5% reported-currency RPU; it is not guidance. Auction-price continuation shifts realized prices uniformly at fixed decision-stage salvage assumptions, deliberately isolating fee pass-through rather than forecasting the full demand equilibrium.

| H1 FY27, $m | Legacy service | Comparable legacy total | Gap to CapIQ total, conditional on ACV exclusion |
|---|---:|---:|---:|
| Flat other branches and economic drivers; fleet roll only | 1,943.35 | 2,276.16 | -73.87 |
| Add international continuation | 1,984.95 | 2,317.76 | -32.27 |
| Also assume +3.7% realized insurance auction prices | 2,009.12 | 2,341.93 | -8.10 |
| Instead assume +6% realized insurance auction prices | 2,023.96 | 2,356.76 | +6.73 |

The +3.7% price case is about 0.34% below CapIQ H1 and $15.93m above JPM's dated H1 total. Its FY27 services are $44.80m above JPM's annual service forecast. Applying JPM's annual purchased-sales growth proportionally to the comparison overlay moves the H1 CapIQ difference to +$3.51m; that proportional quarterly allocation is not a disclosed JPM forecast. A +/-5% other-US activity case changes H1 by +/-$8.38m. The small residual gap is therefore not robust alpha.

The international assumption alone contributes $41.60m to H1, larger than the price-only change between 6% and 3.7% auction-price growth ($14.83m). The prior large downside depended heavily on carrier allocation and unfinished flat branches. This is a result of exposing the model's assumptions, not proof of either a long or short.

With flat insurance units, the conditional all-in insurance-RPU growth needed to meet CapIQ falls from 4.86% with all other branches flat to 2.11% with international continuation. Against JPM's H1 total, the corresponding hurdle falls from 3.27% to 0.51%. These are requirements under assumptions, not the analysts' disclosed RPU forecasts.

## Two thesis directions to prioritize

### 1. The composition of RPU growth and the durability of its offsets

**Research proposition:** how much apparent fee strength is repeatable core transaction pricing, versus vehicle-price mix, new services and international growth? The differentiated claim would be that the specific offsets assumed by a named forecast cannot persist at the required rate—not simply that ASP growth is slowing.

The revised model can separately change prices, fee schedules, buyer/seller mix, service events and international activity. Existing fee schedules give a concrete mechanism: ASP growth does not translate one-for-one into fee growth. Our 6% versus 3.7% price-only comparison changes H1 revenue by $14.83m, only about 0.63% of CapIQ H1 total, with the same other assumptions. A 10% relative increase in assumed title/delivery adoption adds about $9.13m; that number relies on unmeasured product bases. Neither alone establishes a large short.

**Why prioritize:** comparatively accessible operating disclosures and posted fees; direct quarterly tests; less dependence on the unvalidated repair-selection derivative. The thesis may become long if services/international genuinely exceed the required offsets.

**Decisive next evidence:** a named broker's geography/fee-unit/RPU forecast, a compatible US fee-vehicle price/mix observation, and a numerical service growth contribution where available. A narrow analyst-table export is more useful than a large listing scrape. Fail the short if ordinary, supported offsets meet the benchmark. Do not call an unexplained historical RPU residual Title Express adoption.

### 2. Repair-versus-salvage economics at the marginal total-loss decision

**Research proposition:** cheaper alternative repair options or changing salvage recovery alter which vehicles reach auction; the change in supply and selected fees can outweigh ordinary ASP growth. The relevant object is repair cost relative to pre-loss value minus expected net salvage, not the average repaired claim bill or a static truck premium alone.

New practitioner evidence makes this worth focused investigation: LKQ describes high alternative-parts use and recovering repair activity, while Boyd describes repairable-claim stabilization with limited TCOR growth. Neither establishes a comparable-job cost decline; increasing recycled-parts demand might also support salvage proceeds and make totaling more attractive. Both channels must be tested.

Illustrative engine cases around the +3.7%-price/international-continuation reference: repair costs -3% changes H1 services by -$64.97m; expected salvage +3% changes them by +$20.87m; together the change is -$44.82m, including a -$0.73m interaction. The combined scenario is $52.92m below CapIQ H1, conditional on the comparison scope. **These are not forecast coefficients or validated downside.** The current damage distribution creates the marginal response, which remains empirically unidentified. The demonstrated possibility of a material effect is why the evidence is valuable; it is not the evidence itself.

**Decisive next evidence:** compatible fixed-damage repair basket costs and expected net salvage, or an aggregate repair-versus-total cost-gap histogram with dispositions. Repairers, parts suppliers and estimating workflows are useful because they observe different sides of this decision. Auction-only samples cannot identify the vehicles that were repaired instead. A new collection should proceed only if its schema can constrain this response; prior searches did not establish access. A better average repair premium alone would not resolve the local switching mass.

Weakening salvage demand on both decision and sale sides remains an alternative scenario (-$40.40m H1 for the illustrative paired 3% reduction), not a selected thesis: the new supplier evidence does not establish such weakening. Ordinary fleet aging/body turnover remains in the foundation, but current bounded tests do not support prioritizing further subtype detail as a large six-month catalyst.

## Remaining gates and what is genuinely finished

The code now represents the audited relationships and refuses several invalid shortcuts. It does not manufacture the missing evidence. Still unresolved: absolute insurance units/component shares; contract fees and service adoption levels; historical fee vintages; physical lag/opening backlog; the marginal damage-selection response; and CapIQ's acquisition perimeter. These are explicit data/identification limits, not hidden growth lines. No stock-price alpha percentage is inferred from a revenue gap.

**43 meaningful checks pass:** saved legacy neutral/runoff parity, level non-identification, price-only versus selection shocks, equal repair/value scaling, nonfiling neutrality, heterogeneous carrier RPU response, service/auction separation, inventory conservation and title timing, recognition delays, waivers/bundling, currency double counting, unknown fee vintage, core units × fees, and acquisition timing/classification gates. Arithmetic validation is not predictive validation. No new historical out-of-sample claim is made.

## Files and handoff

- `benchmark_perimeter.csv`, `historical_metric_controls.csv`: dated historical/analyst controls, missing values preserved.
- `base_component_ledger.csv`: conditional starting allocations and inferred counts.
- `quarterly_scenarios.csv`, `scenario_summary.csv`: separate complete cases, not a single selected forecast.
- `hurdles.csv`, `interaction.json`: conditional benchmark requirements and exact interaction accounting.
- `scenario_configs.json`: each input case; `fee_schedule_registry.json`: observed snapshot and unknown effective date.
- `evidence_manifest.json`, `manifest.json`, `tests.json`: sources, hashes, extraction and checks.
- `model.py`, `run.py`, `test_model.py`, `evidence.py`: reproducible local calculations. Run the test script, then run.py. No spreadsheet dependencies.

Fable should retain the approved RPM Summary / Volume Build / Vehicle Economics / Revenue Bridge organization. Display separate scenario columns and evidence status, keep reported history distinct from allocated components, and do not label the most bearish case the forecast. Acquisition-null outputs remain unavailable. Start the next data pass with the three narrow fields for direction 1; pursue direction 2 only when a concrete source can constrain the marginal decision, with approval before expensive collection.
