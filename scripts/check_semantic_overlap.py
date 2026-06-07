from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_eval_rows(eval_dir: Path) -> list[dict]:
    rows = []
    for path in sorted(eval_dir.glob("*.jsonl")):
        rows.extend(read_jsonl(path))
    return rows


def get_sft_prompt(row: dict) -> str:
    return "\n".join(
        message["content"]
        for message in row["messages"]
        if message["role"] == "user"
    )


def cosine_similarity_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = a / np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = b / np.linalg.norm(b, axis=1, keepdims=True)
    return np.matmul(a_norm, b_norm.T)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sft", type=Path, required=True)
    parser.add_argument("--eval-dir", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--model-name", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--fail-threshold", type=float, default=0.88)
    args = parser.parse_args()

    sft_rows = read_jsonl(args.sft)
    eval_rows = load_eval_rows(args.eval_dir)

    sft_texts = [get_sft_prompt(row) for row in sft_rows]
    eval_texts = [row["prompt"] for row in eval_rows]

    model = SentenceTransformer(args.model_name)

    sft_embeddings = model.encode(sft_texts, normalize_embeddings=True, show_progress_bar=True)
    eval_embeddings = model.encode(eval_texts, normalize_embeddings=True, show_progress_bar=True)

    sims = cosine_similarity_matrix(np.asarray(eval_embeddings), np.asarray(sft_embeddings))

    high_risk = []
    lines = [
        "# Semantic SFT / Eval Overlap Report",
        "",
        f"Embedding model: `{args.model_name}`",
        f"Fail threshold: `{args.fail_threshold}`",
        "",
        "| Eval ID | Best SFT ID | Cosine Similarity | Risk |",
        "|---|---|---:|---|",
    ]

    for eval_idx, eval_row in enumerate(eval_rows):
        best_sft_idx = int(np.argmax(sims[eval_idx]))
        best_score = float(sims[eval_idx][best_sft_idx])
        best_sft_id = sft_rows[best_sft_idx]["id"]

        risk = "HIGH" if best_score >= args.fail_threshold else "OK"

        if risk == "HIGH":
            high_risk.append((eval_row["id"], best_sft_id, best_score))

        lines.append(
            f"| {eval_row['id']} | {best_sft_id} | {best_score:.4f} | {risk} |"
        )

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {args.output_md}")

    if high_risk:
        print("High semantic overlap found:")
        for eval_id, sft_id, score in high_risk:
            print(f"  eval={eval_id} sft={sft_id} score={score:.4f}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
