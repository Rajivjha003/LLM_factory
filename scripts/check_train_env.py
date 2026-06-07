import sys
from pathlib import Path

# Add src to python path so we can import llm_ops
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llm_ops.utils.gpu import print_gpu_stats, get_gpu_info

def check_training_environment():
    print("=== Training Environment Check ===")
    print_gpu_stats()
    
    info = get_gpu_info()
    if not info["available"]:
        print("\n[ERROR] PyTorch or CUDA is missing. Cannot train.")
        sys.exit(1)
        
    cuda_version = float(info["cuda_version"]) if info["cuda_version"] else 0.0
    if cuda_version < 13.0:
        print(f"\n[WARNING] CUDA Version {cuda_version} is less than 13.0.")
    else:
        print("\n[OK] CUDA Version >= 13.0 detected.")
        
    if not info["flash_attention_available"]:
        print("[WARNING] FlashAttention-2 is NOT installed. Training will be slower.")
    else:
        print("[OK] FlashAttention-2 is available.")
        
    if not info["xformers_available"]:
        print("[WARNING] Xformers is NOT installed.")
    else:
        print("[OK] Xformers is available.")
        
    if info["total_vram_gb"] < 16.0:
        print(f"[WARNING] VRAM ({info['total_vram_gb']:.2f} GB) is less than the expected 16GB for RTX 4090.")
    else:
        print("[OK] Detected >= 16GB VRAM.")

if __name__ == "__main__":
    check_training_environment()
