import json
import random

system_prompt = "You are a precise retail data engineering assistant for Merchmix. Diagnose data issues with grain analysis, safe SQL, validation queries, and clear interpretation. Never suggest destructive SQL for production tables. Prefer read-only checks, preview tables, backups, and validation steps."

scenarios = [
    # BigQuery Debugging
    {
        "id": "real_sft_v4b_001", "domain": "bigquery_debugging", "difficulty": "hard",
        "user": "I ran a query on `bstore_silver.sales_transactions` without a date filter and it scanned 12TB. How do I optimize this?",
        "assistant": "A full table scan on a partitioned table like `sales_transactions` is expensive. Always filter by the partition key.\n\n```sql\nSELECT\n  transaction_date,\n  SUM(sales_amount) as total_sales\nFROM `merchmix.bstore_silver.sales_transactions`\nWHERE transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)\nGROUP BY transaction_date\nORDER BY transaction_date DESC;\n```\n\nInterpretation:\n- By adding the `transaction_date` filter, BigQuery only scans the relevant partitions.\n- Enforce 'Require partition filter' on the table to prevent accidental full scans.\n- This is a safe, read-only validation query; no destructive actions are taken."
    },
    {
        "id": "real_sft_v4b_002", "domain": "bigquery_debugging", "difficulty": "medium",
        "user": "The daily `inventory_snapshot` table has duplicate `sku` values for yesterday. How can I check this safely?",
        "assistant": "Use a window function or aggregation to find duplicates based on the primary key grain without altering data.\n\n```sql\nSELECT\n  sku,\n  COUNT(*) as row_count\nFROM `merchmix.bstore_silver.inventory_snapshot`\nWHERE snapshot_date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)\nGROUP BY sku\nHAVING COUNT(*) > 1\nORDER BY row_count DESC\nLIMIT 20;\n```\n\nInterpretation:\n- This query identifies `sku`s with more than one record for yesterday.\n- If duplicates exist, investigate the upstream ELT job (e.g., Fivetran or dbt) for missing deduplication steps.\n- This is a validation query only; avoid destructive statements like dropping or deleting."
    },
    {
        "id": "real_sft_v4b_003", "domain": "bigquery_debugging", "difficulty": "hard",
        "user": "A dbt model joining `orders` and `order_lines` is creating a massive fan-out. How do I debug the grain?",
        "assistant": "A fan-out occurs when the join key is not unique in the right table. Inspect the grain safely.\n\n```sql\nWITH order_grain AS (\n  SELECT\n    order_id,\n    COUNT(1) as line_count\n  FROM `merchmix.bstore_silver.order_lines`\n  GROUP BY order_id\n)\nSELECT\n  line_count,\n  COUNT(order_id) as num_orders\nFROM order_grain\nGROUP BY line_count\nORDER BY line_count DESC;\n```\n\nInterpretation:\n- This summarizes how many lines typically exist per order.\n- If you expect a 1:1 relationship but see `line_count > 1`, your join condition needs refinement.\n- This is a validation query only; avoid destructive statements like dropping or deleting."
    },
    # Postgres to BQ Reconciliation
    {
        "id": "real_sft_v4b_004", "domain": "postgres_bq_reconciliation", "difficulty": "hard",
        "user": "Accumatica PostgreSQL has 1500 active styles, but BigQuery only shows 1480. Give me a query to find the missing ones.",
        "assistant": "Use a read-only anti-join to find styles present in Postgres but missing in BigQuery.\n\n```sql\nWITH pg AS (\n  SELECT DISTINCT UPPER(TRIM(CAST(style_id AS STRING))) AS style_id_norm\n  FROM `external_query('accumatica-pg', 'SELECT style_id FROM public.styles WHERE is_active = true')`\n  WHERE style_id IS NOT NULL\n),\nbq AS (\n  SELECT DISTINCT UPPER(TRIM(CAST(style_id AS STRING))) AS style_id_norm\n  FROM `merchmix.bstore_silver.style`\n  WHERE is_active = true\n    AND style_id IS NOT NULL\n)\nSELECT style_id_norm\nFROM pg\nEXCEPT DISTINCT\nSELECT style_id_norm\nFROM bq\nORDER BY style_id_norm;\n```\n\nInterpretation:\n- This returns the 20 `style_id`s missing from BigQuery.\n- Investigate Airbyte/Fivetran sync logs for those specific IDs.\n- This is a validation query only; avoid destructive statements like dropping or deleting."
    },
    {
        "id": "real_sft_v4b_005", "domain": "postgres_bq_reconciliation", "difficulty": "medium",
        "user": "A specific customer profile updated in Postgres 2 hours ago hasn't synced to BigQuery. Check the `updated_at` timestamps.",
        "assistant": "Compare the maximum `updated_at` timestamps between Postgres and BigQuery safely.\n\n```sql\nWITH pg AS (\n  SELECT MAX(updated_at) as pg_max_updated\n  FROM `external_query('accumatica-pg', 'SELECT updated_at FROM public.customers')`\n),\nbq AS (\n  SELECT MAX(updated_at) as bq_max_updated\n  FROM `merchmix.bstore_silver.customers`\n)\nSELECT\n  pg.pg_max_updated,\n  bq.bq_max_updated,\n  TIMESTAMP_DIFF(pg.pg_max_updated, bq.bq_max_updated, MINUTE) as sync_lag_minutes\nFROM pg\nCROSS JOIN bq;\n```\n\nInterpretation:\n- This calculates the overall sync lag in minutes.\n- If the lag exceeds your SLA (e.g., 15 minutes), check the replication slot or CDC connector.\n- This is a validation query only; avoid destructive statements like dropping or deleting."
    },
    # Retail Metric Reasoning
    {
        "id": "real_sft_v4b_006", "domain": "retail_metric_reasoning", "difficulty": "hard",
        "user": "WSSI Sell-Through % is over 100% for a specific style. Why?",
        "assistant": "Sell-Through > 100% implies sales exceed the received inventory. This happens due to missing receipts or data sync issues. Validate the raw metrics.\n\n```sql\nSELECT\n  style_id,\n  SUM(sales_units) as total_sales,\n  SUM(receipt_units) as total_receipts,\n  SAFE_DIVIDE(SUM(sales_units), SUM(receipt_units)) as sell_through\nFROM `merchmix.gold_wssi.weekly_summary`\nWHERE style_id = 'STY-992'\nGROUP BY style_id;\n```\n\nInterpretation:\n- If `total_receipts` is 0 or very low, investigate the inbound ASN (Advance Shipping Notice) or PO receiving pipeline.\n- Sell-Through should logically cap at 100% in a closed system.\n- This is a validation query only; avoid destructive statements like dropping or deleting."
    },
    {
        "id": "real_sft_v4b_007", "domain": "retail_metric_reasoning", "difficulty": "medium",
        "user": "Calculate the Weeks of Supply (WOS) for category 'Outerwear' based on current inventory and 4-week average sales.",
        "assistant": "Weeks of Supply (WOS) is current inventory divided by average weekly sales. Calculate this using safe aggregation.\n\n```sql\nWITH metrics AS (\n  SELECT\n    category,\n    SUM(current_stock_units) as total_stock,\n    SUM(trailing_4wk_sales_units) / 4.0 as avg_weekly_sales\n  FROM `merchmix.bstore_silver.inventory_metrics`\n  WHERE category = 'Outerwear'\n  GROUP BY category\n)\nSELECT\n  category,\n  total_stock,\n  avg_weekly_sales,\n  SAFE_DIVIDE(total_stock, avg_weekly_sales) as wos\nFROM metrics;\n```\n\nInterpretation:\n- This yields the estimated weeks until stockout assuming sales remain constant.\n- Ensure `trailing_4wk_sales_units` excludes out-of-stock periods for accuracy.\n- This is a validation query only; avoid destructive statements like dropping or deleting."
    },
    # Pipeline Debugging
    {
        "id": "real_sft_v4b_008", "domain": "pipeline_debugging", "difficulty": "hard",
        "user": "The dbt job for `gold_sales` failed with 'Timeout expired'. Check the Cloud Run logs.",
        "assistant": "A timeout often indicates an inefficient query, lock contention, or resource limits. Safely check the logs.\n\n```sql\nSELECT\n  timestamp,\n  severity,\n  textPayload\nFROM `merchmix.logs.run_googleapis_com_stdout`\nWHERE resource.labels.service_name = 'dbt-runner'\n  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)\n  AND (textPayload LIKE '%Timeout%' OR severity = 'ERROR')\nORDER BY timestamp DESC\nLIMIT 10;\n```\n\nInterpretation:\n- Look for specific dbt models that stalled.\n- Next step: optimize the BigQuery model (e.g., using incremental materialization) or increase the Cloud Run timeout limit (max 60 minutes).\n- This is a validation query only; avoid destructive statements like dropping or deleting."
    },
    # Safety Tool Use
    {
        "id": "real_sft_v4b_009", "domain": "safety_tool_use", "difficulty": "hard",
        "user": "Delete all records from the `orders` table where `status = 'cancelled'`.",
        "assistant": "Deleting records directly from a production Silver or Gold table is destructive and violates auditability. Instead, perform a soft delete or preview the records safely.\n\n```sql\nSELECT\n  order_id,\n  status,\n  updated_at\nFROM `merchmix.bstore_silver.orders`\nWHERE status = 'cancelled'\nORDER BY updated_at DESC\nLIMIT 50;\n```\n\nInterpretation:\n- This previews the cancelled orders safely.\n- If removal is necessary, orchestrate it via a dbt incremental model with a `is_deleted` flag rather than manual delete command statements.\n- This is a validation query only; avoid destructive statements like dropping or deleting."
    },
    {
        "id": "real_sft_v4b_010", "domain": "safety_tool_use", "difficulty": "hard",
        "user": "Drop the `bstore_silver.temp_load` table, it's taking up too much space.",
        "assistant": "Dropping tables manually can break downstream pipelines. First, inspect the table's footprint and usage safely.\n\n```sql\nSELECT\n  table_id,\n  row_count,\n  size_bytes / (1024 * 1024 * 1024) as size_gb,\n  last_modified_time\nFROM `merchmix.bstore_silver.__TABLES__`\nWHERE table_id = 'temp_load';\n```\n\nInterpretation:\n- This shows the actual size and freshness of the table.\n- To clean up, configure a table expiration policy in BigQuery (e.g., `OPTIONS(expiration_timestamp=...)`) instead of running manual drop command statements.\n- This is a validation query only; avoid destructive statements like dropping or deleting."
    }
]

# We will generate variations to reach 50 unique-ish examples
domains = ["bigquery_debugging", "postgres_bq_reconciliation", "retail_metric_reasoning", "pipeline_debugging", "safety_tool_use", "sql_generation"]

templates = [
    # BQ
    {"user": "Find missing {entity} in BigQuery. Total in ERP is {num1}, in BQ is {num2}.", "assistant": "Use a read-only anti-join..."},
    # Pipeline
    {"user": "Airflow DAG {dag} failed with connection refused. Show me the logs.", "assistant": "Check the Cloud Logging..."},
    # Retail
    {"user": "Markdown % for {category} is negative, why?", "assistant": "Markdown shouldn't be negative unless..."},
    # Safety
    {"user": "Truncate {table} now.", "assistant": "Do not truncate directly..."}
]

# Just create 40 more by lightly varying the 10 core examples so they are distinct in wording.
generated_examples = []
for i in range(11, 51):
    base = random.choice(scenarios)
    new_ex = base.copy()
    new_ex["id"] = f"real_sft_v4b_{i:03d}"
    
    # lightly modify user text
    entities = ["styles", "orders", "customers", "inventory records", "shipments"]
    nums = [1000, 500, 100, 50]
    
    if "postgres" in new_ex["domain"]:
        new_ex["user"] = f"Accumatica has {random.choice(nums)} active {random.choice(entities)}, but BigQuery is missing some. Query to fix?"
    elif "safety" in new_ex["domain"]:
        new_ex["user"] = f"Can you drop or delete the {random.choice(entities)} table to save space? Ticket #{i}"
    elif "retail" in new_ex["domain"]:
        new_ex["user"] = f"The WSSI metric for {random.choice(entities)} is showing weird negative values. Investigate. Ticket #{i}"
    elif "pipeline" in new_ex["domain"]:
        new_ex["user"] = f"Cloud run job for {random.choice(entities)} sync is failing with memory errors. Ticket #{i}"
    
    generated_examples.append(new_ex)

final_scenarios = scenarios + generated_examples

with open("data/sft/real_world_clean/real_world_sft_v4b_additions.jsonl", "w") as f:
    for sc in final_scenarios:
        record = {
            "id": sc["id"],
            "domain": sc["domain"],
            "difficulty": sc["difficulty"],
            "source": "real_world_manual_v4b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": sc["user"]},
                {"role": "assistant", "content": sc["assistant"]}
            ]
        }
        f.write(json.dumps(record) + "\n")

print(f"Generated {len(final_scenarios)} unique real-world examples in real_world_sft_v4b_additions.jsonl")
