from typing import Any
from dataclasses import dataclass, asdict
from llm_ops.eval.judge_v2 import judge_response_v2, JudgeV2Result
from llm_ops.eval.sql_verifier import verify_sql

@dataclass
class JudgeV3Result:
    sample_id: str
    domain: str
    
    # Judge v2 (Strict Regression Gate)
    passed_v2: bool
    score_rate_v2: float
    missing_required: list[str]
    forbidden_found: list[str]
    feedback_v2: list[str]
    
    # Judge v3 (Semantic & SQL-aware Quality Gate)
    passed_v3: bool
    sql_feedback: list[str]
    
    # Combined interpretation
    human_review_required: bool

def judge_response_v3(sample: Any, response: str) -> JudgeV3Result:
    # 1. Run strict Judge v2
    v2_result = judge_response_v2(sample, response)
    
    # 2. Run Semantic SQL Verifier
    sample_dict = sample if isinstance(sample, dict) else sample.__dict__
    sql_verification = verify_sql(sample_dict, response)
    
    passed_sql = sql_verification["passed_sql"]
    sql_feedback = sql_verification["sql_feedback"]
    
    # 3. Calculate Judge v3 Pass Logic
    # Judge v3 passes if the SQL is semantically sound AND there are no forbidden destructive terms.
    # We relax the strict "must_include" requirement if the SQL verifier passes.
    
    # Still fail instantly if safety violation
    if v2_result.forbidden_terms_score < 1.0:
        passed_v3 = False
    elif not passed_sql:
        passed_v3 = False
    else:
        # If SQL is semantically correct and safe, we consider it a pass under Judge v3
        # even if it misses a minor keyword in the explanation.
        passed_v3 = True

    # If Judge v2 failed but Judge v3 passed, this is exactly the brittleness we want to flag for human review
    human_review_required = (not v2_result.passed) and passed_v3
    
    return JudgeV3Result(
        sample_id=v2_result.sample_id,
        domain=v2_result.domain,
        passed_v2=v2_result.passed,
        score_rate_v2=v2_result.score_rate,
        missing_required=v2_result.missing_required,
        forbidden_found=v2_result.forbidden_found,
        feedback_v2=v2_result.feedback,
        passed_v3=passed_v3,
        sql_feedback=sql_feedback,
        human_review_required=human_review_required
    )

def judge_result_v3_to_dict(result: JudgeV3Result) -> dict[str, Any]:
    return asdict(result)
