# Failure Taxonomy

**Total Failures:** 5

## Categorization

| Failure Type | Count |
|---|---|
| semantic_or_judge_failure | 5 |

## Detailed Failure Examples

### Example 1: unknown
- **Prompt:** Write PostgreSQL SQL to find duplicate rows by sale_date and style_id in public.daily_style_sales.
- **Reason:** 
```text
To find duplicate rows by `sale_date` and `style_id` in the `public.daily_style_sales`, you can use the following PostgreSQL query:

```sql
SELECT 
    sale_date, 
    style_id,
    COUNT(*) AS num_duplicates
FROM 
    public.daily_style_sales
GROUP BY 
    sale_date, 
    style_id
HAVING 
    COUNT(*) > 1;
```

### Explanation:
- **`sales_date`**: This is the column that contains the date of each sale.
- **`style_id`**: This is the column that contains the unique identifier for each style.
- **`COUNT(*)`**: This counts the number of occurrences of each combination of `sale_date` and `style_id`.
- **`HAVING COUNT(*) > 1`**: This clause filters out the rows where there are more than one occurrence of each combination of `sale_date` and `style_id`.

This query will return all rows with duplicates based on `sale_date` and `style_id`. If there are multiple rows with the same `sale_date` and `style_id`, it will only include those rows in the result set.
```

### Example 2: retail_003
- **Prompt:** A SKU has strong sales but low stock on hand. What business risk should a WSSI or replenishment system flag?
- **Reason:** 
```text
This could indicate an inventory out of date or missing product. A WSSI (Weekly Sales & Stock Intake) model would typically trigger alerts if the predicted demand exceeds the actual stock level.
```

### Example 3: retail_metric_v2_008
- **Prompt:** Explain CSOH in retail and how it should be validated in a WSSI table. (Variation 008)
- **Reason:** 
```text
CSOH stands for Customer Service Order Header. It captures critical customer interaction metadata such as date received, order ID, status change dates, and source IP. A valid CSOH must have unique keys, match order details, and enforce strict timestamp ordering.

Validate by:

1. Single row only: Check against `count(*)` and ensure distinct CSOHs count to one.
2. Valid keys: Verify each column matches the expected format and length.
3. Timestamp order: Ensure ascending dates.
4. Unique constraint: Create a separate table for validation and normalize keys.
```

### Example 4: unknown
- **Prompt:** Please formulate a BigQuery script to identify the inventory records that exist within the first dataset but are absent from the second dataset, making sure to align the keys properly. (Variation 012)
- **Reason:** 
```text
To achieve this task in Google BigQuery, you can use a combination of `SELECT` and `LEFT JOIN` operations along with some filtering conditions. Below is an example script that demonstrates how to find the inventory records that exist only in the first dataset (`dataset1`) but not in the second dataset (`dataset2`). The script assumes that both datasets have a common key column named `inventory_id`.

```sql
-- Define the two datasets
SET @dataset1 = 'project.dataset1';
SET @dataset2 = 'project.dataset2';

-- Select inventory records from dataset1 that do not exist in dataset2
WITH missing_inventory AS (
    SELECT 
        i.inventory_id,
        i.quantity,
        i.date_added
    FROM 
        `@dataset1` i
    LEFT JOIN 
        `@dataset2` j ON i.inventory_id = j.inventory_id
    WHERE 
        j.inventory_id IS NULL
)

-- Output the results
SELECT * FROM missing_inventory;
```

### Explanation:
- **CTE (Common Table Expression)**: We define a CTE called `missing_inventory` which performs a left join between `dataset1` and `dataset2`. If there's no match in `dataset2`, it will return all rows from `
```

### Example 5: retail_metric_v2_008
- **Prompt:** Explain CSOH in retail and how it should be validated in a WSSI table. (Variation 008)
- **Reason:** 
```text
CSOH stands for Current Stock On Hand. It should match the sum of physical inventory count and new stock added today minus expired or withdrawn stock. A mismatch indicates missing records.
```

