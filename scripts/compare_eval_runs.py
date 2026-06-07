import argparse
import json
from pathlib import Path

def load_results(path: Path):
    with open(path, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=str, default="reports/eval_reports/qwen_0_5b_baseline_results.jsonl")
    parser.add_argument("--candidate", type=str, default="reports/eval_reports/qwen_0_5b_adapter_results.jsonl")
    parser.add_argument("--output-md", type=str, default="reports/eval_reports/comparison_report.md")
    args = parser.parse_args()

    baseline_data = load_results(Path(args.baseline))
    candidate_data = load_results(Path(args.candidate))

    baseline_dict = {item.get("id", item.get("sample_id")): item for item in baseline_data}

    total_items = len(candidate_data)
    baseline_passes = sum(1 for item in baseline_data if item.get("passing", item.get("passed", False)))
    candidate_passes = sum(1 for item in candidate_data if item.get("passing", item.get("passed", False)))

    report = []
    report.append("# Eval Comparison Report")
    report.append("")
    report.append(f"**Baseline Passes:** {baseline_passes} / {len(baseline_data)} ({baseline_passes/len(baseline_data)*100:.1f}%)")
    report.append(f"**Candidate Passes:** {candidate_passes} / {total_items} ({candidate_passes/total_items*100:.1f}%)")
    report.append("")
    report.append("## Item Diff")
    report.append("")
    report.append("| ID | Domain | Baseline | Candidate | Diff |")
    report.append("|---|---|---|---|---|")

    for cand in candidate_data:
        base = baseline_dict.get(cand.get("id", cand.get("sample_id")), {})
        base_pass = base.get("passing", base.get("passed", False))
        cand_pass = cand.get("passing", cand.get("passed", False))

        if not base_pass and cand_pass:
            diff = "🟢 IMPROVED"
        elif base_pass and not cand_pass:
            diff = "🔴 REGRESSED"
        elif base_pass and cand_pass:
            diff = "⚪ MAINTAINED PASS"
        else:
            diff = "⚫ MAINTAINED FAIL"

        base_status = "PASS" if base_pass else "FAIL"
        cand_status = "PASS" if cand_pass else "FAIL"

        report.append(f"| {cand['id']} | {cand['domain']} | {base_status} | {cand_status} | {diff} |")

    with open(args.output_md, "w") as f:
        f.write("\n".join(report))

    print(f"Saved comparison report to {args.output_md}")
    
    # Print summary
    print(f"Baseline Passes: {baseline_passes} / {len(baseline_data)}")
    print(f"Candidate Passes: {candidate_passes} / {total_items}")

if __name__ == "__main__":
    main()
