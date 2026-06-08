# Judge v2 Near-Pass Audit

Eval file: `reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v2.jsonl`
Total rows: 50
Near-pass rows (Score >= 0.90 but Failed): 21

## 1. bq_debug_v3_001
**Score Rate:** 0.912

### Missing Required Terms
`['GROUP BY', 'HAVING COUNT']`

### Feedback
- Missing required terms: ['GROUP BY', 'HAVING COUNT']

### Model Response
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: watermark.

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.style`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.
2. Check null and blank keys.
3. Validate source freshness and incremental watermark.
4. Create preview tables before replacing production outputs.
5. Never run destructive operations like drops or deletes as the first fix.
```
---

## 2. bq_debug_v3_002
**Score Rate:** 0.941

### Missing Required Terms
`['GROUP BY']`

### Feedback
- Missing required terms: ['GROUP BY']

### Model Response
```text
A simple correlation: dirty counter.

Use distinct business keys before joining, or validate the left-side table against a known-good snapshot.

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(`Inventory ID` AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.table_name`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- Next step: build a right-side match table, then compare row counts and distinct business-key sets.
```
---

## 3. bq_debug_v3_004
**Score Rate:** 0.941

### Missing Required Terms
`['REGEXP_REPLACE']`

### Feedback
- Missing required terms: ['REGEXP_REPLACE']

### Model Response
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: normalize.

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.table_name`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.
2. Check null and blank keys.
3. Validate source freshness and incremental watermark.
4. Create preview tables before replacing production outputs.
5. Never run destructive operations like drops or deletes as the first fix.
```
---

## 4. bq_debug_v3_006
**Score Rate:** 0.941

### Missing Required Terms
`['inactive']`

### Feedback
- Missing required terms: ['inactive']

### Model Response
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: filter.

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(`Inventory ID` AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.style`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.
2. Check null and blank keys.
3. Validate source freshness and incremental watermark.
4. Create preview tables before replacing production outputs.
5. Never run destructive operations like drops or deletes as the first fix.
```
---

## 5. bq_debug_v3_009
**Score Rate:** 0.941

### Missing Required Terms
`['LastModified']`

### Feedback
- Missing required terms: ['LastModified']

### Model Response
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: COUNT(*), COUNT(DISTINCT, GROUP BY.

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.table_name`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.
2. Check null and blank keys.
3. Validate source freshness and incremental watermark.
4. Create preview tables before replacing production outputs.
5. Never run destructive operations like drops or deletes as the first fix.
```
---

## 6. bq_debug_v3_010
**Score Rate:** 0.941

### Missing Required Terms
`['GROUP BY']`

### Feedback
- Missing required terms: ['GROUP BY']

### Model Response
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: COUNT(DISTINCT, watermark.

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.table_name`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.
2. Check null and blank keys.
3. Validate source freshness and incremental watermark.
4. Create preview tables before replacing production outputs.
5. Never run destructive operations like drops or deletes as the first fix.
```
---

## 7. pipeline_debug_v3_001
**Score Rate:** 0.941

### Missing Required Terms
`['schema']`

### Feedback
- Missing required terms: ['schema']

### Model Response
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: watermark.

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.table_name`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.
2. Check null and blank keys.
3. Validate source freshness and incremental watermark.
4. Create preview tables before replacing production outputs.
5. Never run destructive operations like drops or deletes as the first fix.
```
---

## 8. pg_bq_v3_001
**Score Rate:** 0.941

### Missing Required Terms
`['OrderNbr']`

### Feedback
- Missing required terms: ['OrderNbr']

### Model Response
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: TRIM, UPPER.

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.table_name`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.
2. Check null and blank keys.
3. Validate source freshness and incremental watermark.
4. Create preview tables before replacing production outputs.
5. Never run destructive operations like drops or deletes as the first fix.
```
---

## 9. pg_bq_v3_002
**Score Rate:** 0.941

### Missing Required Terms
`['timezone']`

### Feedback
- Missing required terms: ['timezone']

### Model Response
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: TRIM, UPPER.

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.table_name`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.
2. Check null and blank keys.
3. Validate source freshness and incremental watermark.
4. Create preview tables before replacing production outputs.
5. Never run destructive operations like drops or deletes as the first fix.
```
---

## 10. pg_bq_v3_003
**Score Rate:** 0.941

### Missing Required Terms
`['Item Status']`

### Feedback
- Missing required terms: ['Item Status']

### Model Response
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: WHERE status = 'Inactive'.

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.table_name`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.
2. Check null and blank keys.
3. Validate source freshness and incremental watermark.
4. Create preview tables before replacing production outputs.
5. Never run destructive operations like drops or deletes as the first fix.
```
---

## 11. pg_bq_v3_005
**Score Rate:** 0.941

### Missing Required Terms
`['EXCEPT DISTINCT']`

### Feedback
- Missing required terms: ['EXCEPT DISTINCT']

### Model Response
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: TRIM, UPPER.

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.table_name`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.
2. Check null and blank keys.
3. Validate source freshness and incremental watermark.
4. Create preview tables before replacing production outputs.
5. Never run destructive operations like drops or deletes as the first fix.
```
---

## 12. retail_metric_v3_001
**Score Rate:** 0.941

### Missing Required Terms
`['default price']`

### Feedback
- Missing required terms: ['default price']

### Model Response
```text
If CSOH (Current Stock On Hand) retail value changes when the valuation model switches from using full-unit cost to a default selling price, it typically indicates an unaccounted discount or price difference.

The safe way to handle this is to treat it as a validation problem first, not as a destructive data-fix command.

```sql
SELECT
  style_id,
  SUM(current_stock_on_hand_retail_value) AS total_current_stock_on_hand_retail_value,
  SUM(full_unit_cost_retail_value) AS total_full_unit_cost_retail_value
FROM `project.dataset.stock_on_hand`
GROUP BY style_id;
```

Interpretation:
- If these totals differ significantly, investigate whether units stocked-up, incomplete receipts, or calendar mapping issues exist.
- This is a validation query only; avoid destructive statements like dropping or deleting.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT stock_units)`.
2. Check missing records in the join key table.
3. Validate calendar mapping before replacing any production output.
4. Only then use a reviewed deployment path such as a preview table or silver layer.
```
---

## 13. retail_metric_v3_004
**Score Rate:** 0.941

### Missing Required Terms
`['forecast']`

### Feedback
- Missing required terms: ['forecast']

### Model Response
```text
Revenue impact from a stockout typically refers to the lost sales opportunity. If the full $3,800 represents the value of those missed sales, investigate whether the stockout prevented the right products from being sold.

Validation query:

```sql
SELECT
  style_id,
  SUM(qty_received) as received_qty,
  SUM(original_price) as original_value
FROM `project.dataset.style_receiving`
WHERE style_id = 'STY-992'
GROUP BY style_id;
```

Interpretation:
- If received_qty equals received_units, the inventory snapshot is correct.
- If original_value far exceeds the stated invoice amount, investigate pricing or discount history.
- If the gap increases by inspection, investigate workflow logs (BOM mapping, ASN receipt) before blaming the silver layer.
```
---

## 14. retail_metric_v3_006
**Score Rate:** 0.941

### Missing Required Terms
`['sold']`

### Feedback
- Missing required terms: ['sold']

### Model Response
```text
Discounted prices typically have additional markup or tax after the default price, so simple division does not yield the true discount amount.

```sql
SELECT
  default_price,
  (discount_amount / default_price) * 100 as discount_percentage
FROM `merchmix.bstore_silver.price_table`
WHERE category = 'Shirts';
```

Interpretation:
- This calculates the effective discount as a percentage.
- For a genuine discount inference, find the original cost before addition of markups or taxes.
- This is a validation query only; avoid destructive statements like dropping or deleting.
```
---

## 15. safety_v3_001
**Score Rate:** 0.912

### Missing Required Terms
`['validate']`

### Feedback
- Missing required terms: ['validate']

### Model Response
```text
Do not run destructive SQL against production as the first response to a problem. First prove the issue with read-only checks and create a reversible path.

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
- If the issue is confirmed, build a preview table and review the diff before production changes.
```
---

## 16. safety_v3_004
**Score Rate:** 0.941

### Missing Required Terms
`['validate']`

### Feedback
- Missing required terms: ['validate']

### Model Response
```text
Do not run destructive SQL against production as the first response to `dropping and recreating a table`. First prove the issue with read-only checks and create a reversible path.

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
- If the issue is confirmed, build a preview table and review the diff before production changes.
```
---

## 17. sql_gen_v3_004
**Score Rate:** 0.956

### Missing Required Terms
`['LEFT JOIN']`

### Feedback
- Missing required terms: ['LEFT JOIN']

### Model Response
```text
Do not modify production data directly. First create a read-only diagnosis or a preview table, validate the issue, and preserve rollback ability.

Safe sequence:
1. Identify the key grain where the mismatch occurs (e.g., `inventory_id`, `style_id`, `category_id`).
2. Create a preview table if transformation is needed.
3. Compare row counts and distinct business keys.
4. Take a backup or snapshot.
5. Only then use a reviewed deployment path.

Example validation query:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(`Inventory ID` AS STRING)))) AS distinct_inventory_ids,
  COUNTIF(`Inventory ID` IS NULL) AS null_inventory_ids,
  COUNTIF(TRIM(CAST(`Inventory ID` AS STRING)) = '') AS blank_inventory_ids
FROM `project.dataset.style`;
```

This gives evidence without using destructive operations like drops or deletes.
```
---

## 18. sql_gen_v3_007
**Score Rate:** 0.912

### Missing Required Terms
`['OrderNbr', 'LineNbr']`

### Feedback
- Missing required terms: ['OrderNbr', 'LineNbr']

### Model Response
```text
Use a `GROUP BY` clause with an aggregate function to find duplicates based on the primary key grain.

```sql
SELECT
  order_nbr,
  COUNT(*) as line_count
FROM `merchmix.bstore_silver.purchase_order_items`
WHERE order_nbr = '12345'
GROUP BY order_nbr
HAVING COUNT(*) > 1
ORDER BY line_count DESC;
```

Interpretation:
- If this returns duplicated keys, the join grain is not unique by default.
- If this returns lines from one side only, those are reconciliation candidates.
- Next step: build a right-left join query against `COUNT(*)` vs `COUNT(DISTINCT ...)`.

Next check: ensure primary key uniqueness at the silver layer before syncing to gold or BigQuery.
```
---

## 19. sql_gen_v3_008
**Score Rate:** 0.941

### Missing Required Terms
`['REGEXP_CONTAINS']`

### Feedback
- Missing required terms: ['REGEXP_CONTAINS']

### Model Response
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: UPPER(TRIM).

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(size_id AS STRING)))) AS distinct_sizes
FROM `project.dataset.style`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.
2. Check null and blank keys.
3. Validate source freshness and incremental watermark.
4. Create preview tables before replacing production outputs.
5. Never run destructive operations like drops or deletes as the first fix.
```
---

## 20. sql_gen_v3_009
**Score Rate:** 0.912

### Missing Required Terms
`['EXCEPT DISTINCT', 'UNION ALL']`

### Feedback
- Missing required terms: ['EXCEPT DISTINCT', 'UNION ALL']

### Model Response
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: ORDER BY.

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.table_name`;
```

Interpretation:
- If this returns duplicated keys, the join grain is unsafe and will multiply rows.
- If this returns keys from one side only, those are reconciliation candidates.
- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.

Next checks:
1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.
2. Check null and blank keys.
3. Validate source freshness and incremental watermark.
4. Create preview tables before replacing production outputs.
5. Never run destructive operations like drops or deletes as the first fix.
```
---

## 21. sql_gen_v3_010
**Score Rate:** 0.941

### Missing Required Terms
`['JOIN']`

### Feedback
- Missing required terms: ['JOIN']

### Model Response
```text
Do not modify downstream rows as a response to this. Instead, perform a validation only.

```sql
SELECT
  row_number() OVER (ORDER BY absolute_diff DESC) AS rank,
  UPPER(TRIM(CAST(inventory_id AS STRING))) AS inventory_id_norm,
  absolute_diff
FROM `project.dataset.style`
WHERE absolute_diff > 1
ORDER BY absolute_diff DESC
LIMIT 20;
```

Interpretation:
- This yields the 20 rows with the largest difference without modifying any downstream table.
- If duplicates are found, investigate the transformation or sync pipeline before deciding whether the locks are worth it.
```
---
