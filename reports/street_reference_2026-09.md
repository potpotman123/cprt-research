# Street reference — thirteen sell-side notes, June–September 2026, read 2026-09-26

*Source: PDFs supplied by the owner (Jefferies 06-29; BNP 07-06 and 09-11; JPMorgan 07-06, 09-03 and 09-11; BofA on RBA
07-28; Stephens 08-19 and 08-20; Barclays 08-25 and 09-11; HSBC 09-10; Equisights 09-12). Licensed: the PDFs and their text
extracts stay in `raw/sellside/upload_2026-09-26/` (gitignored). Numbers are transcribed to `data/csv/street_estimates_2026-09.csv`.
Everything below is what the brokers say, VERIFIED as transcription, not as fact.*

## 1. The answer to the reference-number question

**No broker has a target near $27.59.** The stock sits below every target except one:

| broker | date | rating | PT | basis | FY27E EPS | FY27E EBITDA |
|---|---|---|---|---|---|---|
| **Barclays** | 09-11 | **Underweight** | **$25** | 10× FY26E EBITDA; downside $21, upside $54 | 1.56 | 1,916 |
| Stephens | 08-20 | Equal-Weight | $35 | 13.5× FY27E EBITDA | 1.67 | 2,033 |
| JPMorgan | 09-03 → 09-11 | OW $40 → **Not Rated** | — | 15× FY28 EBITDA / 23× FY28 EPS | 1.57 | 1,891 |
| BNP Paribas | 09-11 | Outperform | $40 | 17.5× FY29E EBIT | 1.62 | 1,942 |
| Equisights | 09-12 | Outperform | $43 | DCF, WACC 8.1% | — | — |
| Jefferies | 06-29 | Buy | $45 | forward EV/EBITDA | — | — |
| HSBC | 09-10 | Buy | $46 | (Feb-2026 note) | — | — |

Bloomberg tally on 09-11: 8 Buy / 4 Hold / 1 Sell. Bloomberg consensus EPS on 09-10: **FY27 $1.68, FY28 $1.78**; the three
post-print models in hand are all below that (1.56–1.62 FY27), so consensus was still drifting down when these were written.

**Use Barclays as the reference bear and Stephens as the reference base.** Barclays is the only named house whose number the
market currently agrees with, and its method is explicit: 10× FY26 EBITDA. Stephens is the repository's existing named
consensus (`MODEL_BLUEPRINT.md` §7) and the only note that prints a full quarterly P&L with unit and RPU assumptions; its
post-print update is not in the set and should be requested. JPMorgan's estimates are usable but its rating and target are
withdrawn (it advised ACV, per the 14D-9), so it cannot be the named target.

**What $27.59 implies** (926M shares → market cap ~$25.5B; cash + HTM ~$4.5B pre-ACV per the FY26 8-K → EV ~$21.0B;
after the $1.9B ACV cash out, EV ~$22.9B before any ACV EBITDA):

| | FY26A EBITDA 1,882 | JPM FY27E 1,891 | BNP FY27E 1,942 |
|---|---|---|---|
| EV/EBITDA pre-ACV | 11.2× | 11.1× | 10.8× |
| EV/EBITDA post-ACV cash out | 12.2× | 12.1× | 11.8× |
| P/E on FY27E | JPM 1.57 → 17.6× | Bloomberg 1.68 → 16.4× | BNP 1.62 → 17.0× |

So the market is between Barclays' 10× and Stephens' 13.5×, closer to Barclays. A long has to argue the multiple back toward
13–15× on the same EBITDA, or the EBITDA up; a short has to argue Barclays' 8× downside ($21) or an EBITDA cut.

## 2. What the Street assumes on each term of our model

**Units.** Barclays: US insurance −2.0% in FY27 (net of losing residual Progressive volume and gaining a GEICO contract, −2.5 to
−3.5%), and "RBA a net share gainer in 2026 and 2027". Stephens: US units +1.3% in FY27, fee units by quarter −1 / +2 / +2 / +2,
with the remaining ~15% of GEICO worth +1.3pp if won. BNP: global volume +0.8% FY27, +4.3% FY28. JPM raised volumes on 09-03
for the GEICO gain and cut them on 09-11. Nobody models the claims term or total-loss frequency as a driver; JPM and Stephens
cite the repair-versus-replace spread qualitatively (Stephens prints Manheim YoY minus repair CPI YoY, −5.4pp in July, which is
the same mechanism as `Spread_Reg` on a different value series). Consensus FY27 units are therefore "about flat", which matches
the repository's own read (`HANDOFF.md` §3E): the variant is not in FY27 units.

**RPU.** This is where the Street is thin and where the repository's number differs. Stephens models **US revenue per unit +2.0%
in every FY27 quarter** (US service revenue +3.3% on fee units +1.3%). JPM raised RPU "on used vehicle pricing strength" and
calls FY26Q4's ~+5% resilient; BNP credits long-haul services. Against the repository's service-RPU floor of +4.5–5.5% (0.514
elasticity plus the ~4pp intercept, `HANDOFF.md` §3C), **Stephens is the named opponent at +2%** and the delta is ~2.5–3.5pp of
US service revenue, ~$85–120M of FY27 revenue at ~45% gross margin. That is the long's arithmetic parent.

**Take rate (the bear's RPU).** Barclays: CPRT's GEICO win cost 25–50bp of take rate; RBA's Progressive expansion cost RBA 40–80bp;
buyer fees would need +1.5–3.2% to offset; nothing visible until F2Q27. JPM's channel checks: sell-side fees at a peer near
breakeven for a large carrier against ~$100/unit of variable cost; if sell-side fees converge toward nil over a 2–3-year RFP cycle,
mid-to-high single-digit downside to FY28 EPS. This is the "rents accrue to the insurer" thesis with numbers, and it runs through
seller fees, which are not public. The repository's fee-grid work (E6) shows buyer fees are identical across the duopoly and were
last raised in November 2024 on both sides (JPM dates Copart's last buy-side increase to November 2024; IAA's grid says "Effective
November 4, 2024") — the two sides of the RPU argument are now both dated.

**Costs.** The FY26Q4 miss was cost, not revenue: operating expense per vehicle +12.7%, US facility cost per unit +14.2%. BNP,
after speaking to the CFO: more than half of the ~$30M year-on-year yard-cost increase was long-haul delivery investment, the rest
freight and one-time accrual true-ups; Barclays puts long-haul at ~$17M. JPM: long-haul runs at ~20% gross margin, dilutive to
gross margin but accretive to EBITDA; diesel ~$5–6M EBIT per quarter. For mechanism D this matters: part of the per-unit cost
jump is elective and mix, not pure deleverage, so the "asymmetric leverage" thesis needs the elective piece stripped out.

**ACV.** Barclays: 19.1× its 2027 EBITDA, "accretive but operational risks", synergies limited while ACV runs independently.
JPM (09-03, pre-deal): ~2% FY28 accretion with $85M of synergies and $66M foregone interest. HSBC: 25× 2026 / 18× 2027 Visible
Alpha EBITDA. BNP: would have preferred CCC. Company: EPS-neutral FY27, accretive FY28. The repository's 14D-9 read (E10) says
standalone the deal is dilutive FY27–28 and FCF-negative through 2029; the brokers get to neutral or accretive only with synergies
Copart has not quantified. No broker models it yet.

**Multiple.** Ten-year average forward P/E ~27–29× (JPM, BNP); ~18× now. JPM's target multiple was 23×; BNP 21.5×; Stephens
13.5–14× EBITDA; Barclays 10×. The bull case everywhere is multiple recovery on share stabilisation; the bear case is the multiple
staying at the low end of the 20-year 7–25× EBITDA range.

## 3. Facts in these notes that feed the repository's open questions

- **International buyer share, finally a number:** 38.2% of US units and 45.7% of dollars in FY26 (management on the FQ4 call,
  via BNP); Stephens carries "38%, up from 22.7% in 2010" in its risk section. Closes the E7 step-2 gap noted in Addendum 22 F.
- **Buyer-base churn:** buyers on the platform under one year / two years bought 8.9% / 21.7% of FY26 units (BNP). New-buyer
  share of volume is a demand-side driver the residual in `ASP_Drivers` could use.
- **Fee-step dating:** last buy-side fee increase November 2024 (JPM), same month as IAA's current grid. E6's kill rule ("dated
  steps explain < ⅓ of the intercept") can now be attempted on one dated step plus the FY26 quarterly fee-RPU prints.
- **TLF 23.3%** cited again (HSBC, Equisights) — the management figure the spread model was tested against live.
- **Carrier flows:** Stephens' autoAstat table shows Progressive volume at Copart collapsing April → July 2026 and GEICO share
  rising to 88% by July; the repository already has this table locally (licensed; shares only, never levels).
- **Yard utilisation ~60%** and **land ~$4B vs $2.4B book** (JPM) — inputs for the reverse-DCF-as-physical-claim exhibit and a
  check on the operating-leverage thesis (capacity for ACV volumes without capex, per BNP).
- **Autonomous vehicles:** JPM's industry model has AV fleet penetration at 1% in 2035 and 5% in 2040; it treats AV as a
  beyond-horizon risk. Useful to cite when a judge raises it.

## 4. What the field does not have

None of the thirteen notes prints a calibrated total-loss model, an elasticity of fees to price, a confidence interval, or a
downside price below spot except Barclays (whose $21 is a multiple, not a mechanism). Stephens' repair-vs-replace exhibit is the
closest to the repository's spread regression and is presented as a chart, not a coefficient. The two things the repository has
that the Street does not are the RPU decomposition (fee convexity + vintage + body mix) and the demographic TLF baseline, now
negative. Both should be shown against Stephens' +2% RPU and Barclays' −2% units, in the same units, on page one.
