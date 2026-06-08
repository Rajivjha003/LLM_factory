from __future__ import annotations

import argparse
import json
from pathlib import Path

def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows

def summarize(path: Path) -> dict:
    rows = read_jsonl(path)
    total = len(rows)
    v2_pass = sum(1 for r in rows if r.get("passed_v2", False))
    v3_pass = sum(1 for r in rows if r.get("passed_v3", False))
    sql_pass = sum(1 for r in rows if "SQL verification passed." in r.get("sql_feedback", []))
    hr = sum(1 for r in rows if r.get("human_review_required", False))
    return {"file": str(path), "total": total, "v2_pass": v2_pass, "v3_pass": v3_pass, "sql_pass": sql_pass, "human_review_required": hr}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs", nargs="+", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    summaries = [summarize(p) for p in args.outputs]
    lines = ["# Judge v3 Model Matrix", "", "| Run | Total | V2 Pass | V3 Pass | SQL Pass | HR Needed |", "|---|---:|---:|---:|---:|---:|"]
    for s in summaries:
        lines.append(f"| `{s['file']}` | {s['total']} | {s['v2_pass']} | {s['v3_pass']} | {s['sql_pass']} | {s['human_review_required']} |")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.output_md}")

if __name__ == "__main__":
    main()
