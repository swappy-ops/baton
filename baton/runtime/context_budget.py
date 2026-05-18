from baton.runtime.task_contract import TaskContract

class ContextBudgetManager:
    def __init__(self, vram_limit_gb=8.0):
        self.vram_limit_gb = vram_limit_gb
        
    def get_budget(self, task_type: str, active_model: str) -> dict:
        """
        Dynamically scale retrieval budget based on task complexity and model.
        Target: Maximize leverage per token.
        """
        # Base budgets
        budgets = {
            "code": {
                "max_tokens": 3000,
                "retrieval_limit": 12,
                "priority": "precision"
            },
            "architecture": {
                "max_tokens": 5000,
                "retrieval_limit": 20,
                "priority": "breadth"
            },
            "ux": {
                "max_tokens": 2000,
                "retrieval_limit": 5,
                "priority": "semantic"
            },
            "debug": {
                "max_tokens": 4000,
                "retrieval_limit": 15,
                "priority": "code-heavy"
            },
            "default": {
                "max_tokens": 1500,
                "retrieval_limit": 5,
                "priority": "speed"
            }
        }
        
        budget = budgets.get(task_type, budgets["default"])
        
        # Scaling logic for large models (VRAM awareness)
        if "7b" in active_model.lower():
            # Reduce retrieval limit to save context/kv-cache on 8GB VRAM
            budget["retrieval_limit"] = min(budget["retrieval_limit"], 10)
            budget["max_tokens"] = min(budget["max_tokens"], 3000)
            
        return budget

def get_context_budget_manager():
    return ContextBudgetManager()
