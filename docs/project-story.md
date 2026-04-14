# Project story — from problem to results

---

## 1. The problem

Marketing teams increasingly use **LLMs** to turn campaign briefs into concrete actions. **Changing prompts or models** is risky: a new version can look **better on a few examples** but **worse on other brief types** (e.g. multi-audience, sustainability, messy constraints). If that is not measured **before** release, failures show up **after** spend or campaigns are committed.

The core issue is **release risk**, not “prettier text”: *is a proposed change **safe to roll out broadly**?*

---

## 2. The desired outcome

A **repeatable evaluation loop** that supports a clear decision: **promote**, **block**, or **scope** a change—using **evidence**, not intuition.

Concretely:

- **Same inputs** for every comparison (fair regression-style testing).
- **Scores** that reflect commercial usefulness (relevance, actionability, constraints, structure).
- An explicit **gate** (rules + thresholds) with **documented reasons** when something fails.
- **Persistence and reports** so the decision is **auditable** later.

---

## 3. What was built and why

The deliverable is a **minimal evaluation gate**: a **fixed test suite** of campaign briefs, **baseline vs. candidate** prompts run on **identical** inputs, **scoring**, and **threshold-based** decisions.

**Why this shape:** it mirrors how strong **Analytics & Insights / Innovation & Automation** teams treat AI in production: **evaluation frameworks**, **observability**, and **governance**—making reliability an **engineering** discipline, not an informal sign-off.

---

## 4. How it works (method)

1. **Test data** — Briefs and constraints as **JSONL** rows (portable, line-oriented “analytical” inputs).
2. **Generation** — Each brief is run through the **baseline** and **candidate** prompt versions via a **REST API** (Google Gemini `generateContent`).
3. **Scoring** — **Judge model** (JSON scores) plus **deterministic** checks (structure, constraint hints), combined into a **weighted aggregate** per case.
4. **Aggregation** — Means across the suite; **segment** views where relevant (e.g. launch vs. sustainability).
5. **Gate** — Configurable thresholds (e.g. max allowed drops, variance stability when sample size is sufficient).
6. **Storage & reporting** — **SQLite** for runs and scores; **Markdown** reports for human-readable evidence.

This is intentionally **offline / pre-release**: the same pattern extends to **CI**, scheduled runs, and production monitoring as the next layer.

---

## 5. Results (reference evaluation)

For the documented reference run (**8** briefs, baseline **v1-baseline** vs. candidate **v3-user-candidate**):

| Takeaway | What it means |
|----------|----------------|
| **Gate: BLOCK** | The candidate should **not** replace the baseline as the **global default** on this evidence. |
| **Portfolio mean** | Aggregate and actionability **dropped** on average vs. baseline. |
| **Segmentation** | Candidate **improved** on a **launch-style** case; **regressed strongly** on a **multi-audience sustainability** case. |
| **Lesson** | **Local wins do not imply global safety**—segmented evaluation surfaces **hidden regressions** before a broad rollout. |

Detailed numbers: [`FINAL_DECISION_STORY.md`](../FINAL_DECISION_STORY.md), [`reports/latest_report.md`](../reports/latest_report.md).

---

## 6. Tools and technologies (role-aligned)

Mapped to typical **Analytics Engineer** expectations (Python, SQL, APIs, lifecycle thinking):

| Area | What this repo uses |
|------|---------------------|
| **Language** | **Python 3.10+** — typed, small modules (`src/`), CLI entrypoints (`scripts/`). |
| **Data** | **JSONL** test suites; **SQLite** for run history, outputs, and scores (analytical dataset + audit trail). |
| **APIs** | **REST consumer** — Gemini **HTTP** API via standard library (`urllib`), no extra runtime deps. |
| **Evaluation** | Rubric dimensions + judge model; **baseline vs. candidate** comparison; configurable **quality gate**. |
| **Observability / reporting** | Markdown reports; optional segment and **observability** summaries from the same DB. |
| **Docs & handoff** | **LaTeX** → PDF case studies (`report/`); Markdown in `docs/`. |

**Not in scope** (natural extensions for the role): CI (**GitHub Actions**), **Databricks** / **MLflow**-style tracking, production drift monitors—the narrative and code are structured so those are **next steps**, not missing “magic.”

---

## One-line summary

**Same briefs, two prompt versions, measured scores, explicit gate—evidence that the candidate wins in some segments and fails in others, so a global default is blocked.**
