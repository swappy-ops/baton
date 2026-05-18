import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baton.graphs.router_graph import build_router_graph
from langchain_core.messages import HumanMessage

def run_architecture_review():
    graph = build_router_graph()
    query = "Perform an architecture review of the Baton bridge manager and threading model."
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "task_type": "code", # Forced specialist for testing
        "context": "BridgeManager isolates audio thread from UI thread using SafePointer.",
        "contract": {
            "task_type": "code",
            "model_name": "qwen2.5-coder:7b",
            "retrieval_limit": 5,
            "allowed_tools": ["read_file"]
        }
    }
    
    print("--- ARCHITECTURE REVIEW START ---")
    for event in graph.stream(initial_state):
        for node, data in event.items():
            print(f"Node: {node}")
            if "messages" in data:
                print(f"Response: {data['messages'][-1].content[:200]}...")

if __name__ == "__main__":
    run_architecture_review()
