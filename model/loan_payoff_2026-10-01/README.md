# Loan payoff coverage sensitivity

Read `docs/affordability_2026-10-01/README.md` for evidence, definitions and the pitch decision. Run `python3 model/loan_payoff_2026-10-01/run.py` from the repository root.

This package adds a reproducible calendar and isolated hypothetical scenarios to the existing quarterly engine. `scenario_configs.json` can be inspected or passed to that engine. The central reference, historical calibration and presentation workbook are unchanged. No current coverage-drop coefficient or maturity distribution is identified, and no forecast input is admitted.

The three coverage inputs in `run.py` are prospective insurance-total-loss-weighted cohort exposure, excess coverage cancellation over the existing baseline, and net unit recapture through other routes. Their product produces a uniform claims-exposure multiplier. Recaptured units implicitly receive reference-equivalent economics; the package does not estimate separate non-insurance seller fees. Age/body heterogeneity, renewal timing, surviving loan vintage sizes and route economics would be necessary for calibration.

`maturity_calendar.csv` gives month arithmetic, not counts. `scenarios.csv` assumes the same shock in all four FY27 quarters, not a payoff ramp. `hurdles.csv` compares magnitude with the prior reverse stress but does not reproduce its timing or price case. `checks.json` separates arithmetic checks from forecast admission. The nonfiling-only case must leave units and revenue unchanged while raising reported total-loss frequency.
