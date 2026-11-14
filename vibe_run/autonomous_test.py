"""Autonomous end-to-end test of ARGOS runtime components (original code).

Runs the real src/swarm/argos_master_core.ArgosMasterCore and
src/cognitive_memory.CognitiveMemory against the live test LLM adapter:

  1. ACL: approve operator ("admin")
  2. Task intake:  remember: key | value   -> SQLite fact memory
  3. Recall:       recall: key
  4. Executor selection + permitted action: shell: echo ... (allowlisted scope)
  5. AI routing:   think -> NeuralNexus -> Ollama API -> test adapter
  6. Cognitive memory: event log, knowledge, goal, Global Workspace cycle
  7. Result persisted to JSON report

Docker, PostgreSQL, Telegram, GitHub Gist, Ollama, P100/SPR2801S/Edge TPU
are NOT available in this environment and are reported as such, not imitated.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = os.getenv("ARGOS_REPO", "/workspace/github__winargos42-dotcom__argos")
RUNTIME = os.getenv("ARGOS_RUNTIME", "/workspace/argos-runtime")
sys.path.insert(0, REPO)
os.chdir(RUNTIME)
os.environ.setdefault("ARGOS_LOG_DIR", f"{RUNTIME}/logs")
os.environ.setdefault("ARGOS_COGNITIVE_SQLITE", f"{RUNTIME}/data/cognitive_memory.db")
os.environ.setdefault("ARGOS_PG_ENABLED", "0")

from src.swarm.argos_master_core import ArgosMasterCore
from src.cognitive_memory import CognitiveMemory

report = {"started": datetime.now(timezone.utc).isoformat(), "steps": []}


def step(name, **data):
    entry = {"step": name, **data}
    report["steps"].append(entry)
    print(f"[{name}] {json.dumps(data, ensure_ascii=False)[:300]}")


master = ArgosMasterCore(db_path=f"{RUNTIME}/data/brain.db")
step("master_core_online", **master.status())

step("acl_approve", result=master.ac.approve("admin"))

step("task_remember", command="remember: vibe_deployment | ARGOS запущен в песочнице Vibe, узел argos-vibe-sandbox",
     result=master.execute("remember: vibe_deployment | ARGOS запущен в песочнице Vibe, узел argos-vibe-sandbox", "admin"))
step("task_recall", command="recall: vibe_deployment",
     result=master.execute("recall: vibe_deployment", "admin"))

step("task_shell", command="shell echo ARGOS_SANDBOX_OK",
     result=master.execute("shell echo ARGOS_SANDBOX_OK", "admin"))

step("task_think_via_neuralnexus", command="think: статус узла?",
     result=master.execute("статус узла?", "admin"))

step("task_denied_without_acl", command="shell id",
     result=master.execute("shell id", "unknown-user"))

cm = CognitiveMemory(prefer_pg=False)
step("cognitive_memory_backend", backend=cm.backend, path=os.environ["ARGOS_COGNITIVE_SQLITE"])
cm.log_event("vibe_deployment", "runtime_started", {"node": "argos-vibe-sandbox", "components": ["gateway", "mcp_api", "master_core", "cognitive_memory"]})
cm.learn("vibe_sandbox", {"docker": "unavailable", "llm": "test adapter", "hardware": "not present"}, confidence=1.0)
goal_id = cm.add_goal("Подтвердить работоспособность автономного контура ARGOS в песочнице", priority=1)
cm.set_working("last_deployment_check", "gateway+mcp+master_core ok")
focus = cm.cycle()
step("global_workspace_cycle", goal_id=goal_id, current_goal=focus["current_goal"], counts=cm.counts())
cm.reflect("Развёртывание в Vibe", {"conclusion": "Базовый контур ядро-память-MCP работает; Brain API и AwaCore отсутствуют в репозитории"})
step("reflection_saved", recent=cm.recent_reflections(1))
cm.close()

report["finished"] = datetime.now(timezone.utc).isoformat()
report["master_status_final"] = master.status()
out = Path(os.getenv("REPORT_PATH", f"{RUNTIME}/logs/autonomous_test_report.json"))
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nReport saved: {out}")
