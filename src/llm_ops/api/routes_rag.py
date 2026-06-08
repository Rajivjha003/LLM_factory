from fastapi import APIRouter, Depends
from src.llm_ops.core.schemas import RAGRequest, RAGResponse
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/rag/query", response_model=RAGResponse)
async def rag_query_endpoint(request: RAGRequest):
    logger.info(f"Received RAG query: {request.query}")
    # Call RAG retriever and generator
    return RAGResponse(
        answer="RAG answer placeholder.",
        model="qwen_1_5b_sft_v2_q5_k_m"
    )

@router.post("/rag/retrieve")
async def rag_retrieve_endpoint(request: RAGRequest):
    # Only retrieval, no answer gen
    return {"chunks": []}
