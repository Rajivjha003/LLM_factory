from __future__ import annotations

import argparse
from pathlib import Path
from src.llm_lab.utils.config import load_yaml
from src.llm_lab.utils.io import read_jsonl


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = load_yaml(args.config)
    required = [cfg["paths"]["train_jsonl"], cfg["paths"]["eval_jsonl"]]
    for p in required:
        path = Path(p)
        if not path.exists():
            raise FileNotFoundError(f"Missing required Phase 5 input: {path}")
        rows = read_jsonl(path)
        print(f"OK: {path} rows={len(rows)}")
    print("Phase 5 inputs valid.")


if __name__ == "__main__":
    main()
