from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
from pathlib import Path

# Add src to python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts"))

from scripts.validate_sft_data import validate_sft_file
from scripts.inspect_sft_data import generate_dataset_stats

router = APIRouter()

class ValidateRequest(BaseModel):
    file_path: str = "data/sft/merchmix_sft_v1.jsonl"

class InspectRequest(BaseModel):
    file_path: str = "data/sft/merchmix_sft_v1.jsonl"

@router.post("/validate")
def validate_dataset(req: ValidateRequest):
    """
    Validates a JSONL dataset against the SFTSample schema and strict SQL safety rules.
    """
    try:
        valid_count, errors = validate_sft_file(Path(req.file_path))
        if errors:
            return {"status": "error", "valid_count": valid_count, "errors": errors}
        return {"status": "success", "valid_count": valid_count, "message": "All samples are valid and safe."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/inspect")
def inspect_dataset(file_path: str = "data/sft/merchmix_sft_v1.jsonl"):
    """
    Returns domain distributions and dataset statistics.
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        stats = generate_dataset_stats(path)
        return {"status": "success", "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import subprocess
import logging

logger = logging.getLogger(__name__)

class EvalValidateRequest(BaseModel):
    eval_dir: str = "data/eval_v2"
    expected_count: int = 50

@router.post("/eval/validate")
def validate_eval(req: EvalValidateRequest):
    try:
        cmd = ["python", "scripts/validate_eval_data.py", "--eval-dir", req.eval_dir]
        if req.expected_count:
            cmd.extend(["--expected-count", str(req.expected_count)])
        
        logger.info(f"Running eval validation: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"Validation failed: {result.stderr or result.stdout}")
            raise HTTPException(status_code=400, detail=result.stdout or result.stderr)
            
        return {"status": "success", "output": result.stdout}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error during eval validation")
        raise HTTPException(status_code=500, detail=str(e))

class HashRequest(BaseModel):
    dataset_dir: str = "data/eval_v2"
    output_file: str = "reports/eval_reports/eval_v2_hash_manifest.json"

@router.post("/eval/hash")
def generate_hash(req: HashRequest):
    try:
        cmd = ["python", "scripts/build_dataset_hash_manifest.py", "--dataset-dir", req.dataset_dir, "--output", req.output_file]
        logger.info(f"Running hash generation: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=result.stderr or result.stdout)
            
        return {"status": "success", "output": result.stdout}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error during hash generation")
        raise HTTPException(status_code=500, detail=str(e))

class BuildSFTRequest(BaseModel):
    base: str = "data/sft/merchmix_sft_v1.jsonl"
    additions: str = "data/sft/merchmix_sft_v2_additions.jsonl"
    output_file: str = "data/sft/merchmix_sft_v2.jsonl"
    expected_count: int = 300

@router.post("/sft/build")
def build_sft(req: BuildSFTRequest):
    try:
        cmd = ["python", "scripts/build_sft_v2.py", "--base", req.base, "--additions", req.additions, "--output", req.output_file, "--expected-count", str(req.expected_count)]
        logger.info(f"Running SFT build: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=result.stderr or result.stdout)
            
        return {"status": "success", "output": result.stdout}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error building SFT dataset")
        raise HTTPException(status_code=500, detail=str(e))

class OverlapRequest(BaseModel):
    sft_path: str = "data/sft/merchmix_sft_v2.jsonl"
    eval_dir: str = "data/eval_v2"
    output_file: str = "reports/eval_reports/sft_v2_eval_v2_overlap_report.md"
    fail_threshold: float = 0.80

@router.post("/sft/check-overlap")
def check_overlap(req: OverlapRequest):
    try:
        cmd = ["python", "scripts/check_sft_eval_overlap_strict.py", "--sft", req.sft_path, "--eval-dir", req.eval_dir, "--output", req.output_file, "--fail-threshold", str(req.fail_threshold)]
        logger.info(f"Running strict overlap check: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=result.stdout or result.stderr)
            
        return {"status": "success", "output": result.stdout}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error checking overlap")
        raise HTTPException(status_code=500, detail=str(e))
