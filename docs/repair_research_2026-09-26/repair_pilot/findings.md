# Repair-cost pilot: public estimates and a separate crash-damage check

September 26, 2026. This is a small convenience sample, not an estimate of US fleet repair severity.

## Decision

Public vehicle-specific bodyshop/insurer estimates are available. The pilot does not validate the earlier 1.01 light-truck/car repair-cost multiplier, and does not establish that it is false. Zero fully matched whole-repair pairs were obtained. One narrow operation comparison and one within-vehicle supplement comparison are usable as assumption challenges. No confidence interval or population repair-cost premium is reported. Keep 1.01 as an unvalidated scenario, not a measured base case.

## Procedure and actual scope

Searched public estimates by vehicle, operation and document type; inspected original document text rather than uploaders' AI summaries. Prioritized mainstream Toyota/Honda cars and crossovers and Ford pickups. Extracted component operations, hours, rates, parts, estimate stage and dates where available. Reconstructed three estimate totals arithmetically, then applied common labor/materials rates. Kept supplementary controlled-impact evidence separate from repair-operation evidence.

This turn used 18 targeted search queries, bounded page reads, and one successfully downloaded 844 KB PDF packet. No paid access, outreach, bulk scrape or OCR. A second PDF download returned 403; its public indexed primary-source table was readable through the web tool. A local PDF page-render attempt stalled and was terminated. Some packet pages had corrupt text encoding; these were excluded from numeric comparisons rather than guessed. Source layout was not independently verified visually, so estimates are provisional transcriptions. No owners' names, addresses, VINs or claim identifiers are included in the analytical output.

## 1. Narrow operation test: front-bumper overhaul

A 2022 Toyota RAV4 XLE estimate dated March 14, 2023 lists 2.6 hours for front-bumper overhaul. A 2023 Toyota Camry SE estimate dated February 15, 2024 lists 3.5 hours. At an assumed common $60/hour, these individual labor lines become $156 and $210: RAV4/Camry = 0.743, or 25.7% lower for this operation.

Sources: [RAV4, document p. 2, line 4](https://www.scribd.com/document/720590247/ESTIMATE-22-TOYOTA-RAV4); [Camry, document p. 2, line 2](https://www.scribd.com/document/835879619/Geico-Mobile). The Camry full-page endpoint was intermittent; its indexed original document text supplied the operation and totals. These are uploaded primary documents, not authenticated directly with the preparers.

This is the closest operation-level comparison, not a fully matched repair pair. Both are mainstream Toyotas, adjacent model years, approximately one year old at estimate date, and use the same named estimating operation. However, they have different bumper designs and equipment, dates, damage, and preparers. Overhaul is disassembly/reassembly labor, not the complete cost of repairing bumper damage. The RAV4 cover is repaired; the Camry cover is replaced and additional parts are damaged. Do not extrapolate the 0.743 ratio to full repair bills or totaling probability. This observation only rejects the presumption that SUV labor requirements must be higher in every operation.

## 2. Within-vehicle test: estimate stage

A 2013 Ford F-150 FX2, estimated in August 2023, has an initial estimate of $3,499.97 and a supplement of $1,331.08, reaching $4,831.05: a 38.0% increase. The supplement adds or revises door work, associated disassembly, scans and wheel-related charges. It is not evidence that every increment was hidden crash damage, nor is the supplement a verified paid invoice.

[Source: document pp. 5-6](https://www.scribd.com/document/768641568/estimates). This case is approximately ten years old, making its age more relevant to the target cohorts. Its 1.9-hour bumper-overhaul line is recorded but not pooled with Toyota observations because design, age and equipment differ.

This demonstrates a measurement problem: comparing preliminary sedan quotes against supplemented SUV estimates could manufacture a segment premium. It does not establish a typical supplement rate, a truck-specific effect, or the uncertainty of a population mean.

## 3. Arithmetic and rate normalization

All three component sums reconcile to the stated pretax amounts and gross totals to the cent. Standardization assumes $60/hour for body and paint labor, $100/hour for mechanical labor, and $40 of paint supplies per paint hour. These are analytical choices, not measured national rates. Parts prices stay at their original dates; no inflation or OEM/aftermarket adjustment is made.

| Vehicle | Original pretax, before discount | Standardized pretax, no discount | Main comparability issue |
|---|---:|---:|---|
| 2022 RAV4 | $2,658.94 | $2,678.94 | Preliminary/self-pay; bumper repair, fender replacement, door repair |
| 2023 Camry | $6,904.54 | $7,129.14 | Insurer estimate; bumper replacement, lamps and radiator-support work; different parts mix |
| 2013 F-150 | $4,395.00 | $3,498.00 | Supplemented; bumper and multiple door operations; much older vehicle |

Formula: parts + body hours × common body rate + paint hours × common paint rate + mechanical hours × common mechanical rate + paint hours × common materials rate + other charges. F-150 feather/prime/block hours are included separately at the common body rate. Tax, deductibles and the RAV4 customer discount are excluded from standardized totals. A deductible reduces payment, not physical repair cost.

These totals must not be divided to estimate a segment premium. Standardizing rates does not standardize damaged components, repair versus replacement, or parts quality. The common-rate exercise demonstrates that the extraction is calculable; it does not solve causal comparability.

## 4. Separate controlled-impact check

IIHS tested seven car/SUV pairs in both 10 mph front-into-rear orientations, using 2010-11 vehicles and November 2010 repair prices. Summing each vehicle's front and rear test costs gives SUV/car ratios ranging from 0.43 for Escape/Focus to 1.21 for RAV4/Corolla; six pairs are below one. No fleet-weighted average is appropriate.

The experiment controls collision protocol better than unrelated invoices, but does not hold damage, vehicle mass or collision partner constant. It measures damage susceptibility plus repair pricing. Bumper alignment can shift damage into expensive structures; this is distinct from the cost of performing an identical operation. These historical, low-speed tests cannot calibrate today's older-vehicle total-loss tail. [IIHS primary report, PDF p. 10](https://www.iihs.org/media/e715d94d-5244-440e-bd04-252d823f747c/1122916300/RegulatoryComments/comment%202012-03-05_2.pdf).

## Candidate disposition

- Three estimates above: usable for arithmetic, narrow labor comparison and supplement comparison; no matched whole repair.
- 2016 Honda CR-V: accessible original page gives aftermarket fender $260, replacement labor 1.2 hours, bumper removal/reinstallation 1.7 hours. Retained as extraction example only: removal/reinstallation is not overhaul; full estimate absent from packet. [Packet, PDF p. 15](https://diminishedvalueoforegon.com/wp-content/uploads/2017/09/SAMPLES-of-ESTIMATE-OF-RECORDs.compressed.pdf).
- Same packet's 2013 Challenger: extensive structural/engine work and sports-coupe classification; excluded as a mainstream-car comparator. 2004 Jetta: corrupt extraction on relevant pages; excluded numerically.
- 2021 Accord preliminary estimate: indexed repair/replacement presentation ambiguous; excluded from matched calculation. https://www.scribd.com/document/727021200/2021-Honda-ACCORD
- 2009 Camry and 2007 Accord: accessible line items but incompatible ages/parts/damage with the selected crossover; excluded from ratios. https://www.scribd.com/document/984346379/Mohammed-Camry and https://fr.scribd.com/document/681229666/1
- 2018 RAV4 municipal packet and 2021 Camry municipal claim: indexed overhaul lines but incomplete page access; not treated as verified complete estimates.
- 2020 F-150 municipal packet: relevant document found, text access failed; no numeric inclusion.
- CarAid/RepairSnap and general cost guides: examples or indicative ranges, not authenticated completed invoices; excluded from empirical cost comparisons.

## Consequence for model architecture

Separate (a) damage incidence and component damage conditional on collision, (b) prices/hours conditional on component and operation, (c) repair/total-loss selection, and (d) initial versus supplemented estimate stage. An aggregate paid-claim severity multiplier confounds these mechanisms.

The next useful increment is a prespecified set of older model-year sedan/crossover pairs with identical replacement-operation bundles, including OEM/aftermarket status, full labor operations and final estimate stage. Obtain more public original estimates or a consistent estimating-source comparison; do not simply enlarge a sample of unrelated total bills. This pilot has not produced evidence to choose 1.01, 1.18, or any other full-cost multiplier.
