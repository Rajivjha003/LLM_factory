from typing import Dict, Any, Optional
from src.llm_ops.core.schemas import SelfEvalResult, RAGResponse
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def evaluate_rag(response: RAGResponse) -> SelfEvalResult:
    if not settings.self_eval.self_eval_enabled:
        return SelfEvalResult(answer_quality_score=1.0, grounding_score=1.0, citation_score=1.0)
        
    logger.debug("Evaluating RAG response.")
    
    citation_score = 1.0 if response.citations else 0.0
    grounding_score = 0.9 if response.citations else 0.4
    
    human_review = False
    if grounding_score < settings.self_eval.self_eval_require_human_review_below:
        human_review = True
        
    return SelfEvalResult(
        answer_quality_score=0.9,
        grounding_score=grounding_score,
        citation_score=citation_score,
        confidence=response.confidence,
        human_review_required=human_review,
        reasons=["Citations checked."]
    )
