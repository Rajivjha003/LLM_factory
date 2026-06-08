import json
from pathlib import Path

def test_dpo_dataset_exists_if_built():
    path = Path("data/preferences/merchmix_dpo_v1.jsonl")
    if not path.exists():
        return
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    assert len(rows) >= 20
    for row in rows:
        assert row["prompt"].strip()
        assert row["chosen"].strip()
        assert row["rejected"].strip()
        assert row["chosen"] != row["rejected"]
        assert len(row["chosen"]) >= 250
