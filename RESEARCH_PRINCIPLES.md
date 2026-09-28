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

## 4. Bounded end-to-end execution and token efficiency

Default assignment template, adopted by the user on 28 September 2026:

> Investigate this missing input end-to-end. Check existing work first, run one bounded discovery pass across several plausible source types, assess the strongest evidence and competing explanations, and update the provenance. Stop the research expansion if further progress requires expensive collection or weak proxies. Report what changed, what remains uncertain, and whether the evidence can enter the model.

This template complements sections 1–3; efficiency must not become narrow or confirmation-seeking research. Use abductive reasoning: generate plausible explanations, ask which evidence differentiates them, and update confidence without forcing a long or short conclusion.

- Batch related retrieval, assessment, calculation and documentation into one coherent assignment. Do not require the user to authorize each routine step. Avoid bundling unrelated research directions merely to make a larger prompt.
- Begin with a bounded pass, typically 4–6 well-chosen queries spanning different source families, then selectively open the strongest evidence. These are defaults, not rigid quotas. Additional work should follow a concrete lead or necessary verification, not a repeating search loop with low information gain.
- Inventory local work first. Read relevant sections, filter large tool outputs, and avoid pulling whole documents or scripts into context unnecessarily. Retain exact provenance and sufficient calculation detail to reproduce material findings.
- Distinguish cheap machine computation from low usage: searches, returned text, repeated reasoning, generated code and lengthy writeups all consume model resources. Do not describe a task as low-usage solely because its numerical calculation is small.
- Use compact incremental provenance entries for small updates rather than duplicative multi-page reports. Keep necessary definitions, denominators, population/period mismatches, failure modes and competing interpretations explicit.
- Higher reasoning is most useful for architecture, conflicting evidence, identifying selection effects or double counting, and challenging an integrated thesis. Routine collection and extraction do not automatically justify Ultra. Do not silently change settings or launch agents.
- When further progress requires expensive work, explain the proposed end-to-end steps, alternatives, uncertain cost, expected information gain and stopping rule, then obtain approval. Do not invent precision about token costs. If only weak proxies remain, identify the gap rather than promote them into facts; a user-authorized assumption or sensitivity must remain labeled.

New-chat continuity: read AGENTS.md and this file, inspect the relevant current handoff and latest evidence/results, and identify the unresolved question before doing new work. Durable files preserve the workflow and research state; they are not proof that a new chat remembers the full conversation. The general workflow is also installed locally in `/Users/kwu/.codex/AGENTS.md`; that local file does not travel with a Git clone.
