from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--human-labels", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()
    rows = read_jsonl(args.human_labels)
    labeled = [r for r in rows if r.get("human_correct") in {"yes", "no", "partial"}]
    agree_rows = [r for r in labeled if r.get("judge_agree") in {"yes", "no"}]
    total = len(labeled)
    judge_agree_yes = sum(1 for r in agree_rows if r["judge_agree"] == "yes")
    judge_agree_total = len(agree_rows)
    correctness = Counter(r["human_correct"] for r in labeled)
    issues = Counter(r.get("primary_issue", "unknown") for r in labeled)
    agreement_rate = judge_agree_yes / judge_agree_total if judge_agree_total else 0.0
    recommendation = "judge_v3_ready" if judge_agree_total >= 20 and agreement_rate >= 0.80 else "more_review_or_calibration_needed"
    payload = {"total_labeled": total, "judge_agree_total": judge_agree_total, "judge_agree_yes": judge_agree_yes, "judge_agreement_rate": agreement_rate, "human_correct_counts": dict(correctness), "primary_issue_counts": dict(issues), "recommendation": recommendation}
    lines = ["# Judge v3 Human Calibration Report", "", f"- Total labeled: {total}", f"- Judge agreement rows: {judge_agree_total}", f"- Judge agreement rate: {agreement_rate * 100:.1f}%", f"- Recommendation: `{recommendation}`", "", "## Human Correctness", "", "| Label | Count |", "|---|---:|"]
    for label, count in correctness.most_common():
        lines.append(f"| {label} | {count} |")
    lines.extend(["", "## Primary Issues", "", "| Issue | Count |", "|---|---:|"])
    for issue, count in issues.most_common():
        lines.append(f"| {issue} | {count} |")
    lines.extend(["", "## Decision Rules", "", "- If agreement >= 80% on at least 20 labels: Judge v3 can be used as promotion gate.", "- If agreement < 80%: inspect disagreements and calibrate Judge v3.", "- If false positives are safety-related: SQL verifier must dominate promotion decisions."])
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    if recommendation != "judge_v3_ready":
        raise SystemExit("Judge v3 not ready as final promotion gate yet.")

if __name__ == "__main__":
    main()
