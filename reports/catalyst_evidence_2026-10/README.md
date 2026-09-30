# Evidence and checks for the October pitch preparation

As of 30 September 2026. The [decision](../pitch_decision_2026-10.md), [expectations sheet](../expectations_sheet_2026-10.md) and [scorecard](../catalyst_scorecard_2026-10.md) are the human-readable outputs.

- `checks.json`: deterministic arithmetic and selected source checks. Conditional shocks retain ASSUMED status.
- `source_manifest.json`: file paths, sizes and SHA-256 fingerprints for local sources. No licensed report body is included.
- `search_results.json`: six exact queries, HTTP outcomes, source-file locations where saved and result URLs. Search snippets are not admitted evidence.
- `page_access.json`: primary-page successes, failures and one robots-gated non-request. Five content requests; no retry around a challenge.

Run `python3 scripts/catalyst_checks_2026_10.py` from the repository to reproduce. It uses the standard library and reads existing local files only. Raw filings, licensed originals and successful fetched pages are required for full source rechecking and are outside the portable archive. Saved derived checks alone are portable; their existence is not a fresh verification of the underlying sources.

The source-text comparison confirms the new Copart seller-arrangement sentence is absent from FY25, the competition-section body is unchanged, and the stated facility and insurer-mix values are present. It is not a complete redline of the two 10-Ks; no claim that nothing else changed is made. The RBA filing checks confirm the parent-level acreage and lot populations, not an IAA-only land census.

Failure record: discovery queries 4–6 returned HTTP 202/no results; RBA's two IR pages and LKQ's calendar returned 403; CCC IR robots returned −1 so no content was requested. The source logger retains status, body hash and error metadata. The only extraction setup failures were unavailable `bs4` in the two inspected Python runtimes; standard-library HTML parsing succeeded without installation. PDF native text and rendering were available; no OCR fallback was needed. The pre-existing `scripts/fetch_logged.py` and `reports/phase0_state_2026-09-30.md` were left unchanged.

No engine/workbook changed and no model tests were rerun. New checks validate source labels, populations and arithmetic; they do not validate the predicted magnitude, sign, timing or probability of either thesis.
