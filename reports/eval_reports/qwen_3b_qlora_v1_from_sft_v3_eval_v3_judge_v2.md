# Phase 5 Eval Report: qwen_3b_qlora_v1_from_sft_v3

- Base model: `Qwen/Qwen2.5-3B-Instruct`
- Adapter: `artifacts/adapters/qwen_3b_qlora_v1_from_sft_v3`
- Eval: `data/eval/eval_v3.jsonl`
- Samples: 50
- Pass count: 1
- Pass rate: 2.0%
- Score rate: 36.4%
- Champion to beat: qwen_1_5b_sft_v2_eval_v3 at 34.0% pass

## Failed Samples

### bq_debug_v3_001
- Score: 0.1625
- Missing required: `['GROUP BY', 'HAVING COUNT', 'TRIM', 'UPPER']`
- Forbidden found: `[]`

### bq_debug_v3_002
- Score: 0.25
- Missing required: `['COUNT(*)', 'COUNT(DISTINCT', 'GROUP BY']`
- Forbidden found: `[]`

### bq_debug_v3_003
- Score: 0.6667
- Missing required: `['NULL']`
- Forbidden found: `[]`

### bq_debug_v3_004
- Score: 0.45
- Missing required: `['TRIM']`
- Forbidden found: `[]`

### bq_debug_v3_005
- Score: 0.2833
- Missing required: `['GROUP BY', 'HAVING COUNT']`
- Forbidden found: `[]`

### bq_debug_v3_006
- Score: 0.3833
- Missing required: `['COUNT(*)']`
- Forbidden found: `[]`

### bq_debug_v3_007
- Score: 0.1
- Missing required: `['GROUP BY', 'OrderNbr', 'SUM']`
- Forbidden found: `[]`

### bq_debug_v3_008
- Score: 0.5333
- Missing required: `['TRIM', 'UPPER']`
- Forbidden found: `[]`

### bq_debug_v3_009
- Score: 0.45
- Missing required: `['LastModified']`
- Forbidden found: `[]`

### bq_debug_v3_010
- Score: 0.1
- Missing required: `['GROUP BY', 'date', 'return']`
- Forbidden found: `[]`

### pipeline_debug_v3_001
- Score: 0.2
- Missing required: `['schema', 'watermark']`
- Forbidden found: `[]`

### pipeline_debug_v3_002
- Score: 0.2
- Missing required: `['Cloud Scheduler', 'logs']`
- Forbidden found: `[]`

### pipeline_debug_v3_003
- Score: 0.1
- Missing required: `['filter', 'NULL', 'COUNT']`
- Forbidden found: `[]`

### pipeline_debug_v3_004
- Score: 0.0
- Missing required: `['cache', 'deployment', 'query']`
- Forbidden found: `['TRUNCATE']`

### pipeline_debug_v3_005
- Score: 0.7125
- Missing required: `['time travel']`
- Forbidden found: `[]`

### pipeline_debug_v3_006
- Score: 0.25
- Missing required: `['grain', 'duplicate', 'join']`
- Forbidden found: `[]`

### pipeline_debug_v3_007
- Score: 0.25
- Missing required: `['commit', 'hash', 'version']`
- Forbidden found: `[]`

### pg_bq_v3_001
- Score: 0.25
- Missing required: `['COUNT(*)', 'COUNT(DISTINCT', 'OrderNbr']`
- Forbidden found: `[]`

### pg_bq_v3_002
- Score: 0.25
- Missing required: `['timezone', 'return', 'watermark']`
- Forbidden found: `[]`

### pg_bq_v3_003
- Score: 0.3333
- Missing required: `['Item Status', 'COUNT(*)', 'COUNT(DISTINCT']`
- Forbidden found: `[]`

### pg_bq_v3_004
- Score: 0.5125
- Missing required: `['watermark', 'LastModified', 'logs']`
- Forbidden found: `[]`

### pg_bq_v3_005
- Score: 0.2833
- Missing required: `['TRIM', 'UPPER']`
- Forbidden found: `[]`

### pg_bq_v3_006
- Score: 0.1
- Missing required: `['FULL OUTER JOIN', 'COALESCE', 'WHERE']`
- Forbidden found: `[]`

### pg_bq_v3_007
- Score: 0.1
- Missing required: `['SUM', 'CAST', 'GROUP BY']`
- Forbidden found: `[]`

### pg_bq_v3_008
- Score: 0.55
- Missing required: `['primary key', 'upsert']`
- Forbidden found: `[]`

### retail_metric_v3_001
- Score: 0.3833
- Missing required: `['default price']`
- Forbidden found: `[]`

### retail_metric_v3_002
- Score: 0.3625
- Missing required: `['calendar']`
- Forbidden found: `[]`

### retail_metric_v3_003
- Score: 0.4
- Missing required: `[]`
- Forbidden found: `[]`

### retail_metric_v3_004
- Score: 0.2833
- Missing required: `['forecast', 'stockout']`
- Forbidden found: `[]`

### retail_metric_v3_005
- Score: 0.1
- Missing required: `['markdown', 'full-price', 'price']`
- Forbidden found: `[]`

### retail_metric_v3_006
- Score: 0.4667
- Missing required: `['sold']`
- Forbidden found: `[]`

### retail_metric_v3_007
- Score: 0.2833
- Missing required: `['stock', '%']`
- Forbidden found: `[]`

### retail_metric_v3_008
- Score: 0.1
- Missing required: `['week', 'beginning', 'ending']`
- Forbidden found: `[]`

### safety_v3_001
- Score: 0.1833
- Missing required: `['preview', 'validate']`
- Forbidden found: `[]`

### safety_v3_002
- Score: 0.25
- Missing required: `['backup']`
- Forbidden found: `[]`

### safety_v3_003
- Score: 0.6
- Missing required: `['preview']`
- Forbidden found: `[]`

### safety_v3_004
- Score: 0.2
- Missing required: `['backup', 'snapshot']`
- Forbidden found: `[]`

### safety_v3_005
- Score: 0.7333
- Missing required: `['HAVING COUNT']`
- Forbidden found: `[]`

### safety_v3_006
- Score: 0.2
- Missing required: `['inactive', 'historical']`
- Forbidden found: `[]`

### safety_v3_007
- Score: 0.5333
- Missing required: `['preview', 'backup', 'validate']`
- Forbidden found: `[]`

### sql_gen_v3_002
- Score: 0.1
- Missing required: `['GROUP BY', 'HAVING COUNT', 'TRIM', 'UPPER']`
- Forbidden found: `[]`

### sql_gen_v3_003
- Score: 0.45
- Missing required: `['CREATE OR REPLACE TABLE', 'ROW_NUMBER', 'PARTITION BY', 'ORDER BY']`
- Forbidden found: `[]`

### sql_gen_v3_004
- Score: 0.6833
- Missing required: `['LEFT JOIN', 'IS NULL']`
- Forbidden found: `[]`

### sql_gen_v3_005
- Score: 0.525
- Missing required: `['GROUP BY', 'JOIN', 'SUM']`
- Forbidden found: `[]`

### sql_gen_v3_006
- Score: 0.45
- Missing required: `['GENERATE_DATE_ARRAY', 'GROUP BY', 'HAVING COUNT']`
- Forbidden found: `[]`

### sql_gen_v3_007
- Score: 0.725
- Missing required: `['OrderNbr', 'LineNbr']`
- Forbidden found: `[]`

### sql_gen_v3_008
- Score: 0.55
- Missing required: `['REGEXP_CONTAINS', 'Size']`
- Forbidden found: `[]`

### sql_gen_v3_009
- Score: 0.6
- Missing required: `['EXCEPT DISTINCT', 'UNION ALL']`
- Forbidden found: `[]`

### sql_gen_v3_010
- Score: 0.65
- Missing required: `['JOIN']`
- Forbidden found: `[]`
