#!/usr/bin/env python3
"""Bounded, proposal-only code generation; generated source is NEVER executed."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import time
import uuid
from urllib.request import Request, urlopen

BACKLOG = (
    "Write pure Python function classify_node_state(heartbeat: dict) -> str. Never infer remote node is healthy from a local interface. Return confirmed, running, error or unknown.",
    "Write pure Python function correlate_result(notice: dict, result: dict) -> bool. Validate matching message IDs, task IDs and SHA256 format without network access.",
    "Write pure Python function summarize_tasks(rows: list[dict]) -> dict. Count done, failed, timeout and unknown rows without mutation."
)
BLOCKED_CALLS = {"eval", "exec", "compile", "open", "__import__", "input", "breakpoint"}
BLOCKED_ATTRS = {"__globals__", "__builtins__", "__subclasses__", "__getattribute__", "__dict__"}
MODEL = os.getenv("ARGOS_AUTODEV_MODEL", "qwen2.5:0.5b")


def _ask_local_ollama(goal: str) -> str:
    prompt = (
        "Return a JSON object ONLY with property code containing exactly one small standalone pure Python function. "
        "No imports, globals, file/network I/O, shell, subprocess, code fences, or external dependencies. "
        "The code must be valid Python 3.11, under 850 characters.\nTASK: " + goal
    )
    req = Request("http://127.0.0.1:11434/api/generate",
                  data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                                   "format": "json", "options": {"temperature": 0.1, "num_predict": 650}}).encode(),
                  headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=50) as response:
        body = response.read(65537)
        if len(body) > 65536:
            raise ValueError("model response exceeds cap")
    return json.loads(body)["response"]


def validate_code(code: str) -> dict:
    if not isinstance(code, str) or not (30 <= len(code) <= 950) or "\x00" in code:
        raise ValueError("invalid candidate source")
    parsed = ast.parse(code, filename="candidate.py")
    if len(parsed.body) != 1 or not isinstance(parsed.body[0], ast.FunctionDef):
        raise ValueError("exactly one top-level synchronous function required")
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal)):
            raise ValueError("imports/global state prohibited")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in BLOCKED_CALLS:
            raise ValueError("blocked call")
        if isinstance(node, ast.Attribute) and node.attr in BLOCKED_ATTRS:
            raise ValueError("blocked introspection")
    return {"syntax": "pass", "static_policy": "pass", "function": parsed.body[0].name,
            "code_executed": False, "tests_executed": False, "behavior_verified": False}


def generate_proposal(goal: str, *, root: Path | None = None, generate=None) -> str:
    if not isinstance(goal, str) or not (20 <= len(goal) <= 480):
        raise ValueError("development request too short/long")
    answer = (generate or _ask_local_ollama)(goal)
    if not isinstance(answer, str) or len(answer) > 65536:
        raise ValueError("model response invalid")
    data = json.loads(answer)
    if not isinstance(data, dict) or set(data) != {"code"}:
        raise ValueError("model must return code JSON field")
    code = data["code"]
    report = validate_code(code)
    base = Path(root) if root else Path(os.getenv("ARGOS_RUNTIME", "/workspace/argos-runtime")) / "autodev/proposals"
    base.mkdir(parents=True, exist_ok=True, mode=0o700)
    proposal_id = str(uuid.uuid4())
    dest = base / proposal_id
    dest.mkdir(mode=0o700)
    digest = hashlib.sha256(code.encode()).hexdigest()
    metadata = {"id": proposal_id, "goal": goal,
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "sha256": digest, "model": MODEL, "report": report, "status": "NEEDS_REVIEW"}
    for name, content in (("candidate.py", code), ("report.json", json.dumps(metadata, ensure_ascii=False, indent=2))):
        fd = os.open(dest / name, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "w", encoding="utf8") as out:
            out.write(content)
    return json.dumps({"status": "NEEDS_REVIEW", "sha256": digest, "code": code,
                       "function": report["function"], "syntax": "pass",
                       "tests_executed": False, "behavior_verified": False}, ensure_ascii=False)


def schedule_one(cm, state: dict, *, at: float | None = None) -> dict:
    """At most one local code proposal per day; never deploy generated code."""
    if os.getenv("ARGOS_AUTODEV_ENABLED", "1") != "1":
        return {"queued": False, "reason": "disabled"}
    at = time.time() if at is None else at
    if at - float(state.get("autodev_last_attempt_epoch", 0)) < 86400:
        return {"queued": False, "reason": "cooldown"}
    cursor = int(state.get("autodev_backlog_cursor", 0))
    gid = cm.add_goal("develop: " + BACKLOG[cursor % len(BACKLOG)], priority=1)
    state["autodev_last_attempt_epoch"] = at
    state["autodev_backlog_cursor"] = cursor + 1
    cm.log_event("autodev", "proposal_queued", {"goal_id": gid, "backlog_index": cursor})
    return {"queued": True, "goal_id": gid, "backlog_index": cursor}
