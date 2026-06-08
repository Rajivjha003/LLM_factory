import re
from typing import Optional
from src.llm_ops.core.schemas import GuardrailResult
from src.llm_ops.guardrails.policy import Policy
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def check_prompt_injection(query: str) -> GuardrailResult:
    query_lower = query.lower()
    for kw in Policy.PROMPT_INJECTION_KEYWORDS:
        if kw in query_lower:
            logger.warning(f"Prompt injection detected using keyword: {kw}")
            return GuardrailResult(passed=False, reason="Potential prompt injection detected.", action_taken="block")
            
    return GuardrailResult(passed=True, action_taken="allow")
