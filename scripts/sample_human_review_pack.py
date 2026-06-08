import argparse
import json
import random
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def sample_from_file(path: Path, count: int, seed: int) -> list[dict]:
    rows = read_jsonl(path)
    random.seed(seed)
    # Prefer sampling near-pass or interesting failures, but just uniform random is fine
    # if we want unbiased estimates.
    if len(rows) <= count:
        return rows
    return random.sample(rows, count)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sft-v2-jsonl", type=Path, required=True)
    parser.add_argument("--sft-v4b-jsonl", type=Path, required=True)
    parser.add_argument("--qwen-3b-jsonl", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--sample-size", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    v2_samples = sample_from_file(args.sft_v2_jsonl, args.sample_size, args.seed)
    v4b_samples = sample_from_file(args.sft_v4b_jsonl, args.sample_size, args.seed)
    q3b_samples = sample_from_file(args.qwen_3b_jsonl, args.sample_size, args.seed)

    lines = [
        "# Phase 5C: Human Review Pack",
        "",
        "Please manually inspect these samples and label them. Search for `[ ] human_correct:`.",
        ""
    ]

    def add_samples(title, samples):
        lines.append(f"## {title}")
        for idx, row in enumerate(samples, start=1):
            lines.append(f"### {idx}. ID: {row.get('id')} (Score Rate: {row.get('score_rate', 0.0):.2f})")
            lines.append(f"**Passed:** {row.get('passed', False)}")
            lines.append(f"**Missing Required:** `{row.get('missing_required', [])}`")
            lines.append(f"**Feedback:** {row.get('feedback', [])}")
            lines.append("")
            lines.append("**Model Response:**")
            lines.append("```text")
            lines.append(row.get("response", "").strip())
            lines.append("```")
            lines.append("")
            lines.append("- [ ] `human_correct`: yes / no / partial")
            lines.append("- [ ] `judge_agree`: yes / no")
            lines.append("- `reason`: ")
            lines.append("---")
            lines.append("")

    add_samples("Qwen 1.5B SFT v2 (Champion)", v2_samples)
    add_samples("Qwen 1.5B SFT v4b", v4b_samples)
    add_samples("Qwen 3B QLoRA v1", q3b_samples)

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Generated human review pack with {len(v2_samples) + len(v4b_samples) + len(q3b_samples)} samples.")
    print(f"Wrote to {args.output_md}")


if __name__ == "__main__":
    main()