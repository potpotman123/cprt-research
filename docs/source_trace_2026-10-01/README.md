# Source trace: every number in the revenue architecture, 1 October 2026

70 inputs registered in `trace_register.csv` (regenerate with `python3 scripts/source_trace.py`). Labels: ASSUMED 28, CALIBRATED 4, ENGINE 1, FITTED 7, MEASURED 4, UNVERIFIED 9, VERIFIED 14, VERIFIED (historical) 1, VERIFIED (trend) 1, VERIFIED endpoints 1. Flags: NO SOURCE 22, OK 30, WEAK ANCHOR 18.

A number is traceable when a file in this repository, a page saved to disk, or a licensed report held locally can be put next to it. A number flagged NO SOURCE cannot be defended that way today; it must either be sourced before the build or appear in the workbook only as a labelled sensitivity, never inside a base case.

## Numbers with no source today (22)

| Engine | Parameter | Value | What would close it |
|---|---|---|---|
| E1 Fleet | Vehicles in operation anchor, 2024 | 289M | Replace with the Experian on-disk figure and cite its file; or fetch S&P press release and cite |
| E1 Fleet | Share of fleet aged 7+ years, 2024 | 66% | Fetch the S&P Global Mobility 2024 average-age release (robots permitting) or drop this anchor and fit to counts only |
| E1 Fleet | Expert hard-constraint fleet by age and type | TBD | Download to raw/reference/ and add a Checks row comparing the roll to each constraint cell |
| E2 Claims | Claims multiplier | 1.0 (0.98 stress) | Keep 1.0; present 0.98 only as a labelled stress or drop it |
| E2 Claims | Routing fraction to insurance auction channel | 1.0 | 10-K: LKQ and dismantlers may buy directly from insurers; keep 1.0 as convention with a sensitivity row |
| E3 Carriers | Baseline Copart allocation by carrier | SF .50, PGR .25->.05, GEICO .83->.90, Allstate .95, USAA .95, Farmers .90, Liberty .70, Travelers .85, Nationwide .95, Other .50 | Public anchors only: FQ4 FY26 -7.5% units with assignments +2.3% ex one customer (VERIFIED, call) and listed-inventory split 57.2% (MEASURED, 4 nights). Present allocations as a labelled scenario with the quote bank cited row by row |
| E3 Carriers | GEICO allocation event probability | 60% | Show as red toggle default OFF in A-only case; realised-case view beside expected value |
| E3 Carriers | State Farm adverse event probability | 45% | Same treatment as GEICO |
| E3 Carriers | Other-carrier allocation loss | -5 pts at 45% | Keep off by default; needs an affected-exposure denominator |
| E4 Aftermarket | Donor contribution exposed fraction | 25% | Recycler donor-cohort report (Bidmate route) or keep as sensitivity |
| E4 Aftermarket | Recycler price transmission weight | 50% | Sensitivity 10-50%; the 10% case removes most of the price effect (AUDIT.md) |
| E4 Aftermarket | Rebuilder repair-bill-to-bid ratio | 1.0 | Sensitivity |
| E4 Aftermarket | Repair-job recapture | 1.0 | Sensitivity 0-1 |
| E4 Aftermarket | Supply price response (donor scarcity) | 0.25 | Sensitivity |
| E4 Aftermarket | Expected salvage pass-through | 1.0 | 0/0.5/1 cases exist; keep visible |
| E4 Aftermarket | Threshold-responsive claim fraction | 1.0 | 0/50/100% structural cases |
| E3 Carriers | Probability-weighted moves (memo basis) | SF -5 pts x 45%; Other -5 pts x 45%; GEICO +12 pts x 60% (off); PGR -20 pts realised | Documented row by row; sizing precedents tab not yet readable |
| E5 Fees | Fixed buyer fees (gate / environmental) | $110 inherited | Replace with the posted fixed fees from the CSV; keep 110 only as a labelled legacy row |
| E5 Fees | Preferred / licensed buyer share | 50% | Sensitivity 30-70%; 10-K member counts do not give the mix |
| E5 Fees | Title Express adoption x charge | 50% x $50 | Sensitivity; call commentary on Title Express share gains is qualitative |
| E5 Fees | Long-haul delivery adoption x charge | 10% x $300 | Sensitivity |
| E6 Branches | Other-US fee activity residual | 10% of US service | Disclosed non-insurance unit growth (dealer +5.8%, BluCar +20%, Direct -11.7%; call) can size it; cite |

## Numbers with a weak anchor (18)

A reference exists but with a different population, denominator or date. Keep the reference beside the number on the tab and state the gap.

| Engine | Parameter | Value | Reference | Gap |
|---|---|---|---|---|
| E1 Fleet | Light-truck split into SUV / pickup / minivan | fixed shares by year | docs/historical_body_births_2026-09-28/candidate_body_births.csv (mix_status column) | EPA model-year production composition transferred to sales; pre-EPA years use an inherited fixed split |
| E1 Fleet | Post-2013 drift multiplier (2024) | 1.194 | docs/AGE_CURVES.md s.2.4 | Fitted to two 2024 count anchors (total VIO and share aged 7+) |
| E2 Claims | Body weights by age bucket | 6x4 matrix | age_constrained_engine_results.json body_weights | Fleet composition used as claims composition (no body-level claim data) |
| E2 Claims | Paired repairable non-filing term | 0 | integrated_service assumptions.json incremental_repairable_nonfiling | Deductible-shift placeholder |
| E3 Carriers | Carrier weights (auto premium share x salvage intensity 1.0) | SF .187, PGR .181, GEICO .117, Allstate .103, USAA .062, Farmers .038, Liberty .033, Travelers .020, Nationwide .015, Other .243 | model/linked_service_revenue_2026-09-28/inputs.json carriers[].weights; friend workbook C31:F40 (AM Best/NAIC, mixed years) | Premium share is not claim or total-loss share; salvage intensity set to 1.0 for all |
| E3 Carriers | Progressive runoff ramp | 2.2 quarters, Apr-Jul 2026 | docs/carrier_test_2026-09-28/README.md; share-build Events AB4 | Calibrated to the FQ4 FY26 print it is compared with |
| E3 Carriers | Seller commission rate | 4% of ASP | Barclays 25 Aug 2026 Figure 1 (analyst estimate, licensed, local); driver_register seller .04 | Analyst assumption, not a contract term |
| E3 Carriers | Concession on a won account | 20% of commission | Barclays 25 Aug 2026 Figure 1; docs/repair_research_2026-09-26/contract_scope_screen | Analyst illustration |
| E4 Aftermarket | Aftermarket price relative to OEM | 0.73 (stress 0.50) | Mitchell Q2 2017 Industry Trends Report pp8-10: 2016 discounts 23.3/29.9/27.7%, mean 27%; MapleV 2026 catalogue ~50% as stress | 2016 data; current matched discount unmeasured |
| E4 Aftermarket | Contribution-to-hammer bid ratio | 1.5x | inputs.json; Sturgeon 2018 margins 40-60% make the scale interpretable | Accounting ratio, not a bid elasticity |
| E2 Claims | Physical-damage coverage index (thesis 1) | (1-UM) x collision share; 2017 1.036 -> 2023 1.000 | IRC release 20 Feb 2025 (raw/irc): UM 15.4% 2023, +3 pts over six years; III/NAIC 2023 collision share 77% (raw/discovery_2026-10-02) | Yearly UM path interpolated; collision share history not obtained (NAIC HTTP 403) |
| E2 Claims | Two-point coverage response to premium burden | 0.59 | E2 D110 from the two endpoints | n = 2; indicative only; used in the premium-response path |
| E5 Fees | Insurance share of US service dollars | 90% (80% alt) | driver_register insurance_service_fraction; 10-K FY26: insurers supplied 79% of vehicles processed (global, units) | Nearest public anchor has a different denominator |
| E5 Fees | Expected net salvage recovery curve | 40% of value falling to 20% with age, less seller charges | driver_register expected_salvage (inherited); docs/repair_research_2026-09-26/value_recovery_audit | Inherited curve |
| E5 Fees | Vehicle value ratios by body (car / SUV / pickup / minivan) | 1 / 1.128 / 1.493 / 1.0 | age_constrained_engine_results.json value_ratios; docs/repair_research_2026-09-26/value_recovery_audit (KBB five-model panel) | Small panel |
| E5 Fees | Repair cost ratios by body | 1 / 1.007 / 1.310 / 0.981 | age_constrained_engine_results.json repair_ratios | Calibrated with the value ratios |
| E6 Branches | ACV acquisition scope and timing | excluded; control no earlier than FY27Q2 | raw/sec/acv/sc14d9_2026-09-17.htm, offer_to_purchase (on disk); docs/acv_reconciliation_2026-09-28 | Tender documents on disk can verify timing |
| Street | CapIQ consolidated FY27 total revenue | 4,860.97 | CapIQ export 2026-09-28 (local) | Acquisition perimeter unresolved |

## What this means for the build

- E1 Fleet and E2 Claims are traceable except for the two 2024 fleet anchors (fixable from files already on disk) and the light-truck subtype split (label as proxy).
- E3 Carriers is the largest unsourced block: every carrier allocation is second-hand. It can only be built as a labelled scenario with the quote bank cited row by row, with the two public anchors (the FQ4 FY26 call and the measured 57.2% listed-inventory split) shown beside it.
- E4 Aftermarket has no evidence-backed coefficient; it is built as a reduced form whose every parameter is a visible sensitivity, with the engine solver results pasted for parity.
- E5 Fees: the posted grid is verified; the fixed fee, buyer mix, seller rate, service adoption and the 90% insurance share are not. The $110 fixed fee contradicts the posted schedule on disk and should be replaced.
- E6 Branches: international and purchased are labelled continuations; the ACV timing can be verified from the tender documents already on disk.
