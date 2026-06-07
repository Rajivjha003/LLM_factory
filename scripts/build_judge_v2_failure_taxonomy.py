from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
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


def classify(row: dict) -> list[str]:
    labels = []

    for field in CATEGORY_FIELDS:
        score = float(row.get(field, 1.0))
        if score < 1.0:
            labels.append(field.replace("_score", "_failure"))

    if not labels:
        labels.append("semantic_or_threshold_failure")

    return labels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-jsonl", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.eval_jsonl)
    failed = [row for row in rows if not row.get("passed", False)]

    counts = Counter()
    examples = defaultdict(list)

    for row in failed:
        labels = classify(row)

        for label in labels:
            counts[label] += 1
            if len(examples[label]) < 8:
                examples[label].append(row.get("id", row.get("sample_id", "unknown")))

    lines = [
        "# Judge v2 Failure Taxonomy",
        "",
        f"Eval file: `{args.eval_jsonl}`",
        f"Total samples: {len(rows)}",
        f"Failed samples: {len(failed)}",
        "",
        "| Failure Type | Count | Example IDs |",
        "|---|---:|---|",
    ]

    for label, count in counts.most_common():
        lines.append(f"| {label} | {count} | {', '.join(examples[label])} |")

    lines.extend(
        [
            "",
            "## Recommended Fix Mapping",
            "",
            "| Failure Type | Dataset Fix |",
            "|---|---|",
            "| required_terms_failure | Add examples that explicitly include required SQL/business concepts. |",
            "| forbidden_terms_failure | Add safety examples refusing destructive SQL and using preview/backup/validation. |",
            "| sql_block_failure | Add examples with clean fenced SQL blocks. |",
            "| normalization_failure | Add inventory/key examples using TRIM, UPPER, CAST, REGEXP_REPLACE. |",
            "| safety_failure | Add production-safe workflows. |",
            "| interpretation_failure | Add answer explanations that state what query output means. |",
            "| structure_failure | Add concise structured responses with diagnosis, query, interpretation, next step. |",
        ]
    )

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {args.output_md}")


if __name__ == "__main__":
    main()
