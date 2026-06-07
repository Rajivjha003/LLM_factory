import subprocess
from pathlib import Path

def test_eval_v2_files_valid():
    eval_dir = Path("data/eval_v2")
    assert eval_dir.exists()
    
    result = subprocess.run(
        ["python", "scripts/validate_eval_data.py", "--eval-dir", "data/eval_v2", "--expected-count", "50"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Validation failed: {result.stderr or result.stdout}"

