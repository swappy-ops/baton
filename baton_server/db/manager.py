import os
import aiosqlite
from datetime import datetime

DB_PATH = "baton_server/db/baton.db"

async def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS traces (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                category TEXT,
                message TEXT,
                payload TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS suggestions (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                type TEXT,
                message TEXT,
                status TEXT DEFAULT 'PENDING'
            )
        """)
        await db.commit()

async def log_trace(category, message, payload=None):
    import uuid
    import json
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO traces (id, timestamp, category, message, payload) VALUES (?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), datetime.now().isoformat(), category, message, json.dumps(payload) if payload else None)
        )
        await db.commit()
