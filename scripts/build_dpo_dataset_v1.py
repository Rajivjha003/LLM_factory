from __future__ import annotations

import argparse
import json
from pathlib import Path

SYSTEM_PROMPT = (
    "You are a precise retail data engineering assistant for Merchmix. "
    "Diagnose data issues with grain analysis, safe SQL, validation queries, "
    "and clear interpretation. Never suggest destructive SQL for production tables. "
    "Prefer read-only checks, preview tables, backups, and validation steps."
)

def read_jsonl(path: Path) -> list[dict]:
    rows = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows

def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def build_chosen_answer(row: dict) -> str:
    prompt = row.get("prompt", "")
    lower_prompt = prompt.lower()
    if "duplicate" in lower_prompt or "multiplying" in lower_prompt:
        sql = """```sql
SELECT
  UPPER(TRIM(CAST(`Inventory ID` AS STRING))) AS inventory_id_norm,
  COUNT(*) AS row_count
FROM `project.dataset.style`
WHERE `Inventory ID` IS NOT NULL
  AND TRIM(CAST(`Inventory ID` AS STRING)) != ''
GROUP BY inventory_id_norm
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
```"""
        interp = "If this returns rows, the right-side join key is not unique and can multiply joined rows."
    elif "missing" in lower_prompt or "extra" in lower_prompt or "present" in lower_prompt:
        sql = """```sql
WITH left_side AS (
  SELECT DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING))) AS key_norm
  FROM `project.dataset.table_a`
  WHERE inventory_id IS NOT NULL
    AND TRIM(CAST(inventory_id AS STRING)) != ''
),
right_side AS (
  SELECT DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING))) AS key_norm
  FROM `project.dataset.table_b`
  WHERE inventory_id IS NOT NULL
    AND TRIM(CAST(inventory_id AS STRING)) != ''
)
SELECT key_norm
FROM left_side
EXCEPT DISTINCT
SELECT key_norm
FROM right_side
ORDER BY key_norm;
```"""
        interp = "Every returned row exists in the left table but not the right table after normalization."
    elif "csoh" in lower_prompt or "wssi" in lower_prompt or "retail" in lower_prompt:
        sql = """```sql
SELECT
  calendar_week,
  SUM(active_csoh_qty) AS total_stock_units,
  SUM(fp_csoh_retail_amount) AS fp_csoh_retail_amount
FROM `project.dataset.fp_csoh_retail_table`
GROUP BY calendar_week
ORDER BY calendar_week;
```"""
        interp = "If units are correct but value is wrong, inspect price basis, markdown/full-price logic, and calendar mapping."
    elif "delete" in lower_prompt or "drop" in lower_prompt or "truncate" in lower_prompt or "production" in lower_prompt:
        sql = """```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(`Inventory ID` AS STRING)))) AS distinct_inventory_ids,
  COUNTIF(`Inventory ID` IS NULL) AS null_inventory_ids,
  COUNTIF(TRIM(CAST(`Inventory ID` AS STRING)) = '') AS blank_inventory_ids
FROM `project.dataset.style`;
```"""
        interp = "This validates the issue without destructive production changes."
    else:
        sql = """```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_keys
FROM `project.dataset.table_name`;
```"""
        interp = "Use this to separate physical rows from normalized business keys."
    return (
        "Use a safe diagnosis-first workflow. Do not modify production data until the issue is proven with read-only checks.\n\n"
        f"{sql}\n\n"
        "Interpretation:\n"
        f"- {interp}\n"
        "- Next, inspect source freshness, filters, join grain, and incremental watermark if counts still differ.\n"
        "- Avoid `DROP TABLE`, `DELETE FROM`, or `TRUNCATE` as a first fix; use preview tables, backups, and validation."
    )

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge-v3-results", type=Path, required=True)
    parser.add_argument("--human-labels", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target-count", type=int, default=80)
    args = parser.parse_args()
    results = read_jsonl(args.judge_v3_results)
    human = {r["id"]: r for r in read_jsonl(args.human_labels)}
    pairs = []
    seen_prompts = set()
    for row in results:
        sample_id = row.get("id")
        human_label = human.get(sample_id)
        should_use = (not row.get("judge_v3_passed", row.get("passed", False)) or row.get("human_review_required", False) or (human_label and human_label.get("human_correct") in {"no", "partial"}))
        if not should_use:
            continue
        prompt = row.get("prompt", "").strip()
        rejected = row.get("response", "").strip()
        chosen = build_chosen_answer(row).strip()
        if not prompt or not rejected or not chosen:
            continue
        if prompt in seen_prompts:
            continue
        seen_prompts.add(prompt)
        pairs.append({"id": f"dpo_v1_{len(pairs)+1:04d}", "source_eval_id": sample_id, "domain": row.get("domain", "unknown"), "prompt": prompt, "chosen": chosen, "rejected": rejected, "system": SYSTEM_PROMPT, "source": "judge_v3_failure_or_human_review"})
        if len(pairs) >= args.target_count:
            break
    write_jsonl(args.output, pairs)
    print(f"Wrote {len(pairs)} DPO pairs to {args.output}")
    if len(pairs) < 20:
        raise SystemExit("Too few DPO pairs. Need at least 20 before DPO training.")

if __name__ == "__main__":
    main()
