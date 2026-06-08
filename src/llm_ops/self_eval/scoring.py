from typing import Dict, Any, Optional
from src.llm_ops.core.schemas import SelfEvalResult
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def calculate_final_score(eval_result: SelfEvalResult) -> float:
    logger.debug("Calculating final aggregate score.")
    # Simple weighted average for now
    weights = {
        'answer_quality_score': 0.3,
        'grounding_score': 0.4,
        'citation_score': 0.3
    }
    
    score = (
        eval_result.answer_quality_score * weights['answer_quality_score'] +
        eval_result.grounding_score * weights['grounding_score'] +
        eval_result.citation_score * weights['citation_score']
    )
    
    if eval_result.sql_safety_score < 1.0 or eval_result.tool_safety_score < 1.0:
        score = 0.0 # Veto
        
    return score
