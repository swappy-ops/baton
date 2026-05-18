from baton.agents.nodes import get_model
from langchain_core.messages import HumanMessage, AIMessage

class WorkflowEngine:
    def __init__(self):
        self.workflows = {
            "repo_analysis": "Perform a forensic analysis of the codebase topology. Identify core architectural patterns and bottlenecks.",
            "assisted_debugging": "Analyze the stack trace and relevant source files. Cross-reference with the Neural Observatory for prior similar failures.",
            "refactoring": "Propose a refactoring plan that preserves semantic continuity and adheres to the Forensic Industrial design system.",
            "ux_critique": "Critique the interface based on Baton's cinematic and instrument-like philosophy. Detect SaaS-style drift.",
            "plugin_memory": "Recall plugin-chain configurations and spectral processing parameters from the distillation archive.",
            "diagnostics": "Execute a runtime diagnostic pass. Verify bridge stability and thread-safety constraints.",
            "continuity_recall": "Retrieve architectural reasoning from prior sessions to ensure current edits align with the long-term vision.",
            "project_summary": "Generate a high-density executive summary of the project state using distilled semantic artifacts.",
            "dependency_tracing": "Map the semantic dependencies between components. Identify uncontrolled coupling.",
            "topology_exploration": "Explore the codebase structural map. Identify orphaned or high-complexity nodes."
        }

    def execute_workflow(self, workflow_name: str, state: dict):
        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")
            
        print(f"--- EXECUTING WORKFLOW: {workflow_name.upper()} ---")
        prompt = self.workflows[workflow_name]
        
        # Specialists are already budget-aware and retrieval-gated.
        # This engine simply sets the high-level intent.
        return {
            "task_type": "architecture" if "analysis" in workflow_name or "topology" in workflow_name else "code",
            "workflow_intent": prompt
        }

def get_workflow_engine():
    return WorkflowEngine()
