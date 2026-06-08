from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

VALID_HUMAN = {"yes", "no", "partial"}
VALID_AGREE = {"yes", "no"}

def normalize(value: str) -> str:
    return value.strip().lower().replace("[", "").replace("]", "").strip()

def parse_review_blocks(text: str) -> list[dict]:
    parts = re.split(r"\n### \d+\. ID:\s+", text)
    rows: list[dict] = []
    for part in parts[1:]:
        first_line, _, body = part.partition("\n")
        sample_id = first_line.split(" ")[0].strip()
        model = "qwen_1_5b_sft_v2" # Default since it's the champion we evaluated
        human_match = re.search(r"human_correct:\s*([A-Za-z]+)", body)
        agree_match = re.search(r"judge_agree:\s*([A-Za-z]+)", body)
        issue_match = re.search(r"primary_issue:\s*([A-Za-z0-9_\-]+)", body)
        notes_match = re.search(r"human_notes:\s*(.*)", body)
        human_correct = normalize(human_match.group(1)) if human_match else ""
        judge_agree = normalize(agree_match.group(1)) if agree_match else ""
        primary_issue = normalize(issue_match.group(1)) if issue_match else "unlabeled"
        notes = notes_match.group(1).strip() if notes_match else ""
        if human_correct not in VALID_HUMAN:
            human_correct = "unlabeled"
        if judge_agree not in VALID_AGREE:
            judge_agree = "unlabeled"
        rows.append({"id": sample_id, "model": model, "human_correct": human_correct, "judge_agree": judge_agree, "primary_issue": primary_issue, "notes": notes})
    return rows

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    text = args.input.read_text(encoding="utf-8")
    rows = parse_review_blocks(text)
    labeled = [r for r in rows if r["human_correct"] != "unlabeled"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for row in labeled:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Parsed reviews: {len(rows)}")
    print(f"Labeled reviews written: {len(labeled)}")
    print(f"Output: {args.output}")
    if len(labeled) < 20:
        raise SystemExit("Need at least 20 labeled human review rows before proceeding.")

if __name__ == "__main__":
    main()
