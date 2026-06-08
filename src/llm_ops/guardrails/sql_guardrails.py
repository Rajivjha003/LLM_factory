import re
from typing import Optional
from src.llm_ops.core.schemas import GuardrailResult
from src.llm_ops.core.config import settings
from src.llm_ops.guardrails.policy import Policy
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def check_sql_safety(sql: str) -> GuardrailResult:
    if not settings.guardrail.block_unsafe_sql and settings.security.allow_destructive_sql:
        return GuardrailResult(passed=True, action_taken="allow")
        
    sql_upper = sql.upper().strip()
    
    # Check blocked keywords
    for keyword in Policy.BLOCKED_SQL_KEYWORDS:
        # Regex to match exact word
        if re.search(rf'\b{keyword}\b', sql_upper):
            logger.warning(f"Unsafe SQL blocked: {keyword}")
            return GuardrailResult(
                passed=False, 
                reason=f"Destructive SQL command blocked: {keyword}", 
                action_taken="block"
            )
            
    # Check allowed prefixes
    is_allowed = False
    for prefix in Policy.ALLOWED_SQL_PREFIXES:
        if sql_upper.startswith(prefix):
            is_allowed = True
            break
            
    if not is_allowed:
        logger.warning(f"SQL statement does not start with an allowed prefix: {sql_upper[:20]}...")
        return GuardrailResult(
            passed=False, 
            reason="SQL statement must start with an allowed read-only prefix like SELECT or WITH.", 
            action_taken="block"
        )

    return GuardrailResult(passed=True, action_taken="allow")
