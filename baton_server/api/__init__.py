import os
import time
import aiosqlite
from datetime import datetime
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def get_status():
    from baton_server.main import START_TIME
    from baton_server.websocket.manager import manager
    from baton_server.services.session_memory import session_memory

    db_path = "baton_server/db/baton.db"
    db_exists = os.path.exists(db_path)
    ws_connections = len(manager.active_connections)
    session = session_memory.get_state()

    return {
        "status": "operational",
        "system": "Baton Neural Observatory",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "database": "connected" if db_exists else "missing",
        "websocket_connections": ws_connections,
        "session_mode": session.get("last_active_intent", "DEBUG"),
        "uptime_seconds": round(time.time() - START_TIME, 1),
    }


@router.get("/metrics")
async def get_metrics():
    db_path = "baton_server/db/baton.db"
    db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0

    session_dir = "baton_server/db/sessions"
    session_count = (
        len([f for f in os.listdir(session_dir) if f.endswith(".json")])
        if os.path.exists(session_dir)
        else 0
    )

    memory_path = "baton_memory"
    memory_size = 0
    if os.path.exists(memory_path):
        for dirpath, dirnames, filenames in os.walk(memory_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                memory_size += os.path.getsize(fp)

    trace_count = 0
    if os.path.exists(db_path):
        try:
            async with aiosqlite.connect(db_path) as db:
                async with db.execute("SELECT COUNT(*) FROM traces") as cursor:
                    row = await cursor.fetchone()
                    trace_count = row[0]
        except Exception:
            pass

    import sys

    return {
        "database_size_bytes": db_size,
        "session_count": session_count,
        "memory_size_bytes": memory_size,
        "trace_count": trace_count,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    }
