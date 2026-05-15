import asyncio
import json
import time
import os
from datetime import datetime
from projskep_server.websocket.manager import manager

class OrchestratorBridge:
    def __init__(self):
        self.running = False

    async def start(self):
        self.running = True
        print("Orchestrator Bridge Started")
        asyncio.create_task(self.watch_traces())
        asyncio.create_task(self.simulate_telemetry())

    async def watch_traces(self):
        """Watches the traces directory for new JSON files and broadcasts them."""
        trace_path = "traces/execution"
        os.makedirs(trace_path, exist_ok=True)
        
        last_seen = set()
        
        while self.running:
            try:
                for root, dirs, files in os.walk(trace_path):
                    for file in files:
                        if file.endswith(".json") and file not in last_seen:
                            filepath = os.path.join(root, file)
                            with open(filepath, "r") as f:
                                data = json.load(f)
                                await manager.broadcast_event("trace:new", {
                                    "timestamp": data.get("timestamp", datetime.now().isoformat()),
                                    "category": "EXECUTION",
                                    "message": f"Task {data.get('task_type')} completed with trace {file}"
                                })
                            last_seen.add(file)
            except Exception as e:
                print(f"Trace Watcher Error: {e}")
            await asyncio.sleep(2)

    async def simulate_telemetry(self):
        """Simulates periodic system metrics for the UI."""
        while self.running:
            await manager.broadcast_event("context:update", {
                "promptOverhead": 10 + (time.time() % 5),
                "memoryInjection": 40 + (time.time() % 10),
                "agentChatter": 12 + (time.time() % 4)
            })
            await asyncio.sleep(5)

bridge = OrchestratorBridge()
