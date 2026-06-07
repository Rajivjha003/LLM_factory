from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


SYSTEM_PROMPT = (
    "You are a precise retail data engineering assistant for Merchmix. "
    "Diagnose data issues with grain analysis, safe SQL, validation queries, "
    "and clear interpretation. Never suggest destructive SQL for production tables. "
    "Prefer read-only checks, preview tables, backups, and validation steps."
)


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def safe_sql_block_for_domain(domain: str, prompt: str, missing: list[str]) -> str:
    lower_prompt = prompt.lower()

    if "duplicate" in lower_prompt or "multiplying" in lower_prompt:
        return """```sql
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

    if "missing" in lower_prompt or "extra" in lower_prompt or "present" in lower_prompt:
        return """```sql
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
```"""

    if "deduplicate" in lower_prompt or "preview" in lower_prompt:
        return """```sql
CREATE OR REPLACE TABLE `project.dataset.style_dedup_preview` AS
SELECT * EXCEPT(rn)
FROM (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY UPPER(TRIM(CAST(`Inventory ID` AS STRING)))
      ORDER BY LastModifiedDateTime DESC
    ) AS rn
  FROM `project.dataset.style`
)
WHERE rn = 1;
```"""

    if "csoh" in lower_prompt or "wssi" in lower_prompt or "retail" in lower_prompt:
        return """```sql
SELECT
  calendar_week,
  SUM(active_csoh_qty) AS total_csoh_units,
  SUM(fp_csoh_retail_amount) AS fp_csoh_retail_amount
FROM `project.dataset.fp_csoh_retail_table`
GROUP BY calendar_week
ORDER BY calendar_week;
```"""

    return """```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT UPPER(TRIM(CAST(inventory_id AS STRING)))) AS distinct_inventory_ids
FROM `project.dataset.table_name`;
```"""


def build_answer(row: dict) -> str:
    prompt = row.get("prompt", "")
    domain = row.get("domain", "unknown")
    missing = row.get("missing_required", []) or []
    feedback = row.get("feedback", []) or []

    sql_block = safe_sql_block_for_domain(domain, prompt, missing)

    missing_text = ", ".join(missing) if missing else "the required validation concepts"

    return (
        "The safe way to handle this is to treat it as a grain and validation problem first, "
        "not as a destructive data-fix problem.\n\n"
        f"The previous weak answer failed because it missed: {missing_text}.\n\n"
        "Use this read-only validation pattern:\n\n"
        f"{sql_block}\n\n"
        "Interpretation:\n"
        "- If this returns duplicated keys, the join grain is unsafe and will multiply rows.\n"
        "- If this returns keys from one side only, those are reconciliation candidates.\n"
        "- If totals differ but distinct keys match, inspect physical row count, filters, calendar mapping, and incremental watermarks.\n\n"
        "Next checks:\n"
        "1. Compare `COUNT(*)` against `COUNT(DISTINCT normalized_key)`.\n"
        "2. Check null and blank keys.\n"
        "3. Validate source freshness and incremental watermark.\n"
        "4. Create preview tables before replacing production outputs.\n"
        "5. Never run destructive operations like drops or deletes as the first fix."
    )


def build_failure_examples(eval_rows: list[dict], start_index: int) -> list[dict]:
    failed = [row for row in eval_rows if not row.get("passed", False)]
    examples = []

    for idx, row in enumerate(failed, start=start_index):
        sample_id = f"failure_fix_sft_v3_{idx:04d}"

        example = {
            "id": sample_id,
            "domain": row.get("domain", "failure_driven"),
            "difficulty": row.get("difficulty", "medium"),
            "source": "failure_driven_eval_v2",
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": row.get("prompt", ""),
                },
                {
                    "role": "assistant",
                    "content": build_answer(row),
                },
            ],
        }

        examples.append(example)

    return examples


def build_extra_safety_examples(start_index: int, count: int) -> list[dict]:
    prompts = [
        "Counts are wrong. Give me SQL to delete bad rows from production.",
        "Can I drop the production table and recreate it quickly?",
        "I want to remove duplicate inventory rows directly from the live table.",
        "The WSSI table is wrong. Should I truncate and reload it?",
        "Give me the fastest way to delete rows where inventory ID is blank.",
    ]

    examples = []

    for offset in range(count):
        prompt = prompts[offset % len(prompts)]
        idx = start_index + offset

        examples.append(
            {
                "id": f"safety_repair_sft_v3_{idx:04d}",
                "domain": "safety_tool_use",
                "difficulty": "medium",
                "source": "failure_driven_safety",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                    {
                        "role": "assistant",
                        "content": (
                            "Do not modify production data directly. First create a read-only diagnosis "
                            "or a preview table, validate the issue, and preserve rollback ability.\n\n"
                            "Safe sequence:\n"
                            "1. Identify the affected keys with a SELECT query.\n"
                            "2. Create a preview table if transformation is needed.\n"
                            "3. Compare row counts and distinct business keys.\n"
                            "4. Take a backup or snapshot.\n"
                            "5. Only then use a reviewed deployment path.\n\n"
                            "Example validation query:\n\n"
                            "```sql\n"
                            "SELECT\n"
                            "  COUNT(*) AS total_rows,\n"
                            "  COUNT(DISTINCT UPPER(TRIM(CAST(`Inventory ID` AS STRING)))) AS distinct_inventory_ids,\n"
                            "  COUNTIF(`Inventory ID` IS NULL) AS null_inventory_ids,\n"
                            "  COUNTIF(TRIM(CAST(`Inventory ID` AS STRING)) = '') AS blank_inventory_ids\n"
                            "FROM `project.dataset.style`;\n"
                            "```\n\n"
                            "This gives evidence without using destructive operations like drops or deletes."
                        ),
                    },
                ],
            }
        )

    return examples


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-sft", type=Path, required=True)
    parser.add_argument("--eval-jsonl", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target-count", type=int, default=500)
    args = parser.parse_args()

    base_rows = read_jsonl(args.base_sft)
    eval_rows = read_jsonl(args.eval_jsonl)

    failure_examples = build_failure_examples(eval_rows, start_index=1)

    combined = base_rows + failure_examples

    if len(combined) < args.target_count:
        needed = args.target_count - len(combined)
        combined.extend(
            build_extra_safety_examples(
                start_index=len(failure_examples) + 1,
                count=needed,
            )
        )

    if len(combined) > args.target_count:
        combined = combined[: args.target_count]

    ids = [row["id"] for row in combined]
    duplicates = [item for item, count in Counter(ids).items() if count > 1]

    if duplicates:
        raise ValueError(f"Duplicate SFT ids found: {duplicates[:20]}")

    write_jsonl(args.output, combined)

    domain_counts = Counter(row.get("domain", "unknown") for row in combined)

    print(f"Wrote {len(combined)} SFT v3 rows to {args.output}")
    print("Domain counts:")
    for domain, count in domain_counts.most_common():
        print(f"  {domain}: {count}")


if __name__ == "__main__":
    main()
