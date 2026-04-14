# Management brief — LLM campaign evaluation gate

**Audience:** engineering managers, product leaders, analytics leadership  
**Purpose:** explain what this project is, why it matters commercially, and what evidence it produces—without walking through code.

---

## 1. Purpose in one minute

Marketing and growth teams increasingly rely on **large language models** to turn campaign briefs into concrete actions. The operational risk is not only “bad wording,” but **release risk**: a new prompt or model version can **improve** outcomes on some brief types and **silently degrade** them on others. Teams that ship on anecdotes (“it reads better”) can discover regressions **after** campaigns go live.

This project is a **portfolio-scale demonstration** of how **analytics engineering** can treat that risk like any other production change: **measure first**, **compare systematically**, **document a decision**, and **surface segment-level effects** so a global rollout is not justified by a narrow win.

---

## 2. The business problem (framed for leadership)

| Risk | What goes wrong |
|------|------------------|
| **Hidden regressions** | A candidate assistant looks strong on a few examples but fails on multi-audience, sustainability, or high-complexity briefs. |
| **False confidence** | Portfolio averages hide **where** quality moves; marketing notices problems only in-channel or after spend. |
| **Weak governance** | Without a repeatable gate, “ship the new prompt” becomes a judgment call instead of an **evidence-based** decision. |

The question this work answers is deliberately narrow and managerially useful:

> **“Given a proposed change to how the assistant behaves, is it safe to treat it as the default for all similar briefs—or should we block, scope, or iterate first?”**

---

## 3. What was built (conceptual, not technical)

The implementation is an **offline evaluation pipeline**—a control loop that runs **before** production deployment:

1. **Fixed test suite** — A set of realistic campaign briefs (same inputs every time).
2. **Two versions compared** — A **baseline** prompt and a **candidate** prompt (or, in principle, two model configurations) run against identical inputs.
3. **Scoring** — Outputs are graded on dimensions that map to commercial usefulness (e.g. relevance, actionability, respect for constraints, structure), using a mix of **structured rules** and **model-assisted judging**.
4. **Aggregation** — Scores roll up to portfolio-level metrics **and** can be inspected **per case or segment** (e.g. launch vs. sustainability, single vs. multi-audience).
5. **Quality gate** — Explicit rules produce a decision such as **promote**, **block**, or **conditional** paths, with **documented reasons** when something fails.
6. **Audit trail** — Runs and scores are stored so comparisons are **repeatable** and **reviewable**, not one-off screenshots.

This is **not** a customer-facing product. It is a **template for how to govern LLM-driven recommendations** in a decision-support context—aligned with how serious analytics and AI teams treat **reliability as an engineering discipline**.

---

## 4. Reference outcome (what the evidence showed)

The repository includes a **completed reference evaluation** so stakeholders can review **numbers and narrative** without re-running anything.

**Headline result:** For the reference candidate prompt, the system’s recommendation was to **not** ship it as the **global default**.

**Why that is instructive for management:** The candidate **improved** results on at least one **structured launch-style** brief, but **regressed strongly** on a **complex multi-audience / sustainability** scenario. Portfolio-level averages reflected an overall drop; the important lesson is **segmentation**: *local wins do not imply global safety.*

That story is the core **governance** message—**block or scope** until the weak segments are addressed or routing is explicit.

Detailed tables and the formal write-up appear in the **case study PDF** (LaTeX source under `report/`) and in `FINAL_DECISION_STORY.md`.

---

## 5. Why this maps to modern analytics / AI roles

| Theme | How this project illustrates it |
|--------|----------------------------------|
| **Evaluation** | Benchmark-style runs and rubrics when there is no single “correct” answer. |
| **Observability** | Run history and reports that connect behaviour to **documented** decisions. |
| **Governance** | Thresholds and explicit **block** reasons—not vague sign-off. |
| **Partnership** | The same artefacts can feed **Digital Product**, **Data Office**, and marketing stakeholders with a **shared fact base**. |

---

## 6. Boundaries (what this MVP is not)

To keep expectations aligned in a manager conversation:

- **Not** connected to live LEGO systems or production traffic; **synthetic / portfolio** data and public APIs only.
- **Not** a full MLOps platform (e.g. scheduled CI, experiment registry, Databricks deployment)—those are natural **next steps**, described as extensions in the technical materials.
- **Not** a substitute for human review of creative or brand strategy; it is a **technical gate** for **prompt/model change risk**.

---

## 7. Where to go deeper (optional)

| Document | Best for |
|----------|----------|
| Case study PDF (`report/LEGO_Case_Study_Report.tex` → PDF) | Figures, tables, role-aligned narrative |
| `FINAL_DECISION_STORY.md` | One-screen decision summary |
| `README.md` | Technical orientation and reproduction |
| `docs/case-study.md` | Short engineering narrative |

---

## 8. Suggested talking points (if time is short)

- **Problem:** LLM changes need **evidence**, not only demos.  
- **Approach:** Same briefs, two versions, **scores + gate + audit trail**.  
- **Outcome reference:** **Block** global default; **segment wins and losses** tell the real story.  
- **Value:** Makes **reliability and governance** concrete for **commercial decision support** use cases.

---

*This brief is intended to accompany a live walkthrough of the repository or PDF; it does not replace the detailed case study for technical depth.*
