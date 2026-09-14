# Age curves for mechanism A — how S(age), R(age) and P(age) are calculated, and the evidence behind each

*Built 2026-09-14. Reproduce every number with `./.venv/bin/python scripts/age_curves.py`. Per-age values in
`data/csv/age_curves.csv`; every target and out-of-sample check in `data/csv/age_curves_validation.csv`.*

The cohort roll (`MODEL_BLUEPRINT.md` §3A) needs three curves over vehicle age `a = calendar year − model year`:

| Curve | Meaning | Where it comes from | Status |
|---|---|---|---|
| `S(a)` | share of a model-year cohort still on the road at age a | EPA survival schedule (ORNL TEDB Ed.40 Table 3.15), stretched by one parameter fitted to the IHS/Polk census and to S&P counts | measured shape, calibrated scale |
| `R(a)` | insured physical-damage claims per vehicle on the road, relative to a new vehicle | fitted jointly with P to eight CCC claim-mix statistics; decomposed against EPA miles-by-age | fitted, decomposed |
| `P(a)` | probability a claim on an age-a vehicle is declared a total loss | fitted jointly with R to CCC; reproduces CCC's "1 in 10 for ≤3 years" and "72% of total losses are 7+" | fitted |

**One structural point first.** The tab's output is `TLF_t = Σ_a fleet(a,t)·R(a)·P(a) / Σ_a fleet(a,t)·R(a)`. Only the
*claims-weighted* age mix matters, and `fleet(a)·R(a)` enters as a product. So S and R are not separately identified
by claims data: a longer-lived fleet with a steeper R and a shorter-lived fleet with a flatter R give the same
claims-by-age. That is why (i) S is calibrated to *vehicle counts*, not to claims, (ii) R and P are fitted to *claims
statistics* only, and (iii) §6 shows the model's outputs are robust to the S assumption even though R's slope is not.

---

## 0. What to type into the model

```
S_cars(a, t) = S_EPA,cars( a / k_cars(t) )        S_LT(a, t) = S_EPA,LT( a / k_LT(t) )
    k_cars(2013) = 1.064   k_LT(2013) = 0.921      (fitted to the IHS 2013 census by age)
    k(2024)      = 1.194 × k(2013)                 (fitted to S&P: VIO ≈ 289M light vehicles, 66% aged 7+)
    linear between 2013 and 2024; hold flat after 2024 in the base case (k>1 = vehicles last longer than the EPA schedule)

R(a) = e(a) · exp( −0.0903 · max(a−6, 0) )        e(0) = 0.5, e(a≥1) = 1
       (flat through age 6, then −8.6%/yr; the 0.5 is half-year exposure for the current model year. A free 0–6 slope
        is not identified by the data — fitting one returns +1.6%/yr with no better fit — so it is fixed at zero)

P(a) = 0.048 + (0.480 − 0.048) / ( 1 + exp( −(a − 9.22) / 3.73 ) )
       (8% at age 0, 10% for ≤3 yrs, 20% at 7, 34% at 12, 43% at 17, 48% asymptote)
```

**Resolution.** The roll runs at single years of age, 0 to 31, for every model year 1970–2025; S, miles, R and P are
all single-year curves and the CSV carries all 32 ages. Buckets appear in this document only where the *evidence* is
bucket-level: CCC publishes its claim mix as current-year / 1–3 / 4–6 / 7+ (and 7–12 / 13+ since 2026), and the IHS
census lumps 15+. So the single-year shape of S is measured (EPA schedule, checked against the census age by age),
while the single-year shapes of R and P *between* the bucket anchors come from the parametric forms — the
buckets are where they are pinned, the interior is interpolation. Build the tab at single-year resolution.

Per-age values (cars' EPA survival shown; light trucks in the CSV). Fleet, claims and total-loss shares are the
model's 2024 cross-section:

| age | S_EPA cars | S_2024 cars | S_2024 LT | miles/yr cars | R(a) | P(a) | fleet 2024 (M) | claims % | TL % |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.000 | 1.000 | 1.000 | 13,843 | 0.500 | 0.082 | 15.5 | 4.0 | 1.5 |
| 1 | 0.997 | 0.998 | 0.992 | 13,580 | 1.000 | 0.091 | 15.1 | 7.8 | 3.2 |
| 2 | 0.994 | 0.995 | 0.984 | 13,296 | 1.000 | 0.103 | 13.3 | 6.9 | 3.2 |
| 3 | 0.991 | 0.993 | 0.975 | 12,992 | 1.000 | 0.117 | 14.3 | 7.4 | 3.9 |
| 4 | 0.984 | 0.990 | 0.965 | 12,672 | 1.000 | 0.134 | 13.7 | 7.1 | 4.3 |
| 5 | 0.974 | 0.984 | 0.950 | 12,337 | 1.000 | 0.154 | 16.0 | 8.2 | 5.7 |
| 6 | 0.961 | 0.977 | 0.931 | 11,989 | 1.000 | 0.176 | 16.0 | 8.3 | 6.6 |
| 7 | 0.942 | 0.967 | 0.909 | 11,630 | 0.914 | 0.202 | 15.6 | 7.4 | 6.7 |
| 8 | 0.920 | 0.955 | 0.882 | 11,262 | 0.835 | 0.229 | 15.7 | 6.8 | 7.0 |
| 9 | 0.893 | 0.940 | 0.852 | 10,887 | 0.763 | 0.258 | 15.2 | 6.0 | 7.0 |
| 10 | 0.862 | 0.923 | 0.819 | 10,509 | 0.697 | 0.287 | 14.1 | 5.1 | 6.5 |
| 11 | 0.826 | 0.902 | 0.784 | 10,129 | 0.637 | 0.315 | 12.9 | 4.2 | 6.0 |
| 12 | 0.788 | 0.879 | 0.745 | 9,748 | 0.582 | 0.342 | 11.6 | 3.5 | 5.3 |
| 13 | 0.718 | 0.854 | 0.705 | 9,370 | 0.532 | 0.365 | 9.7 | 2.7 | 4.4 |
| 14 | 0.613 | 0.825 | 0.663 | 8,997 | 0.486 | 0.387 | 8.5 | 2.1 | 3.7 |
| 15 | 0.510 | 0.795 | 0.621 | 8,629 | 0.444 | 0.405 | 7.3 | 1.7 | 3.0 |
| 16 | 0.415 | 0.746 | 0.576 | 8,270 | 0.406 | 0.420 | 8.7 | 1.8 | 3.4 |
| 17 | 0.332 | 0.678 | 0.529 | 7,922 | 0.370 | 0.433 | 9.5 | 1.8 | 3.5 |
| 18 | 0.261 | 0.595 | 0.484 | 7,586 | 0.339 | 0.443 | 8.8 | 1.5 | 3.0 |
| 19 | 0.203 | 0.514 | 0.440 | 7,265 | 0.309 | 0.451 | 7.9 | 1.3 | 2.6 |
| 20 | 0.157 | 0.439 | 0.399 | 6,962 | 0.283 | 0.458 | 7.0 | 1.0 | 2.1 |
| 25 | 0.040 | 0.172 | 0.233 | 5,778 | 0.180 | 0.474 | 3.4 | 0.3 | 0.7 |
| 30 | 0.007 | 0.059 | 0.128 | 5,358 | 0.115 | 0.479 | 1.3 | 0.1 | 0.2 |
| 35 | 0.000 | 0.017 | 0.000 | 5,358 | 0.073 | 0.480 | 0.2 | 0.0 | 0.0 |

By bucket (2024 model): 

| bucket | fleet % | claims % | TL % | R(a) | P(a) | miles/yr |
|---|---|---|---|---|---|---|
| 0 (current MY) | 5.3 | 4.0 | 1.5 | 0.500 | 0.082 | 15,546 |
| 1-3 | 14.6 | 22.0 | 10.2 | 1.000 | 0.103 | 14,911 |
| 4-6 | 15.6 | 23.6 | 16.5 | 1.000 | 0.156 | 13,537 |
| 7-12 | 29.1 | 32.9 | 38.5 | 0.749 | 0.260 | 11,396 |
| 13+ | 35.4 | 17.5 | 33.3 | 0.327 | 0.424 | 7,701 |

### Where each column comes from

| Column | Data or derived? | Exact source |
|---|---|---|
| `age` | convention | `a = calendar year − model year`; a model-year-2024 vehicle is age 0 in 2024. CCC's "current year or newer" ≈ age 0; the IHS census is a mid-year snapshot, so its "under 1" straddles ages 0–1 (compared as a combined bucket). |
| `S_EPA cars` | **data, verbatim** | U.S. EPA, *Draft Technical Assessment Report: Midterm Evaluation of Light-Duty Vehicle GHG Emission Standards and CAFE Standards for MY 2022–2025*, EPA-420-D-16-900, July 2016 — survival-rate schedule for cars, as republished in ORNL *Transportation Energy Data Book* Ed.40 **Table 3.15** (`raw/ornl/tedb40/Table3_15_01312022.xlsx`; extract `data/csv/ornl_tedb40_survival_by_age.csv`). The light-truck column of the same table is in the CSV. |
| `S_2024 cars` | **derived** | `S_EPA,cars(a / 1.270)`, linearly interpolated between the table's integer ages. 1.270 = 1.064 × 1.194: **1.064** is the stretch that best reproduces the IHS 2013 census of cars by single year of age (ORNL **Table 3.11**, source line "IHS Automotive, Detroit, MI"); **1.194** is the further drift that makes the 2024 roll hit S&P's light-vehicle count and 66% aged 7+ (§2.4). Example: age 15 → 15/1.270 = 11.81 → between 0.826 (age 11) and 0.788 (age 12) → 0.795. |
| `S_2024 LT` | **derived** | same construction for light trucks: `S_EPA,LT(a / 1.099)`, 1.099 = 0.921 × 1.194; 0.921 fitted to the IHS 2013 census of trucks (ORNL **Table 3.12**, which includes heavy trucks — heavy sales are rolled separately with Table 3.16 for that comparison). Example: age 15 → 13.65 → between 0.651 and 0.605 → 0.621. |
| `miles/yr cars` | **data, verbatim** | EPA annual vehicle-miles-of-travel schedule by age for cars, same EPA report (EPA-420-D-16-900), republished as ORNL **Table 3.14** (`raw/ornl/tedb40/Table3_14_01312022.xlsx`; extract `data/csv/ornl_tedb40_miles_by_age.csv`). Table 3.14 also cites NHTSA, *Vehicle Survivability and Travel Mileage Schedules*, January 2006, as the earlier schedule. Used only for the R decomposition (§3.4), not in any fit. |
| `R(a)` | **fitted** | `e(a)·exp(−0.0903·max(a−6,0))`, `e(0)=0.5`: flat through age 6, then one fitted slope. That slope is fitted jointly with P's four parameters to the eight CCC 2024 statistics in §5 (Nelder–Mead, 40 restarts, `scripts/age_curves.py`). The 0.5 half-year exposure at age 0 is an assumption with a stated reason (§3.2). Example: ages 1–6 → 1.000; age 7 → exp(−0.0903) = 0.914; age 12 → exp(−0.542) = 0.582. |
| `P(a)` | **fitted** | `0.048 + 0.432 / (1 + exp(−(a − 9.22)/3.73))`, four parameters fitted jointly with R to the same eight statistics. Example: age 0 → 0.048 + 0.432/(1 + e^2.473) = 0.082. |
| `fleet 2024 (M)` | **derived** | `sales(2024 − a) × S_2024` summed over cars and light trucks. Sales: Ward's Communications new retail vehicle sales 1970–2021 via ORNL **Table 3.6** (`data/csv/ornl_tedb40_new_sales.csv`); 2022–2025 FRED `TOTALNSA` and `LTRUCKNSA` (BEA light-vehicle sales, NSA, monthly summed by calendar year, `data/csv/fred_TOTALNSA.csv`, `fred_LTRUCKNSA.csv`), rescaled to Ward's basis (§1). Example: age 3 = MY2021 = Ward's 14.57M × S(3) ≈ 14.3M. |
| `claims %` | **derived** | `fleet(a)·R(a) / Σ_a fleet(a)·R(a)` — the model's 2024 distribution of insured physical-damage claims by age. |
| `TL %` | **derived** | `fleet(a)·R(a)·P(a) / Σ_a fleet(a)·R(a)·P(a)` — the model's 2024 distribution of total losses by age. |

The eight CCC statistics that R and P are fitted to, with the page each comes from (all fetched as ungated HTML,
`PROVENANCE.md` §5; quotes verbatim):

| statistic | value | quote | page |
|---|---|---|---|
| TLF 2024, all loss categories | 22.3% | printed data label, chart "Total Loss Frequency Remains High as Vehicle Values Trend Up" | https://www.cccis.com/reports/crash-course-2026 → `data/csv/ccc_tlf_annual.csv` |
| total losses from 7+ | 72% | "almost 72% of valuations across all loss categories are for vehicles 7 years or older" | https://www.cccis.com/reports/crash-course-2024/q4 |
| repairables from 7+ | 45% | "vehicles seven years or older now make up nearly 45% of all repairable claims, up from 35% in 2019" | https://www.cccis.com/reports/crash-course-2024/q4 |
| repairables ≤3 yrs | ~30% | "Only 26.3% of repairable ICE vehicles are three years or newer"; EVs 79.4% and hybrids 60.3% ≤3 yrs → all-fuel ≈30% | https://www.cccis.com/reports/crash-course-2024/q4 |
| avg age, claim vehicles | 7.6 | "For claims, the average age of vehicles has increased to 7.6 years – up from 6.9 years in 2020" | https://www.cccis.com/reports/crash-course-2025/q1 |
| avg age, repairables / total losses | 6.8 / 10.6 | "The average age of repairable vehicles was 6.8 years in 2024 (up from 6.1 years old in 2020) and 10.6 years for total loss vehicles (up from 10.0 years old in 2020)" | https://www.cccis.com/reports/crash-course-2025/q1 |
| P(≤3 yrs) | 10% | "For claims that are three years old or newer, 1 in 10 are flagged as a total loss by the insurer" | https://www.cccis.com/reports/crash-course-2026 |

Out-of-sample quotes (2025 pages): "Through Q1, 74% of valuations are on vehicles 7 years or older" (…/crash-course-2025/q2);
"AAVV is biased due to the large share of vehicles 7 years or older (73%)" (…/q3); "over 72% of total loss valuations are
on vehicles 7 years or older" and "almost 46% of repairable vehicles are 7 years or older" (…/q4).

**Licence note.** ORNL republishes Tables 3.11, 3.12 and 3.13 from IHS Automotive with the line "FURTHER REPRODUCTION
PROHIBITED". Those three extracts are therefore kept local-only (`raw/ornl/tedb40/extracts/`, gitignored) and cited by
table number; the EPA and Ward's tables carry no such line and are committed. Reproducing the figures in a pitch is
citation of a public DOE publication, not redistribution of the dataset.

Bucket-level: **P(7+) = 31.7%, P(0–6) = 12.7%; R(7+)/R(0–6) = 0.57.** (The closed-form derivation from CCC's
bucket shares alone — 0.455 of repairables and 0.72 of total losses from 7+, 66% of the fleet 7+, TLF 23.1% — gives
32.2% / 13.4% and 0.55; the two routes agree.)

---

## 1. Cohort sizes — `sales(MY)`

`data/csv/light_vehicle_sales_by_year.csv`. Ward's new retail sales 1970–2021, cars and light trucks separately
(ORNL TEDB Ed.40 Table 3.6). 2022–2025 from FRED `TOTALNSA` (light vehicles) and `LTRUCKNSA` (light trucks), monthly
NSA summed by calendar year, **rescaled to Ward's basis on the 2021 overlap** (cars ×0.879, light trucks ×0.968; FRED's BEA-sourced series
runs 5.8% above Ward's retail in total because it counts fleet deliveries, and the gap is concentrated in cars. Without
the rescale the young cohorts are inflated relative to the old ones and every young-vehicle share is wrong by ~1pp). Heavy trucks (Table 3.6) are carried only
for the 2013 truck-census check.

---

## 2. S(age) — survival

### 2.1 The source shape

EPA's survival schedule by age for cars and light trucks (ORNL TEDB Ed.40 **Table 3.15**, from the 2016 mid-term
evaluation of the light-duty GHG standards). Cars: 0.961 at 6, 0.862 at 10, 0.510 at 15, 0.157 at 20; light trucks
decline earlier but have a longer tail (0.553 at 15, 0.324 at 20). Median lifetime on the raw schedule: cars 15.1
years, light trucks 16.0. The same book also carries NHTSA's 2006 schedule (referenced in Table 3.14) and, for heavy
trucks, the Schmoyer/ORNL Greenspan–Cohen schedules (Table 3.16). Shape is taken from the EPA table; nothing is assumed.

### 2.2 Tested against a census: the schedule is right in shape, wrong in scale, and the scale drifts

ORNL Tables **3.11 / 3.12** are IHS Automotive (Polk) registration counts by single year of age for 1970, 2000 and
2013 — an actual census of the fleet. Rolling Ward's sales through the EPA schedule and comparing:

| year, body | raw EPA total vs census | raw EPA share 15+ vs census | stretch k fitted | fitted total | fitted bucket MAE |
|---|---|---|---|---|---|
| 2000 cars | 143.4M vs 127.7M (+12%) | 15.9% vs 15.0% | 0.922 | 131.6M (+3%) | 0.47pp |
| 2000 trucks | 96.2M vs 85.6M (+12%) | 15.3% vs 17.3% | 0.879 | 90.0M (+5%) | 0.82pp |
| 2013 cars | 118.0M vs 130.1M (−9%) | 16.9% vs 18.8% | **1.064** | 126.4M (−3%) | 0.40pp |
| 2013 trucks | 134.0M vs 124.5M (+8%) | 21.8% vs 20.8% | **0.921** | 126.4M (+2%) | 0.44pp |

(*trucks* in the census include heavy trucks, so heavy sales are rolled with Table 3.16 for that comparison.) The
single-year bucket shares match to ~0.4pp on average with one stretch parameter `S_k(a) = S_EPA(a/k)`; the fitted k
rises from ~0.9 in 2000 to ~1.0 in 2013 — vehicles were already outliving the schedule by 2013 and the trend is up.
2013 single-year comparison for cars (share of fleet, %):

```
age :   0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15+
IHS :  7.1  5.9  4.6  4.7  4.2  5.6  6.1  5.9  6.0  5.3  5.6  5.5  5.1  5.3  4.2  18.8
k   :  6.0  5.7  4.8  4.4  4.2  5.2  5.8  5.8  5.6  5.4  5.3  5.4  5.4  5.4  4.8  20.8
```

### 2.3 Why S&P's *average age* must NOT be the calibration target

The blueprint tab calibrated its survival curve to S&P's 12.7 years and produced a curve on which 90% of 17-year-olds
survive. That was not a bug in the tab; it is what the target forces. The IHS 2013 census — the same Polk registration
data S&P uses — implies an average age of **9.6** for cars if the "15 and older" bucket averages 19 years, **10.4** at
23, **11.1** at 27. S&P published **11.4** for 2013 cars. Reproducing S&P needs a 15+ tail averaging ~27–28 years:
registered vehicles that are barely driven and almost never claimed. Stretching the whole schedule until the average
hits 12.8 inflates that tail and blows the total to 341M vehicles (S&P: ~289M). **Calibrate S to counts.** Report the
model's own average age (11.1 in 2024 on the `t−MY+0.5` convention) alongside S&P's 12.8 with this note.

### 2.4 Drift after 2013: one multiplier fitted to S&P's counts

One multiplier on both k's, linear from 1.000 (2013) to **1.194 (2024)**, fitted to two count anchors: 66% aged 7+
(S&P Global Mobility, quoted in Crash Course 2024/Q4: "66% of vehicles in operation are seven years or older") and light
VIO ≈ 289M. ⚠ **The 289M is S&P's 2025 average-age release recalled from memory — it is not on disk.** The on-disk
alternative is Experian's 292.1M light-duty VIO at Q3-2024 (Crash Course 2025/Q1), which the fitted roll lands on
anyway (292M), so the anchor choice barely moves k: refitting with 292.1M as the target gives k ×1.204 instead of
×1.194, moves the R and P parameters in the third decimal, and leaves the bucket values (P(7+) 31.7% / P(0–6) 12.7%)
and the drift (+0.16pp/yr) unchanged. Confirm from the S&P release (§7 item 3). Result and checks:

| check | model | anchor | fitted? |
|---|---|---|---|
| light VIO end-2024 | 292M | ~289M (S&P) | yes |
| share aged 7+ | 64.5% | 66% (S&P via CCC 2024/Q4) | yes |
| VIO growth 2020→2025 | +5.4% | +5.1% (Experian, 2020→Q3-2025, CCC 2026) | **no** |
| avg age cars / LT 2024 | 12.9 / 9.9 | 14.5 / 11.9 (S&P) | no — convention, §2.3 |
| ≤6-yr count 2020→2025 | −9.6M | "over 12 million less" (Experian via CCC 2026) | no — **not reproducible**: sales alone give −9.7M with *zero* scrappage, so Experian's figure is definitional (model-year buckets / database coverage); recorded, not fitted |
| implied median lifetime 2024 | cars 19.2 yrs, LT 17.6 | (raw EPA 15.1 / 16.0; 2013 fit 16.1 / 14.8) | — |

The independent VIO-growth check landing on +5.4% vs +5.1% is the strongest evidence the drift is right: sales 2020–25
were ~2M/yr *below* 2015–19, so the fleet can only have grown 5% if scrappage fell — which is exactly what k rising says.

**Forward assumption (base case): hold k at the 2024 level.** Sensitivity in §6. If used-car prices keep falling from
2025 levels, scrappage recovers and k drifts back toward 1.1; if affordability stays tight, k keeps rising. Both
directions are small for the 12-month horizon.

### 2.5 The 7–12 cohort (the popular "fleet timing" story), on these curves

With k held at 2024: 7–12-year-olds number 76.7M (2022) → 85.1M (2024) → **87.8M peak in 2026** → 82.8M (2028), as
the 17M-unit sales years 2014–2019 pass through the bracket and the 2020–22 trough follows them in. True, but §5
quantifies what it is worth: about +0.16pp of TLF per year.

---

## 3. R(age) — relative insured-claim frequency per vehicle on the road

### 3.1 What it is, and what it is not

R is *insured physical-damage claims* (repairable + total loss, first-party and third-party) per registered vehicle,
relative to age 1. It bundles three things: **exposure** (older vehicles are driven less), **coverage** (older vehicles
more often carry liability-only, so a single-car loss produces no claim; but a two-car crash still produces a
property-damage-liability claim on the not-at-fault car), and **filing** (higher deductibles and self-pay on
low-value cars). It is not crash frequency, and it should not be sourced from crash data.

### 3.2 The evidence

- **Exposure.** EPA annual miles by age (ORNL **Table 3.14**): cars 13,843 at age 0 → 11,630 at 7 → 9,748 at 12 →
  6,962 at 20 → 5,358 at 30; light trucks run ~1,500–2,000 higher. Fleet-weighted 2024: **7+ vehicles drive 0.653×
  the miles of 0–6 vehicles.**
- **Claim mix, CCC national industry data** (quoted verbatim in `scripts/age_curves.py`): 7+ vehicles are "nearly
  45% of all repairable claims" (2024) and "almost 72% of valuations across all loss categories" (2024) against ~66% of
  the fleet; the average age of vehicles in claims was 7.6 years (2024) vs a fleet averaging 11–13; "only 26.3% of
  repairable ICE vehicles are three years or newer" (2024; ≈30% all-fuel once EVs and hybrids, 79% and 60% of which
  are ≤3 years, are added back).
- **Half-year exposure at age 0.** A model-year-t vehicle is on the road on average half of calendar year t. Without
  `e(0)=0.5` the fit cannot reconcile the ≤3-year share with the average claim age (it lands at 36% vs 30%).

### 3.3 The fit

One slope, starting at age 6 — the youngest bucket boundary CCC reports — fitted jointly with P (five parameters
total) to eight 2024 statistics (§5). Result: **flat through age 6, then −8.6%/yr.** The flat segment is a
choice, not a finding: when a second slope for ages 0–6 is left free, the fit returns +1.6%/yr with no meaningful gain
(the loss improves by less than one tolerance unit), so the data cannot tell a slight rise from flat there and the simpler form is kept.
Both halves are plausible: through age 6 nearly every vehicle is financed or leased and carries collision and
comprehensive, and mileage is near its peak (the 4–6 bracket is the largest single claims bucket, 24% of claims on
16% of the fleet); after 6, coverage is dropped, mileage declines, and small claims go unfiled.

### 3.4 Decomposition — how much of the decline is exposure

R(7+)/R(0–6) = **0.565** = miles ratio **0.653** × residual **0.865**. So about two-thirds of the age gradient is
simply that old cars are driven less; the remaining 13–14% is coverage and filing behaviour. That residual is where the
2024–25 deductible shift lives (CCC: $1,000+ deductibles +3.5pp in one year, +6pp in two) — it is a *level* effect on
claims that the industry-claims term of the identity already carries; do not put it in R.

### 3.5 What would upgrade R from fitted to measured

HLDI publishes insurance claim frequencies by vehicle age (collision, property-damage liability, comprehensive) from
insurer data covering most of the market. That is R measured directly, coverage included. `iihs.org` returned 404 on
every HLDI URL tried from this environment; see §7.

---

## 4. P(age) — total-loss propensity given a claim

### 4.1 The mechanism

An insurer totals a vehicle when repair cost plus rental and salvage considerations exceed a threshold share of its
actual cash value (roughly 70–80%, statutory in some states). Repair cost for a given crash is roughly flat in vehicle
age; value falls ~10–15%/yr. So P rises with age until nearly any significant crash totals the car. CCC's TCOR
figures — $5,721 for ≤6-year vehicles vs $3,682 for 7+ (2025) — are a *selection* effect of this rule (the expensive
repairs on old cars became total losses and left the repairable sample), not evidence that old cars are cheaper to fix.

### 4.2 The evidence

- "For claims that are three years old or newer, **1 in 10** are flagged as a total loss" (Crash Course 2026).
- "**Over 70%** of total loss valuations in 2024 were on vehicles 7 years or older"; "almost 72%" (2024/Q4); "74%
  through Q1 2025"; "73%" (2025/Q3); "over 72%" (2025/Q4).
- Average age of total-loss vehicles **10.6** vs repairable **6.8** (2024); 10.0 vs 6.1 in 2020.
- Overall TLF 22.3% (2024), 23.1% (2025) — `data/csv/ccc_tlf_annual.csv`.
- "The age mix of non-comprehensive valuations is highly representative of the vehicle age mix within the U.S. car
  parc" (2025/Q2) — i.e. R falling and P rising roughly cancel, which the fitted curves reproduce (TL share by
  bucket 1/10/17/39/33% vs fleet 5/15/16/29/35%).

### 4.3 The fit and its robustness

Logistic in age (four parameters), fitted jointly with R. P(0–6) = 12.7%, P(7+) = 31.7%; the same two numbers come out
at 12.6%–12.7% / 31.4%–31.8% under every survival assumption in §6, and the closed-form bucket derivation from CCC's shares
alone gives 13.4% / 32.2%. **The bucket values are solid; the interior shape between 7 and 15 is interpolation** — the
only anchors there are the 7+ aggregate and the 10.6-year average TL age.

### 4.4 What is NOT evidenced

- The "45.3% at 13+" anchor carried in the blueprint tab has **no source** in any CCC text on disk. Dropped. The fitted
  curve gives 36% at 13 and 44% at 17.
- P's *level over time.* Held fixed here on purpose: the fitted 2024 P applied to the 2019 fleet gives TLF 21.4% vs
  actual 19.2% — the level was lower in 2019 because used-car values were high relative to repair costs. That gap is
  the totaling-spread regression's job (`MODEL_BLUEPRINT.md` §3, spread cycle), not the cohort tab's.

---

## 5. Validation — fit and out of sample

Fitted on 2024 (eight statistics, five parameters; loss 1.0, i.e. every target within its stated tolerance):

| statistic (2024) | CCC | model | source |
|---|---|---|---|
| TLF, all loss categories | 22.3% | 22.3% | `ccc_tlf_annual.csv` |
| total losses from 7+ | 72% | 71.8% | 2024/Q4 "almost 72%" |
| repairables from 7+ | 45% | 44.3% | 2024/Q4 "nearly 45%" |
| repairables from ≤3 (all-fuel) | ~30% | 30.1% | 2024/Q4 "26.3% of repairable ICE" + EV/hybrid |
| avg age, claim vehicles | 7.6 | 7.7 | 2025/Q1 |
| avg age, repairables | 6.8 | 6.8 | 2025/Q1 |
| avg age, total losses | 10.6 | 10.6 | 2025/Q1 |
| P(≤3 yrs) | 10% | 10.0% | 2026 "1 in 10" |

Out of sample — **R and P frozen at the 2024 fit; only the fleet changes**:

| statistic | actual | model | error |
|---|---|---|---|
| 2020 avg age, claims / repairables / total losses | 6.9 / 6.1 / 10.0 | 7.2 / 6.4 / 10.3 | +0.3 / +0.3 / +0.3 yrs |
| 2025 total losses from 7+ | >72% | 72.5% | +0.5pp |
| 2025 repairables from 7+ | ~46% | 44.9% | −1.1pp |
| 2019 repairables from 7+ | 35% | 38.0% | +3.0pp |
| 2019 repairables from ≤3 | 38.5% | 35.4% | −3.1pp |
| 2019 / 2020 / 2025 TLF, demographics only | 19.2 / 20.6 / 23.1% | 21.3 / 21.4 / 22.3% | +2.1 / +0.8 / −0.8pp (= the non-demographic level) |

The 2020 and 2025 checks pass. The 2019 misses are informative: claims were *younger* in 2019 than the frozen curves
predict, by about 3pp of mix. Two known reasons, both real: the EV/hybrid share of young-vehicle claims roughly quadrupled
2019→2024 (CCC: EVs 1.4% → ~7% of ≤3-year claims), and 2019's young fleet had far less standard AEB, so per-vehicle
collision frequency of new cars has fallen relative to old ones. Either way, R is drifting slowly *against* young
vehicles over time; for a 12-month horizon, ignore it; for a five-year roll, let R(≤6) decay ~1%/yr.

---

## 6. Sensitivity — S is uncertain, the outputs are not

R and P refitted under four survival assumptions (k multiplier by 2024):

| k mult | VIO 2024 | share 7+ | R(7+)/R(0–6) | P(7+) | P(0–6) | demographic TLF drift, pp/yr 2019→25 |
|---|---|---|---|---|---|---|
| 1.000 (raw EPA shape) | 246M | 58.2% | 0.751 | 31.4% | 12.7% | +0.04 |
| 1.100 | 270M | 61.7% | 0.640 | 31.6% | 12.7% | +0.12 |
| **1.194 (fitted)** | **292M** | **64.5%** | **0.565** | **31.7%** | **12.7%** | **+0.16** |
| 1.300 | 318M | 67.2% | 0.500 | 31.8% | 12.6% | +0.18 |

Read across: the survival assumption moves R's slope a lot (0.50–0.75) and P not at all, because claims-by-age is
what CCC pins down and S·R is the product that produces it. **The finding — fleet ageing adds +0.16pp/yr to TLF
(range 0.04–0.18), about a quarter of the +3.9pp rise from 2019 to 2025 — is the same under every S.** The other
three-quarters are the level: the repair-cost/used-value cycle (the spread regression), technology, and filing
behaviour. That is the honest version of the "aging fleet" pitch and it is smaller than the popular one.

---

## 7. Manual pulls that would upgrade the curves (in order of value)

1. **HLDI — insurance loss statistics by vehicle age.** Collision and PD-liability claim frequency per insured
   vehicle year, by vehicle age (HLDI publishes these in its loss bulletins; search iihs.org/hldi for "vehicle age").
   Replaces the fitted R with a measured one and pins the ≤6 shape directly. `iihs.org` 404'd on every URL tried.
2. **CCC Crash Course 2026, Figures 18 and 22** (total-loss valuations by vehicle age group; total-loss values by age).
   Read the printed data labels — if a P-by-age-bucket series is charted it gives the interior of P directly, and it
   settles the unsourced "45.3% at 13+". The report body is ungated; the PDF is behind a Pardot form a human may submit.
3. **S&P Global Mobility, 2025 average-age release** (May 2025): VIO count, average age by body type, and any share-by-
   age-bracket figures. Confirms the two count anchors (289M, 66% 7+) from the primary source rather than via CCC.
4. **Experian Automotive Market Trends, Q3 2025** (VIO by model-year bracket). Resolves the "−12M ≤6-year vehicles"
   definition that no survival curve reproduces.
5. **A depreciation curve — value retained by age** (Cox/Manheim, Edmunds, or iSeeCars). With CCC's TCOR
   distribution this makes P *structural* (P = Pr[repair cost > θ·value(age)]) instead of fitted, and links it to the
   spread cycle explicitly.
6. Optional: Ward's or BEA car vs light-truck retail sales 2022–2025, to replace the FRED rescale in §1.

---

## 8. Files

| File | Contents |
|---|---|
| `scripts/age_curves.py` | everything above, end to end |
| `data/csv/ornl_tedb40_survival_by_age.csv` | EPA survival by age, cars and light trucks (Table 3.15) |
| `data/csv/ornl_tedb40_miles_by_age.csv` | EPA annual miles by age (Table 3.14) |
| `data/csv/ornl_tedb40_new_sales.csv` | Ward's new retail sales 1970–2021 (Table 3.6) |
| `raw/ornl/tedb40/extracts/ornl_tedb40_vehicles_in_operation_by_age.csv` (local only) | IHS cars/trucks in operation by age, 1970/2000/2013 (Tables 3.11/3.12) — sheet is marked "FURTHER REPRODUCTION PROHIBITED", so the extract is not committed; cite the ORNL table |
| `raw/ornl/tedb40/extracts/ornl_tedb40_avg_age.csv` (local only) | IHS/S&P average age 1970–2020 (Table 3.13) — same licence note |
| `data/csv/fred_LTRUCKNSA.csv` | FRED light-truck sales, monthly NSA |
| `data/csv/light_vehicle_sales_by_year.csv` | cohort sizes 1970–2025, cars and light trucks |
| `data/csv/age_curves.csv` | S, miles, R, P by age; 2024 fleet, claims and TL shares |
| `data/csv/age_curves_validation.csv` | every fit target, out-of-sample check, S check and sensitivity row |
| **`model/CPRT_Intermediate.xlsx`** | the workbook to copy from: every data tab, the fleet roll, Curves, Calibration (Solver), TLF_Roll, Spread_Reg, RPU_Reg, Checks. Built by `scripts/build_intermediate_xlsx.py`, verified by `scripts/verify_intermediate_xlsx.py` |
