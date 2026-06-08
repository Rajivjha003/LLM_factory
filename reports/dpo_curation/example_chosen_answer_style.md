# Example Chosen Answer Style

Use this style when filling `CHOSEN_ANSWER` blocks.

```text
Start with the diagnosis.

Then provide safe read-only SQL:

```sql
WITH ...
SELECT ...
```

Interpretation:
- Explain exactly what returned rows mean.
- Explain what to check next.
- Mention production safety if relevant.

Next steps:
1. Validate grain.
2. Compare counts.
3. Check source freshness / watermark.
4. Use preview/backup before replacing production.
```

Never write chosen answers that are just:
- "The answer should include..."
- "Need to mention..."
- "Use SQL..."

DPO chosen answers must be full assistant responses.
