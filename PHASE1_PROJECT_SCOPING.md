# Phase 1 - Project Scoping and Success Definition

## Document Purpose
This document defines what will be built, why it matters for the LEGO Analytics Engineer role, and how success will be measured before implementation starts.

---

## 1) Why this Phase 1 is necessary

For this project, quality is not "model output looks good"; quality is reliability, observability, and business relevance.

This phase ensures:
- the project is directly tailored to the hiring team's real problem,
- the MVP scope is realistic for 2 days,
- success metrics are explicit before development starts.

---

## 2) Job Requisites -> Problem Statement

Based on the job description, the team is hiring for:
- evaluation frameworks for LLM/agent outputs when strict ground truth is missing,
- observability (accuracy, drift, business linkage),
- governance through production quality gates,
- reusable engineering patterns (not one-off demos).

### Real problem to solve
How do we keep LLM-assisted commercial decision support reliable over time, and how do we know when a prompt/model change should be blocked?

### Concrete challenges this project addresses
1. No single correct answer, but outputs still need consistent quality checks.
2. Output behavior drifts with prompt/model/context changes.
3. Weak connection between output quality and business-facing outcomes.

### Key insight
Most performance issues in LLM systems are not caused by the model itself, but by system-level factors:
- prompt changes,
- context quality,
- evaluation blind spots,
- missing feedback loops.

This project treats LLM outputs as part of a controlled system, not as isolated model responses.

---

## 3) What I am developing as a hook (Tailored MVP)

## Project title
**Campaign Suggestion Reliability Gate - LEGO Use Case MVP**

## Use case (committed)
An LLM generates campaign optimization suggestions for a LEGO product launch brief.

## MVP deliverable
A minimal evaluation and observability framework that:
1. scores suggestion quality with rubric + deterministic checks,
2. tracks score trends and regressions over time,
3. applies a quality gate (pass/fail) for candidate prompt/model versions,
4. links quality changes to simple business proxy metrics.

---

## 4) Why this hook fits the role

This project demonstrates the exact work profile in the posting:
- **Evaluation:** structured scoring without strict labels.
- **Observability:** trend and drift monitoring across runs.
- **Governance:** explicit release gate driven by measurable thresholds.
- **Engineering mindset:** reusable template for future AI workflows.

This approach treats LLM systems as engineered products with explicit release criteria, rather than experimental outputs.

## Example failure case (why this system is needed)
A prompt update increases suggestion detail and length, which initially appears as an improvement.  
However:
- suggestions become less actionable,
- decision clarity decreases,
- manual rewrite rate increases.

Without structured evaluation, this change would likely be promoted.  
The reliability gate instead blocks it due to a drop in actionability score and increased variance across outputs.

---

## 5) Scope Definition

## In Scope (Phase 1 to MVP definition)
- single concrete use case (campaign optimization suggestions),
- quality rubric and scoring criteria definition,
- metric framework (quality, reliability, business proxies),
- pass/fail gate rule definition,
- expected outputs and acceptance criteria.

## Out of Scope (for now)
- full production deployment,
- enterprise security/IAM hardening,
- large-scale platform rollout across multiple teams,
- advanced causal inference for business impact.

---

## 6) Goal and Expected End Result

## Goal
Design a practical, measurable framework that can decide whether a prompt/model change improves or degrades production readiness for a commercial decision-support LLM workflow.

## Expected end result
By end of project:
1. A repeatable evaluation run compares baseline vs candidate.
2. A quality gate produces a clear promote/block decision.
3. A compact dashboard/report shows trends, regressions, and metric breakdown.
4. A short narrative links technical quality changes to business proxy movement.

---

## 7) Measurement Plan (What and How)

## A) Output quality metrics (per run)
- Relevance to campaign brief
- Actionability / decision clarity
- Constraint adherence (budget/channel/segment)
- Structural correctness (format/schema)

**How measured**
- Deterministic checks for structure/constraints
- LLM-judge rubric scoring for qualitative criteria
- Weighted aggregate quality score

## B) Reliability over time metrics
- Aggregate quality trend (daily/weekly run history)
- Criterion-level drift detection
- Regression delta vs baseline after each candidate change

**How measured**
- Persist run metadata: prompt version, model version, timestamp, score breakdown
- Compare candidate scores against baseline thresholds

## C) Business proxy metrics
- Suggestion acceptance rate
- Manual rewrite rate
- Follow-up clarification rate

**How measured**
- Simulated or sampled review outcomes linked to each run window
- Correlation table between quality score changes and business proxy shifts

**Why this matters operationally**
In a campaign optimization context, a 10-15% drop in suggestion acceptance rate can translate into:
- slower campaign iteration cycles,
- increased manual analyst workload,
- delayed market response windows.

This framework is designed to catch these regressions before deployment.

---

## 8) Phase 1 Success Criteria

Phase 1 is complete when:
- scope is fixed to one concrete use case,
- all primary metrics are defined with formulas and thresholds,
- quality gate logic is explicit (including block conditions),
- expected outputs for Phase 2 implementation are agreed,
- one concrete regression scenario is defined as a test case for Phase 2.

---

## 9) Next Phase

Phase 2 will focus on infrastructure and implementation:
- data structures and run logging,
- evaluation runner architecture,
- storage, automation flow, and visualization layer.
