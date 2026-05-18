import pytest
from baton_server.services.attention_engine import attention_engine


def test_process_event_adds_attention_score():
    event = {
        "type": "test",
        "severity": "info"
    }
    result = attention_engine.process_event(event)
    assert "attention_score" in result
    assert result["attention_score"] == 0.5


def test_process_event_critical_severity():
    event = {
        "type": "test",
        "severity": "critical"
    }
    result = attention_engine.process_event(event)
    assert result["attention_score"] == 1.0
    assert result["is_pinned"] is True


def test_process_event_warning_severity():
    event = {
        "type": "test",
        "severity": "warning"
    }
    result = attention_engine.process_event(event)
    assert result["attention_score"] == 0.7
    assert result["is_pinned"] is False
