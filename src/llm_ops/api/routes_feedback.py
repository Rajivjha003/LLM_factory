from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class FeedbackRequest(BaseModel):
    trace_id: str
    feedback: str
    is_positive: bool

@router.post("/feedback")
async def feedback_endpoint(req: FeedbackRequest):
    return {"status": "feedback logged"}
