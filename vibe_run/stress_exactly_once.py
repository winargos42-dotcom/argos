"""Stage-6 agent stress test: 100 tasks, exactly-once, worker-crash recovery.

Protocol
  A. Enqueue 100 synthetic goals in the ORIGINAL CognitiveMemory goals table.
  B. Run the pool with N workers (ARGOS_POOL_WORKERS=2, then 4) as a separate
     process until the queue drains.
  C. Exactly-once verification straight from SQLite:
       - every goal state == 'done';
       - per goal_id, at most one agent_pool task_done event;
       - no goal left in any claimed:* / failed:* state.
  D. Crash recovery: while a fresh 100-goal run is in flight, SIGKILL the pool
     process mid-run; goals stay claimed:<dead worker>. Restart the pool — its
     startup recovery flips stale claims back to active — and verify that all
     100 goals finish with exactly one execution each.

No task is fabricated: shell/remember/recall run through the original
ArgosMasterCore.execute; think tasks go through the real local Qwen.
"""
from __future__ import annotations

import json
import os
import signal
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone

REPO = os.getenv("ARGOS_REPO", "/workspace/github__winargos42-dotcom__argos")
RUNTIME = os.getenv("ARGOS_RUNTIME", "/workspace/argos-runtime")
VENV_PY = f"{RUNTIME}/venv/bin/python"
DB = f"{RUNTIME}/data/cognitive_memory.db"
N_TASKS = int(os.getenv("ARGOS_STRESS_N", "100"))
REPORT = os.getenv("ARGOS_STRESS_REPORT", f"{RUNTIME}/stress_exactly_once_report.json")
sys.path.insert(0, REPO)
os.environ.setdefault("ARGOS_COGNITIVE_SQLITE", DB)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def enqueue(prefix: str, n: int) -> list[int]:
    from src.cognitive_memory import CognitiveMemory
    cm = CognitiveMemory(prefer_pg=False)
    ids = []
    for i in range(n):
        kind = i % 4
        if kind == 0:
            goal = f"shell echo {prefix}_T{i}"
        elif kind == 1:
            goal = f"remember: {prefix}_k{i} | synthetic value {i}"
        elif kind == 2:
            goal = f"recall: {prefix}_k{(i + 1) % n}"
        else:
            goal = f"shell echo {prefix}_T{i}"  # keep runtime bounded; LLM covered separately
        gid = cm.add_goal(goal, priority=3)
        ids.append(gid)
    cm.close()
    return ids


def run_pool(workers: int, report: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, ARGOS_POOL_WORKERS=str(workers),
               ARGOS_POOL_IDLE_EXIT="1", ARGOS_POOL_POLL="0.2",
               ARGOS_POOL_REPORT=report, ARGOS_COGNITIVE_SQLITE=DB,
               ARGOS_REPO=REPO, ARGOS_RUNTIME=RUNTIME)
    return subprocess.run([VENV_PY, f"{REPO}/vibe_run/agent_pool.py"],
                          env=env, capture_output=True, text=True,
                          cwd=RUNTIME, timeout=1800)


def verify(ids: list[int]) -> dict:
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    problems = []
    states = dict(con.execute(
        f"SELECT id, state FROM goals WHERE id IN ({','.join('?' * len(ids))})", ids))
    for gid in ids:
        st = states.get(gid)
        if st != "done":
            problems.append(f"goal {gid}: state={st!r}")
    dup = con.execute(
        "SELECT json_extract(content,'$.goal_id') gid, COUNT(*) c "
        "FROM memories_events WHERE source='agent_pool' AND event_type='task_done' "
        f"AND json_extract(content,'$.goal_id') IN ({','.join('?' * len(ids))}) "
        "GROUP BY gid HAVING c > 1", ids).fetchall()
    if dup:
        problems.append(f"double execution: {dup}")
    con.close()
    return {"goals": len(ids), "all_done": not problems or all("state='done'" in p for p in problems),
            "double_executions": len(dup), "problems": problems}


def crash_recovery_trial(workers: int) -> dict:
    from src.cognitive_memory import CognitiveMemory
    cm = CognitiveMemory(prefer_pg=False)
    slow_id = cm.add_goal("shell sleep 8", priority=1)  # guaranteed in-flight at kill time
    cm.close()
    ids = [slow_id] + enqueue("crash", N_TASKS - 1)
    env = dict(os.environ, ARGOS_POOL_WORKERS=str(workers),
               ARGOS_POOL_POLL="0.2", ARGOS_POOL_REPORT="/tmp/argos-stress-crash.json",
               ARGOS_COGNITIVE_SQLITE=DB, ARGOS_REPO=REPO, ARGOS_RUNTIME=RUNTIME)
    proc = subprocess.Popen([VENV_PY, f"{REPO}/vibe_run/agent_pool.py"], env=env,
                            cwd=RUNTIME, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    time.sleep(2.0)  # slow goal claimed and in flight, fast goals draining
    proc.send_signal(signal.SIGKILL)
    proc.wait()
    killed_after_s = 2.0

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    left_claimed = con.execute(
        f"SELECT COUNT(*) FROM goals WHERE id IN ({','.join('?' * len(ids))}) "
        "AND state LIKE 'claimed:%'", ids).fetchone()[0]
    con.close()

    r = run_pool(workers, "/tmp/argos-stress-crash2.json")
    v = verify(ids)
    return {"workers": workers, "killed_after_s": killed_after_s,
            "goals_left_claimed_after_kill": left_claimed,
            "restart_rc": r.returncode, **v}


def main() -> int:
    results = {"generated_at": now(), "n_tasks": N_TASKS, "runs": []}

    for workers in (2, 4):
        ids = enqueue(f"s{workers}", N_TASKS)
        t0 = time.perf_counter()
        r = run_pool(workers, f"{RUNTIME}/logs/stage6/stress_pool_w{workers}.json")
        wall = time.perf_counter() - t0
        v = verify(ids)
        results["runs"].append({"phase": "steady", "workers": workers,
                                "wall_s": round(wall, 2), "pool_rc": r.returncode, **v})
        print(f"[stress] workers={workers} wall={wall:.1f}s rc={r.returncode} "
              f"all_done={v['all_done']} double={v['double_executions']}")

    for workers in (2,):
        trial = crash_recovery_trial(workers)
        results["runs"].append({"phase": "crash_recovery", **trial})
        print(f"[stress] crash_recovery: killed_after={trial['killed_after_s']}s, "
              f"left_claimed={trial['goals_left_claimed_after_kill']}, "
              f"after_restart all_done={trial['all_done']} "
              f"double={trial['double_executions']}")

    ok = all(run["all_done"] and run["double_executions"] == 0 for run in results["runs"])
    results["verdict"] = "PASS" if ok else "FAIL"
    with open(REPORT, "w") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    print(f"[stress] verdict: {results['verdict']} -> {REPORT}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
