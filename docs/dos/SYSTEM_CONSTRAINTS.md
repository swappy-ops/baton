# SYSTEM_CONSTRAINTS.md - Operational Boundaries

## 1. Hardware (Ryzen 5 / RX 6600)
- **VRAM Limit**: 8GB (Strict operation target: <6GB).
- **Compute**: Prioritize sparse activation and lightweight models (`phi4`).
- **Acceleration**: Vulkan/HSA (AMD GPU).

## 2. Software
- **Context Window**: 8k tokens (Target <4k for speed).
- **Retrieval Latency**: <500ms for L1 recall.
- **Persistence**: SQLite (Bridge) + Chroma (Semantic) + JSON (Distilled).

## 3. Design
- **1px Precision**: All UI elements must use industrial, forensic aesthetics.
- **No SaaS**: Avoid rounded corners, soft shadows, and generic dashboards.
