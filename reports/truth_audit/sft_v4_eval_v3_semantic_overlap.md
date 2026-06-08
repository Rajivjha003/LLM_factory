# Semantic SFT / Eval Overlap Report

Embedding model: `sentence-transformers/all-MiniLM-L6-v2`
Fail threshold: `0.88`

| Eval ID | Best SFT ID | Cosine Similarity | Risk |
|---|---|---:|---|
| bq_debug_v3_001 | bq_debug_gen_031 | 0.5158 | OK |
| bq_debug_v3_002 | bq_debug_gen_003 | 0.4281 | OK |
| bq_debug_v3_003 | rubric_sft_v4_0009 | 0.8253 | OK |
| bq_debug_v3_004 | rubric_sft_v4_0002 | 0.6188 | OK |
| bq_debug_v3_005 | rubric_sft_v4_0005 | 0.8628 | OK |
| bq_debug_v3_006 | failure_fix_sft_v3_0014 | 0.6342 | OK |
| bq_debug_v3_007 | bq_debug_gen_002 | 0.6162 | OK |
| bq_debug_v3_008 | failure_fix_sft_v3_0035 | 0.7964 | OK |
| bq_debug_v3_009 | failure_fix_sft_v3_0003 | 0.5306 | OK |
| bq_debug_v3_010 | failure_fix_sft_v3_0003 | 0.5464 | OK |
| pipeline_debug_v3_001 | rubric_sft_v4_0058 | 0.6880 | OK |
| pipeline_debug_v3_002 | rubric_sft_v4_0008 | 0.8009 | OK |
| pipeline_debug_v3_003 | failure_fix_sft_v3_0012 | 0.7009 | OK |
| pipeline_debug_v3_004 | safety_sql_gen_001 | 0.2911 | OK |
| pipeline_debug_v3_005 | failure_fix_sft_v3_0029 | 0.5573 | OK |
| pipeline_debug_v3_006 | rubric_sft_v4_0058 | 0.6038 | OK |
| pipeline_debug_v3_007 | failure_fix_sft_v3_0013 | 0.3511 | OK |
| pg_bq_v3_001 | failure_fix_sft_v3_0019 | 0.7470 | OK |
| pg_bq_v3_002 | bq_debug_gen_013 | 0.6427 | OK |
| pg_bq_v3_003 | failure_fix_sft_v3_0011 | 0.6214 | OK |
| pg_bq_v3_004 | failure_fix_sft_v3_0017 | 0.6178 | OK |
| pg_bq_v3_005 | rubric_sft_v4_0021 | 0.6117 | OK |
| pg_bq_v3_006 | failure_fix_sft_v3_0013 | 0.7623 | OK |
| pg_bq_v3_007 | postgres_bq_reconciliation_v2_add_033 | 0.5870 | OK |
| pg_bq_v3_008 | bq_debug_gen_001 | 0.4984 | OK |
| retail_metric_v3_001 | retail_metric_gen_008 | 0.6529 | OK |
| retail_metric_v3_002 | rubric_sft_v4_0006 | 0.6175 | OK |
| retail_metric_v3_003 | retail_metric_user_001 | 0.3753 | OK |
| retail_metric_v3_004 | retail_metric_gen_004 | 0.5321 | OK |
| retail_metric_v3_005 | retail_metric_reasoning_v2_add_011 | 0.3822 | OK |
| retail_metric_v3_006 | retail_metric_gen_008 | 0.6408 | OK |
| retail_metric_v3_007 | retail_metric_user_001 | 0.4206 | OK |
| retail_metric_v3_008 | rubric_sft_v4_0005 | 0.6356 | OK |
| safety_v3_001 | safety_repair_sft_v3_0200 | 0.4428 | OK |
| safety_v3_002 | rubric_sft_v4_0047 | 0.6086 | OK |
| safety_v3_003 | failure_fix_sft_v3_0036 | 0.5943 | OK |
| safety_v3_004 | rubric_sft_v4_0007 | 0.7158 | OK |
| safety_v3_005 | failure_fix_sft_v3_0002 | 0.4893 | OK |
| safety_v3_006 | rubric_sft_v4_0107 | 0.7972 | OK |
| safety_v3_007 | real_sft_v4_added_028 | 0.5133 | OK |
| sql_gen_v3_001 | failure_fix_sft_v3_0035 | 0.7429 | OK |
| sql_gen_v3_002 | failure_fix_sft_v3_0002 | 0.6272 | OK |
| sql_gen_v3_003 | rubric_sft_v4_0017 | 0.7425 | OK |
| sql_gen_v3_004 | sql_gen_gen_001 | 0.6374 | OK |
| sql_gen_v3_005 | rubric_sft_v4_0041 | 0.5403 | OK |
| sql_gen_v3_006 | rubric_sft_v4_0005 | 0.5289 | OK |
| sql_gen_v3_007 | failure_fix_sft_v3_0002 | 0.5185 | OK |
| sql_gen_v3_008 | failure_fix_sft_v3_0035 | 0.4427 | OK |
| sql_gen_v3_009 | failure_fix_sft_v3_0016 | 0.5256 | OK |
| sql_gen_v3_010 | rubric_sft_v4_0017 | 0.6434 | OK |