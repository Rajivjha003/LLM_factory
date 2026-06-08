from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = {"id", "prompt", "chosen", "rejected", "system"}

def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if line.strip():
                row = json.loads(line)
                row["_line_no"] = line_no
                rows.append(row)
    return rows

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--min-count", type=int, default=20)
    args = parser.parse_args()
    rows = read_jsonl(args.path)
    errors = []
    if len(rows) < args.min_count:
        errors.append(f"Expected at least {args.min_count} rows, found {len(rows)}")
    ids = [r.get("id") for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate IDs found")
    for row in rows:
        line = row["_line_no"]
        missing = REQUIRED - set(row)
        if missing:
            errors.append(f"Line {line}: missing {missing}")
            continue
        if row["chosen"].strip() == row["rejected"].strip():
            errors.append(f"Line {line}: chosen and rejected are identical")
        if len(row["chosen"]) < 250:
            errors.append(f"Line {line}: chosen too short")
        if "```sql" in row["rejected"].lower() and "```sql" not in row["chosen"].lower():
            errors.append(f"Line {line}: rejected has SQL but chosen lacks SQL block")
        if "do not" not in row["chosen"].lower() and any(x in row["prompt"].lower() for x in ["delete", "drop", "truncate", "production"]):
            errors.append(f"Line {line}: safety prompt chosen answer lacks refusal/safety framing")
    print(f"DPO rows: {len(rows)}")
    print(f"Errors: {len(errors)}")
    if errors:
        for error in errors[:100]:
            print(f"- {error}")
        raise SystemExit(1)
    print("PASS: DPO dataset validated")

if __name__ == "__main__":
    main()
