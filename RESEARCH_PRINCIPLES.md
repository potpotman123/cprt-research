# Standing research principles

User instruction, recorded 28 September 2026. Applies to future Copart research, model work and handoffs. These are working requirements, not a one-time search checklist.

## 1. Explain and challenge the entire pipeline

Before a new analysis, state the precise question, competing explanations, measurable target, population, period and how the answer would affect the model or pitch. Walk through every necessary step, including where data come from, how they are accessed, what is extracted, how populations are matched, which transformations and assumptions are required, how the result is checked, and what is delivered.

For each step explain:

- Why it is necessary and how it contributes to the final inference.
- Why this method is preferable to available alternatives on accuracy, identification, coverage, latency and computational/token cost.
- What cheaper or more precise alternative exists, and why it is or is not sufficient.
- What could go wrong, what would falsify the interpretation, and when to stop.

Then review the sequence as a whole: could a different observation, natural comparison, identity, bound or direct disclosure answer the question with fewer steps or fewer assumptions? Do not merely optimize an unnecessarily complex approach. Do not claim a method is universally best without evidence. Distinguish the best currently available method from an ideal inaccessible dataset.

Keep the explanation proportional to the task. Cheap continuation does not need repeated approval. Before expensive OCR, large scrapes, extensive fitting or paid acquisition, give the user the complete proposed workflow, expected cost/range and uncertainty, alternatives, expected information gain, stopping rule and deliverable; wait for approval. Do not invent precise usage estimates.

## 2. Broaden discovery before narrowing execution

Search beyond the named company, ticker and incumbent datasets. Ask who directly observes each decision and what records their ordinary operations generate. Search their vocabulary, not only investment-research terminology.

For example, a truck/car repair premium may be evidenced by repair shops, collision chains, mechanics, parts distributors, OEM procedures, estimating vendors, insurer payment surveys or repair-business filings—not only insurer aggregate claims. Claim disappearance may be observed by agents, renewals, lenders, repair authorization records, cash settlements, regulatory exposure tables or consumers—not only a total-loss chart.

At discovery stage explicitly consider several source families and alternative explanations. Include at least one route outside the current modeling framework. Creativity means generating testable mechanisms and unconventional evidence routes, not inventing facts or searching only for support for a desired trade.

Rank candidates by directness of measurement, compatible population/period, denominator clarity, independence, access and cost. Read selectively. A broad search should end in a narrow execution shortlist, not unlimited browsing.

## 3. Evidence discipline and continuity

Inventory prior work first; do not rediscover existing results or rerun analyses without a reason. Preserve failed searches and retractions. Distinguish observed, derived, proxy, assumed and unknown inputs. Distinguish sources that independently measure an outcome from publications repeating the same underlying dataset.

Record exact queries, URLs/files, access/publication dates where known, relevant pages/sections, units, population, definitions, limitations and derivation. Explain how a source changes confidence, not just that it exists. Explicitly label synthetic examples, calibrated parameters and nonidentified ranges. Null results should narrow the question rather than trigger increasingly flexible fitting.

Separate validation of arithmetic from validation of the economic mechanism. Do not adopt a forecast coefficient merely because it makes a historical result fit. Preserve uncertainty and evidence that challenges the preferred long/short direction.

Current division of work: analytical calculations and provenance here; spreadsheet presentation through Fable unless the user requests otherwise. Do not spend effort rebuilding presentation artifacts to perform calculations that are cheaper in small reproducible scripts.
