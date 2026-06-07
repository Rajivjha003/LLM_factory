from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts"))

from scripts.run_sft_lora import run_lora_training

router = APIRouter()

# Global dict to track job status. In production, use Redis or a database.
jobs = {}

class TrainRequest(BaseModel):
    config_path: str = "configs/training/sft_qwen_0_5b_lora.yaml"

def run_training_task(job_id: str, config_path: str):
    try:
        jobs[job_id] = {"status": "running"}
        run_lora_training(config_path)
        jobs[job_id] = {"status": "completed"}
    except Exception as e:
        jobs[job_id] = {"status": "failed", "error": str(e)}

@router.post("/lora")
def start_lora_training(req: TrainRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending"}
    background_tasks.add_task(run_training_task, job_id, req.config_path)
    return {"status": "accepted", "job_id": job_id, "message": "LoRA training started in background."}

@router.get("/status/{job_id}")
def get_training_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, **jobs[job_id]}
