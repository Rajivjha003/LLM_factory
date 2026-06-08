from __future__ import annotations

import argparse
from pathlib import Path

import torch
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    args = parser.parse_args()

    if not args.model.exists():
        raise FileNotFoundError(args.model)

    print(f"Loading config/tokenizer from {args.model}")
    cfg = AutoConfig.from_pretrained(args.model, trust_remote_code=True)
    tok = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)

    print("Config loaded:")
    print(f"  model_type: {getattr(cfg, 'model_type', None)}")
    print(f"  hidden_size: {getattr(cfg, 'hidden_size', None)}")
    print(f"  num_hidden_layers: {getattr(cfg, 'num_hidden_layers', None)}")
    print(f"  vocab_size: {getattr(cfg, 'vocab_size', None)}")
    print(f"  tokenizer_size: {len(tok)}")

    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    model.eval()

    messages = [
        {
            "role": "system",
            "content": "You are a precise retail data engineering assistant for Merchmix.",
        },
        {
            "role": "user",
            "content": "Give a safe BigQuery query to find duplicate normalized inventory IDs. Include interpretation.",
        },
    ]

    prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tok(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
            pad_token_id=tok.eos_token_id,
        )

    response = tok.decode(out[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
    print("\nSample response:")
    print(response)

    required = ["GROUP BY", "HAVING", "TRIM", "UPPER"]
    missing = [term for term in required if term.lower() not in response.lower()]
    if missing:
        raise SystemExit(f"Merged model sanity check failed. Missing: {missing}")

    print("\nPASS: merged model sanity check")


if __name__ == "__main__":
    main()

