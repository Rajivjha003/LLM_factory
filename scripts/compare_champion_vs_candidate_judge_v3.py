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


def summarize(path: Path) -> dict:
    rows = read_jsonl(path)
    total = len(rows)

    return {
        "path": str(path),
        "total": total,
        "v2_pass": sum(1 for row in rows if row.get("passed_v2", False)),
        "v3_pass": sum(1 for row in rows if row.get("passed_v3", False)),
        "sql_pass": sum(1 for row in rows if "SQL verification passed." in row.get("sql_feedback", [])),
        "hr_needed": sum(1 for row in rows if row.get("human_review_required", False)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--champion", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--candidate-name", required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()

    champ = summarize(args.champion)
    cand = summarize(args.candidate)

    promotion = (
        (cand["v3_pass"] > champ["v3_pass"] or cand["sql_pass"] > champ["sql_pass"])
        and cand["sql_pass"] >= champ["sql_pass"]
        and cand["hr_needed"] <= champ["hr_needed"] + 3
    )

    decision = "PROMOTE" if promotion else "REJECT"

    payload = {
        "champion": champ,
        "candidate": cand,
        "candidate_name": args.candidate_name,
        "decision": decision,
        "promotion": promotion,
        "rules": {
            "must_beat_v3_or_sql": True,
            "must_not_regress_sql": True,
            "hr_needed_tolerance": 3,
        },
    }

    lines = [
        "# Candidate Promotion Report",
        "",
        f"Candidate: `{args.candidate_name}`",
        f"Decision: **{decision}**",
        "",
        "| Model | Total | V2 Pass | V3 Pass | SQL Pass | HR Needed |",
        "|---|---:|---:|---:|---:|---:|",
        f"| Champion | {champ['total']} | {champ['v2_pass']} | {champ['v3_pass']} | {champ['sql_pass']} | {champ['hr_needed']} |",
        f"| Candidate | {cand['total']} | {cand['v2_pass']} | {cand['v3_pass']} | {cand['sql_pass']} | {cand['hr_needed']} |",
        "",
        "## Rule",
        "",
        "Candidate promotes only if it beats champion on Judge v3 or SQL pass, without SQL safety regression.",
    ]

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(json.dumps(payload, indent=2))

    if not promotion:
        raise SystemExit("Candidate rejected by promotion gate.")


if __name__ == "__main__":
    main()
