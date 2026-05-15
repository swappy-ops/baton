from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class TaskContract:
    task_type: str
    max_tokens: int = 1500
    retrieval_limit: int = 5
    allowed_tools: List[str] = field(default_factory=list)
    memory_scope: str = "runtime_only"
    model_name: str = "qwen2.5-coder:7b" # Default specialist

def get_contract_for_task(task_type: str) -> TaskContract:
    contracts = {
        "code": TaskContract(
            task_type="code",
            max_tokens=2000,
            retrieval_limit=10,
            allowed_tools=["read_file", "grep", "write_file"],
            model_name="qwen2.5-coder:7b"
        ),
        "ux": TaskContract(
            task_type="ux",
            max_tokens=1500,
            retrieval_limit=5,
            allowed_tools=["read_file"],
            model_name="phi4"
        ),
        "music": TaskContract(
            task_type="music",
            max_tokens=1000,
            retrieval_limit=8,
            allowed_tools=["read_file"],
            model_name="phi4" # Remapped from mistral-small for VRAM stability
        ),
        "router": TaskContract(
            task_type="router",
            max_tokens=500,
            retrieval_limit=0,
            model_name="phi4"
        )
    }
    return contracts.get(task_type, contracts["router"])
