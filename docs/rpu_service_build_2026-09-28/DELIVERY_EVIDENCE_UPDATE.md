# Delivery evidence update and model implementation decisions

28 September 2026. Small public-page check and targeted searches of existing transcript and sell-side text. No OCR, bulk listings collection, paid data, or Excel authoring. This note supplements rather than validates DELIVERY_BUILD.md.

## Workflow for Fable

User instruction: keep architecture, evidence, assumptions, executable calculations and outputs in Git. Fable owns spreadsheet implementation and presentation. Read supplied spreadsheets when needed, but do not create or format additional workbooks unless requested. Existing workbooks remain historical prototypes, not automatically adopted forecasts. Seek approval before computationally expensive exploration.

## What the buyer actually does

After buying a vehicle, the buyer can select Copart delivery at payment; the public product page also describes a pre-bid estimator. This is a buyer purchase decision, separate from an insurer's assignment decision. A Progressive-origin vehicle and another carrier's vehicle can both be bought by the same delivery customer. Insurer share affects the available vehicles but does not directly identify shipping adoption.

Source: https://www.copart.com/delivery, accessed 2026-09-28, ordering and benefits sections. This page establishes the workflow, not price, realized average revenue, completed deliveries or penetration. The help-page fetch returned a localized navigation shell and the older domestic-shipping page timed out; neither supplied usable numerical evidence. No actual quote was collected. Public search did not establish an aggregate price or adoption series; this is not proof none exists.

US-origin transactions with an eligible domestic delivery leg are the conceptual population, across seller types. Foreign buyer residence alone should not exclude a US transport leg; actual product eligibility for port/forwarder destinations remains to be verified. Do not import UK delivery prices or ACV's reported average transport distance as Copart US parameters.

## Fee offsets are contractually possible

Source: https://www.copart.com/termsAndConditions, accessed 2026-09-28, US section III.E-F (Automatic Deliveries; Payment for Vehicles Delivered by Copart). The terms allow gate and storage waivers for approved automatic domestic delivery. They do not establish waiver prevalence across ordinary Copart Delivered orders. They also describe circumstances in which storage or failed-delivery charges apply. The product page's general storage benefit is therefore not sufficient to assume every shipment has a complete unconditional waiver.

Model consequence: core fees must reflect any applicable waiver when delivery is selected. If the fee engine already subtracts it, do not subtract it again in the delivery schedule. A hypothetical $300 delivery with a $95 gate waiver adds $205 relative to an otherwise identical sale paying that gate fee, before other offsets. Neither the $300 realized price nor universal waiver eligibility is established. Storage displaced means expected storage revenue in the no-delivery alternative, not the maximum posted daily charge. Any switch from an older Copart shipping product also requires subtracting its displaced revenue.

## Tracing the 20% margin

Existing licensed text files are in `/Users/kwu/Documents/ChatGPT/HFAC x Citadel/research/cprt_discovery_plan_2026-09-26/sources/`:

- JPMorgan, 2026-09-11, report ID 124345098, lines 51-54: approximately 20% is an industry comparison for freight forwarding, not a measured Copart delivery margin. Status: analyst analogy usable as a scenario anchor, not company disclosure.
- BNP Paribas, 2026-09-11, report ID 124357601, lines 256-261: management follow-up attributes more than half of the approximately $30m yard-cost increase to long-haul investments. It does not validate a 20% margin in that passage. Its roughly 400-mile distance at lines 179-182 concerns ACV.
- Barclays, 2026-09-11, report ID 124339246, lines 21-25: repeats approximately $17m delivery-related cost increase; no product margin there.
- Company calls: `raw/transcripts/call_2026-05-21.txt` lines 471-477 and `call_2026-09-10.txt` lines 522-528 provide the $15m/$17m YoY cost increases and qualitative margin language.

The earlier SHORT_THESIS_HANDOFF section 3.3 combines sources in a way that can make 20% look company-confirmed. This note corrects that interpretation. At constant assumed 20% margin, $17m implies $21.25m additional product revenue only if the cost and revenue scopes align and the cost increase corresponds to that activity. It is not an observed number or a revenue floor.

## Minimal calculation architecture

For each quarter and a small number of delivery groups:

`eligible sold vehicles × delivery selection rate × fulfillment rate = completed vehicle deliveries attributable to those sales`

Apply a recognition-timing rule to allocate revenue across quarters; completed jobs are an operational starting point, not a verified recognition policy. Separate one-off and automatic delivery only if evidence supports different fees or uptake. A truck carrying several vehicles does not mean one vehicle delivery: keep the unit of measurement consistent.

`recognized delivery revenue = recognized activity × recognized revenue per vehicle delivery`

`net revenue uplift versus no new adoption = added delivery revenue − displaced existing Copart delivery revenue − incremental waived gate/storage revenue`

Gross versus net presentation remains unverified for this product. If Copart recognizes a net arrangement fee, the customer transport bill is not the revenue input. A gross-cost bridge must use matching accounting scope. Likewise, do not apply the waiver adjustment to a revenue estimate already defined net of those offsets.

Total service revenue includes core auction fees, title services, delivery and other identified components. Delivery waivers belong in either core fees or the service bridge once. No additional fee is added to an already all-in historical RPU. Other branches and the dollar starting levels still require a joint historical reconciliation.

## Cheap arithmetic screen and what it resolves

`delivery_identification_check.py` produces `delivery_identification_results.json`. All prices, denominators and waiver frequencies in this screen are scenarios, not collected quotes or measured rates.

At the conditional $21.25m revenue increment, constant realized prices of $300/$600/$900 imply approximately 70,833/35,417/23,611 additional vehicle deliveries. With a hypothetical one million eligible vehicles and unchanged eligibility, prices and fulfillment, these would represent 7.08/3.54/2.36 percentage points of additional completed-delivery penetration. Thus even accepting the cost bridge does not identify adoption without price and denominator data. These prices are not an empirical range.

For 10,000 newly adopted deliveries at $300 each, gross incremental billing is $3m. Gate waivers on 0%/50%/100% at $95 reduce the net revenue addition to $3m/$2.525m/$2.05m, before storage or displaced old services. This is an implementation/materiality check, not a bearish forecast. Do not mechanically deduct it from the historical cost bridge without establishing consistent margin scope.

## Next evidence priorities and stopping rule

1. Highest value: a reported delivery revenue or completed-vehicle series with period, geography and accounting definitions. Search a small number of existing reports/transcripts first. One such series constrains the model more than many isolated customer quotes.
2. A targeted AlphaSense document mentioning delivery penetration, realized shipping revenue, fee waivers or revenue recognition could help. No new user export is required merely to repeat statements already in the repo.
3. If no aggregate disclosure exists, a few comparable pre-bid quotes can test whether a candidate price is plausible for specified routes and vehicles. They cannot estimate national realized average revenue without actual route weights, booking rates, refunds and recognition scope. Do not escalate to mass scraping to solve a problem it cannot identify.
4. Until then preserve explicit scenarios and missing base levels. Neither saturation nor an adoption-driven short is established. The concrete improvement here is correct population, source status and avoidance of additive-fee double counting; no new quarterly forecast is adopted.
