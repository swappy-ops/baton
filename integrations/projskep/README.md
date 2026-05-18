# ProjSkep Integration
Baton uses ProjSkep as its semantic memory and neural observatory layer.
Baton orchestrates ProjSkep. Baton does NOT contain or duplicate ProjSkep.
## Connection
- ProjSkep server: http://localhost:8000 (or configured via PROJSKEP_URL env)
- WebSocket: ws://localhost:8000/ws
## What Baton delegates to ProjSkep
- Semantic retrieval
- Context continuity
- Real-time telemetry stream
