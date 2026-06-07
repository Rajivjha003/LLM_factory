import argparse
import sys
from pathlib import Path

# Add src to python path for internal modules if needed, though this uses huggingface ecosystem mostly
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import yaml
import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM

def run_lora_training(config_path: str) -> None:
    with open(config_path) as f:
        config = yaml.safe_load(f)

    print(f"Loading tokenizer from {config['model_name_or_path']}")
    tokenizer = AutoTokenizer.from_pretrained(config["model_name_or_path"], trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"Loading dataset from {config['dataset_path']}")
    import json
    with open(config["dataset_path"], "r") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    dataset = Dataset.from_list(rows)

    def format_prompts(example):
        texts = []
        for messages in example["messages"]:
            texts.append(tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False))
        return {"text": texts}

    dataset = dataset.map(format_prompts, batched=True, keep_in_memory=True)

    print(f"Loading base model {config['model_name_or_path']}")
    model = AutoModelForCausalLM.from_pretrained(
        config["model_name_or_path"],
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
    )

    lora_config = LoraConfig(
        r=config["lora_r"],
        lora_alpha=config["lora_alpha"],
        lora_dropout=config["lora_dropout"],
        target_modules=config["target_modules"],
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Mask prompts so loss is only calculated on the assistant response
    response_template = "<|im_start|>assistant\n"
    collator = DataCollatorForCompletionOnlyLM(response_template=response_template, tokenizer=tokenizer)

    training_args = TrainingArguments(
        output_dir=config["output_dir"],
        per_device_train_batch_size=config["per_device_train_batch_size"],
        gradient_accumulation_steps=config["gradient_accumulation_steps"],
        learning_rate=float(config["learning_rate"]),
        num_train_epochs=config["num_train_epochs"],
        logging_steps=config["logging_steps"],
        save_strategy=config["save_strategy"],
        fp16=config["fp16"],
        report_to="none", # no tracking integration for now
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        args=training_args,
        formatting_func=lambda x: x["text"],
        data_collator=collator,
        max_seq_length=config["max_seq_length"],
    )

    print("Starting training...")
    train_result = trainer.train()
    
    print(f"Saving adapter to {config['output_dir']}")
    trainer.save_model(config["output_dir"])
    tokenizer.save_pretrained(config["output_dir"])

    # Collect telemetry
    log_history = trainer.state.log_history
    losses = [log.get("loss") for log in log_history if "loss" in log]
    start_loss = losses[0] if losses else None
    end_loss = losses[-1] if losses else None

    trainable_params, all_params = model.get_nb_trainable_parameters()
    
    telemetry = {
        "training_loss_start": start_loss,
        "training_loss_end": end_loss,
        "train_loss_overall": train_result.metrics.get("train_loss"),
        "tokens_per_sec": train_result.metrics.get("train_steps_per_second", 0) * config["per_device_train_batch_size"] * config["max_seq_length"], # Approximate
        "gpu_memory_peak_gb": torch.cuda.max_memory_allocated() / (1024**3) if torch.cuda.is_available() else 0,
        "number_of_optimizer_steps": train_result.global_step,
        "effective_batch_size": config["per_device_train_batch_size"] * config.get("gradient_accumulation_steps", 1),
        "epochs": train_result.metrics.get("epoch"),
        "lora_rank": config["lora_r"],
        "trainable_parameter_count": trainable_params,
        "total_parameter_count": all_params,
    }

    report_path = Path(config["output_dir"]) / "training_report.json"
    with open(report_path, "w") as f:
        json.dump(telemetry, f, indent=2)
    print(f"Saved training telemetry to {report_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/training/sft_qwen_0_5b_lora.yaml")
    args = parser.parse_args()

    run_lora_training(args.config)

if __name__ == "__main__":
    main()
