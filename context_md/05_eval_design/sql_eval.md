# SQL Eval

## Checks
- SQL syntax validity
- Read-only safety
- Correct table grain
- No hallucinated columns
- Uses normalization where needed
- Provides validation query
- Handles null/blank values

## BigQuery-Specific Checks
- Uses SAFE_CAST where appropriate
- Handles backtick table names
- Uses DATE/TIMESTAMP correctly
- Avoids destructive DDL/DML unless asked and approved
