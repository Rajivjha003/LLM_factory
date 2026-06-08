from __future__ import annotations

import argparse
from pathlib import Path
import random
import numpy as np
from src.llm_lab.utils.config import load_yaml
from src.llm_lab.utils.io import read_jsonl, write_json


def bootstrap(values: list[float], n: int = 10000, seed: int = 42) -> dict[str, float]:
    rng = random.Random(seed)
    arr = np.array(values, dtype=float)
    means = []
    for _ in range(n):
        idx = [rng.randrange(len(arr)) for _ in range(len(arr))]
        means.append(float(arr[idx].mean()))
    return {
        "mean": round(float(arr.mean()), 4),
        "ci_95_low": round(float(np.percentile(means, 2.5)), 4),
        "ci_95_high": round(float(np.percentile(means, 97.5)), 4),
        "bootstrap_samples": n,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = load_yaml(args.config)
    run_name = cfg["run_name"]
    rows = read_jsonl(Path(cfg["paths"]["reports_dir"]) / f"{run_name}_eval_v3_judge_v2.jsonl")
    pass_values = [1.0 if r.get("passed") else 0.0 for r in rows]
    score_values = [float(r.get("score", 0.0)) for r in rows]

    confidence = {
        "run_name": run_name,
        "pass_rate": bootstrap(pass_values, seed=int(cfg.get("seed", 42))),
        "score_rate": bootstrap(score_values, seed=int(cfg.get("seed", 42)) + 1),
    }
    out_path = Path(cfg["paths"]["truth_audit_dir"]) / f"{run_name}_eval_v3_confidence.json"
    write_json(out_path, confidence)
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
