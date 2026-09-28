# Core RPU build: service evidence and conditional delivery bridge

**Research priority update:** delivery investigation is parked by user direction. Retain explicit assumptions and the existing evidence limitations; do not spend further effort on this component now. Active work resumes at [fleet and damage-selection foundation](../fleet_selection_2026-09-28/README.md).

Follow-up: [delivery evidence update](DELIVERY_EVIDENCE_UPDATE.md) traces the 20% margin to a JPMorgan industry analogy, identifies possible automatic-delivery fee offsets, and records the user's analysis-in-Git / Excel-in-Fable workflow. Neither margin nor adoption is independently measured.

Actual-disclosure search: [scope and result](DELIVERY_DISCLOSURE_SEARCH.md). No usable delivery revenue level, completed-vehicle count or adoption rate found in the checked filings, calls and supplied research. General logistics movement counts are not delivery-product counts.

28 September 2026. Fee-band catalyst work is parked at the user's request. This pass resumes the operating model: existing local transcripts and small arithmetic only, no new collection or Excel changes.

## Findings and source attribution

| Component | What the source establishes | What it does not establish |
|---|---|---|
| Auction-price pass-through | Existing fee-grid experiment establishes a conditional mechanical response | Historical schedule changes, buyer distributions or realized seller fees |
| Pricing anniversaries | Analyst question in May21 call lines396–398 describes prior pricing actions as fully lapped | Independent dated Copart schedule history or exact contribution; this is an analyst premise |
| Title Express | May21 lines401–407: more accounts penetrated; Sep10 lines569–579: management explicitly says product expansion increased RPU | Dollar price, eligible population, account-level adoption or saturation |
| Title Express rollout | Feb20,2025 lines287–295: pilots precede broad account use; mature clients largely use the service across titles | Marketwide share or the fraction of future growth remaining |
| Delivery | May21 lines471–477: offering changed over12 months earlier, rapid adoption, about$15m YoY facility-cost increase | Exact revenue, job counts, gross margin or allocation of cost between startup and completed jobs |
| Delivery | Sep10 lines522–528: about$17m YoY delivery-cost increase, positive margin description | A quantified20% margin or exact US/insurance allocation |
| Timing | Feb19,2026 lines115–124: retrieval/title services can shorten cycle times | Independent same-quarter revenue recognition of titles or a quantified sales-release effect |

Sources live in `raw/transcripts/call_YYYY-MM-DD.txt`. Source hashes are recorded in provenance.json. Full licensed documents are not copied. The exact quoted-language authority is management where noted; otherwise analyst premise or our calculation.

Insurance ASP versus all-US fee RPU remains a population mismatch. No residual from the price screen is labeled as measured ancillary-service revenue. The aggregate US ASP cited for Q4 also needs confirmation of fee-only scope before use; total-unit and fee-unit mixes differ.

## Delivery arithmetic

For constant product margin m and costs attributable to incremental completed delivery jobs, incremental revenue = incremental cost / (1-m). With all of the disclosed increase attributed to that activity:

| Assumed margin | Q3 conditional revenue increase | Q4 conditional revenue increase |
|---|---:|---:|
| 0% | $15.00m | $17.00m |
| 10% | $16.67m | $18.89m |
| 20% | $18.75m | $21.25m |
| 30% | $21.43m | $24.29m |

At20%, these equal2.09 and2.58 percentage points of prior-year US service revenue, respectively, IF the costs and revenue belong to that geography and recognition period. This is not RPU percentage-point growth and not an observed revenue contribution. Assuming only half the cost increase represents incremental completed jobs halves these figures. All cases are in delivery_cases.csv; margins and attribution fractions are explicitly assumed.

Positive margin on the existing product does not prove positive incremental margin. When margins change, the exact identity is:

`Delta revenue = (Delta cost + prior revenue × (current margin - prior margin)) / (1-current margin)`.

For an invented prior revenue$40m, margin falling20%→10%, and cost increase$15m, incremental revenue is$12.22m, not$18.75m. Wage/fuel/route-length changes and expansion expense create further identification problems. Do not treat the$15m/$17m as revenue floors or additive disclosed sales.

Q3/Q4 figures are year-over-year cost changes, not sequential changes. Their increase from15 to17 does not establish a slowing or accelerating service-adoption growth rate because prior-year bases are unknown.

## Architecture decision

Remove the conceptual dependence on the prototype's unsupported50%×$50 title and10%×$300 delivery assumptions as if they were observations. Do not merely replace them with the20% margin case. Keep them identified as placeholders until a coherent base-level decomposition exists.

The operating forecast should own three linked but separate calculations:

1. Core transaction revenue: sold cohort counts × expected buyer/seller fees. Price and selection use the same underlying vehicle states; numerical dispersion treatment prevents entire synthetic cohorts jumping fee bands together.
2. Title revenue: eligible title-processing activity × contracted revenue per activity, recognized under the applicable contract. Where the service is bundled, do not double count revenue already included in the seller fee. Product volumes may refer to processed titles, not sold units. Mature-client adoption and new-account rollout are distinct drivers; incumbent saturation does not mean no new-account growth.
3. Delivery revenue: external completed jobs × realized revenue per job, with geography, distance/mix and gross/net accounting explicit. Product activity can span insurance and noninsurance sellers. Historical cost increments constrain conditional growth cases but do not identify the starting revenue level. Internal ACV/Copart billings are eliminated on consolidation.

Sum these plus separately identified non-unit services to service revenue; compute consolidated RPU as an output using its disclosed denominator. For internal cohort economics, allocate service dollars only to compatible units. Do not apply all-US delivery revenue exclusively to insurance units. Service cycle-time benefits affect the assignments-to-sales schedule separately; avoid counting faster sales and title activities as two newly created vehicles.

Recognition requires a contract-specific check. The prior FY25 policy groups certain auction-related services at auction, but new stand-alone delivery arrangements may differ. Do not assume every delivery or title activity immediately becomes revenue on its processing date.

## What this means for the research

Delivery can plausibly contribute materially to revenue growth even at modest margins; it deserves a separate schedule rather than being buried in a flat ancillary RPU assumption. The present evidence supports product growth, not a predetermined saturation short. Title Express has qualitative adoption support but insufficient public detail for a numerical marketwide adoption curve. Fee-band mechanics can constrain the core fee response but cannot identify either service's revenue by subtraction.

The next model version should carry transparent component-level assumptions and show their revenue impacts. Prioritize a small targeted disclosure/export for delivery revenue or jobs and Title Express revenue or eligible processed titles before another complex repair calibration. A provider export is useful only if it contains these definitions; no access or coverage is assumed. We can continue with labelled component scenarios if unavailable, but should not claim100% empirical identification.

## Verification and status

Constant-margin identities tested for16 cases; exact margin-change example recorded separately. All data are existing files. No workbook inputs overwritten and no new forecast adopted. Existing service levels remain unsupported; the test constrains what needs explanation rather than resolving the base-dollar decomposition. Catalyst idea stays in its prior note, outside the current core-model task.
