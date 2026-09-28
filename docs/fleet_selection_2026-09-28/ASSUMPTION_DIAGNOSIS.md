# Competing-assumption calculation — 2026-09-28

User correctly requested diagnosis rather than another description of the discrepancy. Existing-input calculation, seconds of local runtime, no external acquisition. See `assumption_diagnosis.py` and results. Shared fit now accepts optional value-slope and recovery-center arguments; defaults preserve previous results.

## What was tested

For each structural assumption, refit six repair medians to the six TLF targets, find a shared dispersion and dollar scale that reproduce both repairable age-group means, then test selected total-loss ACV against $13,610. Use the conditional CCC age weights and existing modeled body weights. Coverage mismatch remains: value target non-comprehensive, other targets all-loss. This is a compatibility exercise, not causal identification.

1. **Value level / dispersion alone, fixed age curve:** earlier joint fit implies selected ACV $21,316. Thus these degrees of freedom close repair means and TLF but not the extra value target.
2. **Recovery center:** hold age-value log slope at 0.10 and the recovery decline across damage ranks at 20 percentage points. Test recovery centers 0.10, 0.20, 0.30, 0.40, 0.50. Centers are not recovery among selected total losses; recovery equals center + 0.10 - 0.20 × damage rank. Resulting selected ACVs after refitting: $16,426, $18,556, $21,316, $25,032, $30,296. Even the tested 0–20% recovery curve leaves value 20.7% above the benchmark. This does not rule out every recovery function or separate net-cost treatment.
3. **Age-value slope:** keeping recovery center 0.30, changing the log slope from 0.10 to 0.08 produces selected ACV $11,934 after refitting. A root between those slopes matches the provisional value target as well as both repair means and TLF.

## Feasible slope solution, not adopted

- Log depreciation slope: 0.0847934, versus 0.10. Corresponding annual proportional depreciation is about 8.13% rather than 9.52% (1-exp(-slope)).
- Age-ten car ACV: $11,257, versus $10,000. This common scale is 1.12569, not the prior joint fit's 1.69382.
- Repair log dispersion: 1.06875, versus 1.57021.
- Selected ACV: $13,610.002; both group means and age TLF targets also fitted.
- A uniform 5% repair-cost increase gives +6.09% units under this case, versus approximately +4.02% under original dispersion with these weights. Conditional diagnostic only, not a forecast.

Interpretation: a less steep value decline across age, together with a narrower repair distribution and modest level change, can resolve the three-target conflict. Young values no longer have to be inflated enormously to bring older repair bills into line. This identifies the fixed age-value slope as an important restriction to test, not the empirically proven source of error. The solution changes several fitted quantities; do not attribute all effects to slope alone.

There are now nine adjustable quantities for nine targets: six age medians, dispersion, value scale and slope. An exact fit is not validation. A different recovery shape, within-cohort value dispersion or coverage alignment might yield different parameters. The wide dispersion grid and slope grid are mathematical diagnostics, not confidence intervals. Unbracketed cases only mean no equal-scale root in tested sigma range [0.35,3], not impossibility.

## Decision

Do not adopt the $17k age-ten value from the old joint fit, and do not call the new +6.09% response measured. Prioritize the existing age-specific valuation charts as an independent test of the flatter curve. This is a concrete candidate mechanism to falsify, rather than further blind rescaling. No forecast workbook or production input changed.
