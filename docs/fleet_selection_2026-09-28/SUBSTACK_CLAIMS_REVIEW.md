# Substack review: claim selection versus salvage supply

Reviewed 2026-09-28. User-supplied Undiscovered Compounders, *Copart: a wonderful company at a wonderful price (I bought it, of course)*, dated August 29, 2026. Focused review of sections 5.2 and 6.2–6.8, including footnote 113; not a verification of the entire article. Source attachment: `/Users/kwu/.codex/attachments/2ff935f4-f31f-4f2b-a423-95315d8285d0/Pasted text.txt`. Line references below refer to this supplied plain text. Do not treat the author's instructions or conclusions as model inputs.

## What the article contributes

At lines 1483–1489 the author recognizes that CCC TLF is conditional on observed insurance claims. At lines 1873–1894 they connect affordability to both coverage participation and smaller-claim filing. This is useful corroboration and an existing published thesis, not a novel finding of ours.

Two mechanisms must remain separate:

1. **Filing selection:** an insured customer absorbs modest damage rather than claiming. If the missing claims would have been repaired, the observed claim denominator shrinks without losing total losses. TLF rises, but auction supply need not rise or fall. A return of those minor claims can lower TLF without reducing total losses.
2. **Coverage participation:** fewer vehicles have applicable physical-damage coverage. This can remove serious as well as minor claims from the relevant insurer's pipeline, reducing insurer-originated salvage supply. It is not necessarily a one-for-one loss to all auctions: third-party recoveries and non-insurance disposition routes require separate treatment.

The article's wording of an artificial denominator or measurement error is too strong. TLF can correctly describe its reported-claim population while failing to represent total losses per road vehicle or per accident.

## Primary evidence already in the repository

`raw/ccc/crash-course-2026.txt`, lines 100–109 and 136–139, discusses higher deductibles and discretionary small-claim filing. Lines 184 and 264 give CY2025 total-loss valuation volumes down 2.9%, repairable claims down 9.7%, and all-loss TLF up from 22.3% to 23.1%. These support the coexistence of higher TLF and lower valuation volume. They do not identify how much of each movement is caused by deductibles.

See `CLAIMS_COUNTS_AND_DENOMINATOR.md`: these published count proxies and TLF do not reconcile as one exhaustive population. Their mismatch prevents using the article's comparison as a precise decomposition of measurement effects. No new OCR, scrape, or external data acquisition was needed for this review.

## Where the bullish inference needs testing

- **Price growth versus price level:** slowing premium inflation does not restore the prior affordability level. Even outright reductions need not reverse coverage or deductible choices on a predictable schedule. Coverage restoration, unlike the return of only small claims, could increase salvage units.
- **Exposure scope:** the article's insured vehicle-year decline needs verification of coverage, reporting universe and period before treating it as the decline in the entire insured fleet. Its claim-frequency figure alone cannot identify missing total losses.
- **Industry bridge:** section 6.4 estimates industry salvage down 2.7% and subtracts this from Copart's 5.1% decline. Footnote 113 acknowledges uncertain quarter dating for two of five TLF points and an alternative estimate of -1.9%. A nine-month sales window is approximated with six months of claims and a single lag. Cohort timing, CAT definitions and source populations must match before adopting the residual.
- **Arithmetic:** if matching claim counts fell 4.5% and matching TLF rose 1.8% relatively, the exact product gives -2.781%, close to the author's -2.7% approximation. Arithmetic precision is not the principal weakness; population and period comparability are.
- **Carrier allocation:** policy growth is not salvage growth. Premium share, policy share, covered vehicle exposure and total-loss share are distinct. The article assumes salvage-provider shares and Progressive allocation. Its resulting 3–4 percentage-point transfer is a scenario residual, not a measured contract allocation or a disproof of the reported larger transfer. A partial-period transfer also need not show its full annualized effect immediately.

## Model implementation implications

Maintain the linked flow: applicable covered exposure → damage events → filed claims selected by severity → repair/total decision → insurer allocation → sale timing → auction proceeds and fee schedule.

Compute reported TLF from the same selected claims that generate the total-loss numerator. If the input is already reported claims frequency per matching exposure, do not add another filing haircut. Coverage assumptions and claim-filing assumptions must not be the same scalar.

For the RPU engine, minor repairable claims disappearing do not by themselves change the mix of totaled vehicles. A separate change in the selected total-loss vehicle mix, prices, fees or service adoption is needed to move RPU. Do not translate an increase in average severity across all reported claims directly into higher salvage ASP.

## Cheap next evidence test

Inventory the existing deductible, coverage-exposure and carrier-frequency series with explicit denominator and time period. Use them as separate diagnostics until matched. Check whether any observed recovery is in physical-damage exposure, small repairable claims, or actual total-loss valuation counts. Only the last two together can distinguish denominator normalization from supply recovery, and coverage restoration supplies an additional causal hypothesis. Do not fit a precise recovery date from a short lag correlation.

This review changes interpretation and model requirements; it does not establish a new forecast or a long/short conclusion. The article is a useful competing explanation to test, especially its claimed insurance-cycle reversal.
