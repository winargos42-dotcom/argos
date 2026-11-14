#!/usr/bin/env python3
"""x230_link.py — автоматизированный обмен файлами VIBE <-> ARGOS X230.

Транспорт: файловый хостинг x0.at + GitHub-ветка как доска объявлений.

Входящие (X230 -> VIBE, полностью автоматизировано):
  X230 коммитит vibe_run/inbox.json в ветку GitHub (у X230 есть запись):
    {"messages": [{"msg_id", "type", "url", "sha256", "created_utc"}, ...]}
  Vibe читает файл через `gh api` (read-only токен), скачивает каждое новое
  сообщение, проверяет SHA256, принимает ТОЛЬКО type=="task" c текстовым
  полем "goal", санитизирует и ставит в SQLite-очередь как analyze:-задачу.
  Shell-цели из непроверенных источников никогда не исполняются.

Исходящие (VIBE -> X230, автоматизировано, кроме уведомления):
  send_result() выгружает файл на x0.at и дописывает запись в outbox.jsonl.
  URL x0.at случайны, поэтому передачу URL X230 пока нужно уведомить вручную;
  автоматизируется после возврата прав записи на GitHub или частного туннеля.

Безопасность: никаких токенов в файлах; скачанный payload ограничен 1 МиБ;
SHA256 обязателен; цели только analyze:.
"""

import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import uuid
import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

RUNTIME = os.getenv("ARGOS_RUNTIME", "/workspace/argos-runtime")
os.environ.setdefault("ARGOS_COGNITIVE_SQLITE", f"{RUNTIME}/data/cognitive_memory.db")
os.environ.setdefault("ARGOS_PG_ENABLED", "0")

import httpx  # noqa: E402

INBOX_REPO = os.getenv("ARGOS_X230_INBOX_REPO", "winargos42-dotcom/argos")
INBOX_BRANCH = os.getenv("ARGOS_X230_INBOX_BRANCH", "vibe/argos-vibe-stage1-11-review-20261114")
INBOX_PATH = os.getenv("ARGOS_X230_INBOX_PATH", "vibe_run/inbox.json")
STATE_FILE = os.getenv("ARGOS_X230_LINK_STATE",
                       "/workspace/argos-runtime/x230_link_state.json")
OUTBOX_FILE = os.getenv("ARGOS_X230_OUTBOX",
                        "/workspace/argos-runtime/logs/stage9/outbox.jsonl")
MAX_PAYLOAD = 1024 * 1024
X0_AT = "https://x0.at"


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def load_state() -> dict:
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"seen_msg_ids": []}


def save_state(state: dict) -> None:
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_FILE)


def fetch_inbox() -> list:
    raw = subprocess.run(
        ["gh", "api", f"repos/{INBOX_REPO}/contents/{INBOX_PATH}",
         "-X", "GET", "-f", f"ref={INBOX_BRANCH}"],
        capture_output=True, text=True, timeout=60)
    if raw.returncode != 0:
        raise RuntimeError(f"gh api inbox failed: {raw.stderr.strip()[:200]}")
    import base64
    content = json.loads(raw.stdout).get("content", "")
    doc = json.loads(base64.b64decode(content))
    return doc.get("messages", [])


def download_verified(url: str, sha256: str) -> bytes:
    r = httpx.get(url, timeout=30, follow_redirects=True)
    r.raise_for_status()
    if len(r.content) > MAX_PAYLOAD:
        raise ValueError(f"payload too large: {len(r.content)}")
    got = hashlib.sha256(r.content).hexdigest()
    if got != sha256:
        raise ValueError(f"sha256 mismatch: expected {sha256[:16]}..., got {got[:16]}...")
    return r.content


def sanitize_goal(text: str) -> str:
    text = re.sub(r"[`$|;&><]", " ", text)
    return "analyze: " + text.strip()[:180]


def check_inbox() -> dict:
    """Одна итерация: забрать новые проверенные задачи из inbox.json."""
    from src.cognitive_memory import CognitiveMemory
    state = load_state()
    seen = set(state.get("seen_msg_ids", []))
    summary = {"ok": False, "new_tasks": 0, "skipped": 0, "errors": []}
    try:
        messages = fetch_inbox()
    except Exception as exc:
        summary["error"] = str(exc)[:300]
        return summary
    cm = CognitiveMemory(prefer_pg=False)
    try:
        for m in messages:
            mid = str(m.get("msg_id", ""))
            if not mid or mid in seen:
                continue
            try:
                if m.get("type") != "task":
                    summary["skipped"] += 1
                    seen.add(mid)
                    continue
                payload = json.loads(download_verified(m["url"], m["sha256"]))
                if payload.get("msg_id") != mid:
                    raise ValueError("inner msg_id mismatch")
                # Signed inbound tasks are checked before enqueue.
                # GitHub inbox remains the existing authenticated source.
                has_secret = bool(os.getenv("ARGOS_LINK_SECRET"))
                signed = isinstance(payload.get("auth"), dict)
                if has_secret and signed:
                    from message_auth import verify_envelope, load_key
                    valid, reason = verify_envelope(payload, load_key())
                    if not valid:
                        raise ValueError("inbound task HMAC invalid: " + reason[:60])
                elif os.getenv("ARGOS_LINK_AUTH_REQUIRED") == "1":
                    raise ValueError("inbound task HMAC signature required")
                # Only a verified HMAC task may start an isolated code proposal.
                if payload.get("mode") == "develop":
                    if not has_secret or not signed:
                        raise ValueError("develop requires authenticated signed task")
                    goal = "develop: " + str(payload.get("goal", "")).strip()[:480]
                else:
                    goal = sanitize_goal(str(payload.get("goal", "")))
                if goal in ("analyze: ", "develop: ") or len(goal) < 12:
                    raise ValueError("empty goal")
                gid = cm.add_goal(goal, priority=3)
                # Persist the inbound correlation before the worker can publish
                # any result. Only these goal IDs may leave via public outbox.
                replies = state.setdefault("reply_to_by_goal", {})
                replies[str(gid)] = mid
                save_state(state)
                cm.log_event("x230_link", "task_enqueued",
                             {"goal_id": gid, "msg_id": mid, "goal": goal[:200], "at": now()})
                summary["new_tasks"] += 1
            except Exception as exc:
                summary["errors"].append(f"{mid[:8]}: {str(exc)[:120]}")
                cm.log_event("x230_link", "task_rejected",
                             {"msg_id": mid[:64], "error": str(exc)[:200], "at": now()})
                seen.add(mid)
                continue
            seen.add(mid)
        summary["ok"] = True
    finally:
        cm.close()
    state["seen_msg_ids"] = list(seen)[-200:]
    state["reply_to_by_goal"] = dict(list(state.get("reply_to_by_goal", {}).items())[-1000:])
    state["last_check"] = now()
    save_state(state)
    return summary


def reply_id_for_goal(goal_id: object) -> str | None:
    """Return the verified inbox message ID for an originally accepted goal.

    An arbitrary local task must not be uploaded to public file hosting.
    """
    try:
        return load_state().get("reply_to_by_goal", {}).get(str(goal_id))
    except (TypeError, ValueError):
        return None


RETURN_CFG = Path(__file__).with_name("return_channel.json")
NOTIFIED_FILE = os.getenv("ARGOS_X230_NOTIFIED",
    f"{RUNTIME}/logs/stage9/notice_receipts.jsonl")


def notify_x230(rec: dict) -> dict:
    """Announce only the result URL and SHA, never the full body."""
    if not rec.get("in_reply_to") or (
            reply_id_for_goal(rec.get("goal_id")) != rec["in_reply_to"]):
        raise ValueError("non-inbox result cannot be announced")
    config = json.loads(RETURN_CFG.read_text(encoding="utf-8"))
    if config.get("server") != "https://ntfy.sh":
        raise ValueError("unapproved notice server")
    topic = config.get("topic", "")
    if not re.fullmatch(r"[a-z0-9-]{16,96}", topic):
        raise ValueError("invalid ntfy topic")
    notice = {"schema": 1, "type": "vibe_result_notice",
              "in_reply_to": rec["in_reply_to"],
              "result_msg_id": rec.get("result_msg_id", rec["msg_id"]),
              "goal_id": rec.get("goal_id"),
              "url": rec["url"], "sha256": rec["sha256"],
              "created_utc": now()}
    if os.getenv("ARGOS_LINK_SECRET"):
        from message_auth import sign_envelope, load_key
        notice = sign_envelope(notice, load_key())
    elif os.getenv("ARGOS_LINK_AUTH_REQUIRED") == "1":
        raise RuntimeError("HMAC required but ARGOS_LINK_SECRET absent")
    response = httpx.post(f"https://ntfy.sh/{topic}",
        content=json.dumps(notice, separators=(",", ":")),
        headers={"Content-Type": "text/plain"}, timeout=20)
    response.raise_for_status()
    receipt = response.json()
    if receipt.get("event") != "message" or receipt.get("topic") != topic:
        raise ValueError("ntfy acknowledgement invalid")
    os.makedirs(os.path.dirname(NOTIFIED_FILE), exist_ok=True)
    entry = {"outbox_msg_id": rec["msg_id"], "ntfy_id": receipt["id"],
             "at": now(), "in_reply_to": rec["in_reply_to"]}
    with open(NOTIFIED_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def retry_unnotified(limit: int = 20) -> dict:
    """Retry unpublished notices for previously uploaded inbox results."""
    if not os.path.exists(OUTBOX_FILE):
        return {"pending": 0, "notified": 0, "errors": []}
    already = set()
    if os.path.exists(NOTIFIED_FILE):
        with open(NOTIFIED_FILE, encoding="utf-8") as f:
            for line in f:
                try:
                    already.add(json.loads(line)["outbox_msg_id"])
                except (ValueError, KeyError):
                    continue
    pending = []
    with open(OUTBOX_FILE, encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
                if (rec["msg_id"] not in already and rec.get("in_reply_to")
                        and reply_id_for_goal(rec.get("goal_id")) == rec["in_reply_to"]):
                    pending.append(rec)
            except (ValueError, KeyError):
                continue
    result = {"pending": len(pending), "notified": 0, "errors": []}
    for rec in pending[:limit]:
        try:
            notify_x230(rec)
            result["notified"] += 1
        except Exception as exc:
            result["errors"].append(f"{rec['msg_id'][:8]}: {type(exc).__name__}: {str(exc)[:80]}")
    return result


def send_result(path: str, *, in_reply_to: str | None = None,
                goal_id: object = None) -> dict:
    """Upload verified inbox result; save correlation for notice retries."""
    if in_reply_to and reply_id_for_goal(goal_id) != in_reply_to:
        raise ValueError("cannot export unrelated private task")
    with open(path, "rb") as f:
        raw = f.read()
    if len(raw) > MAX_PAYLOAD:
        raise ValueError(f"payload too large: {len(raw)}")
    source = json.loads(raw)
    if not isinstance(source, dict) or source.get("type") != "result":
        raise ValueError("only result envelopes are eligible")
    if in_reply_to and source.get("in_reply_to") != in_reply_to:
        raise ValueError("outbox correlation mismatch")
    if in_reply_to and source.get("goal_id") != goal_id:
        raise ValueError("outbox goal mismatch")
    if not isinstance(source.get("msg_id"), str):
        raise ValueError("missing result msg_id")
    r = httpx.post(X0_AT,
                   files={"file": (os.path.basename(path), raw, "application/octet-stream")},
                   timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"x0.at upload failed: HTTP {r.status_code} {r.text[:100]}")
    url = r.text.strip()
    rec = {"msg_id": str(uuid.uuid4()), "file": os.path.basename(path),
           "url": url, "sha256": hashlib.sha256(raw).hexdigest(),
           "size": len(raw), "ts": now(),
           "result_msg_id": source["msg_id"],
           "in_reply_to": in_reply_to, "goal_id": goal_id}
    os.makedirs(os.path.dirname(OUTBOX_FILE), exist_ok=True)
    with open(OUTBOX_FILE, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "--status"
    if cmd == "--check":
        print(json.dumps(check_inbox(), indent=2))
    elif cmd == "--send":
        print(json.dumps(send_result(sys.argv[2]), indent=2))
    else:
        state = load_state()
        print(json.dumps({"state_file": STATE_FILE,
                          "seen_msg_ids": len(state.get("seen_msg_ids", [])),
                          "last_check": state.get("last_check"),
                          "inbox": f"{INBOX_REPO}@{INBOX_BRANCH}:{INBOX_PATH}"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
