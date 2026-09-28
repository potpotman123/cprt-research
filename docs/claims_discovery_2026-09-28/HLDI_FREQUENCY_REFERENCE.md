# External reference for the older-vehicle claim-age curve

28 September 2026. Three discovery searches, one seven-page public PDF retrieved, one relevant page rendered and inspected, three approximate chart readings, and six arithmetic checks. No OCR, mass digitization, new parameter fit or production edits.

## Source and limited observations

[HLDI Bulletin 39(7), April 2022](https://platform.vox.com/wp-content/uploads/sites/2/chorus/uploads/chorus_asset/file/24341429/39_07.pdf), Figure 5, printed p.4: CY2020 collision claims per 100 insured vehicle-years. Approximate readings of the all-vehicle curve: age13 3.6; age20 2.15; age25 1.5. These are visually read, not printed numeric labels. Use ±0.15 as a conservative reading allowance, not a statistical confidence interval. Pickup frequency is below passenger-car frequency in the chart; categories do not map exactly to our model. Demographic/geographic standardization is absent, and 2020 is pandemic-affected. The report is primary-authored but retrieved from a third-party mirror.

The source PDF is retained locally at raw/hldi/hldi_39_07_2022.pdf; input and source hashes are saved with the calculation. Only analytical notes and small calculations are staged for Git.

## End-to-end pipeline and alternatives

1. Inspect source methods and denominator first. A large sample does not solve a mismatched denominator. Insured vehicle-years differ from our surviving vehicle counts.
2. Render the relevant page using the PDF workflow. Text extraction identifies the figure but cannot supply unlabelled line values. A visual check avoids confusing collision's denominator of100 with the neighboring fire chart's10,000.
3. Read only three ages. They span the older bucket and permit a first shape test. Bulk pixel digitization or OCR would add false precision; source tabular data would be better but were not supplied with the retrieved chart.
4. Normalize at age13. This isolates within-bucket shape and avoids the model's half-year exposure assumption at age0. Read the model's actual relative_claim_weight inputs rather than reconstructing them from rounded documentation.
5. Compare slopes and propagate reading allowances. Treat differences as a compatibility diagnostic, not estimated coverage. Because the underlying populations differ, no optimization, confidence interval or empirical elasticity is justified.
6. Search for repeated exhibits. Three queries below returned newer make/model studies and other fire/ADAS research, but no comparable repeated exact-age panel was verified. Stop before turning a bounded check into a literature census.
7. Decide whether to modify the model. The observed shape is broadly compatible with declining older-vehicle claim propensity. Its mismatch does not identify a replacement value. Keep production fixed.

## Model comparison

All relative quantities below normalize age13 to100. The external column describes insured vehicles; the model describes the existing broader claim propensity per surviving vehicle. Their levels are not directly comparable.

| Age | Approximate external relative frequency | Model relative propensity | Model/external ratio, conditional diagnostic |
|---|---:|---:|---:|
| 13 | 100 | 100 | 1.00 |
| 20 | 59.7 | 53.2 | 0.89 |
| 25 | 41.7 | 33.8 | 0.81 |

Holding all other population and time differences aside, the diagnostic residual ranges from0.80–1.00 at age20 and0.71–0.94 at age25 under the reading allowances. These are not probability estimates and not statistical intervals.

## Why the comparison cannot identify coverage

For one compatible collision population and period, claims per surviving vehicle equal collision coverage exposure per surviving vehicle multiplied by collision claims per insured vehicle-year. The latter already reflects driving, incident risk, reporting and selection among covered vehicles.

Under that identity, the quotient of two matched age-relative curves would recover relative coverage exposure. Our comparison is not matched: it combines a fitted broader claims curve anchored to later CCC statistics with a historical collision-only panel. Its residual may therefore include coverage, coverage mix, cohort composition, pandemic driving, population selection, or model error.

Do not multiply the existing claim-age curve by the external frequency curve. That would count the age-related decline twice. Do not label the0.81 diagnostic as81% coverage or an18.8% observed loss of coverage over time. This is a comparison across vehicle ages, not a change from2024 to2025.

## Consequence for the current research step

This source supports treating older-age claim frequency as an explicit component worth checking; it does not validate the fitted coefficient. It does not resolve why 13+ TLF increased in2025. We now have a historical external benchmark and a clear denominator contract, but still need either repeated matched age/coverage counts or direct coverage exposure by age.

A better next acquisition is a small existing published cross-tab or provider table with matching years, not hundreds of auction records or more precise extraction of this old chart. Potential analysis branches are: check historical model shape against this reference; locate repeated insured-exposure tables; or preserve the reference as a validation constraint and move to another unresolved engine component. None requires pretending that the missing older-cohort panel exists.

## Search provenance

- site.iihs.org "collision claim frequencies" "vehicle age" "2023"
- site.iihs.org "noncrash fire" "2024" report
- site.iihs.org "39.7" fire

Also inspected IIHS's public auto-insurance overview to distinguish newer make/model comparisons from age curves. New-model cross-sections were not adopted as older-fleet evidence.

Reproduction: hldi_frequency_check.py; results: hldi_frequency_check.json. The saved JSON includes source locator, approximate-reading status, ranges, model-input hash and six checks. Assumptions and forecasts unchanged.
