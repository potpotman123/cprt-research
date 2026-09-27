# Modern repair-frequency search: findings and model decision

September 26, 2026. Ten targeted public-web queries plus bounded primary-source reads. No OCR, paid access, outreach or bulk scrape. A direct historical PDF request failed with 403; indexed primary text was readable. This is a bounded search result, not proof that relevant public data do not exist.

## Outcome

No current US component-involvement/repair-versus-replacement table cross-classified by car/crossover/pickup and vehicle age was found. Modern aggregate metrics, a controlled young-vehicle EV/ICE comparison, historical age-dependent parts sourcing, and a body-type cycle-time table were found. These answer adjacent questions but must not be substituted for missing repair frequencies.

## Usable findings

CCC Crash Course 2026 reports overall parts counts and sourcing metrics for national non-comprehensive repairable appraisals. Figure 37 shows 13.0 replacement parts per claim in 2025; the report also discusses lower OEM counts and higher aftermarket dollar share. Figures 39-40 distinguish initial estimates and supplements. These are useful aggregate checks but cannot specify which panels are replaced on older SUVs. Do not spread the aggregate decline proportionately across every component or segment. A change in repaired vehicle mix, exclusion into total losses or estimating practices can change the average without uniformly changing component involvement. Earlier report vintages show a different 2024 aggregate count; retain vintage identifiers rather than combining them silently.

https://www.cccis.com/reports/crash-course-2026

CCC's July 2022 EV/ICE comparison explicitly restricts claims to driveable front-impact collision losses and vehicles current to three years old, with selected comparable models. This supports using age, impact and driveability controls. It does not estimate a current older-car/pickup/SUV repair premium, and luxury midsize SUVs must not be compared directly with small nonluxury cars as though only body type changed.

https://www.cccis.com/news-and-insights/posts/electric-vs-ice-vehicles-unpacking-repair-cost-impacts

CCC's 2014 Parts of the Vehicle Repair article reports that, in 2013, OEM parts represented 47.6% of replacement dollars but 59.0% of replacement count for vehicles seven years and older. Historical evidence only. It demonstrates that OEM-only catalog pricing is not equivalent to observed repair spending and that dollar shares cannot be used as unit sourcing probabilities. Do not infer an equivalent-part OEM discount from aggregate source-type averages: component composition differs.

https://studylib.net/doc/18165568/parts-of-the-vehicle-repair

The 2016 Crash Course figure 53/body-type discussion concerns cycle time and labor hours per repair day. Those measures do not establish labor hours per repair, repair prices, or component frequencies. No repair premium is calculated from that table.

https://www.tech-cor.com/OtherResources/CCC-Crash-Course-2016.pdf

CCC glossary search results confirm some body-category and claims/parts measures exist in its analytics product. They do not provide the underlying observations, confirm our access, or demonstrate that our requested cross-tab can be exported.

## Architecture decision after the search

Maintain one common-frequency repair index first, labeled an index rather than a measured segment average. Keep three separate uncertain mechanisms: (1) which components are involved/repaired/replaced; (2) OEM/aftermarket/recycled sourcing conditional on component and age; (3) parts/labor cost for those operations. Current evidence cannot identify all three by body type.

Use the historical Mitchell frequencies only as provisional common weights, preserving their population and age limitations. Modern CCC totals can challenge aggregate plausibility, not calibrate missing segment frequencies. Do not fill SUV/pickup/car frequency columns by copying pooled values and labeling them observations. Do not populate missing component costs with zero. The existing two-panel index is incomplete and remains so.

The low-cost fallback is a common-work comparison across a small fixed set of representative older models, with source-type price scenarios. That can test whether a large repair-price premium is plausible without claiming to know body-specific crash patterns. Body-specific frequencies require a suitable claims/repair export or a new credible public release; random public estimates lack a representative denominator. All-claim total-loss inference remains a separate step because repairable samples exclude many high-cost outcomes.

No new repair-cost multiplier, EPS forecast or price target is justified by this search. No model inputs were replaced. Further broad searches are unlikely to be the best immediate use of effort; any substantial collection or paid access should be scoped and approved before execution.
