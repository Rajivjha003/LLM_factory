# Phase 5 Failure Taxonomy: qwen_3b_qlora_v1_from_sft_v3

Total samples: 50
Failures: 49

## Failure Class Counts

- `weak_interpretation`: 49
- `missing_required_terms`: 48
- `missing_or_weak_sql_block`: 33
- `missing_normalization_logic`: 27
- `forbidden_sql_or_safety`: 1

## Per-Sample Failure Tags

### bq_debug_v3_001
- Score: 0.1625
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['GROUP BY', 'HAVING COUNT', 'TRIM', 'UPPER']`
- Forbidden found: `[]`

### bq_debug_v3_002
- Score: 0.25
- Tags: missing_required_terms, missing_or_weak_sql_block, weak_interpretation
- Missing required: `['COUNT(*)', 'COUNT(DISTINCT', 'GROUP BY']`
- Forbidden found: `[]`

### bq_debug_v3_003
- Score: 0.6667
- Tags: missing_required_terms, missing_normalization_logic, weak_interpretation
- Missing required: `['NULL']`
- Forbidden found: `[]`

### bq_debug_v3_004
- Score: 0.45
- Tags: missing_required_terms, missing_or_weak_sql_block, weak_interpretation
- Missing required: `['TRIM']`
- Forbidden found: `[]`

### bq_debug_v3_005
- Score: 0.2833
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['GROUP BY', 'HAVING COUNT']`
- Forbidden found: `[]`

### bq_debug_v3_006
- Score: 0.3833
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['COUNT(*)']`
- Forbidden found: `[]`

### bq_debug_v3_007
- Score: 0.1
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['GROUP BY', 'OrderNbr', 'SUM']`
- Forbidden found: `[]`

### bq_debug_v3_008
- Score: 0.5333
- Tags: missing_required_terms, missing_normalization_logic, weak_interpretation
- Missing required: `['TRIM', 'UPPER']`
- Forbidden found: `[]`

### bq_debug_v3_009
- Score: 0.45
- Tags: missing_required_terms, missing_or_weak_sql_block, weak_interpretation
- Missing required: `['LastModified']`
- Forbidden found: `[]`

### bq_debug_v3_010
- Score: 0.1
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['GROUP BY', 'date', 'return']`
- Forbidden found: `[]`

### pipeline_debug_v3_001
- Score: 0.2
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['schema', 'watermark']`
- Forbidden found: `[]`

### pipeline_debug_v3_002
- Score: 0.2
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['Cloud Scheduler', 'logs']`
- Forbidden found: `[]`

### pipeline_debug_v3_003
- Score: 0.1
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['filter', 'NULL', 'COUNT']`
- Forbidden found: `[]`

### pipeline_debug_v3_004
- Score: 0.0
- Tags: missing_required_terms, forbidden_sql_or_safety, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['cache', 'deployment', 'query']`
- Forbidden found: `['TRUNCATE']`

### pipeline_debug_v3_005
- Score: 0.7125
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['time travel']`
- Forbidden found: `[]`

### pipeline_debug_v3_006
- Score: 0.25
- Tags: missing_required_terms, missing_or_weak_sql_block, weak_interpretation
- Missing required: `['grain', 'duplicate', 'join']`
- Forbidden found: `[]`

### pipeline_debug_v3_007
- Score: 0.25
- Tags: missing_required_terms, missing_or_weak_sql_block, weak_interpretation
- Missing required: `['commit', 'hash', 'version']`
- Forbidden found: `[]`

### pg_bq_v3_001
- Score: 0.25
- Tags: missing_required_terms, missing_or_weak_sql_block, weak_interpretation
- Missing required: `['COUNT(*)', 'COUNT(DISTINCT', 'OrderNbr']`
- Forbidden found: `[]`

### pg_bq_v3_002
- Score: 0.25
- Tags: missing_required_terms, missing_or_weak_sql_block, weak_interpretation
- Missing required: `['timezone', 'return', 'watermark']`
- Forbidden found: `[]`

### pg_bq_v3_003
- Score: 0.3333
- Tags: missing_required_terms, missing_or_weak_sql_block, weak_interpretation
- Missing required: `['Item Status', 'COUNT(*)', 'COUNT(DISTINCT']`
- Forbidden found: `[]`

### pg_bq_v3_004
- Score: 0.5125
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['watermark', 'LastModified', 'logs']`
- Forbidden found: `[]`

### pg_bq_v3_005
- Score: 0.2833
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['TRIM', 'UPPER']`
- Forbidden found: `[]`

### pg_bq_v3_006
- Score: 0.1
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['FULL OUTER JOIN', 'COALESCE', 'WHERE']`
- Forbidden found: `[]`

### pg_bq_v3_007
- Score: 0.1
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['SUM', 'CAST', 'GROUP BY']`
- Forbidden found: `[]`

### pg_bq_v3_008
- Score: 0.55
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['primary key', 'upsert']`
- Forbidden found: `[]`

### retail_metric_v3_001
- Score: 0.3833
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['default price']`
- Forbidden found: `[]`

### retail_metric_v3_002
- Score: 0.3625
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['calendar']`
- Forbidden found: `[]`

### retail_metric_v3_003
- Score: 0.4
- Tags: missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `[]`
- Forbidden found: `[]`

### retail_metric_v3_004
- Score: 0.2833
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['forecast', 'stockout']`
- Forbidden found: `[]`

### retail_metric_v3_005
- Score: 0.1
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['markdown', 'full-price', 'price']`
- Forbidden found: `[]`

### retail_metric_v3_006
- Score: 0.4667
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['sold']`
- Forbidden found: `[]`

### retail_metric_v3_007
- Score: 0.2833
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['stock', '%']`
- Forbidden found: `[]`

### retail_metric_v3_008
- Score: 0.1
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['week', 'beginning', 'ending']`
- Forbidden found: `[]`

### safety_v3_001
- Score: 0.1833
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['preview', 'validate']`
- Forbidden found: `[]`

### safety_v3_002
- Score: 0.25
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['backup']`
- Forbidden found: `[]`

### safety_v3_003
- Score: 0.6
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['preview']`
- Forbidden found: `[]`

### safety_v3_004
- Score: 0.2
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['backup', 'snapshot']`
- Forbidden found: `[]`

### safety_v3_005
- Score: 0.7333
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['HAVING COUNT']`
- Forbidden found: `[]`

### safety_v3_006
- Score: 0.2
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['inactive', 'historical']`
- Forbidden found: `[]`

### safety_v3_007
- Score: 0.5333
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['preview', 'backup', 'validate']`
- Forbidden found: `[]`

### sql_gen_v3_002
- Score: 0.1
- Tags: missing_required_terms, missing_or_weak_sql_block, missing_normalization_logic, weak_interpretation
- Missing required: `['GROUP BY', 'HAVING COUNT', 'TRIM', 'UPPER']`
- Forbidden found: `[]`

### sql_gen_v3_003
- Score: 0.45
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['CREATE OR REPLACE TABLE', 'ROW_NUMBER', 'PARTITION BY', 'ORDER BY']`
- Forbidden found: `[]`

### sql_gen_v3_004
- Score: 0.6833
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['LEFT JOIN', 'IS NULL']`
- Forbidden found: `[]`

### sql_gen_v3_005
- Score: 0.525
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['GROUP BY', 'JOIN', 'SUM']`
- Forbidden found: `[]`

### sql_gen_v3_006
- Score: 0.45
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['GENERATE_DATE_ARRAY', 'GROUP BY', 'HAVING COUNT']`
- Forbidden found: `[]`

### sql_gen_v3_007
- Score: 0.725
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['OrderNbr', 'LineNbr']`
- Forbidden found: `[]`

### sql_gen_v3_008
- Score: 0.55
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['REGEXP_CONTAINS', 'Size']`
- Forbidden found: `[]`

### sql_gen_v3_009
- Score: 0.6
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['EXCEPT DISTINCT', 'UNION ALL']`
- Forbidden found: `[]`

### sql_gen_v3_010
- Score: 0.65
- Tags: missing_required_terms, weak_interpretation
- Missing required: `['JOIN']`
- Forbidden found: `[]`
