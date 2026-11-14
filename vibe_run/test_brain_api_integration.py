"""Tests against the original ARGOS Brain Flask API; no mocked endpoints.

Run against a copy of the original files in an isolated environment:
    python -m pytest vibe_run/test_brain_api_integration.py -v

If argos_ai_brain is absent, these tests report SKIP rather than success.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
os.environ.setdefault("ARGOS_LOG_DIR", "/tmp/argos-brain-test-logs")

pytest.importorskip(
    "argos_ai_brain",
    reason="Original argos_ai_brain.py not yet restored from X230 recovery",
)


@pytest.fixture(scope="module")
def brain_client():
    import argos_brain_api as api
    from argos_ai_brain import ARGOSBrain, AgentRole

    api.brain = ARGOSBrain(node_id="vibe-integration-test")
    api.brain.create_agent("Главный координатор", AgentRole.MASTER)
    api.brain.create_agent("Аналитик", AgentRole.ANALYST)
    api.app.config["TESTING"] = True
    with api.app.test_client() as client:
        yield client


def test_health(brain_client):
    response = brain_client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("status") in ("ok", "healthy", "online") or data.get("ok") is True


def test_brain_status(brain_client):
    response = brain_client.get("/brain/status")
    assert response.status_code == 200
    assert response.get_json()["node_id"] == "vibe-integration-test"


def test_list_agents(brain_client):
    response = brain_client.get("/agents")
    assert response.status_code == 200
    body = response.get_json()
    assert body["count"] >= 2
    assert len(body["agents"]) == body["count"]


def test_create_agent_roundtrip(brain_client):
    response = brain_client.post("/agents", json={"name": "Vibe Испытатель", "role": "executor"})
    assert response.status_code in (200, 201), response.get_data(as_text=True)
    body = response.get_json()
    # Actual API returns {"success": true, "agent": {"id": "...", ...}}
    agent_id = body["agent"]["id"]
    assert agent_id
    fetched = brain_client.get(f"/agents/{agent_id}")
    assert fetched.status_code == 200
    assert fetched.get_json()["id"] == agent_id


def test_create_agent_invalid_role(brain_client):
    response = brain_client.post("/agents", json={"name": "X", "role": "no-such-role"})
    assert response.status_code == 400
    assert "available_roles" in response.get_json()


def test_system_status(brain_client):
    assert brain_client.get("/system/status").status_code == 200


def test_p2p_status(brain_client):
    assert brain_client.get("/p2p/status").status_code == 200
