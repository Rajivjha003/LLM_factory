from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import dataclasses
from llm_ops.eval.judge_v3 import judge_response_v3
from llm_ops.eval.reporting import write_json, write_jsonl


SYSTEM_PROMPT = (
    "You are a precise retail data engineering assistant for Merchmix. "
    "Diagnose data issues with grain analysis, safe SQL, validation queries, "
    "and clear interpretation. Never suggest destructive SQL for production tables. "
    "Prefer read-only checks, preview tables, backups, and validation steps."
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_samples(eval_dir: Path) -> list[EvalSample]:
    rows = []
    for path in sorted(eval_dir.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    rows.append(EvalSample(json.loads(line)))
    return rows


def dataset_hash(eval_dir: Path) -> dict:
    files = sorted(eval_dir.glob("*.jsonl"))
    combined = hashlib.sha256()
    parts = []
    for path in files:
        h = sha256_file(path)
        combined.update(path.name.encode())
        combined.update(h.encode())
        parts.append({"path": str(path), "sha256": h})
    return {"combined_sha256": combined.hexdigest(), "files": parts}


def generate(model, tok, prompt: str, max_new_tokens: int) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tok(text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            num_beams=1,
            pad_token_id=tok.eos_token_id,
        )

    return tok.decode(out[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)


def write_md(path: Path, rows: list[dict], metadata: dict) -> None:
    total = len(rows)
    v3 = sum(1 for r in rows if r.get("judge_v3_passed", False))
    sql = sum(1 for r in rows if r.get("sql_verifier", {}).get("passed", False))
    hr = sum(1 for r in rows if r.get("human_review_required", False))

    lines = [
        "# Merged Model Judge v3 Evaluation",
        "",
        f"- Total: {total}",
        f"- Judge v3 pass: {v3}/{total} ({v3 / total * 100:.1f}%)" if total else "- Judge v3 pass: 0",
        f"- SQL pass: {sql}/{total} ({sql / total * 100:.1f}%)" if total else "- SQL pass: 0",
        f"- Human review required: {hr}",
        "",
        "## Metadata",
        "",
        "```json",
        json.dumps(metadata, indent=2),
        "```",
        "",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--eval-dir", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--metadata-json", type=Path, required=True)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    args = parser.parse_args()

    tok = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    model.eval()

    rows = []
    for sample in load_samples(args.eval_dir):
        response = generate(model, tok, sample.prompt, args.max_new_tokens)
        judged = judge_response_v3(sample, response)
        row = {
            "id": sample.id,
            "domain": sample.domain,
            "difficulty": sample.difficulty,
            "prompt": sample.prompt,
            "response": response,
            **dataclasses.asdict(judged),
        }
        rows.append(row)
        print(f"{sample.id}: v3={row.get('judge_v3_passed')} sql={row.get('sql_verifier', {}).get('passed')}")

    metadata = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "model": str(args.model),
        "eval_dir": str(args.eval_dir),
        "dataset_hash": dataset_hash(args.eval_dir),
        "judge": "judge_v3",
        "generation_config": {"do_sample": False, "num_beams": 1, "max_new_tokens": args.max_new_tokens},
    }

    write_jsonl(args.output_jsonl, rows)
    write_json(args.metadata_json, metadata)
    write_md(args.output_md, rows, metadata)


if __name__ == "__main__":
    main()

