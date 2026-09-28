# Search for actual delivery revenue or vehicle counts

As of 28 September 2026. Result: **no usable Copart Delivered revenue level, completed-vehicle count or adoption rate found in the materials checked.** Missing is not zero. This is a scoped search result, not a claim that no such disclosure exists anywhere.

## Coverage and method

- Keyword-screened 17 local call transcripts, including FY26 Q1–Q4, with context review of relevant passages. Terms included long-haul, Copart Delivered, delivery revenue, deliveries, transportation, shipping and logistics. General uses of “over the long haul” were rejected.
- Screened 22 existing research text files in the project research directory, including 13 documents in the supplied sell-side source folder. Relevant hits came from September JPMorgan, BNP, Barclays and EQUISIGHTS reports. These are not 22 independent delivery studies. The other nine text files produced no hits in the initial specific-term screen. No PDF OCR was performed.
- Retrieved and text-parsed all three FY26 10-Qs: October 31, 2025; January 31, 2026; April 30, 2026. Delivery/transport hits concern general operations and risk factors, not product-level revenue or paid deliveries. Preserved extracted text and source hashes in `disclosure_search/`.
- Checked the FY25 10-K's business description and service-revenue discussion. Transport to and from facilities is included in the broader service offering; it does not provide the required product split.
- Queried SEC submissions metadata. The newest 10-K returned was FY25, filed September 26, 2025; the newest 10-Q was April 30, 2026, filed May 29. No FY26 10-K was returned by that check. Do not label FY25 policy as newly verified FY26 product accounting.
- Checked the SEC-filed September 10, 2026 call transcript and performed a small public search for product revenue, volumes and penetration. Public results mostly repeat the cost disclosure. Secondary estimates were not promoted to reported figures.

## Source links

- [FY26 Q3 10-Q](https://www.sec.gov/Archives/edgar/data/900075/000119312526245578/cprt-20260430.htm)
- [FY26 Q2 10-Q](https://www.sec.gov/Archives/edgar/data/900075/000119312526088593/cprt-20260131.htm)
- [FY26 Q1 10-Q](https://www.sec.gov/Archives/edgar/data/900075/000119312525291660/cprt-20251031.htm)
- [FY25 10-K](https://www.sec.gov/Archives/edgar/data/900075/000162828025042946/cprt-20250731.htm)
- [September 10 call, filed as ACV transaction exhibit](https://www.sec.gov/Archives/edgar/data/1637873/000119312526388383/d138398dex992.htm)
- [SEC submissions metadata](https://data.sec.gov/submissions/CIK0000900075.json)

## What survives the review

| Item | Evidence status | Use |
|---|---|---|
| FY26 Q3 approximately $15m YoY delivery-related facility-cost increase | Management disclosure, May 21 call lines 471–477 | Conditional cost-to-revenue scenario only |
| FY26 Q4 approximately $17m YoY delivery-related facility-cost increase | Management disclosure, September 10 call lines 522–528; SEC exhibit corroborates | Conditional cost-to-revenue scenario only |
| Approximately 20% margin | JPMorgan freight-forwarding industry analogy | Assumption; not a measured product margin |
| 15,000–20,000 vehicle movements on some days | September 10 call lines 283–288, general logistics capability in acquisition discussion | Reject as paid Copart Delivered volume; no annualization |
| Roughly 400-mile average transport distance | BNP discussion of ACV | Reject as Copart Delivered average distance |
| $21.25m revenue increment | Our $17m / (1 − 20%) calculation | Conditional increment, not actual revenue level |
| 120,833 jobs / 12.08% adoption in prior prototype | Derived from assumed $300 price, starting revenue and eligible population | Illustrative only; not historical data |

The logistics movement statistic lacks product boundary, paid-job status, geography and period-average frequency. It could encompass other movements. No defensible conversion to completed customer deliveries follows from it.

## Model decision

Leave actual delivery revenue, paid deliveries and adoption **unavailable** in the evidence layer. Preserve the scenario engine, but do not calibrate it to the broad logistics count or to an invented historical starting level. Broad service-revenue disclosure cannot identify the product because auction fees, Title Express, storage and other services change simultaneously.

An explicit assumption remains permissible for a provisional forecast, but it must not be called an accurate disclosure. The cost bridge constrains possible changes under specified assumptions; it does not establish saturation, quarterly adoption additions, or absolute service dollars. Do not rerun arbitrary price grids as a substitute for missing evidence.

## Next targeted evidence request

The best remaining low-cost source is a broker follow-up or management-meeting note in AlphaSense that was not among the supplied reports. Search Copart with the exact product name and long-haul delivery, then narrow to revenue, vehicles transported, completed deliveries, penetration or attach rate. Limit the first pass to recent relevant documents rather than exporting the whole result set.

Ask for a passage providing **either quarterly/annual revenue or paid vehicle deliveries**, together with period, US versus global coverage, outbound buyer delivery versus all transport, and whether the number is company-reported or the analyst's estimate. For revenue, check gross billings versus recognized revenue. For counts, check vehicles versus multi-car truckloads and completed versus booked orders. A single correctly defined figure is useful; another repetition of $15m/$17m costs is not.

No external message has been sent. No account access, paid research, mass quote collection or additional Excel work was performed. If the targeted proprietary check also fails, keep this component explicitly assumed and continue the main model rather than spending heavily trying to derive an unidentifiable number.
