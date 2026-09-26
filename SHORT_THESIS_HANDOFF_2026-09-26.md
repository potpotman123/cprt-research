# Copart (CPRT) — direction decided: SHORT on a 3–6 month horizon. Full context for the next model

*Written 2026-09-26 at the end of the third session. This file is the entry point for whoever continues the work (the owner's
next model). It restates the business, the model, every experiment run and how it performed, the sell-side reference numbers,
the decision to pitch a short, the weaknesses in the evidence, and the next steps in order with the reason for each. Terms
are defined where first used. Every number carries a label: MEASURED (computed from public data by a committed script),
FITTED (a parameter chosen so a model reproduces measured data), ASSUMED (our judgement), VERIFIED (read in a filing, a
transcript or a fetched page), UNVERIFIED (not yet found in a source on disk).*

---

## 0. How to work in this repository

- Read `HANDOFF.md` §0–§2 and §5 (how the model doing this work fails), then this file, then `findings.md` Addenda 22–23, then
  the report under `reports/` for whatever you touch. `MODEL_BLUEPRINT.md` is the model architecture. `docs/AGE_CURVES.md`
  is the fleet-age method.
- Rules that do not bend (the owner's): every HTTP request goes through `scripts/prov.py`; read `robots.txt` first and obey it;
  at least 2 seconds between requests to one host; no logins, no paywall or challenge-page workarounds; report a blocker with
  its status code instead of working around it; label every number as above; commit each result when its report is done;
  state what each result implies for both directions even though the direction is now chosen.
- Licensed files never enter git: `raw/` is gitignored and holds the earnings-call transcripts, the sell-side PDFs
  (`raw/sellside/upload_2026-09-26/`), the HLDI insurance-loss sheets and the IHS fleet tables. Numbers extracted from them are
  committed with a provenance header; the files are not.
- The owner welcomes disagreement. If a step below looks wrong, say why and propose the alternative before doing it.
- Dates (UNVERIFIED, from a brief without a cited source; confirm): preliminary submission October 2, finals October 22–24,
  2026. Copart reports its August–October quarter in late November, after the finals.

---

## 1. The decision and why

**Pitch a short with a price target about 20% below the current price ($27.59 on 2026-09-26), for the next two reported
quarters, with a stated set of conditions under which the view flips to long.**

The reason is the timing of the evidence, not its balance. Everything that supports a long is dated after the quarter ending
January 2027: the loss of the Progressive account drops out of the year-on-year comparison only in May–July 2027; the GEICO
volume gain is fully visible only in the November–January quarter; the industry total-loss increase implied by repair costs
reaches Copart's reported cars only after the account drag is out of the comparison. Everything that supports a short lands in
the two quarters reported in late November 2026 and late February 2027: cars sold still down 4–6% from the Progressive loss,
revenue per car slowing because the extra growth above price is fading and used-car prices are falling, cost per car up
double digits with management committed to further investment, the ACV acquisition closing with a reduction in earnings per
share on ACV's own plan, the share buyback paused to pay for it, and consensus earnings estimates for fiscal 2027 still above
every model published after the last results.

The differentiated part of the short is not the price target, which coincides with Barclays'. It is the mechanism: Barclays
reaches $25 by assuming continued loss of market share to IAA. We concede the share point (the loss was one account, and it is
dated) and reach a similar price through revenue per car and margin, using a fee model estimated from Copart's own data.

Probability judgement (ASSUMED): 55–60% that the stock is lower at the February 2027 report than today, adjusted for the
market. Close to even on a twelve-month view, where the same mechanisms turn positive.

---

## 2. The business, from the bottom

When an insured car is damaged, the insurer decides whether to repair it or to pay the owner the car's value and take the car.
A car the insurer takes is a **total loss**. The insurer sends it to an auction company. In the United States there are two:
Copart and IAA (owned by RB Global, ticker RBA). Copart tows the car to one of about 200 US yards, obtains a salvage title from
the state, lists it online and sells it in a weekly online auction to dismantlers, repairers, dealers and exporters. Buyers
outside the US took 38.2% of US cars and paid 45.7% of the dollars in fiscal 2026 (management on the September 10 call,
VERIFIED via the BNP note). Copart sells about 4 million cars a year worldwide. About 80% of its US cars come from insurers;
the rest from dealers, rental fleets, banks and charities. Copart's fiscal year ends July 31; "FQ1 FY27" is August–October 2026.

**How Copart is paid on an insurer's car.** Three kinds of fees:
1. **Buyer fees**, paid by the buyer. Published on Copart's website as a table: a fixed dollar amount per sale-price band up to
   $15,000, then 7.25–7.50% (5.75–6.00% for high-volume licensed buyers) above it, plus a gate fee ($79 clean title / $95
   other), an environmental fee ($15) and an online-bid fee ($39–160). IAA's table is identical to Copart's non-clean-title
   table at every band (`reports/E6_fee_grid.md`, VERIFIED). Copart last raised buyer fees in November 2024 (JPMorgan
   2026-09-03, VERIFIED as a quote); IAA's current table is dated November 4, 2024.
2. **Seller fees**, paid by the insurer, set in each insurer's contract. Neither company publishes them. When an insurer moves
   cars from one company to the other it usually obtains a lower seller fee. Barclays estimates Copart's 2026 GEICO win cost
   Copart 0.25–0.50 percentage points of its overall fee rate; JPMorgan's channel checks say a peer's seller fees on one large
   carrier are close to zero against about $100 per car of variable cost.
3. **Service fees**: towing, storage, title processing ("Title Express"), and long-distance delivery of the car to the buyer.

All three together are **service revenue**. Copart also buys some cars and resells them (**vehicle sales**, thin margin).

| fiscal 2026 (Aug 2025–Jul 2026), $ millions, VERIFIED (8-K) | |
|---|---|
| service revenue, US | 3,388 |
| service revenue, international | 581 |
| vehicle sales | 697 |
| total revenue | 4,666 |
| gross profit | 2,083 |
| facility (yard) operations cost | 1,756 |
| EBITDA = operating profit + depreciation and amortisation | 1,882 |
| net income / earnings per share | 1,480 / $1.55 |
| cash and investments before the ACV payment; debt | ~4,500; 0 |
| diluted shares (millions) | ~930 |

---

## 3. The model: revenue = cars × revenue per car, each built from parts

Copart discloses only percentage changes in cars sold and in average sale price, on its calls, never levels. So the model
starts from fiscal 2026 revenue and applies percentage changes: next period revenue = base revenue × (1 + change in cars) ×
(1 + change in revenue per car), by segment (US service, international service, vehicle sales).

### 3.1 Cars sold (US insurance)

US insurance cars = industry accident claims × fraction of claims that become total losses × Copart's share of total losses.
In percentage-change terms the three add.

**Claims.** Progressive states its accident-frequency change every quarter in its 10-Q. MEASURED from 47 filings
(`data/csv/pgr_frequency_quarterly.csv`): −9/−8/−5% in 2024, −3/−4/−2% in 2025, 0/−2% in the first half of 2026. Claims are
roughly flat now. Higher deductibles remove small claims; the share of claims with a $1,000+ deductible follows insurance
prices with a 4–6 quarter lag and should stop rising around mid-2027 (`reports/E2_affordability_claims.md`). Input for the
next two quarters: 0 to −2%.

**Total-loss fraction (TLF).** CCC, a claims-software company, publishes it: 14.0% in 2013, 23.1% in 2025, 23.3% cited by
management for the latest quarter (`data/csv/ccc_tlf_annual.csv`, `ccc_tlf_quarterly.csv`). Two drivers:
- The **repair-versus-value gap**: the insurer totals a car when repair cost exceeds a threshold share of the car's value, so
  the fraction rises when repair-price inflation exceeds used-car-price inflation. MEASURED on 27 CCC quarters: each 1
  percentage point of gap raises the fraction 0.08 points the following quarter, intercept +0.6 points a year, R² 0.81
  (`scripts/analysis_20260911.py`, `data/csv/tlf_calibration.csv`). The gap was +15.7 points in mid-2024, +2.3 in
  September 2025 (the period that hurt Copart), +8.3 in mid-2026, implying about +1.3 points of TLF over the next year.
  Caveat: the repair-price index is running about 3 points above its measurable inputs (wages, parts), so the gap may narrow
  (`reports/E3_repair_labour.md`); used-car values are set to soften on a known schedule, adding +0.2/+0.4 points in
  FY27/FY28 (`reports/E4_offlease_values.md`).
- **Fleet age and body mix**: CCC's own age buckets show fleet ageing added about +1.5 points in 2020–22 and nothing since
  2023 (`reports/CCC_age_buckets_2026.md`, MEASURED). The rising share of trucks and SUVs lowers the fraction about 0.13
  points a year through 2030, because a truck is worth about 1.5× a car of the same age and is repaired more often
  (`reports/E1_step4_6_body_propensity.md`; direction MEASURED, size FITTED/ASSUMED, range −0.08 to −0.18). Net demographic
  drift about −0.1 points a year.

**Copart's share.** Progressive moved almost all its cars from Copart to IAA between April and July 2026. Copart's US insurance
cars fell 7.5% in May–July 2026; excluding that one customer they rose 2.3% (management, VERIFIED). The drag persists in each
quarter's year-on-year comparison until May–July 2027. GEICO moved some cars to Copart in 2026, worth about +1 percentage
point of US cars if fully won (Stephens). No share loss is visible before the account in the six-quarter decomposition
(`data/csv/units_decomp_panel_v2.csv`).

**Forecast for August–October 2026:** claims 0 to −2, TLF +1, Progressive −7, GEICO +1 → US insurance cars **−4 to −6%**
(ASSUMED composition of MEASURED parts). Sell-side models published before the results assumed −1 (Stephens) to −3 (Barclays).

### 3.2 Revenue per car

**Average sale price** follows used-car prices: MEASURED on 15 quarters, price change = 0.60 × used-car CPI change + 3.2
points (`data/csv/recovery_divergence_quarterly.csv`, `ASP_Drivers` tab). Of the 3.2 points, about 1.0 is the cars being
newer model years each year (MEASURED, `data/csv/asp_vintage_effect.csv`) and about 0.7 is the shift toward trucks and SUVs
(ASSUMED value ratio 1.50, `reports/E8_body_value_ratio.md`); the rest is unexplained. Used-car CPI is about −3% year to date
in 2026, so the chain gives average price +1 to +2%.

**Service revenue per car** follows price: MEASURED on 17 quarters, change = 0.51 × price change + 4.1 points, R² 0.61,
95% interval on the slope 0.29–0.73, effective sample about 6 because residuals are autocorrelated
(`data/csv/elasticity_rebuild.csv`). The 0.51 is produced independently by the buyer-fee table's shape: fixed dollars
dominate at low prices, so fees rise about half as fast as prices (`scripts/experiments/e6_fee_grid_simulation.py`).

**The point the short turns on.** The +4.1 points is an average over quarters containing fee increases. The November 2024
increase entered the year-on-year comparison in November 2024–January 2025 and left it a year later; the quarters after that
were inflated by hurricane comparisons. The May–July 2026 quarter is the first with neither effect: US fee revenue per car
+3.5% on US insurance price +3.7% gives an extra of about 1.6 points; global service revenue per car +4.4% on global price
+3.5% gives about 2.6 points. With price at +1 to +2%, service revenue per car for the next two quarters is about **+3%**
(0.51 × 1.5 + 2). Stephens models US revenue per car at +2.0% each quarter of fiscal 2027; JPMorgan raised its number after
the results and headlined "resilient RPU"; the repository's earlier long case assumed +4.5 to +5.5%. A further item to verify
from the transcripts (on the owner's machine): Stephens' KPI table shows US gross profit per fee car −9% in February–April
2026 while revenue per car rose, consistent with the added revenue being low-margin delivery services.

### 3.3 Costs

Yard operations (towing, labour, storage, title processing) were $1,756 million in fiscal 2026 and are mostly fixed per yard,
so cost per car rose 14.2% in May–July 2026 when cars fell. About half of the $30 million year-on-year rise in yard cost that
quarter was spending Copart chose to add, mainly long-distance delivery (about $17 million, at about a 20% margin); the rest
was freight and one-time accruals (BNP after speaking with the CFO; Barclays; JPMorgan). General and administrative cost was
about $430 million. Management said it will tighten costs and will keep investing. Consolidated gross margin was 41.8% in
May–July against 46.5% a year earlier.

### 3.4 ACV

Copart is buying ACV Auctions (an online dealer-to-dealer used-car auction) for $1.9 billion cash, closing by December 2026.
ACV's own plan, filed in its SC 14D-9 (`reports/E10_filings.md`, VERIFIED): revenue $964M / EBITDA $123M in 2027; unlevered
free cash flow −$97M, −$69M, −$8M in 2027–29. Copart earns about 4% on cash, so the payment forgoes about $75M a year of
interest income, more than ACV's 2027 operating profit. On ACV's plan the deal reduces Copart's earnings per share in fiscal
2027 and 2028; Copart says neutral in fiscal 2027 and accretive in fiscal 2028, which requires unquantified cost savings.
A rival bid at $11–12 was withdrawn; the reverse termination fee is $115M.

### 3.5 Valuation

At $27.59: market value about $25.5 billion; enterprise value (market value minus net cash) about $21 billion before the ACV
payment and $22.9 billion after; 11.2× fiscal 2026 EBITDA before, 12.2× after; about 17× fiscal 2027 consensus earnings.
Ten-year average forward price-to-earnings 27–29×; forward EV/EBITDA range over 20 years 7–25×.

---

## 4. The experiments run in September 2026 and how each performed

Specified in `NEXT_STEPS_FOR_OTHER_CLAUDE_FABLE.md`; scoped in `reports/00_scoping_2026-09-26.md`. The standard set for each:
a named driver you can measure, a reason it moved when it did, a reason it will move next, and a consequence for a Copart
number that consensus does not contain.

| id | question | result | verdict | effect on the model |
|---|---|---|---|---|
| E1 | do trucks total differently from cars, and what does the truck-heavy fleet do to supply and price | trucks total ~0.72–0.76× as often at ages 8–12; body mix lowers TLF ~0.13 pts/yr to 2030 and lifts price ~0.7 pts/yr; two-body fleet model matches Copart's listed truck share within 1–3 pts where the one-body model missed by 4–6 | passed; small magnitude; not a 3–12 month driver | demographic TLF drift from +0.16 to ≈ −0.1 pts/yr; body-mix column on `ASP_Drivers` filled |
| CCC buckets | read CCC's total-loss rate by age group 2020–2025 | ageing added +1.5 pts in 2020–22, ≈0 since; the 2022–25 rise of +4.2 pts was within-age (the repair/value cycle) | passed; the most useful new fact | replaces the fitted age curve; removes "ageing fleet" as a forward driver |
| E2 | does insurance affordability drive the claims term with a lag | accident-frequency channel: no lag structure once 2020–21 is excluded (killed); deductible channel: real, 4–6 quarter lag; claims decline ending (0/−2% in 2026 H1) | half | claims input from −3/−5% to 0/−2%; repairable-claim recovery is a 2027 H2 event |
| E3 | is repair inflation labour scarcity | body-shop wages at the all-private rate, jobs flat, parts +2.4%, repair CPI +6.6%: the index runs ~3 pts above inputs | mechanism killed; a bound produced | repair-CPI reversion scenario: −0.25 pts TLF/yr |
| E4 | does off-lease supply move used-car values on a schedule | growth form: no; level form (pre-2020): elasticity −0.175; known stock path → +0.2/+0.4 pts TLF FY27/FY28 | passed; small | used-value row with a calendar |
| E5 | is listed inventory falling because titles process faster | state-level dispersion mean-reverts, no titling structure | killed at the screen | listed-inventory decline stays a volume signal |
| E6 | read the fee tables | Copart and IAA buyer-fee tables identical band for band; convexity gives elasticity 0.4–0.5 | passed on mechanism; history undated except Nov-2024 | mechanism behind the 0.51 |
| E7 | export demand and the dollar | not run (FRED unreachable); international buyer share now known (38.2% units / 45.7% dollars) | open | a level for the price residual |
| E8 | truck vs car value at the same age | 1.58 at age 5; 1.50 used | done | input to E1 |
| E9 | IAA yard congestion | untestable from public data | dead | none |
| E10 | read ACV's filing and the FY26 10-K | ACV plan read (above); 10-K not filed as of 09-26 | passed on ACV | ACV block quantifiable; base year still on the 8-K |

Overall: four produced a driver with a calendar (E1, E4, E6, E10), three killed a mechanism (E2 frequency, E3, E5), one is
open (E7). The batch moved the pitch from "cars will recover" to "revenue per car is the only differentiated leg", and this
session's read of the clean quarter says that leg is fading, which is what makes the near-term short.

---

## 5. Quality of each component (how tight, tested, believable, reproducible)

| component | precision | tested out of sample | mechanism believable | reproducible by a judge | proprietary |
|---|---|---|---|---|---|
| TLF cycle (gap regression) | medium (t > 10 but effective n ≈ 6 on the preferred variant) | yes: MAE 0.39 pts; one live test within 0.4 pts | high | high (public charts, BLS) | no (Stephens prints the same gap as a chart) |
| TLF demographic baseline (two-body) | low (assumed dispersion and depreciation; range −0.08 to −0.18) | partly (listing match; 2020/2025 age shares) | medium-high | high | yes |
| claims term | low | no | medium (correlation, not causal) | high (Progressive 10-Qs) | no |
| share term | n/a | history only (management disclosure) | high | medium | no |
| revenue-per-car slope and intercept | low (interval 0.29–0.73; effective n ≈ 6) | in-sample only; misses FY26Q4 by 0.8 pts | high (fee table reproduces the slope) | medium (hand-transcribed calls, 15/15 cross-checked) | yes |
| price chain (CPI → price) | low; residual unstable | weak (1.4-pt miss on the one quarter checked) | medium | high | partly |
| cost leverage | medium | no | medium (elective spend not yet separated) | high | partly |

Known weak points, stated plainly: the +4.1 intercept is an average over fee increases and is not yet decomposed; the
dispersion parameter in the body-mix work is an assumption bracketed by two bounds; the frequency ratio in E1 was adjudicated
with Copart's own listings (a third-tier source) against an adjusted HLDI figure (first-tier); seller fees are not published by
either company and the model has no series for them; the FY26 base year is on the 8-K until the 10-K is read; Copart's
cars-sold series is from transcripts, not filings.

---

## 6. Sell-side reference (13 notes, June–September 2026; `reports/street_reference_2026-09.md`, `data/csv/street_estimates_2026-09.csv`)

| broker | date | rating | target | basis | FY27 EPS | FY27 EBITDA $M |
|---|---|---|---|---|---|---|
| Barclays | 09-11 | Underweight | $25 | 10× FY26 EBITDA; downside $21 at 8×; upside $54 | 1.56 | 1,916 |
| Stephens | 08-20 (pre-results) | Equal-Weight | $35 | 13.5× FY27 EBITDA | 1.67 | 2,033 |
| JPMorgan | 09-03 → 09-11 | Overweight $40 → Not Rated (advised ACV) | none | 15× FY28 EBITDA / 23× EPS | 1.57 | 1,891 |
| BNP Paribas | 09-11 | Outperform | $40 | 17.5× FY29 EBIT | 1.62 | 1,942 |
| HSBC / Jefferies / Equisights | Sep / Jun / Sep | Buy | $46 / $45 / $43 | various | not stated | not stated |

Bloomberg consensus fiscal 2027 EPS on 09-10: $1.68; every model published after the results is $1.56–1.62. Rating count
8 Buy / 4 Hold / 1 Sell. Reference bear: Barclays. Reference base: Stephens (only full quarterly model with unit and
revenue-per-car assumptions; its post-results update is not in hand and should be obtained). The stock fell about 10% from
the September 10 price after the results and the ACV announcement.

What the notes assume on each term: US insurance cars −2% (Barclays) to +1.3% (Stephens) for fiscal 2027; US revenue per car
+2.0% per quarter (Stephens); seller-fee concession 25–50 basis points visible from the November–January quarter (Barclays);
yards about 60% utilised and land worth about $4 billion against $2.4 billion book (JPMorgan); no broker models the claims
term, the total-loss fraction or ACV.

---

## 7. The short thesis, quantified (preliminary; rebuild against post-results consensus)

| August–October 2026 (reported late November) | our chain | sell-side models |
|---|---|---|
| US insurance cars | −4 to −6% | −1% (Stephens) to −3% (Barclays) |
| US insurance average price | +1.5 to +2.5% | not stated |
| service revenue per car | ~+3% | +2% (Stephens) to ~+5% (JPMorgan) |
| total service revenue | −0.5 to 0% | +2.7% (Stephens) |
| adjusted EBITDA | $450–465M, −6 to −9% y/y | $473–488M |
| adjusted EPS | $0.36–0.37 | $0.39–0.41 |

Fiscal 2027 EPS on this path: about $1.45–1.50 against consensus $1.60–1.68. Price target: 9.5–10× fiscal 2027 EBITDA of
about $1.85 billion plus about $2.6 billion of net cash after the ACV payment, divided by 926 million shares = **$21–23**,
about 20% below $27.59. All figures in this table are ASSUMED compositions of MEASURED and FITTED parts and must be rebuilt
in the workbook with the coefficients flexed to their interval bounds.

Bounded downside, to be stated in the pitch: net cash, no debt, land carried below market value, eight Buy ratings with
targets at $40+, a board member with M&A and activism background added in August 2026. Sizing and the flip conditions matter.

**Flip conditions (publish them):** service revenue per car at or above +4% in the November–January quarter; a buyer-fee
increase announced; IAA's share of listed duopoly inventory failing to rise (`data/csv/duopoly_daily.csv`, `usable = 1`
nights only); the repair-versus-value gap widening above +12 points. Any one of these and the twelve-month long case returns.

---

## 8. Weaknesses in the evidence and the next steps to fill them, in order

1. **Decompose the revenue-per-car intercept.** Weakness: the +4.1 is an average over quarters with fee increases and
   hurricane comparisons; the clean-quarter reads (1.6 and 2.6 points) are single points. How: from the transcripts on the
   owner's machine, rebuild the quarterly US fee-revenue-per-car series fiscal 2022–2026; mark the dated fee increases
   (November 2024 known; earlier ones from 10-K text and exporter blogs, UNVERIFIED until found); add a dummy for
   hurricane-affected comparison quarters; regress the intercept on those. Why: it decides whether the near-term floor is
   +2 or +4, which is the whole pitch. Local; no network.
2. **Refresh the price nowcast.** Weakness: used-car CPI on disk stops mid-2026. How: fetch BLS used-car CPI through August
   (the September print lands October 14, before the finals) and Manheim's mid-month index; run the chain for the
   August–October quarter. Why: this is the dated clock the field lacks. Needs a machine that can reach `download.bls.gov`
   (this session's container could not; status codes in `findings.md` Addendum 23 D).
3. **Rebuild the delta against live consensus.** Weakness: Stephens' numbers are from August 20. How: obtain Stephens'
   post-results note and Visible Alpha quarterly consensus for cars, revenue per car, EBITDA and EPS. Why: the page-one number
   must be against the current consensus.
4. **Run the cars identity quarter by quarter** for August–October and November–January with the four parts and their ranges,
   and compare with consensus cars. Why: to know which way cars can surprise, and to show the account drag arithmetic.
5. **Split yard cost into elective and volume-driven.** How: take the call figures ($17M long-haul, $30M yard-cost rise, half
   elective) and the 10-K segment note when it files; model gross margin at cars −5, 0, +5. Why: the EBITDA path for the two
   quarters is a cost story as much as a revenue story.
6. **Consolidate ACV** from close on its standalone plan with zero synergies and forgone interest at 4%; show fiscal 2027 and
   2028 EPS. Why: the deal closes inside the horizon and the dilution is on the record.
7. **Bound the seller-fee risk.** Weakness: no public series. How: use RB Global's automotive take rate and service revenue
   per car (`data/csv/rba_automotive_series.csv`; RB Global reports early November) as the read-through for what a
   concession looks like after its Progressive expansion; use Barclays' 25–50 basis points and JPMorgan's "toward zero on one
   carrier" as the base and bear cases. Why: it is the bear's main channel and the pitch must size it, not ignore it.
8. **Check positioning.** How: short interest and days to cover; the reaction after September 10. Why: a crowded short into
   the ACV close or a cost-discipline surprise is how the pitch loses.
9. **Tie the base year to the 10-K** when it files (last three years filed September 26–30); check
   `data.sec.gov/submissions/CIK0000900075.json` first each session. Why: the whole revenue chain hangs off fiscal 2026.
10. **Continue the CCC quarterly TLF series** (last public point 2025 Q3): check the Crash Course Q3 2026 page in October.
    Why: the cycle regression's dependent variable.
11. Lower priority: Progressive's fourth-quarter frequency (11 Exhibit-13 fetches); the dollar and export screen (E7) now
    that the international share is known; HLDI claim frequency by age and body (would make the fleet curves measured).

---

## 9. What is measured, fitted and assumed, in one place

- MEASURED: TLF and its relation to the repair-versus-value gap; Progressive claim frequency; the buyer-fee tables; the fleet
  age and body mix and CCC's age buckets; the fiscal 2026 financials (8-K); ACV's plan (14D-9); listed inventory and the
  Copart-versus-IAA split (sitemaps, with the quality gate); the vintage effect on price.
- FITTED: the 0.51 slope and +4.1 intercept; the 0.60 slope and +3.2 intercept; the totaling curves by age and body; the
  survival stretch; the used-value elasticity.
- ASSUMED: the size of the Progressive drag per quarter and the GEICO gain; the claims input; the cost path; the truck-to-car
  value ratio level; the dispersion and depreciation in the body split; the seller-fee concession; the multiple; the
  probability judgement in §1.

---

## 10. File map for this handoff

| file | contents |
|---|---|
| `HANDOFF.md` | the whole project by thread; §5 lists how the model doing this work fails |
| `MODEL_BLUEPRINT.md` | model architecture, tab map, fiscal 2026 base year, build order |
| `findings.md` | every result and retraction in order; Addenda 22–23 are the September experiments |
| `reports/*.md` | one report per experiment; `street_reference_2026-09.md` for the sell-side read |
| `data/csv/*.csv` | every series with a provenance header; index in `data/csv/README.md` |
| `scripts/`, `scripts/experiments/` | every script that produced a number; index in `scripts/README.md` |
| `model/CPRT_Intermediate.xlsx` | every series as a tab plus the fleet calculation, regressions and checks; rebuild with `scripts/build_intermediate_xlsx.py`, verify with `scripts/verify_intermediate_xlsx.py` |
| `raw/` (local only, gitignored) | transcripts, sell-side PDFs and text, HLDI sheets, IHS tables, fetched pages |
| `RESUME_2026-09-26.md` | the short operational resume note |
