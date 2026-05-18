from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import asyncio
import json
import os
import time

START_TIME = time.time()

from baton_server.websocket.manager import manager
from baton_server.api import router as api_router
from baton_server.orchestration.engine import engine
from baton_server.services.session_memory import session_memory
from baton_server.db.manager import log_trace, init_db

app = FastAPI(title="Baton Neural Observatory API")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

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
    print("Baton Neural Observatory: ONLINE")

@app.get("/")
async def root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    ping_task = asyncio.create_task(manager.keepalive(websocket))
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
                if msg.get("type") == "intent":
                    session_memory.save_state({"last_active_intent": msg.get("mode", "DEBUG")})
                    await manager.broadcast_event("intent:received", {
                        "content": msg.get("content", ""),
                        "mode": msg.get("mode", "DEBUG")
                    })
                    await log_trace("INTENT", msg.get("content", ""), msg)
            except json.JSONDecodeError:
                await manager.broadcast_event("raw", {"text": raw})
    except Exception:
        pass
    finally:
        ping_task.cancel()
        manager.disconnect(websocket)

@app.get("/api/session")
async def get_session():
    return session_memory.get_state()

@app.post("/api/intent")
async def update_intent(intent: dict):
    session_memory.save_state({"last_active_intent": intent.get("mode", "DEBUG")})
    await manager.broadcast_event("intent:received", {
        "content": intent.get("intent", ""),
        "mode": intent.get("mode", "DEBUG")
    })
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
