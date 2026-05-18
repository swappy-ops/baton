#!/usr/bin/env python3
"""Generate docs/architecture.md from repo structure."""
import os

ARCH_CONTENT = """# Baton Architecture

Auto-generated. Do not edit manually — run scripts/update_architecture.py

```mermaid
graph TD
    User([User Intent]) --> Baton[Baton Orchestration Layer]
    Baton --> Agents[Agent Nodes]
    Baton --> Memory[Memory Manager]
    Baton --> Workflows[Workflow Engine]
    Baton --> ProjSkep[ProjSkep Neural Observatory]
    Agents --> Ollama[Ollama LLM]
    Memory --> ChromaDB[ChromaDB]
    ProjSkep --> Telemetry[Real-time Telemetry]
    ProjSkep --> SemanticContinuity[Semantic Continuity]
```

## Components

| Component | Path | Role |
|-----------|------|------|
| Orchestration Server | baton_server/ | FastAPI, WebSocket, event routing |
| Agent Layer | baton/agents/ | LangGraph nodes, intent routing |
| Memory | baton/memory/ | ChromaDB retrieval pipeline |
| Runtime | baton/runtime/ | Context budget, task contracts |
| Workflows | baton/graphs/ | LangGraph orchestration graphs |
| UI | baton_ui/ | React/Vite control surface |
| Integrations | integrations/ | External system connectors |
"""

os.makedirs("docs", exist_ok=True)
with open("docs/architecture.md", "w") as f:
    f.write(ARCH_CONTENT)
print("docs/architecture.md generated")
