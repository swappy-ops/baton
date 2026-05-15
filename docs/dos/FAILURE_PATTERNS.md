# FAILURE_PATTERNS.md - Forensic Instability Log

## 1. Threading Failures
- **Pattern**: Blocking the message thread during high-volume retrieval.
- **Fix**: Offload retrieval to `@SafeThread` and use async bridges.

## 2. Memory Bloat
- **Pattern**: Accumulating redundant JSON snapshots without distillation.
- **Fix**: Mandatory `DistillationNode` pass every 5 interactions.

## 3. Semantic Fragmentation
- **Pattern**: Multiple specialist nodes using different names for the same subsystem.
- **Fix**: Centralize terminology via `TERMINOLOGY.md`.

## 4. Hardware Overreach
- **Pattern**: Loading >2 large models simultaneously on 8GB VRAM.
- **Fix**: Implement automatic model unloading and re-mapping to `phi4`.
