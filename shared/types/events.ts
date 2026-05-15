export type Severity = "info" | "warning" | "critical";

export interface SystemEvent {
  id: string;
  type: string;
  timestamp: number;
  source: string;
  severity: Severity;
  payload: any;
}

export interface TraceEvent extends SystemEvent {
  type: "trace:new";
  payload: {
    category: 'EXECUTION' | 'RETRIEVAL' | 'AUDITS' | 'DRIFT' | 'FAILURES';
    message: string;
    traceId: string;
  };
}

export interface WorkflowEvent extends SystemEvent {
  type: "workflow:update";
  payload: {
    workflowId: string;
    name: string;
    status: 'IDLE' | 'RUNNING' | 'COMPLETED' | 'FAILED';
    progress: number;
    step?: string;
  };
}

export interface MetricEvent extends SystemEvent {
  type: "metric:update";
  payload: {
    promptOverhead: number;
    memoryInjection: number;
    retrievalDuplication: number;
    agentChatter: number;
    semanticRedundancy: number;
  };
}
