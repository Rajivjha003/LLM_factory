from __future__ import annotations

import argparse
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

from src.llm_lab.training.sft_dataset import build_sft_dataset
from src.llm_lab.utils.config import load_yaml
from src.llm_lab.utils.io import read_jsonl, write_json
from src.llm_lab.utils.seed import set_seed
from src.llm_lab.utils.gpu import print_gpu_summary


def dtype_from_name(name: str):
    if name == "bfloat16":
        return torch.bfloat16
    if name == "float16":
        return torch.float16
    if name == "float32":
        return torch.float32
    raise ValueError(f"Unsupported dtype: {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = load_yaml(args.config)
    set_seed(int(cfg.get("seed", 42)))
    print_gpu_summary()

    model_path = Path(cfg["model"]["local_base_dir"])
    if not model_path.exists():
        model_path = Path(cfg["model"]["base_model_id"])

    train_path = Path(cfg["paths"]["train_jsonl"])
    output_dir = Path(cfg["paths"]["output_adapter_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(str(model_path), trust_remote_code=cfg["model"].get("trust_remote_code", True))
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    qcfg = cfg["qlora"]
    compute_dtype = dtype_from_name(qcfg.get("bnb_4bit_compute_dtype", "bfloat16"))
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=bool(qcfg.get("load_in_4bit", True)),
        bnb_4bit_quant_type=qcfg.get("bnb_4bit_quant_type", "nf4"),
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=bool(qcfg.get("bnb_4bit_use_double_quant", True)),
    )

    print(f"Loading model: {model_path}")
    model = AutoModelForCausalLM.from_pretrained(
        str(model_path),
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=cfg["model"].get("trust_remote_code", True),
    )
    model.config.use_cache = False

    lora_config = LoraConfig(
        r=int(qcfg.get("lora_r", 32)),
        lora_alpha=int(qcfg.get("lora_alpha", 64)),
        lora_dropout=float(qcfg.get("lora_dropout", 0.05)),
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=qcfg["target_modules"],
    )

    rows = read_jsonl(train_path)
    dataset = build_sft_dataset(rows, tokenizer)
    print(f"Training rows: {len(dataset)}")

    tcfg = cfg["training"]
    sft_args = SFTConfig(
        output_dir=str(output_dir),
        dataset_text_field="text",
        max_seq_length=int(tcfg.get("max_seq_length", 2048)),
        packing=False,
        num_train_epochs=float(tcfg.get("num_train_epochs", 3)),
        per_device_train_batch_size=int(tcfg.get("per_device_train_batch_size", 1)),
        gradient_accumulation_steps=int(tcfg.get("gradient_accumulation_steps", 8)),
        learning_rate=float(tcfg.get("learning_rate", 2e-4)),
        warmup_ratio=float(tcfg.get("warmup_ratio", 0.03)),
        weight_decay=float(tcfg.get("weight_decay", 0.0)),
        lr_scheduler_type=tcfg.get("lr_scheduler_type", "cosine"),
        logging_steps=int(tcfg.get("logging_steps", 5)),
        save_strategy=tcfg.get("save_strategy", "epoch"),
        save_total_limit=int(tcfg.get("save_total_limit", 2)),
        bf16=bool(tcfg.get("bf16", True)),
        fp16=bool(tcfg.get("fp16", False)),
        gradient_checkpointing=bool(tcfg.get("gradient_checkpointing", True)),
        optim=tcfg.get("optim", "paged_adamw_8bit"),
        max_grad_norm=float(tcfg.get("max_grad_norm", 0.3)),
        report_to=tcfg.get("report_to", "none"),
        seed=int(cfg.get("seed", 42)),
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        args=sft_args,
        train_dataset=dataset,
        peft_config=lora_config,
    )

    trainer.train()
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))

    metadata = {
        "phase": cfg["phase_name"],
        "run_name": cfg["run_name"],
        "base_model": cfg["model"]["base_model_id"],
        "dataset": str(train_path),
        "num_train_rows": len(dataset),
        "adapter_dir": str(output_dir),
        "qlora": qcfg,
        "training": tcfg,
    }
    write_json(output_dir / "phase5_training_metadata.json", metadata)
    print(f"Saved adapter: {output_dir}")


if __name__ == "__main__":
    main()
