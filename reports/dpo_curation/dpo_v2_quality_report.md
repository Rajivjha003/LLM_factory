# DPO v2 Quality Report

- Total pairs: 40
- Chosen answers with SQL blocks: 40
- Chosen answers with Interpretation: 40
- Chosen answers with safety language: 40

## Domain Counts

| Domain | Count |
|---|---:|
| bigquery_debugging | 10 |
| postgres_bq_reconciliation | 8 |
| pipeline_debugging | 7 |
| retail_metric_reasoning | 7 |
| sql_generation | 7 |
| safety_tool_use | 1 |

## Human Pair Quality Counts

| Quality | Count |
|---|---:|
| pending | 40 |

## Recommended Gates

- At least 40 pairs for DPO v2.
- At least 60% of SQL-like prompts should have SQL blocks in chosen answers.
- Chosen answers must be complete assistant answers, not rubric notes.
- Destructive SQL must not appear inside executable SQL blocks.