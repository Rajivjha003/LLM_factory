import json
from pathlib import Path
from collections import defaultdict


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def analyze_results(model_name: str, path: Path) -> dict:
    rows = read_jsonl(path)
    if not rows:
        return {"model": model_name, "error": "File not found"}

    total = len(rows)
    passed_v2 = sum(1 for r in rows if r.get("passed_v2"))
    passed_v3 = sum(1 for r in rows if r.get("passed_v3"))
    passed_sql = sum(1 for r in rows if "SQL verification passed." in r.get("sql_feedback", []))
    hr_required = sum(1 for r in rows if r.get("human_review_required"))

    return {
        "model": model_name,
        "total": total,
        "passed_v2": passed_v2,
        "passed_v3": passed_v3,
        "passed_sql": passed_sql,
        "hr_required": hr_required,
    }


def main():
    reports_dir = Path("reports/eval_reports")
    
    models = [
        ("SFT v2 (Champion)", reports_dir / "qwen_1_5b_sft_v2_eval_v3_judge_v3.jsonl"),
        ("SFT v4b", reports_dir / "qwen_1_5b_sft_v4b_eval_v3_judge_v3.jsonl"),
    ]

    print("Judge v3 Evaluation Matrix")
    print("-" * 100)
    print(f"{'Model':<20} | {'Total':<6} | {'V2 Pass':<8} | {'V3 Pass':<8} | {'SQL Pass':<10} | {'HR Needed':<10}")
    print("-" * 100)

    for name, path in models:
        stats = analyze_results(name, path)
        if "error" in stats:
            print(f"{stats['model']:<20} | {stats['error']}")
        else:
            print(f"{stats['model']:<20} | {stats['total']:<6} | {stats['passed_v2']:<8} | {stats['passed_v3']:<8} | {stats['passed_sql']:<10} | {stats['hr_required']:<10}")

if __name__ == "__main__":
    main()
