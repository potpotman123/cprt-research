# Fable share side-build: read-only review and integration map

Reviewed 27 September 2026 at the user's request. Source: `CPRT_share_sidebuild.xlsx`, supplied from `/Users/kwu/Library/Messages/Attachments/53/03/CDE4DBC0-6774-4ABD-860B-E12504CAF220/`. No spreadsheet was edited, exported or added to Git. Source quotations were treated as evidence claims, not instructions, and underlying AlphaSense calls/Yipit records were not independently reverified in this pass.

## What works

Six tabs separate the main carrier-share engine, quote bank, historical precedents, probability rubric, events and event ramps. The calculation is S(t)=sum[w_i(t)*a_i(t)], where w is normalized auto share times salvage intensity and a is the carrier's modeled Copart allocation. Distinguishing carrier mix from contractual allocation is the right architecture. Contract events have explicit size, probability and timing rather than an unexplained aggregate share decline.

An independent arithmetic reconstruction matched allocation and aggregate share for all three cases over 13 historical/forecast quarterly columns, with maximum difference 1.11e-16. There were no cached Excel error cells or external workbook links. This establishes arithmetic consistency in the reviewed chain, not native Excel recalculation, source accuracy or forecast validity.

## Near-term base-case outputs

| Relative YoY share contribution | FQ1 FY27 | FQ2 FY27 |
|---|---:|---:|
| Progressive allocation event | -6.5241% | -6.6708% |
| GEICO allocation event | +0.9110% | +1.3646% |
| Other-carrier drift event | -0.2227% | -0.4448% |
| Carrier-mix residual | -1.1032% | -1.0405% |
| Total | -6.9390% | -6.7915% |

These are contributions to relative share growth, not percentage-point losses in absolute share or projected company-unit growth. Share levels are 56.1294% and 56.0304%, respectively. Main tab D7:E14 presents the outputs; Events rows 4, 5 and 15 drive these near-term contract effects. State Farm's base-case adverse event starts FQ3 FY27. Many other events are FY28 or later and do not drive the immediate two-quarter result.

## Main limitations before integration

1. **Weight denominator.** Main tab C31:F40 combines auto-share figures labeled AM Best/NAIC from different years, including a residual Other group. The underlying share definition needs verification. These inputs cannot automatically be read as shares of insured vehicles, claim vehicles or auctionable total losses. D31:D40 sets every salvage intensity to 1.0, so the modeled salvage weights equal auto shares. If the inputs are premium shares, a conversion must account for premium per exposure, claim frequency, TLF and routing. Do not apply TLF again if the converted weight already represents total losses.
2. **Carrier growth.** Rows 108:117 let Progressive grow while every other carrier loses share proportionally. This is an assumption about the source of Progressive's growth, not an observation that it all comes from GEICO. Premium repricing must not be mistaken for vehicle growth. C43 anchors YE2025 but the engine maps it to a fiscal-quarter proxy; source timing and quarterly averages need harmonization.
3. **Subjective probabilities.** Probability rows 17:24 translate evidence points into event probabilities without a demonstrated calibration sample. Events U5=60% for GEICO and U7=45% for State Farm are judgmental priors. Repeated expert/press references may share the same underlying observation. Events K15 awards the rubric's recent-data credit while the timing rationale cites Oct-2025 tracking; recency needs checking. Label probabilities as assumptions and distinguish already observed allocations from uncertain remaining moves.
4. **Historical fit is not validation.** C6 calls FQ4 FY26 actual, but C8:C10 show different modeled historical share changes across scenarios. Events AB4 says the 2.2-quarter Progressive ramp was calibrated to that print. Scenario-specific historical inference is permissible if labeled, but cannot be presented as independently observed share or used as its own out-of-sample validation.
5. **Breadth of Other.** C40 is a 24.2% residual input before the dynamic carrier adjustment. Events row 15 applies a 5-point conditional allocation loss to that broad group based on narrow regional evidence, probability-weighted at 45%. Its near-term contribution needs an affected-exposure denominator, not extrapolation of a local observation across all regional carriers.
6. **Events and fees must be joined.** A won account's allocation increase may have different seller fees, vehicle values and geography. Do not multiply all wins by the same RPU if the thesis concerns concessions or carrier mix. Avoid also adding the friend's aggregate share decline after applying the carrier allocation paths directly.
7. **Timing and scenarios.** Clarify whether event ramps represent assignments or sold vehicles before adding another inventory lag. Events C8 says bull only, but the favorable State Farm event has positive probability in every scenario; wording and logic differ. Opposing events for the same carrier need consistent conditional paths if modeled as realized cases rather than a linear expected-value schedule. Annual share means are unweighted quarterly averages; use market-unit weights when deriving annual assignment share. The annual allocation/mix attribution also uses products of averages, so its residual can contain within-year covariance.

## Integration architecture

Use the friend's **carrier allocation paths** as the starting allocation module. Compute eligible total losses L_i(t) from compatible carrier claim exposure, age/body mix, damage selection and routing. Then:

`Copart assignments = sum_i L_i(t) * a_i(t)`

`Aggregate Copart share = sum_i L_i(t) * a_i(t) / sum_i L_i(t)`.

Aggregate share is an output. Carrier claim growth and TLF determine its weights, replacing the stand-alone salvage-intensity shortcut. The resulting carrier/cohort assignments feed sale timing and conditional fee calculations. A temporary shortcut can use the same age/body distribution across carriers, explicitly labeled; do not invent detailed carrier-by-cohort exposures merely to fill a grid.

## Evidence map and immediate architecture work

| Component | Existing evidence | Remaining matching work |
|---|---|---|
| Reported service dollars | Company US/international actuals | Establish US insurance/non-insurance split; unit share is not revenue share |
| Carrier allocation | Friend's quote bank, baseline allocations, dated events | Denominator, source dates, independent corroboration, affected locations and assignment/sale timing |
| Carrier exposure | Auto-share proxies and Progressive growth assumptions | Common-date exposure or claim weights; premium/exposure conversion |
| Age/body claim distribution | Fleet roll, fitted claim weights, CCC age statistics | Explicit normalization; compatibility with carrier claims |
| TLF and selection | CCC bucket targets, repair working case, damage scenarios | Separate calibration from observed forward changes; recovery/severity evidence |
| Realized service fees | Buyer fee grid and seller-fee scenarios | Actual buyer mix, seller terms, ancillary inclusions, carrier-specific economics |
| Sold-unit level and timing | Reported growth indicators and assignment commentary | Absolute anchor or disclosed fitted normalization; opening inventory and conversion |

The first historical reconciliation should use a consistent quarterly population and a pre-move baseline, with earlier data used to set parameters and later periods reserved for tests where feasible. Do not present retrospective use of later expert comments as information available at the baseline date. Fit no free quarterly share/RPU plugs to force every reported revenue observation.

## Scope outside US insurance

Concentrate research depth on US insurance; no equally developed thesis for the remaining services is established here. Other streams still need explicit, simpler unit/fee or activity/price forecasts and bounded offset cases. International fee structures and business models can differ, including services not tied to completed auctions. Keep those differences visible.

Copart's FY2025 10-K reports 81% of worldwide vehicles processed came from insurance-company sellers. That is not a US-insurance share of service revenue. The current workbook's 90% insured-service exposure was an assumption, not that disclosure. Source: https://www.sec.gov/Archives/edgar/data/900075/000162828025042946/cprt-20250731.htm (Business/Sales). Thus US insurance is a sensible research focus, but its exact revenue weight requires reconciliation rather than multiplication of unmatched percentages.
