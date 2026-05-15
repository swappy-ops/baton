import os
import json
from datetime import datetime
from typing import TypedDict, List, Dict, Any, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, AIMessage
from projskep.agents.nodes import intent_router_node, retrieval_node, specialist_node, distillation_node

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    task_type: str
    context: str
    contract: Dict[str, Any]
    suggestion: str # For HITL proposals
    approved: bool  # Whether the proposal was accepted
    trace_id: str   # Unique session trace

def trace_logger_node(state):
    """Logs the current state to a structured trace file."""
    trace_id = state.get("trace_id", "unknown")
    task_type = state.get("task_type", "general")
    
    # Organize by trace type
    trace_dir = f"traces/execution/{task_type}"
    os.makedirs(trace_dir, exist_ok=True)
    
    trace_file = os.path.join(trace_dir, f"{trace_id}.json")
    
    serializable_state = {
        "timestamp": datetime.now().isoformat(),
        "task_type": state["task_type"],
        "messages": [m.content for m in state["messages"]],
        "suggestion": state.get("suggestion", ""),
        "approved": state.get("approved", False)
    }
    
    with open(trace_file, "w") as f:
        json.dump(serializable_state, f, indent=2)
    
    print(f"--- TRACE LOGGED: {trace_file} ---")
    return state

def build_router_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("intent_router", intent_router_node)
    workflow.add_node("retrieval", retrieval_node)
    workflow.add_node("specialist", specialist_node)
    workflow.add_node("distillation", distillation_node)
    workflow.add_node("trace_logger", trace_logger_node)

    workflow.set_entry_point("intent_router")
    workflow.add_edge("intent_router", "retrieval")
    workflow.add_edge("retrieval", "specialist")
    workflow.add_edge("specialist", "distillation")
    workflow.add_edge("distillation", "trace_logger")
    workflow.add_edge("trace_logger", END)

    return workflow.compile()

if __name__ == "__main__":
    graph = build_router_graph()
    print("ProjSkep Orchestration Graph: COMPILED")
    
    # Test run
    from langchain_core.messages import HumanMessage
    import uuid
    
    test_state = {
        "messages": [HumanMessage(content="Audit the recent changes in the retrieval pipeline.")],
        "task_type": "code",
        "context": "",
        "contract": {},
        "suggestion": "",
        "approved": False,
        "trace_id": str(uuid.uuid4())
    }
    
    print("Executing diagnostic test...")
    for output in graph.stream(test_state):
        for key, value in output.items():
            print(f"Finished node: {key}")
