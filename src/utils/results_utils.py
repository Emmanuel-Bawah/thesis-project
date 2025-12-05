import json
from pathlib import Path
from datetime import datetime
import pandas as pd


def create_run_id(run_index: int = 1) -> str:
    date_str = datetime.now().strftime("%Y_%m_%d")
    return f"run_{date_str}_{run_index:02d}"


def get_run_paths(run_id: str):
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    csv_path = results_dir / f"{run_id}.csv"
    json_path = results_dir / f"{run_id}_summary.json"

    return csv_path, json_path


def save_run_csv(run_id: str, rows: list[dict]):
    csv_path, _ = get_run_paths(run_id)
    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV: {csv_path}")


def save_run_summary(run_id: str, seed: int, notes: str = "", config_file: str = "configs/config.yaml"):
    _, json_path = get_run_paths(run_id)

    summary = {
        "run_id": run_id,
        "config_file": config_file,
        "seed": seed,
        "notes": notes,
    }

    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Saved summary: {json_path}")
