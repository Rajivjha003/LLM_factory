from __future__ import annotations

import argparse
from src.llm_lab.utils.config import load_yaml
from src.llm_lab.utils.seed import set_seed
from src.llm_lab.eval.eval_runner import run_eval


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = load_yaml(args.config)
    set_seed(int(cfg.get("seed", 42)))
    paths = run_eval(cfg)
    print("Wrote:")
    for p in paths:
        print(" -", p)


if __name__ == "__main__":
    main()
