from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

class EvalSample(BaseModel):
    id: str = Field(min_length=3)
    domain: str = Field(min_length=2)
    difficulty: str
    prompt: str = Field(min_length=5)
    expected_traits: list[str] = Field(default_factory=list)
    must_include: list[str] = Field(default_factory=list)
    must_not_include: list[str] = Field(default_factory=list)
    max_score: int = Field(default=3, ge=1, le=10)

def iter_jsonl_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(path.glob("*.jsonl"))

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-dir", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=None)
    args = parser.parse_args()

    errors: list[str] = []
    ids: list[str] = []
    domains: Counter[str] = Counter()
    total = 0

    for file_path in iter_jsonl_files(args.eval_dir):
        with file_path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                total += 1

                try:
                    row = json.loads(line)
                    sample = EvalSample.model_validate(row)
                except (json.JSONDecodeError, ValidationError) as exc:
                    errors.append(f"{file_path}:{line_no}: {exc}")
                    continue

                ids.append(sample.id)
                domains[sample.domain] += 1

                forbidden_upper = [x.upper() for x in sample.must_not_include]
                for destructive in ["DROP TABLE", "DELETE FROM", "TRUNCATE"]:
                    if destructive not in forbidden_upper:
                        errors.append(
                            f"{file_path}:{line_no}: missing destructive guard {destructive}"
                        )

    duplicates = [item for item, count in Counter(ids).items() if count > 1]
    for duplicate in duplicates:
        errors.append(f"duplicate eval id: {duplicate}")

    if args.expected_count is not None and total != args.expected_count:
        errors.append(f"expected {args.expected_count} samples, found {total}")

    print(f"Total eval samples: {total}")
    print("Domain counts:")
    for domain, count in domains.most_common():
        print(f"  {domain}: {count}")

    if errors:
        print("\nERRORS:")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)

    print("PASS: eval data validated")

if __name__ == "__main__":
    main()
