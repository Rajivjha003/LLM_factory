from typing import List, Dict, Any, Optional
from src.llm_ops.core.schemas import GuardrailResult, Citation
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def check_citations(answer: str, citations: List[Citation]) -> GuardrailResult:
    if not settings.guardrail.guardrails_enabled:
        return GuardrailResult(passed=True, action_taken="allow")
        
    logger.debug("Checking citation guardrails.")
    
    # Very basic placeholder for unsupported claim detection
    if "fact" in answer.lower() and not citations:
        logger.warning("Factual claim made without citations.")
        return GuardrailResult(
            passed=False, 
            reason="Factual claim detected but no citations provided.", 
            action_taken="block"
        )
        
    return GuardrailResult(passed=True, action_taken="allow")
