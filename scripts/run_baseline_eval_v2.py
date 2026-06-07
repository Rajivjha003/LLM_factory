from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from llm_ops.eval.judge_v2 import judge_response_v2, judge_result_to_dict
from llm_ops.eval.reporting import write_eval_markdown, write_json, write_jsonl


SYSTEM_PROMPT = (
    "You are a precise retail data engineering assistant for Merchmix. "
    "Diagnose data issues with grain analysis, safe SQL, validation queries, "
    "and clear interpretation. Never suggest destructive SQL for production tables."
)


class EvalSample:
    def __init__(self, row: dict[str, Any]) -> None:
        self.id = row["id"]
        self.domain = row.get("domain", "unknown")
        self.difficulty = row.get("difficulty", "unknown")
        self.prompt = row["prompt"]
        self.expected_traits = row.get("expected_traits", [])
        self.must_include = row.get("must_include", [])
        self.must_not_include = row.get("must_not_include", [])
        self.max_score = row.get("max_score", 3)


def git_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def package_version(package_name: str) -> str | None:
    try:
        import importlib.metadata

        return importlib.metadata.version(package_name)
    except Exception:
        return None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def dataset_hash(eval_dir: Path) -> dict[str, Any]:
    files = sorted(eval_dir.glob("*.jsonl"))
    combined = hashlib.sha256()
    entries = []

    for path in files:
        file_hash = sha256_file(path)
        combined.update(path.name.encode("utf-8"))
        combined.update(file_hash.encode("utf-8"))
        entries.append({"path": str(path), "sha256": file_hash})

    return {
        "combined_sha256": combined.hexdigest(),
        "files": entries,
    }


def load_samples(eval_dir: Path) -> list[EvalSample]:
    rows = []

    for path in sorted(eval_dir.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    rows.append(EvalSample(json.loads(line)))

    return rows


def generate_response(model, tokenizer, prompt: str, max_new_tokens: int) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            num_beams=1,
            pad_token_id=tokenizer.eos_token_id,
        )

    return tokenizer.decode(
        output_ids[0][inputs["input_ids"].shape[-1]:],
        skip_special_tokens=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--eval-dir", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--metadata-json", type=Path, required=True)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    model.eval()

    samples = load_samples(args.eval_dir)

    results = []

    for sample in samples:
        response = generate_response(
            model=model,
            tokenizer=tokenizer,
            prompt=sample.prompt,
            max_new_tokens=args.max_new_tokens,
        )

        judged = judge_response_v2(sample, response)
        judged_dict = judge_result_to_dict(judged)

        row = {
            "id": sample.id,
            "domain": sample.domain,
            "difficulty": sample.difficulty,
            "prompt": sample.prompt,
            "response": response,
            **judged_dict,
        }

        results.append(row)
        print(f"{sample.id}: passed={row['passed']} score={row['total_score']}/{row['max_score']}")

    metadata = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "commit_hash": git_commit(),
        "model_path": args.model_path,
        "eval_dir": str(args.eval_dir),
        "dataset_hash": dataset_hash(args.eval_dir),
        "generation_config": {
            "max_new_tokens": args.max_new_tokens,
            "do_sample": False,
            "num_beams": 1,
        },
        "judge": "judge_v2",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "torch": package_version("torch"),
            "transformers": package_version("transformers"),
        },
    }

    write_jsonl(args.output_jsonl, results)
    write_json(args.metadata_json, metadata)
    write_eval_markdown(args.output_md, results, metadata)

    print(f"Wrote JSONL: {args.output_jsonl}")
    print(f"Wrote Markdown: {args.output_md}")
    print(f"Wrote Metadata: {args.metadata_json}")


if __name__ == "__main__":
    main()
