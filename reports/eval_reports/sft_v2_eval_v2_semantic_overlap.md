# Semantic SFT / Eval Overlap Report

Embedding model: `sentence-transformers/all-MiniLM-L6-v2`
Fail threshold: `0.88`

| Eval ID | Best SFT ID | Cosine Similarity | Risk |
|---|---|---:|---|
| bq_debug_v2_001 | bq_debug_user_001 | 0.8043 | OK |
| bq_debug_v2_002 | bq_debug_gen_002 | 0.6111 | OK |
| bq_debug_v2_003 | bq_debug_gen_001 | 0.6969 | OK |
| bq_debug_v2_004 | sql_generation_v2_add_030 | 0.4701 | OK |
| bq_debug_v2_005 | bq_debug_gen_031 | 0.5675 | OK |
| bq_debug_v2_006 | bq_debug_user_001 | 0.8057 | OK |
| bq_debug_v2_007 | bq_debug_user_001 | 0.8058 | OK |
| bq_debug_v2_008 | bq_debug_user_001 | 0.8049 | OK |
| bq_debug_v2_009 | bq_debug_user_001 | 0.8038 | OK |
| bq_debug_v2_010 | bq_debug_user_001 | 0.8012 | OK |
| bq_debug_v2_011 | bq_debug_user_001 | 0.8013 | OK |
| bq_debug_v2_012 | bq_debug_user_001 | 0.8033 | OK |
| pipeline_debug_v2_001 | safety_tool_use_v2_add_005 | 0.5463 | OK |
| pipeline_debug_v2_002 | bq_debug_gen_026 | 0.5185 | OK |
| pipeline_debug_v2_003 | safety_tool_use_v2_add_005 | 0.5654 | OK |
| pipeline_debug_v2_004 | safety_tool_use_v2_add_004 | 0.5647 | OK |
| pipeline_debug_v2_005 | safety_tool_use_v2_add_005 | 0.5664 | OK |
| pg_bq_recon_v2_001 | postgres_bq_reconciliation_v2_add_001 | 0.6564 | OK |
| pg_bq_recon_v2_002 | bq_debug_gen_012 | 0.5138 | OK |
| pg_bq_recon_v2_003 | bq_debug_user_001 | 0.6396 | OK |
| pg_bq_recon_v2_004 | postgres_bq_reconciliation_v2_add_001 | 0.6830 | OK |
| pg_bq_recon_v2_005 | postgres_bq_reconciliation_v2_add_005 | 0.6760 | OK |
| pg_bq_recon_v2_006 | postgres_bq_reconciliation_v2_add_001 | 0.6812 | OK |
| pg_bq_recon_v2_007 | postgres_bq_reconciliation_v2_add_001 | 0.6782 | OK |
| pg_bq_recon_v2_008 | postgres_bq_reconciliation_v2_add_001 | 0.6802 | OK |
| retail_metric_v2_001 | retail_metric_user_001 | 0.7233 | OK |
| retail_metric_v2_002 | retail_metric_gen_008 | 0.6705 | OK |
| retail_metric_v2_003 | retail_metric_user_001 | 0.5944 | OK |
| retail_metric_v2_004 | retail_metric_user_001 | 0.7246 | OK |
| retail_metric_v2_005 | retail_metric_user_001 | 0.7298 | OK |
| retail_metric_v2_006 | retail_metric_user_001 | 0.7298 | OK |
| retail_metric_v2_007 | retail_metric_user_001 | 0.7245 | OK |
| retail_metric_v2_008 | retail_metric_user_001 | 0.7261 | OK |
| safety_tool_v2_001 | bq_debug_gen_003 | 0.6278 | OK |
| safety_tool_v2_002 | safety_tool_use_v2_add_002 | 0.6683 | OK |
| safety_tool_v2_003 | bq_debug_gen_003 | 0.6393 | OK |
| safety_tool_v2_004 | bq_debug_gen_003 | 0.6360 | OK |
| safety_tool_v2_005 | bq_debug_gen_003 | 0.6422 | OK |
| sql_gen_v2_001 | sql_gen_gen_001 | 0.6456 | OK |
| sql_gen_v2_002 | safety_sql_user_001 | 0.8042 | OK |
| sql_gen_v2_003 | safety_sql_user_001 | 0.6686 | OK |
| sql_gen_v2_004 | safety_sql_user_001 | 0.7226 | OK |
| sql_gen_v2_005 | sql_gen_gen_001 | 0.6363 | OK |
| sql_gen_v2_006 | sql_gen_gen_001 | 0.6368 | OK |
| sql_gen_v2_007 | sql_gen_gen_001 | 0.6368 | OK |
| sql_gen_v2_008 | sql_gen_gen_001 | 0.6372 | OK |
| sql_gen_v2_009 | sql_gen_gen_001 | 0.6353 | OK |
| sql_gen_v2_010 | sql_gen_gen_001 | 0.6346 | OK |
| sql_gen_v2_011 | sql_gen_gen_001 | 0.6352 | OK |
| sql_gen_v2_012 | sql_gen_gen_001 | 0.6384 | OK |