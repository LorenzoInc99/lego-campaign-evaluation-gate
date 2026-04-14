# Case study: evaluation and governance for LLM campaign assistants

## Problem

Marketing and growth teams increasingly use internal LLMs for **campaign-style** workflows. The risk is **release risk**: a new prompt can read better on a few examples while **silently degrading** other scenarios. Without structured evaluation, those **hidden regressions** erode trust—exactly what **AI governance** and **observability** are meant to prevent.

**Question this MVP answers:** *Is a candidate assistant version safe to deploy portfolio-wide?*

## What was built

1. **Structured regression suite** — Campaign briefs and constraints as JSONL; the same inputs are run under **baseline** and **candidate** prompt versions.
2. **Scoring** — Rubric-aligned dimensions (e.g. relevance, actionability, constraints, structure) using model-assisted judging with controlled temperature.
3. **Quality gates** — Thresholds on aggregate and component drops, plus **sample-size-aware** variance checks so decisions are not over-confident on tiny sets.
4. **Persistence and reporting** — SQLite stores runs and scores; scripts emit **Markdown reports** and support **segment rollups** (e.g. launch vs. multi-audience sustainability) so failures are localized.
5. **API discipline** — Gemini accessed via **REST** (`urllib`), no extra runtime dependencies.

## Example outcome (illustrative)

On a validation suite of eight cases, a candidate version can **improve** on a structured launch brief while **regressing** on a complex multi-audience sustainability scenario. A **portfolio mean** drop plus segment signals supports a **BLOCK** decision rather than a global ship—demonstrating **segmented evaluation** as a governance tool.

## Role fit (Analytics Engineer, Innovation & Automation)

- **Evaluation frameworks** for LLM outputs without a single ground-truth label  
- **Observability** via run history and report artifacts  
- **Governance** through explicit, documented gate logic  
- **Python**, **SQL** (SQLite analytical store), **REST API** consumption  
- **Lifecycle** mindset: evaluate → gate → document, not only “prompt once”

## Artefacts for reviewers

| Artefact | Where |
|----------|--------|
| PDF case study (figures, tables, role keywords) | Build from `report/LEGO_Case_Study_Report.tex` |
| Runnable code | `src/`, `scripts/` |
| Decision narrative | `FINAL_DECISION_STORY.md` |

## Future hardening (not in this MVP)

CI (e.g. GitHub Actions) for scheduled evals, experiment tracking, Databricks-style deployment patterns, and production **drift** signals once telemetry exists.
