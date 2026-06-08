from fastapi import APIRouter
from src.llm_ops.core.schemas import GuardrailResult
from src.llm_ops.guardrails.input_guardrails import check_input_guardrails
from src.llm_ops.guardrails.output_guardrails import check_output_guardrails
from pydantic import BaseModel

router = APIRouter()

class InputCheckRequest(BaseModel):
    query: str
    mode: str = "direct"

class OutputCheckRequest(BaseModel):
    response_text: str
    mode: str = "direct"

@router.post("/guardrails/check-input", response_model=GuardrailResult)
async def check_input(req: InputCheckRequest):
    return check_input_guardrails(req.query, req.mode)

@router.post("/guardrails/check-output", response_model=GuardrailResult)
async def check_output(req: OutputCheckRequest):
    class FakeResponse:
        answer = req.response_text
    return check_output_guardrails(FakeResponse(), req.mode)
