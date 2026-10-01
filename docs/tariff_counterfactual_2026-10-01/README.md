# Aftermarket adoption without tariffs

1 October 2026. Removing tariffs could make imported aftermarket parts more competitive, but the premise that tariffs have substantially suppressed adoption is not established. Supplier inventory, margins and competitor prices matter. The reproducible sensitivity gives an illustrative **0.84–1.69 percentage point increase from a 25% physical aftermarket share** when half/all tariff dollars reach buyers and the assumed relative-price odds elasticity is two. Neither the elasticity nor national exposure is measured. Zero incremental adoption remains possible; stronger response assumptions produce larger effects.

## Evidence and the counterfactual

Existing CCC extraction gives aftermarket replacement spending shares of21.0% in2024 and22.7% in2025. Its rounded counts imply physical shares near23.5% and25.4%, with an increase bounded0.92–2.79pp under common-population/rounding assumptions. This is observed adoption despite tariffs, not a tariff treatment effect. Reuse `docs/repair_salvage_execution_2026-09-28/MIX_SEGMENTATION.md` and `docs/aftermarket_transition_evidence_2026-09-29/README.md`; do not add the counterfactual below to historical growth as a forecast.

PartsTrader's February11,2026 article describes its fixed basket of high-volume collision parts and reports OEM/recycled inflation exceeding aftermarket inflation following tariff announcements. It attributes muted aftermarket pricing partly to advance inventory purchases and competition. It gives a **hypothetical $60 acquisition cost, $200 list price and $9 duty at15%**. This is not a measured national customs-to-delivered-price ratio or matched installer transaction. Its commentary on tariff dates is not used as legal implementation evidence. The source is a marketplace vendor with a commercial interest in competitive bidding; it shares Enlyte ownership with Mitchell, so it is not independent corroboration of Mitchell data.

[PartsTrader source](https://www.partstrader.com/why-parts-inflation-looks-so-uneven/)

CBP's 27 May 2026 guidance verifies a combined 15% Column 1/Section 232 rate for specified qualifying Taiwanese automobile parts with ordinary rates below 15%, effective for entries from 1 May 2026. Where the ordinary rate is at least 15%, the guidance adds no Section 232 duty; it does not lower that ordinary rate. This is a verified dated implementation, not a complete audit of every tariff classification or subsequent policy change. Product classification, eligibility and entry dates govern treatment; a headline country rate is not a universal rate for all collision parts. China cannot be assigned the Taiwan rate. The sensitivity uses15% as a specified hypothetical affected-basket duty and separately distinguishes15%→0,25%→0 and25%→15. Zero means removal of the entire modeled duty; repealing only an incremental tariff could leave ordinary duties. A2.5% residual-duty example is explicitly assumed, not a verified tariff classification.

[CBP Taiwan guidance](https://content.govdelivery.com/accounts/USDHSCBP/bulletins/4193d0a)

## Calculation

Define an otherwise identical eligible part with untaxed delivered price P0, customs value C, duty t, and dollar pass-through λ. Assume `P(t)=P0+λ×C×t`, holding other costs and dollar margins constant. This is an explicit pricing convention, not a claim that markups cannot amplify pass-through. Supplier concessions, currency, rebates, freight and long-run margin policy could change it.

Using P0=$200 and C=$60 adapts the source's illustrative list-price example into a hypothetical delivered-price basket:

| Tariff-dollar pass-through | Price with15% tariff | Price after removal | Price reduction |
|---|---:|---:|---:|
| None | $200.00 | $200.00 | 0% |
|25% | $202.25 | $200.00 |1.11% |
|50% | $204.50 | $200.00 |2.20% |
|100% | $209.00 | $200.00 |4.31% |

The supplier may receive margin relief even when prices and adoption do not change. A15% import tariff is therefore not automatically a15% decrease in the buyer's price when removed. With a customs-value ratio of60% rather than30%, the assumed50% pass-through case gives4.31% price relief. This demonstrates that the cost base is material and remains unidentified.

To translate price into adoption, use a transparent two-alternative sensitivity:

`odds_after = odds_before × [(AM price_after / AM price_before) / (competitor price_after / competitor price_before)]^(−ε)`

`share_after = odds_after / (1 + odds_after)`.

The baseline25% is an illustrative round number near the historical physical-share calculation, not a matched eligible basket calibration. ε is an **assumed elasticity of aftermarket-versus-other sourcing odds**, not a fitted demand elasticity. At ε=2, a1% relative-price reduction approximately raises sourcing odds2%, not aftermarket share2 percentage points. Assume a fixed replacement market, eligibility and competitor prices for the table:

| Price pass-through | AM price reduction | Share gain at ε=1 | Share gain at ε=2 | Share gain at ε=4 |
|---|---:|---:|---:|---:|
|0% |0% |0pp |0pp |0pp |
|25% |1.11% |0.21pp |0.42pp |0.85pp |
|50% |2.20% |0.42pp |0.84pp |1.71pp |
|100% |4.31% |0.83pp |1.69pp |3.44pp |

There is no basis here to prefer ε=2 as an empirical best estimate. The table is an assumption map, not a confidence interval or universal upper bound. Under the middle illustration, share25%→25.84% means3.37% more aftermarket units in a fixed-size market, not0.84% more units. A5pp gain to30% would require ε≈11.29 at half pass-through or5.71 at full pass-through under this pricing example. That is the response a large “masked transition” claim must substantiate.

If only half the market is affected and both submarkets start at25%, the0.84pp gain becomes0.42pp overall. This mixture is illustrative; national customs and eligible-claim weights are not supplied. Certification, insurer rules, patents, fitment and availability can prevent switching regardless of price. New product investment after tariff relief is a separate longer-run channel with no quantified response here.

## Competing prices and measurement

In the middle illustration, if competitor prices also decline1%, AM gains only0.46pp. If they fall3%, more than AM's2.20% reduction, AM share **falls0.31pp**. PartsTrader's OEM/recycled price observations are a reason to test these alternatives, not proof of either exact counterfactual. Broad tariff removal affects OEM components and pricing incentives too; recycled pricing can respond to OEM competition even without paying a new-parts import duty.

The historical25%→15% step produces0.55pp under the middle assumptions. A full25%→0 scenario produces1.41pp. These do not establish actual past adoption effects or forecast a new policy event. A change already effective before October2026 cannot be called an unannounced future catalyst, although inventory and contracting could delay transmission.

Track quantities separately from spending: holding quantities fixed, the2.20% AM price reduction takes an initial22.7% AM dollar share to approximately22.31%. Cheaper parts can lower spending share even with unchanged physical adoption. With actual substitution, both prices and quantities must be recalculated; neither a dollar-share series nor nominal supplier revenue identifies installed units alone.

## Implication for Copart

The incremental physical mix change must be split into OEM, recycled and other displacement. OEM-to-AM substitution may lower repair bills; recycled-to-AM substitution may reduce dismantler demand. Neither channel equals a proportional reduction in total-loss vehicles or salvage bids. Lower repair costs can also support rebuilders' bids, and OEM competitive price cuts may affect repair costs without much AM share movement. The saved aftermarket model has unmeasured donor and auction transmission inputs; multiplying them onto the new assumed elasticity would create an apparently precise but unvalidated Copart revenue number.

No central forecast or prior bridge input was changed. The new calculator preserves a tariff layer that can be used once component-level prices and exposure are available. The minimum useful empirical test is a fixed-part/vehicle panel around a verified tariff change, including tariff classification, origin, customs value, inventory vintage, net delivered quotes, OEM/recycled competing quotes and fulfilled source quantities. Compare affected parts with credible untreated components, check pretrends and account for insurer-policy changes. A before/after aggregate adoption rate alone cannot isolate the tariff effect.

## Scope and checks

Six targeted queries covered the distributor, industry association, marketplace and official trade-policy sources; prior CCC and aftermarket work was read first. Primary page retrievals and robots checks are logged separately; search discovery and limitations are in `source_manifest.json`. No paid collection, OCR, fitting, agents or outreach. Stopped at the missing pass-through, origin weights and substitution elasticity rather than estimate them from aggregate trends.

Run `python3 docs/tariff_counterfactual_2026-10-01/calculate.py`. Outputs are `sensitivity_grid.csv`, `alternative_cases.csv`, `five_point_hurdle.csv`, and `results.json`. Zero-duty, zero-exposure, equal-relative-price, share bounds, monotonicity and reverse-solved hurdle checks pass. These validate arithmetic, not economic identification.
