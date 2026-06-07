from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add src to sys path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pydantic import ValidationError

from llm_ops.data.sft_schemas import SFTSample


FORBIDDEN_ASSISTANT_TERMS = [
    "DROP TABLE",
    "TRUNCATE TABLE",
    "DELETE FROM",
]


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []

    with path.open("r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_no}: {exc}") from exc

    return rows


def validate_sft_file(path: Path) -> tuple[int, list[str]]:
    rows = load_jsonl(path)

    if not rows:
        return 0, [f"No samples found in {path}"]

    seen_ids: set[str] = set()
    errors: list[str] = []

    for idx, row in enumerate(rows, start=1):
        try:
            sample = SFTSample.model_validate(row)
        except ValidationError as exc:
            errors.append(f"Line {idx}: schema error: {exc}")
            continue

        if sample.id in seen_ids:
            errors.append(f"Line {idx}: duplicate id {sample.id}")
        seen_ids.add(sample.id)

        assistant_text = "\n".join(
            message.content.upper()
            for message in sample.messages
            if message.role == "assistant"
        )

        for term in FORBIDDEN_ASSISTANT_TERMS:
            if term in assistant_text:
                errors.append(
                    f"Line {idx}: forbidden destructive SQL term found: {term}"
                )

    return len(rows), errors

def validate_file(path: Path) -> None:
    valid_count, errors = validate_sft_file(path)
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print(f"PASS: {valid_count} SFT samples validated from {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("data/sft/merchmix_sft_v1.jsonl"),
    )
    args = parser.parse_args()

    validate_file(args.path)


if __name__ == "__main__":
    main()
