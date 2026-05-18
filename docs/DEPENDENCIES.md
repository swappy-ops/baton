# Baton — Dependency Map

> Generated: 2026-05-18
> Method: Manual inspection of all import statements across the codebase

---

## 1. baton_server/ (ACTIVE RUNTIME — in Docker)

### baton_server/main.py
```
fastapi (FastAPI, WebSocket)
fastapi.middleware.cors (CORSMiddleware)
fastapi.responses (HTMLResponse, FileResponse)
fastapi.staticfiles (StaticFiles)
datetime, asyncio, json, os
→ baton_server.websocket.manager (manager)
→ baton_server.api (router)
→ baton_server.orchestration.engine (engine)
→ baton_server.services.session_memory (session_memory)
→ baton_server.db.manager (log_trace, init_db)
```

### baton_server/api/__init__.py
```
fastapi (APIRouter)
```

### baton_server/websocket/manager.py
```
json, asyncio, typing (List)
fastapi (WebSocket)
```

### baton_server/db/manager.py
```
os, aiosqlite, datetime
uuid, json (inline imports)
```

### baton_server/orchestration/engine.py
```
asyncio, uuid, time, datetime
→ baton_server.services.event_bus (event_bus)
→ baton_server.schemas.events (SystemEvent, TracePayload, WorkflowPayload, MetricPayload)
```

### baton_server/services/event_bus.py
```
asyncio, typing (Dict, List, Callable)
→ baton_server.services.attention_engine (attention_engine)
→ baton_server.schemas.events (SystemEvent)
→ baton_server.websocket.manager (manager)
```

### baton_server/services/attention_engine.py
```
time, typing (List, Dict, Any)
→ baton_server.schemas.events (SystemEvent)
```

### baton_server/services/session_memory.py
```
json, os, datetime, typing (Dict, Any, Optional)
```

### baton_server/services/health_check.py
```
asyncio, httpx, sys, os
socket (standard library)
```

### baton_server/services/orchestrator_bridge.py
```
asyncio, json, time, os, datetime
→ baton_server.websocket.manager (manager)
```

### baton_server/schemas/events.py
```
pydantic (BaseModel)
typing (Any, Optional, Literal)
datetime, uuid
```

---

## 2. baton/ (OPTIONAL PACKAGE — NOT in Docker)

### baton/agents/nodes.py
```
langchain_ollama (ChatOllama)
langchain_core.messages (BaseMessage, HumanMessage, AIMessage)
→ baton.retrieval.pipeline (get_retrieval_pipeline)
→ baton.runtime.task_contract (get_contract_for_task)
→ baton.runtime.context_budget (get_context_budget_manager)
→ baton.runtime.stability (get_stability_manager)
```

### baton/agents/distillation_node.py
```
langchain_core.messages (HumanMessage, AIMessage)
→ baton.agents.nodes (get_model)
→ baton.memory.manager (get_memory_manager)
→ baton.runtime.dos_sync (get_dos_sync_engine)
```

### baton/memory/manager.py
```
os, json, datetime
→ baton.retrieval.pipeline (get_retrieval_pipeline)
→ baton.runtime.dos_sync (get_dos_sync_engine)
```

### baton/memory/governance.py
```
os, shutil, datetime, timedelta
```

### baton/retrieval/pipeline.py
```
chromadb, chromadb.config (Settings)
json, time, datetime, os
sentence_transformers (SentenceTransformer)
```

### baton/retrieval/structural_index.py
```
os, ast
→ baton.retrieval.pipeline (get_retrieval_pipeline)
```

### baton/runtime/workflows.py
```
→ baton.agents.nodes (get_model)
langchain_core.messages (HumanMessage, AIMessage)
```

### baton/runtime/context_budget.py
```
→ baton.runtime.task_contract (TaskContract)
```

### baton/runtime/task_contract.py
```
typing (List, Optional)
dataclasses (dataclass, dataclass, field)
```

### baton/runtime/stability.py
```
subprocess, time, os
```

### baton/runtime/dos_sync.py
```
re, logging, os
```

### baton/graphs/router_graph.py
```
os, json, datetime, typing (TypedDict, List, Dict, Any, Annotated)
langgraph.graph (StateGraph, END)
langchain_core.messages (BaseMessage, AIMessage, HumanMessage)
→ baton.agents.nodes (intent_router_node, retrieval_node, specialist_node, distillation_node)
```

### baton/scripts/ingest_docs.py
```
os, sys
→ baton.retrieval.pipeline (get_retrieval_pipeline)
```

### baton/scripts/event_orchestrator.py
```
time, os, sys, uuid, threading (Timer)
watchdog.observers (Observer)
watchdog.events (FileSystemEventHandler)
→ baton.graphs.router_graph (build_router_graph)
langchain_core.messages (HumanMessage)
```

### baton/scripts/validate_continuity.py
```
os, json, datetime
→ baton.runtime.dos_sync (get_dos_sync_engine)
```

---

## 3. Root-Level Prototypes (ARCHIVED — not imported by anything)

| File | Imports | Status |
|------|---------|--------|
| `baton_core.py` | ollama, chromadb, sentence_transformers | Standalone REPL — archived |
| `multi_agent.py` | ollama | Standalone multi-agent REPL — archived |
| `tools_agent.py` | ollama, subprocess | Standalone tool-calling REPL — archived |
| `watcher_agent.py` | time, ollama, watchdog | Standalone file watcher — archived |
| `orchestrator.py` | (no imports — just a string) | System prompt template — archived |
| `test_baton.py` | ollama | Single Ollama test call — archived |
| `memory_test.py` | sentence_transformers | Embedding length test — archived |

---

## 4. baton_ui/ (ARCHIVED — NOT served, NOT built)

| File | Imports | Status |
|------|---------|--------|
| `src/App.tsx` | react, zustand, framer-motion, 8 local components | Not served by server |
| `src/main.tsx` | react-dom | Entry point — not built |
| `src/hooks/useWebSocket.ts` | react, zustand | Uses raw WebSocket (correct) |
| `src/stores/useStore.ts` | zustand, zustand/middleware | State named `ProjskepState` (legacy) |
| `package.json` | socket.io-client | INCOMPATIBLE — server uses raw WebSocket |

---

## 5. Dead Code / Orphan Files

| File/Dir | Reason | Action |
|----------|--------|--------|
| `baton_server/db/projskep.db` | Not referenced by any Python code | Archive |
| `docs/ARCHITECTURE.md` | Outdated content ("cinematic creative operating system", "Spectral Engine") | Replace |
| `docs/architecture.md` | Auto-generated, contains "ProjSkep" references | Delete (replaced by canonical) |
| `integrations/projskep/` | External system docs — not used by runtime | Archive |
| `scripts/update_architecture.py` | Generates outdated architecture.md | Archive |
| `configs/` | Editor tool configs (aider, continue) — not runtime | Archive |
| `launch_dev.ps1` | Hardcoded `D:/Baton` path, Windows-only dev script | Archive |
| `baton_ui/` | React app not served, wrong WS library | Archive |
| `incoming_tasks/` | Gitignored runtime artifact | Archive |
| `processing_tasks/` | Gitignored runtime artifact | Archive |
| `completed_tasks/` | Gitignored runtime artifact | Archive |
| `failed_tasks/` | Gitignored runtime artifact | Archive |

---

## 6. Active Scripts (used at runtime)

| Script | Purpose | Status |
|--------|---------|--------|
| `start.sh` | Creates venv, installs deps, starts uvicorn | Active |
| `Dockerfile` | Builds minimal server image | Active |
| `docker-compose.yml` | Orchestrates container with volumes | Active |

---

## 7. Import Health Check

- **Circular dependencies:** None detected in baton_server/
- **Missing imports in Docker:** None — all baton_server/ imports are in requirements-server.txt
- **Missing imports for baton/:** None — all baton/ imports are in requirements.txt
- **External hardcoded URLs:** `http://192.168.1.19:11434` in archived prototypes only
