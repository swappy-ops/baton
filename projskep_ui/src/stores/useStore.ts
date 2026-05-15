import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type IntentMode = 'DEBUG' | 'RESEARCH' | 'BUILD' | 'DESIGN' | 'FORENSIC' | 'DEEP_WORK';

interface Trace {
  timestamp: string;
  category: 'EXECUTION' | 'RETRIEVAL' | 'AUDITS' | 'DRIFT' | 'FAILURES';
  message: string;
  attention_score?: number;
  is_pinned?: boolean;
}

interface Workflow {
  workflowId: string;
  name: string;
  status: 'IDLE' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  progress: number;
  step?: string;
}

interface FrictionRecord {
  timestamp: number;
  category: string;
  message: string;
}

interface ProjskepState {
  intent: {
    mode: IntentMode;
    depth: 'low' | 'high';
    retrievalWeight: number;
  };
  metrics: {
    promptOverhead: number;
    memoryInjection: number;
    retrievalDuplication: number;
    agentChatter: number;
    semanticRedundancy: number;
  };
  traces: Trace[];
  workflows: Workflow[];
  suggestions: any[];
  frictionLogs: FrictionRecord[];
  
  setIntent: (intent: Partial<ProjskepState['intent']>) => void;
  addTrace: (trace: Trace) => void;
  updateWorkflow: (workflow: Partial<Workflow> & { workflowId: string }) => void;
  addSuggestion: (suggestion: any) => void;
  reportFriction: (category: string, message: string) => void;
  setMetrics: (metrics: ProjskepState['metrics']) => void;
}

export const useStore = create<ProjskepState>()(
  persist(
    (set) => ({
      intent: {
        mode: 'DEBUG',
        depth: 'high',
        retrievalWeight: 0.8,
      },
      metrics: {
        promptOverhead: 0,
        memoryInjection: 0,
        retrievalDuplication: 0,
        agentChatter: 0,
        semanticRedundancy: 0,
      },
      traces: [],
      workflows: [],
      suggestions: [],
      frictionLogs: [],

      setIntent: (intent) => set((state) => ({ intent: { ...state.intent, ...intent } })),
      addTrace: (trace) => set((state) => ({ 
        traces: [trace, ...state.traces].slice(0, 100) 
      })),
      updateWorkflow: (wf) => set((state) => {
        const index = state.workflows.findIndex(w => w.workflowId === wf.workflowId);
        if (index === -1) return { workflows: [wf as Workflow, ...state.workflows] };
        const newWorkflows = [...state.workflows];
        newWorkflows[index] = { ...newWorkflows[index], ...wf };
        return { workflows: newWorkflows };
      }),
      addSuggestion: (s) => set((state) => ({ suggestions: [s, ...state.suggestions] })),
      reportFriction: (category, message) => set((state) => ({
        frictionLogs: [{ timestamp: Date.now(), category, message }, ...state.frictionLogs]
      })),
      setMetrics: (metrics) => set({ metrics }),
    }),
    { name: 'projskep-operational-state' }
  )
);
