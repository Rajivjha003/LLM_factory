from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip()
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    files = sorted(args.dataset_dir.glob("*.jsonl"))

    combined = hashlib.sha256()
    file_entries = []

    for path in files:
        file_hash = sha256_file(path)
        combined.update(path.name.encode("utf-8"))
        combined.update(file_hash.encode("utf-8"))
        file_entries.append(
            {
                "path": str(path),
                "sha256": file_hash,
            }
        )

    manifest = {
        "dataset_dir": str(args.dataset_dir),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "commit_hash": git_commit(),
        "combined_sha256": combined.hexdigest(),
        "files": file_entries,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote hash manifest: {args.output}")


if __name__ == "__main__":
    main()
