from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = {"id", "prompt", "chosen", "rejected", "system"}


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            if line.strip():
                row = json.loads(line)
                row["_line_no"] = line_no
                rows.append(row)
    return rows


def has_destructive_inside_sql(text: str) -> bool:
    lower = text.lower()
    blocks = []
    parts = lower.split("```")
    for i in range(1, len(parts), 2):
        blocks.append(parts[i])
    return any(term in block for block in blocks for term in ["drop table", "delete from", "truncate"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--min-count", type=int, default=40)
    args = parser.parse_args()

    rows = read_jsonl(args.path)
    errors = []
    warnings = []

    if len(rows) < args.min_count:
        errors.append(f"Expected at least {args.min_count} rows, found {len(rows)}")

    ids = [row.get("id") for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate IDs found")

    prompts = [row.get("prompt", "").strip() for row in rows]
    if len(prompts) != len(set(prompts)):
        warnings.append("Duplicate prompts found. Inspect whether they are intentional.")

    for row in rows:
        line = row["_line_no"]
        missing = REQUIRED - set(row)
        if missing:
            errors.append(f"Line {line}: missing required fields: {sorted(missing)}")
            continue

        prompt = row["prompt"].strip()
        chosen = row["chosen"].strip()
        rejected = row["rejected"].strip()

        if not prompt:
            errors.append(f"Line {line}: empty prompt")

        if len(chosen) < 300:
            errors.append(f"Line {line}: chosen answer too short")

        if chosen == rejected:
            errors.append(f"Line {line}: chosen and rejected are identical")

        if "TODO" in chosen:
            errors.append(f"Line {line}: chosen still contains TODO")

        if "```sql" in rejected.lower() and "```sql" not in chosen.lower():
            warnings.append(f"Line {line}: rejected has SQL but chosen does not")

        if has_destructive_inside_sql(chosen):
            errors.append(f"Line {line}: chosen has destructive SQL inside executable SQL block")

        safety_prompt = any(term in prompt.lower() for term in ["delete", "drop", "truncate", "production"])
        if safety_prompt and not any(term in chosen.lower() for term in ["do not", "avoid", "never", "preview", "backup", "validate"]):
            errors.append(f"Line {line}: safety prompt lacks safety framing")

        if "interpretation" not in chosen.lower() and "sql" in chosen.lower():
            warnings.append(f"Line {line}: SQL answer lacks explicit Interpretation block")

    print(f"DPO v2 rows: {len(rows)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings[:50]:
            print(f"- {warning}")

    if errors:
        print("\nErrors:")
        for error in errors[:100]:
            print(f"- {error}")
        raise SystemExit(1)

    print("PASS: DPO v2 dataset validated")


if __name__ == "__main__":
    main()
