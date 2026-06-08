from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SYSTEM_PROMPT = (
    "You are a precise retail data engineering assistant for Merchmix. "
    "Diagnose data issues with grain analysis, safe SQL, validation queries, "
    "and clear interpretation. Never suggest destructive SQL for production tables. "
    "Prefer read-only checks, preview tables, backups, and validation steps."
)


def extract_fenced(section: str, heading: str) -> str:
    # Match from ```text to the last ``` before the next ### or end of string
    pattern = rf"###\s+{re.escape(heading)}\s*```(?:text)?\s*(.*?)\s*```\s*(?:###|\Z)"
    match = re.search(pattern, section, flags=re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


def extract_inline(section: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", section, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def parse_pack(text: str) -> list[dict]:
    pair_pattern = re.compile(r"^##\s+Pair\s+\d+\s*:\s*(.+?)\s*$", re.MULTILINE)
    matches = list(pair_pattern.finditer(text))
    pairs = []

    for idx, match in enumerate(matches, start=1):
        title_id = match.group(1).strip()
        start = match.end()
        end = matches[idx].start() if idx < len(matches) else len(text)
        section = text[start:end]

        source_eval_id = extract_inline(section, "source_eval_id") or title_id
        domain = extract_inline(section, "domain") or "unknown"
        quality = extract_inline(section, "human_pair_quality") or "pending"
        notes = extract_inline(section, "human_notes")

        prompt = extract_fenced(section, "Prompt")
        rejected = extract_fenced(section, "Rejected Answer")
        chosen = extract_fenced(section, "CHOSEN_ANSWER")

        if not chosen or "TODO_WRITE_FULL_CHOSEN_ANSWER_HERE" in chosen:
            continue

        pairs.append(
            {
                "id": f"dpo_v2_human_{len(pairs)+1:04d}",
                "source_eval_id": source_eval_id,
                "domain": domain,
                "prompt": prompt,
                "chosen": chosen,
                "rejected": rejected,
                "system": SYSTEM_PROMPT,
                "human_pair_quality": quality,
                "human_notes": notes,
                "source": "human_curated_dpo_v2",
            }
        )

    return pairs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-md", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--min-pairs", type=int, default=40)
    args = parser.parse_args()

    text = args.input_md.read_text(encoding="utf-8")
    pairs = parse_pack(text)

    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with args.output_jsonl.open("w", encoding="utf-8") as file:
        for pair in pairs:
            file.write(json.dumps(pair, ensure_ascii=False) + "\n")

    print(f"Parsed DPO pairs: {len(pairs)}")
    print(f"Output: {args.output_jsonl}")

    if len(pairs) < args.min_pairs:
        raise SystemExit(
            f"Need at least {args.min_pairs} completed human-curated DPO pairs. Found {len(pairs)}."
        )


if __name__ == "__main__":
    main()
