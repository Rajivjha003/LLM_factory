# Preference Dataset Schema

## Purpose
Teach the model what a better answer looks like compared with a worse answer.

## Schema
```json
{
  "id": "pref_000001",
  "domain": "sql_debugging",
  "prompt": "User problem here.",
  "chosen": "Better answer here.",
  "rejected": "Worse answer here.",
  "preference_reason": "Chosen is more precise, safer, and includes validation query."
}
```

## Chosen Answer Should Prefer
- Correctness
- Specificity
- Safe execution
- Validation
- Structured reasoning summary
- Minimal noise

## Rejected Answer Examples
- Generic advice
- No SQL
- Wrong table grain
- Hallucinated column
- Unsafe destructive query
- Overconfident unsupported claim
