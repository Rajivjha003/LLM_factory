# Semantic SFT / Eval Overlap Report

Embedding model: `sentence-transformers/all-MiniLM-L6-v2`
Fail threshold: `0.88`

| Eval ID | Best SFT ID | Cosine Similarity | Risk |
|---|---|---:|---|
| bq_debug_v3_001 | bq_debug_gen_031 | 0.5158 | OK |
| bq_debug_v3_002 | bq_debug_gen_014 | 0.4281 | OK |
| bq_debug_v3_003 | style_response_quality_v2_add_018 | 0.5602 | OK |
| bq_debug_v3_004 | bq_debug_gen_001 | 0.5795 | OK |
| bq_debug_v3_005 | bq_debug_gen_031 | 0.4306 | OK |
| bq_debug_v3_006 | failure_fix_sft_v3_0014 | 0.6342 | OK |
| bq_debug_v3_007 | bq_debug_gen_002 | 0.6162 | OK |
| bq_debug_v3_008 | failure_fix_sft_v3_0035 | 0.7964 | OK |
| bq_debug_v3_009 | failure_fix_sft_v3_0003 | 0.5306 | OK |
| bq_debug_v3_010 | failure_fix_sft_v3_0003 | 0.5464 | OK |
| pipeline_debug_v3_001 | failure_fix_sft_v3_0012 | 0.5229 | OK |
| pipeline_debug_v3_002 | cloud_debug_gen_003 | 0.5322 | OK |
| pipeline_debug_v3_003 | failure_fix_sft_v3_0012 | 0.7009 | OK |
| pipeline_debug_v3_004 | safety_sql_gen_004 | 0.2911 | OK |
| pipeline_debug_v3_005 | failure_fix_sft_v3_0029 | 0.5573 | OK |
| pipeline_debug_v3_006 | bq_debug_gen_003 | 0.4426 | OK |
| pipeline_debug_v3_007 | failure_fix_sft_v3_0013 | 0.3511 | OK |
| pg_bq_v3_001 | failure_fix_sft_v3_0019 | 0.7470 | OK |
| pg_bq_v3_002 | bq_debug_gen_013 | 0.6427 | OK |
| pg_bq_v3_003 | failure_fix_sft_v3_0011 | 0.6214 | OK |
| pg_bq_v3_004 | failure_fix_sft_v3_0017 | 0.6178 | OK |
| pg_bq_v3_005 | bq_debug_user_003 | 0.5453 | OK |
| pg_bq_v3_006 | failure_fix_sft_v3_0013 | 0.7623 | OK |
| pg_bq_v3_007 | postgres_bq_reconciliation_v2_add_033 | 0.5870 | OK |
| pg_bq_v3_008 | bq_debug_gen_001 | 0.4984 | OK |
| retail_metric_v3_001 | retail_metric_gen_008 | 0.6529 | OK |
| retail_metric_v3_002 | failure_fix_sft_v3_0023 | 0.4814 | OK |
| retail_metric_v3_003 | retail_metric_user_001 | 0.3753 | OK |
| retail_metric_v3_004 | retail_metric_gen_002 | 0.5321 | OK |
| retail_metric_v3_005 | retail_metric_reasoning_v2_add_011 | 0.3822 | OK |
| retail_metric_v3_006 | retail_metric_gen_008 | 0.6408 | OK |
| retail_metric_v3_007 | retail_metric_user_001 | 0.4206 | OK |
| retail_metric_v3_008 | failure_fix_sft_v3_0017 | 0.4363 | OK |
| safety_v3_001 | safety_repair_sft_v3_0045 | 0.4428 | OK |
| safety_v3_002 | safety_repair_sft_v3_0048 | 0.5707 | OK |
| safety_v3_003 | failure_fix_sft_v3_0036 | 0.5943 | OK |
| safety_v3_004 | safety_repair_sft_v3_0046 | 0.6968 | OK |
| safety_v3_005 | failure_fix_sft_v3_0002 | 0.4893 | OK |
| safety_v3_006 | bq_debug_gen_015 | 0.4503 | OK |
| safety_v3_007 | safety_repair_sft_v3_0045 | 0.3543 | OK |
| sql_gen_v3_001 | failure_fix_sft_v3_0035 | 0.7429 | OK |
| sql_gen_v3_002 | failure_fix_sft_v3_0002 | 0.6272 | OK |
| sql_gen_v3_003 | failure_fix_sft_v3_0036 | 0.7028 | OK |
| sql_gen_v3_004 | sql_gen_gen_001 | 0.6374 | OK |
| sql_gen_v3_005 | failure_fix_sft_v3_0017 | 0.5288 | OK |
| sql_gen_v3_006 | sql_gen_gen_004 | 0.3149 | OK |
| sql_gen_v3_007 | failure_fix_sft_v3_0002 | 0.5185 | OK |
| sql_gen_v3_008 | failure_fix_sft_v3_0035 | 0.4427 | OK |
| sql_gen_v3_009 | failure_fix_sft_v3_0016 | 0.5256 | OK |
| sql_gen_v3_010 | failure_fix_sft_v3_0035 | 0.6250 | OK |