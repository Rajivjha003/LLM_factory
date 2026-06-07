from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--additions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=300)
    args = parser.parse_args()

    base_rows = read_jsonl(args.base)
    addition_rows = read_jsonl(args.additions)

    combined = base_rows + addition_rows

    seen = set()
    duplicates = []
    for row in combined:
        if row["id"] in seen:
            duplicates.append(row["id"])
        seen.add(row["id"])

    if duplicates:
        raise ValueError(f"Duplicate SFT ids: {duplicates[:20]}")

    if len(combined) != args.expected_count:
        raise ValueError(
            f"Expected {args.expected_count} rows, got {len(combined)}. "
            f"Base={len(base_rows)}, additions={len(addition_rows)}"
        )

    domain_counts = Counter(row.get("domain", "unknown") for row in combined)

    write_jsonl(args.output, combined)

    print(f"Wrote {len(combined)} rows to {args.output}")
    print("Domain counts:")
    for domain, count in domain_counts.most_common():
        print(f"  {domain}: {count}")


if __name__ == "__main__":
    main()
