# Use Cases

## Tier 1: Must-Have Use Cases
1. Generate correct BigQuery SQL for data checks and reconciliation.
2. Explain SQL bugs, duplicate rows, grain mismatches, and join issues.
3. Diagnose ETL pipeline problems across bronze/silver/gold layers.
4. Explain retail metrics such as sales, CSOH, WSSI, markdowns, purchase orders, stock, revenue, and margin.
5. Generate validation queries for BigQuery and Postgres.
6. Summarize schema and map source-to-target lineage.
7. Serve a local OpenAI-compatible API.
8. Run local quantized inference on GGUF models.
9. Use RAG to answer from project documents.
10. Use safe tools through controlled agentic workflows.

## Tier 2: Should-Have Use Cases
1. Generate Dataform/dbt-style transformations.
2. Generate FastAPI service plans for LLM apps.
3. Evaluate generated SQL using static and runtime checks.
4. Produce structured output in JSON/YAML/Markdown.
5. Support self-correction after tool errors.
6. Create model cards and eval reports automatically.

## Tier 3: Future Use Cases
1. Multi-agent workflows.
2. Cloud GPU scaling.
3. TensorRT-LLM deployment.
4. Distillation from larger teacher models.
5. Verifiable reward training with execution feedback.

## Explicitly Out of Scope for Local Phase
1. Training a 7B+ base model from scratch.
2. Frontier benchmark chasing.
3. Unsafe automated database mutation.
4. Unapproved shell/cloud deployment actions.
