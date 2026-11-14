"""Goal-driven autonomous agent loop for ARGOS-VIBE (original modules only).

Cycle per iteration:
  1. CognitiveMemory.list_goals() -> pick the highest-priority active goal
  2. Route the goal through ArgosMasterCore.execute() (ACL-gated):
     shell:* / remember:* / recall:* run as-is, anything else goes to
     NeuralNexus -> Ollama API -> local Qwen2.5-0.5B (llama.cpp, :11434)
  3. Persist the outcome: CognitiveMemory.log_event + learn + reflect
  4. Mark the goal done (set_goal_state) and record the next queued goal

Only original ARGOS code performs routing, ACL and memory. External services
(Telegram, GitHub Gist, PostgreSQL) are absent and reported as such by the
original code itself; no component is imitated.
"""
from __future__ import annotations

import os
import sys
import time
from datetime import datetime, timezone

REPO = os.getenv("ARGOS_REPO", "/workspace/github__winargos42-dotcom__argos")
RUNTIME = os.getenv("ARGOS_RUNTIME", "/workspace/argos-runtime")
sys.path.insert(0, REPO)
os.chdir(RUNTIME)
os.environ.setdefault("ARGOS_LOG_DIR", f"{RUNTIME}/logs")
os.environ.setdefault("ARGOS_COGNITIVE_SQLITE", f"{RUNTIME}/data/cognitive_memory.db")
os.environ.setdefault("ARGOS_PG_ENABLED", "0")

from src.swarm.argos_master_core import ArgosMasterCore  # noqa: E402
from src.cognitive_memory import CognitiveMemory  # noqa: E402

INTERVAL = float(os.getenv("ARGOS_LOOP_INTERVAL", "20"))
MAX_ITERS = int(os.getenv("ARGOS_LOOP_MAX", "0"))  # 0 = until no active goals
OPERATOR = os.getenv("ARGOS_OPERATOR", "admin")

SHELL_PREFIXES = ("shell ", "remember:", "recall:", "ghost ", "flash ")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def route(master: ArgosMasterCore, goal_text: str) -> tuple[str, str]:
    text = goal_text.strip()
    low = text.lower()
    if low.startswith(SHELL_PREFIXES):
        return "direct", master.execute(text, user_id=OPERATOR)
    return "think", master.execute(f"think: {text}", user_id=OPERATOR)


def main() -> int:
    master = ArgosMasterCore(db_path=f"{RUNTIME}/data/brain.db")
    cm = CognitiveMemory(prefer_pg=False)
    master.ac.approve(OPERATOR)
    cm.log_event("agent_loop", "start", {"node": master.node_id, "at": now()})
    print(f"[agent_loop] node={master.node_id} operator={OPERATOR} interval={INTERVAL}s")

    iterations = 0
    try:
        while True:
            goals = cm.list_goals(state="active")
            if not goals:
                print("[agent_loop] no active goals — idling")
                if MAX_ITERS or os.getenv("ARGOS_LOOP_IDLE_EXIT") == "1":
                    break
                time.sleep(INTERVAL)
                continue

            goal = sorted(goals, key=lambda g: g.get("priority", 5))[0]
            goal_id = goal.get("id")
            goal_text = goal.get("goal", "")
            cm.set_working("current_goal", goal_text)
            print(f"[agent_loop] goal #{goal_id}: {goal_text}")

            mode, result = route(master, goal_text)
            print(f"[agent_loop] mode={mode} result={result[:300]}")

            cm.log_event("agent_loop", "goal_executed", {"goal_id": goal_id,
                                        "mode": mode, "result": result[:2000], "at": now()})
            cm.learn(f"goal:{goal_id}", {"goal": goal_text, "mode": mode,
                                         "result": result[:2000], "at": now()})
            cm.reflect(f"Цель #{goal_id} выполнена узлом {master.node_id}",
                       {"goal": goal_text, "mode": mode, "result": result[:500]})
            cm.set_goal_state(goal_id, "done")
            iterations += 1
            if MAX_ITERS and iterations >= MAX_ITERS:
                print(f"[agent_loop] reached MAX_ITERS={MAX_ITERS}")
                break
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("[agent_loop] interrupted")
    finally:
        cm.log_event("agent_loop", "stop", {"iterations": iterations, "at": now()})
        cm.close()
        print(f"[agent_loop] finished after {iterations} iteration(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
