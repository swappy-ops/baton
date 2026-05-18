import pytest
from baton_server.schemas.events import SystemEvent, TracePayload, WorkflowPayload, MetricPayload


def test_system_event():
    event = SystemEvent(
        type="test",
        source="test_source",
        payload={"key": "value"}
    )
    assert event.type == "test"
    assert event.severity == "info"


def test_trace_payload():
    payload = TracePayload(
        category="EXECUTION",
        message="test trace",
        traceId="test-123"
    )
    assert payload.category == "EXECUTION"


def test_workflow_payload():
    payload = WorkflowPayload(
        workflowId="wf-1",
        name="test",
        status="RUNNING",
        progress=50.0,
        step="Testing"
    )
    assert payload.status == "RUNNING"


def test_metric_payload():
    payload = MetricPayload(
        promptOverhead=12.0,
        memoryInjection=45.0,
        retrievalDuplication=8.0,
        agentChatter=15.0,
        semanticRedundancy=22.0
    )
    assert payload.promptOverhead == 12.0
