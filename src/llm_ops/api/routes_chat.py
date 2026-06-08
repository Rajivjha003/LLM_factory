from fastapi import APIRouter, Depends
from src.llm_ops.core.schemas import ChatRequest, ChatResponse
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    logger.info(f"Received chat request: {request.query}")
    # Call router logic here
    return ChatResponse(
        answer="Direct answer placeholder.",
        model="qwen_1_5b_sft_v2_q5_k_m"
    )
