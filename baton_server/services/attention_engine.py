import time
from typing import List, Dict, Any
from baton_server.schemas.events import SystemEvent


class AttentionEngine:
    def __init__(self):
        self.signal_scores = {}
        self.decay_rate = 0.1  # Per minute
        self.critical_threshold = 0.8
        self.noise_threshold = 0.2

    def score_event(self, event: SystemEvent) -> float:
        """Assigns a score to an event based on its severity and source."""
        base_score = 0.3
        if event.severity == "critical":
            base_score = 0.9
        elif event.severity == "warning":
            base_score = 0.6

        # Source-based weighting
        source_weights = {
            "vst3_stability_audit": 0.8,
            "continuity_validator": 0.7,
            "retrieval_pipeline": 0.4,
            "telemetry": 0.1,
        }

        weight = source_weights.get(event.source, 0.3)
        return min(1.0, base_score * weight * 2)

    def filter_events(self, events: List[SystemEvent]) -> List[SystemEvent]:
        """Filters out noise and batches low-priority signals."""
        high_priority = []
        for event in events:
            score = self.score_event(event)
            if score >= self.noise_threshold:
                high_priority.append(event)

        return high_priority

    def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Adds attention metadata to an event before broadcasting."""
        # Simple signal scoring logic
        score = 0.5
        if "severity" in event:
            if event["severity"] == "critical":
                score = 1.0
            if event["severity"] == "warning":
                score = 0.7

        event["attention_score"] = score
        event["is_pinned"] = score >= self.critical_threshold

        return event


attention_engine = AttentionEngine()
