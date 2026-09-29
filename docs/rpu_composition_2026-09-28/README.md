# RPU composition: a slower growth rate is not yet an earnings-revision thesis

28 September 2026. Bounded continuation using existing licensed research, company transcripts and prior fee calculations. No browser collection, OCR, fitting, new agents or spreadsheet changes. This is an expectations and identification check, not a new forecast.

## New finding and decision

**Stephens already assumes 2% U.S. fee RPU growth in each FY27 quarter.** Its August20 pre-results model forecasts U.S. fee-unit growth of −1%, +2%, +2%, +2%, and U.S. service revenue of $863.9m, $852.6m, $931.6m and $845.4m. The quarterly multiplicative revenue identities reconcile within 0.05 percentage points using rounded published numbers.

This is one named analyst's older forecast, not current consensus or an estimate of what the stock price uniquely discounts. Its FY26Q4 was still estimated, and the report predates the ACV announcement. Do not overwrite the September11 JPM or September28 CapIQ benchmarks with it. It nevertheless disproves the premise that all available analysts mechanically extrapolate recent 5–7% RPU growth.

The September11 JPM report describes roughly 5% **historical Q4 US service RPU**, not a 5% FY27 forecast. It says its RPU assumptions improved but the passages inspected do not quantify that forecast. Its September3 report explicitly anticipates that ancillary penetration, ASP inflation and potential buyer-fee increases can outweigh seller-fee pressure. Thus ancillary services are already part of at least one bullish analyst's reasoning; discovering their existence is not differentiation.

## What size of miss would matter?

Hold Stephens' fee-unit path and every other revenue line fixed. Reprice its published U.S. service forecast by `(1 + alternative RPU growth) / 1.02`. This preserves the original table's rounding and avoids borrowing our uncertain insurance revenue allocation or absolute-unit calibration.

| FY27 U.S. RPU growth scenario | H1 revenue difference vs Stephens | Difference / Stephens H1 total revenue | FY revenue difference |
|---|---:|---:|---:|
| +3% | +$16.8m | +0.71% | +$34.3m |
| +2%: published assumption | $0 | 0% | $0 |
| +1% | −$16.8m | −0.71% | −$34.3m |
| 0% | −$33.7m | −1.43% | −$68.5m |
| −2% | −$67.3m | −2.85% | −$137.0m |

The H1 denominator is **$2,361.5m total revenue**; U.S. service revenue is $1,716.5m. A 3% H1 total-revenue miss attributable solely to this RPU line requires approximately **−2.21% RPU growth**, versus Stephens' +2%. That is a hurdle, not our forecast. These differences are not differences against CapIQ; all other branches are deliberately held at Stephens' estimates. A combined unit/RPU miss could be larger, but requires evidence for both and their interaction.

## Composition: what would actually have to happen?

For a compatible population and period, define `RPU = core auction revenue / sold fee units + recognized ancillary revenue / sold fee units`.

Core auction revenue should separately reflect buyer schedule, realized auction-price distribution, seller contract terms and vehicle/customer mix. Ancillary revenue should reflect eligible events, paid adoption, net fees and revenue-recognition timing. Title events and deliveries need not occur one-for-one or in the same quarter as completed fee-unit sales. When that timing differs, the ancillary ratio is a reporting ratio rather than a price charged on each sold car.

Three competing explanations must remain live:

1. **Adoption continues:** more eligible events receive a paid service, raising recognized ancillary revenue and reported RPU. This is supported directionally by management; adoption rates and net revenue are unknown.
2. **Adoption growth slows:** penetration stops increasing, but the existing paid-service base persists. This removes an incremental growth contribution; it does not erase the existing service revenue. If core fees still grow enough to deliver ~2% total RPU, this can meet Stephens rather than miss it.
3. **The service base contracts or is repriced:** fewer paid events, fee reductions/waivers, changed contract scope or adverse recognition timing can reduce service dollars per sold unit. This could produce a larger miss, but the reviewed sources do not demonstrate it. A falling denominator can also raise reported RPU without a higher fee or adoption rate; test service events and sale timing before interpreting that ratio.

For a common denominator, if ancillary services account for fraction `a` of base RPU, total RPU growth is `(1−a) × core growth + a × ancillary-per-sold-unit growth`. This is an accounting decomposition, not permission to assume `a` or recover it from an unmatched ASP series. Delivery's lower margin does not itself lower revenue or prove an RPU slowdown.

## Checks that weaken a simple short

- **Old fee increases may already be in the comparison base.** JPM September3 dates the last buyer-fee increase to November2024. Its analyst question in the May21 call characterizes prior pricing actions as fully lapped. Both are analyst evidence, not an independently effective-dated schedule. Even so, they challenge treating that same anniversary as a new FY27 catalyst. A new fee increase would instead be upside risk.
- **Price effects can cover a modest RPU assumption.** Our existing fixed-distribution screen gives illustrative all-in RPU growth of 1.46–2.45% for a uniform 4.1% auction-price increase. That overlaps Stephens' 2%. It is not a forecast: distribution, seller fees and ancillary levels are assumed, the current schedule is not a historical schedule, and insurance ASP cannot stand in for all-US fee-vehicle ASP. It does show that a service slowdown need not automatically cause a miss.
- **No proved saturation.** May21 management describes further Title Express account penetration; September10 identifies product expansion and potential loan-payoff services. Processing far more titles than a competitor does not establish penetration of Copart's own eligible population.
- **Do not manufacture residual adoption.** All-US fee RPU, insurance ASP, total U.S. vehicle units and insurance assignments are different populations/measures. Purchased vehicles can contaminate apparent ASP/unit comparisons. No historical component allocation has been promoted to observed data here.

## Next evidence, ranked by decision value

1. **An updated post-results broker operating table:** U.S. fee units, U.S. service revenue and implied RPU by FY27 quarter, explicitly excluding/including ACV. This directly measures the hurdle and is cheaper and more precise than inferring analyst beliefs from prose. The local Stephens table supplies the template; an updated Stephens or JPM underlying model/export would be useful. Do not claim a universal 2% consensus.
2. **A measurable source of RPU deterioration or upside:** effective-dated matched U.S. fee schedules; recognized product revenue plus eligible/paid event counts; or a broker bridge with explicit sourced estimates. Buyer invoices or insurer procurement records could measure net fees more directly, but selection, confidentiality/access and sample coverage matter. A platform partner's booking counts would only measure adoption if its Copart population and recognition basis were identified. Current disclosures do not supply these fields.
3. **Only then integrate the joint forecast:** carry the resulting components into the existing units/RPU engine, including service-event timing. Preserve unallocated components. Do not fit an exact service share to force aggregate RPU to reconcile or run a new bulk listing scrape to estimate service usage.

Decision: keep RPU composition as a live explanatory and upside/downside research branch, but **downgrade generic “RPU growth slows as services mature” as a standalone large short**. It needs either higher demonstrated current expectations, evidence of materially negative components, or an independently supported unit miss. Public evidence currently establishes growth mechanisms more clearly than their exhaustion.

## Provenance and reproducibility

Local source root: `/Users/kwu/Documents/ChatGPT/HFAC x Citadel/research/cprt_discovery_plan_2026-09-26/sources/`.

- Stephens August20, file ending `123970131.txt`, printed pp9–10; lines563–565 consolidated forecasts; 632–635 U.S. forecasts. Extraction and SHA256 in `results.json`; `check.py` reproduces `rpu_hurdles.csv`. FY annual published total differs slightly from summed rounded quarters; annual percentage uses published annual total.
- JPM September3, file ending `124204096.txt`, lines194–207: seller pressure, service offsets and November2024 fee-date statement. JPM September11, ending `124345098.txt`, lines37–59: excludes ACV, historical Q4 RPU estimate, qualitative forecast revision. These are separate vintages, not one coherent forecast.
- Company May21 call, `raw/transcripts/call_2026-05-21.txt`, lines396–407: analyst lapping premise and management's directional RPU explanation. September10 call, `raw/transcripts/call_2026-09-10.txt`, lines569–579: explicit refusal to quantify pricing mix, product expansion.
- Prior calculations: `docs/auction_price_test_2026-09-28/README.md`. Prior failed delivery data searches: `docs/rpu_service_build_2026-09-28/DELIVERY_DISCLOSURE_SEARCH.md` and `ALPHASENSE_CHECK.md`; not repeated.

Checks establish extraction alignment and arithmetic, not economic validation. No production forecast inputs changed. The initial extraction correctly stopped on multiple historical fee-unit rows; it was restricted to the financial-table section before calculation.
