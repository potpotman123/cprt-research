# Broader discovery: missing older-vehicle claims evidence

28 September 2026. Completed the authorized three bounded stages: existing-file inventory, sixteen discovery queries spanning eight source families, and three focused leads with small arithmetic checks. No OCR, bulk collection, paid access, outreach or forecast edits. Search terms, access limitations, source populations and negative results are in SEARCH_LEDGER.md. Reproducible observations and calculations are in small_checks.json and checks.py.

## What changed our understanding

### 1. Coverage-specific frequency divergence is corroborated beyond CCC

The [LexisNexis 2026 report summary](https://risk.lexisnexis.com/insights-resources/white-paper/auto-insurance-trends-report) reports collision paid frequency down 16.4% since 2022 versus property-damage liability down 3.5%. Indexing each to 100 in 2022 gives 83.6 and 96.5; their ratio declines 13.37%. The linked public interactive report did not expose further sections through the text reader, so no additional cohort detail is claimed.

[Progressive's 2025 financial review](https://www.progressiveproxy.com/Progressive-2025-Financial-Review.pdf), App.-A-64, supplies incurred-frequency changes. Compounding 2023–25 gives collision 81.282 versus liability 94.08 on the same base-100 convention, a 13.60% relative decline. Its 2025-only changes are −5% and −2%. Management explicitly identifies customer-mix improvement as one contributor. This rechecks existing carrier evidence.

**Our inference:** the direction is consistent with some force disproportionately reducing first-party collision claims, rather than a uniform fall in incidents alone. It does not quantify that force. Coverage populations, drivers, exposures, fault, payment timing and claim definitions differ. The two sources cannot be pooled as independent samples; their populations may overlap. Neither percentage is an estimate of missing small claims, a 13+ rate, or incremental Copart units. A decline in frequency among covered exposures also does not measure the number of people dropping coverage.

### 2. Repair-business evidence improves the timing check, but is not necessarily independent

[Boyd's Q3 release](https://boydgroup.com/investor/investor-news/news-details/2025/Boyd-Group-Services-Inc--Reports-Third-Quarter-2025-Results-11-12-2025/default.aspx) estimates 2025 repairable-claim declines of 9–10% in Q1, 6–8% in Q2 and 3–5% in Q3, attributing the estimates to claims-processing platforms. Its [annual report](https://s25.q4cdn.com/123825503/files/doc_financials/2025/ar/2025-Annual-Report.pdf), printed p.3, gives 2–4% for Q4. The change in the YoY rate from Q1 to Q4 is therefore 5–8 percentage points; it is not sequential growth. Printed p.43 separately discusses capacity and conversion of sales opportunities into repair orders.

**Our inference:** falling shop activity must not be equated with unfiled insurance claims. A claim can be filed and paid without a completed repair; a shop can also miss a job because of capacity or customer choice. A third-party transcript search surfaced a cash-settlement discussion, but it was not promoted to a verified primary quote. We did not locate measured cash-settlement or age-specific repair-authorization rates in the primary material inspected. Boyd's industry estimates cannot be counted as an independent shop census or averaged with CCC. Exact panel compatibility is unknown.

### 3. Several apparently promising sources answer different questions

The search located regulatory coverage/exposure publications, estimating-software workflows, shop-operation surveys, lender coverage explanations, fleet-registration reports and auction research. Their relevance differs. Registration counts constrain fleet survival; they do not reveal insurance coverage. Payment-for-repair-operation surveys constrain allowed cost; they do not measure unfiled events. Software documentation identifies records that may exist; it does not provide their historical distribution. A loan-payoff explanation establishes a possible choice, not the probability that customers make it.

The Guardian result was a different survey from the one cited in CCC, so it does not validate the cited coverage-downgrade percentage. This is precisely why tracing original populations matters.

## Architecture implications

Use distinct events rather than treating every reduction in repairs as a lost claim:

1. A covered or uncovered damage event occurs.
2. A claim is or is not recorded.
3. A recorded claim is assessed as repairable or a total loss.
4. A repairable settlement may or may not produce a completed repair.
5. A total loss may be owner-retained or assigned to salvage, then routed and sold.

Steps 2 and 4 are different selection mechanisms. Claim-filing selection can change measured TLF. A decision not to complete an already-recorded repair need not change a claims-based TLF denominator; its effect depends on what the source records. Neither automatically adds salvage units. Keep repair-shop completion data as an external check unless the input population is explicitly repaired vehicles.

The prior numerical filing filter remains a hypothetical scenario. Do not calibrate it to the relative collision/liability decline or survey respondent percentages. The search narrows mechanisms without resolving the oldest-bucket residual.

## What to seek next, precisely

**First choice: matched insurer or claims-platform cross-tabs.** Ask for CY2024 and CY2025, ideally quarterly, with vehicle ages 13–15, 16–19 and 20+; collision versus property-damage liability; insured earned vehicle-years where meaningful; recorded unique claim counts; repairable and total-loss counts; deductible bands; valuation/repair-cost distributions; and unchanged-panel methodology. For liability, clarify whether age refers to the claimant's damaged vehicle or the insured's vehicle—these are different. Never divide claimant-vehicle-age counts by insured-vehicle-age exposure without justification.

**Second choice: repairer conversion records.** Seek estimates received, jobs authorized/completed, total-loss referrals, self-pay repairs and insurance-paid claims without repairs, split by vehicle age and insurer for comparable shops/periods. Count unique vehicles/claims rather than supplements. A modest anonymized summary is preferable to thousands of invoices. Shops cannot observe all damage never presented to them.

**Public-data fallback:** extract a small national coverage/exposure table from the NAIC report, with matched years and earned/written definitions preserved, to test coverage penetration direction. This is a historical foundation check, not a solution to current 13+ identification. For near-term repairable-volume context, retain provider-specific series separately rather than merging them.

No external requests were sent. No evidence yet warrants a production forecast revision. The best finding is the first-party/third-party contrast and the newly explicit distinction between recorded claims and completed repairs—not a precise new TLF coefficient.

## Validation

Five arithmetic assertions passed. All numerical inputs have source URL, period, scope and locator in small_checks.json. The sixteen exact queries and read-versus-discovery distinction are preserved in SEARCH_LEDGER.md. Links may change; observed values are recorded as retrieved on the access date, without claiming local copies of full publications.
