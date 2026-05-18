from langchain_core.messages import HumanMessage, AIMessage
from baton.agents.nodes import get_model
from baton.memory.manager import get_memory_manager
from baton.runtime.dos_sync import get_dos_sync_engine

class DistillationNode:
    def __init__(self, model_name="phi4"):
        self.model_name = model_name
        self.manager = get_memory_manager()
        self.sync_engine = get_dos_sync_engine()

    def process(self, state):
        print("--- DISTILLATION NODE: COMPRESSING COGNITION ---")
        task_type = state.get("task_type", "general")
        messages = state.get("messages", [])
        context = state.get("context", "")
        
        # 1. Compress history
        history_text = "\n".join([f"{m.type}: {m.content}" for m in messages])
        
        prompt = f"""Extract high-density architectural insights and decisions from the following execution history.
        
Canonical Terminology to preserve: Neural Observatory, Spectral Fingerprint, Bridge, Forensic Industrial.

History:
{history_text}

Task Type: {task_type}
Context Used: {context}

Output format:
SUMMARY: <2-3 sentence high-density summary>
DECISIONS:
- <decision 1>
- <decision 2>
PATTERNS:
- <pattern 1>
"""
        model = get_model(self.model_name)
        response = model.invoke([HumanMessage(content=prompt)])
        distilled_text = response.content
        
        # 2. Extract components
        summary = ""
        decisions = []
        if "SUMMARY:" in distilled_text:
            parts = distilled_text.split("DECISIONS:")
            summary = parts[0].replace("SUMMARY:", "").strip()
            if len(parts) > 1:
                decision_block = parts[1].split("PATTERNS:")[0]
                decisions = [d.strip("- ") for d in decision_block.strip().split("\n") if d.strip()]

        # 3. Save to MemoryManager (which handles normalization and indexing)
        metadata = {
            "specialist": state.get("task_type", "unknown"),
            "sources": [state.get("task_id", "session_0")],
            "tags": ["distillation", task_type]
        }
        
        artifact_path = self.manager.save_distilled_memory(task_type, summary, decisions, metadata)
        
        # 4. Return summary to state
        return {
            "distilled_summary": summary,
            "artifact_path": artifact_path
        }

def distillation_node(state):
    node = DistillationNode()
    return node.process(state)
