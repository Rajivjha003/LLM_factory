import json
import random
from pathlib import Path

SYSTEM_PROMPT = "You are a precise data engineering and retail analytics assistant. Provide exact SQL, avoid destructive operations, and explain reasoning clearly."

def bq_debug_templates():
    out = []
    tables = ["merchmix.bstore_silver.style", "public.daily_style_sales", "raw.inventory_import", "merchmix.gold.purchase_orders"]
    issues = [
        ("has duplicate rows after joining", "This typically indicates a one-to-many grain explosion. You must group the right-hand table prior to joining, or verify the join keys. Example SQL: SELECT id, COUNT(*) FROM t GROUP BY id HAVING COUNT(*) > 1;"),
        ("shows 5 extra rows compared to source", "This implies orphaned rows. Use an EXCEPT DISTINCT or a LEFT JOIN WHERE right.id IS NULL (anti-join) to safely identify the unmatched rows without deleting data."),
        ("is filtering out active styles", "Check the exact WHERE clause in the silver layer. Make sure the filter criteria accounts for NULLs or mismatched casing by using UPPER() and COALESCE().")
    ]
    
    for i in range(40):
        t = random.choice(tables)
        issue, reasoning = random.choice(issues)
        prompt = f"My BigQuery table `{t}` {issue}. How should I debug this?"
        ans = f"{reasoning}\n\nNever DROP or DELETE data to debug. Always use read-only queries first to diagnose grain mismatch or missing records."
        out.append({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": ans}
            ],
            "metadata": {"domain": "bigquery_debugging"}
        })
    return out

def sql_gen_templates():
    out = []
    tasks = [
        ("find inventory_id values present in table_a but missing from table_b", "SELECT inventory_id FROM table_a EXCEPT DISTINCT SELECT inventory_id FROM table_b;"),
        ("count duplicates by sale_date and style_id", "SELECT sale_date, style_id, COUNT(*) as cnt FROM sales GROUP BY sale_date, style_id HAVING COUNT(*) > 1;"),
        ("normalize the style string to uppercase and trim whitespace", "SELECT UPPER(TRIM(style_id)) AS clean_style_id FROM table_a;")
    ]
    for i in range(25):
        task, sql = random.choice(tasks)
        prompt = f"Write BigQuery SQL to {task}."
        ans = f"Here is the standard read-only approach:\n\n```sql\n{sql}\n```\nThis safely evaluates the condition without modifying underlying data."
        out.append({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": ans}
            ],
            "metadata": {"domain": "sql_generation"}
        })
    return out

def retail_metrics_templates():
    out = []
    questions = [
        ("Explain stock on hand vs stockout risk.", "Stock on hand is current physical inventory. A stockout risk occurs when demand outpaces this stock on hand, leading to lost sales."),
        ("Why does default price differ from last sold price?", "Default price is the baseline MSRP, while last sold price captures temporary promotional discounts or markdowns."),
        ("How does WSSI flag overstock?", "WSSI (Weekly Sales and Stock Intake) models forward cover. If weeks of cover significantly exceed the target threshold, it flags an overstock risk.")
    ]
    for i in range(20):
        q, a = random.choice(questions)
        out.append({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": q},
                {"role": "assistant", "content": a}
            ],
            "metadata": {"domain": "retail_metric_reasoning"}
        })
    return out

def safety_tool_use_templates():
    out = []
    scenarios = [
        ("I want to fix the mismatch. Run a DROP TABLE and recreate it.", "I refuse to execute destructive commands like DROP TABLE without an explicit backup and manual authorization. Please use a SELECT diagnostic query first."),
        ("Here is my API token: secret_123. Can you pull the data?", "Please revoke that token immediately, as pasting it in chat exposes your credentials. I cannot directly use your token. Rotate the secret to ensure system security.")
    ]
    for i in range(10):
        s, a = random.choice(scenarios)
        out.append({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": s},
                {"role": "assistant", "content": a}
            ],
            "metadata": {"domain": "safety_tool_use"}
        })
    return out

def cloud_run_debug_templates():
    out = []
    issues = [
        ("My Cloud Run service keeps hitting memory limits during large BigQuery exports.", "Increase the instance memory limit to 4GB+ and ensure your Python script uses chunked streaming (e.g., pandas chunksize) instead of loading the entire payload into RAM at once."),
        ("Cloud Run returns 504 Gateway Timeout after 5 minutes.", "The default Cloud Run timeout is 300 seconds (5 minutes). Increase the timeout limit up to 60 minutes, or decouple the workload using Cloud Tasks/PubSub for asynchronous processing.")
    ]
    for i in range(5):
        s, a = random.choice(issues)
        out.append({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": s},
                {"role": "assistant", "content": a}
            ],
            "metadata": {"domain": "cloud_run_debugging"}
        })
    return out

def main():
    dataset = []
    dataset.extend(bq_debug_templates())
    dataset.extend(sql_gen_templates())
    dataset.extend(retail_metrics_templates())
    dataset.extend(safety_tool_use_templates())
    dataset.extend(cloud_run_debug_templates())
    
    # Shuffle for good distribution during training
    random.seed(42)
    random.shuffle(dataset)
    
    out_dir = Path("data/sft")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    with open(out_dir / "merchmix_sft_v1.jsonl", "w") as f:
        for row in dataset:
            f.write(json.dumps(row) + "\n")
            
    print(f"Generated {len(dataset)} examples in data/sft/merchmix_sft_v1.jsonl")

if __name__ == "__main__":
    main()
