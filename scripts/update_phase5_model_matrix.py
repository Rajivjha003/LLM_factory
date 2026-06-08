from __future__ import annotations

import argparse
from pathlib import Path
from src.llm_lab.utils.config import load_yaml
from src.llm_lab.utils.io import read_json, write_text


def decision(pass_rate: float, cfg: dict) -> str:
    rules = cfg["promotion_rules"]
    champ = cfg["champion"]["pass_rate"]
    if pass_rate >= float(rules["strong_promotion_pass_rate"]):
        return "PROMOTE_STRONG: 3B clears 45%+ gate. Prepare DPO on 3B."
    if pass_rate >= float(rules["minimum_candidate_pass_rate"]):
        return "CANDIDATE: scale helped but not enough. Consider 3B v2 with real-heavy SFT v4b."
    if pass_rate > champ:
        return "WEAK_CANDIDATE: beats champion but below promotion gate. Inspect taxonomy before deciding."
    return "REJECT_OR_HOLD: keep 1.5B champion; data/judge/verifier is bottleneck."


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = load_yaml(args.config)
    run_name = cfg["run_name"]
    meta = read_json(Path(cfg["paths"]["reports_dir"]) / f"{run_name}_eval_v3_judge_v2.metadata.json")
    pass_rate = float(meta["pass_rate"])
    score_rate = float(meta["score_rate"])
    dec = decision(pass_rate, cfg)

    lines = [
        "# Phase 5 Model Matrix",
        "",
        "| Model | Eval | Pass Rate | Score Rate | Status |",
        "|---|---:|---:|---:|---|",
        f"| {cfg['champion']['name']} | eval_v3 | {cfg['champion']['pass_rate']:.1%} | {cfg['champion']['score_rate']:.1%} | Current champion before Phase 5 |",
        f"| {run_name} | eval_v3 | {pass_rate:.1%} | {score_rate:.1%} | {dec} |",
        "",
        "## Decision",
        "",
        dec,
        "",
        "## Gates",
        "",
        f"- Minimum candidate: {float(cfg['promotion_rules']['minimum_candidate_pass_rate']):.1%}",
        f"- Strong promotion: {float(cfg['promotion_rules']['strong_promotion_pass_rate']):.1%}",
        f"- Excellent: {float(cfg['promotion_rules']['excellent_pass_rate']):.1%}",
    ]
    out_path = Path(cfg["paths"]["matrix_dir"]) / "model_matrix_phase5_qwen3b_eval_v3.md"
    write_text(out_path, "\n".join(lines))
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
