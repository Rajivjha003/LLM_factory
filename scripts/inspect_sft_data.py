from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("data/sft/merchmix_sft_v1.jsonl"),
    )
    args = parser.parse_args()

    rows = []
    with args.path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    domain_counts = Counter(row["domain"] for row in rows)
    difficulty_counts = Counter(row["difficulty"] for row in rows)

    assistant_lengths = []
    for row in rows:
        assistant_text = "\n".join(
            message["content"]
            for message in row["messages"]
            if message["role"] == "assistant"
        )
        assistant_lengths.append(len(assistant_text))

    print(f"Total samples: {len(rows)}")
    print("\nDomain counts:")
    for domain, count in domain_counts.most_common():
        print(f"  {domain}: {count}")

    print("\nDifficulty counts:")
    for difficulty, count in difficulty_counts.most_common():
        print(f"  {difficulty}: {count}")

    print("\nAssistant response length:")
    print(f"  min: {min(assistant_lengths)}")
    print(f"  max: {max(assistant_lengths)}")
    print(f"  avg: {sum(assistant_lengths) / len(assistant_lengths):.1f}")


if __name__ == "__main__":
    main()
