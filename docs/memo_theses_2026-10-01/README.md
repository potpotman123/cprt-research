# Copart memo thesis choices and evidence audit

1 October 2026. The strongest organizing question is **whether a cyclical recovery restores Copart's insured volumes and economics on the timetable in a named forecast**. The evidence does not justify asserting that the industry has permanently ceased to be cyclical. Lead with a recovery that may be slower or less profitable than expected; use aftermarket substitution as a conditional structural extension. Options below are candidates, not established trade recommendations. The user will select theses before the forecast is revised.

## The story that can be supported

Pandemic disruption constrained the flow of new vehicles, while replacement-price and later financing-cost pressure encouraged longer ownership. Insurance-price increases added a separate household cost. Those shocks can leave a persistent stock of older vehicles and changes in coverage/deductibles even after inflation slows. But repairable-claim avoidance, actual physical-damage coverage loss and crash incidence are different channels; none can be inferred solely from a CPI index.

The business backdrop to the selloff includes a large customer loss, catastrophe comparisons and weak claim frequency, alongside resilient auction prices. This is a description of reported operating pressures, not an identified attribution of share-price movements. Copart's September call reported US insurance sold units down7.5%, but assignments up2.3% excluding the lost customer and insurance ASP up3.7%. The positive ex-customer figure is material opposing evidence to a claim of current broad supply collapse. Do not compare assignments directly with sold-unit growth or call the account loss a permanent industry-volume decline.

The bull case deserves its strongest formulation: premiums are easing, claims declines have moderated, retained customers are growing, carrier losses eventually lap, and auction liquidity plus service adoption supports revenue per unit. A bear must show which recovery assumption fails, not just repeat the already known weakness.

Stephens'20 August note says it is **possible** a cyclical issue is being confused with a secular one; it also acknowledges the logic of competition concerns. Its model assumes US fee units −1% in FY27Q1 and+2% inQ2–Q4, with+2% RPU throughout. Attribute this to Stephens at that date, not to every investor. The held material does not establish a general belief that Progressive will necessarily return. Barclays already includes net contract volume losses and25–50bp take-rate pressure; those are not fresh surprises.

Sources: `reports/expectations_sheet_2026-10.md`; `docs/catalyst_assessment_2026-09-29/README.md`; the Stephens source path and hash are in the manifest.

## Fresh arithmetic and competing evidence

BLS's saved transportation CPI file, seasonally adjusted series, provides this level-versus-growth comparison:

| August2026 index | Versus January2020 | Versus August2025 |
|---|---:|---:|
| Motor vehicle insurance | +48.54% | −5.13% |
| New vehicles | +21.22% | +0.57% |
| Used cars and trucks | +29.79% | −2.32% |

[BLS source file](https://download.bls.gov/pub/time.series/cu/cu.data.14.USTransportation). The local file was retrieved in September2026; the latest news-release refresh was blocked at robots403. Calculations use its saved August vintage. These indices are neither household premium quotes nor an income-adjusted affordability measure. They substantiate elevated price levels and actual insurance-price relief at the same time. Do not say there is no relief, and do not infer a coverage cancellation rate from the remaining level gap.

The new [BEA August2026 release](https://www.bea.gov/news/2026/personal-income-and-outlays-august-2026), published30 September, reports real disposable personal income flat month-on-month following+0.3% in July, real consumption+0.6%, and saving rate4.1%. This does not establish falling aggregate purchasing power or an imminent trough. Financial stress in particular households can coexist with those aggregates, but requires distributional evidence and a link to insured losses.

Existing CCC evidence supports a conditional persistence story, not a proved secular collapse: $1,000+ deductibles rose from24.5% to28.1% of **repairable collision claims** between Q4 2024 andQ4 2025. This is not policy penetration. CCC's May2026 recap says Q1 non-comprehensive claim volume was down1.6% versus a5.7% decline for CY2025; different period comparisons, but moderation is real opposing evidence. Earlier Fast Track exposure data did not show falling collision exposure relative to liability in that particular sample/period. [Coverage screen](../fleet_selection_2026-09-28/COVERAGE_RECOVERY_SCREEN.md), [CCC recap](https://www.cccis.com/news-and-insights/posts/crash-course-2026-webinar-recap).

The full supplied CCC age/body panel changes an important claim in the draft. Symmetric rate/mix decomposition, using implied claim weights from total-loss mix divided by frequency:

| Window | Aggregate TLF increase | Within-group contribution | Composition contribution |
|---|---:|---:|---:|
|2020–2025 |2.2883pp |1.3603pp |0.9280pp |
|2024–2025 |0.8854pp |1.0043pp |−0.1189pp |

Composition explains about40.6% of the full-period increase, not most of it; it slightly offsets the latest annual increase. Broad7+ buckets still hide within-bucket aging, and within-group changes do not isolate repair inflation. This is descriptive accounting under the shared-population assumption, not a causal decomposition. It also corrects a cell error: Car age4–6 frequency is19.25%→19.78%, not12.1%→14.8%. The12.1% figure is a total-loss-mix cell in2020, a different denominator. Absolute claims and insured exposure cannot be recovered from the supplied shares alone. See `check.py`, `checks.json`, and the original extraction manifest.

## Short thesis options

### Premium relief does not guarantee an insured volume recovery

**Memo wording:** Insurance-price relief can arrive before the recovery in insured salvage supply. Elevated ownership costs and persistent coverage choices may keep auction-producing claims below the rebound in bullish forecasts.

**Evidence:** price level/growth distinction, high-deductible claim composition, Kyle's mechanism. **Missing:** current matched coverage retention and total-loss counts after premium relief. **Disconfirmation:** covered exposure and comparable total-loss assignments recover sufficiently. **Model:** vary incremental insured claims exposure and its recovery path; keep repairable nonfiling separate. Do not add another age coverage penalty already embedded in baseline.

### The total loss rate can recover faster than the salvage pool

**Memo wording:** A record total-loss percentage is not a unit forecast. If small repair claims disappear, total losses account for a larger share of a smaller claims pool; Copart still needs the numerator to grow.

**Evidence:** accounting identity and existing claims-selection model. **Missing:** paired total-loss and repairable counts for the same population and period; not merely two unmatched growth rates. **Disconfirmation:** rising total-loss counts and assignments. **Model:** model totals directly; pure repairable nonfiling changes reported TLF but produces zero unit/revenue change. This is the explanation supporting the first thesis, not a second additive revenue haircut.

### The customer loss can lap without the economics coming back

**Memo wording:** The anniversary of a lost account improves the comparison; it does not return the account. Replacement volume can restore growth while concessions leave revenue per vehicle below the old economics.

**Evidence:** dated analyst forecasts, disclosed customer loss, RBA automotive gains and pricing incentives. **Missing:** worse retained/won-account economics or timing than analysts already allow. **Disconfirmation:** replacement volumes arrive with resilient net fees. **Model:** carrier allocation and net seller fees by quarter; distinguish same-store activity from easy comparisons. Generic2–3-year vendor contracts do not identify a renewal calendar.

### Strong auction prices are an offset not a guarantee

**Memo wording:** Higher hammer prices can cushion weak units, but they do not mechanically replace lost fee-generating transactions. The relevant test is whether realized fees and paid services offset the unit shortfall.

**Evidence:** fee schedules have steps and percentage tiers; management identifies service expansion; total service revenue depends on units and realized RPU. **Missing:** matched ASP-to-fee transmission, buyer mix and a miss against the already modest+2% Stephens RPU assumption. **Disconfirmation:** observed RPU/service growth offsets volume weakness. **Model:** separate price distribution, fee vintage, seller economics and paid services. Do not infer exact service contribution from an unexplained residual or call the whole fee stream flat.

### Aftermarket substitution could weaken both supply and recycler bids

**Memo wording:** More competitive aftermarket parts could keep marginal vehicles repairable and reduce demand for recycled components. If both occur at scale, the traditional volume-and-price offset weakens.

**Evidence:** observed AM sourcing gains and component availability; tariff sensitivity documents a possible relative-price channel. **Missing:** matched repair savings, actual recycled displacement, marginal total-loss response and auction transmission. **Disconfirmation:** gains mainly replace OEM, recycled contribution holds, or rebuilders/exporters and supply scarcity support bids. **Model:** incremental eligible-component substitution and separate repair/recycler/rebuilder channels. Retain offsets. The source evidence does not establish a rare unidirectional lever or a future tariff repeal.

Recommended structure: combine the first two into the volume pillar; use the third as the competition/economics pillar; use the fourth to test the claimed hedge. Keep the fifth as an explicitly conditional extension unless matched evidence arrives. Three parallel questions are easier to defend than five supposedly independent downside mechanisms.

## Corrections before circulating the draft

- Replace “purchasing power is about to trough” with the narrower price-level/persistent-choice hypothesis. Current aggregate income data do not substantiate the trough.
- Remove the loan-maturity crisis. Kyle said70 months; fully amortizing payoff frees cash. Coverage may change, but no quantified payoff wave or net negative effect is established.
- Remove “both missing claim types raise TLF.” Removing repairable claims raises the ratio; removing total losses reduces numerator and denominator and can lower it. Losing a mixture depends on its relative TLF. Uninsured damaged vehicles can still reach auction by other routes.
- Replace “wrecked beyond repair” with “economically totaled.” The repair-versus-value-minus-net-salvage rule is a simplified economic decision, not a universal statutory test. An insured total-loss deductible is normally netted against proceeds; upfront repair affordability is not automatically missing-total-loss evidence.
- Replace “composition drives the record” with the full decomposition above. Rising repair costs and higher expected salvage genuinely can increase the economic incentive to total; aging does not negate those mechanisms.
- Remove “SUVs total one-third less at every age.” Aggregate rates cannot establish every-age comparisons, and body/value/repair selection remains relevant. Fleet mix is not identical to the total-loss or Copart sold mix.
- Remove the incompatible $747/$1,000 examples at the same auction-price range until buyer class, payment method and schedule vintage match. Crossing fee bands raises fees below$15,000; buyer fees are only one revenue component. A within-band example cannot identify aggregate price elasticity or explain all historical RPU growth.
- Do not treat approximately$491 aggregate cost per car as the marginal cost for every car. Delivery, geography, catastrophe operations, storage duration and fixed-cost absorption matter. Aggregate per-unit cost growth does not prove identical costs across vehicle values.
- Treat a12–13x multiple as a dated broker NTM EBITDA valuation, not today's unspecified multiple.10x is a valuation scenario requiring earnings/cash/perimeter assumptions, not an inevitable outcome of delayed recovery.
- Remove unverified20% annual RFP turnover, IAA cycle-time parity and specific carrier motivations. Generic testimony is not Copart contract data. Barclays'25–50bp concessions and net unit-loss range are already in the held notes; do not call their realization a new consensus discovery.
- The September SUV/pickup price, fuel and Fed claims were not verified by the bounded search. Remove them as dated catalysts pending a compatible primary series; a body-segment wholesale index still needs a bridge to Copart damaged-vehicle ASP.
- Replace the blanket25% tariff with product/origin/date-specific treatment. Current research verified May1 implementation for qualifying Taiwan categories, not national exposure. Tariffs may be absorbed in margins; competitors also pay duties.

## Forecast handoff after thesis selection

Keep the current reference and actuals intact. Each selected thesis needs a named input, quarterly path, source or explicit assumption, timing lag, comparator and kill condition. The volume pillar changes excess covered exposure/total-loss claims; the competition pillar changes allocation and net terms; the price pillar changes auction distributions and fee/service contributions. Avoid adding denominator effects, tariff effects and age effects twice. The CCC level calibration does not validate forward derivatives.

Stephens'Q2 US fee-unit+2% is a concrete benchmark. At0% instead, unchanged RPU and other lines imply a$16.72m Q2 service shortfall versus that broker, not a forecast and not necessarily a miss versus JPM. Definitions must match all-US fee units, not insurance assignments. Exact future earnings dates and surprises remain unverified. No new forecast coefficients or workbook inputs were changed in this memo pass.

## Research scope

Read the attachment, prior handoffs, broker text, CCC cell extraction and prior coverage/parts/fee evidence. Ran six targeted searches spanning official prices/income, credit, claims, wholesale vehicles and insurance; all returned202 without usable results. Retrieved the known BEA primary release after a successful robots check. BLS's release host robots403 prevented a fresh release fetch; reused its already logged September flat-file download. These access failures are not proof that evidence does not exist. No expensive collection, fitting, paid data, agents or outreach. Exact URLs, source hashes and request outcomes are retained in `source_manifest.json`.
