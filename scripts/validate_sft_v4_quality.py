from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


REQUIRED_BY_DOMAIN = {
    "bigquery_debugging": ["```sql", "TRIM", "UPPER", "Interpretation"],
    "sql_generation": ["```sql"],
    "postgres_bq_reconciliation": ["TRIM", "UPPER", "Interpretation"],
    "retail_metric_reasoning": ["Interpretation"],
    "pipeline_debugging": ["Interpretation"],
    "safety_tool_use": ["validate"],
}

FORBIDDEN = ["DROP TABLE", "DELETE FROM", "TRUNCATE"]


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            row["_line_no"] = line_no
            rows.append(row)
    return rows


def assistant_text(row: dict) -> str:
    return "\n".join(
        message["content"]
        for message in row["messages"]
        if message["role"] == "assistant"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sft", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--min-count", type=int, default=800)
    args = parser.parse_args()

    rows = read_jsonl(args.sft)

    errors = []
    warnings = []

    domain_counts = Counter(row.get("domain", "unknown") for row in rows)
    source_counts = Counter(row.get("source", "unknown") for row in rows)

    if len(rows) < args.min_count:
        warnings.append(f"SFT has {len(rows)} rows, below recommended minimum {args.min_count}")

    ids = [row["id"] for row in rows]
    duplicate_ids = sorted({id_ for id_ in ids if ids.count(id_) > 1})
    if duplicate_ids:
        errors.append(f"Duplicate IDs found: {duplicate_ids[:20]}")

    for row in rows:
        line_no = row["_line_no"]
        domain = row.get("domain", "unknown")
        text = assistant_text(row)
        upper_text = text.upper()

        if not text.strip():
            errors.append(f"Line {line_no}: empty assistant response")

        if len(text) < 250:
            warnings.append(f"Line {line_no}: assistant response may be too short")

        for forbidden in FORBIDDEN:
            if forbidden in upper_text:
                lower_text = text.lower()
                if "do not" not in lower_text and "avoid" not in lower_text and "never" not in lower_text:
                    errors.append(
                        f"Line {line_no}: unsafe forbidden SQL term not framed as refusal: {forbidden}"
                    )

        required_terms = REQUIRED_BY_DOMAIN.get(domain, [])
        for term in required_terms:
            if term.lower() not in text.lower():
                warnings.append(f"Line {line_no}: missing recommended term for {domain}: {term}")

    lines = [
        "# SFT v4 Quality Report",
        "",
        f"Rows: {len(rows)}",
        "",
        "## Domain Counts",
        "",
        "| Domain | Count |",
        "|---|---:|",
    ]

    for domain, count in domain_counts.most_common():
        lines.append(f"| {domain} | {count} |")

    lines.extend(
        [
            "",
            "## Source Counts",
            "",
            "| Source | Count |",
            "|---|---:|",
        ]
    )

    for source, count in source_counts.most_common():
        lines.append(f"| {source} | {count} |")

    lines.extend(["", "## Errors", ""])

    if errors:
        for error in errors:
            lines.append(f"- {error}")
    else:
        lines.append("- None")

    lines.extend(["", "## Warnings", ""])

    if warnings:
        for warning in warnings[:300]:
            lines.append(f"- {warning}")
        if len(warnings) > 300:
            lines.append(f"- ... truncated {len(warnings) - 300} more warnings")
    else:
        lines.append("- None")

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {args.output_md}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
