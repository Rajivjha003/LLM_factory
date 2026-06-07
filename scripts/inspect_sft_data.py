from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def generate_dataset_stats(path: Path) -> dict:
    rows = []
    with path.open("r", encoding="utf-8") as file:
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

    return {
        "total_samples": len(rows),
        "domain_counts": dict(domain_counts),
        "difficulty_counts": dict(difficulty_counts),
        "assistant_lengths": {
            "min": min(assistant_lengths) if assistant_lengths else 0,
            "max": max(assistant_lengths) if assistant_lengths else 0,
            "avg": sum(assistant_lengths) / len(assistant_lengths) if assistant_lengths else 0
        }
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("data/sft/merchmix_sft_v1.jsonl"),
    )
    args = parser.parse_args()

    stats = generate_dataset_stats(args.path)
    
    print(f"Total samples: {stats['total_samples']}")
    print("\nDomain counts:")
    for domain, count in stats['domain_counts'].items():
        print(f"  {domain}: {count}")

    print("\nDifficulty counts:")
    for difficulty, count in stats['difficulty_counts'].items():
        print(f"  {difficulty}: {count}")

    print("\nAssistant response length:")
    print(f"  min: {stats['assistant_lengths']['min']}")
    print(f"  max: {stats['assistant_lengths']['max']}")
    print(f"  avg: {stats['assistant_lengths']['avg']:.1f}")


if __name__ == "__main__":
    main()
