# GRPO Task Schema

## Purpose
Define verifiable tasks for reasoning alignment.

## Schema
```json
{
  "id": "grpo_000001",
  "task_type": "sql_generation",
  "prompt": "Generate a BigQuery query to find extra inventory IDs in table A compared to table B.",
  "expected_properties": [
    "uses anti-join or EXCEPT DISTINCT",
    "normalizes TRIM/UPPER",
    "read-only query"
  ],
  "verifier": "sql_static_checker_v1",
  "reward_rules": {
    "valid_sql": 1.0,
    "correct_grain": 1.0,
    "safe_read_only": 1.0,
    "hallucinated_column": -1.0,
    "unsafe_mutation": -2.0
  }
}
```

## Reward Rule Principles
- Reward only measurable behavior.
- Penalize unsafe behavior strongly.
- Keep reward functions simple first.
- Inspect reward hacking manually.
