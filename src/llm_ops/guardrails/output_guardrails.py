from typing import List, Dict, Any, Optional
from src.llm_ops.core.schemas import GuardrailResult, RAGResponse, ChatResponse
from src.llm_ops.core.config import settings
from src.llm_ops.guardrails.sql_guardrails import check_sql_safety
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def check_output_guardrails(response: Any, mode: str = "direct") -> GuardrailResult:
    if not settings.guardrail.guardrails_enabled:
        return GuardrailResult(passed=True, action_taken="allow")
        
    logger.debug(f"Checking output guardrails for mode: {mode}")
    
    if mode == "rag" and isinstance(response, RAGResponse):
        # We will also use citation_guardrails for this, but as a general output guardrail:
        if settings.guardrail.require_citations_for_facts and not response.citations:
            if not settings.guardrail.allow_missing_citations_if_low_confidence or response.confidence == "high":
                logger.warning("RAG response missing citations.")
                return GuardrailResult(
                    passed=False, 
                    reason="Answer requires citations but none were provided.", 
                    action_taken="block"
                )
                
    if mode == "sql_debug":
        if hasattr(response, 'answer'):
            sql_check = check_sql_safety(response.answer)
            if not sql_check.passed:
                return sql_check
                
    return GuardrailResult(passed=True, action_taken="allow")
