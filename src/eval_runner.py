from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from .config import AppConfig
from .db import insert_output, insert_run, insert_score
from .llm_client import generate_text
from .scoring import score_output


def load_test_cases(path: Path) -> List[Dict[str, object]]:
    cases: List[Dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        row = line.strip()
        if not row:
            continue
        cases.append(json.loads(row))
    if not cases:
        raise RuntimeError("No test cases found")
    return cases


def _prompt_template(prompt_version: str, brief: str, constraints: Dict[str, object]) -> str:
    if prompt_version == "v3-user-candidate":
        return f"""
You are an internal campaign planner supporting marketing teams.

Your task is to convert a campaign brief and its constraints into EXACTLY 3 concrete campaign actions that can be executed by a marketing team or agency.

INPUTS:
- Brief: {brief}
- Constraints: {json.dumps(constraints, ensure_ascii=True)}

OUTPUT REQUIREMENTS (MANDATORY):
You must return EXACTLY 3 actions. No introduction, no conclusion.

Each action must follow this structure:

Action X:
- What to run:
- Target segment:
- Channels used:
- Execution details:
- Rationale:
- Expected impact:

HARD RULES:
1) Use ONLY the channels listed in the constraints. No exceptions.
2) Respect the budget band:
- Low: simple executions, limited production
- Medium: creator collaborations, paid social/video, moderate production
- High: large-scale campaigns (do NOT assume this unless specified)
3) Address ALL target audiences explicitly:
- If multiple audiences exist, either dedicate actions to each, or explain split between them
4) Each action must be EXECUTABLE:
- specify what content is produced
- who is involved (creators, brand, partners)
- where it runs (exact channel)
5) Avoid vague language.
6) Stay realistic for the specified market/geography.
7) Keep output concise and briefing-ready.

QUALITY STANDARD:
- Actions must be specific, on-channel, on-audience, and aligned with the objective.
- If constraints are violated, the output is incorrect.

Return only the 3 actions in the required format.
"""

    if prompt_version == "v2-verbose":
        return f"""
You are a campaign strategist.
Produce a polished and comprehensive optimization plan for this LEGO campaign brief.
Give exactly 3 actions with rich context and alternatives.
Write with detailed explanation and broader strategic framing.

Brief:
{brief}

Constraints:
{json.dumps(constraints, ensure_ascii=True)}

Output format:
Action 1: ...
Rationale: ...
Target Segment: ...
Expected Impact: ...

Action 2: ...
Rationale: ...
Target Segment: ...
Expected Impact: ...

Action 3: ...
Rationale: ...
Target Segment: ...
Expected Impact: ...
"""

    return f"""
You are a campaign optimizer for LEGO product launches.
Provide exactly 3 actionable suggestions.
Each suggestion must be clear, concise, and immediately executable.
Respect budget/channel/segment constraints strictly.

Brief:
{brief}

Constraints:
{json.dumps(constraints, ensure_ascii=True)}

Output format:
Action 1: ...
Rationale: ...
Target Segment: ...
Expected Impact: ...

Action 2: ...
Rationale: ...
Target Segment: ...
Expected Impact: ...

Action 3: ...
Rationale: ...
Target Segment: ...
Expected Impact: ...
"""


def run_evaluation(conn, config: AppConfig, run_type: str, prompt_version: str) -> int:
    run_id = insert_run(
        conn=conn,
        run_type=run_type,
        timestamp=datetime.now(timezone.utc).isoformat(),
        prompt_version=prompt_version,
        model_version=config.model.name,
        evaluator_version=config.evaluator_version,
    )
    cases = load_test_cases(config.dataset_path)
    for case in cases:
        prompt = _prompt_template(prompt_version, str(case["brief_text"]), dict(case["constraints"]))
        output = generate_text(config.api_key, config.model, prompt)
        output_id = insert_output(
            conn=conn,
            run_id=run_id,
            test_case_id=str(case["test_case_id"]),
            raw_output=str(output["text"]),
            latency_ms=int(output["latency_ms"]),
        )
        scores = score_output(
            config=config,
            brief_text=str(case["brief_text"]),
            constraints=dict(case["constraints"]),
            output_text=str(output["text"]),
        )
        insert_score(conn=conn, output_id=output_id, scores=scores)
    return run_id
