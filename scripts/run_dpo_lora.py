from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
import yaml
from datasets import Dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import DPOConfig, DPOTrainer

def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows

def format_dataset(rows: list[dict], tokenizer: AutoTokenizer) -> Dataset:
    formatted = []
    for row in rows:
        system = row.get("system", "")
        prompt = row["prompt"]
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        prompt_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        formatted.append({"prompt": prompt_text, "chosen": row["chosen"], "rejected": row["rejected"], "id": row.get("id"), "domain": row.get("domain", "unknown")})
    return Dataset.from_list(formatted)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    base_model_path = cfg["model"]["base_model_path"]
    preference_file = Path(cfg["data"]["preference_file"])
    output_dir = cfg["output"]["output_dir"]
    tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=cfg["model"].get("trust_remote_code", True))
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    rows = read_jsonl(preference_file)
    dataset = format_dataset(rows, tokenizer)
    model = AutoModelForCausalLM.from_pretrained(base_model_path, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=cfg["model"].get("trust_remote_code", True))
    model.config.use_cache = False
    lora_cfg = cfg["lora"]
    peft_config = LoraConfig(r=lora_cfg["r"], lora_alpha=lora_cfg["alpha"], lora_dropout=lora_cfg["dropout"], bias="none", task_type="CAUSAL_LM", target_modules=lora_cfg["target_modules"])
    train_cfg = cfg["training"]
    training_args = DPOConfig(
        output_dir=output_dir,
        num_train_epochs=train_cfg["num_train_epochs"],
        per_device_train_batch_size=train_cfg["per_device_train_batch_size"],
        gradient_accumulation_steps=train_cfg["gradient_accumulation_steps"],
        learning_rate=train_cfg["learning_rate"],
        warmup_ratio=train_cfg["warmup_ratio"],
        weight_decay=train_cfg["weight_decay"],
        logging_steps=train_cfg["logging_steps"],
        save_steps=train_cfg["save_steps"],
        bf16=train_cfg["bf16"],
        fp16=train_cfg["fp16"],
        gradient_checkpointing=train_cfg["gradient_checkpointing"],
        max_grad_norm=train_cfg["max_grad_norm"],
        seed=train_cfg["seed"],
        report_to="none",
        save_total_limit=2,
        beta=train_cfg["beta"],
        max_length=cfg["data"]["max_length"],
        max_prompt_length=cfg["data"]["max_prompt_length"]
    )
    trainer = DPOTrainer(model=model, ref_model=None, args=training_args, train_dataset=dataset, tokenizer=tokenizer, peft_config=peft_config)

    # Fix name collision between trl's DPOTrainer.get_batch_samples and transformers' Trainer.get_batch_samples
    from transformers import Trainer
    trainer.get_batch_samples = Trainer.get_batch_samples.__get__(trainer)

    # Monkey patch for compute_loss signature mismatch
    original_compute_loss = trainer.compute_loss
    def patched_compute_loss(model, inputs, return_outputs=False, **kwargs):
        return original_compute_loss(model, inputs, return_outputs=return_outputs)
    trainer.compute_loss = patched_compute_loss

    # Monkey patch for log signature mismatch
    original_log = trainer.log
    def patched_log(logs, *args, **kwargs):
        return original_log(logs)
    trainer.log = patched_log

    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"DPO adapter saved to: {output_dir}")

if __name__ == "__main__":
    main()
