import sys

def check_vllm():
    print("=== vLLM Environment Check ===")
    try:
        import vllm
        print(f"[OK] vLLM is installed. Version: {vllm.__version__}")
        
        # Check if vLLM can detect CUDA
        try:
            from vllm.engine.arg_utils import EngineArgs
            print("[OK] vLLM EngineArgs can be imported.")
        except Exception as e:
            print(f"[ERROR] Failed to import vLLM internals: {e}")
            
    except ImportError:
        print("[ERROR] vLLM is NOT installed. Inference will not be available.")
        sys.exit(1)

if __name__ == "__main__":
    check_vllm()
