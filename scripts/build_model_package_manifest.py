from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def dir_manifest(path: Path) -> list[dict]:
    if not path.exists():
        return []

    rows = []
    for item in sorted(path.rglob("*")):
        if item.is_file():
            rows.append(
                {
                    "path": str(item),
                    "size_bytes": item.stat().st_size,
                    "sha256": sha256_file(item),
                }
            )
    return rows


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

    merged = Path(cfg["champion"]["merged_model"])
    gguf_dir = Path(cfg["llama_cpp"]["gguf_dir"])
    out = Path(cfg["outputs"]["package_manifest"])

    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "champion": cfg["champion"],
        "merged_model_files": dir_manifest(merged),
        "gguf_files": dir_manifest(gguf_dir),
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote package manifest: {out}")


if __name__ == "__main__":
    main()

