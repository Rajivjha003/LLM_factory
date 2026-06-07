from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run_command(command: list[str]) -> dict:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sft", type=Path, required=True)
    parser.add_argument("--eval-dir", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--lexical-output", type=Path, required=True)
    parser.add_argument("--semantic-output", type=Path, required=True)
    parser.add_argument("--lexical-threshold", type=float, default=0.80)
    parser.add_argument("--semantic-threshold", type=float, default=0.88)
    args = parser.parse_args()

    lexical_cmd = [
        "python",
        "scripts/check_sft_eval_overlap_strict.py",
        "--sft",
        str(args.sft),
        "--eval-dir",
        str(args.eval_dir),
        "--output",
        str(args.lexical_output),
        "--fail-threshold",
        str(args.lexical_threshold),
    ]

    semantic_cmd = [
        "python",
        "scripts/check_semantic_overlap.py",
        "--sft",
        str(args.sft),
        "--eval-dir",
        str(args.eval_dir),
        "--output-md",
        str(args.semantic_output),
        "--fail-threshold",
        str(args.semantic_threshold),
    ]

    lexical = run_command(lexical_cmd)
    semantic = run_command(semantic_cmd)

    passed = lexical["returncode"] == 0 and semantic["returncode"] == 0

    payload = {
        "sft": str(args.sft),
        "eval_dir": str(args.eval_dir),
        "passed": passed,
        "lexical": lexical,
        "semantic": semantic,
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Wrote {args.output_json}")

    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
