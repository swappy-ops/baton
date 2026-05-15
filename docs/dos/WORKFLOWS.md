# WORKFLOWS.md - Production Creative Operations

## 1. Core Workflow Map
These workflows are implemented in `runtime/workflows.py` and utilize the `WorkflowEngine`.

| Workflow | Objective | Specialist |
| :--- | :--- | :--- |
| **Repo Architecture Analysis** | Map codebase topology and patterns. | Architecture (phi4) |
| **Assisted Debugging** | Forensic error analysis with prior recall. | Code (qwen2.5-coder) |
| **Refactoring** | Propose continuity-preserving edits. | Code (qwen2.5-coder) |
| **UX Critique** | Interface audit for SaaS drift. | UX (phi4) |
| **Plugin-Chain Recall** | Retrieve spectral processing history. | Music (phi4) |
| **Runtime Diagnostics** | Verify stability and thread safety. | Architecture (phi4) |
| **Architecture Recall** | Retrieve session-spanning reasoning. | Architecture (phi4) |
| **Project Summary** | High-density semantic executive report. | General (phi4) |
| **Dependency Tracing** | Map semantic coupling between nodes. | Architecture (phi4) |
| **Topology Exploration** | Structural discovery of orphaned code. | Architecture (phi4) |

## 2. Operational Constraints
- **Retrieval-First**: No workflow proceeds without a `Neural Observatory` pass.
- **VRAM Gating**: Workflows dynamically scale retrieval budgets via `runtime/context_budget.py`.
- **Forensic Tracing**: All outputs are logged to `traces/runtime/`.

## 3. Cross-Links
- [GLOBAL_RULES.md](GLOBAL_RULES.md) - Governance Primitives
- [SEMANTIC_CONTINUITY.md](SEMANTIC_CONTINUITY.md) - Memory Principles
- [SYSTEM_CONSTRAINTS.md](SYSTEM_CONSTRAINTS.md) - Hardware Limits
- [TERMINOLOGY.md](TERMINOLOGY.md) - Canonical Lexicon
