import json
import subprocess
from pathlib import Path

def run_mode(env_vars: dict):
    # Run the retrieval harness in a sub-process to isolate config states
    cmd = ["uv", "run", "python", "scripts/run_retrieval_harness.py"]
    subprocess.run(cmd, env=env_vars, check=True)
    
def get_report(mode_name: str):
    path = Path(f"reports/rag/retrieval_harness_{mode_name}.json")
    if not path.exists():
        return None
    with open(path, "r") as f:
        return json.load(f)["metrics"]

def main():
    import os
    base_env = os.environ.copy()
    
    modes = [
        {"name": "dense", "env": {"RAG_MODE": "dense", "RERANKER_ENABLED": "false", "QDRANT_USE_HYBRID": "false"}},
        {"name": "hybrid", "env": {"RAG_MODE": "hybrid", "RERANKER_ENABLED": "false", "QDRANT_USE_HYBRID": "true"}},
        {"name": "hybrid_rerank", "env": {"RAG_MODE": "hybrid_rerank", "RERANKER_ENABLED": "true", "QDRANT_USE_HYBRID": "true"}}
    ]
    
    for m in modes:
        print(f"--- Running mode: {m['name']} ---")
        env = base_env.copy()
        env.update(m["env"])
        # We catch exceptions so we can still print comparison if one fails
        try:
            run_mode(env)
        except Exception as e:
            print(f"Mode {m['name']} failed: {e}")
            
    print("\n=== Retrieval Modes Comparison ===")
    
    markdown_lines = [
        "# Retrieval Modes Comparison",
        "",
        "| Mode | Recall@5 | Precision@5 | MRR | Source Hit Rate | Metadata Validity |",
        "|------|----------|-------------|-----|-----------------|-------------------|"
    ]
    
    for m in modes:
        name = m["name"]
        metrics = get_report(name)
        if metrics:
            r5 = f"{metrics['recall_at_5']:.2f}"
            p5 = f"{metrics['precision_at_5']:.2f}"
            mrr = f"{metrics['mrr']:.2f}"
            shr = f"{metrics['source_hit_rate']:.2f}"
            meta = f"{metrics['metadata_validity_rate']:.2f}"
            line = f"| {name} | {r5} | {p5} | {mrr} | {shr} | {meta} |"
            print(line)
            markdown_lines.append(line)
        else:
            line = f"| {name} | FAILED | FAILED | FAILED | FAILED | FAILED |"
            print(line)
            markdown_lines.append(line)
            
    out_path = Path("reports/rag/retrieval_comparison_phase8c.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(markdown_lines))
        
    print(f"\nComparison written to {out_path}")

if __name__ == "__main__":
    main()
