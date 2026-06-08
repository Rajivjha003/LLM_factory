from __future__ import annotations

from typing import Any
from datasets import Dataset
from transformers import PreTrainedTokenizerBase


def normalize_messages(row: dict[str, Any]) -> list[dict[str, str]]:
    if "messages" in row and isinstance(row["messages"], list):
        return row["messages"]

    instruction = row.get("instruction") or row.get("prompt") or row.get("user")
    output = row.get("output") or row.get("response") or row.get("assistant")
    system = row.get("system") or "You are a precise Merchmix retail data engineering assistant."
    if not instruction or not output:
        raise ValueError("Each SFT row must contain either messages[] or instruction/prompt + output/response.")
    return [
        {"role": "system", "content": str(system)},
        {"role": "user", "content": str(instruction)},
        {"role": "assistant", "content": str(output)},
    ]


def build_sft_dataset(rows: list[dict[str, Any]], tokenizer: PreTrainedTokenizerBase) -> Dataset:
    texts: list[str] = []
    for row in rows:
        messages = normalize_messages(row)
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        texts.append(text)
    return Dataset.from_dict({"text": texts})
