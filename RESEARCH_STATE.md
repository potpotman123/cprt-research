# Copart research state — updated 1 October 2026

**Agreed investment conclusion:** We have an intellectually interesting structural pitch, but have not established one measurable forecast error supported by evidence and tied to an observable near-term catalyst. There is not yet a demonstrated actionable reason for investors to adopt the view within twelve months. An earnings date is an observation window; a catalyst requires an identifiable surprise that changes a forecast or valuation assumption.

The revenue architecture is coherent for conditional scenarios. The magnitude, benchmark gap and timing of the two competition theses remain insufficiently established for a high-conviction 12-month short. The absence of a catalyst is central to the pitch audit and must remain visible in the Excel/Fable handoff.

**30 September expectations/catalyst follow-up:** the held reports now supply a named operating hurdle: Stephens 20 August assumes US fee units −1% in FY27 Q1, then +2% in Q2–Q4, with +2% US fee RPU. Barclays already incorporates net contract volume losses and 25–50 bp take-rate pressure. Neither thesis establishes evidence that those assumptions will be missed; JPM's quarterly operating drivers remain undisclosed. The new filings verify contractual contestability, but do not identify another award, renewal date or IAA-only land parity. Clean listed-inventory share is 57.2065% across four nights, not an equilibrium flow share. RB Global's 2025 automotive lots are 2,447.7k, differing from Stephens' illustrative 2,516k. No central forecast or workbook was changed. The approved public pass was completed with access failures preserved; it cannot prove the absence of a catalyst. **Recommendation: structural research; do not pitch either mechanism as an established catalyst-backed short.**

**1 October affordability and loan follow-up:** [Kyle call and three-source assessment](docs/affordability_2026-10-01/README.md) distinguishes physical-damage coverage attrition from repairable nonfiling. Verified financing averages near70 months put much of the 2021–22 cohort into2027–28, with wider60–84-month timing2026–29. Standard amortizing payoff releases cash; no evidenced maturity cliff. ABPA30 selected interviews explain hardship but not cancellation prevalence; Experian measures registered fleet; iSeeCars retained asking values are not salvage prices. [New isolated sensitivity](model/loan_payoff_2026-10-01/README.md): hypothetical1.5% uniform unit loss lowers FY27 legacy service $46.25m;10% repairable nonfiling alone leaves revenue unchanged. No observed incremental coverage coefficient, named catalyst or central forecast change. Six-query discovery and access failures preserved; no outreach or agents.

**1 October tariff counterfactual:** [Tariff/adoption sensitivity](docs/tariff_counterfactual_2026-10-01/README.md) verifies Taiwan's qualifying 15% combined-duty implementation from May 1 using CBP. PartsTrader observes muted AM price inflation versus OEM/recycled, challenging the premise that tariffs necessarily suppressed relative competitiveness. A hypothetical 30% customs/untaxed-price ratio, half/full dollar pass-through and assumed odds elasticity 2 gives +0.84/+1.69pp AM physical share from a 25% baseline for 15%→0 duty. Zero pass-through gives zero; competitor price cuts can reverse the sign. No causal elasticity, China-weighted rate, repeal catalyst or Copart revenue input admitted. Calculator, alternatives, exact queries and source hashes saved.

This Markdown file is the recovery index, not a replacement for the model files and datasets. Equations are preserved in the implementation and model notes; numeric inputs, calibrations, outputs and evidence records remain in their original directories. Publication preserves the work; it does not validate the assumptions.

| Subject | Authoritative entry point |
|---|---|
| User-requested reverse stress: explicit assumptions producing 2%/3%/5% JPM misses, with catalyst gates still open | [Conditional short hurdles](model/reverse_short_2026-09-30/README.md) |
| Latest one-page investment decision and conditional model-admission result | [PM brief](reports/pitch_decision_2026-10.md) |
| Named quarterly expectations, missing operating inputs and source locators | [Expectations sheet](reports/expectations_sheet_2026-10.md) |
| Ranked surprise/kill tests, new filing facts, carrier comparisons and bounded search failures | [Catalyst scorecard](reports/catalyst_scorecard_2026-10.md) |
| Follow-up recovery, source fingerprints and reproducible local checks | [Recovery checkpoint](reports/recovery_checkpoint_2026-10.md), [evidence directory](reports/catalyst_evidence_2026-10/README.md) |
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

The original 30 September publication snapshot included the nonignored artifacts then present. Subsequent working updates are indexed above; this note does not assert they have been pushed. Raw licensed/private source material, large collection caches/databases and environment files remain local under the existing repository rules; extracted analytical datasets and source provenance are the publication boundary. A GitHub clone is therefore an analytical archive, not a byte-for-byte backup of the research computer or a verbatim chat transcript.

**Change log — 2026-09-30:** recovered named quarterly fee-unit/RPU expectations, checked new filings and completed the approved bounded catalyst pass; no evidence-backed surprise admitted, no model integration triggered.

**Subsequent user-requested scenario change — 2026-09-30:** separate engine configurations now reverse-solve 2%/3%/5% FY27 service misses versus JPM. With the assumed price driver fading to zero by Q3, the 3% miss requires insurance units 3.23% below reference in Q2 and 6.46% below in Q3/Q4; services $3,939.17m. This is a reverse stress, not a supported forecast or verified catalyst. Reference/history/workbook remain unchanged; the earlier investment conclusion stands pending evidence.
