import pytest
import os
import tempfile
import json
from fastapi.testclient import TestClient
from unittest.mock import patch
from baton_server.main import app


@pytest.fixture
def client():
    # Use temp directory for sessions during tests
    with tempfile.TemporaryDirectory() as tmpdir:
        session_dir = os.path.join(tmpdir, "sessions")
        os.makedirs(session_dir)
        with patch("baton_server.services.session_memory.SESSION_DIR", session_dir):
            yield TestClient(app)


def test_status_endpoint(client):
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "system" in data


def test_root_serves_ui(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "BATON" in response.text
    assert "Neural Observatory" in response.text


def test_session_endpoint(client):
    response = client.get("/api/session")
    assert response.status_code == 200
    data = response.json()
    assert "last_active_intent" in data


def test_intent_endpoint(client):
    response = client.post("/api/intent", json={
        "intent": "test intent",
        "mode": "DEBUG"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_friction_endpoint(client):
    response = client.post("/api/friction", json={
        "category": "test",
        "message": "test friction"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "logged"
