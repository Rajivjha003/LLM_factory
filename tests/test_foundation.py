import unittest
import sys
import os
from pathlib import Path

# Add src to python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llm_ops.utils.config import load_config
from llm_ops.utils.gpu import get_gpu_info
from llm_ops.observability.logging import setup_logging
from llm_ops.exceptions.errors import LLMOpsError

class TestFoundation(unittest.TestCase):
    
    def test_imports(self):
        """Confirm import path works."""
        from llm_ops.utils import gpu
        from llm_ops.utils import config
        from llm_ops.observability import logging
        from llm_ops.exceptions import errors
        from llm_ops.exceptions import handlers
        
        self.assertTrue(hasattr(gpu, 'get_gpu_info'))
        
    def test_cuda(self):
        """Confirm CUDA check doesn't crash."""
        info = get_gpu_info()
        self.assertIn("available", info)
        self.assertIn("total_vram_gb", info)
        
    def test_logging(self):
        """Confirm logging initialization works."""
        logger = setup_logging()
        self.assertIsNotNone(logger)
        logger.info("Test logging initialized successfully.")
        
    def test_config(self):
        """Confirm configuration loading works."""
        os.environ["MAX_VRAM_GB"] = "12"
        os.environ["BATCH_SIZE"] = "8"
        
        config = load_config()
        self.assertEqual(config.hardware.max_vram_gb, 12)
        self.assertEqual(config.training.batch_size, 8)
        self.assertTrue(config.hardware.use_flash_attention)

if __name__ == "__main__":
    unittest.main()
