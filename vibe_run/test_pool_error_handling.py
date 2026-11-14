"""Tests for agent_pool error handling: a failing execute() must never be
reported as a successful task (defect found in stage 8 probing).

These tests use a fake master object — no LLM, no network, no original-code
modification.
"""
from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("ARGOS_COGNITIVE_SQLITE", "/tmp/argos-test-pool.db")
os.environ.setdefault("ARGOS_PG_ENABLED", "0")

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "vibe_run"))
import agent_pool  # noqa: E402


class FakeACL:
    def approve(self, user: str) -> None:
        pass


class RaisingMaster:
    """Master whose execute() always fails (e.g. LLM transport down)."""

    class ac(FakeACL):
        pass

    node_id = "fake-node"

    def execute(self, cmd: str, user_id: str = "admin") -> str:
        raise ConnectionError("Ollama transport unreachable")


class WorkingMaster(RaisingMaster):
    def execute(self, cmd: str, user_id: str = "admin") -> str:
        return "ok-result"


def test_run_task_captures_exception():
    out: dict = {}
    agent_pool.run_task(RaisingMaster(), "analyze: anything", out)
    assert out["mode"] == "error"
    assert "ConnectionError" in out["result"]
    assert "Ollama transport unreachable" in out["result"]


def test_run_task_success_path():
    out: dict = {}
    agent_pool.run_task(WorkingMaster(), "analyze: anything", out)
    assert out["mode"] == "think"
    assert out["result"] == "ok-result"


def test_error_is_not_reported_as_ok():
    out: dict = {}
    agent_pool.run_task(RaisingMaster(), "shell echo hi", out)
    assert out["mode"] != "direct"
    assert out["mode"] == "error"
