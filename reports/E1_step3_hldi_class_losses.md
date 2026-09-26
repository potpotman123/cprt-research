# E1 step 3 — HLDI collision losses by vehicle class: the body-level inputs exist, and they point the supply half of E1 down

*2026-09-26. Source: HLDI "Loss facts — Collision coverage: Comparison of losses by vehicle class and size, 2022–24 model years"
(December 2025) and "Distribution of collision claims by claim size, 2024 calendar year", plus the comprehensive-coverage
sheet, from `iihs.org/research-areas/auto-insurance/auto-insurance-fact-sheets` (robots: only `/logos/` and
`/ratings-wall-display/` disallowed). 3 PDF requests. **Licence:** the sheets are marked "COPYRIGHTED DOCUMENT, DISTRIBUTION
RESTRICTED … no part may be reproduced." Following the repository's rule for the IHS tables, the PDFs and any extract stay
local-only (`raw/hldi/`, gitignored) and this note cites class-level summary ratios only. Usage: ~15k tokens.*

## What the sheets contain

Relative collision claim frequency, claim severity and overall losses (100 = all passenger vehicles; 2022–24 MY averages
5.9 claims per 100 insured vehicle years and $10,267 per claim), by class (two-door cars, four-door cars, station wagons,
minivans, sports cars, luxury cars, pickups, SUVs, luxury SUVs, vans) and size within class. Results are adjusted for driver
age, calendar year, density, gender, marital status, model year, risk class, state and deductible. The claim-size sheet gives
the 2024 distribution of collision claim amounts in $1,000 bands (median claim ≈ $4,500; 25% of claims ≥ $9,000; 10% ≥ $18,000).

## Class means (unweighted over size rows; relative to 100)

| class | collision claim frequency | claim severity | overall losses |
|---|---|---|---|
| four-door cars (mini to large) | 138 | 96 | 129 |
| pickups | 87 | 101 | 87 |
| SUVs (non-luxury) | 94 | 95 | 89 |
| minivans | 100 | 91 | 91 |
| **light trucks (pickups + SUVs + minivans)** | **92** | **97** | 89 |

**LT ÷ car: claim frequency 0.67, claim severity 1.01.**

## What it means for E1

The totaling decision compares repair cost with vehicle value. For a light truck and a car of the same age and model year:
severity is the same (ratio 1.01) while value is ~1.5× (E8). So the repair-cost-to-value ratio of a truck claim is roughly
**two-thirds** of a car claim's, and a smaller share of truck claims should cross the totaling threshold. On top of that,
light trucks file **one-third fewer** collision claims per insured vehicle year. Both effects run the *same* way:

- **Supply half of E1: negative, not positive.** As the truck-heavy 2014–2020 model years enter the totaling ages, the
  claims-weighted propensity at a given age should fall, not rise. The fleet roll's single R(age) and P(age) therefore
  *overstate* the demographic contribution of the truck wave. Direction MEASURED (HLDI + E8), magnitude not yet computed.
- **Price half of E1: positive.** Fewer, higher-value total losses per vehicle. This is the ASP body-mix effect already
  wired to `ASP_Drivers!B4` (E8).
- **Net for Copart:** units per registered vehicle drift down with the truck share; revenue per unit drifts up. Whether
  revenue per registered vehicle rises depends on the elasticity of fees to value (0.514 on service RPU), so the net is
  positive for revenue and mildly negative for units. This is a driver-based reason to expect exactly the pattern of the last
  two years — flat-to-down units, rising RPU — and it has a calendar.

**Caveats.** HLDI's relatives are for 2022–24 model years (age 0–3), where totaling is rare; the frequency gap partly reflects
who buys trucks (adjusted for driver age but not fully for use). Severity by class at age 7–12 is not published. The
claim-size distribution is all-vehicle. A quantified P_body(age) needs the claim-size distribution scaled by class severity
against an age-specific value, which is E1 step 4 — now feasible with what is on disk, and its sign is known in advance.

## Kill rule, revisited

The scoping doc's rule was "if P_truck ≈ P_car within tolerance, body mix is a price story only." The data say P_truck < P_car,
so E1 is a price story *plus* a small negative supply story. Step 4 should be run to size the negative, because the popular
"truck wave lifts total losses" narrative (CCC's own framing) appears to be wrong on the totaling side and right only on thefts
and value.
