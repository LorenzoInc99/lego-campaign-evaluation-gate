# Phase 3 - Implementation Plan (Build Execution)

## Document Purpose
Translate Phase 1 scope and Phase 2 infrastructure into an implementation-ready execution plan for a small MVP.

This phase focuses on building the first working version end-to-end:
- baseline run,
- candidate run,
- scoring and gate decision,
- final report with business proxies.

---

## 1) Phase 3 Target Outcome

By the end of Phase 3, the project should produce:
1. A reproducible baseline evaluation run.
2. A reproducible candidate evaluation run.
3. A comparison with explicit `PROMOTE`/`BLOCK` decision.
4. A markdown report summarizing quality, regressions, and business proxy impact.

---

## 2) Build Sequence (Execution Order)

Implement in this order to reduce integration risk:

1. **Project skeleton + config**
2. **Data layer (SQLite + schema)**
3. **LLM client wrapper**
4. **Evaluation runner**
5. **Scoring engine**
6. **Gate logic**
7. **Comparison + reporting**
8. **Business proxy ingestion**
9. **Validation run (baseline vs candidate)**

---

## 3) File-by-File Implementation Plan

## A) Configuration and constants
### `src/config.py`
Implement:
- model/provider identifiers,
- scoring weights,
- gate thresholds,
- file paths (dataset, SQLite DB, output reports),
- run metadata defaults (`evaluator_version`, etc.).

Definition of done:
- single source of truth for runtime settings,
- no hardcoded values across other modules.

## B) Data access layer
### `src/db.py`
Implement:
- SQLite connection helper,
- table creation/migration function,
- insert helpers for `runs`, `outputs`, `scores`, `gate_decisions`, `business_proxies`,
- query helpers for run comparison.

Definition of done:
- one command initializes DB schema,
- read/write flow works for one synthetic sample.

## C) LLM API wrapper
### `src/llm_client.py`
Implement:
- single function to generate campaign suggestions,
- timeout/retry handling,
- normalized response format (string + metadata).

Definition of done:
- returns stable structured payload for downstream scoring.

## D) Evaluation runner
### `src/eval_runner.py`
Implement:
- load test cases from `data/test_cases.jsonl`,
- execute model for each test case,
- capture latency and output text,
- write run + output records to DB.

Definition of done:
- `baseline` and `candidate` runs can be executed via script.

## E) Scoring engine
### `src/scoring.py`
Implement:
- deterministic checks:
  - required structure present,
  - constraints referenced,
  - expected output sections present,
- rubric scoring hook (LLM-judge),
- aggregate score computation with weights.

Definition of done:
- score breakdown generated per output and persisted in DB.

## F) Gate decision engine
### `src/gate.py`
Implement:
- baseline vs candidate score delta computation,
- threshold checks for:
  - aggregate drop,
  - actionability drop,
  - variance increase,
- decision object with failed criteria.

Definition of done:
- gate returns deterministic `PROMOTE`/`BLOCK` + reason list.

## G) Reporting layer
### `src/reporting.py`
Implement:
- generate markdown summary:
  - baseline vs candidate score table,
  - per-criterion deltas,
  - gate decision summary,
  - highlighted failure case,
  - business proxy panel.

Definition of done:
- report written to `reports/latest_report.md`.

## H) Script entry points
### `scripts/run_baseline.py`
- initialize DB if needed,
- run evaluation for baseline config,
- score and persist.

### `scripts/run_candidate.py`
- run evaluation for candidate config,
- score and persist.

### `scripts/compare_runs.py`
- compute deltas,
- execute gate decision,
- save gate output.

### `scripts/generate_report.py`
- compile all outputs into markdown report.

Definition of done:
- full workflow executable via four scripts in sequence.

---

## 4) Minimal Dataset Plan

### `data/test_cases.jsonl`
Create 20 campaign briefs with variety:
- campaign goals (awareness, conversion, retention),
- budget bands,
- channel constraints,
- segment constraints.

Include at least 3 "stress" cases:
- ambiguous brief,
- conflicting constraints,
- short sparse brief.

Definition of done:
- dataset is realistic enough to trigger scoring variation.

---

## 5) First Failure Scenario to Implement

Implement one explicit regression scenario:
- Candidate prompt is more verbose and polished.
- It decreases actionability and constraint adherence.
- Gate blocks promotion due to threshold failure.

This is the core proof that the framework catches non-obvious quality regressions.

---

## 6) Measurement and Threshold Defaults (Initial)

Suggested initial weights:
- relevance: 0.30
- actionability: 0.35
- constraint adherence: 0.25
- structure: 0.10

Suggested initial block rules:
- aggregate score drop > 5% vs baseline,
- actionability drop > 8%,
- variance increase > defined threshold (e.g., +20%).

These are initial and can be tuned after first run.

---

## 7) Validation Checklist (End of Phase 3)

Phase 3 is complete when:
- baseline and candidate runs execute without manual patching,
- scores are persisted for all test cases,
- gate decision is generated with explicit reasons,
- one regression is correctly blocked,
- markdown report is generated and readable by non-technical stakeholders.

---

## 8) Risks and Mitigations

Risk: LLM-judge scoring noise.  
Mitigation: keep deterministic checks and use stable prompt rubric.

Risk: Overfitting thresholds to small dataset.  
Mitigation: document thresholds as provisional and include confidence caveat.

Risk: Time overrun due to UI/dashboard scope creep.  
Mitigation: markdown-first reporting only.

---

## 9) Handoff to Phase 4

Phase 4 will focus on strengthening observability and governance:
- trend tracking across multiple runs,
- improved drift diagnostics,
- cleaner audit trail for release decisions.
