from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


SYSTEM_PROMPT = (
    "You are a precise retail data engineering assistant for Merchmix. "
    "Diagnose data issues with grain analysis, safe SQL, validation queries, "
    "and clear interpretation. Never suggest destructive SQL for production tables. "
    "Prefer read-only checks, preview tables, backups, and validation steps."
)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def make_sample(
    id_: str,
    domain: str,
    difficulty: str,
    user: str,
    assistant: str,
    source: str = "rubric_generated_v4",
) -> dict:
    return {
        "id": id_,
        "domain": domain,
        "difficulty": difficulty,
        "source": source,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
    }


def anti_join_answer(left_name: str, right_name: str, key: str) -> str:
    return f"""Use a read-only anti-join after normalizing the business key. Do not delete or overwrite anything until the mismatches are classified.

```sql
WITH left_side AS (
  SELECT DISTINCT
    UPPER(TRIM(CAST({key} AS STRING))) AS key_norm
  FROM `{left_name}`
  WHERE {key} IS NOT NULL
    AND TRIM(CAST({key} AS STRING)) != ''
),
right_side AS (
  SELECT DISTINCT
    UPPER(TRIM(CAST({key} AS STRING))) AS key_norm
  FROM `{right_name}`
  WHERE {key} IS NOT NULL
    AND TRIM(CAST({key} AS STRING)) != ''
)
SELECT key_norm
FROM left_side
EXCEPT DISTINCT
SELECT key_norm
FROM right_side
ORDER BY key_norm;
```

Interpretation:
- Every returned row exists in the left table but not in the right table after `TRIM`, `UPPER`, and `CAST` normalization.
- If the count matches the reported difference, these are the exact records to investigate.
- Next check status, latest modified timestamp, source freshness, and incremental watermark before deciding whether the rows are valid or sync artifacts."""


def left_join_anti_answer(left_name: str, right_name: str, key: str) -> str:
    return f"""Use a read-only left anti-join when you want rows from the left table that have no matching normalized key on the right table.

```sql
WITH left_side AS (
  SELECT
    *,
    UPPER(TRIM(CAST({key} AS STRING))) AS key_norm
  FROM `{left_name}`
  WHERE {key} IS NOT NULL
    AND TRIM(CAST({key} AS STRING)) != ''
),
right_side AS (
  SELECT DISTINCT
    UPPER(TRIM(CAST({key} AS STRING))) AS key_norm
  FROM `{right_name}`
  WHERE {key} IS NOT NULL
    AND TRIM(CAST({key} AS STRING)) != ''
)
SELECT left_side.*
FROM left_side
LEFT JOIN right_side
  ON left_side.key_norm = right_side.key_norm
WHERE right_side.key_norm IS NULL
ORDER BY left_side.key_norm;
```

Interpretation:
- Rows returned are present in the left table but missing from the right table after normalization.
- This is a validation query only.
- Classify the returned rows before any production change."""


def duplicate_key_answer(table: str, key: str) -> str:
    return f"""First check whether the join key is unique at the grain you are joining on. Row multiplication usually happens when the right-side table has multiple rows per key.

```sql
SELECT
  UPPER(TRIM(CAST({key} AS STRING))) AS key_norm,
  COUNT(*) AS row_count
FROM `{table}`
WHERE {key} IS NOT NULL
  AND TRIM(CAST({key} AS STRING)) != ''
GROUP BY key_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
```

Interpretation:
- If this returns rows, the table is not unique by normalized key.
- Joining another table to this table on that key can multiply rows.
- Fix by deduplicating into a preview table with `ROW_NUMBER()` and a deterministic `ORDER BY`, then validate counts before replacing production outputs."""


def row_count_answer(table: str, key: str) -> str:
    return f"""Separate physical row count from distinct business-key count. A table can have the same distinct keys but extra physical rows because of duplicates.

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST({key} AS STRING)))) AS distinct_keys,
  COUNTIF({key} IS NULL) AS null_keys,
  COUNTIF(TRIM(CAST({key} AS STRING)) = '') AS blank_keys
FROM `{table}`;
```

Then inspect duplicate normalized keys:

```sql
SELECT
  UPPER(TRIM(CAST({key} AS STRING))) AS key_norm,
  COUNT(*) AS row_count
FROM `{table}`
WHERE {key} IS NOT NULL
  AND TRIM(CAST({key} AS STRING)) != ''
GROUP BY key_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
```

Interpretation:
- `total_rows` measures physical records.
- `distinct_keys` measures unique business keys.
- If total rows exceed distinct keys, investigate duplicate grain before blaming sync or source data."""


def safe_dedupe_preview_answer(table: str, key: str, order_col: str) -> str:
    return f"""Do not deduplicate the production table directly. Create a preview table first, then validate it.

```sql
CREATE OR REPLACE TABLE `project.dataset.dedup_preview` AS
SELECT * EXCEPT(rn)
FROM (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY UPPER(TRIM(CAST({key} AS STRING)))
      ORDER BY {order_col} DESC
    ) AS rn
  FROM `{table}`
)
WHERE rn = 1;
```

Validation:

```sql
SELECT 'source' AS table_name, COUNT(*) AS total_rows
FROM `{table}`
UNION ALL
SELECT 'preview' AS table_name, COUNT(*) AS total_rows
FROM `project.dataset.dedup_preview`;
```

Interpretation:
- The preview keeps one row per normalized key.
- The `ORDER BY` controls which row wins.
- Review duplicates and counts before any production replacement.
- Avoid dropping tables, deleting rows, or truncating as a first fix."""


def calendar_answer(calendar_table: str) -> str:
    return f"""Check whether one calendar date maps to more than one retail week. Overlapping calendar ranges can duplicate sales after a date join.

```sql
WITH expanded_calendar AS (
  SELECT
    calendar_date,
    financial_year,
    calendar_week
  FROM `{calendar_table}`,
  UNNEST(GENERATE_DATE_ARRAY(beginning_date, ending_date)) AS calendar_date
)
SELECT
  calendar_date,
  COUNT(*) AS mapping_count
FROM expanded_calendar
GROUP BY calendar_date
HAVING COUNT(*) > 1
ORDER BY mapping_count DESC, calendar_date;
```

Interpretation:
- If this returns rows, those dates map to multiple calendar records.
- Joining sales by date will duplicate those sales rows.
- Fix the calendar grain first, then rerun weekly reconciliation."""


def retail_metric_answer(metric: str) -> str:
    return f"""For `{metric}`, separate units, value basis, and calendar mapping before debugging totals.

Validation query:

```sql
SELECT
  calendar_week,
  SUM(active_csoh_qty) AS total_stock_units,
  SUM(fp_csoh_retail_amount) AS fp_csoh_retail_amount
FROM `project.dataset.fp_csoh_retail_table`
GROUP BY calendar_week
ORDER BY calendar_week;
```

Checks:
1. Confirm stock quantity source and snapshot date.
2. Confirm whether value uses default price, last sold price, or unit cost.
3. Confirm full-price versus markdown classification.
4. Confirm date-to-week calendar mapping.
5. Compare totals at week, style, and store grain.

Interpretation:
- If stock units are correct but value is wrong, investigate price basis.
- If both units and value are wrong, investigate stock source and calendar mapping.
- Do not change downstream WSSI tables until the input grain is validated."""


def safety_answer(action: str) -> str:
    return f"""Do not run destructive SQL against production as the first response to `{action}`. First prove the issue with read-only checks and create a reversible path.

Safe sequence:
1. Run a `SELECT` query to identify affected rows.
2. Create a preview table if transformation is needed.
3. Compare row counts and distinct business keys.
4. Take a backup or snapshot.
5. Use reviewed deployment steps before replacing production.

Read-only validation example:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(`Inventory ID` AS STRING)))) AS distinct_inventory_ids,
  COUNTIF(`Inventory ID` IS NULL) AS null_inventory_ids,
  COUNTIF(TRIM(CAST(`Inventory ID` AS STRING)) = '') AS blank_inventory_ids
FROM `project.dataset.style`;
```

Interpretation:
- This gives evidence without using destructive statements like dropping or deleting.
- If the issue is confirmed, build a preview table and review the diff before production changes."""


def pipeline_answer(topic: str) -> str:
    return f"""Debug `{topic}` by isolating the layer where the count or freshness changed.

Checks:
1. Confirm source table freshness.
2. Compare bronze, silver, gold, and Postgres row counts.
3. Check filters added in the transformation.
4. Check incremental watermark and latest modified timestamp.
5. Check join grain and duplicate keys.
6. Review Cloud Run, Scheduler, or Dataform logs if orchestration is involved.

Example count check:

```sql
SELECT
  'bronze' AS layer,
  COUNT(*) AS total_rows
FROM `project.bronze.table_name`
UNION ALL
SELECT
  'silver' AS layer,
  COUNT(*) AS total_rows
FROM `project.silver.table_name`
UNION ALL
SELECT
  'gold' AS layer,
  COUNT(*) AS total_rows
FROM `project.gold.table_name`;
```

Interpretation:
- The first layer where the count changes is where to inspect logic.
- If freshness differs, inspect watermark or job logs.
- If count increases after a join, inspect duplicate join keys."""


def join_filter_answer(left_table: str, right_table: str, key: str) -> str:
    return f"""If a `LEFT JOIN` starts dropping rows after adding a right-table filter, the filter may have turned the logic into an effective inner join.

Risky pattern:

```sql
SELECT *
FROM `{left_table}` l
LEFT JOIN `{right_table}` r
  ON UPPER(TRIM(CAST(l.{key} AS STRING))) = UPPER(TRIM(CAST(r.{key} AS STRING)))
WHERE r.status = 'Active';
```

Safer diagnostic pattern:

```sql
SELECT *
FROM `{left_table}` l
LEFT JOIN `{right_table}` r
  ON UPPER(TRIM(CAST(l.{key} AS STRING))) = UPPER(TRIM(CAST(r.{key} AS STRING)))
 AND r.status = 'Active';
```

Interpretation:
- A `WHERE` condition on the right table removes rows where the right side is `NULL`.
- Putting the condition in the `ON` clause preserves unmatched left rows.
- Validate row counts before and after the change."""


def po_header_line_answer(header_table: str, line_table: str) -> str:
    return f"""Purchase order headers and lines have different grains. Do not sum header totals after joining to lines unless the header is first deduplicated or allocated.

Validation query:

```sql
SELECT
  h.OrderNbr,
  COUNT(*) AS joined_rows,
  COUNT(DISTINCT l.LineNbr) AS distinct_lines,
  MAX(h.Total) AS header_total,
  SUM(l.Qty * l.UnitCost) AS line_total
FROM `{header_table}` h
JOIN `{line_table}` l
  ON h.OrderNbr = l.OrderNbr
GROUP BY h.OrderNbr
HAVING joined_rows != distinct_lines
   OR ABS(MAX(h.Total) - SUM(l.Qty * l.UnitCost)) > 0.01
ORDER BY h.OrderNbr;
```

Interpretation:
- Header total is order-level.
- Line total is line-level.
- Repeating header total across lines can inflate totals.
- Aggregate at the correct grain before reporting."""


def build_examples(count: int, seed: int) -> list[dict]:
    random.seed(seed)
    examples: list[dict] = []

    table_pairs = [
        ("merchmix.bstore_silver.style", "merchmix.source.accumatica_inventory", "`Inventory ID`"),
        ("merchmix.gold.purchase_items", "merchmix.postgres.purchase_items_extract", "InventoryID"),
        ("merchmix.gold.sales_daily", "merchmix.postgres.sales_daily_extract", "style_id"),
        ("merchmix.bronze.stock", "merchmix.silver.csoh", "inventory_id"),
    ]

    duplicate_tables = [
        ("merchmix.bstore_silver.style", "`Inventory ID`"),
        ("merchmix.gold.final_purchase_detail_table", "InventoryID"),
        ("merchmix.gold.daily_style_sales", "style_id"),
        ("merchmix.silver.retail_calendar", "calendar_week"),
    ]

    safety_actions = [
        "deleting duplicate inventory rows",
        "dropping and recreating a WSSI table",
        "truncating a gold table after wrong counts",
        "removing inactive styles from reporting",
        "overwriting production style with deduped data",
    ]

    pipeline_topics = [
        "bronze to silver row-count drop",
        "Cloud Scheduler job that succeeded but did not refresh the downstream table",
        "Dataform incremental table with stale output",
        "gold table total shift after a silver dedupe rule change",
    ]

    idx = 1

    while len(examples) < count:
        pattern = len(examples) % 10

        if pattern == 0:
            left, right, key = random.choice(table_pairs)
            user = (
                f"BigQuery and source counts do not match. Find records in {left} "
                f"that are missing from {right}. Give safe SQL only."
            )
            assistant = anti_join_answer(left, right, key)
            domain = "postgres_bq_reconciliation"
            difficulty = "medium"

        elif pattern == 1:
            table, key = random.choice(duplicate_tables)
            user = (
                f"My join is multiplying rows. Check whether {table} has duplicate keys "
                f"for {key} after normalization."
            )
            assistant = duplicate_key_answer(table, key)
            domain = "bigquery_debugging"
            difficulty = "medium"

        elif pattern == 2:
            table, key = random.choice(duplicate_tables)
            user = (
                f"Give me a count check for {table}: total rows, distinct normalized keys, "
                f"null keys, blank keys."
            )
            assistant = row_count_answer(table, key)
            domain = "sql_generation"
            difficulty = "medium"

        elif pattern == 3:
            table, key = random.choice(duplicate_tables)
            user = (
                f"I need to deduplicate {table}, but safely. Create a preview-table approach."
            )
            assistant = safe_dedupe_preview_answer(table, key, "LastModifiedDateTime")
            domain = "safety_tool_use"
            difficulty = "hard"

        elif pattern == 4:
            user = "Weekly sales duplicated after calendar mapping. How do I validate overlapping calendar weeks?"
            assistant = calendar_answer("merchmix.bstore_silver.retail_calendar")
            domain = "pipeline_debugging"
            difficulty = "hard"

        elif pattern == 5:
            user = "WSSI CSOH retail value does not match the business spreadsheet. Give me the debug plan."
            assistant = retail_metric_answer("FP CSOH retail amount")
            domain = "retail_metric_reasoning"
            difficulty = "medium"

        elif pattern == 6:
            action = random.choice(safety_actions)
            user = f"Can I fix this quickly by {action} in production?"
            assistant = safety_answer(action)
            domain = "safety_tool_use"
            difficulty = "medium"

        elif pattern == 7:
            topic = random.choice(pipeline_topics)
            user = f"My pipeline has a problem with {topic}. Give me the debug order."
            assistant = pipeline_answer(topic)
            domain = "pipeline_debugging"
            difficulty = "medium"

        elif pattern == 8:
            user = "A LEFT JOIN started removing rows after I added a filter from the right table. Explain and fix the SQL pattern."
            assistant = join_filter_answer("project.dataset.sales", "project.dataset.style", "inventory_id")
            domain = "bigquery_debugging"
            difficulty = "hard"

        else:
            user = "When doing an inner join between PO headers and detail rows, the aggregate amount duplicates. What's the best way to investigate the mismatched level of detail?"
            assistant = po_header_line_answer("project.dataset.purchase_orders", "project.dataset.purchase_order_items")
            domain = "sql_generation"
            difficulty = "hard"

        examples.append(
            make_sample(
                id_=f"rubric_sft_v4_{idx:04d}",
                domain=domain,
                difficulty=difficulty,
                user=user,
                assistant=assistant,
            )
        )
        idx += 1

    return examples


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--count", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rows = build_examples(count=args.count, seed=args.seed)
    write_jsonl(args.output, rows)

    print(f"Wrote {len(rows)} rubric SFT v4 additions to {args.output}")


if __name__ == "__main__":
    main()
