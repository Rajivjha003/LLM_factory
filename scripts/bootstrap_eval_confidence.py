from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    rows = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    return rows


def summarize(rows: list[dict]) -> dict:
    total = len(rows)
    passed = sum(1 for row in rows if row.get("passed", False))
    total_score = sum(float(row.get("total_score", row.get("score", 0.0))) for row in rows)
    max_score = sum(float(row.get("max_score", 0.0)) for row in rows)

    return {
        "pass_rate": passed / total if total else 0.0,
        "score_rate": total_score / max_score if max_score else 0.0,
    }


def percentile(values: list[float], p: float) -> float:
    values = sorted(values)
    if not values:
        return 0.0

    k = (len(values) - 1) * p
    lower = int(k)
    upper = min(lower + 1, len(values) - 1)
    weight = k - lower

    return values[lower] * (1 - weight) + values[upper] * weight


def bootstrap(rows: list[dict], n: int, seed: int) -> dict:
    random.seed(seed)

    pass_rates = []
    score_rates = []

    for _ in range(n):
        sample = [random.choice(rows) for _ in rows]
        summary = summarize(sample)
        pass_rates.append(summary["pass_rate"])
        score_rates.append(summary["score_rate"])

    base = summarize(rows)

    return {
        "base_pass_rate": base["pass_rate"],
        "base_score_rate": base["score_rate"],
        "pass_rate_ci_95": [percentile(pass_rates, 0.025), percentile(pass_rates, 0.975)],
        "score_rate_ci_95": [percentile(score_rates, 0.025), percentile(score_rates, 0.975)],
        "bootstrap_samples": n,
        "seed": seed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-jsonl", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rows = read_jsonl(args.eval_jsonl)
    result = bootstrap(rows, n=args.samples, seed=args.seed)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
