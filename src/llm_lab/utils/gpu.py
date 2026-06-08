from __future__ import annotations

import torch


def print_gpu_summary() -> None:
    print("CUDA available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        idx = torch.cuda.current_device()
        props = torch.cuda.get_device_properties(idx)
        print("GPU:", props.name)
        print("VRAM GB:", round(props.total_memory / 1024**3, 2))
        print("Capability:", props.major, props.minor)
