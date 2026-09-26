# E1 step 1 — light-truck share of Copart's listed pool, 2022–2026 (the free reality check on the fleet roll)

*2026-09-26. Script `scripts/experiments/e1_listed_body_share.py`; data `data/csv/listed_body_share_monthly.csv`. No network:
100 archived `lot.xml` page files (`raw/lotxml/`, Internet Archive captures 2022-08 → 2026-01) and 17 nightly live captures
(`data/cprt.db` `lot_snapshots`, 2026-09-08 → 09-25). Requests: 0. Usage: ~45k tokens including the classifier.*

## What was done

Every listed lot's make/model slug was classified as **CAR**, **light truck** (pickup ≤ 10,000 lb GVWR, SUV/crossover, van —
Ward's/EPA convention, crossovers are light trucks) or **OTHER** (class 3+ trucks, motorcycles, RVs, trailers, equipment,
boats, unrecognised). Share = LT ÷ (CAR + LT). Pages within a capture are unioned on lot id. Salvage-title and clean-title
lots are reported separately because the clean-title pool (dealer, fleet, charity consignments) is a different business.
Ambiguous crossovers (Outback, Soul, Niro, EV6, Crosstrek, Kicks, HHR, Element, ID.4, Ioniq 5) are counted as light trucks
in the headline and as cars in the `*_exambig` columns; the band is ~1.8pp.

Coverage on live nights: OTHER 6.1%, unclassified 2.4% (the top unclassified tokens are "other", RV brands, boats and
equipment — not light vehicles), so 91–92% of listed lots are classified light vehicles.

## Result (MEASURED)

| Year (archive captures) | n captures | LT share, salvage-title | LT share, all light | LT share, clean-title | pickup / SUV / van, % of light |
|---|---|---|---|---|---|
| 2022 (Aug–Dec) | 4 | 46.3% | 47.4% | 51.8% | 9.9 / 33.0 / 4.6 |
| 2023 | 7 | 48.4% | 49.4% | 53.2% | 10.2 / 34.6 / 4.6 |
| 2024 | 9 | 50.8% | 51.7% | 55.0% | 10.2 / 36.9 / 4.6 |
| 2025 | 6 | 54.0% | 55.0% | 58.4% | 10.9 / 39.4 / 4.8 |
| Jan 2026 | 1 | 55.4% | 56.4% | 60.0% | 10.9 / 40.9 / 4.7 |
| **Sep 2026 (live, 17 nights)** | 17 | **56.7%** | 58.2% | 63.5% | — |

Against the fleet roll's modelled light-truck share of **total losses** (`asp_vintage_effect.csv`, column `lt_share_tl`):

| | 2019 | 2024 | 2026 | 2027 | 2030 |
|---|---|---|---|---|---|
| Roll: LT share of modelled total losses | 50.7% | 57.2% | 60.7% | 62.4% | 67.7% |
| Listed pool, salvage-title | — | 50.8% | 56.7% (Sep) | — | — |
| Gap (roll − listed) | — | +6.4pp | +4.0pp | — | — |

**Gate: passed.** The kill rule was a divergence of more than 10 points; the gap is 4–6 points and closing. The listed pool
runs *below* the roll and rises *faster*: +2.7pp/yr listed (2022→2026) versus +1.7pp/yr modelled. Both are consistent with
the mechanism — the truck-heavy 2014–2019 model years are entering the totaling ages now — and the listed series is the
more direct measurement of Copart's own mix.

Two other things the slugs say, for free:
- **Trucks in the pool are newer than cars.** Median model year of listed light trucks is 2018 on live nights versus 2016
  for cars, and the truck median has advanced from 2013 (2022) to 2018 (2026) — faster than one year per year. Newer
  trucks at the same age-of-totaling means higher sticker per unit: the body-mix price effect (E8) has a vintage
  component on top of the class differential.
- **The SUV/crossover share does all the work.** Pickups are flat at ~10–11% of the listed light pool; SUVs went from 33%
  to 41%; vans flat. The "truck wave" is a crossover wave.

## Caveats (print them)

- Listed inventory, not total losses; includes non-insurance consignments. The salvage-title column is the closer
  comparator but still not a total-loss count.
- Archive captures can be page-out-of-sync (see `ARCHITECTURE.md`); union counts are used only for *shares*, which are
  insensitive to the sync problem because the mix is similar across pages. Two archive months (2023-10, 2025-10) have only
  page 4 on disk and are empty rows.
- Body classification is a lookup on ~330 model tokens; the 1.8pp ambiguity band is stated. Crossover treatment follows
  BEA/Ward's (light truck); the EPA/NHTSA fuel-economy classes would move a few models the other way.
- The roll's share is of *modelled* total losses (fitted R and P); the listed share is of *listings*. Agreement within
  4–6 points is a consistency check, not a validation of R and P by body.

## What it means for E1 and the pitch

- The roll's body split survives contact with Copart's own listings. E1 steps 2–6 (body-level totaling propensity and
  value) are worth the fetches; nothing needs reconciling first.
- For the model, the listed series is a usable *measured* input for the body-mix column on `ASP_Drivers`: use the
  salvage-title LT share by year (2022–2026) in place of the roll's modelled share for the historical rows, and the roll for
  2027+. That still needs the truck-vs-car value ratio (E8) to become a pp-of-ASP number.
