"""ARGOS-VIBE persistent daemon: background task processing node.

Stage 7. Runs the ORIGINAL ArgosMasterCore/CognitiveMemory stack as a long-lived
background node:

  * 2 worker threads (hard cap) draining the original CognitiveMemory goals
    table through agent_pool (atomic claim, exactly-once crash recovery).
  * Heartbeat: every ARGOS_DAEMON_HEARTBEAT_S seconds a heartbeat event is
    written to SQLite and a heartbeat JSON file is refreshed atomically.
  * Sandbox-restart detection: /proc/sys/kernel/random/boot_id is compared
    with the stored one; on change a sandbox_restart event is logged and the
    queue is recovered (exactly-once) before workers start.
  * GitHub watcher (read-only, gh CLI): every ARGOS_DAEMON_POLL_S seconds
    (default 900 = 15 min) new commits on main and open issues of
    winargos42-dotcom/argos are checked. New items are enqueued ONLY as
    "analyze:" goals routed to the local LLM. Issue bodies are never executed:
    titles are sanitized, and no shell-prefixed goal is ever auto-enqueued
    from unverified sources.
  * Results of every processed task are appended to a JSONL results file and
    to CognitiveMemory (events/knowledge/reflections), so unfinished work
    survives a restart in the SQLite queue.

Honest limitation: this daemon lives inside the Vibe sandbox. Files persist,
processes live only while the sandbox VM lives; after a sandbox restart the
boot-id check detects it and the daemon recovers the queue on its next start.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO = os.getenv("ARGOS_REPO", "/workspace/github__winargos42-dotcom__argos")
RUNTIME = os.getenv("ARGOS_RUNTIME", "/workspace/argos-runtime")
VENV_PY = f"{RUNTIME}/venv/bin/python"
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(RUNTIME)
os.environ.setdefault("ARGOS_LOG_DIR", f"{RUNTIME}/logs")
os.environ.setdefault("ARGOS_COGNITIVE_SQLITE", f"{RUNTIME}/data/cognitive_memory.db")
os.environ.setdefault("ARGOS_PG_ENABLED", "0")
os.environ.setdefault("ARGOS_POOL_WORKERS", "2")
os.environ.setdefault("ARGOS_POOL_TASK_TIMEOUT", "120")

import agent_pool  # noqa: E402
from src.cognitive_memory import CognitiveMemory  # noqa: E402

REPO_SLUG = os.getenv("ARGOS_WATCH_REPO", "winargos42-dotcom/argos")
HEARTBEAT_S = float(os.getenv("ARGOS_DAEMON_HEARTBEAT_S", "60"))
POLL_S = float(os.getenv("ARGOS_DAEMON_POLL_S", "900"))
STATE_FILE = Path(os.getenv("ARGOS_DAEMON_STATE", f"{RUNTIME}/daemon_state.json"))
HEARTBEAT_FILE = Path(os.getenv("ARGOS_DAEMON_HEARTBEAT", f"{RUNTIME}/daemon_heartbeat.json"))
RESULTS_FILE = Path(os.getenv("ARGOS_DAEMON_RESULTS", f"{RUNTIME}/logs/stage7/daemon_results.jsonl"))

WORKERS = 2  # hard cap per task assignment


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def boot_id() -> str:
    try:
        return Path("/proc/sys/kernel/random/boot_id").read_text().strip()
    except OSError:
        return "unknown"


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {}


def save_state(state: dict) -> None:
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    tmp.replace(STATE_FILE)


def service_ok(url: str) -> bool:
    try:
        import httpx
        return httpx.get(url, timeout=5).status_code == 200
    except Exception:
        return False


def enqueue_goal(cm: CognitiveMemory, text: str, priority: int = 3) -> int:
    gid = cm.add_goal(text, priority=priority)
    cm.log_event("daemon", "goal_enqueued", {"goal_id": gid, "goal": text[:300], "at": now()})
    return gid


def sanitize_unverified(text: str) -> str:
    text = re.sub(r"[`$|;&><]", " ", text)
    low = text.strip().lower()
    for p in agent_pool.SHELL_PREFIXES:
        if low.startswith(p):
            return "analyze: " + text.strip()[len(p):].strip()[:180]
    return "analyze: " + text.strip()[:180]


def github_watch(cm: CognitiveMemory, state: dict, results: agent_pool.TaskResult) -> dict:
    """Read-only GitHub watcher; returns a poll summary for logging."""
    summary = {"repo": REPO_SLUG, "ok": False, "new_commits": 0, "new_issues": 0}
    try:
        commits = json.loads(subprocess.run(
            ["gh", "api", f"repos/{REPO_SLUG}/commits", "-X", "GET",
             "-f", "sha=main", "-f", "per_page=10"],
            capture_output=True, text=True, timeout=60).stdout)
        seen_shas = set(state.get("seen_shas", []))
        shas = [c["sha"] for c in commits]
        new = [c for c in commits if c["sha"] not in seen_shas]
        if seen_shas and new:
            summary["new_commits"] = len(new)
            short = ", ".join(c["sha"][:8] for c in new[:5])
            enqueue_goal(cm, f"analyze: new commits on {REPO_SLUG} main: {short}")
        elif not seen_shas:
            summary["baseline"] = len(shas)
        state["seen_shas"] = shas[-50:]

        issues = json.loads(subprocess.run(
            ["gh", "api", f"repos/{REPO_SLUG}/issues", "-X", "GET",
             "-f", "state=open", "-f", "per_page=20"],
            capture_output=True, text=True, timeout=60).stdout)
        seen_issues = set(state.get("seen_issues", []))
        for issue in issues:
            n = issue["number"]
            if n in seen_issues or "pull_request" in issue:
                continue
            title = sanitize_unverified(issue.get("title", ""))
            enqueue_goal(cm, f"analyze: issue #{n}: {title}")
            seen_issues.add(n)
            summary["new_issues"] += 1
        state["seen_issues"] = sorted(seen_issues)[-50:]
        state["last_poll_at"] = now()
        summary["ok"] = True
        save_state(state)
    except Exception as exc:
        summary["error"] = str(exc)[:300]
    return summary


def heartbeat_loop(cm: CognitiveMemory, results: agent_pool.TaskResult, state: dict,
                   stop: threading.Event) -> None:
    beat = 0
    while not stop.wait(HEARTBEAT_S):
        beat += 1
        try:
            con_state = cm.counts() if hasattr(cm, "counts") else {}
        except Exception:
            con_state = {}
        payload = {
            "ts": now(), "pid": os.getpid(), "boot_id": boot_id(),
            "workers": WORKERS, "beats": beat,
            "services": {"mcp": service_ok("http://127.0.0.1:8000/health"),
                         "gateway": service_ok("http://127.0.0.1:8080/health"),
                         "llm": service_ok("http://127.0.0.1:11434/health")},
            "tasks_processed": len(results.rows),
            "last_poll_at": state.get("last_poll_at"),
            "memory_counts": con_state,
        }
        tmp = HEARTBEAT_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        tmp.replace(HEARTBEAT_FILE)
        cm.log_event("daemon", "heartbeat", payload)


def result_envelope(row: dict, reply_id: str) -> dict:
    return {
        "msg_id": str(uuid.uuid4()),
        "type": "result",
        "in_reply_to": reply_id,
        "from": "argos-vibe-sandbox",
        "to": "argos-x230",
        "goal_id": row.get("goal_id"),
        "status": row.get("status"),
        "mode": row.get("mode"),
        "exec_s": row.get("exec_s"),
        "result": str(row.get("result", ""))[:4000],
        "created_utc": now(),
    }


def x230_outbox_push(row: dict) -> None:
    """Upload a finished task result to x0.at and record it in outbox.jsonl.

    The upload is automatic; delivering the new URL to X230 still needs one
    manual hop until VIBE regains GitHub write or a private tunnel exists.
    """
    try:
        import tempfile

        import x230_link
        reply_id = x230_link.reply_id_for_goal(row.get("goal_id"))
        if not reply_id:
            return  # Local tasks/results must never be exported publicly.
        env = result_envelope(row, reply_id)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                         encoding="utf-8") as tf:
            json.dump(env, tf, ensure_ascii=False, indent=2)
            path = tf.name
        try:
            rec = x230_link.send_result(
                path, in_reply_to=reply_id, goal_id=env["goal_id"])
        finally:
            os.unlink(path)
        cm = CognitiveMemory(prefer_pg=False)
        cm.log_event("x230_link", "result_outboxed",
                     {"url": rec["url"], "sha256": rec["sha256"],
                      "goal_id": env["goal_id"], "at": now()})
        try:
            notice = x230_link.notify_x230(rec)
            cm.log_event("x230_link", "result_notice_sent", notice)
        except Exception as exc:
            cm.log_event("x230_link", "result_notice_error",
                         {"goal_id": env["goal_id"], "error": str(exc)[:200], "at": now()})
        cm.close()
    except Exception as exc:
        cm = CognitiveMemory(prefer_pg=False)
        cm.log_event("x230_link", "result_outbox_error",
                     {"error": str(exc)[:200], "goal_id": row.get("goal_id"), "at": now()})
        cm.close()


def results_writer(results: agent_pool.TaskResult, stop: threading.Event) -> None:
    written = 0
    auto_outbox = os.getenv("ARGOS_X230_AUTO_OUTBOX", "1") == "1"
    while not stop.wait(10):
        rows = results.rows
        if len(rows) > written:
            new_rows = rows[written:]
            with RESULTS_FILE.open("a") as fh:
                for row in new_rows:
                    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            written = len(rows)
            if auto_outbox:
                import x230_link
                for row in new_rows:
                    # Explicitly scope public uploads to validated inbox tasks.
                    if (row.get("status") == "ok" and
                            x230_link.reply_id_for_goal(row.get("goal_id"))):
                        threading.Thread(target=x230_outbox_push, args=(row,),
                                         daemon=True).start()


def main() -> int:
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = load_state()
    old_boot = state.get("boot_id")
    current_boot = boot_id()
    restarted = old_boot is not None and old_boot != current_boot

    cm = CognitiveMemory(prefer_pg=False)
    if restarted:
        cm.log_event("daemon", "sandbox_restart",
                     {"old_boot_id": old_boot, "new_boot_id": current_boot, "at": now()})
        print(f"[daemon] sandbox restart detected (boot_id changed) — queue recovered below")
    state["boot_id"] = current_boot
    state["daemon_pid"] = os.getpid()

    recovery = agent_pool.recover_stale_claims()
    cm.log_event("daemon", "start", {"pid": os.getpid(), "recovery": recovery,
                                     "restarted": restarted, "workers": WORKERS, "at": now()})
    save_state(state)
    print(f"[daemon] pid={os.getpid()} workers={WORKERS} heartbeat={HEARTBEAT_S}s "
          f"github_poll={POLL_S}s restarted={restarted} recovery={recovery}")

    results = agent_pool.TaskResult()
    stop = threading.Event()

    threads = [threading.Thread(target=agent_pool.worker_loop,
                                args=(f"d{i}", stop, results), daemon=True)
               for i in range(WORKERS)]
    threads.append(threading.Thread(target=heartbeat_loop,
                                    args=(cm, results, state, stop), daemon=True))
    threads.append(threading.Thread(target=results_writer,
                                    args=(results, stop), daemon=True))
    for t in threads:
        t.start()

    poll = github_watch(cm, state, results)
    cm.log_event("daemon", "github_poll", poll)
    print(f"[daemon] first github poll: {poll}")

    # A successful first poll alone does not keep the node useful.
    # Schedule subsequent polls on a monotonic clock, avoiding tight loops if
    # a misconfigured interval is zero or negative. External tasks remain
    # analyze-only via github_watch() and are never executed as shell goals.
    interval = max(30.0, POLL_S)
    next_poll_at = time.monotonic() + interval
    try:
        while True:
            delay = next_poll_at - time.monotonic()
            if delay > 0:
                time.sleep(min(5.0, delay))
                continue
            poll = github_watch(cm, state, results)
            cm.log_event("daemon", "github_poll", poll)
            print(f"[daemon] scheduled github poll: {poll}", flush=True)
            try:
                import x230_link
                inbox = x230_link.check_inbox()
                cm.log_event("daemon", "x230_inbox", inbox)
                if inbox.get("new_tasks") or inbox.get("errors"):
                    print(f"[daemon] x230 inbox: {inbox}", flush=True)
            except Exception as exc:
                cm.log_event("daemon", "x230_inbox_error", {"error": str(exc)[:200], "at": now()})
            try:
                import x230_link
                retries = x230_link.retry_unnotified()
                cm.log_event("daemon", "x230_notice_retries", retries)
            except Exception as exc:
                cm.log_event("daemon", "x230_notice_retry_error",
                             {"error": str(exc)[:200], "at": now()})
            next_poll_at = time.monotonic() + interval
    except KeyboardInterrupt:
        print("[daemon] interrupt — stopping")
    finally:
        stop.set()
        for t in threads:
            t.join(timeout=5)
        cm.log_event("daemon", "stop", {"tasks_processed": len(results.rows), "at": now()})
        cm.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
