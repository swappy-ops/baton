import os
import json
from datetime import datetime
from projskep.retrieval.pipeline import get_retrieval_pipeline
from projskep.runtime.dos_sync import get_dos_sync_engine

class MemoryManager:
    def __init__(self, distilled_path="./memory/distilled", traces_path="./traces/runtime"):
        self.distilled_path = distilled_path
        self.traces_path = traces_path
        os.makedirs(distilled_path, exist_ok=True)
        os.makedirs(traces_path, exist_ok=True)
        self.sync_engine = get_dos_sync_engine()
        self.pipeline = get_retrieval_pipeline()

    def save_distilled_memory(self, task_type: str, summary: str, decisions: list, metadata: dict = None):
        """Phase 5: Store distilled artifacts in retrieval-optimized markdown."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{task_type}_{timestamp}.md"
        filepath = os.path.join(self.distilled_path, filename)
        
        # Normalize terminology before saving
        normalized_summary = self.sync_engine.normalize_terminology(summary)
        
        # Construct markdown artifact
        content = f"""---
timestamp: {timestamp}
task_type: {task_type}
specialist: {metadata.get('specialist', 'unknown') if metadata else 'unknown'}
retrieval_sources: {metadata.get('sources', []) if metadata else []}
semantic_tags: {metadata.get('tags', []) if metadata else []}
---

# Distilled Memory: {task_type}

## Summary
{normalized_summary}

## Architectural Decisions
"""
        for d in decisions:
            content += f"- {d}\n"
            
        content += f"\n## Semantic References\n- DOS Terminology Verified: Yes\n"

        with open(filepath, "w") as f:
            f.write(content)
            
        # Phase 7: Auto-embed into Chroma (Neural Observatory)
        doc_id = f"distilled_{task_type}_{timestamp}"
        self.pipeline.add_documents(
            documents=[normalized_summary],
            metadatas=[{"type": "distilled_memory", "task": task_type, "timestamp": timestamp}],
            ids=[doc_id]
        )
        
        print(f"Memory distilled and indexed: {filepath}")
        return filepath

    def log_runtime_trace(self, trace_data: dict):
        """Phase 8: Forensic Observability."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.traces_path, f"trace_{timestamp}.json")
        with open(filepath, "w") as f:
            json.dump(trace_data, f, indent=4)

def get_memory_manager():
    return MemoryManager()
