import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs", nargs="+", type=Path, required=True, help="List of evaluation JSONL output files")
    parser.add_argument("--output-md", type=Path, required=True, help="Output markdown report file")
    args = parser.parse_args()

    lines = [
        "# Model Matrix Report (Phase 3.6)",
        "",
        "| Model/Eval Run | Total Samples | Passed | Pass Rate (%) | Avg Score |",
        "|---|---|---|---|---|",
    ]

    for path in args.outputs:
        if not path.exists():
            print(f"Warning: {path} does not exist, skipping.")
            continue
            
        total = 0
        passed = 0
        total_score = 0
        total_max_score = 0
        
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                
                total += 1
                if row.get("passing", False):
                    passed += 1
                total_score += row.get("score", 0)
                total_max_score += row.get("max_score", 3)
                
        pass_rate = (passed / total) * 100 if total > 0 else 0
        avg_score = total_score / total if total > 0 else 0
        
        name = path.stem
        lines.append(f"| {name} | {total} | {passed} | {pass_rate:.1f}% | {avg_score:.1f} |")

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    print(f"Matrix report saved to {args.output_md}")

if __name__ == "__main__":
    main()
