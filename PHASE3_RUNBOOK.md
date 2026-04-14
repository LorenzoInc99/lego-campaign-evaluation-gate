# Phase 3 Runbook

## Prerequisites
- Python 3.11+ available.
- `.env` contains `Gemini_API_KEY=...`.

## Run Sequence
From `job-application-lego` directory:

1. `python3 scripts/run_baseline.py`
2. `python3 scripts/run_candidate.py`
3. `python3 scripts/compare_runs.py`
4. `python3 scripts/generate_report.py`

## Expected Artifacts
- `data/runs.sqlite` (all run/output/score/gate records)
- `reports/latest_report.md` (manager-friendly summary)

## How to test quickly
- Verify both run commands return a `run_id`.
- Verify compare command prints JSON with `decision`.
- Open `reports/latest_report.md` and confirm:
  - baseline vs candidate table exists,
  - gate decision is present,
  - failed checks listed (if blocked),
  - business proxy panel present.

## Phase 3 complete criteria
Proceed to Phase 4 when all are true:
1. Baseline and candidate runs execute end-to-end.
2. Scores are persisted for all test cases.
3. Gate returns deterministic decision with explicit reasons.
4. Report is generated and readable.
5. Failure scenario is demonstrated (candidate looks better but is blocked when quality drops).

## Phase 4 observability step
After Phase 3 runs are available:

- `python3 scripts/generate_phase4_report.py`

Expected artifact:
- `reports/phase4_observability_report.md`

This report summarizes:
- metric trends across historical runs,
- drift direction per metric,
- governance audit history (`PROMOTE` vs `BLOCK`, failed checks).
