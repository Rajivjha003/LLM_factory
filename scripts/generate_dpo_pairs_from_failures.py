from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    rows = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_chosen(row: dict) -> str:
    prompt = row.get("prompt", "")
    missing = row.get("missing_required", []) or []

    required_hint = ", ".join(missing) if missing else "the required validation concepts"

    return (
        "Treat this as a safe data-engineering diagnosis. First identify the grain, "
        "then provide read-only SQL, then explain how to interpret the output.\n\n"
        f"The answer must include: {required_hint}.\n\n"
        "Use normalized keys where relevant with `TRIM`, `UPPER`, and `CAST`. "
        "For reconciliation, prefer `EXCEPT DISTINCT` or a left anti-join. "
        "For duplicates, use `GROUP BY` with `HAVING COUNT(*) > 1`. "
        "For production tables, do not use destructive SQL; use preview, backup, and validation."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-jsonl", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.eval_jsonl)

    pairs = []

    for row in rows:
        if row.get("passed", False):
            continue

        prompt = row.get("prompt", "")
        rejected = row.get("response", "")

        if not prompt or not rejected:
            continue

        pairs.append(
            {
                "id": f"dpo_from_failure_{row.get('id', len(pairs))}",
                "prompt": prompt,
                "chosen": build_chosen(row),
                "rejected": rejected,
                "source": "eval_failure",
                "domain": row.get("domain", "unknown"),
            }
        )

    write_jsonl(args.output, pairs)
    print(f"Wrote {len(pairs)} DPO pairs to {args.output}")


if __name__ == "__main__":
    main()
