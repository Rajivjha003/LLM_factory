from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts"))

from scripts.run_adapter_eval import run_evaluation
from scripts.compare_eval_runs import generate_comparison

router = APIRouter()

# Global dict to track eval jobs
eval_jobs = {}

class EvalRequest(BaseModel):
    base_model: str = "/home/rajiv/models/base/qwen2_5_0_5b_instruct"
    adapter: str = "models/adapters/qwen_0_5b_merchmix_v1"
    eval_dir: str = "data/eval"
    output_jsonl: str = "reports/eval_reports/qwen_0_5b_adapter_results.jsonl"

class CompareRequest(BaseModel):
    baseline: str = "reports/eval_reports/qwen_0_5b_baseline_results.jsonl"
    candidate: str = "reports/eval_reports/qwen_0_5b_adapter_results.jsonl"
    output_md: str = "reports/eval_reports/comparison_report.md"

def run_eval_task(job_id: str, req: EvalRequest):
    try:
        eval_jobs[job_id] = {"status": "running"}
        run_evaluation(req.base_model, req.adapter, req.eval_dir, req.output_jsonl)
        eval_jobs[job_id] = {"status": "completed", "output_jsonl": req.output_jsonl}
    except Exception as e:
        eval_jobs[job_id] = {"status": "failed", "error": str(e)}

@router.post("/run")
def start_eval(req: EvalRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    eval_jobs[job_id] = {"status": "pending"}
    background_tasks.add_task(run_eval_task, job_id, req)
    return {"status": "accepted", "job_id": job_id, "message": "Evaluation started in background."}

@router.get("/status/{job_id}")
def get_eval_status(job_id: str):
    if job_id not in eval_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, **eval_jobs[job_id]}

@router.post("/compare")
def compare_evals(req: CompareRequest):
    try:
        result = generate_comparison(req.baseline, req.candidate, req.output_md)
        return {"status": "success", "comparison": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
