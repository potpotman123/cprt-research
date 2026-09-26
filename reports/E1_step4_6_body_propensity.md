# E1 steps 4–6 — body-specific totaling propensity, and what the truck wave does to units and price through 2030

*2026-09-26, third session. Script `scripts/experiments/e1_body_propensity.py`; data `data/csv/age_curves_by_body.csv`,
`data/csv/body_mix_tlf_asp_2015_2030.csv`. No network (every host this session needed is denied by the container's egress
policy — see the blockers in `findings.md` Addendum 23). Inputs are all committed: the fleet roll's sales and survival tables,
the fitted R and P parameters in the `age_curves.csv` header, CCC's measured P by age bucket (Figure 19), the HLDI class
ratios recorded in `reports/E1_step3_hldi_class_losses.md`, the E8 value ratio, and the listed body share from E1 step 1.
Usage: ~60k tokens.*

## 1. The mechanism, stated before the numbers

A claim is declared a total loss when repair cost exceeds a threshold share of the vehicle's value: **P = Pr[C > θ·V]**.
With repair cost and value lognormal within an age, P(a) = Φ((μ_C − ln θ − ln V(a))/σ): a probit in log value, hence a
probit in age when value depreciates geometrically. For two bodies at the same age everything is common except the value
level and the repair-cost level, so the body difference collapses to **one number, a shift Δz in the probit index**:

```
Δz = ( ln(V_LT / V_car) − ln(C_LT / C_car) ) / σ_eff
     V_LT/V_car = 1.50   E8 (KBB ATP × iSeeCars retention; range 1.3–1.7)         ASSUMED level, MEASURED direction
     C_LT/C_car = 1.01   E1 step 3 (HLDI collision claim severity by class, 2022–24 MY)   MEASURED
     σ_eff      = dispersion of ln(C/V) within an age                                    see §2
P_LT(a) = Φ( Φ⁻¹(P_car(a)) − Δz )
```

The two curves are then pinned at every age by the requirement that the claims-weighted mix reproduce the single fitted
P(a), which already reproduces CCC 2024: `s(a)·P_LT(a) + (1−s(a))·P_car(a) = P(a)`, with s(a) the light-truck share of
claims at age a from the fleet roll. One unknown per age, one equation. **Nothing is refitted**; the 2024 aggregate
cross-section is unchanged by construction, so this cannot break any check on `TLF_Roll`.

## 2. σ_eff: CCC's own buckets say the probit form is right, and give the slope

Regressing the probit index of CCC's measured P by bucket (Figure 19) on the claims-weighted mean age of each bucket:

| year | fit | R² | fitted P by bucket vs CCC |
|---|---|---|---|
| 2024 | z = −1.336 + **0.0701**·age | **0.980** | 9.1 / 11.6 / 16.3 / 21.8 / 28.3 / 45.7 vs 9.7 / 10.2 / 15.4 / 22.8 / 31.5 / 43.6 |
| 2025 | z = −1.331 + 0.0724·age | 0.986 | 9.2 / 11.7 / 16.7 / 22.4 / 29.3 / 47.3 vs 9.6 / 10.7 / 15.7 / 23.4 / 32.3 / 45.3 |

A two-parameter probit in age explains 98% of the variance across six buckets in both years (MEASURED). The slope is
γ = δ/σ_eff, so σ_eff = δ/γ with δ the cross-sectional decline of log value per year of age:

| δ (per yr) | basis | σ_eff | Δz (V 1.50) |
|---|---|---|---|
| 0.08 | low | 1.14 | 0.35 |
| **0.11** | **iSeeCars 5-yr retention 58.2% → 0.108, plus ~0.01 for older model years' lower stickers (base, ASSUMED)** | **1.57** | **0.25** |
| 0.14 | high | 2.00 | 0.20 |
| — | claim-size distribution alone (HLDI 2024: median $4.5k, 25% ≥ $9k → σ 1.03; 10% ≥ $18k → σ 1.08) | 1.05 | 0.38 |

The claim-size-only σ omits the dispersion of value within an age, so it is a lower bound on σ_eff and an **upper bound on
Δz**. The HLDI claim-size figures are cited from the step 3 report; the sheets themselves are licence-restricted and not
in this container.

## 3. The body curves (base: Δz 0.25, R_LT = R_car)

| age | P single (fitted, = CCC) | LT share of claims 2024 | **P_car** | **P_LT** | P_LT / P_car |
|---|---|---|---|---|---|
| 0 | 8.2% | 80% | 11.6% | 7.4% | 0.64 |
| 3 | 11.7% | 77% | 15.8% | 10.5% | 0.66 |
| 5 | 15.4% | 71% | 19.8% | 13.6% | 0.68 |
| 8 | 22.9% | 58% | 27.4% | 19.7% | 0.72 |
| 10 | 28.7% | 49% | 32.9% | 24.4% | 0.74 |
| 12 | 34.2% | 45% | 38.3% | 29.1% | 0.76 |
| 16 | 42.0% | 42% | 46.1% | 36.3% | 0.79 |
| 20 | 45.8% | 53% | 51.1% | 41.1% | 0.80 |

At the totaling ages (7–12) a light truck's claim is totaled about **three-quarters as often as a car's** of the same age
(0.61–0.66 under the claim-size-only σ; 0.81–0.84 with a 1.30 value ratio). The single curve sits between the two because
trucks are 45–58% of claims at those ages. Direction MEASURED (HLDI severity, E8 value), magnitude FITTED/ASSUMED (σ_eff, δ).

## 4. The reality check that decides the frequency question — and validates the split

Step 1 found the listed salvage pool *below* the one-body roll's modelled light-truck share of total losses (50.8% vs 57.2%
in 2024; 56.7% vs 60.7% in Sep-2026) and called the 4–6pp gap a consistency check. The two-body roll closes it:

| variant | Δz | LT share of TL 2024 / 2026 / 2030 | gap to listed (2024 / 2026) | body-mix effect on TLF, pp/yr 2024→30 |
|---|---|---|---|---|
| one-body roll (reference) | — | 57.2 / 60.7 / 67.7 | +6.4 / +4.0 | — |
| **base: f = 1.00, V 1.50, σ base** | **0.25** | **50.0 / 53.7 / 61.2** | **−0.8 / −3.0** | **−0.130** |
| f = 1.00, V 1.50, σ claim-size only | 0.38 | 46.4 / 50.1 / 57.8 | −4.4 / −6.6 | −0.195 |
| f = 0.85, V 1.50, σ base | 0.25 | 45.9 / 49.6 / 57.2 | −4.9 / −7.1 | −0.136 |
| f = 0.67 (HLDI adjusted), V 1.50, σ base | 0.25 | 40.0 / 43.6 / 51.2 | −10.8 / −13.1 | −0.138 |
| f = 1.00, V 1.30, σ base | 0.16 | 52.6 / 56.3 / 63.6 | +1.8 / −0.4 | −0.083 |
| f = 1.00, V 1.70, σ base | 0.33 | 47.7 / 51.4 / 59.0 | −3.1 / −5.3 | −0.172 |

Solving for the frequency ratio f = R_LT/R_car that puts the roll's light-truck share of total losses exactly on the listed
share: **f = 1.03 (2024) / 1.13 (2026)** at the base Δz; f = 1.19 / 1.29 at the claim-size-only Δz. Three conclusions:

1. **The propensity split alone explains the gap step 1 found.** With no frequency differential, the two-body roll lands
   within 1pp of Copart's listed truck share in 2024 and 3pp in 2026. The one-body roll was 4–6pp too high because it
   totals trucks like cars. This is an out-of-sample validation of the sign and roughly the size of Δz: the listed share
   was not used to build the curves.
2. **HLDI's adjusted frequency relative (0.67) is not visible in the aggregate.** Applying it would put the truck share of
   total losses 11–13pp below the listing. HLDI adjusts for driver age, gender, density, risk class and deductible; in the
   real fleet those driver characteristics offset the vehicle effect. The unadjusted differential is ≈ 1 (MEASURED against
   the listing, with the caveat that listings include non-insurance consignments). **Use f = 1.0.**
3. The claim-size-only σ (the upper bound on Δz) would need trucks to claim 20–30% *more* often than cars to match the
   listing — the wrong direction against HLDI. So the base σ_eff is preferred over the bound, and the honest range for
   the supply effect is **−0.08 to −0.18pp/yr**, base **−0.13**.

## 5. Step 5 — KPIs by year (base variant)

| year | TLF one-body (roll) | TLF two-body | ΔTLF yoy one-body | ΔTLF yoy two-body | **body-mix supply effect, pp** | LT share of claims | LT share of TL | **ASP body-mix, pp** | Copart units, % | service RPU, % | revenue, % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2022 | 21.85 | 22.13 | +0.24 | +0.11 | −0.13 | 59.5 | 46.9 | +0.56 | −0.58 | +0.29 | −0.29 |
| 2023 | 22.08 | 22.23 | +0.23 | +0.09 | −0.14 | 61.3 | 48.4 | +0.60 | −0.62 | +0.31 | −0.31 |
| 2024 | 22.25 | 22.25 | +0.17 | +0.03 | −0.14 | 63.2 | 50.0 | +0.65 | −0.64 | +0.34 | −0.30 |
| 2025 | 22.29 | 22.14 | +0.03 | −0.11 | −0.15 | 65.3 | 51.8 | +0.73 | −0.66 | +0.37 | −0.29 |
| 2026 | 22.31 | 22.01 | +0.02 | −0.13 | −0.15 | 67.3 | 53.7 | +0.75 | −0.66 | +0.39 | −0.28 |
| 2027 | 22.31 | 21.88 | +0.01 | −0.13 | −0.14 | 69.1 | 55.6 | +0.75 | −0.62 | +0.38 | −0.24 |
| 2028 | 22.30 | 21.75 | −0.01 | −0.14 | −0.13 | 70.7 | 57.5 | +0.74 | −0.58 | +0.38 | −0.20 |
| 2029 | 22.28 | 21.61 | −0.02 | −0.14 | −0.12 | 72.3 | 59.4 | +0.73 | −0.54 | +0.38 | −0.16 |
| 2030 | 22.25 | 21.47 | −0.03 | −0.14 | −0.11 | 73.6 | 61.2 | +0.72 | −0.50 | +0.37 | −0.13 |

Definitions: body-mix supply effect = two-body ΔTLF − one-body ΔTLF (what the single-curve `TLF_Roll` overstates each
year); ASP body-mix = the `ASP_Drivers!H` formula with ratio 1.50 on the two-body share path; Copart units = supply effect ÷
TLF; service RPU = 0.514 × ASP effect; revenue = the sum. Sales after 2025 are held at the 2025 level and mix (83% light
truck) — ASSUMED. The two-body level is higher than the one-body level before 2024 and lower after: only the *drift*
matters, and the level is the spread regression's job.

**What the table says.**
- **Demographics net out to about −0.1pp of TLF a year, not +0.16.** The single-curve roll's demographic drift, which was
  already ≈0 forward (Addendum 19), becomes −0.11 to −0.15pp/yr once trucks total less often: the ageing tailwind and the
  body-mix headwind are the same size and the body one persists to 2030. This is consistent with CCC's own decomposition
  (`reports/CCC_age_buckets_2026.md`): CCC's "within-age propensity" term of +3.8pp for 2022→25 contains about −0.4pp of
  body mix, so the cyclical (spread) part of the 2023–25 surge is slightly *larger* than that report stated.
- **The price half is +0.7pp/yr of ASP**, a little above the workbook's placeholder path (which used the one-body share and
  gave +0.5–0.8), because the two-body truck share of the pool rises from a lower base.
- **Net for Copart the truck wave is unit-negative and roughly revenue-neutral**: −0.6%/yr on US insurance units, +0.4%/yr
  on service RPU (0.514 elasticity), about −0.3%/yr on revenue; with management's total-RPU definition (0.752) the net is
  ≈ −0.1%. The step 3 report's guess that the net was "positive for revenue" was wrong on this arithmetic; retract it.

## 6. Step 6 (the cross-check) was step 1

The listed truck share by month (E1 step 1) is the cross-check the plan called step 6; it is used above as the calibration
target for f and as the validation of Δz. Step 2 (a CCC or Mitchell total-loss-by-body statement) was searched on the CCC
pages and not found (`reports/CCC_age_buckets_2026.md`, "What was not found"); nothing further is available offline.

## 7. Implications for both directions

- **Short:** the popular "ageing fleet + truck wave lifts total losses" narrative is wrong on the totaling side. Fleet
  ageing is over as a driver (CCC buckets, ≈0 since 2023) and the truck wave *lowers* age-specific totaling by ~0.13pp of
  TLF a year with a calendar that runs to 2030 — worth about −0.6% a year of US insurance units. Combined with claims
  frequency no longer falling (E2) but not rising either, the unit base has no demographic support; the FY28 "+5–7% units"
  in the earlier long case needs the spread cycle, not demographics.
- **Long:** the same mechanism is the ASP tailwind (+0.7pp/yr) that, with the fee grid's convexity (E6), feeds the RPU
  intercept; and it is a reason Copart's *units per registered vehicle* can drift down while revenue holds — the pattern
  of the last two years, explained rather than excused. Whether revenue per registered vehicle rises depends on the fee
  elasticity: at 0.514 it does not quite; at 0.752 it is flat.
- **Either way:** the earlier documents' demographic drift row (+0.16pp/yr, or ≈0 forward) should be replaced by −0.1pp/yr
  with the range −0.08 to −0.18, and the two-body share path should feed `ASP_Drivers`.

## 8. Caveats (print them)

- σ_eff and δ are the magnitude; both are assumptions with stated bases, bracketed by the claim-size bound on one side and
  the listing check on the other. A body-specific depreciation rate (pickups hold value better than SUVs; the pool is 80%
  SUV) would tilt Δz within the range shown.
- HLDI's severity relatives are for 2022–24 model years, i.e. ages 0–3, and are paid-claim severities that include
  total-loss payouts. At the totaling ages the repair-cost ratio could differ (aluminium bodies, ADAS sensor counts on
  trucks push it up; larger, simpler panels push it down). A ratio of 1.10 instead of 1.01 would cut Δz by a third.
- The listing is Copart's US listed pool (salvage-title lots), not industry total losses; carrier mix, consignor mix and
  page-sync noise are in it. It is used as a check on the combined effect, not as a fit target for the curves.
- Sales mix after 2025 is held at 83% light truck; a reversal toward cars (affordability) would slow the 2028–30 rows.
- R is still common to both bodies apart from the scalar f; HLDI's claim frequency *by age and body* would make it measured
  (the manual-pull item in `docs/AGE_CURVES.md` §7 stands).

## 9. For the workbook

- `Data_BodyCurves` and `Data_BodyMix` tabs carry the two CSVs (rebuilt this session; `verify_intermediate_xlsx.py` ALL
  CHECKS OK).
- `TLF_Roll`: the demographic drift row is the one-body roll; read the body-mix supply effect from `Data_BodyMix` column
  `body_mix_supply_effect_pp` and subtract it, or cite the two-body TLF directly. A note under the checks block says so.
- `ASP_Drivers`: the body-mix column can take `lt_share_tl_pct` from `Data_BodyMix` in place of the one-body
  `Data_AspVintage!E` path; the difference is ~+0.1pp/yr.
