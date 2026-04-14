from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_type TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            prompt_version TEXT NOT NULL,
            model_version TEXT NOT NULL,
            evaluator_version TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS outputs (
            output_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            test_case_id TEXT NOT NULL,
            raw_output TEXT NOT NULL,
            latency_ms INTEGER NOT NULL,
            FOREIGN KEY(run_id) REFERENCES runs(run_id)
        );

        CREATE TABLE IF NOT EXISTS scores (
            score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            output_id INTEGER NOT NULL,
            relevance_score REAL NOT NULL,
            actionability_score REAL NOT NULL,
            constraint_score REAL NOT NULL,
            structure_score REAL NOT NULL,
            aggregate_score REAL NOT NULL,
            score_variance REAL NOT NULL,
            FOREIGN KEY(output_id) REFERENCES outputs(output_id)
        );

        CREATE TABLE IF NOT EXISTS gate_decisions (
            decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
            baseline_run_id INTEGER NOT NULL,
            candidate_run_id INTEGER NOT NULL,
            decision TEXT NOT NULL,
            failed_checks_json TEXT NOT NULL,
            decision_note TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS business_proxies (
            proxy_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            acceptance_rate REAL NOT NULL,
            rewrite_rate REAL NOT NULL,
            clarification_rate REAL NOT NULL
        );
        """
    )
    conn.commit()


def insert_run(
    conn: sqlite3.Connection, run_type: str, timestamp: str, prompt_version: str, model_version: str, evaluator_version: str
) -> int:
    cur = conn.execute(
        """
        INSERT INTO runs (run_type, timestamp, prompt_version, model_version, evaluator_version)
        VALUES (?, ?, ?, ?, ?)
        """,
        (run_type, timestamp, prompt_version, model_version, evaluator_version),
    )
    conn.commit()
    return int(cur.lastrowid)


def insert_output(conn: sqlite3.Connection, run_id: int, test_case_id: str, raw_output: str, latency_ms: int) -> int:
    cur = conn.execute(
        "INSERT INTO outputs (run_id, test_case_id, raw_output, latency_ms) VALUES (?, ?, ?, ?)",
        (run_id, test_case_id, raw_output, latency_ms),
    )
    conn.commit()
    return int(cur.lastrowid)


def insert_score(conn: sqlite3.Connection, output_id: int, scores: Dict[str, float]) -> None:
    conn.execute(
        """
        INSERT INTO scores (
            output_id, relevance_score, actionability_score, constraint_score, structure_score, aggregate_score, score_variance
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            output_id,
            scores["relevance_score"],
            scores["actionability_score"],
            scores["constraint_score"],
            scores["structure_score"],
            scores["aggregate_score"],
            scores["score_variance"],
        ),
    )
    conn.commit()


def insert_business_proxies(
    conn: sqlite3.Connection, run_id: int, acceptance_rate: float, rewrite_rate: float, clarification_rate: float
) -> None:
    conn.execute(
        """
        INSERT INTO business_proxies (run_id, acceptance_rate, rewrite_rate, clarification_rate)
        VALUES (?, ?, ?, ?)
        """,
        (run_id, acceptance_rate, rewrite_rate, clarification_rate),
    )
    conn.commit()


def insert_gate_decision(
    conn: sqlite3.Connection, baseline_run_id: int, candidate_run_id: int, decision: str, failed_checks_json: str, decision_note: str
) -> None:
    conn.execute(
        """
        INSERT INTO gate_decisions (baseline_run_id, candidate_run_id, decision, failed_checks_json, decision_note)
        VALUES (?, ?, ?, ?, ?)
        """,
        (baseline_run_id, candidate_run_id, decision, failed_checks_json, decision_note),
    )
    conn.commit()


def get_run_scores(conn: sqlite3.Connection, run_id: int) -> List[sqlite3.Row]:
    return list(
        conn.execute(
            """
            SELECT o.test_case_id, s.*
            FROM outputs o
            JOIN scores s ON s.output_id = o.output_id
            WHERE o.run_id = ?
            ORDER BY o.output_id ASC
            """,
            (run_id,),
        )
    )


def get_run_meta(conn: sqlite3.Connection, run_id: int) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
    if row is None:
        raise RuntimeError(f"Run {run_id} not found")
    return row


def get_latest_run_id(conn: sqlite3.Connection, run_type: str) -> int:
    row = conn.execute("SELECT run_id FROM runs WHERE run_type = ? ORDER BY run_id DESC LIMIT 1", (run_type,)).fetchone()
    if row is None:
        raise RuntimeError(f"No runs found for type={run_type}")
    return int(row["run_id"])


def get_business_proxy(conn: sqlite3.Connection, run_id: int) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT acceptance_rate, rewrite_rate, clarification_rate
        FROM business_proxies
        WHERE run_id = ?
        ORDER BY proxy_id DESC LIMIT 1
        """,
        (run_id,),
    ).fetchone()


def aggregate_scores(rows: Iterable[sqlite3.Row]) -> Dict[str, float]:
    data = list(rows)
    if not data:
        raise RuntimeError("No score rows to aggregate")
    n = float(len(data))
    return {
        "relevance_score": sum(r["relevance_score"] for r in data) / n,
        "actionability_score": sum(r["actionability_score"] for r in data) / n,
        "constraint_score": sum(r["constraint_score"] for r in data) / n,
        "structure_score": sum(r["structure_score"] for r in data) / n,
        "aggregate_score": sum(r["aggregate_score"] for r in data) / n,
        "score_variance": sum(r["score_variance"] for r in data) / n,
    }
