import json
from pathlib import Path


def read_rows(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def test_dpo_v2_dataset_quality_if_exists():
    path = Path("data/preferences/merchmix_dpo_v2_human.jsonl")
    if not path.exists():
        return

    rows = read_rows(path)
    assert len(rows) >= 40

    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids))

    for row in rows:
        assert row["prompt"].strip()
        assert row["chosen"].strip()
        assert row["rejected"].strip()
        assert row["chosen"] != row["rejected"]
        assert len(row["chosen"]) >= 300
        assert "TODO" not in row["chosen"]
