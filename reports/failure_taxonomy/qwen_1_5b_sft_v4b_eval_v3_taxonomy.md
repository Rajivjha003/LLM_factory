# Judge v2 Failure Taxonomy

Eval file: `reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v2.jsonl`
Total samples: 50
Failed samples: 38

| Failure Type | Count | Example IDs |
|---|---:|---|
| required_terms_failure | 38 | bq_debug_v3_001, bq_debug_v3_002, bq_debug_v3_003, bq_debug_v3_004, bq_debug_v3_006, bq_debug_v3_007, bq_debug_v3_009, bq_debug_v3_010 |
| structure_failure | 2 | bq_debug_v3_003, pipeline_debug_v3_006 |
| sql_block_failure | 1 | bq_debug_v3_003 |
| interpretation_failure | 1 | pipeline_debug_v3_006 |

## Recommended Fix Mapping

| Failure Type | Dataset Fix |
|---|---|
| required_terms_failure | Add examples that explicitly include required SQL/business concepts. |
| forbidden_terms_failure | Add safety examples refusing destructive SQL and using preview/backup/validation. |
| sql_block_failure | Add examples with clean fenced SQL blocks. |
| normalization_failure | Add inventory/key examples using TRIM, UPPER, CAST, REGEXP_REPLACE. |
| safety_failure | Add production-safe workflows. |
| interpretation_failure | Add answer explanations that state what query output means. |
| structure_failure | Add concise structured responses with diagnosis, query, interpretation, next step. |