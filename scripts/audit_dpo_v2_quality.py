from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.path)

    domain_counts = Counter(row.get("domain", "unknown") for row in rows)
    quality_counts = Counter(row.get("human_pair_quality", "unknown") for row in rows)

    sql_chosen = sum(1 for row in rows if "```sql" in row.get("chosen", "").lower())
    interpretation = sum(1 for row in rows if "interpretation" in row.get("chosen", "").lower())
    safety = sum(1 for row in rows if any(term in row.get("chosen", "").lower() for term in ["do not", "avoid", "never", "preview", "backup", "validate"]))

    lines = [
        "# DPO v2 Quality Report",
        "",
        f"- Total pairs: {len(rows)}",
        f"- Chosen answers with SQL blocks: {sql_chosen}",
        f"- Chosen answers with Interpretation: {interpretation}",
        f"- Chosen answers with safety language: {safety}",
        "",
        "## Domain Counts",
        "",
        "| Domain | Count |",
        "|---|---:|",
    ]

    for domain, count in domain_counts.most_common():
        lines.append(f"| {domain} | {count} |")

    lines.extend(["", "## Human Pair Quality Counts", "", "| Quality | Count |", "|---|---:|"])

    for quality, count in quality_counts.most_common():
        lines.append(f"| {quality} | {count} |")

    lines.extend(
        [
            "",
            "## Recommended Gates",
            "",
            "- At least 40 pairs for DPO v2.",
            "- At least 60% of SQL-like prompts should have SQL blocks in chosen answers.",
            "- Chosen answers must be complete assistant answers, not rubric notes.",
            "- Destructive SQL must not appear inside executable SQL blocks.",
        ]
    )

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.output_md}")


if __name__ == "__main__":
    main()
