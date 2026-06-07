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
    parser.add_argument("--fail-threshold", type=float, default=0.80)
    args = parser.parse_args()

    sft_rows = read_jsonl(args.sft)
    eval_rows = []
    for path in sorted(args.eval_dir.glob("*.jsonl")):
        eval_rows.extend(read_jsonl(path))

    high_risk = []
    lines = [
        "# SFT / Eval Overlap Strict Report",
        "",
        f"Fail threshold: {args.fail_threshold}",
        "",
        "| Eval ID | Best SFT ID | Similarity | Risk |",
        "|---|---|---:|---|",
    ]

    for eval_row in eval_rows:
        eval_prompt = eval_row["prompt"]
        best_ratio = -1.0
        best_sft_id = None

        for sft_row in sft_rows:
            sft_prompt = get_sft_user_text(sft_row)
            ratio = SequenceMatcher(None, eval_prompt, sft_prompt).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_sft_id = sft_row["id"]

        risk = "LOW"
        if best_ratio >= 0.8:
            risk = "HIGH"
            high_risk.append((eval_row["id"], best_sft_id, best_ratio))
        elif best_ratio >= 0.6:
            risk = "MEDIUM"

        lines.append(f"| {eval_row['id']} | {best_sft_id} | {best_ratio:.3f} | {risk} |")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    
    print(f"Saved strict overlap report to {args.output}")

    if high_risk:
        print("\nFATAL ERROR: High overlap detected between Eval and SFT!")
        for e_id, s_id, ratio in high_risk:
            print(f"  {e_id} <-> {s_id} (Ratio: {ratio:.3f})")
        raise SystemExit(1)
        
    print("PASS: No strict data contamination detected.")

if __name__ == "__main__":
    main()
