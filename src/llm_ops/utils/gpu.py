import logging

logger = logging.getLogger(__name__)

def check_cuda_availability() -> bool:
    """Checks if CUDA is available using PyTorch."""
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        logger.warning("PyTorch is not installed.")
        return False

def get_gpu_info() -> dict:
    """Retrieves basic GPU information and VRAM stats."""
    info = {
        "available": False,
        "device_count": 0,
        "current_device": None,
        "device_name": None,
        "total_vram_gb": 0.0,
        "flash_attention_available": False,
        "xformers_available": False,
        "cuda_version": None
    }
    
    try:
        import torch
        if torch.cuda.is_available():
            info["available"] = True
            info["device_count"] = torch.cuda.device_count()
            info["current_device"] = torch.cuda.current_device()
            info["device_name"] = torch.cuda.get_device_name(0)
            
            # Convert bytes to GB
            total_memory = torch.cuda.get_device_properties(0).total_memory
            info["total_vram_gb"] = total_memory / (1024 ** 3)
            info["cuda_version"] = torch.version.cuda
            
            # Check flash attention
            try:
                import flash_attn
                info["flash_attention_available"] = True
            except ImportError:
                info["flash_attention_available"] = False
                
            # Check xformers
            try:
                import xformers
                info["xformers_available"] = True
            except ImportError:
                info["xformers_available"] = False
                
    except ImportError:
        pass
        
    return info

def print_gpu_stats():
    """Prints a friendly summary of the GPU stats."""
    info = get_gpu_info()
    if info["available"]:
        print(f"--- GPU STATUS ---")
        print(f"Device: {info['device_name']}")
        print(f"CUDA Version: {info['cuda_version']}")
        print(f"Total VRAM: {info['total_vram_gb']:.2f} GB")
        print(f"FlashAttention-2: {'Installed' if info['flash_attention_available'] else 'Not Installed'}")
        print(f"Xformers: {'Installed' if info['xformers_available'] else 'Not Installed'}")
    else:
        print("--- GPU STATUS ---")
        print("CUDA is NOT available or PyTorch is not installed.")
