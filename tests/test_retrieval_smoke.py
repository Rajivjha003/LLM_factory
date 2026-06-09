import pytest
import subprocess
from src.llm_ops.core.config import settings

@pytest.mark.integration
def test_retrieval_smoke_script_execution():
    # This runs the actual script to ensure it passes end-to-end
    result = subprocess.run(
        ["uv", "run", "python", "scripts/test_retrieval.py"],
        capture_output=True,
        text=True
    )
    
    # The script exits with 0 if it successfully matched evidence for all queries
    assert result.returncode == 0, f"Retrieval script failed:\n{result.stderr}\n{result.stdout}"
