from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import load_config
from src.db import connect, init_db
from src.eval_runner import run_evaluation


def main() -> None:
    config = load_config()
    conn = connect(config.db_path)
    init_db(conn)
    run_id = run_evaluation(conn, config, run_type="baseline", prompt_version=config.baseline_prompt_version)
    print(f"Baseline run complete. run_id={run_id}")


if __name__ == "__main__":
    main()
