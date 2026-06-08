from typing import List, Dict, Any, Optional
import datetime
from src.llm_ops.core.schemas import GuardrailResult, FailureRecord
from src.llm_ops.core.config import settings
from src.llm_ops.guardrails.prompt_injection_detector import check_prompt_injection
from src.llm_ops.guardrails.sql_guardrails import check_sql_safety
from src.llm_ops.learning_loop.failure_inbox import log_failure
from src.llm_ops.core.logging import get_logger
import uuid

logger = get_logger(__name__)

def check_input_guardrails(query: str, mode: str = "direct") -> GuardrailResult:
    if not settings.guardrail.guardrails_enabled:
        return GuardrailResult(passed=True, action_taken="allow")
        
    logger.debug(f"Checking input guardrails for mode: {mode}")
    
    # 1. Prompt Injection
    if settings.guardrail.block_prompt_injection:
        injection_result = check_prompt_injection(query)
        if not injection_result.passed:
            _log_guardrail_failure(query, mode, "prompt_injection", injection_result.reason)
            return injection_result
            
    # 2. SQL specific input guardrails
    if mode == "sql_debug" or "sql" in mode:
        sql_check = check_sql_safety(query)
        if not sql_check.passed:
            _log_guardrail_failure(query, mode, "unsafe_sql", sql_check.reason)
            return sql_check
            
    return GuardrailResult(passed=True, action_taken="allow")
    
def _log_guardrail_failure(query: str, mode: str, failure_type: str, reason: str):
    try:
        record = FailureRecord(
            trace_id=str(uuid.uuid4()),
            timestamp=datetime.datetime.utcnow().isoformat(),
            user_query=query,
            mode=mode,
            answer="",
            self_eval={"reason": reason},
            failure_type=failure_type,
            action_taken="block"
        )
        log_failure(record)
    except Exception as e:
        logger.error(f"Error logging guardrail failure: {e}")
