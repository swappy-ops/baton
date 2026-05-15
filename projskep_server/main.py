from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import asyncio

from projskep_server.websocket.manager import manager
from projskep_server.api import router as api_router
from projskep_server.orchestration.engine import engine
from projskep_server.services.session_memory import session_memory
from projskep_server.db.manager import log_trace, init_db

app = FastAPI(title="ProjSkep Neural Observatory API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()
    await engine.start_mock_streams()
    print("ProjSkep Neural Observatory: ONLINE")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        pass
    finally:
        manager.disconnect(websocket)

@app.get("/api/session")
async def get_session():
    return session_memory.get_state()

@app.post("/api/intent")
async def update_intent(intent: dict):
    session_memory.save_state({"last_active_intent": intent.get("mode", "DEBUG")})
    return {"status": "success"}

@app.post("/api/friction")
async def report_friction(data: dict):
    timestamp = datetime.now().isoformat()
    log_entry = f"| {timestamp} | {data.get('category')} | {data.get('message')} | High | [New] |\n"
    
    with open("docs/FRICTION_LOG.md", "a") as f:
        f.write(log_entry)
    
    await log_trace("FRICTION", f"User reported friction: {data.get('message')}", data)
    return {"status": "logged"}

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
