# Segmented evaluation report

- Baseline run: `21`
- Candidate run: `22`
- Source: `validation_suite.jsonl`

## By `evaluation_segment` (data-backed)

| Segment | Cases | n | Mean agg baseline | Mean agg candidate | Mean Δ aggregate | Signal |
|---|---|---:|---:|---:|---:|---|
| conversion | TC05, TC08 | 2 | 4.732 | 4.779 | +0.046 | **FLAT** |
| launch | TC01 | 1 | 4.630 | 5.880 | +1.250 | **PROMOTE_SEGMENT** |
| multi_audience | TC02 | 1 | 4.239 | 4.338 | +0.099 | **PROMOTE_SEGMENT** |
| retention | TC03 | 1 | 4.838 | 4.671 | -0.167 | **BLOCK_SEGMENT** |
| stress_ambiguous | TC11 | 1 | 4.968 | 4.505 | -0.463 | **BLOCK_SEGMENT** |
| stress_conflicting | TC12 | 1 | 3.271 | 3.506 | +0.235 | **PROMOTE_SEGMENT** |
| sustainability | TC10 | 1 | 7.343 | 3.881 | -3.462 | **BLOCK_SEGMENT** |

## Rollup groups (narrative alignment)

| Group | Cases | n | Mean Δ aggregate | Signal | Notes |
|---|---|---:|---:|---|---|
| launch | TC01 | 1 | +1.250 | **PROMOTE_SEGMENT** | Single structured launch brief. |
| multi_audience_briefs | TC02, TC10, TC12 | 3 | -1.043 | **BLOCK_SEGMENT** | Briefs with multiple segments and/or channels. |
| sustainability | TC10 | 1 | -3.462 | **BLOCK_SEGMENT** | EU sustainability storytelling (parents + educators). |
| stress | TC11, TC12 | 2 | -0.114 | **BLOCK_SEGMENT** | Ambiguous or conflicting constraints. |

## How to read `Signal`

- **PROMOTE_SEGMENT**: mean aggregate improved vs baseline for that slice (toy threshold ±0.05).
- **BLOCK_SEGMENT**: mean aggregate worsened materially for that slice.
- **FLAT**: mixed or neutral on average — treat as no global claim for that slice.

Portfolio gate on the full 8 cases remains authoritative for **global** release; segments explain *where* v3 helps or hurts.
