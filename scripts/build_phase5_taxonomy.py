from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from src.llm_lab.utils.config import load_yaml
from src.llm_lab.utils.io import read_jsonl, write_text


def classify(row: dict) -> list[str]:
    tags = []
    judge = row.get("judge", {})
    if row.get("missing_required"):
        tags.append("missing_required_terms")
    if row.get("forbidden_found"):
        tags.append("forbidden_sql_or_safety")
    if float(judge.get("sql_block_score", 0.0)) < 1.0:
        tags.append("missing_or_weak_sql_block")
    if float(judge.get("normalization_score", 0.0)) < 1.0:
        tags.append("missing_normalization_logic")
    if float(judge.get("interpretation_score", 0.0)) < 0.75:
        tags.append("weak_interpretation")
    if not tags:
        tags.append("near_miss_or_judge_threshold")
    return tags


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = load_yaml(args.config)
    run_name = cfg["run_name"]
    rows = read_jsonl(Path(cfg["paths"]["reports_dir"]) / f"{run_name}_eval_v3_judge_v2.jsonl")
    failures = [r for r in rows if not r.get("passed")]
    counter = Counter()
    per_sample = []
    for r in failures:
        tags = classify(r)
        counter.update(tags)
        per_sample.append((r.get("id"), tags, r.get("score"), r.get("missing_required"), r.get("forbidden_found")))

    lines = [
        f"# Phase 5 Failure Taxonomy: {run_name}",
        "",
        f"Total samples: {len(rows)}",
        f"Failures: {len(failures)}",
        "",
        "## Failure Class Counts",
        "",
    ]
    for tag, count in counter.most_common():
        lines.append(f"- `{tag}`: {count}")
    lines.extend(["", "## Per-Sample Failure Tags", ""])
    for sid, tags, score, missing, forbidden in per_sample:
        lines.append(f"### {sid}")
        lines.append(f"- Score: {score}")
        lines.append(f"- Tags: {', '.join(tags)}")
        lines.append(f"- Missing required: `{missing}`")
        lines.append(f"- Forbidden found: `{forbidden}`")
        lines.append("")

    out_path = Path(cfg["paths"]["taxonomy_dir"]) / f"{run_name}_eval_v3_taxonomy.md"
    write_text(out_path, "\n".join(lines))
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
