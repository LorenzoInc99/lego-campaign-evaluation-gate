# Phase 4 - Observability and Governance Hardening

## Purpose
Phase 3 proved that a single baseline-vs-candidate comparison can block a weak release.

Phase 4 extends this into an operational control layer:
- monitor quality trends across multiple runs,
- detect drift patterns early,
- keep an auditable history of release decisions.

---

## 1) Business Objective

Move from "one-off evaluation" to "continuous reliability monitoring."

This helps stakeholders answer:
- Is assistant quality stable over time?
- Are we seeing systematic degradation in a specific metric?
- Are release decisions traceable and defensible?

---

## 2) Scope

## In Scope
- trend tracking across historical runs,
- drift diagnostics for each quality metric,
- governance audit summary for decisions (`PROMOTE`/`BLOCK`),
- manager-friendly observability report.

## Out of Scope
- real-time dashboard UI,
- external alert integrations (Slack/email),
- automated rollback workflow.

---

## 3) Key Deliverables

1. **Trend report script** over historical runs.
2. **Drift diagnostics** (run-to-run change and rolling trend).
3. **Governance audit section**:
   - when each decision happened,
   - baseline/candidate IDs,
   - failed checks,
   - final decision.
4. **Phase 4 report artifact** for stakeholder review.

---

## 4) Phase 4 Data Questions

For each metric (`relevance`, `actionability`, `constraint`, `structure`, `aggregate`):
- average score by run,
- trend direction (improving / stable / degrading),
- largest negative jump (potential regression event).

For governance:
- count of blocked vs promoted candidates,
- top recurring failed checks,
- latest decision rationale.

---

## 5) Expected Outcomes

By end of Phase 4:
- quality is observable over time, not only at release snapshots,
- drift risks are visible before stakeholder complaints,
- governance decisions are auditable with clear evidence.

---

## 6) Exit Criteria

Phase 4 is complete when:
- observability report is generated from `runs.sqlite`,
- report includes both trend and governance sections,
- at least one drift insight is extracted from actual run history,
- decision history is readable by non-technical stakeholders.

---

## 7) Handoff to Phase 5

Phase 5 can focus on operationalization:
- threshold calibration using more cases,
- stronger business KPI linkage (non-synthetic),
- CI/CD integration for automatic pre-release checks.
