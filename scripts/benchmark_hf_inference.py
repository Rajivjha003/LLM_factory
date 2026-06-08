from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


PROMPTS = [
    "Give SQL to find duplicate normalized inventory IDs in BigQuery. Include interpretation.",
    "Postgres has fewer rows than BigQuery for purchase order items. Give a safe reconciliation plan.",
    "Explain why CSOH retail value changes when valuation moves from unit cost to default price.",
    "A Cloud Scheduler job succeeded but downstream table did not refresh. What should I check?",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--max-new-tokens", type=int, default=256)
    args = parser.parse_args()

    tok = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    model.eval()

    rows = []

    for prompt in PROMPTS:
        messages = [
            {"role": "system", "content": "You are a precise retail data engineering assistant for Merchmix."},
            {"role": "user", "content": prompt},
        ]
        text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tok(text, return_tensors="pt").to(model.device)

        start = time.perf_counter()
        with torch.no_grad():
            out = model.generate(
                **inputs,
                max_new_tokens=args.max_new_tokens,
                do_sample=False,
                pad_token_id=tok.eos_token_id,
            )
        elapsed = time.perf_counter() - start

        generated_tokens = int(out.shape[-1] - inputs["input_ids"].shape[-1])
        tokens_per_sec = generated_tokens / elapsed if elapsed else 0.0
        response = tok.decode(out[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)

        rows.append(
            {
                "prompt": prompt,
                "generated_tokens": generated_tokens,
                "elapsed_seconds": elapsed,
                "tokens_per_second": tokens_per_sec,
                "response": response,
            }
        )

        print(f"{generated_tokens} tokens in {elapsed:.2f}s = {tokens_per_sec:.2f} tok/s")

    payload = {
        "model": str(args.model),
        "max_new_tokens": args.max_new_tokens,
        "runs": rows,
        "avg_tokens_per_second": sum(r["tokens_per_second"] for r in rows) / len(rows),
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote benchmark: {args.output_json}")


if __name__ == "__main__":
    main()

