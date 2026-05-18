# Baton — Runtime Truth Audit

> Generated: 2026-05-18
> Status: VERIFIED — all entries confirmed by file inspection

## Entrypoint

| Method | Command | File |
|--------|---------|------|
| Primary | `uvicorn baton_server.main:app --host 0.0.0.0 --port 8000` | `baton_server/main.py:91` |
| Docker CMD | `["uvicorn", "baton_server.main:app", "--host", "0.0.0.0", "--port", "8000"]` | `Dockerfile:17` |
| Shell script | `./start.sh` — creates venv, installs deps, starts uvicorn | `start.sh` |
| PowerShell | `.\launch_dev.ps1` — starts backend + orchestrator + UI dev server | `launch_dev.ps1` |

## Ports

| Port | Protocol | Purpose | Verified |
|------|----------|---------|----------|
| 8000 | HTTP + WebSocket | FastAPI server + WS `/ws` | `baton_server/main.py` |

No other ports used by the server.

## Memory

| Type | Location | Format | Verified |
|------|----------|--------|----------|
| Session memory | `baton_server/db/sessions/` | JSON files, keeps last 5 | `services/session_memory.py` |
| SQLite traces | `baton_server/db/baton.db` | Tables: `traces`, `suggestions` | `db/manager.py` |
| ChromaDB | `baton_memory/` | `chroma.sqlite3` + collection data | Directory exists |
| Legacy DB | `baton_server/db/projskep.db` | Orphan — not referenced by any code | `grep -r projskep.db` = 0 matches |

## Model Host

| System | URL | Config | Used By |
|--------|-----|--------|---------|
| Ollama | `http://192.168.1.19:11434` (hardcoded in prototypes) | `OLLAMA_HOST` env var (docker-compose.yml) | `baton/` package + archived prototypes only |
| Models | `phi4` (router), `qwen2.5-coder:7b` (specialist) | — | `baton/agents/nodes.py` |

**CRITICAL:** `baton_server` does NOT connect to Ollama. Only `baton/` package and root prototypes do.

## Task Flow (VERIFIED)

```
User intent → WebSocket /api/intent → session_memory.save_state()
                                      → manager.broadcast_event()
                                      → log_trace() → SQLite

OrchestrationEngine.start_mock_streams()
  → _metric_stream() every 3s → event_bus → attention_engine → WebSocket broadcast
  → _background_tasks() every 15s → run_workflow() → event_bus → WebSocket broadcast
```

Source: `baton_server/main.py:30-34`, `orchestration/engine.py:72-103`

## Dependencies — Active Runtime (Docker)

| Package | Version | Used By |
|---------|---------|---------|
| fastapi | >=0.115.0 | `baton_server/main.py` |
| uvicorn[standard] | >=0.34.0 | Server runner |
| aiosqlite | >=0.20.0 | `db/manager.py` |
| websockets | >=14.0 | `websocket/manager.py` |
| httpx | >=0.28.0 | `services/health_check.py` |
| python-dotenv | >=1.0.0 | Env loading |
| pydantic | >=2.0.0 | `schemas/events.py` |

Source: `requirements-server.txt`, `Dockerfile:10-11`

## Dependencies — baton/ Package (NOT in Docker)

| Package | Version | Used By |
|---------|---------|---------|
| watchdog | >=6.0.0 | `scripts/event_orchestrator.py` |
| langgraph | >=0.3.0 | `graphs/router_graph.py` |
| langchain | >=0.3.0 | `agents/nodes.py` |
| langchain-community | >=0.3.0 | Agent tools |
| langchain-ollama | >=0.2.0 | `agents/nodes.py` |
| chromadb | >=1.0.0 | `retrieval/pipeline.py` |
| sentence-transformers | >=3.0.0 | `retrieval/pipeline.py` |

Source: `requirements.txt` — NOT installed in Docker (`Dockerfile:10` uses `requirements-server.txt`)

## UI

| Component | Path | Status | Notes |
|-----------|------|--------|-------|
| Active UI | `baton_server/static/index.html` | SERVED | 1508 lines vanilla HTML/CSS/JS, served at `/` |
| React app | `baton_ui/` | NOT SERVED | Vite + React + TS, uses socket.io-client (INCOMPATIBLE with raw WS) |

WebSocket protocol: **Raw WebSocket** (not Socket.IO)
Source: `websocket/manager.py` — uses `websocket.send_text()` / `websocket.send_bytes()`

## Server Module Dependency Graph (VERIFIED)

```
baton_server/main.py
├── baton_server/websocket/manager.py
├── baton_server/api/__init__.py
├── baton_server/orchestration/engine.py
│   └── baton_server/services/event_bus.py
│       ├── baton_server/services/attention_engine.py
│       └── baton_server/websocket/manager.py
├── baton_server/services/session_memory.py
├── baton_server/db/manager.py
└── baton_server/schemas/events.py
```

All imports resolve. No circular dependencies. No missing modules.

## Docker Configuration

| Setting | Value | Source |
|---------|-------|--------|
| Base image | `python:3.11-slim` | `Dockerfile:1` |
| Workdir | `/app` | `Dockerfile:3` |
| Exposed port | 8000 | `Dockerfile:15` |
| Volume mount (compose) | `.:/app`, `baton_data:/app/baton_server/db`, `baton_embeddings:/app/baton_memory` | `docker-compose.yml:6-9` |
| Env file | `.env` | `docker-compose.yml:11` |
| OLLAMA_HOST | `http://host.docker.internal:11434` | `docker-compose.yml:13` |
