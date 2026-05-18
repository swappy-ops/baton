import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

SESSION_DIR = "baton_server/db/sessions"


class SessionMemory:
    def __init__(self):
        self.current_session_id = None
        self.state = {
            "last_active_intent": "DEBUG",
            "active_investigation": None,
            "unresolved_workflows": [],
            "current_architecture_focus": None,
            "recent_topology_changes": [],
        }
        self._load_latest_session()

    def _load_latest_session(self):
        if not os.path.exists(SESSION_DIR):
            os.makedirs(SESSION_DIR)

        sessions = sorted(
            [f for f in os.listdir(SESSION_DIR) if f.endswith(".json")], reverse=True
        )
        if sessions:
            with open(os.path.join(SESSION_DIR, sessions[0]), "r") as f:
                self.state.update(json.load(f))
                print(f"✅ Session Restored: {sessions[0]}")

    def save_state(self, updates: Dict[str, Any]):
        self.state.update(updates)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"session_{timestamp}.json"

        with open(os.path.join(SESSION_DIR, filename), "w") as f:
            json.dump(self.state, f, indent=4)

        # Cleanup old sessions (keep last 5)
        sessions = sorted(
            [f for f in os.listdir(SESSION_DIR) if f.endswith(".json")], reverse=True
        )
        for old in sessions[5:]:
            os.remove(os.path.join(SESSION_DIR, old))

    def get_state(self) -> Dict[str, Any]:
        return self.state


session_memory = SessionMemory()
