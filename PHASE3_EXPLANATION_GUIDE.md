# Phase 3 Explanation Guide (Business-Friendly)

## Purpose of this document
This guide explains the "why" behind Phase 3 decisions so the project can be presented clearly to non-technical stakeholders and hiring managers.

It answers:
- why these metrics were chosen,
- why these thresholds were chosen,
- why a baseline is assumed,
- how to interpret `PROMOTE` vs `BLOCK`.

---

## 1) Why this governance layer exists

Without a release gate, AI updates are often approved because they "sound better."  
In real operations, this can hide regressions: less usable recommendations, lower consistency, and higher manual rework.

Phase 3 introduces a reliability gate so each candidate version is judged against explicit policy before release.

---

## 2) Is a baseline realistic?

Yes. It is both realistic and necessary.

In practice, a baseline is the currently approved behavior in production (prompt/model/workflow version).  Even if a team does not yet have a formal baseline process, creating one is the first step toward production governance.

Why it matters:
- no baseline -> no meaningful regression detection,
- no regression detection -> no controlled release decisions.

---

## 3) Why these KPIs

The selected KPIs represent business usability, not just text quality.

## A) Relevance
- **Question answered:** Does the suggestion match the campaign brief and objective?
- **Business risk if low:** team executes ideas that do not address the real goal.

## B) Actionability
- **Question answered:** Can a manager execute the recommendation immediately?
- **Business risk if low:** recommendations require reinterpretation; cycle time slows.

## C) Constraint Adherence
- **Question answered:** Does the recommendation respect budget/channel/segment constraints?
- **Business risk if low:** infeasible actions and wasted planning effort.

## D) Structure
- **Question answered:** Is output consistently formatted for review/use?
- **Business risk if low:** harder review, harder automation, inconsistent handoffs.

---

## 4) KPI scoring scale and interpretation

All KPI values are on a 0-10 scale.

- **0-3:** poor / high risk
- **4-6:** acceptable but weak
- **7-8:** good
- **9-10:** excellent and dependable

Important note:
- In a small MVP, absolute values are less important than **relative movement** (candidate vs baseline) and gate decision behavior.

---

## 5) Why these gate rules

Current Phase 3 gate policy:
- block if aggregate quality drops more than 5%,
- block if actionability drops more than 8%,
- block if score variance increases more than 20%.

### Why aggregate drop > 5% blocks
- protects overall quality from meaningful regressions,
- avoids shipping changes that degrade the system materially.

### Why actionability drop > 8% blocks
- actionability is tightly linked to operational usefulness,
- even polished output is low-value if hard to execute.

### Why variance increase > 20% blocks
- catches instability across different briefs,
- unstable systems are risky even when average quality looks acceptable.

---

## 6) Why a small quality drop is tolerated

A zero-tolerance gate (any drop blocks release) is usually too strict due to measurement noise:
- model response variability,
- evaluator variability,
- small sample effects in MVP datasets.

A tolerance band allows minor fluctuation while still blocking meaningful regressions.

This is standard in quality engineering:
- strict enough to protect reliability,
- flexible enough to keep delivery practical.

---

## 7) Interpreting Phase 3 result

In the latest run, the candidate was **BLOCKED** because it exceeded allowed degradation thresholds.

Business interpretation:
- the update should not be promoted yet,
- the governance mechanism worked as designed,
- the team avoided releasing a lower-reliability variant.

This demonstrates the core project value:
AI changes are now controlled by evidence-based release policy, not by intuition.

---

## 8) How to present this in interview/business language

Use this short framing:

"We treated prompt/model updates as release candidates.  
Each candidate was evaluated against a baseline using explicit quality and stability thresholds.  
If regression exceeded tolerance, release was blocked.  
This converts LLM output quality from subjective review into an engineering governance process."

---

## 9) Recommended placement in the project docs

Use this document as a companion to:
- `PHASE3_IMPLEMENTATION_PLAN.md` (what was built),
- `PHASE3_RUNBOOK.md` (how to run),
- `reports/latest_report.md` (latest evidence).

Together they provide:
- design intent,
- execution mechanics,
- measurable outcomes,
- explainability for decision-makers.
