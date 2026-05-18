# Known Limitations

## Current Version: 0.1.0 → 1.0.0 (in progress)

### Telemetry is Mock
The OrchestrationEngine generates simulated telemetry data (metrics, background workflows). This is intentional — the UI needs live data to demonstrate observability. Real telemetry from actual agent execution requires the `baton/` package with full ML stack.

### baton/ Package Not in Docker
The `baton/` directory contains the full agent orchestration layer (LangGraph, ChromaDB, Ollama integration). It is NOT included in the Docker image because:
- Docker uses `requirements-server.txt` (minimal deps)
- `requirements.txt` includes heavy ML packages (chromadb, sentence-transformers, langchain, langgraph)
- These packages add significant image size and build time

To use the `baton/` package, install locally with `./install.sh` and answer "Y" to the ML stack prompt.

### React UI Not Integrated
`archive/baton_ui_react/` contains a React/Vite frontend that was never integrated:
- Uses `socket.io-client` but server uses raw WebSockets
- Not served by FastAPI
- Not built into Docker image

The active UI is `baton_server/static/index.html` (vanilla HTML/CSS/JS).

### Ollama Not Required for Server
The FastAPI server does NOT connect to Ollama. Ollama is only used by:
- `baton/` package agents (LangGraph nodes)
- Archived prototype scripts

The server runs fully without Ollama.

### Hardcoded IP in Prototypes
Archived prototype scripts (`archive/prototypes/`) contain hardcoded `http://192.168.1.19:11434` for Ollama. These are archived and not part of the runtime.

### Single-User Only
The system is designed for single-user local deployment. No authentication, multi-user support, or role-based access.

### No Persistent Workflow State
Background workflows are simulated. Real task execution requires the `baton/` package with Ollama connected.
