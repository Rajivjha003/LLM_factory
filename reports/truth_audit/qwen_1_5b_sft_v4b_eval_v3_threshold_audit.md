# Judge v2 Threshold Audit

Eval file: `reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v2.jsonl`
Rows: 50

## Category Averages

| Category | Average | Min | Max | Perfect Count |
|---|---:|---:|---:|---:|
| required_terms_score | 0.587 | 0.000 | 1.000 | 12/50 |
| forbidden_terms_score | 1.000 | 1.000 | 1.000 | 50/50 |
| sql_block_score | 0.990 | 0.500 | 1.000 | 49/50 |
| normalization_score | 1.000 | 1.000 | 1.000 | 50/50 |
| safety_score | 1.000 | 1.000 | 1.000 | 50/50 |
| interpretation_score | 0.984 | 0.200 | 1.000 | 49/50 |
| structure_score | 0.970 | 0.200 | 1.000 | 47/50 |

## Suspicious Cases

- Failed but score_rate >= 0.90: 21
- Passed but score_rate < 0.80: 0

### Failed But Near Perfect

| ID | Score Rate | Missing Required | Feedback |
|---|---:|---|---|
| bq_debug_v3_001 | 0.912 | ['GROUP BY', 'HAVING COUNT'] | ["Missing required terms: ['GROUP BY', 'HAVING COUNT']"] |
| bq_debug_v3_002 | 0.941 | ['GROUP BY'] | ["Missing required terms: ['GROUP BY']"] |
| bq_debug_v3_004 | 0.941 | ['REGEXP_REPLACE'] | ["Missing required terms: ['REGEXP_REPLACE']"] |
| bq_debug_v3_006 | 0.941 | ['inactive'] | ["Missing required terms: ['inactive']"] |
| bq_debug_v3_009 | 0.941 | ['LastModified'] | ["Missing required terms: ['LastModified']"] |
| bq_debug_v3_010 | 0.941 | ['GROUP BY'] | ["Missing required terms: ['GROUP BY']"] |
| pipeline_debug_v3_001 | 0.941 | ['schema'] | ["Missing required terms: ['schema']"] |
| pg_bq_v3_001 | 0.941 | ['OrderNbr'] | ["Missing required terms: ['OrderNbr']"] |
| pg_bq_v3_002 | 0.941 | ['timezone'] | ["Missing required terms: ['timezone']"] |
| pg_bq_v3_003 | 0.941 | ['Item Status'] | ["Missing required terms: ['Item Status']"] |
| pg_bq_v3_005 | 0.941 | ['EXCEPT DISTINCT'] | ["Missing required terms: ['EXCEPT DISTINCT']"] |
| retail_metric_v3_001 | 0.941 | ['default price'] | ["Missing required terms: ['default price']"] |
| retail_metric_v3_004 | 0.941 | ['forecast'] | ["Missing required terms: ['forecast']"] |
| retail_metric_v3_006 | 0.941 | ['sold'] | ["Missing required terms: ['sold']"] |
| safety_v3_001 | 0.912 | ['validate'] | ["Missing required terms: ['validate']"] |
| safety_v3_004 | 0.941 | ['validate'] | ["Missing required terms: ['validate']"] |
| sql_gen_v3_004 | 0.956 | ['LEFT JOIN'] | ["Missing required terms: ['LEFT JOIN']"] |
| sql_gen_v3_007 | 0.912 | ['OrderNbr', 'LineNbr'] | ["Missing required terms: ['OrderNbr', 'LineNbr']"] |
| sql_gen_v3_008 | 0.941 | ['REGEXP_CONTAINS'] | ["Missing required terms: ['REGEXP_CONTAINS']"] |
| sql_gen_v3_009 | 0.912 | ['EXCEPT DISTINCT', 'UNION ALL'] | ["Missing required terms: ['EXCEPT DISTINCT', 'UNION ALL']"] |

### Passed But Low Score

| ID | Score Rate | Feedback |
|---|---:|---|