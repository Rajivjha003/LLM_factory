import argparse
import json
from collections import defaultdict
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs", type=Path, nargs="+", required=True, help="Evaluation output JSONL files to analyze")
    parser.add_argument("--output-md", type=Path, required=True, help="Output markdown taxonomy file")
    args = parser.parse_args()

    for path in args.outputs:
        if not path.exists():
            print(f"Error: {path} does not exist.")
            return

    failures = []
    taxonomy = defaultdict(int)
    
    for eval_jsonl in args.outputs:
        with open(eval_jsonl, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            
            if not row.get("passing", False):
                failures.append(row)
                
                # Simple taxonomy categorization
                reason_parts = str(row.get("reason", "")).lower()
                
                if "missing required terms" in reason_parts or "must_include" in reason_parts:
                    taxonomy["missing_required_terms"] += 1
                if "contains forbidden terms" in reason_parts or "must_not_include" in reason_parts:
                    taxonomy["violates_forbidden_terms"] += 1
                if "failed validation" in reason_parts:
                    taxonomy["sql_validation_error"] += 1
                
                # If we don't know, it's generic semantic or judge
                if not any(k in taxonomy for k in ["missing_required_terms", "violates_forbidden_terms", "sql_validation_error"]):
                    taxonomy["semantic_or_judge_failure"] += 1

    lines = [
        f"# Failure Taxonomy",
        "",
        f"**Total Failures:** {len(failures)}",
        "",
        "## Categorization",
        "",
        "| Failure Type | Count |",
        "|---|---|",
    ]
    
    for k, v in taxonomy.items():
        lines.append(f"| {k} | {v} |")
        
    lines.extend([
        "",
        "## Detailed Failure Examples",
        ""
    ])
    
    for i, fail in enumerate(failures[:10]):
        lines.append(f"### Example {i+1}: {fail.get('id', 'unknown')}")
        lines.append(f"- **Prompt:** {fail.get('prompt', '')}")
        lines.append(f"- **Reason:** {fail.get('reason', '')}")
        lines.append("```text")
        lines.append(fail.get('response', ''))
        lines.append("```")
        lines.append("")

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    print(f"Failure taxonomy saved to {args.output_md}")

if __name__ == "__main__":
    main()
