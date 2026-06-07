# Judge v2 Threshold Audit

Eval file: `reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v2.jsonl`
Rows: 50

## Category Averages

| Category | Average | Min | Max | Perfect Count |
|---|---:|---:|---:|---:|
| required_terms_score | 0.590 | 0.000 | 1.000 | 17/50 |
| forbidden_terms_score | 1.000 | 1.000 | 1.000 | 50/50 |
| sql_block_score | 1.000 | 1.000 | 1.000 | 50/50 |
| normalization_score | 1.000 | 1.000 | 1.000 | 50/50 |
| safety_score | 1.000 | 1.000 | 1.000 | 50/50 |
| interpretation_score | 1.000 | 1.000 | 1.000 | 50/50 |
| structure_score | 1.000 | 1.000 | 1.000 | 50/50 |

## Suspicious Cases

- Failed but score_rate >= 0.90: 13
- Passed but score_rate < 0.80: 0

### Failed But Near Perfect

| ID | Score Rate | Missing Required | Feedback |
|---|---:|---|---|
| bq_debug_v3_004 | 0.941 | ['REGEXP_REPLACE'] | ["Missing required terms: ['REGEXP_REPLACE']"] |
| bq_debug_v3_006 | 0.941 | ['inactive'] | ["Missing required terms: ['inactive']"] |
| bq_debug_v3_009 | 0.941 | ['LastModified'] | ["Missing required terms: ['LastModified']"] |
| pipeline_debug_v3_001 | 0.941 | ['schema'] | ["Missing required terms: ['schema']"] |
| pg_bq_v3_001 | 0.941 | ['OrderNbr'] | ["Missing required terms: ['OrderNbr']"] |
| pg_bq_v3_002 | 0.941 | ['timezone'] | ["Missing required terms: ['timezone']"] |
| pg_bq_v3_003 | 0.941 | ['Item Status'] | ["Missing required terms: ['Item Status']"] |
| retail_metric_v3_002 | 0.941 | ['stock'] | ["Missing required terms: ['stock']"] |
| retail_metric_v3_006 | 0.941 | ['sold'] | ["Missing required terms: ['sold']"] |
| sql_gen_v3_004 | 0.912 | ['LEFT JOIN', 'IS NULL'] | ["Missing required terms: ['LEFT JOIN', 'IS NULL']"] |
| sql_gen_v3_005 | 0.956 | ['WITH'] | ["Missing required terms: ['WITH']"] |
| sql_gen_v3_007 | 0.912 | ['OrderNbr', 'LineNbr'] | ["Missing required terms: ['OrderNbr', 'LineNbr']"] |
| sql_gen_v3_009 | 0.912 | ['EXCEPT DISTINCT', 'UNION ALL'] | ["Missing required terms: ['EXCEPT DISTINCT', 'UNION ALL']"] |

### Passed But Low Score

| ID | Score Rate | Feedback |
|---|---:|---|