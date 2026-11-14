"""Integration tests for the ORIGINAL argos_brain_api.py (no reimplementation).

These tests exercise the real Flask app from the repository root. They require
the original ``argos_ai_brain`` module to be present (recovered from the X230
path /home/argos-data/recovery/argos_ai_brain.py). Until that file is restored
into the repository or PYTHONPATH, the whole module is SKIPPED — never faked.

Run:  python -m pytest vibe_run/test_brain_api_integration.py -v
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
    reason="argos_ai_brain отсутствует в репозитории; восстановить оригинал с X230 "
           "(/home/argos-data/recovery/argos_ai_brain.py) — подмена запрещена",
)


@pytest.fixture(scope="module")
def brain_client():
    import argos_brain_api as api
    from argos_ai_brain import ARGOSBrain, AgentRole

    if api.brain is None:
        api.brain = ARGOSBrain(node_id="vibe-integration-test")
        api.brain.create_agent("Главный координатор", AgentRole.MASTER)
        api.brain.create_agent("Аналитик", AgentRole.ANALYST)
    api.app.config["TESTING"] = True
    with api.app.test_client() as client:
        yield client


def test_health(brain_client):
    r = brain_client.get("/health")
    assert r.status_code == 200
    body = r.get_json()
    assert body.get("status") in ("ok", "healthy", "online") or body.get("ok") is True


def test_brain_status(brain_client):
    r = brain_client.get("/brain/status")
    assert r.status_code == 200
    assert r.get_json() is not None


def test_list_agents(brain_client):
    r = brain_client.get("/agents")
    assert r.status_code == 200
    body = r.get_json()
    assert body["count"] >= 2
    assert len(body["agents"]) == body["count"]


def test_create_agent_roundtrip(brain_client):
    r = brain_client.post("/agents", json={"name": "Vibe Испытатель", "role": "executor"})
    assert r.status_code in (200, 201), r.get_data(as_text=True)
    created = r.get_json()
    agent = created.get("agent") or created
    agent_id = agent.get("agent_id") or agent.get("id")
    assert agent_id, f"нет id в ответе: {created}"
    r2 = brain_client.get(f"/agents/{agent_id}")
    assert r2.status_code == 200


def test_create_agent_invalid_role(brain_client):
    r = brain_client.post("/agents", json={"name": "X", "role": "no-such-role"})
    assert r.status_code == 400
    assert "available_roles" in r.get_json()


def test_system_status(brain_client):
    r = brain_client.get("/system/status")
    assert r.status_code == 200


def test_p2p_status(brain_client):
    r = brain_client.get("/p2p/status")
    assert r.status_code == 200
