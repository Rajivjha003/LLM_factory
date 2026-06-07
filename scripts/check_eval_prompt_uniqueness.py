from __future__ import annotations

import argparse
import json
from difflib import SequenceMatcher
from pathlib import Path


def read_eval_dir(eval_dir: Path) -> list[dict]:
    rows = []

    for path in sorted(eval_dir.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    row = json.loads(line)
                    row["_file"] = str(path)
                    rows.append(row)

    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-dir", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--warn-threshold", type=float, default=0.82)
    parser.add_argument("--fail-threshold", type=float, default=0.92)
    args = parser.parse_args()

    rows = read_eval_dir(args.eval_dir)
    issues = []

    lines = [
        "# Eval Prompt Uniqueness Report",
        "",
        f"Eval dir: `{args.eval_dir}`",
        f"Samples: {len(rows)}",
        f"Warn threshold: {args.warn_threshold}",
        f"Fail threshold: {args.fail_threshold}",
        "",
        "| Prompt A | Prompt B | Similarity | Risk |",
        "|---|---|---:|---|",
    ]

    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a = rows[i]
            b = rows[j]
            sim = SequenceMatcher(None, a["prompt"], b["prompt"]).ratio()

            if sim >= args.warn_threshold:
                risk = "FAIL" if sim >= args.fail_threshold else "WARN"
                lines.append(f"| {a['id']} | {b['id']} | {sim:.3f} | {risk} |")

                if risk == "FAIL":
                    issues.append((a["id"], b["id"], sim))

    if len(lines) == 8:
        lines.append("| None | None | 0.000 | OK |")

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {args.output_md}")

    if issues:
        print("Near-duplicate eval prompts found:")
        for a, b, sim in issues:
            print(f"  {a} vs {b}: {sim:.3f}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
