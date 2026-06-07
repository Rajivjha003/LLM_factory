from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def summarize(path: Path) -> dict:
    rows = read_jsonl(path)

    total = len(rows)
    passed = sum(1 for row in rows if row.get("passed", False))
    total_score = sum(float(row.get("total_score", row.get("score", 0))) for row in rows)
    max_score = sum(float(row.get("max_score", 0)) for row in rows)

    return {
        "file": str(path),
        "total": total,
        "passed": passed,
        "pass_rate": passed / total if total else 0.0,
        "total_score": total_score,
        "max_score": max_score,
        "score_rate": total_score / max_score if max_score else 0.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs", nargs="+", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summaries = [summarize(path) for path in args.outputs]

    lines = [
        "# Model Matrix v2",
        "",
        "| Run | Samples | Passed | Pass Rate | Score | Score Rate |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for item in summaries:
        lines.append(
            f"| `{item['file']}` | {item['total']} | {item['passed']} | "
            f"{item['pass_rate'] * 100:.1f}% | "
            f"{item['total_score']:.2f}/{item['max_score']:.2f} | "
            f"{item['score_rate'] * 100:.1f}% |"
        )

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {args.output_md}")


if __name__ == "__main__":
    main()
