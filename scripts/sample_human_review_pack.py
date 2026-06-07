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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-jsonl", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--sample-size", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rows = read_jsonl(args.eval_jsonl)
    random.seed(args.seed)

    failed = [row for row in rows if not row.get("passed", False)]
    passed = [row for row in rows if row.get("passed", False)]

    selected = []

    selected.extend(random.sample(passed, min(len(passed), args.sample_size // 2)))
    selected.extend(random.sample(failed, min(len(failed), args.sample_size - len(selected))))

    lines = [
        "# Human Review Pack",
        "",
        f"Eval file: `{args.eval_jsonl}`",
        f"Sample size: {len(selected)}",
        "",
        "For each sample, manually fill:",
        "",
        "```text",
        "human_correct: yes/no",
        "human_notes: ...",
        "judge_agree: yes/no",
        "```",
        "",
    ]

    for idx, row in enumerate(selected, start=1):
        lines.extend(
            [
                f"## Review {idx}: {row.get('id')}",
                "",
                f"- Domain: {row.get('domain')}",
                f"- Judge passed: {row.get('passed')}",
                f"- Judge score: {row.get('total_score')}/{row.get('max_score')}",
                f"- Judge feedback: {row.get('feedback', [])}",
                "",
                "### Prompt",
                "",
                "```text",
                row.get("prompt", ""),
                "```",
                "",
                "### Response",
                "",
                "```text",
                row.get("response", ""),
                "```",
                "",
                "### Manual Review",
                "",
                "```text",
                "human_correct:",
                "human_notes:",
                "judge_agree:",
                "```",
                "",
            ]
        )

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {args.output_md}")


if __name__ == "__main__":
    main()