#!/usr/bin/env python3
"""Source-trace register for every numeric input in the Copart revenue architecture.
Writes docs/source_trace_2026-10-01/trace_register.csv and README.md. Edit the ROWS list; rerun.
Labels: VERIFIED (in a filing/page/file on disk), MEASURED (computed from verified data by a committed script),
FITTED (parameter chosen to reproduce data), CALIBRATED (level-matched to targets), ASSUMED (chosen; may cite a
reference), UNVERIFIED (recalled or second-hand), ENGINE (output of the Python engine pasted as values).
Flag: NO SOURCE = no file or page can be put next to the number; WEAK ANCHOR = a reference exists but with a
different population or denominator; OK = traceable."""
import csv, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'docs/source_trace_2026-10-01'
R = []  # engine, parameter, value, unit, label, source, basis, flag, fix
def add(*a): R.append(a)
# ---------------- E1 Fleet
add('E1 Fleet','New light-vehicle sales 1970-2021 by car/light truck','series','000s/yr','VERIFIED','raw/ornl/tedb40 Table 3.6 (Ward\'s); data/csv/ornl_tedb40_*.csv','ORNL TEDB Ed.40, fetched 2026-09-14','OK','')
add('E1 Fleet','New light-vehicle sales 2022-2025 by car/light truck','series','000s/yr','VERIFIED','raw/fred/TOTALNSA, LTRUCKNSA; data/csv/fred_*.csv','FRED monthly, summed','OK','')
add('E1 Fleet','Light-truck split into SUV / pickup / minivan','fixed shares by year','share','ASSUMED','docs/historical_body_births_2026-09-28/candidate_body_births.csv (mix_status column)','EPA model-year production composition transferred to sales; pre-EPA years use an inherited fixed split','WEAK ANCHOR','Use EPA Trends production shares where a model year exists; label pre-1975 rows explicitly; sensitivity on the split')
add('E1 Fleet','EPA survival schedule S(a), cars and light trucks','curve','share','VERIFIED','raw/ornl/tedb40 Table 3.15; docs/AGE_CURVES.md s.1','ORNL TEDB Ed.40','OK','')
add('E1 Fleet','Survival stretch k_cars(2013)','1.064','x','FITTED','docs/AGE_CURVES.md s.2.3; ORNL Table 3.11 (IHS census, licensed extract local)','Reproduces IHS 2013 cars-by-age census; bucket MAE ~0.4pp','OK','')
add('E1 Fleet','Survival stretch k_LT(2013)','0.921','x','FITTED','docs/AGE_CURVES.md s.2.3; ORNL Table 3.12','Reproduces IHS 2013 trucks-by-age census','OK','')
add('E1 Fleet','Post-2013 drift multiplier (2024)','1.194','x','FITTED','docs/AGE_CURVES.md s.2.4','Fitted to two 2024 count anchors (total VIO and share aged 7+)','WEAK ANCHOR','Anchors below must be sourced before this is OK')
add('E1 Fleet','Vehicles in operation anchor, 2024','289M','vehicles','UNVERIFIED','recalled S&P figure; Experian 292M is on disk (raw/ via www.experian.com, see PROVENANCE)','HANDOFF says recalled, not sourced; Experian on-disk figure gives the same stretch','NO SOURCE','Replace with the Experian on-disk figure and cite its file; or fetch S&P press release and cite')
add('E1 Fleet','Share of fleet aged 7+ years, 2024','66%','share','UNVERIFIED','docs/AGE_CURVES.md s.2.4 (S&P, no file)','Recalled from S&P average-age release','NO SOURCE','Fetch the S&P Global Mobility 2024 average-age release (robots permitting) or drop this anchor and fit to counts only')
add('E1 Fleet','Expert hard-constraint fleet by age and type','TBD','vehicles','UNVERIFIED','Google Sheet 1h_KrkIqv45RJBBISogkUA7Qguz5fm8qV (owner-supplied)','Supplied 2026-10-01; not yet on disk','NO SOURCE','Download to raw/reference/ and add a Checks row comparing the roll to each constraint cell')
# ---------------- E2 Claims & Totals
add('E2 Claims','Relative claims propensity by age bucket','0.219/1.0/0.949/0.889/...','index','CALIBRATED','docs/fleet_selection_2026-09-28/age_constrained_engine_results.json relative_claim_weights; CCC Crash Course 2026 claim-mix statistics','Fitted so claim mix by age matches CCC statistics; flat to age 6 then declining','OK','Show the CCC target figures beside the fitted weights')
add('E2 Claims','Body weights by age bucket','6x4 matrix','share','CALIBRATED','age_constrained_engine_results.json body_weights','Fleet composition used as claims composition (no body-level claim data)','WEAK ANCHOR','HLDI class loss frequencies (reports/E1_step3) could reweight; otherwise label as proxy')
add('E2 Claims','Total-loss frequency by 16 age x body cells, 2020-2025','matrix','share','VERIFIED','model/ccc_age_body_2026-09-29/source_cells.csv (owner-supplied CCC workbook, SHA recorded)','Observed CCC cells; geography/coverage of the workbook provisional','OK','')
add('E2 Claims','Claim weight and repair multiplier per cell','24 cells','index','CALIBRATED','model/ccc_age_body_2026-09-29/cohort_anchor.json','Derived from CCC cell TLF and mix; level calibration only','OK','')
add('E2 Claims','Claims multiplier','1.0 (0.98 stress)','x','ASSUMED','driver_register.json claims_multiplier','Neutral default; the 0.98 stress has no empirical anchor','NO SOURCE','Keep 1.0; present 0.98 only as a labelled stress or drop it')
add('E2 Claims','Paired repairable non-filing term','0','share','ASSUMED','integrated_service assumptions.json incremental_repairable_nonfiling','Deductible-shift placeholder','WEAK ANCHOR','CCC deductible share series (data/csv/ccc_deductible_share_quarterly.csv) could bound it')
add('E2 Claims','Routing fraction to insurance auction channel','1.0','share','ASSUMED','driver_register.json routing_CAT_and_sale_timing','Convention; owner-retained and direct-to-dismantler totals ignored','NO SOURCE','10-K: LKQ and dismantlers may buy directly from insurers; keep 1.0 as convention with a sensitivity row')
add('E2 Claims','Extra catastrophe unit fraction','0','share','ASSUMED','driver_register.json','Convention','OK','Convention stated; FY25 Helene/Milton comparison handled in history')
add('E2 Claims','Fiscal-quarter calendar weights','4 rows','share','MEASURED','model/linked_service_revenue_2026-09-28/inputs.json periods[].weights','Day-count overlap of fiscal quarters with calendar years','OK','')
add('E2 Claims','TLF spread regression dTLF = 0.599 + 0.0815 x spread(t-1)','0.599, 0.0815','pp','FITTED','data/csv/tlf_calibration.csv; ccc_tlf_quarterly.csv; totaling_spread_quarterly.csv (27 CCC quarters)','Diagnostic cross-check, not a driver','OK','')
# ---------------- E3 Carriers
add('E3 Carriers','Carrier weights (auto premium share x salvage intensity 1.0)','SF .187, PGR .181, GEICO .117, Allstate .103, USAA .062, Farmers .038, Liberty .033, Travelers .020, Nationwide .015, Other .243','share','UNVERIFIED','model/linked_service_revenue_2026-09-28/inputs.json carriers[].weights; friend workbook C31:F40 (AM Best/NAIC, mixed years)','Premium share is not claim or total-loss share; salvage intensity set to 1.0 for all','WEAK ANCHOR','Cite the NAIC/AM Best table and year per carrier on D Carriers; convert premium to exposure where PIF counts exist (PGR, GEICO on disk)')
add('E3 Carriers','Baseline Copart allocation by carrier','SF .50, PGR .25->.05, GEICO .83->.90, Allstate .95, USAA .95, Farmers .90, Liberty .70, Travelers .85, Nationwide .95, Other .50','share','UNVERIFIED','inputs.json carriers[].allocations; friend quote bank (expert calls, AlphaSense, Yipit)','Second-hand; no Copart disclosure identifies any carrier','NO SOURCE','Public anchors only: FQ4 FY26 -7.5% units with assignments +2.3% ex one customer (VERIFIED, call) and listed-inventory split 57.2% (MEASURED, 4 nights). Present allocations as a labelled scenario with the quote bank cited row by row')
add('E3 Carriers','Progressive runoff ramp','2.2 quarters, Apr-Jul 2026','quarters','FITTED','docs/carrier_test_2026-09-28/README.md; share-build Events AB4','Calibrated to the FQ4 FY26 print it is compared with','WEAK ANCHOR','State on the tab that the ramp is fitted to one print')
add('E3 Carriers','GEICO allocation event probability','60%','prob','ASSUMED','friend workbook U5; docs/FABLE_SHARE_BUILD_REVIEW_2026-09-27.md','Judgmental rubric, no calibration sample','NO SOURCE','Show as red toggle default OFF in A-only case; realised-case view beside expected value')
add('E3 Carriers','State Farm adverse event probability','45%','prob','ASSUMED','friend workbook U7','Judgmental','NO SOURCE','Same treatment as GEICO')
add('E3 Carriers','Other-carrier allocation loss','-5 pts at 45%','pts','ASSUMED','share-build Events row 15; regional anecdote','Narrow regional evidence extrapolated to a 24% bucket','NO SOURCE','Keep off by default; needs an affected-exposure denominator')
add('E3 Carriers','Seller commission rate','4% of ASP','share','UNVERIFIED','Barclays 25 Aug 2026 Figure 1 (analyst estimate, licensed, local); driver_register seller .04','Analyst assumption, not a contract term','WEAK ANCHOR','Label as Barclays estimate; sensitivity 3-5%')
add('E3 Carriers','Concession on a won account','20% of commission','share','UNVERIFIED','Barclays 25 Aug 2026 Figure 1; docs/repair_research_2026-09-26/contract_scope_screen','Analyst illustration','WEAK ANCHOR','Use only inside the labelled win scenario')
add('E3 Carriers','Copart share of duopoly listed US inventory','57.2% (n=4 nights, 11-27 Sep 2026)','share','MEASURED','data/csv/duopoly_daily.csv usable=1','Listed inventory, not assignments or sales','OK','Grow the sample; show n beside the figure')
# ---------------- E4 Aftermarket
add('E4 Aftermarket','Eligible parts share of repair bill','40%','share','ASSUMED','model/aftermarket_bridge_2026-09-29/inputs.json; CCC all-parts spend 36-44% by age (docs/aftermarket_parameter_audit)','All-parts spend is not the substitutable share','WEAK ANCHOR','Keep as sensitivity 30-45%; cite CCC parts-spend pages')
add('E4 Aftermarket','Eligible-basket source shares OEM/AM/recycled','65 / 25 / 10','share','ASSUMED','inputs.json source_quantity_shares; CCC 2025 dollar shares AM 22.7%, recycled 10.5% (whole bill)','Different denominator (whole bill vs eligible basket)','WEAK ANCHOR','Present CCC shares beside the basket assumption; show the conversion')
add('E4 Aftermarket','Relative prices OEM/AM/recycled','1.00 / 0.50 / 0.60','ratio','ASSUMED','inputs.json; Mitchell Q2 2017 report pp8-10 (2016 AM discounts 23-30%); MapleV Tesla catalogue ~50%','50% exceeds the only matched national dataset','WEAK ANCHOR','Default to the Mitchell range (0.70-0.77) with 0.50 as the stress; cite both files')
add('E4 Aftermarket','Donor contribution exposed fraction','25%','share','ASSUMED','inputs.json; docs/aftermarket_parameter_audit_2026-09-29/FORWARD_ASSUMPTIONS.md','No supporting record','NO SOURCE','Recycler donor-cohort report (Bidmate route) or keep as sensitivity')
add('E4 Aftermarket','Contribution-to-hammer bid ratio','1.5x','ratio','ASSUMED','inputs.json; Sturgeon 2018 margins 40-60% make the scale interpretable','Accounting ratio, not a bid elasticity','WEAK ANCHOR','Sensitivity 1.0-2.0; cite Sturgeon page')
add('E4 Aftermarket','Recycler price transmission weight','50%','share','ASSUMED','inputs.json','No evidence on marginal-bidder influence','NO SOURCE','Sensitivity 10-50%; the 10% case removes most of the price effect (AUDIT.md)')
add('E4 Aftermarket','Rebuilder repair-bill-to-bid ratio','1.0','ratio','ASSUMED','inputs.json','','NO SOURCE','Sensitivity')
add('E4 Aftermarket','Repair-job recapture','1.0','ratio','ASSUMED','inputs.json','Assumes comparable parts usage per incremental repair','NO SOURCE','Sensitivity 0-1')
add('E4 Aftermarket','Supply price response (donor scarcity)','0.25','elasticity','ASSUMED','inputs.json','','NO SOURCE','Sensitivity')
add('E4 Aftermarket','Expected salvage pass-through','1.0','share','ASSUMED','inputs.json','Immediate updating of insurers\' expected salvage','NO SOURCE','0/0.5/1 cases exist; keep visible')
add('E4 Aftermarket','Threshold-responsive claim fraction','1.0','share','ASSUMED','inputs.json','Not measured component eligibility','NO SOURCE','0/50/100% structural cases')
add('E4 Aftermarket','Incremental sourcing shift paths','OEM->AM 2/4/6 pp; recycled->AM 0.5/1.5/2.5 pp; quarterly 1/2/3/4 pp','pp','ASSUMED','inputs.json cases; model/thesis_audit_2026-10-01/assumptions.json; CCC AM dollar share +1.7pp 2024-25','Historical gain already in the base; future increments unobserved','WEAK ANCHOR','Show CCC 2020-2025 series beside the path; label the 5.5pp endpoint a stress')
# ---------------- E5 Prices & Fees
add('E5 Fees','Copart buyer fee grid by price band (licensed/non-licensed, clean/non-clean, standard/heavy, virtual bid)','schedule','USD','VERIFIED','data/csv/copart_fee_grid_2026-09.csv; raw/fees/live_2026-09/ (owner-driven page reads 2026-09-26)','One dated snapshot','OK','Historical application is a proxy; say so in row 2')
add('E5 Fees','Fixed buyer fees (gate / environmental)','$110 inherited','USD','ASSUMED','driver_register buyer_and_seller_fees; data/csv/copart_fixed_fees_2026-09.csv shows posted gate fee $79/$95','Inherited 110 does not match the posted fixed fees','NO SOURCE','Replace with the posted fixed fees from the CSV; keep 110 only as a labelled legacy row')
add('E5 Fees','Preferred / licensed buyer share','50%','share','ASSUMED','driver_register.json','No disclosure','NO SOURCE','Sensitivity 30-70%; 10-K member counts do not give the mix')
add('E5 Fees','Insurance share of US service dollars','90% (80% alt)','share','ASSUMED','driver_register insurance_service_fraction; 10-K FY26: insurers supplied 79% of vehicles processed (global, units)','Nearest public anchor has a different denominator','WEAK ANCHOR','Carry 80/90 as two cases; cite the 10-K 79% beside them')
add('E5 Fees','US insurance ASP growth, forward','+3.7% continuation (6% alt)','pct','ASSUMED','raw/transcripts/call_2026-09-10.txt lines 216-226 (FQ4 FY26 +3.7% VERIFIED)','Observed quarter continued; not guidance','OK','Label continuation')
add('E5 Fees','Manheim used-vehicle index, FQ4 FY26','+2.8%','pct','VERIFIED','call_2026-09-10.txt','Reference row','OK','')
add('E5 Fees','Title Express adoption x charge','50% x $50','share, USD','ASSUMED','driver_register title_delivery','Undisclosed product','NO SOURCE','Sensitivity; call commentary on Title Express share gains is qualitative')
add('E5 Fees','Long-haul delivery adoption x charge','10% x $300','share, USD','ASSUMED','driver_register title_delivery','Undisclosed; gross/net unknown','NO SOURCE','Sensitivity')
add('E5 Fees','Expected net salvage recovery curve','40% of value falling to 20% with age, less seller charges','share','ASSUMED','driver_register expected_salvage (inherited); docs/repair_research_2026-09-26/value_recovery_audit','Inherited curve','WEAK ANCHOR','Value-recovery audit gives two descriptive fractions; keep as assumption with that cite')
add('E5 Fees','Vehicle value ratios by body (car / SUV / pickup / minivan)','1 / 1.128 / 1.493 / 1.0','ratio','FITTED','age_constrained_engine_results.json value_ratios; docs/repair_research_2026-09-26/value_recovery_audit (KBB five-model panel)','Small panel','WEAK ANCHOR','Cite the KBB panel rows; sensitivity')
add('E5 Fees','Repair cost ratios by body','1 / 1.007 / 1.310 / 0.981','ratio','FITTED','age_constrained_engine_results.json repair_ratios','Calibrated with the value ratios','WEAK ANCHOR','As above')
add('E5 Fees','Cohort selection parameters (sigma, repair medians, value scales)','12 targets','mixed','CALIBRATED','age_constrained_engine_results.json; CCC Crash Course 2026 figures (repair means 5721/3682; selected ACVs 40187/30259/20328/9122)','Levels match; derivative unvalidated','OK','Show targets vs fitted on the tab')
add('E5 Fees','Selected-price band shares (for SUMPRODUCT with the fee grid)','per quarter','share','ENGINE','model/revenue_architecture_2026-09-28 run outputs (1,024-node integration)','Pasted values with file/date/SHA','OK','')
add('E5 Fees','Quarterly US and international service and vehicle revenue, FY25-FY26','8 quarters','USD m','VERIFIED','raw/sec/8k/er_*.htm; inputs.json actuals/prior_actuals','8-K exhibits','OK','')
# ---------------- E6 Other branches
add('E6 Branches','Other-US fee activity residual','10% of US service','share','ASSUMED','driver_register other_US','Residual convention','NO SOURCE','Disclosed non-insurance unit growth (dealer +5.8%, BluCar +20%, Direct -11.7%; call) can size it; cite')
add('E6 Branches','Other-US activity stress','+/-5%','pct','ASSUMED','driver_register','Stress only','OK','Label stress')
add('E6 Branches','International fee RPU growth','+3.5% (FQ4 FY26 disclosed), continued','pct','ASSUMED','call_2026-09-10.txt (VERIFIED quarter); continuation assumed','About $90m/yr vs flat','OK','Toggle continuation vs flat on the tab')
add('E6 Branches','International fee-unit growth','derived: service growth / 1.035','pct','MEASURED','EVIDENCE_UPDATE.md','Identity from disclosed growth','OK','')
add('E6 Branches','Purchased-vehicle revenue path','flat (alt: JPM FY27 $721m)','USD m','ASSUMED','driver_register purchased_revenue; JPM 11 Sep 2026 (licensed, local)','Comparison convention','OK','Label')
add('E6 Branches','ACV acquisition scope and timing','excluded; control no earlier than FY27Q2','gate','ASSUMED','raw/sec/acv/sc14d9_2026-09-17.htm, offer_to_purchase (on disk); docs/acv_reconciliation_2026-09-28','Tender documents on disk can verify timing','WEAK ANCHOR','Read the expiration date from the SC TO-T and cite it')
# ---------------- Benchmarks
add('Street','JPM FY27 service / purchased / total revenue','4,061 / 721 / 4,782','USD m','VERIFIED','licensed JPM report 2026-09-11 (local), Table 3 lines 275-278; evidence_manifest.json','Dated ex-ACV benchmark','OK','')
add('Street','CapIQ consolidated FY27 total revenue','4,860.97','USD m','VERIFIED','CapIQ export 2026-09-28 (local)','Acquisition perimeter unresolved','WEAK ANCHOR','Keep perimeter note')
add('Street','Named broker FY27 driver assumptions (7 brokers)','see Street tab','mixed','VERIFIED','licensed reports (local); extraction JSON 2026-09-30/10-01','Where a figure is absent it is recorded as not disclosed','OK','')

OUT.mkdir(parents=True, exist_ok=True)
hdr = ['engine','parameter','value','unit','label','source','basis','flag','fix']
with open(OUT/'trace_register.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(hdr); w.writerows(R)
by_label=collections.Counter(r[4] for r in R); by_flag=collections.Counter(r[7] for r in R)
nos=[r for r in R if r[7]=='NO SOURCE']; weak=[r for r in R if r[7]=='WEAK ANCHOR']
md=['# Source trace: every number in the revenue architecture, 1 October 2026','',
 f'{len(R)} inputs registered in `trace_register.csv` (regenerate with `python3 scripts/source_trace.py`). Labels: '+', '.join(f'{k} {v}' for k,v in sorted(by_label.items()))+'. Flags: '+', '.join(f'{k} {v}' for k,v in sorted(by_flag.items()))+'.','',
 'A number is traceable when a file in this repository, a page saved to disk, or a licensed report held locally can be put next to it. A number flagged NO SOURCE cannot be defended that way today; it must either be sourced before the build or appear in the workbook only as a labelled sensitivity, never inside a base case.','',
 '## Numbers with no source today (' + str(len(nos)) + ')','', '| Engine | Parameter | Value | What would close it |','|---|---|---|---|']
md += [f'| {r[0]} | {r[1]} | {r[2]} | {r[8]} |' for r in nos]
md += ['', '## Numbers with a weak anchor (' + str(len(weak)) + ')', '', 'A reference exists but with a different population, denominator or date. Keep the reference beside the number on the tab and state the gap.', '', '| Engine | Parameter | Value | Reference | Gap |','|---|---|---|---|---|']
md += [f'| {r[0]} | {r[1]} | {r[2]} | {r[5]} | {r[6]} |' for r in weak]
md += ['', '## What this means for the build', '',
 '- E1 Fleet and E2 Claims are traceable except for the two 2024 fleet anchors (fixable from files already on disk) and the light-truck subtype split (label as proxy).',
 '- E3 Carriers is the largest unsourced block: every carrier allocation is second-hand. It can only be built as a labelled scenario with the quote bank cited row by row, with the two public anchors (the FQ4 FY26 call and the measured 57.2% listed-inventory split) shown beside it.',
 '- E4 Aftermarket has no evidence-backed coefficient; it is built as a reduced form whose every parameter is a visible sensitivity, with the engine solver results pasted for parity.',
 '- E5 Fees: the posted grid is verified; the fixed fee, buyer mix, seller rate, service adoption and the 90% insurance share are not. The $110 fixed fee contradicts the posted schedule on disk and should be replaced.',
 '- E6 Branches: international and purchased are labelled continuations; the ACV timing can be verified from the tender documents already on disk.']
(OUT/'README.md').write_text('\n'.join(md)+'\n')
print(f'{len(R)} rows; labels {dict(by_label)}; flags {dict(by_flag)}')
