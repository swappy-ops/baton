import time
import os
import sys
import uuid
from threading import Timer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from projskep.graphs.router_graph import build_router_graph
from langchain_core.messages import HumanMessage

class ProjSkepEventHandler(FileSystemEventHandler):
    def __init__(self, debounce_seconds=5.0):
        self.debounce_seconds = debounce_seconds
        self.timer = None
        self.pending_files = set()
        self.graph = build_router_graph()
        print(f"--- EVENT ORCHESTRATOR INITIALIZED ---")
        print(f"Monitoring: D:/ProjSkep")
        print(f"Debounce Window: {debounce_seconds}s")

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith((".py", ".md", ".json")):
            self.debounce_event(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith((".py", ".md", ".json")):
            self.debounce_event(event.src_path)

    def debounce_event(self, filepath):
        if self.timer:
            self.timer.cancel()
        
        self.pending_files.add(filepath)
        self.timer = Timer(self.debounce_seconds, self.process_events)
        self.timer.start()

    def process_events(self):
        print(f"\n--- DEBOUNCE COMPLETE: PROCESSING {len(self.pending_files)} FILES ---")
        
        # Batch events into a single orchestrated task
        files_list = list(self.pending_files)
        self.pending_files.clear()
        
        query = f"The following files were modified or created: {', '.join(files_list)}. Perform a continuity audit and identify any architectural deltas. Return suggestions for human approval."
        
        state = {
            "messages": [HumanMessage(content=query)],
            "task_type": "code",
            "context": "",
            "contract": {},
            "suggestion": "",
            "approved": False,
            "trace_id": f"event_{int(time.time())}"
        }
        
        try:
            print("Triggering LangGraph workflow...")
            for output in self.graph.stream(state):
                for key in output.keys():
                    print(f"Node '{key}' completed.")
            print("--- EVENT-DRIVEN ORCHESTRATION CYCLE COMPLETE ---")
        except Exception as e:
            print(f"ERROR in orchestration cycle: {e}")

if __name__ == "__main__":
    path = "D:/ProjSkep"
    if not os.path.exists(path):
        os.makedirs(path)
        
    event_handler = ProjSkepEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
