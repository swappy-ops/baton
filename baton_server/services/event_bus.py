import asyncio
from typing import Dict, List, Callable
from baton_server.services.attention_engine import attention_engine
from baton_server.schemas.events import SystemEvent
from baton_server.websocket.manager import manager


class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    async def publish(self, event: SystemEvent):
        # Process through Attention Engine
        processed_payload = attention_engine.process_event(event.dict())

        # Broadcast to WebSockets
        await manager.broadcast_event(event.type, processed_payload)

        # Internal callbacks
        if event.type in self.subscribers:
            for callback in self.subscribers[event.type]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)


event_bus = EventBus()
