import sys
import os
# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baton.graphs.router_graph import build_router_graph
from langchain_core.messages import HumanMessage

def run_repo_analysis(query: str):
    graph = build_router_graph()
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "task_type": "",
        "context": "",
        "contract": {}
    }
    
    print(f"Starting analysis for: {query}")
    for output in graph.stream(initial_state):
        # Stream outputs for observability
        for key, value in output.items():
            print(f"Node: {key} completed.")
    
    print("Workflow finished.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_repo_analysis(" ".join(sys.argv[1:]))
    else:
        run_repo_analysis("Analyze the current project structure and identify key components.")
