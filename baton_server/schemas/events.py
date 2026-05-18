from pydantic import BaseModel
from typing import Any, Optional, Literal
from datetime import datetime
import uuid

Severity = Literal["info", "warning", "critical"]


class SystemEvent(BaseModel):
    id: str = str(uuid.uuid4())
    type: str
    timestamp: float = datetime.now().timestamp()
    source: str
    severity: Severity = "info"
    payload: Any


class TracePayload(BaseModel):
    category: Literal["EXECUTION", "RETRIEVAL", "AUDITS", "DRIFT", "FAILURES"]
    message: str
    traceId: str


class WorkflowPayload(BaseModel):
    workflowId: str
    name: str
    status: Literal["IDLE", "RUNNING", "COMPLETED", "FAILED"]
    progress: float
    step: Optional[str] = None


class MetricPayload(BaseModel):
    promptOverhead: float
    memoryInjection: float
    retrievalDuplication: float
    agentChatter: float
    semanticRedundancy: float
