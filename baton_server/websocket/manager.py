import json
import asyncio
from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self._ping_interval = 20
        self._ping_timeout = 60

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_event(self, event_type: str, data: dict):
        payload = json.dumps({
            "type": event_type,
            "data": data
        })
        await self.broadcast(payload)

    async def keepalive(self, websocket: WebSocket):
        """Send pings every 20s, close if no pong within 60s."""
        try:
            while True:
                await asyncio.sleep(self._ping_interval)
                try:
                    await websocket.send_bytes(b"ping")
                except Exception:
                    break
        except asyncio.CancelledError:
            pass
        except Exception:
            pass

# Global manager instance for services to use
manager = ConnectionManager()
