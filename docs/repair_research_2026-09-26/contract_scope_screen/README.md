# Contract-scope source and arithmetic screen

2026-09-26 US Eastern. Bounded local-only work: inspected supplied Barclays 25-Aug-2026 note, Figure 1 on PDF page 4, and surrounding narrative; reconstructed arithmetic. Extracted one embedded image and composited its transparency on white to read labels. No OCR, new scraping, provider purchase, or workbook changes.

## Result

Do not promote broad retained-account repricing as a newly discovered source of downside. The analyst's published contract-win EBITDA is consistent with a discount applied to a much larger carrier base than incremental assignments. That does not verify the actual contract, but it substantially weakens the novelty claim. The modeled contract win remains EBITDA-positive.

## Source inputs and interpretation

Barclays Figure 1 (analyst estimates, not disclosed terms): Copart US automotive insurance volume 3,336.7k; Insurer B volume 621.9k; GTV/lot $3,850; seller commission 4%; discount 20%; total services revenue/lot $950; incremental volume 120-130k; cost-of-services increase shown as ($40m); F2027 EBITDA impact +$60m. We interpret the cost increase as a $40m reduction in EBITDA. Do not mistake 20% off a 4% commission for 20 percentage points off total service revenue.

The table labels insurers A/B, not GEICO/Progressive. Earlier project notes associate them with those carriers, but this arithmetic does not require or independently establish the identity.

## Reconstruction, USD unless stated

Using 125k midpoint incremental units:

- Concession per affected vehicle = 3,850 * 4% * 20% = 30.80.
- Added service revenue = 125,000 * 950 = 118.750m.
- Contribution before concession = 118.750m - 40m = 78.750m.
- Concession on table carrier base = 621,900 * 30.80 = 19.15452m.
- Incremental EBITDA = 78.750m - 19.15452m = **59.59548m**, rounding to the published approximately 60m.
- If only incremental vehicles are discounted, gain = **74.900m**.
- If 621.9k is pre-award retained volume and new units also receive the discount, gain = **55.74548m**.

Thus broad carrier repricing is strongly suggested by the table arithmetic. However, the static image does not expose formulas or define whether 621.9k is pre/post award. Do not claim to have verified exactly how all retained/new assignments are treated. The last alternative implies only 3.85m more cost than the best-fit reconstruction, not a new large hidden loss.

Cross-check RBA block: 245k new vehicles * $850 - $80m additional cost - 1,003k carrier vehicles * $3,642 GTV * 4% commission * 15% discount = $106.332m versus published $105m (inputs and impact rounded). Same broad-base interpretation is consistent there.

## Break-even and materiality

With Copart's other Figure 1 inputs fixed, the concession on its 621.9k carrier base would need to be $126.63/vehicle, or **82.23% of the assumed $154 seller commission**, to erase the contract gain. A 40% commission discount still yields +$40.441m. These are conditional bounds; no likelihood is assigned, and neither costs nor volumes are held fixed by an actual contract.

Contract loss block: 240-250k lost vehicles, $950 service revenue/lot, $80m avoided cost, published EBITDA loss $150m. Midpoint reconstruction gives $152.750m lost contribution. Combined reconstructed gain/loss is -$93.155m; published blocks net to -$90m. This is an illustrative combination of labeled source blocks, not a new synchronized fiscal-quarter forecast. Timing labels differ (F2027 gain versus 2026 loss). The note also cuts FY2027 EBITDA by $90m, but that revision includes G&A, volume and other model changes, so numerical coincidence is not an exact reconciliation.

Conclusion: the substantial modeled loss comes from the combination of lost business and offsetting wins, not a negative-profit contract win. The note already reduces estimates. Do not add its fee or contract losses again to a baseline containing them. A differentiated short requires actual worse economics, timing or carrier composition than a dated named forecast, not rediscovery of its assumptions.

## Implications for the bottom-up supply build

Construct US insurance auction supply by carrier, then age/body cohort where defensible:
insured exposures * claim frequency * total-loss probability * allocation to Copart, shifted from assignment to completed-sale timing. Match cohort fee/cost assumptions to that same population. Policy counts require conversion to vehicles/exposure, and premium share is not vehicle share.

Fleet hypothesis: average fleet age can rise without an equivalent increase in insured, claiming vehicles crossing the steep part of the total-loss curve. Cohort size, survival, coverage and driving matter; the marginal effect of another year depends on age. Existing local CCC decomposition finds little 2024-25 age-weight contribution, not an independently established imminent negative demographic inflection. Do not subtract this again from a TLF forecast that already incorporates it.

Carrier hypothesis: industry total-loss growth can be concentrated at carriers whose allocation to Copart is low. Copart then underparticipates even with no new contract loss. Hold within-carrier allocation fixed to isolate this carrier-composition effect; separately model awarded/lost assignments and their timing. Once a one-time contract loss laps, continuing disadvantage requires differential carrier exposure/claims growth or another ongoing mechanism. Do not extend a one-time YoY drag indefinitely.

Body-mix hypothesis: higher values per vehicle do not ensure higher revenue per insured exposure because transaction frequency and fee schedules intervene. Existing -0.16pp working result remains assumption-dependent and small. No unconditional net-negative assertion is justified by this screen.

## Files and source

- results.json and calculate.py reproduce the arithmetic, including both volume-scope interpretations and RBA cross-check.
- barclays_figure1.png is a local rendering of the supplied research table; original PDF remains unchanged.
- Source: `../../sources/2026-08-25-RBA.TO-Barclays-U.S. Auto Retail CPRT vs. RBA Salvage Auction Wars-124041014.pdf` in the workspace research directory (copied report folder uses the absolute source below).
- Absolute PDF: `/Users/kwu/Documents/ChatGPT/HFAC x Citadel/research/cprt_discovery_plan_2026-09-26/sources/2026-08-25-RBA.TO-Barclays-U.S. Auto Retail CPRT vs. RBA Salvage Auction Wars-124041014.pdf`.
- Latest local age-method audit: adjacent `../first_pass_findings.md` in workspace; source-population limitations apply.

No probability of concession scope or new short price target estimated. No present-day market/consensus update undertaken; this is a dated source screen.
