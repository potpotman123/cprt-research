# E10 — The two documents: ACV's SC 14D-9 (read) and Copart's FY26 10-K (not yet filed)

*2026-09-26. Requests: 6 to sec.gov / data.sec.gov (descriptive UA, logged). Files: `raw/sec/submissions_CIK0000900075.json`
(refreshed), `raw/sec/company_tickers.json`, `raw/sec/submissions_CIK0001637873.json`, `raw/sec/acv/sc14d9_2026-09-17.htm` (+ `.txt`),
`raw/sec/acv/sctot_index.json`. Data: `data/csv/acv_14d9_projections.csv`. Usage: ~60k tokens.*

## 1. Copart's FY26 10-K — NOT FILED as of 2026-09-26 17:00Z

Copart's last three 10-Ks were filed Sept 26 (2025), Sept 30 (2024) and Sept 28 (2023). The refreshed submissions index shows
nothing after the Sept 17 tender-offer documents. **Re-check Monday Sept 28 and daily after** (one request:
`data.sec.gov/submissions/CIK0000900075.json`). The base-year tie-out in `MODEL_BLUEPRINT.md` §7 stays on the 8-K until then.

## 2. ACV Auctions' SC 14D-9 (filed 2026-09-17) — the standalone projections, VERIFIED

The figures that circulated second-hand (Addendum 19: 2027 adj. EBITDA $123M, EBIT $20M, uFCF −$97M) are exactly what the
filing says. Full table, management's standalone plan as given to J.P. Morgan and approved by ACV's board ($M, FY Dec):

| | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|---|---|---|---|---|
| Revenue | 857 | 964 | 1,116 | 1,322 | 1,525 |
| Adj. EBITDA (unburdened by SBC) | 78 | 123 | 187 | 283 | 382 |
| Adj. EBIT (burdened by SBC) | (15) | 20 | 73 | 152 | 244 |
| NOPAT | na | 15 | 55 | 114 | 183 |
| Unlevered FCF | na | (97) | (69) | (8) | 37 |

**Stated assumptions (verbatim in substance):** low-double-digit dealer-to-dealer unit growth through the period; commercial
units accelerating to 235,000 by 2030 on a "land expansion strategy"; SaaS/data revenue to $135M by 2030; revenue margin
+4pp 2025A→2030E; opex from mid-40% of revenue (2025A) to low-30% (2030). Projections exclude synergies and deal costs.
Management also prepared projections through 2036 for the DCF; only 2026–2030 are disclosed.

**Arithmetic on the price ($1.9B equity value, $10.50/share, per Copart's 8-K):** 24× 2026E adj. EBITDA, 15.4× 2027E,
10.2× 2028E, 6.7× 2029E; unlevered FCF is negative through 2029 on management's own plan (cumulative −$174M 2027–29), so the
asset does not fund itself until 2030. Copart's foregone interest on $1.9B of cash at ~4% is ~$75M/yr pre-tax against ACV's
2027E EBIT of $20M: **on the standalone plan the deal is EPS-dilutive in FY27 and FY28**; Copart's stated "accretion from
FY28" therefore requires synergies or a cost-of-capital argument, neither quantified in the 14D-9 (it mentions "cost and
revenue synergies" without numbers).

**J.P. Morgan's fairness analysis:** DCF on 2027–2036 unlevered FCF, terminal growth 2.5–3.5%, WACC 10.0–11.0% → **$9.50–13.00
per share**; public trading multiples (comps: Copart, RB Global, OPENLANE, Uber, Airbnb, Wayfair, Chewy, Etsy) → $7.50–10.75.
Unaffected price $7.03 (Sept 8, 2026). The offer sits inside the DCF range, near its low-middle.

**The process (Background section) — a genuine auction, not a bilateral deal:**
- "Party A", a strategic, has pursued ACV since 2022: all-stock at 0.31–0.34× (Nov 2025, rejected), $8.75 cash+stock (Mar 2026,
  rejected), **$10.50 half cash / half stock (Aug 6, 2026)**, then a *lower* $10.00 on Sept 8 with diligence incomplete.
- "Party B" bid **$11.00–12.00 all cash (Aug 6)** — EV $1.88–2.07B, 30.4–33.4× TTM EBITDA — and withdrew Aug 15 after "a
  recent material decline" in its own stock. Party C declined; Parties D and E never advanced.
- Copart: first proposal July 2 (a 10–16% premium, ≈ $8.00–8.50), final **$10.50 all cash on Sept 6**, diligence complete.
  ACV's board noted media reports that Copart "might be considering an alternative acquisition" and could walk.
- Reverse termination fee payable by Copart **$115.3M (~6% of equity value)** on antitrust failure; a negotiated
  "regulatory efforts covenant". ACV's board lists HSR clearance as a risk.

No mention of yards, staging, Purple Wave or physical integration anywhere in the filing (searched: 0 hits). The
staging-at-Copart-yards angle in thesis #2 remains UNVERIFIED and has no document behind it.

## 3. What this changes in the repository's ACV position

- `HANDOFF.md` §3J called ACV "genuinely ambiguous" pending this document. It is now **quantifiable and mildly negative on
  the standalone numbers**: Copart paid a price a rival strategic matched and a financial-style bidder exceeded, for a plan
  that is FCF-negative for three years and needs synergies to be accretive. The price is defensible as an auction outcome;
  the *asset* is a bet on the 2029–2030 ramp (EBITDA 78 → 382) and on Copart's ability to run whole-car dealer volume, which
  the repo's competitive section already doubts.
- For the two pages: one risk paragraph with three numbers (15.4× 2027E EBITDA, −$174M cumulative uFCF 2027–29, $115M
  reverse break fee) and one sentence on the auction (a rival bid $11–12 and walked). Do not promote it to a thesis.
- For the model: an `Acquisitions` input block — $1.9B cash out (FY27), ACV revenue/EBITDA from the table above as a
  consolidated line from close, foregone interest at the cash yield, and a synergy input defaulting to zero (ASSUMED until
  Copart quantifies it). Sensitivity: accretion year vs synergy $.

## 4. Copart's own tender-offer documents

`raw/sec/acv/sctot_index.json` lists the Offer to Purchase (Ex. (a)(1)(i), 442 KB) and the merger agreement (Ex. (d)(3)).
The Offer to Purchase (`raw/sec/acv/offer_to_purchase_2026-09-17.htm`, 442 KB) was read for its "Purpose of the Offer;
Plans for ACV" section. **It contains no synergy, integration, accretion, yard or facility language at all** (searched: 0
hits each) — only the statutory purpose ("to acquire all of the outstanding Shares") and the funding sentence: about $1.9B,
paid from cash on hand, no financing condition, no alternative financing arrangements. Copart has therefore put nothing on
the record about what it will do with ACV; the only quantified view of the asset is ACV's own standalone plan above.
