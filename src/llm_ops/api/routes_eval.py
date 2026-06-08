from fastapi import APIRouter
from src.llm_ops.core.schemas import SelfEvalResult
from src.llm_ops.self_eval.answer_evaluator import evaluate_answer
from src.llm_ops.core.schemas import ChatResponse
from pydantic import BaseModel

router = APIRouter()

class EvalRequest(BaseModel):
    answer: str
    confidence: str = "high"
    
@router.post("/self-eval", response_model=SelfEvalResult)
async def self_eval_endpoint(req: EvalRequest):
    mock_resp = ChatResponse(answer=req.answer, confidence=req.confidence, model="qwen")
    return evaluate_answer(mock_resp)

@router.post("/eval/replay")
async def eval_replay_endpoint():
    return {"status": "replaying production failures..."}
