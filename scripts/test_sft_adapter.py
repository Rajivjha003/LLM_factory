import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-model", type=str, default="/home/rajiv/models/base/qwen2_5_0_5b_instruct")
    parser.add_argument("--adapter", type=str, default="models/adapters/qwen_0_5b_merchmix_v1")
    parser.add_argument("--prompt", type=str, default="Write BigQuery SQL to find inventory_id values present in table_a but missing from table_b.")
    args = parser.parse_args()

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model, trust_remote_code=True)

    print("Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
    )

    print("Loading adapter...")
    model = PeftModel.from_pretrained(model, args.adapter)
    
    messages = [
        {"role": "system", "content": "You are a precise data engineering and retail analytics assistant. Provide exact SQL, avoid destructive operations, and explain reasoning clearly."},
        {"role": "user", "content": args.prompt}
    ]
    
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    
    print("\nGenerating response...\n")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=512)
        
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    print(f"User: {args.prompt}")
    print("-" * 40)
    print(f"Assistant:\n{response}")

if __name__ == "__main__":
    main()
