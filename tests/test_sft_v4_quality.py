import json
from pathlib import Path


def read_sft(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def assistant_text(row):
    return "\n".join(
        msg["content"]
        for msg in row["messages"]
        if msg["role"] == "assistant"
    )


def test_sft_v4_exists_and_has_enough_rows():
    path = Path("data/sft/merchmix_sft_v4.jsonl")
    assert path.exists()
    rows = read_sft(path)
    assert len(rows) >= 800


def test_sft_v4_ids_unique():
    rows = read_sft(Path("data/sft/merchmix_sft_v4.jsonl"))
    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids))


def test_sft_v4_has_sql_training_examples():
    rows = read_sft(Path("data/sft/merchmix_sft_v4.jsonl"))
    sql_count = sum(1 for row in rows if "```sql" in assistant_text(row).lower())
    assert sql_count >= 300


def test_sft_v4_has_safety_language():
    rows = read_sft(Path("data/sft/merchmix_sft_v4.jsonl"))
    safety_count = 0

    for row in rows:
        text = assistant_text(row).lower()
        if "do not" in text and ("drop table" in text or "delete from" in text or "truncate" in text):
            safety_count += 1

    assert safety_count >= 50


def test_sft_v4_has_interpretation_blocks():
    rows = read_sft(Path("data/sft/merchmix_sft_v4.jsonl"))
    interpretation_count = sum(
        1 for row in rows
        if "interpretation" in assistant_text(row).lower()
    )
    assert interpretation_count >= 300
