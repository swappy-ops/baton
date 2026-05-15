# ARCHITECTURE_MAP.md - Spatial System Topology

## Cognition & Observation Flow
```mermaid
graph TD
    User([User Intent]) --> ControlSurface[Neural Observatory UI]
    ControlSurface -- CMD+K / Intent --> API[FastAPI Server]
    API -- Event Bus --> Orchestrator[Event Orchestrator]
    
    subgraph Execution_Layer [LangGraph Orchestration]
        Router{Intent Router: phi4}
        Specialist[Specialist Nodes]
        Distillation[Distillation Node]
        Router --> Specialist --> Distillation
    end
    
    Orchestrator -- Trigger --> Router
    
    subgraph Retrieval_Gating [Neural Observatory Core]
        Pipeline[Retrieval Pipeline]
        Quality[Quality Scorer]
        ChromaDB[(ChromaDB)]
        Pipeline <--> ChromaDB
        Pipeline --> Quality
    end
    
    Specialist <--> Pipeline
    Quality -- Telemetry --> API
    API -- WebSocket --> ControlSurface
    
    subgraph Persistence
        Memory[(Memory Persistence)]
        Traces[(SQLite Traces)]
        Distillation --> Memory
        API --> Traces
    end
```

## Component Boundaries
- **Control Surface**: `projskep_ui/` - React-based reactive dashboard.
- **Backend Hub**: `projskep_server/` - FastAPI, WebSocket manager, and event routing.
- **Orchestration**: `graphs/router_graph.py` & `scripts/event_orchestrator.py`.
- **Retrieval**: `retrieval/pipeline.py` - Vector index with quality scoring.
- **Memory**: `memory/manager.py` - Distillation of findings.
- **Observability**: `traces/` - Structured execution and audit logs.
