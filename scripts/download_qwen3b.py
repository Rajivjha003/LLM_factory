from __future__ import annotations

import argparse
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

from src.llm_lab.utils.config import load_yaml


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = load_yaml(args.config)

    model_id = cfg["model"]["base_model_id"]
    local_dir = Path(cfg["model"]["local_base_dir"])
    local_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading tokenizer: {model_id}")
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=cfg["model"].get("trust_remote_code", True))
    tokenizer.save_pretrained(local_dir)

    print(f"Downloading model: {model_id}")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        trust_remote_code=cfg["model"].get("trust_remote_code", True),
        torch_dtype="auto",
        device_map="cpu",
    )
    model.save_pretrained(local_dir, safe_serialization=True)
    print(f"Saved to: {local_dir}")


if __name__ == "__main__":
    main()
