import argparse
import asyncio
import json
from pathlib import Path
from openai import AsyncOpenAI
from llm_ops.eval.schemas import EvalSample, EvalResult
from llm_ops.eval.simple_judge import SimpleJudge

async def main():
    parser = argparse.ArgumentParser(description="Run baseline evaluation")
    parser.add_argument("--model-path", type=str, required=True, help="Path to the model")
    parser.add_argument("--eval-dir", type=str, required=True, help="Directory containing eval JSONL files")
    parser.add_argument("--output-jsonl", type=str, required=True, help="Output JSONL file path")
    parser.add_argument("--output-md", type=str, required=True, help="Output Markdown report path")
    args = parser.parse_args()

    client = AsyncOpenAI(
        base_url="http://127.0.0.1:8000/v1",
        api_key="test_key"
    )
    
    judge = SimpleJudge()
    eval_dir = Path(args.eval_dir)
    jsonl_files = sorted(eval_dir.glob("*.jsonl"))
    
    samples = []
    for file in jsonl_files:
        with open(file, "r") as f:
            for line in f:
                if line.strip():
                    samples.append(EvalSample(**json.loads(line)))
                    
    print(f"Loaded {len(samples)} samples to evaluate from {args.eval_dir}.")
    
    results = []
    
    async def process_sample(sample: EvalSample):
        try:
            response = await client.chat.completions.create(
                model=args.model_path,
                messages=[
                    {"role": "system", "content": "You are a helpful expert assistant."},
                    {"role": "user", "content": sample.prompt}
                ],
                max_tokens=256,
                temperature=0.0
            )
            model_text = response.choices[0].message.content
        except Exception as e:
            model_text = f"[API Error: {e}]"
            
        result = judge.evaluate(sample, model_text)
        return result

    for i in range(0, len(samples), 5):
        batch = samples[i:i+5]
        batch_results = await asyncio.gather(*[process_sample(s) for s in batch])
        results.extend(batch_results)
        print(f"Processed {len(results)}/{len(samples)}...")
        
    out_jsonl = Path(args.output_jsonl)
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    out_md = Path(args.output_md)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    
    pass_count = 0
    total_score = 0.0
    max_possible = sum(s.max_score for s in samples)
    
    domain_stats = {}
    
    with open(out_jsonl, "w") as f:
        for res in results:
            f.write(res.model_dump_json() + "\n")
            if res.passed:
                pass_count += 1
            total_score += res.score
            
            if res.domain not in domain_stats:
                domain_stats[res.domain] = {"pass": 0, "total": 0, "score": 0.0, "max_score": 0}
            domain_stats[res.domain]["total"] += 1
            if res.passed:
                domain_stats[res.domain]["pass"] += 1
            domain_stats[res.domain]["score"] += res.score
            domain_stats[res.domain]["max_score"] += next(s.max_score for s in samples if s.id == res.sample_id)
            
    # Write Markdown Report
    with open(out_md, "w") as f:
        f.write(f"# Baseline Evaluation Report\n\n")
        f.write(f"**Model:** `{args.model_path}`\n")
        f.write(f"**Total Samples:** {len(samples)}\n")
        f.write(f"**Pass Rate:** {pass_count}/{len(samples)} ({(pass_count/len(samples)*100 if samples else 0):.1f}%)\n")
        f.write(f"**Total Score:** {total_score}/{max_possible}\n\n")
        
        f.write("## Domain Breakdown\n\n")
        f.write("| Domain | Pass Rate | Score |\n")
        f.write("|---|---|---|\n")
        for dom, stats in domain_stats.items():
            pass_pct = (stats["pass"] / stats["total"]) * 100
            f.write(f"| {dom} | {stats['pass']}/{stats['total']} ({pass_pct:.1f}%) | {stats['score']}/{stats['max_score']} |\n")
        
        f.write("\n## Failures\n\n")
        for res in results:
            if not res.passed:
                f.write(f"### {res.sample_id} ({res.domain})\n")
                f.write(f"- **Prompt:** {res.prompt}\n")
                f.write(f"- **Reasoning:** {res.reasoning}\n")
                f.write(f"- **Score:** {res.score}\n")
                f.write(f"- **Response Snippet:** {res.response[:150]}...\n\n")
                
    print("\n--- Evaluation Complete ---")
    print(f"Pass Rate: {pass_count}/{len(samples)} ({(pass_count/len(samples)*100 if samples else 0):.1f}%)")
    print(f"Results saved to {out_jsonl}")
    print(f"Report saved to {out_md}")

if __name__ == "__main__":
    asyncio.run(main())
