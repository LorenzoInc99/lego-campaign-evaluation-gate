# Validation suite run — summary

**Primary artifacts (read these first):**

- `FINAL_DECISION_STORY.md` — one-screen portfolio decision (BLOCK v3 globally)
- `reports/segment_report.md` — per-segment and rollup signals (where v3 wins / loses)
- `ROUTING_SUGGESTION.md` — optional routing idea only (not implemented)

## Suite definition (`data/validation_suite.jsonl`)

Eight cases chosen for coverage and robustness:

| ID | Type | Role in suite |
|----|------|----------------|
| TC01 | Awareness | Product launch, geo + holiday, IG/YouTube |
| TC02 | Conversion | Promo window, search + email, high budget |
| TC03 | Retention | Lapsed members, low budget, email + app |
| TC05 | Conversion | Flagship Technic, search + retargeting |
| TC08 | Conversion | Flash sale, low budget, email + onsite |
| TC10 | Awareness | Sustainability, EU, YouTube + LinkedIn, dual audience |
| TC11 | Stress | Ambiguous brief, “digital” channel |
| TC12 | Stress | Conflicting goals + low budget + multi-channel |

## Run settings

- **Dataset:** `data/validation_suite.jsonl` (8 cases)
- **Baseline prompt:** `v1-baseline`
- **Candidate prompt:** `v3-user-candidate` (internal planner format)
- **Model:** `gemini-2.5-flash`, `MODEL_TEMPERATURE=0.0`, `JUDGE_TEMPERATURE=0.0`
- **Runs:** baseline `21`, candidate `22`

## Gate outcome

| Field | Value |
|--------|--------|
| **Decision** | **BLOCK** |
| **Confidence** | **1.00** (n = 8 ≥ minimum for variance gate) |
| **Variance gate** | Applied |

### Failed checks

1. `aggregate_drop_pct=6.23%` > 5%
2. `actionability_drop_pct=9.47%` > 8%
3. `variance_delta_abs=0.839` > 0.5 (with n ≥ 5)

### Aggregate scorecard (mean across 8 cases)

| Metric | Baseline | Candidate | Delta |
|--------|----------|-------------|-------|
| Relevance | 2.966 | 2.901 | -0.065 |
| Actionability | 4.750 | 4.300 | -0.450 |
| Constraint | 7.501 | 7.085 | -0.416 |
| Structure | 4.165 | 3.955 | -0.210 |
| **Aggregate** | **4.844** | **4.542** | **-0.302** |

## Per-case aggregate score (candidate − baseline)

| Case | Baseline | Candidate | Δ |
|------|----------|-------------|---|
| TC10 | 7.343 | 3.881 | **-3.462** |
| TC08 | 5.959 | 5.219 | -0.740 |
| TC11 | 4.968 | 4.505 | -0.463 |
| TC03 | 4.838 | 4.671 | -0.167 |
| TC02 | 4.239 | 4.338 | +0.099 |
| TC12 | 3.271 | 3.506 | +0.235 |
| TC05 | 3.506 | 4.338 | +0.832 |
| TC01 | 4.630 | 5.880 | **+1.250** |

## Interpretation

- **TC01** improved strongly under the candidate prompt (aligned with the single-case experiment).
- **TC10** dropped sharply — sustainability / parents + educators / YouTube + LinkedIn is hard; candidate output likely missed structure or channel fit vs baseline on this run.
- **Portfolio mean** still regressed on actionability and aggregate, so the **release gate correctly blocks** promotion of `v3` as the default for all brief types without further iteration.
- **Recommendation:** Treat `v3` as promising for structured launches (e.g. TC01) but **not** as a blind replacement; refine for multi-audience / EU / stress cases or use **routing** (different prompts per campaign type).

## Artifacts

- `reports/latest_report.md` — full Phase 3 report for runs 21 vs 22
- `reports/phase4_observability_report.md` — trend + governance history
