# Data Sources

## Allowed Sources
- Public datasets with compatible licenses
- Self-created instruction examples
- Project documentation with permission
- Synthetic examples generated and reviewed by humans
- SQL/debugging examples derived from non-sensitive schemas
- RAG documents intended for retrieval

## Restricted Sources
- Client private data without permission
- Secrets, tokens, credentials
- Raw production data containing PII
- Proprietary content without rights
- Eval set content reused as training data

## Domain Sources to Prioritize
- BigQuery schema explanations
- SQL debugging cases
- Bronze/silver/gold pipeline issues
- Retail metric definitions
- WSSI logic
- Postgres vs BigQuery reconciliation
- Cloud Run/Scheduler debugging
- LLMOps and agentic system notes
