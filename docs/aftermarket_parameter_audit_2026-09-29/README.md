# Aftermarket parameter provenance and model corrections

29 September 2026. Requested parameter audit ahead of the CCC director interview. Existing model files and evidence were checked first. No source refresh or calibration of the core revenue model; no agents, outreach, paid data or extensive fitting. All original numeric scenarios are preserved.

## What the original numbers actually were

The original adapter explicitly labels every new numeric bridge input assumed in `model/aftermarket_bridge_2026-09-29/inputs.json`. They were illustrative scenario choices, not extracted estimates. The precision of the resulting revenue calculation does not confer precision on these inputs. The CCC workbook supplied today measures age/body total-loss frequencies and composition, not these aftermarket parameters.

| Input | Current setting | Provenance / meaning | Better measurement |
|---|---:|---|---|
| Source quantities: OEM / aftermarket / recycled | 65% / 25% / 10% | Assumed physical mix in a hypothetical eligible basket; no dataset establishes it | Unrounded replacement quantities within the same component/vehicle population; retain optional-OEM and reconditioned categories |
| Eligible basket / complete repair bill | 40% | Assumed eligible-parts spending, not measured all-parts spending | All-parts/bill share multiplied by eligible spending/all-parts spending, or direct eligible line dollars / bill |
| AM / OEM equivalent price | 0.50 | Assumed; existing historical Mitchell evidence challenges its universality | Matched delivered/allowed prices for the same component/interchange, date, condition and quality |
| Recycled / OEM equivalent price | 0.60 | Assumed; not derived from national dollar and count shares | Same matched comparison including freight, grading, returns and assemblies |
| Exposed donor contribution / total contribution | 25% | Assumed collision-parts share of expected net contribution, not part count or gross sales | Recycler donor-linked contribution by component and sell-through horizon |
| Total donor contribution / hammer bid | 1.5× | Assumed financial amplification; not measured profit margin | Expected lifetime contribution after variable fulfillment costs divided by hammer price; separately account for buyer fees/tow and required profit |
| Recycler transmission weight | 50% | Assumed influence on the auction-clearing price; not recycler buyer share | Auction bid/valuation evidence and competition from rebuilders/exporters |
| Rebuilder repair bill / hammer bid | 1.0× | Assumed dollar sensitivity, applied with full saving transmission | Rebuilder repair budgets, resale values, margins and bid ceilings |
| Additional repair-job recapture | 100% | Assumes all modeled avoided totals become repair demand | Completed repairs versus cash settlement, abandonment and noncompletion, with timing |
| Scarcity coefficient | 0.25 | Assumed price support per log supply contraction; a different parameter from 25% donor exposure | Joint supply/demand estimates or retain scenario range |
| Expected salvage pass-through | 100% | Assumes insurers incorporate auction shock without lag | Expected net salvage records/revision timing |
| Threshold-responsive fraction | 100% (50%, 0% diagnostics exist) | Assumed fraction following inherited economic switching rule | All-disposition threshold-gap distribution and overrides |
| OEM/recycled transfers | Small 2/0.5 pp; larger 4/1.5 pp; stress 6/2.5 pp | Hypothetical additional future transfers, not historical measured substitution | Same-component source transitions and rollout/adoption timing |

## What “basket” means

A basket is a fixed list of repair components with weights: for example, specified bumper covers, hoods and lamps for specified vehicles. Hold that list constant and compare the cost when some replacements come from another source. This isolates sourcing from changes in the kind of damage or vehicle repaired.

The existing adapter does not contain a measured list. It represents a hypothetical 100 component-equivalents, all with normalized OEM price $100: 65 OEM, 25 aftermarket at $50, 10 recycled at $60. Cost is $8,350. The larger scenario moves four OEM and 1.5 recycled equivalents to aftermarket: $8,135, a 2.57485% basket saving. Multiplying by the assumed 40% share of the complete bill gives 1.02994% whole-bill savings. Fractional components are an average across claims, not a single vehicle repair.

This abstraction cannot be populated with aggregate all-parts counts and retain its same-component interpretation. A clip, hood and engine are not interchangeable units. In particular, a recycled assembly can represent several components. Unmatched average source prices mostly reflect what each source supplies.

## New constraints from primary evidence

**CCC Crash Course 2026, Figure 35:** visually checked 2025 rounded all-parts / total repair cost shares: current/newer 44%, age 1–3 43%, age 4–6 41%, age 7+ 36%. This supports the scale of TOTAL parts spending, not a 40% substitutable basket. At a 40% all-parts share, a 40% eligible share assumes every parts dollar is eligible. For older vehicles it even exceeds the rounded average all-parts share. Cohort-specific exposure is preferable; these repaired-sample averages are not bounds on individual near-total-loss claims. [Source](https://www.cccis.com/reports/crash-course-2026).

**Existing CCC Figure 39 counts:** 2025 OEM 8.8, AM 3.3, recycled 0.5, reconditioned 0.1, optional OEM 0.3, total 13.0. Their approximate quantity shares are 67.7%, 25.4%, 3.8%, 0.8%, 2.3%. The model's 10% recycled quantity share is not supported as an all-parts share. It could differ within a selected basket, but no measured selected basket exists. Rounding and part-versus-assembly definitions remain material. Do not use 10.5% recycled spending share as a physical share. [Source](https://www.cccis.com/reports/crash-course-2026).

**LKQ 2024 sustainability report, page 16:** illustrative March 2025 OEM/salvage prices for a 2021 Equinox hood are $1,117/$625 (salvage/OEM 55.95%). Transmission, steering and infotainment examples have much lower ratios. None supplies a matched aftermarket quote. The hood supports the possibility of a ratio near 0.60 for one part, not the average or the premise that aftermarket undercuts recycled. It is a seller-selected example, not a transaction sample. The report's aggregate parts and vehicle counts cannot identify component contribution or same-donor lifetime yield. [Source](https://www.lkqcorp.com/wp-content/uploads/2025/05/LKQ_2024_Sustainability-Report_Final.pdf).

**LKQ 2025 10-K, printed pages 38 and 56:** North America gross margin is 42.8%; segment products and expenses span multiple businesses, and customer delivery costs are in SG&A. This does not measure the adapter's net contribution/hammer-price ratio. Deriving 1.5× from a corporate gross margin would mix denominators and costs. [Source](https://s205.q4cdn.com/926050515/files/doc_financials/2025/ar/LKQ-Corporations-Full-Year-Form-10K.pdf).

Existing [Mitchell historical component prices](../aftermarket_transition_evidence_2026-09-29/README.md) remain more defensible than treating 50% as universal: 2016 six-component AM/OEM ratios were approximately 0.70–0.77 across origin groups. These are dated diagnostics, not new current inputs. No direct public measurement of the 25% or 1.5× parameters was established in this bounded pass.

## How extra repairs are included

The adapter holds claim count N fixed, recalculates total losses T, and sets repair jobs R=N−T. Recycled demand changes as:

`demand_ratio = recycled_source_retention × [1 + recapture × (new_repair_jobs / old_repair_jobs − 1)]`.

In the original larger-shift family, recycled retention is 0.85 and repair jobs rise about 0.608%. Recycled demand therefore becomes about 0.8552 of reference, a 14.48% decline instead of 15%. This is a modeled offset, not measured demand. The two percentage denominators differ: a 2% decline in totals does not mean 2% more repairs.

The model also adds positive scarcity support `−0.25 × log(new_totals / old_totals)` and higher rebuilder bids from cheaper repairs. It solves for an auction-price shock consistent with those responses and the insurer's resulting expected salvage and total-loss decisions. The original larger scenario's approximate fixed-selection price contributions are −2.72 pp recycler pressure, +0.515 pp rebuilder support and +0.520 pp scarcity support, net −1.68%. Selected-auction prices and fee changes also reflect changed vehicle composition.

Weaknesses: avoided totals are assumed to require the average repair basket, although marginal repairs may require more parts; all non-totaled claims are treated as repairs; there are no completion/inventory lags. The linear donor calculation assumes recycled demand changes pass proportionately into exposed contribution. Reduced donor supply can have component-specific yield effects. Separate scarcity and demand coefficients should not both absorb the same observed equilibrium price response.

## Better parameterization

1. Use actual component lines: `repair saving = sum(switched quantities × [old delivered price − new delivered price]) − added labor/returns/fitment costs`. Divide by the compatible whole-bill denominator. This eliminates the fictitious 65/25/10 basket and arbitrary 40% if the needed lines are available. A spending-weight version also works: original-bill share of each source/component × fraction switched × matched discount.
2. For observed repaired claims, use measured part quantities. For newly repaired former totals, add their own expected component demand and completion rate: `new recycled demand = demand from continuing repairs + demand from switched claims`. Do not assign the average repair basket to marginal claims without a sensitivity.
3. Derive donor value from component sell-through probability × net proceeds, plus unaffected recoveries, less acquisition/holding requirements. The present 25% × 1.5 × 50% is just one composite assumed exposure (0.1875) in the direct price equation. Aggregate auction outcomes will not identify the three factors separately. Until recycler evidence exists, show a single composite sensitivity rather than three apparently measured estimates.
4. Keep cheaper-repair, recycler impairment, rebuilder competition and supply responses separate in reporting. An OEM-only transition can lower units and raise RPU. The sign of both outputs is not guaranteed.
5. The new CCC levels anchor the starting population; they do not identify the density of claims close to a switching threshold. Obtain that distribution before assigning forecast confidence to the unit derivative.

`diagnostic_sensitivities.csv` holds three bounded CCC-family diagnostics: halve eligible bill exposure to 20%, remove exposed donor contribution, and allow only OEM displacement. These are tests of dependence, not estimated replacements. Original defaults are unchanged. Reproduction script and source hashes are preserved alongside this note.

| CCC-family test | FY27 service delta vs own reference | Insurance RPU delta |
|---|---:|---:|
| Existing larger sourcing scenario | −$90.66m | −0.914% |
| Eligible bill exposure 20%, other inputs unchanged | −$79.51m | −1.045% |
| Zero exposed donor contribution, other inputs unchanged | −$23.52m | +0.252% |
| OEM displacement only, 4 pp | −$20.58m | +0.256% |

Halving repair-bill exposure does not halve the revenue loss because the assumed donor-demand shock remains and the positive rebuilder offset shrinks. This is why apparent downside robustness cannot validate the mechanism. Removing donor impairment does not establish zero exposure empirically; it demonstrates that simultaneous falling units and RPU depend on that assumption.

See [CCC_INTERVIEW.md](CCC_INTERVIEW.md) for prioritized questions and exact requested tables. No new public evidence justifies promoting the approximately $91m scenario loss to a central forecast.

Follow-up: [evidence admission and future projections](FORWARD_ASSUMPTIONS.md) adds practitioner cost guidance and explains why the original adoption shock is not an extrapolated forecast.

Latest follow-up: [Bidmate documentation and the 5.5-point evidence test](../bidmate_adoption_2026-09-29/README.md).
