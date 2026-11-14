"""Parallel agent pool for ARGOS-VIBE (original modules only).

Dispatcher/worker model on top of ORIGINAL ArgosMasterCore + CognitiveMemory:

  * Goals live in the original CognitiveMemory `goals` table (add_goal /
    list_goals / set_goal_state are the original APIs).
  * N worker threads each own one ArgosMasterCore + one CognitiveMemory
    connection (SQLite-safe: one connection per thread).
  * Claiming: a worker flips goal state active -> claimed:<worker> via the
    original set_goal_state, then re-reads it; if another worker already
    claimed it, the goal is skipped (optimistic locking on the original schema).
  * Execution control: each task runs under a watchdog; on timeout the goal is
    marked failed:<worker> and the abandoned work is reported honestly (a
    Python thread cannot be killed, the timeout marks the result, it does not
    terminate the underlying call).
  * Every task records queue wait, execution time and outcome into the pool
    report (JSON) and into CognitiveMemory events/knowledge.

Routing is the original ArgosMasterCore.execute: shell:/remember:/recall: run
directly, everything else goes through NeuralNexus -> local Qwen2.5-0.5B.
"""
from __future__ import annotations

import json
import os
import sys
import threading
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

WORKERS = int(os.getenv("ARGOS_POOL_WORKERS", "3"))
TASK_TIMEOUT = float(os.getenv("ARGOS_POOL_TASK_TIMEOUT", "120"))
POLL = float(os.getenv("ARGOS_POOL_POLL", "1.0"))
OPERATOR = os.getenv("ARGOS_OPERATOR", "admin")
MAX_TASKS = int(os.getenv("ARGOS_POOL_MAX_TASKS", "0"))  # 0 = drain queue
REPORT = os.getenv("ARGOS_POOL_REPORT", f"{RUNTIME}/agent_pool_report.json")

SHELL_PREFIXES = ("shell ", "remember:", "recall:", "ghost ", "flash ")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class TaskResult:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.rows: list[dict] = []

    def add(self, row: dict) -> None:
        with self.lock:
            self.rows.append(row)


def route(master: ArgosMasterCore, goal_text: str) -> tuple[str, str]:
    low = goal_text.strip().lower()
    if low.startswith(SHELL_PREFIXES):
        return "direct", master.execute(goal_text.strip(), user_id=OPERATOR)
    return "think", master.execute(f"think: {goal_text.strip()}", user_id=OPERATOR)


def run_task(master: ArgosMasterCore, goal_text: str, out: dict) -> None:
    mode, result = route(master, goal_text)
    out["mode"] = mode
    out["result"] = result
    out["done_at"] = now()


def recover_stale_claims() -> int:
    """Re-activate goals left claimed by dead workers (crash recovery).

    A worker killed mid-task leaves its goal in state claimed:<worker> forever.
    On pool startup every claimed:* goal is returned to active so it runs
    exactly once under the new generation of workers.
    """
    import sqlite3
    con = sqlite3.connect(f"{RUNTIME}/data/cognitive_memory.db", timeout=10)
    try:
        cur = con.execute(
            "UPDATE goals SET state='active' WHERE state LIKE 'claimed:%'")
        con.commit()
        return cur.rowcount
    finally:
        con.close()


def claim(worker: str) -> dict | None:
    """Atomic claim on the ORIGINAL goals table (SQLite-level guard).

    The optimistic set_goal_state approach raced: two workers could each
    re-claim the same goal and execute it twice. This uses a single conditional
    UPDATE ... WHERE state='active' so exactly one worker wins. The table and
    states remain the original CognitiveMemory schema.
    """
    import sqlite3
    con = sqlite3.connect(f"{RUNTIME}/data/cognitive_memory.db", timeout=10)
    try:
        row = con.execute(
            "SELECT id, goal FROM goals WHERE state='active' "
            "ORDER BY priority ASC, id ASC LIMIT 1").fetchone()
        if row is None:
            return None
        gid, text = row
        cur = con.execute(
            "UPDATE goals SET state=? WHERE id=? AND state='active'",
            (f"claimed:{worker}", gid))
        con.commit()
        if cur.rowcount != 1:
            return None
        return {"id": gid, "goal": text}
    finally:
        con.close()


def worker_loop(name: str, stop: threading.Event, results: TaskResult) -> None:
    master = ArgosMasterCore(db_path=f"{RUNTIME}/data/brain.db")
    cm = CognitiveMemory(prefer_pg=False)
    master.ac.approve(OPERATOR)
    done = 0
    while not stop.is_set():
        if MAX_TASKS and done >= MAX_TASKS:
            break
        goal = claim(name)
        if goal is None:
            if os.getenv("ARGOS_POOL_IDLE_EXIT") == "1":
                break
            if stop.wait(POLL):
                break
            continue
        gid = goal.get("id")
        text = goal.get("goal", "")
        queued_at = goal.get("created_at") or goal.get("ts")
        row: dict = {"goal_id": gid, "worker": name, "goal": text[:200],
                     "started_at": now(), "queued_at": queued_at}
        out: dict = {}
        t0 = time.perf_counter()
        th = threading.Thread(target=run_task, args=(master, text, out), daemon=True)
        th.start()
        th.join(TASK_TIMEOUT)
        exec_s = time.perf_counter() - t0
        if th.is_alive():
            row.update({"status": "timeout", "exec_s": round(exec_s, 3),
                        "note": f"watchdog fired after {TASK_TIMEOUT}s; underlying call abandoned"})
            cm.set_goal_state(gid, f"failed:{name}")
            cm.log_event("agent_pool", "task_timeout",
                         {"goal_id": gid, "worker": name, "exec_s": exec_s})
        else:
            row.update({"status": "ok", "exec_s": round(exec_s, 3),
                        "mode": out.get("mode"), "result": str(out.get("result"))[:2000]})
            cm.set_goal_state(gid, "done")
            cm.log_event("agent_pool", "task_done",
                         {"goal_id": gid, "worker": name, "mode": out.get("mode"),
                          "exec_s": exec_s})
            cm.learn(f"task:{gid}", {"goal": text[:500], "mode": out.get("mode"),
                                     "exec_s": exec_s, "worker": name})
        cm.reflect(f"Задача #{gid} ({row['status']}) рабочим {name}",
                   {"goal": text[:200], "exec_s": row.get("exec_s")})
        results.add(row)
        done += 1
        print(f"[pool/{name}] #{gid} {row['status']} {row['exec_s']}s: "
              f"{str(row.get('result', ''))[:120]}")
    cm.log_event("agent_pool", "worker_stop", {"worker": name, "tasks": done})
    cm.close()


def main() -> int:
    stop = threading.Event()
    results = TaskResult()
    probe = CognitiveMemory(prefer_pg=False)
    recovered = recover_stale_claims()
    probe.log_event("agent_pool", "start", {"workers": WORKERS, "recovered": recovered,
                                            "at": now()})
    probe.close()
    print(f"[pool] starting {WORKERS} workers, timeout={TASK_TIMEOUT}s, "
          f"recovered_stale_claims={recovered}, report={REPORT}")

    threads = [threading.Thread(target=worker_loop, args=(f"w{i}", stop, results),
                                daemon=True)
               for i in range(WORKERS)]
    for t in threads:
        t.start()

    try:
        while any(t.is_alive() for t in threads):
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("[pool] interrupt — stopping workers")
        stop.set()
        for t in threads:
            t.join(timeout=5)

    rows = results.rows
    exec_times = sorted(r["exec_s"] for r in rows)
    summary = {
        "generated_at": now(),
        "workers": WORKERS,
        "tasks": len(rows),
        "ok": sum(1 for r in rows if r["status"] == "ok"),
        "timeout": sum(1 for r in rows if r["status"] == "timeout"),
        "exec_s_min": exec_times[0] if exec_times else None,
        "exec_s_median": exec_times[len(exec_times) // 2] if exec_times else None,
        "exec_s_max": exec_times[-1] if exec_times else None,
        "rows": rows,
    }
    with open(REPORT, "w") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
    print(f"[pool] done: {summary['ok']} ok / {summary['timeout']} timeout, "
          f"median exec {summary['exec_s_median']}s -> {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
