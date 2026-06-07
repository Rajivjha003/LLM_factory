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
