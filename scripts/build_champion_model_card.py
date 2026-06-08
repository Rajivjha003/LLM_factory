from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml


def git_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("configs/phase7/phase7_paths.yaml"))
    args = parser.parse_args()

    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    out = Path(cfg["outputs"]["model_card"])
    out.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Champion Model Card — Qwen 1.5B SFT v2",
        "",
        f"Created UTC: `{datetime.now(timezone.utc).isoformat()}`",
        f"Git commit: `{git_commit()}`",
        "",
        "## Champion",
        "",
        f"- Base model: `{cfg['champion']['base_model']}`",
        f"- Adapter: `{cfg['champion']['adapter']}`",
        f"- Merged model: `{cfg['champion']['merged_model']}`",
        f"- Evaluation set: `{cfg['champion']['eval_dir']}`",
        "- Judge: Judge v3 + SQL verifier",
        "",
        "## Verified Champion Metrics",
        "",
        "- Judge v3 pass: 44/50 = 88%",
        "- SQL verifier pass: 44/50 = 88%",
        "- Strict Judge v2 pass: 17/50 = 34%",
        "",
        "## Promotion History",
        "",
        "- SFT v4: rejected.",
        "- SFT v4b: rejected.",
        "- Qwen 3B QLoRA v1: rejected.",
        "- DPO v1: rejected.",
        "- DPO v2: rejected/tied, not promoted.",
        "",
        "## Intended Use",
        "",
        "Merchmix retail/data-engineering assistant for:",
        "",
        "- BigQuery debugging",
        "- SQL generation and validation",
        "- Postgres vs BigQuery reconciliation",
        "- WSSI / CSOH / retail metric reasoning",
        "- Pipeline debugging",
        "- Safe read-only data diagnostics",
        "",
        "## Safety Rules",
        "",
        "- Must prefer read-only SQL.",
        "- Must not place destructive SQL inside executable SQL blocks.",
        "- Must use preview/backup/validation framing for production changes.",
        "- Must explain query interpretation and next checks.",
        "",
        "## Limitations",
        "",
        "- Not a production autonomous database agent.",
        "- SQL verifier is semantic/static, not a full BigQuery dry-run verifier yet.",
        "- Human review is still required for high-risk production changes.",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote model card: {out}")


if __name__ == "__main__":
    main()

