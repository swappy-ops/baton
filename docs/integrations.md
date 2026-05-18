# Baton Ecosystem

Baton orchestrates external systems. It does NOT own them.

## Integrated systems
- **ProjSkep** — semantic memory, neural observatory, real-time telemetry
- **Ollama** — local LLM inference (phi4, qwen2.5-coder:7b)
- **ChromaDB** — vector retrieval (managed by ProjSkep)

## Ownership boundaries
Baton owns: agents, workflows, orchestration logic, task routing
Baton does NOT own: inference servers, vector DBs, UI rendering engines
