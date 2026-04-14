# Optional routing (consequence only — not implemented)

This is a **logical follow-up** to segmented results, not a product feature in this repo.

**Idea:** Deploy v3 only where evidence supports it.

Example policy (illustrative):

| If brief looks like… | Suggested path |
|----------------------|----------------|
| Single-market product launch with clear channels (e.g. segment `launch`) | Consider **v3** after human review |
| Sustainability / multi-audience EU (e.g. TC10-class) | Keep **baseline** until v3 is fixed or a dedicated prompt exists |
| Stress / ambiguous / conflicting constraints | **Baseline** or human triage |

**Pseudo-rule (not code):**

```text
if evaluation_segment == "launch" and single-case pilot passed:
    allow v3 in scoped rollout
else:
    default to baseline
```

Real routing would need tagging in the product intake, not only offline evaluation.
