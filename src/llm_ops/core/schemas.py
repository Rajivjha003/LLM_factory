from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class Citation(BaseModel):
    chunk_id: str
    source_path: str
    content_snippet: str

class RetrievedChunk(BaseModel):
    chunk_id: str
    content: str
    metadata: Dict[str, Any]
    score: float

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    mode: str = "direct"

class ChatResponse(BaseModel):
    answer: str
    confidence: str = "high"
    model: str
    trace_id: Optional[str] = None

class RAGRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    top_k: int = 8

class RAGResponse(BaseModel):
    answer: str
    citations: List[Citation] = []
    confidence: str = "high"
    limitations: Optional[str] = None
    next_action: Optional[str] = None
    trace_id: Optional[str] = None
    model: str

class SelfEvalResult(BaseModel):
    answer_quality_score: float = 0.0
    grounding_score: float = 0.0
    citation_score: float = 0.0
    sql_safety_score: float = 0.0
    tool_safety_score: float = 0.0
    confidence: str = "high"
    human_review_required: bool = False
    reasons: List[str] = []

class GuardrailResult(BaseModel):
    passed: bool
    reason: Optional[str] = None
    action_taken: str = "allow"

class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

class ToolResult(BaseModel):
    success: bool
    output: Any
    error_message: Optional[str] = None

class AgentState(BaseModel):
    session_id: str
    steps_taken: int = 0
    tools_called: List[ToolCall] = []
    is_done: bool = False
    final_answer: Optional[str] = None

class FailureRecord(BaseModel):
    trace_id: str
    timestamp: str
    user_query: str
    mode: str
    answer: str
    retrieved_chunks: List[Dict[str, Any]] = []
    tools_called: List[Dict[str, Any]] = []
    self_eval: Dict[str, Any]
    failure_type: str
    human_label: Optional[str] = None
    action_taken: Optional[str] = None
