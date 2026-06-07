import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

@dataclass
class HardwareConfig:
    max_vram_gb: int = field(default=16)
    max_system_ram_gb: int = field(default=64)
    use_flash_attention: bool = field(default=True)
    cuda_device: str = field(default="cuda:0")

@dataclass
class TrainingConfig:
    batch_size: int = field(default=4)
    gradient_accumulation_steps: int = field(default=4)
    learning_rate: float = field(default=2e-5)
    max_seq_length: int = field(default=4096)
    use_qlora: bool = field(default=True)

@dataclass
class LLMOpsConfig:
    project_root: Path = field(default_factory=lambda: Path(os.getcwd()))
    data_dir: Path = field(default_factory=lambda: Path(os.getcwd()) / "data")
    output_dir: Path = field(default_factory=lambda: Path(os.getcwd()) / "artifacts")
    
    hardware: HardwareConfig = field(default_factory=HardwareConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    
    def __post_init__(self):
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

def load_config() -> LLMOpsConfig:
    """
    Loads configuration from environment variables or returns defaults.
    """
    config = LLMOpsConfig()
    
    # Simple override examples based on environment variables
    if "MAX_VRAM_GB" in os.environ:
        config.hardware.max_vram_gb = int(os.environ["MAX_VRAM_GB"])
        
    if "BATCH_SIZE" in os.environ:
        config.training.batch_size = int(os.environ["BATCH_SIZE"])
        
    return config
