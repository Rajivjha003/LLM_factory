from typing import Dict, Any, Optional
from src.llm_ops.core.schemas import SelfEvalResult, AgentState
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def evaluate_agent(agent_state: AgentState) -> SelfEvalResult:
    if not settings.self_eval.self_eval_enabled:
        return SelfEvalResult(tool_safety_score=1.0)
        
    logger.debug("Evaluating agent state.")
    
    # Placeholder: if agent exceeded step budget
    if agent_state.steps_taken > settings.agent.agent_max_steps:
        return SelfEvalResult(
            tool_safety_score=0.5,
            confidence="low",
            human_review_required=True,
            reasons=["Agent exceeded max steps budget."]
        )
        
    return SelfEvalResult(
        tool_safety_score=1.0,
        confidence="high",
        human_review_required=False,
        reasons=["Agent completed plan safely."]
    )
