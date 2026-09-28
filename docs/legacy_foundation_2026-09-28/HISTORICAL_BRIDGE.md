# Historical service-revenue bridge

Completed September 28, 2026. Workbook: `outputs/cprt-historical-20260928/CPRT_Historical_Service_Bridge.xlsx`. Two tabs: Historical Bridge (formulas and model comparison) and Source Data (observations and provenance). Existing forecast workbooks are unchanged.

## Method

For each geography and fiscal quarter, start with prior-year service revenue. With unit growth u and fee RPU growth p, attribute the dollar change to prior revenue × u, prior revenue × p, and prior revenue × u × p. Keep the interaction separate. Reported current dollars provide the control. Where one operating growth input is disclosed, derive the other from the revenue identity. This is accounting attribution, not independent causal validation. It does not establish absolute units, fees or quarterly unit seasonality.

US Q1: company-disclosed +7.5% fee RPU; inferred fee-unit growth -7.46%. US Q2/Q3: newly checked Stephens August 20 report, Exhibit 7, PDF page 7, historical fee-unit growth -9.0%/-3.3%; implied RPU +3.73%/+3.05%. The PDF's period header and row positions were extracted with pdfplumber, without OCR, to confirm 2Q26/3Q26 alignment. These are broker-compiled history and have not been independently located in company disclosures. They are not company-reported RPU. US Q4 remains unavailable for attribution; the known -$6.991m revenue change appears as unallocated, not assigned to an invented unit/RPU pair.

International: company fee-RPU growth 8.1%, 7.6%, 10.5%, 3.5%; inferred fee-unit changes produce all four bridges. The separately disclosed rounded Q4 +11.5% fee-unit growth remains a cross-check, not a second calibration input. Rounding tolerance was checked in the earlier foundation audit.

US Q1–Q3 dollar contributions: volume -$171.931m, RPU +$124.280m, interaction -$8.629m; plus Q4 unallocated -$6.991m yields FY26 revenue decline -$63.271m. These annual contributions are explicitly partial. International: volume +$24.158m, RPU +$38.495m, interaction +$1.477m = +$64.129m. Together service revenue increased $0.858m. RPU contribution includes fee schedules, ASP/vehicle mix, service uptake and relevant FX; no attribution to a particular cause is established.

The new US RPU sequence is consistent with slowing aggregate fee RPU growth through Q3, but does not establish Title Express saturation, a permanent trend, or a forecast. Company-versus-broker provenance differs by period. Catastrophes, mix, pricing anniversaries and denominator changes remain competing explanations.

## Verification

Artifact Tool recalculation and export completed. Changed a US fee-unit input and verified inferred RPU changes while the revenue identity still reconciles. Set it unavailable and verified unit/RPU attribution becomes unavailable and the change becomes unallocated; restored the source value. Independent read-only Python arithmetic checked each available dollar contribution and all eight quarterly reconciliations; no cached Excel error cells. Both tabs rendered and visually inspected, then numeric/missing-input alignment refined. Native desktop Excel was not tested.

Source references are on Source Data and in the preceding foundation README. Original full licensed reports were not copied. Only targeted reading and small arithmetic were used. The workbook is a historical research build, not a replacement forecast or independent test of the damage engine.
