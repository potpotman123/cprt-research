# Follow-up: an unexpected source challenges the old-age curve assumption

28 September 2026. Standing process principles now live in /RESEARCH_PRINCIPLES.md, linked from the root README and AGENTS.md. This follow-up used ten bounded search queries and selective text reads, then a tiny local shape calculation. No OCR, paid collection, source-chart digitization or forecast revision.

## End-to-end method, rationale and alternatives

1. **Define the missing observation.** We need age-specific coverage/claim selection changes, not another all-age TLF number. An older historical age curve can still test whether our structural assumptions are reasonable, but cannot explain a current change by itself.
2. **Search outside the investment narrative.** Search HLDI research, actuarial datasets, repair cash-settlement terminology and claims-provider documentation. These sources may disclose fields or comparison groups incidental to their main topic. A ticker search would be less likely to find them. Public actuarial examples from other countries were not substituted for U.S. current cohorts.
3. **Inspect methods before collecting chart points.** A seven-page HLDI report surfaced through a study of vehicle fires. Its text specifies the comparator population, denominator and age-pattern qualification. Reading those sections is cheaper and more reliable for this question than extracting dozens of unlabeled graph coordinates. The primary-authored report is accessible on a third-party host; do not call that an official-host retrieval.
4. **Test the implication using existing model distributions.** Rather than treating an old chart as a precise 2025 curve, allow a broad family of fixed curves that rise and then fall. Compute the maximum composition effect this family permits. This avoids fitting the very residual we seek to explain.
5. **Qualify the earlier result and preserve both versions.** The earlier monotonicity ceiling is conditional, not a universal exclusion of composition. Save the new assumption and bound separately; do not overwrite source observations or forecast inputs.
6. **Reassess the overall approach.** A modern matched age/coverage panel remains superior for identification. More curve fitting or bulk auction listings cannot recover unfiled claims. The cheap bound answers whether this newly discovered shape feature alone rescues the simple explanation under our current weights. It does not answer whether the weights themselves are right.

## New source evidence

[HLDI Bulletin 39(7), April 2022: Noncrash fire insurance losses overview](https://platform.vox.com/wp-content/uploads/sites/2/chorus/uploads/chorus_asset/file/24341429/39_07.pdf), authored by HLDI, mirrored by Vox. CY2020 data. Printed p.3 / Figure 3 includes collision TLF by exact age: the text says it generally increases until about age 20 and then declines. Printed p.4 / Figure 5 provides collision frequency by age/body, with insured vehicle-years as denominator. Methods on p.2 warn that total-loss identification arrives via salvage notification and recent data may undercount totals. Results are not demographic/geographic-standardized.

These are historical cross-sections, not a 2024–25 coverage-transition panel. The source supports challenging monotonicity and considering reporting development. It does not establish why the oldest-age curve falls or that notification delays changed in 2025.

## Cheap recalculation

Retain our modeled 2024/2025 claims-weighted exact-age distributions, ages 13–45, vintage body mapping. Permit any one common probability curve in [0,1] that rises up to an assumed peak, then falls. No empirical probability levels are imposed. For each possible interval containing the peak, calculate its change in population share; the largest positive change bounds the effect of every curve in this family. This follows because each probability level's superlevel set is an interval containing the peak.

| Assumed peak age | Generous maximum composition-driven TLF increase |
|---|---:|
| 18 | 0.014 pp |
| 19 | 0.044 pp |
| 20 | 0.227 pp |
| 21 | 0.227 pp |
| 22 | 0.227 pp |

The most permissive interval for peaks 20–22 is ages 20–33. Its extreme 0%-outside/100%-inside curve is a ceiling device, not a realistic prediction. The HLDI plotted age curve stops at 30; applying the assumed shape through model age 45 is an explicit tail assumption. No baseline TLF constraint is imposed, so the ceiling is deliberately loose.

Within this alternative family, current modeled composition still cannot generate the full +1.70 pp older-bucket increase. This does NOT rehabilitate the former claim as an unconditional result: time-varying curves, body-specific shapes, coverage composition and wrong claim weights remain possible. The source's cross-section also does not establish that this exact shape persists across years.

## Revised next evidence priorities

- HLDI's exact-age collision frequency is a concrete historical reference for checking the shape of our claim-propensity assumption. It is conditional on insured exposure; our claim propensity per surviving vehicle also includes coverage. Do not replace one with the other directly.
- Seek repeated versions of age/coverage exhibits or a provider summary of their underlying counts before buying or scraping records. A single 2020 pandemic cross-section cannot identify 2025 changes.
- Claim development is now an explicit comparability check: recorded totals may mature after initial claim counts. This is a possible measurement issue, not an explanation proven by the source.

No provider was contacted. The search failed to retrieve a current matched panel; that gap remains. The search nevertheless changed a consequential modeling assumption, which is useful progress.

## Search record

1. site.iihs.org "vehicle age" "coverage" "older" HLDI collision
2. site.mitchell.com "2025" "total loss" "age" trends
3. site.crashnetwork.com "cash" "2025" repair
4. site.risk.lexisnexis.com "vehicle age" "collision" "2026"
5. "vehicle age" "collision coverage" "percentage" HLDI
6. "collision" "coverage retention" vehicle age
7. "repair" "cash out" "2025" "Tractable"
8. "auto insurance" "vehicle age" "data" "CAS"
9. site.iihs.org "39" "7" "noncrash" "2022"
10. site.iihs.org "collision coverage" "30" "2020" fire

Other results: Mitchell current repair-age commentary (broad, not older claim coverage); HLDI ADAS studies (younger populations); foreign actuarial sample datasets (wrong market/period); public fleet insurance tenders (wrong population); third-party summaries repeating CCC (not independent); a Copart research website (not used, potential circular research evidence). None was treated as a new model input.

Calculation: unimodal_check.py; results and input hash: unimodal_bound.json. Twenty-two checks cover normalization and smooth hump-shaped functions lying below the computed ceilings. Arithmetic checks do not validate economic assumptions.
