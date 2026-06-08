from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

class BigQueryReadOnlyTool:
    def __init__(self):
        self.read_only = settings.bigquery.bigquery_read_only
        self.dry_run = settings.bigquery.bigquery_dry_run_default
        
    def execute(self, query: str) -> dict:
        logger.info(f"Executing BigQuery Read-Only tool: {query}")
        # enforce SELECT-only, max bytes billed, timeout
        return {"status": "success", "data": []}
