from __future__ import annotations

import argparse
import json
from pathlib import Path


CATEGORY_FIELDS = [
    "required_terms_score",
    "forbidden_terms_score",
    "sql_block_score",
    "normalization_score",
    "safety_score",
    "interpretation_score",
    "structure_score",
]


def read_jsonl(path: Path) -> list[dict]:
    rows = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-jsonl", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.eval_jsonl)

    lines = [
        "# Judge v2 Threshold Audit",
        "",
        f"Eval file: `{args.eval_jsonl}`",
        f"Rows: {len(rows)}",
        "",
        "## Category Averages",
        "",
        "| Category | Average | Min | Max | Perfect Count |",
        "|---|---:|---:|---:|---:|",
    ]

    for field in CATEGORY_FIELDS:
        values = [float(row.get(field, 0.0)) for row in rows]
        avg = sum(values) / len(values) if values else 0.0
        perfect = sum(1 for value in values if value >= 1.0)

        lines.append(
            f"| {field} | {avg:.3f} | {min(values):.3f} | {max(values):.3f} | {perfect}/{len(values)} |"
        )

    near_pass = [
        row for row in rows
        if not row.get("passed", False) and float(row.get("score_rate", 0.0)) >= 0.90
    ]

    low_score_pass = [
        row for row in rows
        if row.get("passed", False) and float(row.get("score_rate", 0.0)) < 0.80
    ]

    lines.extend(
        [
            "",
            "## Suspicious Cases",
            "",
            f"- Failed but score_rate >= 0.90: {len(near_pass)}",
            f"- Passed but score_rate < 0.80: {len(low_score_pass)}",
            "",
            "### Failed But Near Perfect",
            "",
            "| ID | Score Rate | Missing Required | Feedback |",
            "|---|---:|---|---|",
        ]
    )

    for row in near_pass[:20]:
        lines.append(
            f"| {row.get('id')} | {float(row.get('score_rate', 0.0)):.3f} | "
            f"{row.get('missing_required', [])} | {row.get('feedback', [])} |"
        )

    lines.extend(
        [
            "",
            "### Passed But Low Score",
            "",
            "| ID | Score Rate | Feedback |",
            "|---|---:|---|",
        ]
    )

    for row in low_score_pass[:20]:
        lines.append(
            f"| {row.get('id')} | {float(row.get('score_rate', 0.0)):.3f} | {row.get('feedback', [])} |"
        )

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {args.output_md}")


if __name__ == "__main__":
    main()
