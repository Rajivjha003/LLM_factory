from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def run_once(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--eval-dir", type=Path, required=True)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    run_records = []

    for idx in range(1, args.runs + 1):
        output_jsonl = args.output_dir / f"repeat_{idx}.jsonl"
        output_md = args.output_dir / f"repeat_{idx}.md"
        metadata_json = args.output_dir / f"repeat_{idx}.metadata.json"

        command = [
            "python",
            "scripts/run_adapter_eval_v2.py",
            "--base-model",
            args.base_model,
            "--adapter",
            args.adapter,
            "--eval-dir",
            str(args.eval_dir),
            "--output-jsonl",
            str(output_jsonl),
            "--output-md",
            str(output_md),
            "--metadata-json",
            str(metadata_json),
        ]

        result = run_once(command)

        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            raise SystemExit(result.returncode)

        run_records.append(
            {
                "run": idx,
                "jsonl": str(output_jsonl),
                "sha256": sha256_file(output_jsonl),
            }
        )

    unique_hashes = sorted({record["sha256"] for record in run_records})
    deterministic = len(unique_hashes) == 1

    summary = {
        "deterministic": deterministic,
        "runs": run_records,
        "unique_hashes": unique_hashes,
    }

    summary_path = args.output_dir / "repeated_eval_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))

    if not deterministic:
        raise SystemExit("Repeated deterministic eval produced different result files")


if __name__ == "__main__":
    main()
