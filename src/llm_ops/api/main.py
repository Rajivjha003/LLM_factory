from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import setup_logging

# Import routes
from .routes_health import router as health_router
from .routes_chat import router as chat_router
from .routes_rag import router as rag_router
from .routes_eval import router as eval_router
from .routes_guardrails import router as guardrails_router
from .routes_feedback import router as feedback_router

setup_logging()

app = FastAPI(
    title=settings.app.app_name,
    description="Merchmix Local LLMOps + RAG + Agentic AI factory",
    version="0.1.0",
)

# CORS optional
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, tags=["Health"])
app.include_router(chat_router, tags=["Chat"])
app.include_router(rag_router, tags=["RAG"])
app.include_router(eval_router, tags=["Eval"])
app.include_router(guardrails_router, tags=["Guardrails"])
app.include_router(feedback_router, tags=["Feedback"])
