from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read_jsonl(path: Path, required: bool = True) -> list[dict]:
    if not path.exists():
        if required:
            raise FileNotFoundError(path)
        return []

    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc

    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-sft", type=Path, required=True)
    parser.add_argument("--rubric-additions", type=Path, required=True)
    parser.add_argument("--real-additions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target-count", type=int, default=900)
    args = parser.parse_args()

    base_rows = read_jsonl(args.base_sft)
    rubric_rows = read_jsonl(args.rubric_additions)
    real_rows = read_jsonl(args.real_additions, required=False)

    combined = base_rows + rubric_rows + real_rows

    ids = [row["id"] for row in combined]
    duplicates = sorted({id_ for id_, count in Counter(ids).items() if count > 1})
    if duplicates:
        raise ValueError(f"Duplicate SFT IDs found: {duplicates[:20]}")

    if len(combined) < args.target_count:
        print(
            f"WARNING: target_count={args.target_count}, but only {len(combined)} rows available. "
            "Proceeding with available rows."
        )

    if len(combined) > args.target_count:
        combined = combined[: args.target_count]

    write_jsonl(args.output, combined)

    domain_counts = Counter(row.get("domain", "unknown") for row in combined)
    source_counts = Counter(row.get("source", "unknown") for row in combined)

    print(f"Wrote SFT v4: {args.output}")
    print(f"Rows: {len(combined)}")

    print("\nDomain counts:")
    for domain, count in domain_counts.most_common():
        print(f"  {domain}: {count}")

    print("\nSource counts:")
    for source, count in source_counts.most_common():
        print(f"  {source}: {count}")


if __name__ == "__main__":
    main()
