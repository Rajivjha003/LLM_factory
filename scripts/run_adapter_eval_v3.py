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
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from llm_ops.eval.judge_v3 import judge_response_v3, judge_result_v3_to_dict
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
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def dataset_hash(eval_dir: Path) -> dict[str, Any]:
    files = sorted(eval_dir.glob("*.jsonl"))
    combined = hashlib.sha256()
    entries = []
    for path in files:
        h = sha256_file(path)
        combined.update(path.name.encode())
        combined.update(h.encode())
        entries.append({"path": str(path), "sha256": h})
    return {"combined_sha256": combined.hexdigest(), "files": entries}

def load_samples(eval_dir: Path) -> list[EvalSample]:
    rows = []
    for path in sorted(eval_dir.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(EvalSample(json.loads(line)))
    return rows

def generate_response(model, tokenizer, prompt: str, max_new_tokens: int) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, num_beams=1, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(out[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)

def write_md(path: Path, rows: list[dict], metadata: dict) -> None:
    total = len(rows)
    v3_pass = sum(1 for r in rows if r.get("judge_v3_passed", False))
    sql_pass = sum(1 for r in rows if r.get("sql_verifier", {}).get("passed", False))
    hr = sum(1 for r in rows if r.get("human_review_required", False))
    lines = ["# Judge v3 Evaluation Report", "", f"- Total: {total}", f"- Judge v3 passed: {v3_pass}/{total} ({v3_pass/total*100:.1f}%)" if total else "- Judge v3 passed: 0", f"- SQL verifier passed: {sql_pass}/{total} ({sql_pass/total*100:.1f}%)" if total else "- SQL verifier passed: 0", f"- Human review required: {hr}", "", "## Metadata", "", "```json", json.dumps(metadata, indent=2), "```", "", "## Samples", ""]
    for r in rows:
        lines.extend([f"### {r['id']}", "", f"- Domain: {r.get('domain')}", f"- Judge v3 passed: {r.get('judge_v3_passed')}", f"- SQL passed: {r.get('sql_verifier', {}).get('passed')}", f"- Human review required: {r.get('human_review_required')}", "", "Prompt:", "```text", r.get("prompt", ""), "```", "Response:", "```text", r.get("response", ""), "```", ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--eval-dir", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--metadata-json", type=Path, required=True)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(args.base_model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    base_model = AutoModelForCausalLM.from_pretrained(args.base_model, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    model = PeftModel.from_pretrained(base_model, args.adapter)
    model.eval()
    rows = []
    for sample in load_samples(args.eval_dir):
        response = generate_response(model, tokenizer, sample.prompt, args.max_new_tokens)
        result = judge_response_v3(sample, response)
        result_dict = judge_result_v3_to_dict(result)
        row = {"id": sample.id, "domain": sample.domain, "difficulty": sample.difficulty, "prompt": sample.prompt, "response": response, **result_dict}
        rows.append(row)
        print(f"{sample.id}: v3={row.get('judge_v3_passed')} sql={row.get('sql_verifier', {}).get('passed')} hr={row.get('human_review_required')}")
    metadata = {"created_at_utc": datetime.now(timezone.utc).isoformat(), "commit_hash": git_commit(), "base_model": args.base_model, "adapter": args.adapter, "eval_dir": str(args.eval_dir), "dataset_hash": dataset_hash(args.eval_dir), "generation_config": {"do_sample": False, "num_beams": 1, "max_new_tokens": args.max_new_tokens}, "judge": "judge_v3", "platform": platform.platform()}
    write_jsonl(args.output_jsonl, rows)
    write_json(args.metadata_json, metadata)
    write_md(args.output_md, rows, metadata)
    print(f"Wrote {args.output_jsonl}")
    print(f"Wrote {args.output_md}")
    print(f"Wrote {args.metadata_json}")

if __name__ == "__main__":
    main()
