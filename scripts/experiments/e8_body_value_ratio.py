#!/usr/bin/env python3
"""E8 — light-truck vs car value ratio at the same age, for the body-mix column on ASP_Drivers.

ratio = (new-price ratio LT/car, KBB ATP Aug-2026 weighted by an ASSUMED segment mix) × (5-yr retained-value ratio LT/car, iSeeCars 2026)
Sources on disk: data/csv/kbb_atp_by_segment_2026-08.csv (VERIFIED), raw/iseecars/iseecars_hold_value.txt (VERIFIED: 5-yr depreciation
trucks 34.2%, SUVs 44.9%, overall 41.8%; no car-only figure published). Listed-pool body weights from E1 step 1 (MEASURED).
"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
atp = {r['segment']: float(r['atp_aug2026_usd']) for r in csv.DictReader(l for l in open(ROOT/'data/csv/kbb_atp_by_segment_2026-08.csv') if not l.startswith('#'))}
# ASSUMED within-body segment mixes for the salvage pool (mass-market weighted; luxury excluded; subcompact car Aug-26 print is anomalous, +50% YoY, so cars use compact/mid-size)
car = 0.55 * atp['Compact Car'] + 0.45 * atp['Mid-size Car']
suv = 0.10 * atp['Subcompact SUV/Crossover'] + 0.45 * atp['Compact SUV/Crossover'] + 0.35 * atp['Mid-size SUV/Crossover'] + 0.10 * atp['Full-size SUV/Crossover']
pick = 0.75 * atp['Full-size Pickup Truck'] + 0.25 * atp['Small/Mid-size Pickup Truck']
van = 0.7 * atp['Minivan'] + 0.3 * atp['Van']
w_pick, w_suv, w_van = 10.9, 40.9, 4.7          # E1 step 1: % of listed light pool, 2025-26 (MEASURED)
lt = (w_pick * pick + w_suv * suv + w_van * van) / (w_pick + w_suv + w_van)
sticker = lt / car
ret_truck, ret_suv, ret_all = 1 - .342, 1 - .449, 1 - .418     # iSeeCars 2026, 5-yr retained value
ret_lt = (w_pick * ret_truck + (w_suv + w_van) * ret_suv) / (w_pick + w_suv + w_van)
ret_car = ret_all                                               # ASSUMED: no car-only figure; overall used as proxy
retention = ret_lt / ret_car
print(f"new-price: car ${car:,.0f}  SUV ${suv:,.0f}  pickup ${pick:,.0f}  van ${van:,.0f}  LT blended ${lt:,.0f}  -> sticker ratio {sticker:.2f}")
print(f"5-yr retained value: LT {ret_lt:.3f} (trucks {ret_truck:.3f}, SUVs {ret_suv:.3f}) vs car proxy {ret_car:.3f} -> retention ratio {retention:.2f}")
print(f"value ratio at age 5 = {sticker*retention:.2f}")
lo, hi = sticker * 0.85 * retention * 0.95, sticker * 1.05 * retention * 1.03
print(f"range from mix/retention assumptions: {lo:.2f}–{hi:.2f}; recommended ASP_Drivers!B4 = {round(sticker*retention,2)} (ASSUMED at age ~10: retention convergence unknown)")
