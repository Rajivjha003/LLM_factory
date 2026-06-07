# Hardware Constraints

## Primary Hardware Context
- **Machine**: Alienware
- **CPU**: Intel Core i9-14900HX
- **RAM**: 64GB System RAM
- **GPU**: NVIDIA RTX 4090
- **VRAM**: 16GB
- **OS**: Windows 11 Home (Build 26200) w/ WSL (Ubuntu)

## Technical Constraints & Guidelines
1. **Local Execution Priority**: For AI tasks requiring `< 14GB VRAM`, local execution is strictly preferred over Cloud APIs.
2. **CUDA Support**: Default to CUDA 13.0+ compatible syntax. 
3. **Optimizations**:
   - High-performance, multi-threaded code is required.
   - Utilize PyTorch with `FlashAttention-2` and `xformers` by default for maximum throughput.
   - Leverage the massive 64GB System RAM for memory-intensive indexing, caching, and data processing.
4. **Library Variants**: Avoid 'lite' versions of libraries. The system is powerful enough to handle full versions.
