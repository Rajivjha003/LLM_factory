# SFT Schema

## Purpose
Teach the model response format, tone, domain behavior, and structured problem-solving.

## Schema
```json
{
  "id": "sft_000001",
  "domain": "bigquery_debugging",
  "difficulty": "medium",
  "messages": [
    {"role": "system", "content": "You are a precise data engineering assistant."},
    {"role": "user", "content": "User problem here."},
    {"role": "assistant", "content": "High-quality answer here."}
  ],
  "quality_score": 5,
  "source": "human_curated",
  "contains_private_data": false
}
```

## Good SFT Answer Traits
- Direct diagnosis
- Exact SQL or exact steps
- Explains grain/logic
- Mentions validation
- Avoids hallucinated columns
- Avoids motivational fluff
- Uses safe operations
