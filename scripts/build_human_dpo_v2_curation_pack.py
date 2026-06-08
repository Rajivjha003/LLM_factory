from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def should_include(row: dict) -> bool:
    judge_v3_passed = bool(row.get("judge_v3_passed", row.get("passed", False)))
    sql_passed = bool(row.get("sql_verifier", {}).get("passed", False))
    human_review_required = bool(row.get("human_review_required", False))

    # Best candidates for DPO:
    # - failed under Judge v3
    # - SQL failed
    # - human review required
    return (not judge_v3_passed) or (not sql_passed) or human_review_required


def primary_issue(row: dict) -> str:
    if not row.get("sql_verifier", {}).get("passed", False):
        return "sql_verifier_failure"
    if row.get("human_review_required", False):
        return "judge_v2_false_negative_or_near_pass"
    if not row.get("judge_v3_passed", False):
        return "judge_v3_failure"
    return "quality_improvement_candidate"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge-v3-results", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--max-items", type=int, default=80)
    args = parser.parse_args()

    rows = read_jsonl(args.judge_v3_results)
    candidates = [row for row in rows if should_include(row)]

    # Prioritize real failures, then human-review-needed rows.
    candidates.sort(
        key=lambda row: (
            row.get("judge_v3_passed", False),
            row.get("sql_verifier", {}).get("passed", False),
            not row.get("human_review_required", False),
        )
    )

    candidates = candidates[: args.max_items]

    lines = [
        "# DPO v2 Human Curation Pack",
        "",
        "Fill the `CHOSEN_ANSWER` block manually. Do not leave it as placeholder.",
        "",
        "Rules for chosen answers:",
        "",
        "- Must be a full assistant answer, not a checklist.",
        "- Must answer the prompt directly.",
        "- Must include safe SQL if SQL is expected.",
        "- Must keep destructive commands out of executable SQL blocks.",
        "- Must include interpretation and next steps where useful.",
        "- Must be clearly better than the rejected answer.",
        "",
    ]

    for idx, row in enumerate(candidates, start=1):
        sample_id = row.get("id", f"candidate_{idx:04d}")
        issue = primary_issue(row)
        sql_feedback = row.get("sql_verifier", {}).get("feedback", [])
        judge_feedback = row.get("feedback", row.get("judge_v2", {}).get("feedback", []))

        lines.extend(
            [
                f"## Pair {idx}: {sample_id}",
                "",
                f"source_eval_id: {sample_id}",
                f"domain: {row.get('domain', 'unknown')}",
                f"primary_issue: {issue}",
                f"judge_v3_passed: {row.get('judge_v3_passed', False)}",
                f"sql_verifier_passed: {row.get('sql_verifier', {}).get('passed', False)}",
                f"human_review_required: {row.get('human_review_required', False)}",
                "",
                "### Prompt",
                "",
                "```text",
                row.get("prompt", ""),
                "```",
                "",
                "### Rejected Answer",
                "",
                "```text",
                row.get("response", ""),
                "```",
                "",
                "### Judge / SQL Feedback",
                "",
                "```text",
                f"judge_feedback: {judge_feedback}",
                f"sql_feedback: {sql_feedback}",
                "```",
                "",
                "### CHOSEN_ANSWER",
                "",
                "```text",
                "TODO_WRITE_FULL_CHOSEN_ANSWER_HERE",
                "```",
                "",
                "### Human Metadata",
                "",
                "```text",
                "human_pair_quality: pending",
                "human_notes: ",
                "```",
                "",
            ]
        )

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {len(candidates)} DPO curation candidates to {args.output_md}")

    if len(candidates) < 20:
        raise SystemExit("Too few candidates. Need at least 20 for DPO v2 curation.")


if __name__ == "__main__":
    main()
