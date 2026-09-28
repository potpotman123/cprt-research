# Validation status: repair-cost response remains unidentified

28 September2026. Reused prior historical tests, six discovery queries and bounded primary-source retrievals; one small diagnostic. No paid collection, bulk downloads, OCR or forecast changes.

## Finding

The current model assumes that a5% repair-cost increase converts about1.48% of all baseline claims, or1.92% of baseline repairables, into additional totals in FY27Q1. With baseline TLF22.83%, that produces6.49% additional totals at fixed claim activity. This implied mass near the threshold explains why a modest cost shock produces a large revenue response. It has not been measured independently.

`threshold_validation_cells.csv` exposes the threshold and switching mass in all24 age/body cells. `threshold_validation_results.json` gives quarterly weighted results and source hashes. Twenty-four monotonicity checks pass. These are model diagnostics, not empirical validation. The chosen recovery schedule changes with damage rank; the switching band is therefore calculated from both solved cutoffs, not a fixed threshold divided by1.05.

## Existing evidence does not validate the response

`WITHIN_AGE_ECONOMICS.md` already tested historical proxies. Broad price indices matched the aggregate TLF change approximately but not all age results or selected repair costs. Substituting observed repaired-vehicle mean growth for latent same-damage cost growth failed because the repaired population changes when vehicles cross into total loss. `JOINT_CLAIM_SELECTION.md` found no case meeting its tighter joint tolerances; looser results are not a confidence interval. Do not rerun these fits and call the same endpoints independent validation.

Fitting total-loss probability establishes the distribution's cumulative mass at the threshold. Fitting average repaired cost adds a truncated-mean constraint. Neither uniquely determines how much probability lies immediately around that threshold without the imposed distributional family. A historical level fit therefore does not establish the derivative used in the sensitivity screen.

## External source pass

- [Mitchell estimating documentation](https://wwwca.mymitchell.com/tchs/helpfiles/RCW/1033/Content/40682.htm), retrieved2026-09-28, explains that the threshold is set in an estimate profile, triggers a potential-total-loss notification, and the user makes the final designation. This confirms a workflow distinction between an alert and a disposition; it supplies no empirical switching distribution or error rate. Do not interpret the economic inequality as a fully observed deterministic decision rule.
- [CCC Total vs Repair glossary](https://help.cccis.com/webhelp/insurance_company/thecccportal/Content/Insurance/AnalyticsTableau/CategorizedGlossariesDropdn/TotalvsRepairGlossary.htm) appeared in search with repair-option and salvage-comparison fields, but full retrieval failed. It remains a schema/access lead, not an available dataset. Earlier salvage glossary work was already documented in `docs/research_execution_2026-09-26/repair_recovery_source_audit.md`.
- Creative public-record route: [NHTSA investigation attachment](https://static.nhtsa.gov/odi/inv/2019/INRD-PE19004-75786.pdf) and [Smith County agenda packet](https://smithcountycommissioner.com/wp-content/uploads/2025/03/3-18-2025_Commissioners_Court_Agenda_Packet-RE2.pdf) surfaced indexed estimate/valuation fields. Reader rejected their sizes,41.3MB and15.5MB. No bulk retrieval/OCR attempted. Even accessible isolated claims would be mechanism examples, not a representative threshold-density estimate; investigation and public-fleet selection differ from insured private vehicles.
- CISS/CRSS: prior feasibility work remains useful for collision mix but does not supply the matched insurer-approved repair/ACV/net-salvage comparison needed here. Do not substitute crash severity for economic damage dollars.

Queries: `"total loss" "repair cost" "vehicle value" distribution HLDI`; `site.cccis.com "repair costs" "percent" "actual cash value"`; `site.mitchell.com "total loss" "repair" "threshold" 2025`; `site.nhtsa.gov CISS repair cost vehicle value total loss`; `site.cccis.com "repair" "ACV" "percent" "2025"`; `site.mitchell.com "repair" "cash value" "percentage" total loss`.

## Decision and thesis discipline

Do not promote the ±$106m repair-cost sensitivity into a forecast or investment thesis. Keep carrier allocation isolated. The potentially material non-carrier question is whether economics or filing selection changes the near-threshold population, and whether auction proceeds reinforce or offset the unit effect. It remains a hypothesis, not a demonstrated opportunity.

A useful validation export would contain de-identified claim/estimate-version IDs, period, body/model year, coverage, damage scope, initial/final repair estimates, ACV, expected net salvage and final repair/total disposition. Include both repaired and totaled cases, not only auction inventory or disputes. A representative histogram of repair-versus-total cost gaps and subsequent dispositions could be sufficient and cheaper than individual records. Access has not been established and no outreach is authorized.

Stop further broad searches on this branch pending a concrete dataset lead. Next practical non-carrier research priority is ancillary-service incremental revenue: use the documented sell-side offset expectation as the benchmark, distinguish adoption from pricing and waived/displaced fees, and keep undisclosed quantities explicit. Do not force this or any other mechanism to deliver a large delta. The goal is a supported difference versus expectations; magnitude alone is not validation.
