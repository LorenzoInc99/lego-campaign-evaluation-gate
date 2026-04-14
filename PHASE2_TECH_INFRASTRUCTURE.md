# Phase 2 - Technical Infrastructure (Small Project)

## Document Purpose
Define the minimum technical infrastructure required to implement the Phase 1 scope for a 2-day MVP, while preserving production-style engineering signals (traceability, repeatability, and release gating).

---

## 1) Infrastructure Principles

This is intentionally a small project. Infrastructure should be:
- **Minimal:** only components required to evaluate, track, and gate LLM outputs.
- **Traceable:** every run is versioned and reproducible.
- **Extensible:** structure can scale later without rework.
- **Fast to demo:** setup and execution should remain lightweight.

---

## 2) Recommended Stack (MVP)

## Core language and runtime
- **Python 3.11+**
- Why: strong fit with role requirements, fast implementation, rich tooling for data and LLM workflows.

## Storage
- **SQLite (local file DB)** for MVP run logging and metrics.
- Why: zero setup, SQL-based analysis, portable.
- Upgrade path: PostgreSQL if project is extended.

## LLM provider integration
- **Single provider via REST API** (any existing key/account you already use).
- Why: keep integration simple and focus on evaluation/governance logic.

## Reporting and visualization
- **Markdown report + simple charts (matplotlib or plotly)**
- Why: manager-friendly outputs without building a UI.

## Optional lightweight orchestration
- **Makefile or simple Python CLI (`python -m ...`)**
- Why: repeatable commands for baseline, candidate, compare, report.

---

## 3) System Components

## A) Evaluation Runner
Inputs:
- test campaign briefs,
- baseline prompt/model config,
- candidate prompt/model config.

Responsibilities:
- execute prompts,
- collect outputs and metadata,
- pass outputs to scoring pipeline.

## B) Scoring Engine
Responsibilities:
- deterministic checks (format, required fields, constraints),
- rubric scoring (LLM-judge),
- weighted aggregate score and per-criterion breakdown.

## C) Run Logger
Responsibilities:
- persist run-level and sample-level results,
- store versions (prompt, model, evaluator config),
- support baseline vs candidate comparisons.

## D) Reliability Gate
Responsibilities:
- apply threshold logic,
- produce decision (`PROMOTE` / `BLOCK`),
- provide reason codes (which metrics failed).

## E) Reporting Layer
Responsibilities:
- generate concise summary for stakeholders,
- visualize trend, regression deltas, and gate result,
- include business proxy interpretation.

---

## 4) Data Model (Minimal)

Use SQLite tables:

1. **runs**
- `run_id`
- `run_type` (`baseline` or `candidate`)
- `timestamp`
- `prompt_version`
- `model_version`
- `evaluator_version`

2. **test_cases**
- `test_case_id`
- `campaign_type`
- `brief_text`
- `constraints_json`

3. **outputs**
- `output_id`
- `run_id`
- `test_case_id`
- `raw_output`
- `latency_ms`

4. **scores**
- `score_id`
- `output_id`
- `relevance_score`
- `actionability_score`
- `constraint_score`
- `structure_score`
- `aggregate_score`

5. **gate_decisions**
- `decision_id`
- `run_id`
- `decision` (`PROMOTE`/`BLOCK`)
- `failed_checks_json`
- `decision_note`

6. **business_proxies**
- `proxy_id`
- `run_id`
- `acceptance_rate`
- `rewrite_rate`
- `clarification_rate`

---

## 5) Folder Structure (MVP)

```text
job-application-lego/
  docs/
  data/
    test_cases.jsonl
    runs.sqlite
  src/
    config.py
    eval_runner.py
    scoring.py
    gate.py
    reporting.py
    llm_client.py
    db.py
  reports/
    latest_report.md
  scripts/
    run_baseline.py
    run_candidate.py
    compare_runs.py
    generate_report.py
  PHASE1_PROJECT_SCOPING.md
  PHASE2_TECH_INFRASTRUCTURE.md
```

---

## 6) Configuration and Versioning

Track versions explicitly:
- `prompt_version` (e.g., `v1`, `v2`)
- `model_version` (provider/model identifier)
- `evaluator_version` (scoring weights and rubric revision)

Use one config file (`config.py` or `.env`) for:
- API credentials,
- thresholds,
- scoring weights,
- active dataset path.

This guarantees each run can be reproduced and audited.

---

## 7) Gate Logic (Initial)

Example block conditions:
- aggregate score drops by more than 5% vs baseline,
- actionability score drops by more than 8%,
- score variance increases above threshold across test cases.

Decision output:
- status: `PROMOTE` or `BLOCK`
- failed criteria list
- short reason summary for manager review

---

## 8) Visualization Plan (No UI Build)

Deliver one markdown report containing:
1. **Scorecard:** baseline vs candidate (per criterion + aggregate).
2. **Trend chart:** quality trend across runs.
3. **Gate panel:** decision and failed checks.
4. **Business proxy panel:** acceptance/rewrite/clarification deltas.
5. **Failure case highlight:** one example where output looked better but failed reliability criteria.

This is enough to communicate system behavior clearly without frontend overhead.

---

## 9) Definition of Done for Phase 2

Phase 2 is complete when:
- stack and components are fixed,
- data schema is defined and documented,
- folder structure and run commands are specified,
- gate thresholds are explicit,
- reporting format is agreed for implementation in Phase 3.

---

## 10) What comes next (Phase 3)

Implement the evaluation runner + scoring engine + run logging using this infrastructure, then execute the first baseline and candidate comparison.
