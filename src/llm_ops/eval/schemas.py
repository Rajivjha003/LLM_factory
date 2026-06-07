from pydantic import BaseModel
from typing import List

class EvalSample(BaseModel):
    id: str
    domain: str
    difficulty: str
    prompt: str
    expected_traits: List[str]
    must_include: List[str]
    must_not_include: List[str]
    max_score: int

class EvalResult(BaseModel):
    sample_id: str
    domain: str
    prompt: str
    response: str
    score: float
    passed: bool
    reasoning: str
