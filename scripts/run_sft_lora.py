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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/training/sft_qwen_0_5b_lora.yaml")
    args = parser.parse_args()

    with open(args.config) as f:
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
    trainer.train()
    
    print(f"Saving adapter to {config['output_dir']}")
    trainer.save_model(config["output_dir"])
    tokenizer.save_pretrained(config["output_dir"])

if __name__ == "__main__":
    main()
