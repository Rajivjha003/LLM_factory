from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = {
    "id",
    "domain",
    "prompt",
    "response",
    "passed",
    "total_score",
    "max_score",
    "score_rate",
    "required_terms_score",
    "forbidden_terms_score",
    "sql_block_score",
    "normalization_score",
    "safety_score",
    "interpretation_score",
    "structure_score",
}


def read_jsonl(path: Path) -> list[dict]:
    rows = []

    with path.open("r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc

            row["_line_no"] = line_no
            rows.append(row)

    return rows


def audit_rows(rows: list[dict]) -> dict:
    errors = []
    warnings = []

    if not rows:
        errors.append("No rows found in eval result.")

    ids = []
    pass_count = 0
    total_score = 0.0
    max_score = 0.0

    for row in rows:
        line_no = row.get("_line_no", "?")
        missing = REQUIRED_FIELDS - set(row)

        if missing:
            errors.append(f"Line {line_no}: missing fields: {sorted(missing)}")

        ids.append(row.get("id"))

        passed = row.get("passed")
        if not isinstance(passed, bool):
            errors.append(f"Line {line_no}: passed must be bool, got {type(passed)}")

        if passed is True:
            pass_count += 1

        try:
            row_total = float(row.get("total_score", 0.0))
            row_max = float(row.get("max_score", 0.0))
            row_rate = float(row.get("score_rate", 0.0))
        except Exception:
            errors.append(f"Line {line_no}: score fields are not numeric")
            continue

        if row_max <= 0:
            errors.append(f"Line {line_no}: max_score must be positive")

        if row_total < 0:
            errors.append(f"Line {line_no}: total_score cannot be negative")

        if row_total > row_max + 1e-6:
            errors.append(f"Line {line_no}: total_score exceeds max_score")

        expected_rate = row_total / row_max if row_max else 0.0
        if abs(expected_rate - row_rate) > 0.01:
            errors.append(
                f"Line {line_no}: score_rate mismatch. "
                f"found={row_rate}, expected={expected_rate:.4f}"
            )

        if row.get("forbidden_found") and row.get("forbidden_terms_score", 1.0) != 0.0:
            errors.append(
                f"Line {line_no}: forbidden_found exists but forbidden_terms_score is not 0"
            )

        if passed and row.get("forbidden_found"):
            errors.append(f"Line {line_no}: passed=True but forbidden terms found")

        if passed and row_rate < 0.70:
            warnings.append(f"Line {line_no}: passed=True with low score_rate={row_rate}")

        total_score += row_total
        max_score += row_max

    duplicate_ids = sorted({id_ for id_ in ids if ids.count(id_) > 1 and id_ is not None})
    if duplicate_ids:
        errors.append(f"Duplicate result ids: {duplicate_ids}")

    total = len(rows)
    pass_rate = pass_count / total if total else 0.0
    score_rate = total_score / max_score if max_score else 0.0

    return {
        "total": total,
        "passed": pass_count,
        "pass_rate": pass_rate,
        "total_score": total_score,
        "max_score": max_score,
        "score_rate": score_rate,
        "errors": errors,
        "warnings": warnings,
        "audit_passed": len(errors) == 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-jsonl", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.eval_jsonl)
    audit = audit_rows(rows)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(audit, indent=2), encoding="utf-8")

    print(json.dumps(audit, indent=2))

    if not audit["audit_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
