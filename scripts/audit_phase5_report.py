from __future__ import annotations

import argparse
from pathlib import Path
from src.llm_lab.utils.config import load_yaml
from src.llm_lab.utils.io import read_jsonl, read_json, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = load_yaml(args.config)
    run_name = cfg["run_name"]
    jsonl_path = Path(cfg["paths"]["reports_dir"]) / f"{run_name}_eval_v3_judge_v2.jsonl"
    meta_path = Path(cfg["paths"]["reports_dir"]) / f"{run_name}_eval_v3_judge_v2.metadata.json"
    out_path = Path(cfg["paths"]["truth_audit_dir"]) / f"{run_name}_eval_v3_report_audit.json"

    rows = read_jsonl(jsonl_path)
    meta = read_json(meta_path)
    pass_count = sum(1 for r in rows if bool(r.get("passed")))
    pass_rate = pass_count / max(1, len(rows))
    score_rate = sum(float(r.get("score", 0.0)) for r in rows) / max(1, len(rows))

    errors = []
    if pass_count != int(meta.get("pass_count")):
        errors.append(f"pass_count mismatch: rows={pass_count}, metadata={meta.get('pass_count')}")
    if round(pass_rate, 4) != round(float(meta.get("pass_rate")), 4):
        errors.append(f"pass_rate mismatch: rows={pass_rate}, metadata={meta.get('pass_rate')}")
    if round(score_rate, 4) != round(float(meta.get("score_rate")), 4):
        errors.append(f"score_rate mismatch: rows={score_rate}, metadata={meta.get('score_rate')}")

    duplicate_ids = sorted({r.get("id") for r in rows if [x.get("id") for x in rows].count(r.get("id")) > 1})
    if duplicate_ids:
        errors.append(f"duplicate ids: {duplicate_ids}")

    audit = {
        "run_name": run_name,
        "jsonl_path": str(jsonl_path),
        "metadata_path": str(meta_path),
        "num_rows": len(rows),
        "pass_count_recomputed": pass_count,
        "pass_rate_recomputed": round(pass_rate, 4),
        "score_rate_recomputed": round(score_rate, 4),
        "metadata_pass_count": meta.get("pass_count"),
        "metadata_pass_rate": meta.get("pass_rate"),
        "metadata_score_rate": meta.get("score_rate"),
        "passed_audit": len(errors) == 0,
        "errors": errors,
    }
    write_json(out_path, audit)
    print(f"Audit passed: {audit['passed_audit']}")
    print(f"Wrote: {out_path}")
    if errors:
        raise SystemExit("Audit failed: " + "; ".join(errors))


if __name__ == "__main__":
    main()
