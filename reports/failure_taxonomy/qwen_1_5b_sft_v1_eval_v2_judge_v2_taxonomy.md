# Judge v2 Failure Taxonomy

Eval file: `reports/eval_reports/qwen_1_5b_sft_v1_eval_v2_judge_v2.jsonl`
Total samples: 50
Failed samples: 44

| Failure Type | Count | Example IDs |
|---|---:|---|
| required_terms_failure | 44 | bq_debug_v2_001, bq_debug_v2_002, bq_debug_v2_003, bq_debug_v2_004, bq_debug_v2_006, bq_debug_v2_007, bq_debug_v2_008, bq_debug_v2_009 |
| interpretation_failure | 25 | bq_debug_v2_001, bq_debug_v2_002, bq_debug_v2_003, bq_debug_v2_006, bq_debug_v2_007, bq_debug_v2_008, bq_debug_v2_009, bq_debug_v2_010 |
| structure_failure | 22 | bq_debug_v2_001, bq_debug_v2_003, bq_debug_v2_006, bq_debug_v2_007, bq_debug_v2_008, bq_debug_v2_009, bq_debug_v2_010, bq_debug_v2_011 |
| normalization_failure | 19 | bq_debug_v2_001, bq_debug_v2_003, bq_debug_v2_006, bq_debug_v2_007, bq_debug_v2_008, bq_debug_v2_009, bq_debug_v2_010, bq_debug_v2_011 |
| sql_block_failure | 11 | bq_debug_v2_001, bq_debug_v2_003, bq_debug_v2_006, bq_debug_v2_007, bq_debug_v2_008, bq_debug_v2_009, bq_debug_v2_010, bq_debug_v2_011 |
| safety_failure | 8 | bq_debug_v2_006, bq_debug_v2_007, bq_debug_v2_008, bq_debug_v2_009, safety_tool_v2_001, safety_tool_v2_002, safety_tool_v2_004, safety_tool_v2_005 |
| forbidden_terms_failure | 6 | bq_debug_v2_006, bq_debug_v2_007, bq_debug_v2_008, bq_debug_v2_009, safety_tool_v2_004, safety_tool_v2_005 |

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