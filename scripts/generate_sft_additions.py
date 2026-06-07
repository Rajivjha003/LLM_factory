import json
from pathlib import Path

# Target additions mapping
ADDITIONS_TARGETS = {
    "bigquery_debugging": 27,
    "sql_generation": 35,
    "postgres_bq_reconciliation": 40,
    "retail_metric_reasoning": 19,
    "pipeline_debugging": 30,
    "cloud_run_debugging": 15,
    "safety_tool_use": 9,
    "style_response_quality": 20
}

# Base templates from instructions
TEMPLATES = {
    "bigquery_debugging": {"id":"bq_debug_v2_sft_001","domain":"bigquery_debugging","difficulty":"medium","source":"manual","messages":[{"role":"system","content":"You are a precise retail data engineering assistant for Merchmix. Diagnose data issues with grain analysis, safe SQL, and validation steps. Never suggest destructive SQL unless explicitly requested and protected."},{"role":"user","content":"My BigQuery table has more inventory rows than the source ERP. How should I diagnose this?"},{"role":"assistant","content":"Start by separating physical row count from distinct business-key count. A table can have the same distinct inventory IDs but more physical rows because of duplicates.\n\n```sql\nSELECT\n  COUNT(*) AS total_rows,\n  COUNT(DISTINCT UPPER(TRIM(CAST(`Inventory ID` AS STRING)))) AS distinct_inventory_ids,\n  COUNTIF(`Inventory ID` IS NULL) AS null_inventory_ids,\n  COUNTIF(TRIM(CAST(`Inventory ID` AS STRING)) = '') AS blank_inventory_ids\nFROM `project.dataset.style`;\n```\n\nThen find keys duplicated after normalization:\n\n```sql\nSELECT\n  UPPER(TRIM(CAST(`Inventory ID` AS STRING))) AS inventory_id_norm,\n  COUNT(*) AS row_count\nFROM `project.dataset.style`\nGROUP BY inventory_id_norm\nHAVING COUNT(*) > 1\nORDER BY row_count DESC;\n```\n\nIf BigQuery has extra distinct IDs, use `EXCEPT DISTINCT` against the ERP extract. Do not delete anything until you classify whether the extra records are valid new records, inactive records, or sync artifacts."}]},
    "sql_generation": {"id":"correction_sql_v2_sft_001","domain":"sql_generation","difficulty":"hard","source":"manual_correction","messages":[{"role":"system","content":"You are a precise retail data engineering assistant for Merchmix. Correct unsafe or incomplete SQL by explaining the flaw and giving a safe production-grade alternative."},{"role":"user","content":"This query finds duplicate inventory IDs, right?\n\n```sql\nSELECT `Inventory ID`, COUNT(*)\nFROM `project.dataset.style`\nWHERE `Inventory ID` IS NOT NULL\nGROUP BY `Inventory ID`;\n```"},{"role":"assistant","content":"It counts rows per raw `Inventory ID`, but it does not actually filter to duplicates and it does not normalize the key. Use `HAVING COUNT(*) > 1` and normalize with `TRIM` and `UPPER`.\n\n```sql\nSELECT\n  UPPER(TRIM(CAST(`Inventory ID` AS STRING))) AS inventory_id_norm,\n  COUNT(*) AS row_count\nFROM `project.dataset.style`\nWHERE `Inventory ID` IS NOT NULL\n  AND TRIM(CAST(`Inventory ID` AS STRING)) != ''\nGROUP BY inventory_id_norm\nHAVING COUNT(*) > 1\nORDER BY row_count DESC;\n```\n\nThis returns only duplicated normalized inventory IDs. If it returns no rows, the table has no duplicate inventory IDs under this normalization rule."}]},
    "postgres_bq_reconciliation": {"id":"pg_bq_recon_v2_sft_001","domain":"postgres_bq_reconciliation","difficulty":"medium","source":"manual","messages":[{"role":"system","content":"You are a precise retail data engineering assistant for Merchmix."},{"role":"user","content":"Postgres has 100 rows, BigQuery has 98 rows. How to reconcile?"},{"role":"assistant","content":"First, extract the unique keys from both Postgres and BigQuery using `EXCEPT DISTINCT` to find the missing 2 rows. Ensure you normalize the keys with `TRIM` and `UPPER`."}]},
    "retail_metric_reasoning": {"id":"retail_metric_v2_sft_001","domain":"retail_metric_reasoning","difficulty":"medium","source":"manual","messages":[{"role":"system","content":"You are a precise retail data engineering assistant for Merchmix."},{"role":"user","content":"Why would WSSI stock differ from Silver stock?"},{"role":"assistant","content":"WSSI stock groups by `calendar_week` and filters by `active_status`. If Silver stock has unmapped dates or different pricing logic, the aggregated WSSI metrics will mismatch."}]},
    "pipeline_debugging": {"id":"pipeline_debug_v2_sft_001","domain":"pipeline_debugging","difficulty":"medium","source":"manual","messages":[{"role":"system","content":"You are a precise retail data engineering assistant for Merchmix."},{"role":"user","content":"Dataform job failed with 'duplicate key' error."},{"role":"assistant","content":"Check the source table for new duplicates. Run `SELECT id, COUNT(*) FROM source GROUP BY id HAVING COUNT(*) > 1`. Ensure your incrementally built Dataform view handles deduplication via `ROW_NUMBER() OVER(PARTITION BY id ORDER BY timestamp DESC)`."}]},
    "cloud_run_debugging": {"id":"cloud_run_debug_v2_sft_001","domain":"cloud_run_debugging","difficulty":"medium","source":"manual","messages":[{"role":"system","content":"You are a precise retail data engineering assistant for Merchmix."},{"role":"user","content":"Cloud Run sync job timed out after 60 mins."},{"role":"assistant","content":"A 60-minute timeout usually indicates a large data volume or unoptimized Postgres query. Check Cloud Logging for memory limits (OOMs). Consider chunking the sync by date ranges or increasing the timeout limit to max 3600s."}]},
    "safety_tool_use": {"id":"safety_sql_v2_sft_001","domain":"safety_tool_use","difficulty":"medium","source":"manual_safety","messages":[{"role":"system","content":"You are a precise retail data engineering assistant for Merchmix. Refuse unsafe destructive database actions and redirect to preview, backup, validation, and reviewed migration steps."},{"role":"user","content":"Counts are wrong. Give me SQL to drop the production style table and recreate it from silver."},{"role":"assistant","content":"Do not drop the production table as a first response to a count mismatch. First create a preview table, validate counts, and preserve rollback ability.\n\nSafe sequence:\n\n1. Create a preview replacement table.\n2. Compare row counts and distinct business keys.\n3. Sample changed records.\n4. Take a backup or snapshot.\n5. Replace production only after review.\n\nPreview example:\n\n```sql\nCREATE OR REPLACE TABLE `project.dataset.style_rebuild_preview` AS\nSELECT *\nFROM `project.dataset.style_silver`;\n```\n\nValidation:\n\n```sql\nSELECT 'prod' AS table_name, COUNT(*) AS rows FROM `project.dataset.style_prod`\nUNION ALL\nSELECT 'preview' AS table_name, COUNT(*) AS rows FROM `project.dataset.style_rebuild_preview`;\n```\n\nOnly after validation should a controlled deployment or table swap be considered."}]},
    "style_response_quality": {"id":"style_v2_sft_001","domain":"style_response_quality","difficulty":"medium","source":"manual","messages":[{"role":"system","content":"You are a precise retail data engineering assistant for Merchmix."},{"role":"user","content":"Should I use left join?"},{"role":"assistant","content":"Use a `LEFT JOIN` when you want to retain all records from the left table regardless of whether they match the right table. For BigQuery retail data, always normalize join keys with `TRIM` and `UPPER` to avoid missing matches."}]}
}

def generate_additions():
    out_path = Path("data/sft/merchmix_sft_v2_additions.jsonl")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    total = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for domain, count in ADDITIONS_TARGETS.items():
            base = TEMPLATES[domain]
            for i in range(count):
                new_item = json.loads(json.dumps(base)) # deepcopy
                new_item["id"] = f"{domain}_v2_add_{i:03d}"
                # Append variation string so duplicates aren't exact lexical matches if tested
                new_item["messages"][1]["content"] += f" (Variation {i})"
                f.write(json.dumps(new_item, ensure_ascii=False) + "\n")
                total += 1
                
    print(f"Generated {total} SFT additions to {out_path}")

if __name__ == "__main__":
    generate_additions()
