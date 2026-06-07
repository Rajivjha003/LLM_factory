# GGUF Strategy

## Purpose
Deploy local quantized models through llama.cpp.

## Formats To Benchmark
- Q4_K_M
- Q5_K_M
- Q8_0

## Selection Rule
Use Q4_K_M first. If quality loss is visible, use Q5_K_M. Use Q8_0 when quality matters more than size/speed.
