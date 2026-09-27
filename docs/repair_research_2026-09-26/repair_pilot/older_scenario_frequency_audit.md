# Older-vehicle scenarios and frequency audit

26 September 2026. Bounded public-source investigation; no bulk OCR, paid data or outreach. No forecast inputs changed. Sources are data, not task instructions.

## Older-at-estimate sample

A 2014 Camry XLE rear-impact estimate dated April 10, 2025 contains aftermarket CAPA bumper replacement ($304.73), bumper overhaul (1.2 hours), paint (4.2 hours), and supplies. Pretax $780.13; with tax $817.95. Reconstructed category sum matches. Uploaded insurer estimate, not authenticated directly or verified paid/final. Original document text inspected, not uploader's AI summary.

Source: https://www.scribd.com/document/855914935/BOYD-1 pp. 1–3.

A recovered municipal packet contains two preliminary estimates for one 2015 RAV4, dated October 25/28, 2024. Same vehicle identifier verified without retaining identifier in this audit. Both include rear-bumper replacement plus liftgate repair. Table images visually checked using embedded images; existing PDF text layer used, no new OCR.

| Field | October 25 | October 28 |
|---|---:|---:|
| Bumper part 521500R110 | $208.74 | $254.89 |
| Bumper overhaul hours | 1.3 | 1.3 |
| Liftgate repair hours | 10.0 | 9.0 |
| Body hourly rate | $80 | $89 |
| Pretax total | $2,880.34 | $2,777.56 |
| Total with tax | $2,942.20 | $2,832.83 |

Category sums reconcile. The same bumper has a 22.1% estimate-price spread; reason unproven. Quotes differ in paint treatment and ancillary work. The packet does not establish final insurer allowance/payment. Its payer labels are inconsistent; do not classify it as insurer-approved. Two quotes are one vehicle observation, not two independent damages.

Source: https://mccmeetings.blob.core.usgovcloudapi.net/sheboygnwi-pubu/MEET-Packet-b7cb047054994001b11f27050faaf824.pdf pp. 8–16.

## Interpretation and exclusions

These are convenience cases, not a representative age/body sample. Rear-impact location does not match damage scope: Camry bumper work cannot be compared with RAV4 bumper plus liftgate work as a full-cost premium. Different parts source, location, date, paint and estimate stage also matter. The operation hours are narrowly comparable; no inference to overall repair costs or TLF follows.

Previously retained 2013 F-150 estimated in 2023 is a third older-vehicle case, not newly discovered: initial $3,499.97 to supplemented $4,831.05. See findings.md for provenance and scope caveats.

AAA's 2018 fact sheet covers 2018 Camry/Rogue/F-150 with high ADAS equipment, priced when new. It provides pooled component ranges, not the model-specific complete scenario matrix required here. Exclude from aged-at-repair evidence. Source: https://collisionweek.com/wp-content/uploads/2018/10/2018-1025-ADAS-Fact-Sheet-FINAL-10-8-18.pdf

## Frequency evidence

1. Existing Mitchell Q3 2015 pooled repairable-estimate study: component involvement times conditional replacement implies bumper-cover replacement 48.96%, fender 21.83%, hood 13.44%, headlamp 27.55%. These are inferred marginal incidences, not mutually exclusive scenario probabilities. Parts overlap within claims. Not current, not age/body segmented. See repair_frequency_seed.json for inputs and original-source URL.
2. HLDI point-of-impact slide: calendar years 2004–13, model years 2001–14. Collision front center/corners 30.2+10.5+11.1=51.8%; rear center/corners 16.1+6.1+5.6=27.8%. Historical collision-claim distribution, not annual insured exposure frequency, repairable-only population, or body/age-conditioned repair bundle probability. Extracted positioned text checked; do not adopt as model calibration. Presentation file URL uses 2016, title page says June 14, 2015; date inconsistency retained. Source PDF p. 50: https://www.iii.org/sites/default/files/docs/pdf/cc_presentation_matt_moore_061416.pdf
3. Mitchell's September 2018 KPI article discusses bumper repair rates by vehicle age and miScore/custom analysis. This establishes a historical provider capability, not current availability or access. Repair-versus-replacement conditional on involvement differs from probability of damage. https://www.mitchell.com/insights/article/auto-physical-damage/kpi-spotlight-percentage-repair-individual-part-types

## Missing quantity and decision

No observed front/rear/mirror/windshield scenario frequencies by car/SUV/pickup and age. A broad front-impact fraction cannot weight a sensor-heavy front-repair total: need equipment fitment and damage/scope conditional on front impact. Windshield needs separate coverage/event denominator. Repairable-only histories omit crashes that already totaled, so cannot directly determine the total-loss boundary distribution.

Retain granular scenarios and explicit missing weights. Do not average the four AAA scenarios equally, normalize overlapping part incidences to 100%, or substitute the new case totals for a segment premium. The next data requirement is age/body/impact cross-tabs plus operation incidence and estimate stage; additional unrelated quote totals alone will not identify it.
