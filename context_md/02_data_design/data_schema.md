# General Data Schema

Every dataset item should include:

```json
{
  "id": "unique_id",
  "dataset_type": "sft|preference|grpo|rag|eval",
  "domain": "sql_debugging",
  "difficulty": "easy|medium|hard",
  "source": "human_curated|synthetic_reviewed|public|project_doc",
  "quality_score": 5,
  "contains_private_data": false,
  "created_at": "YYYY-MM-DD",
  "version": "v1"
}
```

## Required Principles
- Unique ID for every row.
- Explicit source.
- Explicit privacy flag.
- Quality score.
- Dataset version.
