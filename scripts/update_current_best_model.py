from __future__ import annotations

import argparse
from pathlib import Path
from src.llm_lab.utils.config import load_yaml
from src.llm_lab.utils.io import read_json, write_text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = load_yaml(args.config)
    run_name = cfg["run_name"]
    meta = read_json(Path(cfg["paths"]["reports_dir"]) / f"{run_name}_eval_v3_judge_v2.metadata.json")
    pass_rate = float(meta["pass_rate"])
    score_rate = float(meta["score_rate"])
    champ_pass = float(cfg["champion"]["pass_rate"])
    min_candidate = float(cfg["promotion_rules"]["minimum_candidate_pass_rate"])
    strong = float(cfg["promotion_rules"]["strong_promotion_pass_rate"])

    if pass_rate >= strong:
        status = "NEW_CHAMPION"
        recommendation = "Promote Qwen 3B QLoRA v1. Next phase: DPO preparation on 3B failure/chosen-rejected pairs."
        current_best = run_name
    elif pass_rate >= min_candidate:
        status = "PROMISING_CANDIDATE"
        recommendation = "Do not fully promote yet. Run 3B v2 with repaired real-heavy SFT v4b or inspect failure taxonomy."
        current_best = cfg["champion"]["name"]
    elif pass_rate > champ_pass:
        status = "WEAK_IMPROVEMENT"
        recommendation = "Keep 1.5B champion unless human review confirms meaningful improvement. Data quality remains bottleneck."
        current_best = cfg["champion"]["name"]
    else:
        status = "NOT_PROMOTED"
        recommendation = "Keep 1.5B champion. Return to dataset quality, SQL verifier, or Judge v3 calibration."
        current_best = cfg["champion"]["name"]

    lines = [
        "# Current Best Model Registry",
        "",
        f"- Phase: {cfg['phase_name']}",
        f"- Phase 5 run: `{run_name}`",
        f"- Phase 5 pass rate: {pass_rate:.1%}",
        f"- Phase 5 score rate: {score_rate:.1%}",
        f"- Previous champion: `{cfg['champion']['name']}` at {champ_pass:.1%}",
        f"- Registry status: `{status}`",
        f"- Current best: `{current_best}`",
        "",
        "## Recommendation",
        "",
        recommendation,
    ]
    out_path = Path(cfg["paths"]["registry_dir"]) / "current_best_model.md"
    write_text(out_path, "\n".join(lines))
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
