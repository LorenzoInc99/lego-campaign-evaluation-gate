# Final decision story — v3 vs baseline (portfolio evaluation)

**Read time: ~20 seconds**

---

## Question

**Is candidate prompt v3 safe to deploy portfolio-wide?**

## Answer

**No — BLOCK.**

---

## Evidence

| Fact | Detail |
|------|--------|
| Evaluation set | **8** realistic campaign briefs (`data/validation_suite.jsonl`) |
| Baseline / candidate | `v1-baseline` vs `v3-user-candidate` |
| Reference runs | Baseline run **21**, candidate run **22** |
| Portfolio mean (aggregate score) | **Decreased** (4.844 → 4.542) |
| Per-case aggregate | **4** cases improved vs baseline, **4** degraded |
| Largest regression | **TC10** (sustainability, multi-audience, EU): **−3.46** aggregate points |
| Largest gain | **TC01** (launch / awareness): **+1.25** aggregate points |
| Gate confidence | **1.00** (n ≥ 5; variance gate applied) |

Failed checks (portfolio gate): aggregate drop > 5%, actionability drop > 8%, variance stability threshold exceeded.

---

## Key insight

**A single prompt does not generalize across campaign types.**

v3 can **win** on a structured launch-style brief (TC01) and **lose** badly on multi-audience / sustainability complexity (TC10). Shipping v3 globally after TC01-only testing would risk **hidden regressions** where marketing only notices problems later.

---

## Decision

**Do not release v3 as the default for all briefs.**

---

## Recommendation

1. **Targeted deployment only** — e.g. routing or scoped release (launch / single-audience paths first).
2. **Iterate v3** for sustainability + stress cases, **or** keep a separate baseline path for those segments.
3. **Segmented evaluation** — see `reports/segment_report.md` (per-category means and suite-level signals).

---

## One-line positioning

*This system prevents incorrect global deployment of an AI prompt by showing where it works and where it breaks — before production.*
