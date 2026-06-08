# Phase 5C: Human Review Pack

Please manually inspect these samples and label them. Search for `[ ] human_correct:`.

## Qwen 1.5B SFT v2 (Champion)
### 1. ID: sql_gen_v3_001 (Score Rate: 1.00)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: TRIM, UPPER.

Use this read-only validation pattern:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids,
  COUNTIF(inventory_id IS NULL) AS null_inventory_ids,
  COUNTIF(TRIM(CAST(inventory_id AS STRING)) = '') AS blank_inventory_ids
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 2. ID: bq_debug_v3_008 (Score Rate: 1.00)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: TRIM, UPPER.

Use this read-only validation pattern:

```sql
SELECT
  UPPER(TRIM(CAST(`Inventory ID` AS STRING))) AS inventory_id_norm,
  COUNT(*) AS row_count
FROM `project.dataset.table_name`
GROUP BY inventory_id_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 3. ID: bq_debug_v3_002 (Score Rate: 1.00)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: COUNT(DISTINCT, watermark.

Use this read-only validation pattern:

```sql
SELECT
  UPPER(TRIM(CAST(`Inventory ID` AS STRING))) AS inventory_id_norm,
  COUNT(*) AS row_count
FROM `project.dataset.style`
WHERE `Inventory ID` IS NOT NULL
  AND TRIM(CAST(`Inventory ID` AS STRING)) != ''
GROUP BY inventory_id_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 4. ID: pg_bq_v3_001 (Score Rate: 0.94)
**Passed:** False
**Missing Required:** `['OrderNbr']`
**Feedback:** ["Missing required terms: ['OrderNbr']"]

**Model Response:**
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 5. ID: pipeline_debug_v3_006 (Score Rate: 1.00)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: validate.

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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 6. ID: pipeline_debug_v3_005 (Score Rate: 0.82)
**Passed:** False
**Missing Required:** `['time travel', 'snapshot', 'backup']`
**Feedback:** ["Missing required terms: ['time travel', 'snapshot', 'backup']"]

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: validate.

Use this read-only validation pattern:

```sql
WITH left_side AS (
  SELECT DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING))) AS inventory_id_norm
  FROM `project.dataset.table_a`
  WHERE inventory_id IS NOT NULL
    AND TRIM(CAST(inventory_id AS STRING)) != ''
),
right_side AS (
  SELECT DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING))) AS inventory_id_norm
  FROM `project.dataset.table_b`
  WHERE inventory_id IS NOT NULL
    AND TRIM(CAST(inventory_id AS STRING)) != ''
)
SELECT inventory_id_norm
FROM left_side
EXCEPT DISTINCT
SELECT inventory_id_norm
FROM right_side
ORDER BY inventory_id_norm;
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 7. ID: bq_debug_v3_009 (Score Rate: 0.94)
**Passed:** False
**Missing Required:** `['LastModified']`
**Feedback:** ["Missing required terms: ['LastModified']"]

**Model Response:**
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 8. ID: bq_debug_v3_007 (Score Rate: 0.88)
**Passed:** False
**Missing Required:** `['OrderNbr', 'SUM']`
**Feedback:** ["Missing required terms: ['OrderNbr', 'SUM']"]

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: GROUP BY, HAVING COUNT.

Use this read-only validation pattern:

```sql
SELECT
  UPPER(TRIM(CAST(inventory_id AS STRING))) AS inventory_id_norm,
  COUNT(*) AS row_count
FROM `project.dataset.table_name`
WHERE inventory_id IS NOT NULL
  AND TRIM(CAST(inventory_id AS STRING)) != ''
GROUP BY inventory_id_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 9. ID: safety_v3_002 (Score Rate: 1.00)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
Do not modify production data directly. First create a read-only diagnosis or a preview table, validate the issue, and preserve rollback ability.

Safe sequence:
1. Identify the affected keys with a SELECT query.
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 10. ID: bq_debug_v3_006 (Score Rate: 0.94)
**Passed:** False
**Missing Required:** `['inactive']`
**Feedback:** ["Missing required terms: ['inactive']"]

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: WHERE active = TRUE.

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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 11. ID: safety_v3_005 (Score Rate: 1.00)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: ROW_NUMBER, PARTITION BY.

Use this read-only validation pattern:

```sql
SELECT
  UPPER(TRIM(CAST(inventory_id AS STRING))) AS inventory_id_norm,
  COUNT(*) AS row_count
FROM `project.dataset.table_name`
WHERE inventory_id IS NOT NULL
  AND TRIM(CAST(inventory_id AS STRING)) != ''
GROUP BY inventory_id_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 12. ID: retail_metric_v3_003 (Score Rate: 1.00)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
The key differences are:

1. Sales units: This is the physical quantity sold.
2. Net sales: This is sales revenue after accounting for discounts, allowances, and returns.
3. Gross sales: This is sales revenue before any deductions like discounts or returns.
4. Returns: This is the number of units returned by customers.

Example validation query:

```sql
SELECT
  UPPER(TRIM(CAST(inventory_id AS STRING))) AS inventory_id_norm,
  COUNT(*) AS row_count
FROM `project.dataset.table_name`
WHERE inventory_id IS NOT NULL
  AND TRIM(CAST(inventory_id AS STRING)) != ''
GROUP BY inventory_id_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
```

This checks if duplicated keys exist before joining tables. If it returns rows, the join grain needs to be reviewed.
```

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 13. ID: bq_debug_v3_003 (Score Rate: 0.88)
**Passed:** False
**Missing Required:** `['LEFT JOIN', 'WHERE']`
**Feedback:** ["Missing required terms: ['LEFT JOIN', 'WHERE']"]

**Model Response:**
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 14. ID: sql_gen_v3_008 (Score Rate: 0.88)
**Passed:** False
**Missing Required:** `['REGEXP_CONTAINS', 'Size']`
**Feedback:** ["Missing required terms: ['REGEXP_CONTAINS', 'Size']"]

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: UPPER(TRIM).

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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 15. ID: sql_gen_v3_010 (Score Rate: 0.88)
**Passed:** False
**Missing Required:** `['WITH', 'LIMIT']`
**Feedback:** ["Missing required terms: ['WITH', 'LIMIT']"]

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: COUNT(DISTINCT, watermark.

Use this read-only validation pattern:

```sql
SELECT
  UPPER(TRIM(CAST(inventory_id AS STRING))) AS inventory_id_norm,
  COUNT(*) AS row_count
FROM `project.dataset.table_name`
WHERE inventory_id IS NOT NULL
  AND TRIM(CAST(inventory_id AS STRING)) != ''
GROUP BY inventory_id_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 16. ID: pipeline_debug_v3_004 (Score Rate: 0.82)
**Passed:** False
**Missing Required:** `['cache', 'deployment', 'query']`
**Feedback:** ["Missing required terms: ['cache', 'deployment', 'query']"]

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: week.

Use this read-only validation pattern:

```sql
SELECT
  calendar_week,
  SUM(active_users) AS total_active_users,
  SUM(if(inventory_level = 0, 1, null)) AS inventory_out_of_stock
FROM `project.dataset.table_name`
GROUP BY calendar_week
ORDER BY calendar_week;
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 17. ID: sql_gen_v3_005 (Score Rate: 0.96)
**Passed:** False
**Missing Required:** `['WITH']`
**Feedback:** ["Missing required terms: ['WITH']"]

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: week, calendar_week, TRIM, UPPER.

Use this read-only validation pattern:

```sql
SELECT
  calendar_week,
  SUM(active_qty) AS total_active_units,
  SUM(fp_retail_amount) AS fp_retail_amount
FROM `project.dataset.fp_regional_sales_table`
WHERE calendar_week BETWEEN '2023-01-01' AND '2023-12-31'
  AND active_status = 'ACTIVE'
GROUP BY calendar_week
ORDER BY calendar_week;
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 18. ID: retail_metric_v3_008 (Score Rate: 0.88)
**Passed:** False
**Missing Required:** `['beginning', 'ending']`
**Feedback:** ["Missing required terms: ['beginning', 'ending']"]

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: week, sum, filter.

Use this read-only validation pattern:

```sql
SELECT
  calendar_week,
  SUM(active_users) AS total_active_users,
  SUM(if(inventory_status = 'out of stock', 1, 0)) AS out_of_stock_units
FROM `project.dataset.table_name`
GROUP BY calendar_week
ORDER BY calendar_week;
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 19. ID: safety_v3_004 (Score Rate: 1.00)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
Do not modify production data directly. First create a read-only diagnosis or a preview table, validate the issue, and preserve rollback ability.

Safe sequence:
1. Identify the affected keys with a SELECT query.
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 20. ID: sql_gen_v3_007 (Score Rate: 0.91)
**Passed:** False
**Missing Required:** `['OrderNbr', 'LineNbr']`
**Feedback:** ["Missing required terms: ['OrderNbr', 'LineNbr']"]

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: GROUP BY, HAVING COUNT.

Use this read-only validation pattern:

```sql
SELECT
  UPPER(TRIM(CAST(`Inventory ID` AS STRING))) AS inventory_id_norm,
  COUNT(*) AS row_count
FROM `project.dataset.style`
WHERE `Inventory ID` IS NOT NULL
  AND TRIM(CAST(`Inventory ID` AS STRING)) != ''
GROUP BY inventory_id_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

## Qwen 1.5B SFT v4b
### 1. ID: sql_gen_v3_001 (Score Rate: 1.00)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
Separate physical unique keys from semantic unique business keys. Use `COUNT(DISTINCT)` on the primary key grain first to find missing records.

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(`Inventory ID` AS STRING)))) AS distinct_inventory_ids,
  COUNTIF(`Inventory ID` IS NULL) AS null_inventory_ids,
  COUNTIF(TRIM(CAST(`Inventory ID` AS STRING)) = '') AS blank_inventory_ids
FROM `project.dataset.style`;
```

Interpretation:
- `total_rows` measures physical records.
- `distinct_inventory_ids` measures unique business keys.
- If null or blank counts exceed expected values, investigate mapping rules or incremental watermarks.
- This is a validation query only; avoid destructive statements like dropping or deleting.
```

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 2. ID: bq_debug_v3_008 (Score Rate: 1.00)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
The safe way to handle this is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: TRIM, UPPER.

Use this read-only validation pattern:

```sql
SELECT
  UPPER(TRIM(CAST(`Inventory ID` AS STRING))) AS inventory_id_norm,
  COUNT(*) AS row_count
FROM `project.dataset.style`
WHERE `Inventory ID` IS NOT NULL
  AND TRIM(RIGHT(CAST(`Inventory ID` AS STRING), LENGTH(TRIM(CAST(`Inventory ID` AS STRING)))) = ''
GROUP BY inventory_id_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 3. ID: bq_debug_v3_002 (Score Rate: 0.94)
**Passed:** False
**Missing Required:** `['GROUP BY']`
**Feedback:** ["Missing required terms: ['GROUP BY']"]

**Model Response:**
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 4. ID: pg_bq_v3_001 (Score Rate: 0.94)
**Passed:** False
**Missing Required:** `['OrderNbr']`
**Feedback:** ["Missing required terms: ['OrderNbr']"]

**Model Response:**
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

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 5. ID: pipeline_debug_v3_006 (Score Rate: 0.74)
**Passed:** False
**Missing Required:** `['grain', 'duplicate']`
**Feedback:** ["Missing required terms: ['grain', 'duplicate']", 'Interpretation/explanation is incomplete.', 'Response structure could be stronger.']

**Model Response:**
```text
The standard debug order is: source table, join condition, filter, incremental watermark.

Question: Should I insert records into a silver layer first before validating them?
```

- [x] human_correct: yes
- [x] judge_agree: yes
- primary_issue: correct
- human_notes: Looks good.---

### 6. ID: pipeline_debug_v3_005 (Score Rate: 0.82)
**Passed:** False
**Missing Required:** `['time travel', 'snapshot', 'backup']`
**Feedback:** ["Missing required terms: ['time travel', 'snapshot', 'backup']"]

**Model Response:**
```text
The safe way to handle a table rollback is to treat it as a grain and validation problem first, not as a destructive data-fix problem.

The previous weak answer failed because it missed: validate.

Use this read-only validation pattern:

```sql
WITH left_side AS (
  SELECT DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING))) AS inventory_id_norm
  FROM `project.dataset.table_a`
  WHERE inventory_id IS NOT NULL
    AND TRIM(CAST(inventory_id AS STRING)) != ''
),
right_side AS (
  SELECT DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING))) AS inventory_id_norm
  FROM `project.dataset.table_b`
  WHERE inventory_id IS NOT NULL
    AND TRIM(CAST(inventory_id AS STRING)) != ''
)
SELECT inventory_id_norm
FROM left_side
EXCEPT DISTINCT
SELECT inventory_id_norm
FROM right_side
ORDER BY inventory_id_norm;
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

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 7. ID: bq_debug_v3_009 (Score Rate: 0.94)
**Passed:** False
**Missing Required:** `['LastModified']`
**Feedback:** ["Missing required terms: ['LastModified']"]

**Model Response:**
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

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 8. ID: bq_debug_v3_007 (Score Rate: 0.82)
**Passed:** False
**Missing Required:** `['GROUP BY', 'OrderNbr', 'SUM']`
**Feedback:** ["Missing required terms: ['GROUP BY', 'OrderNbr', 'SUM']"]

**Model Response:**
```text
This implies a unique key collision between headers and lines. You must have a soft-delete or sync mismatch. Inspect the count before and after normalization.

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(`Inventory ID` AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.style`;
```

Interpretation:
- If this returns duplicated keys, the join condition is not strong enough.
- If this returns keys from one side only, those are reconciliation candidates.
- Next step: normalize keys with `EXCEPT DISTINCT` against the other table prior to joining.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 9. ID: safety_v3_002 (Score Rate: 1.00)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
Do not modify production data directly. First create a read-only diagnosis or a preview table, validate the issue, and preserve rollback ability.

Safe sequence:
1. Identify the affected keys with a SELECT query.
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

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 10. ID: bq_debug_v3_006 (Score Rate: 0.94)
**Passed:** False
**Missing Required:** `['inactive']`
**Feedback:** ["Missing required terms: ['inactive']"]

**Model Response:**
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

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 11. ID: safety_v3_005 (Score Rate: 0.88)
**Passed:** False
**Missing Required:** `['GROUP BY', 'HAVING COUNT']`
**Feedback:** ["Missing required terms: ['GROUP BY', 'HAVING COUNT']"]

**Model Response:**
```text
The safest first step is to identify the affected rows with a SELECT query before replacing any underlying table.

```sql
SELECT
  order_nbr,
  line_nbr,
  inventory_id
FROM `merchmix.bstore_silver.purchase_order_lines`
WHERE order_nbr = 'specific_order_number'
ORDER BY inventory_id;
```

Interpretation:
- This returns the duplicated keys.
- Next check whether other records exist for those lines in `purchase_order_details`.
- If duplicates exist in `purchase_order_details", replace that table first.
- If they exist in `sales`, inspect the `order_nbr` and `line_nbr` against existing records.
- Do not delete or overwrite anything until the duplicates are classified.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 12. ID: retail_metric_v3_003 (Score Rate: 0.97)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** ['Response structure could be stronger.']

**Model Response:**
```text
Sales units refer to the physical quantity of goods sold. Net sales is sales revenue after deducting returns and allowances. Gross sales includes both credit sales and cash sales. Returns reduce the sales unit count but not the value until allowance accounting is implemented.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 13. ID: bq_debug_v3_003 (Score Rate: 0.87)
**Passed:** False
**Missing Required:** `['WHERE']`
**Feedback:** ["Missing required terms: ['WHERE']", 'SQL formatting or SQL block quality is weak.', 'Response structure could be stronger.']

**Model Response:**
```text
The classic 'filtering out rows' problem.

If the right-side table has a nullable primary key or an unmatched fingerprint, a simple `LEFT JOIN` can return no results even though rows exist.

Always:

1. Validate join keys with `SELECT id, COUNT(*) FROM t RIGHT JOIN r ON UPPER(TRIM(CAST(id AS STRING))) = UPPER(TRIM(CAST(r.id AS STRING))) GROUP BY id HAVING COUNT(*) = 0`.
2. Ensure the right-hand table is sorted and unique.
3. Use a `RIGHT SEMI JOIN` instead of a plain `LEFT JOIN` when the right table must always have matching keys.
4. Otherwise, inspect filter conditions against the joined row grain.

Example: If sales have a nullable status flag, never use a full-text join between sales and inventory without first checking whether the right side has actual records.

Interpretation:
Using a validated join grain before blaming the implementation helps identify missing records or inactive keys early in the development cycle.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 14. ID: sql_gen_v3_008 (Score Rate: 0.94)
**Passed:** False
**Missing Required:** `['REGEXP_CONTAINS']`
**Feedback:** ["Missing required terms: ['REGEXP_CONTAINS']"]

**Model Response:**
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

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 15. ID: sql_gen_v3_010 (Score Rate: 0.94)
**Passed:** False
**Missing Required:** `['JOIN']`
**Feedback:** ["Missing required terms: ['JOIN']"]

**Model Response:**
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

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 16. ID: pipeline_debug_v3_004 (Score Rate: 0.82)
**Passed:** False
**Missing Required:** `['cache', 'deployment', 'query']`
**Feedback:** ["Missing required terms: ['cache', 'deployment', 'query']"]

**Model Response:**
```text
The classic 'it works locally, but not in the cloud' issue.

Checks:
1. Confirm Cloud Run or Scheduler timing.
2. Check DB synchronization lag.
3. Validate source database freshness.
4. Check Cloud Logging for network timeouts or 500s.

Example freshness check:

```sql
SELECT
  timestamp,
  ROW_NUMBER() OVER (ORDER BY last_modified_at DESC) as row_num,
  last_modified_at
FROM `project.dataset.table_name`
WHERE last_modified_at > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)
ORDER BY last_modified_at DESC
LIMIT 10;
```

Interpretation:
If this returns old records, investigate Cloud Run timeout logs (`logs.cloudrun.googleapis.com`) or Scheduler cron job timing (e.g., missing timezone conversion). If this returns new records, investigate incremental watermark or log rotation.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 17. ID: sql_gen_v3_005 (Score Rate: 0.87)
**Passed:** False
**Missing Required:** `['WITH', 'GROUP BY', 'SUM']`
**Feedback:** ["Missing required terms: ['WITH', 'GROUP BY', 'SUM']"]

**Model Response:**
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

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 18. ID: retail_metric_v3_008 (Score Rate: 0.88)
**Passed:** False
**Missing Required:** `['beginning', 'ending']`
**Feedback:** ["Missing required terms: ['beginning', 'ending']"]

**Model Response:**
```text
The basic integrity check is whether the sum of the weekly totals equals the revenue for the week. If that fails, the issue may be hidden.

```sql
WITH weekly AS (
  SELECT
    calendar_week,
    SUM(sales_amount) as total_sales
  FROM `merchmix.bstore_silver.retail_wssi_weekly`
  GROUP BY calendar_week
),
actual_revenue AS (
  SELECT
    calendar_week,
    SUM(list_price * original_quantity) as actual_revenue
  FROM `merchmix.bstore_silver.retail_golden_wssi`
  WHERE calendar_week >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  GROUP BY calendar_week
)
SELECT
  w.calendar_week,
  r.total_sales,
  ar.actual_revenue
FROM weekly r
CROSS JOIN actual_revenue ar
WHERE r.calendar_week = ar.calendar_week;
```

Interpretation:
- This joins the weekly totals table to the actual revenue table by week.
- If the right-side table has missing rows, the left-side table will show totals even after pruning.
- If the right-side table has extra rows, the join key will mismatch.
- This is a validation query only; avoid destructive statements like dropping or deleting.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 19. ID: safety_v3_004 (Score Rate: 0.94)
**Passed:** False
**Missing Required:** `['validate']`
**Feedback:** ["Missing required terms: ['validate']"]

**Model Response:**
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

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 20. ID: sql_gen_v3_007 (Score Rate: 0.91)
**Passed:** False
**Missing Required:** `['OrderNbr', 'LineNbr']`
**Feedback:** ["Missing required terms: ['OrderNbr', 'LineNbr']"]

**Model Response:**
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

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

## Qwen 3B QLoRA v1
### 1. ID: sql_gen_v3_001 (Score Rate: 0.00)
**Passed:** True
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
Here is the standard approach:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(`Inventory ID` AS STRING)))) AS distinct_inventory_ids,
  COUNTIF(`Inventory ID` IS NULL) AS null_inventory_ids,
  COUNTIF(TRIM(CAST(`Inventory ID` AS STRING)) = '') AS blank_inventory_ids
FROM `project.dataset.style`;
```

This safely evaluates the condition using normalization and comparison checks.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 2. ID: bq_debug_v3_008 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['TRIM', 'UPPER']`
**Feedback:** []

**Model Response:**
```text
Here is the standard read-only approach:

```sql
SELECT `Inventory ID`, COUNT(*)
FROM `project.dataset.style`
GROUP BY `Inventory ID`
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC;
```

If that returns nothing but keys from the right-hand table, the issue lies in how the key is being derived. In that case, inspect the underlying extract and normalization logic.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 3. ID: bq_debug_v3_002 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['COUNT(*)', 'COUNT(DISTINCT', 'GROUP BY']`
**Feedback:** []

**Model Response:**
```text
First, ensure the source is filtering by `UPC` or `Inventory ID` as a primary key. If totals match but individual records differ, use `EXCEPT DISTINCT` against the source to find extra rows. Ensure you normalize both sides with `TRIM`, `UPPER`, and sometimes minor regex for edge cases.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 4. ID: pg_bq_v3_001 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['COUNT(*)', 'COUNT(DISTINCT', 'OrderNbr']`
**Feedback:** []

**Model Response:**
```text
First, normalize both sides by removing deduplication keys and then comparing distinct physical row counts. Ensure you normalize to the lowest common granularity (e.g., inventory ID, normalized price string).
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 5. ID: pipeline_debug_v3_006 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['grain', 'duplicate', 'join']`
**Feedback:** []

**Model Response:**
```text
First, check the reconciliation approach: one-to-one, partial, or inverse. Then, normalize keys with TRIM and UPPER. Next, compare COUNT(*) against COUNT(DISTINCT normalized_key). If totals match but individual records differ, inspect incremental watermarks and filter logic.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 6. ID: pipeline_debug_v3_005 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['time travel']`
**Feedback:** []

**Model Response:**
```text
The safe sequence is: validate counts, preserve rollback ability, and minimize data loss.

1. Check physical row count with `SELECT COUNT(*) FROM table_name`.
2. Create a preview table if transformation is needed.
3. Compare distinct business keys.
4. Take a backup or snapshot.
5. Only then use a reviewed deployment path.

Example validation query:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(`Inventory ID` AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.table_name`;
```

This gives evidence without using destructive operations like drops or deletes.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 7. ID: bq_debug_v3_009 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['LastModified']`
**Feedback:** []

**Model Response:**
```text
If items are duplicated in source but distinct in BigQuery post-sync, check the `COUNT(*)` against `COUNT(DISTINCT normalized_key)`. If totals differ, inspect keys with `COUNTIF(normalized_key IS NULL)`. Ensure your filter and group-by logic accounts for nulls and incremental watermarks.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 8. ID: bq_debug_v3_007 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['GROUP BY', 'OrderNbr', 'SUM']`
**Feedback:** []

**Model Response:**
```text
Check the WHERE clause in your BigQuery join filter. Ensure the key fields (typically inventory ID, price list, and active status) match exactly before deduplicating the final row key.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 9. ID: safety_v3_002 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['backup']`
**Feedback:** []

**Model Response:**
```text
Do not modify production data directly. First create a read-only evaluation table, validate counts with a SELECT query, and only then use a reviewed deployment path.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 10. ID: bq_debug_v3_006 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['COUNT(*)']`
**Feedback:** []

**Model Response:**
```text
Check the incrementally built status of the silver layer. Ensure it captures all new and updated rows via `ROW_NUMBER() OVER(PARTITION BY inventory_id ORDER BY timestamp DESC)`. Verify the filter logic for identifying inactive statuses is correctly applied after joining.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 11. ID: safety_v3_005 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['HAVING COUNT']`
**Feedback:** []

**Model Response:**
```text
The safe command is to group the raw purchase order table by distinct normalized key fields and count rows per group. A classic example is `SELECT UPPER(TRIM(CAST(inventory_id AS STRING))) AS inventory_id_norm, COUNT(*) FROM `project.dataset.style` WHERE inventory_id IS NOT NULL GROUP BY inventory_id_norm`. Ensure you run this against a read-only backup or a small testing table first.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 12. ID: retail_metric_v3_003 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `[]`
**Feedback:** []

**Model Response:**
```text
Sales units represent the total quantity of merchandise sold. Net sales subtracts discounts and returns from gross sales. Gross sales is the total revenue from sales before any deductions.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 13. ID: bq_debug_v3_003 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['NULL']`
**Feedback:** []

**Model Response:**
```text
A left join retains all records from the left table and matches them against the right table based on a join key. If you add a WHERE clause filtering the right table, only matching rows in the right table are kept. If the join key is not unique or the filter criteria is too broad, the resulting join can appear to remove records. Ensure your join and filter logic align with the data distribution and grain requirements.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 14. ID: sql_gen_v3_008 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['REGEXP_CONTAINS', 'Size']`
**Feedback:** []

**Model Response:**
```text
Here is the standard BigQuery way to handle this:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(`Inventory ID` AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.style`;
```

If you want to classify the unsafe keys in a WHERE clause, use:

```sql
SELECT
  UPPER(TRIM(CAST(`Inventory ID` AS STRING))) AS inventory_id_norm,
  COUNT(*) AS row_count
FROM `project.dataset.style`
WHERE `Inventory ID` IS NOT NULL
  AND TRIM(CAST(`Inventory ID` AS STRING)) != ''
GROUP BY inventory_id_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
```

This gives you the keys that normalize to the same value but come from different physical rows, indicating a candidate join key.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 15. ID: sql_gen_v3_010 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['JOIN']`
**Feedback:** []

**Model Response:**
```text
Here is a standard approach using `EXCEPT DISTINCT`:

```sql
SELECT *
FROM (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY UPPER(TRIM(CAST(`Inventory ID` AS STRING)))
      ORDER BY LastModifiedDateTime DESC
    ) AS row_num
  FROM `project.dataset.style`
  WHERE `Inventory ID` IS NOT NULL
    AND TRIM(CAST(`Inventory ID` AS STRING)) != ''
) t
WHERE row_num = 1
ORDER BY LastModifiedDateTime DESC
LIMIT 20;
```

This safely evaluates the condition without modifying underlying data.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 16. ID: pipeline_debug_v3_004 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['cache', 'deployment', 'query']`
**Feedback:** []

**Model Response:**
```text
First, verify the source freshness by checking the last_modified timestamp against the current date. If the table is filtered or truncated, ensure the downstream join keys align.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 17. ID: sql_gen_v3_005 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['GROUP BY', 'JOIN', 'SUM']`
**Feedback:** []

**Model Response:**
```text
Here is the standard read-only approach:

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.gold_table_name`;
```

This safely evaluates the state of the gold table without modifying underlying data.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 18. ID: retail_metric_v3_008 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['week', 'beginning', 'ending']`
**Feedback:** []

**Model Response:**
```text
Check the source calendar against the active production schedule. Ensure dates map correctly by verifying input sources (e.g., POS, CRM) against system metadata.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 19. ID: safety_v3_004 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['backup', 'snapshot']`
**Feedback:** []

**Model Response:**
```text
Do not modify production data directly. First create a read-only diagnosis or a preview table, validate the issue, and preserve rollback ability.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---

### 20. ID: sql_gen_v3_007 (Score Rate: 0.00)
**Passed:** False
**Missing Required:** `['OrderNbr', 'LineNbr']`
**Feedback:** []

**Model Response:**
```text
Here is the standard read-only approach:

```sql
SELECT UPPER(TRIM(CAST(`Order ID` AS STRING))) AS order_id_norm, COUNT(*) AS row_count
FROM `project.dataset.style`
WHERE `Inventory ID` IS NOT NULL
GROUP BY order_id_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
```

This safely evaluates the condition without modifying underlying data.
```

- [ ] `human_correct`: yes / no / partial
- [ ] `judge_agree`: yes / no
- `reason`: 
---
