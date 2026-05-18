import asyncio
import uuid
import time
from datetime import datetime
from baton_server.services.event_bus import event_bus
from baton_server.schemas.events import (
    SystemEvent,
    TracePayload,
    WorkflowPayload,
    MetricPayload,
)


class OrchestrationEngine:
    def __init__(self):
        self.active_workflows = {}

    async def run_workflow(self, name: str, category: str):
        workflow_id = str(uuid.uuid4())
        self.active_workflows[workflow_id] = {
            "name": name,
            "status": "RUNNING",
            "progress": 0,
        }

        # Start notification
        await event_bus.publish(
            SystemEvent(
                type="workflow:update",
                source="orchestrator",
                payload=WorkflowPayload(
                    workflowId=workflow_id,
                    name=name,
                    status="RUNNING",
                    progress=0,
                    step="Initializing",
                ).dict(),
            )
        )

        # Simulate execution steps
        steps = [
            "Context Retrieval",
            "Semantic Validation",
            "Drift Detection",
            "Proposal Generation",
        ]
        for i, step in enumerate(steps):
            await asyncio.sleep(2)
            progress = (i + 1) / len(steps) * 100

            await event_bus.publish(
                SystemEvent(
                    type="workflow:update",
                    source="orchestrator",
                    payload=WorkflowPayload(
                        workflowId=workflow_id,
                        name=name,
                        status="RUNNING",
                        progress=progress,
                        step=step,
                    ).dict(),
                )
            )

            await event_bus.publish(
                SystemEvent(
                    type="trace:new",
                    source="orchestrator",
                    severity="info",
                    payload=TracePayload(
                        category=category,
                        message=f"Step '{step}' completed for workflow {name}",
                        traceId=workflow_id,
                    ).dict(),
                )
            )

        # Finalize
        await event_bus.publish(
            SystemEvent(
                type="workflow:update",
                source="orchestrator",
                payload=WorkflowPayload(
                    workflowId=workflow_id,
                    name=name,
                    status="COMPLETED",
                    progress=100,
                    step="Finished",
                ).dict(),
            )
        )
        del self.active_workflows[workflow_id]

    async def start_mock_streams(self):
        """Generates continuous mock telemetry for the UI."""
        asyncio.create_task(self._metric_stream())
        asyncio.create_task(self._background_tasks())

    async def _metric_stream(self):
        while True:
            await event_bus.publish(
                SystemEvent(
                    type="metric:update",
                    source="telemetry",
                    payload=MetricPayload(
                        promptOverhead=12 + (time.time() % 4),
                        memoryInjection=45 + (time.time() % 8),
                        retrievalDuplication=8 + (time.time() % 2),
                        agentChatter=15 + (time.time() % 5),
                        semanticRedundancy=22 + (time.time() % 3),
                    ).dict(),
                )
            )
            await asyncio.sleep(3)

    async def _background_tasks(self):
        workflow_types = [
            ("stability_audit", "AUDITS"),
            ("continuity_check", "AUDITS"),
            ("retrieval_query", "RETRIEVAL"),
            ("plugin_audit", "EXECUTION"),
        ]
        while True:
            await asyncio.sleep(15)
            import random

            name, cat = random.choice(workflow_types)
            asyncio.create_task(self.run_workflow(name, cat))


engine = OrchestrationEngine()
