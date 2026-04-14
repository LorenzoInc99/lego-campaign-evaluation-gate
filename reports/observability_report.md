# Observability and governance report

## Run Trend Overview
| run_id | run_type | relevance | actionability | constraints | structure | aggregate |
|---:|---|---:|---:|---:|---:|---:|
| 3 | baseline | 5.000 | 5.000 | 0.833 | 1.670 | 3.625 |
| 4 | candidate | 5.000 | 5.000 | 0.000 | 0.000 | 3.250 |
| 5 | baseline | 5.000 | 5.000 | 1.110 | 1.670 | 3.694 |
| 6 | candidate | 5.000 | 5.000 | 0.000 | 0.000 | 3.250 |
| 7 | baseline | 0.083 | 3.492 | 0.555 | 1.670 | 1.553 |
| 8 | candidate | 0.052 | 2.500 | 0.000 | 0.000 | 0.890 |
| 9 | baseline | 4.083 | 4.750 | 5.833 | 5.414 | 4.887 |
| 10 | candidate | 7.276 | 3.342 | 3.888 | 0.694 | 4.394 |
| 11 | baseline | 3.597 | 4.975 | 7.223 | 6.387 | 5.265 |
| 12 | candidate | 3.657 | 4.750 | 6.945 | 5.693 | 5.065 |
| 13 | baseline | 3.750 | 3.400 | 3.330 | 3.330 | 3.481 |
| 14 | candidate | 6.250 | 4.300 | 6.670 | 8.330 | 5.880 |
| 15 | baseline | 3.650 | 4.300 | 6.000 | 5.664 | 4.667 |
| 17 | baseline | 3.750 | 3.400 | 3.330 | 3.330 | 3.481 |
| 18 | candidate | 6.250 | 4.300 | 6.670 | 8.330 | 5.880 |
| 19 | baseline | 3.750 | 4.300 | 6.670 | 3.330 | 4.630 |
| 20 | candidate | 6.250 | 4.300 | 6.670 | 8.330 | 5.880 |
| 21 | baseline | 2.966 | 4.750 | 7.501 | 4.165 | 4.844 |
| 22 | candidate | 2.901 | 4.300 | 7.085 | 3.955 | 4.542 |

## Drift Diagnostics
- `relevance_score`: 5.000 -> 2.901 (degrading)
- `actionability_score`: 5.000 -> 4.300 (degrading)
- `constraint_score`: 0.833 -> 7.085 (improving)
- `structure_score`: 1.670 -> 3.955 (improving)
- `aggregate_score`: 3.625 -> 4.542 (improving)

## Governance Decision Summary
- Total decisions logged: 9
- PROMOTE count: 2
- PROMOTE_CONDITIONAL count: 1
- BLOCK count: 6

### Top Failed Check Categories
- `aggregate_drop_pct` occurred 5 time(s)
- `variance_increase_pct` occurred 4 time(s)
- `actionability_drop_pct` occurred 3 time(s)
- `variance_delta_abs` occurred 1 time(s)

## Decision Audit Trail
| decision_id | baseline_run_id | candidate_run_id | decision | note |
|---:|---:|---:|---|---|
| 1 | 3 | 4 | BLOCK | Candidate blocked by reliability gate. |
| 2 | 5 | 6 | BLOCK | Candidate blocked by reliability gate. |
| 3 | 7 | 8 | BLOCK | Candidate blocked by reliability gate. |
| 4 | 9 | 10 | BLOCK | Candidate blocked by reliability gate. |
| 5 | 11 | 12 | PROMOTE | Candidate passes reliability gate. |
| 6 | 13 | 14 | BLOCK | Candidate blocked by reliability gate. |
| 7 | 17 | 18 | PROMOTE | Candidate passes quality checks (conditional: limited sample size). |
| 8 | 19 | 20 | PROMOTE_CONDITIONAL | Candidate passes quality checks with limited sample-size confidence. |
| 9 | 21 | 22 | BLOCK | Candidate blocked by reliability gate. |
