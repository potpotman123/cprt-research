# Memo appendix: the three theses as encoded in the model (CPRT_Model_v2.xlsx, 2 October 2026)

FY27E legacy service revenue, $m. Case 0 is the Street-implied path; case 1 is the known-facts path (Progressive runoff laps, coverage flat, no thesis). Every input behind these numbers is listed on the workbook's Sources tab with its label and source.

| Case | FY27E | Δ vs case 1 | Δ vs case 0 | Δ vs JPM $4,061m |
|---|---:|---:|---:|---:|
| 0 Street-implied (coverage recovery reverse-solved to JPM) | 4,061.0 | +104.0 | — | 0 |
| 1 Known facts / thesis 1 sticky | 3,957.0 | — | −104.0 | −104.0 |
| 1b Premium-response coverage (mechanistic bull) | 4,103.5 | +146.5 | +42.5 | +42.5 |
| Thesis 2 on case 1 (observed CCC trend; Mitchell price) | 3,948.1 | −8.9 | −112.9 | −112.9 |
| Thesis 3 on case 1 (probability-weighted carrier moves) | 3,930.9 | −26.1 | −130.1 | −130.1 |
| All three | 3,922.1 | −34.9 | −138.9 | −138.9 |
| Bull (premium-response, ASP +6%) | 4,132.4 | +175.4 | +71.4 | +71.4 |

| Thesis | Mechanism in the model | Key inputs and labels | Source | What it is worth |
|---|---|---|---|---|
| 1 Once burned, twice shy | Insured claims = fleet claims × physical-damage coverage index; three forward paths (sticky, premium-response, Street-implied) | Uninsured rate 12.4% (2017) → 15.4% (2023), VERIFIED endpoints; collision share 76% / 77% / 77% (2021–23), VERIFIED republication via archived III pages; insurance CPI and earnings, VERIFIED; two-point response 0.59, UNVERIFIED; r = 3.53%, MEASURED identity | IRC release 20 Feb 2025; III analysis of NAIC 2023; BLS CUUR0000SETE and CES0500000003 | JPM's FY27 needs insured volume 3.5% above the known-facts path, more than the whole measured 2017–23 coverage decline (about 2.2%, all from the uninsured leg; collision take-up was flat through the spike) returning in one year: $104m. Caveat the memo must carry: the insurance CPI is falling (−5.1% y/y, Aug 2026); if coverage responded as in 2017–23, volumes would recover (case 1b) |
| 2 The seesaw breaks | Sourcing shift → repair-bill saving → fewer total losses (η from the engine); recycled displacement → bids → prices (engine endpoint scaled) | Shares 66.8/22.7/10.5, VERIFIED; parts 40% of bill (36–44%), VERIFIED range; AM price 0.73, VERIFIED historical; recycled price 0.60, ASSUMED; path: AM +1.7 pts/yr, recycled −0.2 pts/yr, VERIFIED trend; donor exposure 25%, bid ratio 1.5×, transmission 50%, ASSUMED | CCC Crash Course 2026; Mitchell Q2 2017 ITR; aftermarket bridge engine | $9m on the observed trend; the memo's 5.5-pt stress is worth about 0.4% of the bill at sourced prices (the engine's 1.03% needed the assumed basket). Shifting recycled to aftermarket raises cost at sourced prices, so the "both sides" claim rests on OEM displacement. LKQ 10-K: limited salvage supply could raise its costs (counter-evidence) |
| 3 Structural share shift | Share = Σ weights × allocation; probability-weighted moves reproduce the inherited paths; seller terms | State Farm −5 pts × 45%, Other −5 pts × 45%, GEICO +12 × 60% (off), Progressive −20 realised: UNVERIFIED dated expert items; parity facts VERIFIED from RB Global 10-K and proxy and Copart 10-K | RB Global FY2025 10-K, 2026 DEF 14A; Copart FY2026 10-K; Downloads share-loss build (expert, dated) | −$26m (share 56.6% → 55.3%, as in the memo). The Progressive move is derived in-model at −5.0% of FY26 service revenue (−4.3% of total revenue), replacing the asserted 5.2%. IAA acreage 14,803 verified; Copart's 19.1k acres has no located source |
