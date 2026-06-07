import json
from pathlib import Path


def read_eval_v3():
    rows = []

    for path in Path("data/eval_v3").glob("*.jsonl"):
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))

    return rows


def test_eval_v3_count():
    rows = read_eval_v3()
    assert len(rows) == 50


def test_eval_v3_unique_ids():
    rows = read_eval_v3()
    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids))


def test_eval_v3_has_destructive_guards():
    rows = read_eval_v3()
    required = {"DROP TABLE", "DELETE FROM", "TRUNCATE"}

    for row in rows:
        guards = {item.upper() for item in row.get("must_not_include", [])}
        assert required.issubset(guards), row["id"]


def test_eval_v3_has_required_fields():
    rows = read_eval_v3()

    required_fields = {
        "id",
        "domain",
        "difficulty",
        "prompt",
        "expected_traits",
        "must_include",
        "must_not_include",
        "max_score",
    }

    for row in rows:
        assert required_fields.issubset(set(row)), row
