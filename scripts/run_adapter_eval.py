import argparse
import json
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import sys

# Add src to python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from llm_ops.eval.simple_judge import SimpleJudge

def load_eval_data(path: Path):
    with open(path, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def run_evaluation(base_model: str, adapter: str, eval_dir: str, output_jsonl: str) -> None:
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)

    print("Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
    )

    print("Loading adapter...")
    model = PeftModel.from_pretrained(model, adapter)

    eval_files = list(Path(eval_dir).glob("*.jsonl"))
    print(f"Found {len(eval_files)} eval files")

    judge = SimpleJudge()
    results = []

    for file in eval_files:
        items = load_eval_data(file)
        for item in items:
            messages = [
                {"role": "system", "content": "You are a precise retail data engineering assistant for Merchmix. Diagnose data issues with grain analysis, safe SQL, and validation steps. Never suggest destructive SQL unless explicitly requested and protected."},
                {"role": "user", "content": item["prompt"]}
            ]
            
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer(text, return_tensors="pt").to(model.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=512,
                    do_sample=False,
                    temperature=None,
                    top_p=None
                )
                
            response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
            
            from llm_ops.eval.schemas import EvalSample
            sample = EvalSample(**item)
            
            result = judge.evaluate(
                sample=sample,
                response=response
            )
            
            results.append({
                "id": item["id"],
                "domain": item["domain"],
                "prompt": item["prompt"],
                "response": response,
                "score": result.score,
                "passing": result.passed,
                "max_score": item.get("max_score", 3)
            })

    Path(output_jsonl).parent.mkdir(parents=True, exist_ok=True)
    with open(output_jsonl, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    print(f"Saved {len(results)} eval results to {output_jsonl}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-model", type=str, default="/home/rajiv/models/base/qwen2_5_0_5b_instruct")
    parser.add_argument("--adapter", type=str, default="models/adapters/qwen_0_5b_merchmix_v1")
    parser.add_argument("--eval-dir", type=str, default="data/eval")
    parser.add_argument("--output-jsonl", type=str, default="reports/eval_reports/qwen_0_5b_adapter_results.jsonl")
    args = parser.parse_args()

    run_evaluation(args.base_model, args.adapter, args.eval_dir, args.output_jsonl)

if __name__ == "__main__":
    main()
