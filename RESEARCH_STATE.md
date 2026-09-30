# Copart research state — publication snapshot, 30 September 2026

**Agreed investment conclusion:** We have an intellectually interesting structural pitch, but have not established one measurable forecast error supported by evidence and tied to an observable near-term catalyst. There is not yet a demonstrated actionable reason for investors to adopt the view within twelve months. An earnings date is an observation window; a catalyst requires an identifiable surprise that changes a forecast or valuation assumption.

The revenue architecture is coherent for conditional scenarios. The magnitude, benchmark gap and timing of the two competition theses remain insufficiently established for a high-conviction 12-month short. The absence of a catalyst is central to the pitch audit and must remain visible in the Excel/Fable handoff.

This Markdown file is the recovery index, not a replacement for the model files and datasets. Equations are preserved in the implementation and model notes; numeric inputs, calibrations, outputs and evidence records remain in their original directories. Publication preserves the work; it does not validate the assumptions.

| Subject | Authoritative entry point |
|---|---|
| Self-contained prompt for a new high-reasoning session: two theses → catalyst search → decision → model integration, with the load-bearing unsourced assumptions listed | [Prompt](PROMPT_HIGH_REASONING_FABLE_2026-09-30.md) |
| PM assessment of both competition theses, opposing evidence, missing proof, additions and comparison with prior successful pitches | [Full pitch audit](docs/pitch_audit_2026-09-29/README.md) |
| Catalyst windows, what each would need to reveal, limits of earnings revisions | [Catalyst assessment](docs/catalyst_assessment_2026-09-29/README.md) |
| Current revenue architecture, assumptions, equations/code, scenarios, fee and timing guards | [Revenue architecture](model/revenue_architecture_2026-09-28/README.md) |
| Named forecast benchmark and scope | [Evidence update](model/revenue_architecture_2026-09-28/EVIDENCE_UPDATE.md) |
| Aftermarket sourcing, donor/rebuilder economics, repair-demand and scarcity feedback | [Aftermarket model](model/aftermarket_bridge_2026-09-29/README.md) |
| User-supplied CCC age/body data: all extracted observations, source cells, derived weights and calibration | [CCC integration](model/ccc_age_body_2026-09-29/README.md) |
| Quantity shares, repair-bill exposure, 25% and 1.5× assumptions, offsets and interview requests | [Parameter audit](docs/aftermarket_parameter_audit_2026-09-29/README.md) and [forward assumptions](docs/aftermarket_parameter_audit_2026-09-29/FORWARD_ASSUMPTIONS.md) |
| Historical component price evidence and limits of discount extrapolation | [Transition evidence](docs/aftermarket_transition_evidence_2026-09-29/README.md) |
| Evidence for the 5.5-point shift and what Bidmate can establish | [Adoption/Bidmate review](docs/bidmate_adoption_2026-09-29/README.md) |
| Insurance carrier allocation, contract timing and concessions | [Carrier test](docs/carrier_test_2026-09-28/README.md), [share-build review](docs/FABLE_SHARE_BUILD_REVIEW_2026-09-27.md), [contract arithmetic](docs/repair_research_2026-09-26/contract_scope_screen/README.md) |
| Revenue-model audit, source/calibration checks and reproducible Excel handoff | [Audit](docs/model_audit_2026-09-29/AUDIT.md), [Fable instructions](docs/model_audit_2026-09-29/FABLE_HANDOFF.md), [ZIP](docs/model_audit_2026-09-29/CPRT_revenue_Fable_handoff_2026-09-29.zip) |
| Supplied conceptual Mermaid diagrams | [Archived images](docs/revenue_architecture_diagrams_2026-09-30/README.md) |
| Dataset families, including failed/legacy series | [Dataset index](data/csv/README.md) |
| Auction listing versus completed-sale limitations and prior failed searches | [Scraper status](docs/scraper_status_2026-09-28/README.md) |
| Earlier research history and methods | [Research principles](RESEARCH_PRINCIPLES.md), [historical handoff](HANDOFF.md), [lab notebook](findings.md) |
| Exact publication inventory and exclusions | [Repository snapshot](docs/repository_snapshot_2026-09-30/README.md) |

Important distinctions to preserve:

- The approximately $91m larger aftermarket scenario is versus its own reference. The CCC version is roughly $59m, or 1.4%, below the dated JPM FY27 ex-ACV service forecast. It is not a measured consensus miss.
- The full 5.5-point eligible-basket shift is applied throughout FY27 in the saved case. A gradual three-year national adoption path was discussed but has not been implemented. Do not retain the old revenue delta under a different timing narrative.
- Increased aftermarket usage does not by itself prove recycled displacement or lower auction prices. Rebuilder economics, additional repairs and donor scarcity can offset the proposed headwind.
- The two competition theses need one consistent, dated combined forecast. Do not add independent scenario losses from different references or repeat already included account losses.
- The CCC workbook supplies age/body total-loss frequencies and mix, not aftermarket shares, threshold elasticities or bid responses. The original and CCC calibration families have different targets and limitations.
- Global FY26 unit growth of −5.5%, versus −3.1% excluding CAT, supports a catastrophe comparison effect at that scope. It is not an available adjustment to Q4 US insurance's −7.5% sold-unit figure. Assignments and sold units remain distinct.
- Earnings, cash flow, WACC and valuation remain the user's planned subsequent work. Those models have not been silently completed.

All nonignored research artifacts in this repository are included in this publication snapshot. Raw licensed/private source material, large collection caches/databases and environment files remain local under the existing repository rules; extracted analytical datasets and source provenance are published. The snapshot inventory records this boundary explicitly. A GitHub clone is therefore an analytical archive, not a byte-for-byte backup of the research computer or a verbatim chat transcript.
