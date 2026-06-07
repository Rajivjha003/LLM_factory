from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def summarize_eval_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    passed = sum(1 for row in rows if row.get("passed"))
    total_score = sum(float(row.get("total_score", row.get("score", 0))) for row in rows)
    max_score = sum(float(row.get("max_score", 0)) for row in rows)

    by_domain: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"total": 0, "passed": 0, "score": 0.0, "max_score": 0.0}
    )

    for row in rows:
        domain = row.get("domain", "unknown")
        by_domain[domain]["total"] += 1
        by_domain[domain]["passed"] += 1 if row.get("passed") else 0
        by_domain[domain]["score"] += float(row.get("total_score", row.get("score", 0)))
        by_domain[domain]["max_score"] += float(row.get("max_score", 0))

    domain_summary = {}

    for domain, values in by_domain.items():
        domain_summary[domain] = {
            **values,
            "pass_rate": values["passed"] / values["total"] if values["total"] else 0.0,
            "score_rate": values["score"] / values["max_score"] if values["max_score"] else 0.0,
        }

    return {
        "total": total,
        "passed": passed,
        "pass_rate": passed / total if total else 0.0,
        "total_score": total_score,
        "max_score": max_score,
        "score_rate": total_score / max_score if max_score else 0.0,
        "domain_summary": domain_summary,
    }


def write_eval_markdown(path: Path, rows: list[dict[str, Any]], metadata: dict[str, Any]) -> None:
    summary = summarize_eval_rows(rows)

    lines = [
        "# Evaluation Report",
        "",
        "## Summary",
        "",
        f"- Total samples: {summary['total']}",
        f"- Passed: {summary['passed']}/{summary['total']}",
        f"- Pass rate: {summary['pass_rate'] * 100:.1f}%",
        f"- Score: {summary['total_score']:.2f}/{summary['max_score']:.2f}",
        f"- Score rate: {summary['score_rate'] * 100:.1f}%",
        "",
        "## Metadata",
        "",
        "```json",
        json.dumps(metadata, indent=2, ensure_ascii=False),
        "```",
        "",
        "## Domain Summary",
        "",
        "| Domain | Total | Passed | Pass Rate | Score Rate |",
        "|---|---:|---:|---:|---:|",
    ]

    for domain, item in summary["domain_summary"].items():
        lines.append(
            f"| {domain} | {item['total']} | {item['passed']} | "
            f"{item['pass_rate'] * 100:.1f}% | {item['score_rate'] * 100:.1f}% |"
        )

    lines.extend(["", "## Sample Results", ""])

    for row in rows:
        lines.extend(
            [
                f"### {row.get('id', row.get('sample_id', 'unknown'))}",
                "",
                f"- Domain: {row.get('domain')}",
                f"- Passed: {row.get('passed')}",
                f"- Score: {row.get('total_score', row.get('score'))}/{row.get('max_score')}",
                f"- Score rate: {float(row.get('score_rate', 0.0)) * 100:.1f}%",
                f"- Missing required: {row.get('missing_required', [])}",
                f"- Forbidden found: {row.get('forbidden_found', [])}",
                f"- Feedback: {row.get('feedback', [])}",
                "",
                "Prompt:",
                "",
                "```text",
                row.get("prompt", ""),
                "```",
                "",
                "Response:",
                "",
                "```text",
                row.get("response", ""),
                "```",
                "",
            ]
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
