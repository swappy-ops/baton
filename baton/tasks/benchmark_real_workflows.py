import time
import json
import os
from baton.runtime.context_budget import get_context_budget_manager
from baton.runtime.stability import get_stability_manager

class BenchmarkSuite:
    def __init__(self, output_path="traces/validation/benchmark_report.json"):
        self.output_path = output_path
        self.budget_manager = get_context_budget_manager()
        self.stability_manager = get_stability_manager()
        self.results = []

    def run_benchmark(self, workflow_name, task_type):
        print(f"Benchmarking Workflow: {workflow_name}...")
        start_time = time.time()
        
        # Simulate budget lookup
        budget = self.budget_manager.get_budget(task_type, "phi4")
        
        # Simulate VRAM check
        vram = self.stability_manager.monitor_vram()
        
        end_time = time.time()
        latency = (end_time - start_time) * 1000 # ms
        
        result = {
            "workflow": workflow_name,
            "latency_ms": latency,
            "vram_usage": vram,
            "retrieval_limit": budget["retrieval_limit"],
            "max_tokens": budget["max_tokens"],
            "timestamp": time.time()
        }
        self.results.append(result)
        return result

    def save_report(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, "w") as f:
            json.dump(self.results, f, indent=4)
        print(f"Benchmark report saved to {self.output_path}")

if __name__ == "__main__":
    suite = BenchmarkSuite()
    suite.run_benchmark("repo_analysis", "architecture")
    suite.run_benchmark("assisted_debugging", "debug")
    suite.run_benchmark("refactoring", "code")
    suite.save_report()
