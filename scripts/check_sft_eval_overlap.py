from __future__ import annotations

import argparse
import json
from difflib import SequenceMatcher
from pathlib import Path

def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def get_sft_user_text(row: dict) -> str:
    return "\n".join(
        m["content"] for m in row["messages"] if m["role"] == "user"
    )

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sft", type=Path, required=True)
    parser.add_argument("--eval-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    sft_rows = read_jsonl(args.sft)
    eval_rows = []
    for path in sorted(args.eval_dir.glob("*.jsonl")):
        eval_rows.extend(read_jsonl(path))

    lines = [
        "# SFT / Eval Overlap Report",
        "",
        "| Eval ID | Best SFT ID | Similarity | Risk |",
        "|---|---|---:|---|",
    ]

    for eval_row in eval_rows:
        eval_prompt = eval_row["prompt"]
        best = None

        for sft_row in sft_rows:
            sft_prompt = get_sft_user_text(sft_row)
            ratio = SequenceMatcher(None, eval_prompt, sft_prompt).ratio()
            if best is None or ratio > best[0]:
                best = (ratio, sft_row["id"])

        ratio, sft_id = best
        risk = "HIGH" if ratio >= 0.80 else "MEDIUM" if ratio >= 0.60 else "LOW"
        lines.append(
            f"| {eval_row['id']} | {sft_id} | {ratio:.3f} | {risk} |"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.output}")

if __name__ == "__main__":
    main()
