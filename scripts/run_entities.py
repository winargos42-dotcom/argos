#!/usr/bin/env python3
"""
ARGOS Entity Bus v4 — WORKERS, not talkers.

- TASKS from real system problems, not "what should we think?"
- ACTIONS executed by CODE directly, AI only for analysis
- AI called ONLY when real problem needs analysis
- No "I suggest" — only "done" or "failed"
"""

import os, sys, time, json, threading, requests, subprocess, datetime, re
import urllib.request, tempfile, shutil
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from logging_config import configure_logging
    configure_logging()
except Exception:
    pass

from dotenv import load_dotenv
load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────

BRAIN = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")

# Ноды, которые ожидаемо могут быть оффлайн — не генерируют задачи
EXPECTED_OFFLINE = {"argos-android", "argos-phone-agent", "argos-esp32-display", "argos-phone-redmi"}
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
ARGOS_ROOT = Path(__file__).resolve().parent.parent
if os.name == "nt":
    VAULT = Path(os.getenv("ARGOS_VAULT", r"F:\debug\аргос\05 SharedMemory Mirror"))
else:
    VAULT = Path(os.getenv("ARGOS_VAULT", "/home/ava/Documents/MyObsidianVault/SharedMemory"))
GROUP_ID = -5129226282
TOKENS_FILE = ARGOS_ROOT / "data/entity_bot_tokens.json"

env_text = open(ARGOS_ROOT / ".env", encoding="utf-8").read()
def _envkey(n):
    return next((l.split("=",1)[1].strip().strip('"').strip("'") for l in env_text.split("\n") if l.startswith(f"{n}=")), "")

HA_TOKEN = _envkey("HA_TOKEN") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjMWIwZDgxNzdkNDY0NGRjOWM4YmI4OGZiM2VkOGRjZSIsImlhdCI6MTc3NzkyMDY5MiwiZXhwIjoyMDkzMjgwNjkyfQ.nV0ps3wDPz4NAiqwKCyyTLcwK-oxUdvg2ohIG4p6Ozs"

# ── AI providers (minimal calls) ──────────────────────────────────────────

API_KEYS = {
    "claude": _envkey("ANTHROPIC_API_KEY"),
    "deepseek": _envkey("DEEPSEEK_API_KEY"),
    "openai": _envkey("OPENAI_API_KEY"),
    "gemini": _envkey("GEMINI_API_KEY") or _envkey("GOOGLE_API_KEY"),
    "cloudflare": _envkey("CF_AI_TOKEN"),
}

def ask_claude(prompt: str, system: str = "", max_tokens: int = 200) -> str | None:
    key = API_KEYS["claude"]
    if not key: return None
    try:
        body = json.dumps({"model": "claude-haiku-4-5-20251001", "max_tokens": max_tokens,
            "system": system[:800], "messages": [{"role": "user", "content": prompt[:1500]}]}).encode()
        req = urllib.request.Request("https://api.anthropic.com/v1/messages",
            data=body, headers={"x-api-key": key, "anthropic-version": "2023-06-01",
            "content-type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())["content"][0]["text"]
    except Exception: return None

def ask_deepseek(prompt: str, system: str = "", max_tokens: int = 200) -> str | None:
    key = API_KEYS["deepseek"]
    if not key: return None
    try:
        msgs = []
        if system: msgs.append({"role": "system", "content": system[:800]})
        msgs.append({"role": "user", "content": prompt[:1500]})
        body = json.dumps({"model": "deepseek-chat", "messages": msgs,
            "max_tokens": max_tokens, "temperature": 0.3}).encode()
        req = urllib.request.Request("https://api.deepseek.com/chat/completions",
            data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"]
    except Exception: return None

def ask_ollama(prompt: str, system: str = "", max_tokens: int = 200) -> str | None:
    """Fallback через локальную Ollama (Nexus laptop)."""
    for model in ["argos-v2:latest", "qwen2.5:0.5b"]:
        try:
            full = f"{system}\n\n{prompt}" if system else prompt
            body = json.dumps({"model": model, "prompt": full[:2000],
                "stream": False, "options": {"temperature": 0.7, "num_predict": max_tokens}}).encode()
            req = urllib.request.Request("http://localhost:11434/api/generate",
                data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                text = json.load(r).get("response", "")
                if text and len(text) > 10:
                    return text[:500]
        except Exception:
            continue
    return None

def ask_gemini(prompt: str, system: str = "") -> str | None:
    # Gemini геоблокирован — используем OpenAI gpt-4o-mini как замену
    key = API_KEYS.get("openai") or _envkey("OPENAI_API_KEY")
    if not key: return None
    try:
        msgs = []
        if system: msgs.append({"role": "system", "content": system})
        msgs.append({"role": "user", "content": prompt[:3000]})
        body = json.dumps({"model": "gpt-4o-mini", "max_tokens": 200, "messages": msgs}).encode()
        req = urllib.request.Request("https://api.openai.com/v1/chat/completions",
            data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)["choices"][0]["message"]["content"]
    except Exception: return None


# ── Actions (no AI parsing!) ──────────────────────────────────────────────

class Actions:
    """Each method = concrete action with measurable result."""

    @staticmethod
    def restart_service(service: str) -> str:
        try:
            r = subprocess.run(["sudo", "-n", "systemctl", "restart", service],
                capture_output=True, text=True, timeout=10)
            return f"OK restart {service}" if r.returncode == 0 else f"FAIL {r.stderr[:60]}"
        except Exception as e: return f"FAIL {e}"

    @staticmethod
    def check_services() -> list:
        try:
            r = subprocess.run(["systemctl", "list-units", "argos-*", "--no-pager", "--no-legend"],
                capture_output=True, text=True, timeout=10)
            results = []
            for line in r.stdout.strip().split("\n"):
                # Strip unicode bullets (●) and leading whitespace
                line = line.lstrip().encode('ascii', errors='ignore').decode().strip()
                if not line: continue
                parts = line.split()
                if len(parts) >= 4:
                    results.append({"service": parts[0], "active": parts[2] == "active", "sub": parts[3]})
            return results
        except Exception: return []

    @staticmethod
    def ha_get_states() -> list:
        try:
            url = "http://localhost:8123/api/states"
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {HA_TOKEN}"})
            with urllib.request.urlopen(req, timeout=8) as r:
                return json.loads(r.read())
        except Exception: return None

    @staticmethod
    def ha_call_service(domain: str, service: str, data: dict = None) -> str:
        try:
            url = f"http://localhost:8123/api/services/{domain}/{service}"
            body = json.dumps(data or {}).encode()
            req = urllib.request.Request(url, data=body, method="POST",
                headers={"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=8) as r:
                return f"OK {domain}.{service}"
        except Exception as e: return f"FAIL {e}"

    @staticmethod
    def brain_get(path: str) -> dict:
        try:
            req = urllib.request.Request(f"{BRAIN}{path}")
            with urllib.request.urlopen(req, timeout=5) as r:
                return json.loads(r.read())
        except Exception: return None

    @staticmethod
    def mqtt_pub(topic: str, payload: dict):
        try:
            subprocess.run(["mosquitto_pub", "-h", MQTT_HOST, "-p", str(MQTT_PORT),
                "-t", topic, "-m", json.dumps(payload, ensure_ascii=False)],
                capture_output=True, timeout=5)
        except Exception: pass

    @staticmethod
    def run_cmd(cmd: str, timeout: int = 15) -> str:
        BLOCKED = ["rm -rf", "mkfs", "dd if=", "> /dev/", "format", "shutdown", "reboot", "passwd"]
        for b in BLOCKED:
            if b in cmd: return f"BLOCKED: {b}"
        # AI часто выдаёт "systemctl restart/start/stop/reload ..." и "docker restart ..." без sudo,
        # что падает с "Access denied as the requested operation requires interactive authentication"
        # (sudoers разрешает NOPASSWD именно с sudo -n).
        if re.match(r"^\s*(systemctl\s+(restart|start|stop|reload)\b|docker\s+restart\b)", cmd):
            cmd = f"sudo -n {cmd.strip()}"
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            return (r.stdout + r.stderr)[:300].strip() or f"exit={r.returncode}"
        except Exception as e: return f"FAIL {e}"

    @staticmethod
    def write_obsidian(content: str, path: str) -> str:
        full_path = VAULT / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n## [{ts}]\n{content[:500]}\n"
        try:
            existing = full_path.read_text(encoding="utf-8") if full_path.exists() else f"# {full_path.stem}\n"
            lines = (existing + entry).split("\n")
            if len(lines) > 100: lines = lines[:10] + lines[-90:]
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                 dir=full_path.parent, suffix='.tmp', delete=False) as tf:
                tf.write("\n".join(lines))
                shutil.move(tf.name, str(full_path))
            return f"OK {path}"
        except Exception as e: return f"FAIL {e}"

    @staticmethod
    def check_url(url: str, timeout: int = 5, headers: dict = None) -> str:
        try:
            req = urllib.request.Request(url)
            if headers:
                for k, v in headers.items():
                    req.add_header(k, v)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return f"OK {url} -> {r.status}"
        except urllib.error.HTTPError as e:
            # 401/403 = сервер живой, просто авторизация — не считаем падением
            if e.code in (401, 403):
                return f"OK {url} -> {e.code} (auth)"
            return f"FAIL {url}: HTTP {e.code}"
        except Exception as e: return f"FAIL {url}: {str(e)[:60]}"


# ── Problem Scanner ───────────────────────────────────────────────────────

class ProblemScanner:
    """Scans system and generates TASKS from real problems."""

    @staticmethod
    def scan_failed_services() -> list:
        tasks = []
        svcs = Actions.check_services()
        for s in svcs:
            # Skip services that are expected to be in auto-restart (like autopilot without API key)
            if s["service"] in ("argos-autopilot.service",): continue
            if not s["active"] and s["sub"] in ("failed", "auto-restart") and s["sub"] != "activating":
                tasks.append({
                    "type": "restart_service",
                    "priority": "critical",
                    "target": s["service"],
                    "reason": f"Service {s['service']} state={s['sub']}",
                    "assignee": "autoheal",
                })
        return tasks

    @staticmethod
    def scan_ha_problems() -> list:
        tasks = []
        states = Actions.ha_get_states()
        if not states: return [{"type": "check_ha", "priority": "critical",
            "reason": "HA API unreachable", "assignee": "gemini"}]

        unavailable = [s for s in states if s.get("state") == "unavailable"]
        if unavailable:
            domains = defaultdict(list)
            for s in unavailable:
                domain = s["entity_id"].split(".")[0]
                domains[domain].append(s["entity_id"])
            top_domains = sorted(domains.items(), key=lambda x: -len(x[1]))[:3]
            summary = ", ".join(f"{d}:{len(e)}" for d, e in top_domains)
            tasks.append({
                "type": "fix_ha_entities",
                "priority": "normal",
                "reason": f"{len(unavailable)} unavailable: {summary}",
                "assignee": "gemini",
                "data": {"unavailable": [s["entity_id"] for s in unavailable[:20]]},
            })
        return tasks

    @staticmethod
    def scan_brain_nodes() -> list:
        tasks = []
        data = Actions.brain_get("/brain/nodes")
        if not data: return [{"type": "check_brain", "priority": "critical",
            "reason": "Brain API unreachable", "assignee": "deepseek"}]
        # Исключаем ноды, которые ожидаемо могут быть оффлайн
        offline = [n for n in data.get("nodes", [])
                   if n.get("status") != "online" and n["node_id"] not in EXPECTED_OFFLINE]
        if offline:
            tasks.append({
                "type": "check_offline_nodes",
                "priority": "normal",
                "reason": f"Offline: {', '.join(n['node_id'] for n in offline[:5])}",
                "assignee": "deepseek",
                "data": {"offline": [n["node_id"] for n in offline]},
            })
        return tasks

    @staticmethod
    def scan_endpoints() -> list:
        tasks = []
        # HA проверяется в scan_ha_problems — не дублируем здесь
        checks = [
            (f"{BRAIN}/health", "Brain PC Master", {}),
        ]
        for url, name, headers in checks:
            result = Actions.check_url(url, headers=headers)
            if "FAIL" in result:
                tasks.append({
                    "type": "check_endpoint",
                    "priority": "critical",
                    "reason": f"{name} down: {result}",
                    "assignee": "deepseek",
                    "data": {"url": url, "name": name},
                })
        return tasks

    @staticmethod
    def scan_system_resources() -> list:
        tasks = []
        try:
            r = subprocess.run(["free", "--mega"], capture_output=True, text=True, timeout=5)
            lines = r.stdout.strip().split("\n")
            if len(lines) >= 2:
                parts = lines[1].split()
                total, used = int(parts[1]), int(parts[2])
                pct = used / total * 100 if total > 0 else 0
                if pct > 90:
                    tasks.append({
                        "type": "high_ram",
                        "priority": "critical",
                        "reason": f"RAM {pct:.0f}%",
                        "assignee": "autoheal",
                        "data": {"ram_pct": pct},
                    })
        except Exception: pass

        try:
            r = subprocess.run(["uptime"], capture_output=True, text=True, timeout=5)
            load = r.stdout.strip()
            if "load average" in load:
                parts = load.split("load average:")[-1].strip().split(",")
                if parts:
                    load1 = float(parts[0].strip())
                    if load1 > 8:
                        tasks.append({
                            "type": "high_cpu",
                            "priority": "normal",
                            "reason": f"Load {load1:.1f}",
                            "assignee": "autoheal",
                        })
        except Exception: pass
        return tasks

    @staticmethod
    def scan_all() -> list:
        tasks = []
        tasks.extend(ProblemScanner.scan_failed_services())
        tasks.extend(ProblemScanner.scan_brain_nodes())
        tasks.extend(ProblemScanner.scan_endpoints())
        tasks.extend(ProblemScanner.scan_system_resources())
        tasks.extend(ProblemScanner.scan_ha_problems())
        priority_order = {"critical": 0, "normal": 1, "low": 2}
        tasks.sort(key=lambda t: priority_order.get(t.get("priority", "normal"), 1))
        return tasks


# ── Task Executor ─────────────────────────────────────────────────────────

class TaskExecutor:
    """Executes tasks directly. AI only for complex analysis."""

    @staticmethod
    def execute(task: dict) -> str:
        t = task["type"]

        if t == "restart_service":
            result = Actions.restart_service(task["target"])
            Actions.mqtt_pub("argos/actions", {"type": "restart", "service": task["target"], "result": result})
            return f"RESTART: {task['target']} -> {result}"

        elif t == "check_ha":
            result = Actions.check_url("http://localhost:8123/api/")
            if "FAIL" in result:
                r = Actions.run_cmd("docker restart homeassistant")
                return f"HA DOWN -> restart docker: {r[:100]}"
            return f"HA OK: {result}"

        elif t == "check_brain":
            r1 = Actions.check_url(f"{BRAIN}/health")
            return f"Brain PC Master: {r1}"

        elif t == "fix_ha_entities":
            unavailable = task.get("data", {}).get("unavailable", [])
            if not unavailable: return "No unavailable entities"
            # Reload homeassistant integration to re-discover entities
            r = Actions.ha_call_service("homeassistant", "reload_core_config")
            return f"Reload core config: {r}"

        elif t == "check_offline_nodes":
            offline = task.get("data", {}).get("offline", [])
            results = []
            for node_id in offline[:3]:
                try:
                    requests.post(f"{BRAIN}/brain/heartbeat", json={"node_id": node_id}, timeout=3)
                    results.append(f"{node_id}: hb sent")
                except Exception:
                    results.append(f"{node_id}: unreachable")
            return f"Re-hb: {'; '.join(results)}"

        elif t == "check_endpoint":
            url = task.get("data", {}).get("url", "")
            name = task.get("data", {}).get("name", "")
            result = Actions.check_url(url)
            return f"{name}: {result}"

        elif t == "high_ram":
            r = Actions.run_cmd("ps aux --sort=-%mem | head -6")
            return f"Top RAM:\n{r}"

        elif t == "high_cpu":
            r = Actions.run_cmd("ps aux --sort=-%cpu | head -6")
            return f"Top CPU:\n{r}"

        else:
            return f"Unknown: {t}"

    @staticmethod
    def execute_with_ai_analysis(task: dict) -> str:
        result = TaskExecutor.execute(task)
        if task.get("priority") == "critical" and "FAIL" in result:
            analysis = ask_deepseek(
                f"ARGOS problem: {task.get('reason','')}\nAttempt: {result}\nOne shell command to fix. Max 30 words.",
                "System engineer. Only concrete commands.",
            )
            if analysis:
                Actions.write_obsidian(
                    f"CRITICAL: {task.get('reason','')}\nAttempt: {result}\nAI: {analysis[:300]}",
                    "entities/alerts/critical.md"
                )
                return f"{result}\nAI: {analysis[:120]}"
        return result


# ── Registration and Heartbeat ──────────────────────────────────────────────

AI_ENTITIES = {
    "entity-claude": {"name": "Claude", "role": "analyst"},
    "entity-deepseek": {"name": "DeepSeek", "role": "network engineer"},
    "entity-kimi": {"name": "Kimi", "role": "researcher"},
    "entity-openai": {"name": "OpenAI", "role": "api developer"},
    "entity-gemini": {"name": "Gemini", "role": "ha analyst"},
    "entity-cloudflare": {"name": "Cloud", "role": "tunnel monitor"},
    "entity-argos": {"name": "ARGOS", "role": "orchestrator"},
}

INFRA_NODES = {
    "argos-pc": {"endpoint": "192.168.1.53:5001"},
    "argos-laptop": {"endpoint": "192.168.1.53:5001"},
    "orangepi": {"endpoint": "192.168.2.168:7777"},
    "argos-railway": {"endpoint": "argos-v2-production.up.railway.app"},
    "argos-gcp": {"endpoint": "argos-core-m3gk27ccqa-uc.a.run.app"},
    "argos-esp-bridge": {"endpoint": "192.168.1.181"},
    "argos-esp32-display": {"endpoint": "192.168.1.211"},
    "argos-phone-redmi": {"endpoint": "192.168.1.149"},
    "ollama-pc": {"endpoint": "192.168.1.53:11434"},
    # Cloud AI entities
    "railway-claude": {"endpoint": "argos-v2-production.up.railway.app"},
    "railway-deepseek": {"endpoint": "argos-v2-production.up.railway.app"},
    "gcp-claude": {"endpoint": "argos-core-m3gk27ccqa-uc.a.run.app"},
    "gcp-gemini": {"endpoint": "argos-core-m3gk27ccqa-uc.a.run.app"},
    "gcp-openai": {"endpoint": "argos-core-m3gk27ccqa-uc.a.run.app"},
}

ALL_NODES = {**AI_ENTITIES, **INFRA_NODES}

def register_all():
    for eid, info in ALL_NODES.items():
        try:
            addr = info.get("endpoint", eid)
            requests.post(f"{BRAIN}/brain/register", json={
                "node_id": eid, "address": addr,
                "capabilities": ["ai"] if eid in AI_ENTITIES else ["infra"],
                "meta": {"role": info.get("role", "")}
            }, timeout=5)
            print(f"  + {eid}: registered")
        except Exception as e:
            print(f"  - {eid}: {e}")


def heartbeat_loop():
    while True:
        for eid in ALL_NODES:
            try:
                requests.post(f"{BRAIN}/brain/heartbeat", json={"node_id": eid}, timeout=3)
            except Exception: pass
        time.sleep(60)


def mqtt_heartbeat_loop():
    while True:
        for eid, info in AI_ENTITIES.items():
            Actions.mqtt_pub(f"argos/agents/{eid}/heartbeat", {
                "agent": eid, "status": "online", "role": info.get("role", ""), "time": time.time()
            })
        time.sleep(60)


# ── Main worker loop ──────────────────────────────────────────────────────

last_action_log = defaultdict(float)
last_tg_alert_ts = 0.0
TG_ALERT_COOLDOWN = 1800  # не чаще раза в 30 мин

# Cooldown в секундах по типу задачи
TASK_COOLDOWNS = {
    "check_ha":            600,   # 10 мин — HA не поднимается мгновенно
    "fix_ha_entities":     600,   # 10 мин — reload не помогает при аппаратных проблемах
    "check_offline_nodes": 600,   # 10 мин — оффлайн ноды не восстанавливаются сами
    "check_endpoint":      300,   # 5 мин
    "restart_service":     300,   # 5 мин (с target)
    "check_brain":         300,
    "high_ram":            300,
    "high_cpu":            180,
}

def should_execute(task: dict) -> bool:
    t = task["type"]
    # Для restart_service включаем target чтобы разные сервисы не блокировали друг друга
    if t == "restart_service":
        key = f"{t}:{task.get('target', '')}"
    else:
        # Для всех остальных — только тип, без reason (reason меняется → bypass cooldown)
        key = t
    cooldown = TASK_COOLDOWNS.get(t, 300)
    if time.time() - last_action_log.get(key, 0) < cooldown:
        return False
    last_action_log[key] = time.time()
    return True


def worker_loop():
    cycle = 0
    while True:
        cycle += 1
        ts = time.strftime("%H:%M:%S")

        tasks = ProblemScanner.scan_all()

        if not tasks:
            if cycle % 5 == 0:
                print(f"  [{ts}] System stable")
                Actions.mqtt_pub("argos/bus/status", {"status": "stable", "tasks": 0, "time": time.time()})
            time.sleep(60)
            continue

        fresh_tasks = [t for t in tasks if should_execute(t)]

        if not fresh_tasks:
            if cycle % 5 == 0:
                print(f"  [{ts}] {len(tasks)} problems, cooling down")
            time.sleep(60)
            continue

        print(f"  [{ts}] {len(fresh_tasks)} tasks ({len(tasks)} total)")
        results = []
        for task in fresh_tasks[:5]:
            result = TaskExecutor.execute_with_ai_analysis(task)
            assignee = task.get("assignee", "?")
            reason = task.get("reason", "")[:60]
            print(f"  >> [{assignee}] {task['type']}: {reason}")
            print(f"     -> {result[:120]}")
            results.append({"task": task["type"], "assignee": assignee, "result": result[:200]})

            Actions.write_obsidian(
                f"[{assignee}] {task['type']}: {reason}\nResult: {result[:300]}",
                "entities/actions/log.md"
            )

        Actions.mqtt_pub("argos/bus/actions", {
            "cycle": cycle, "tasks": len(fresh_tasks),
            "results": results, "time": time.time()
        })

        if any("FAIL" in r.get("result", "") for r in results):
            global last_tg_alert_ts
            if time.time() - last_tg_alert_ts > TG_ALERT_COOLDOWN:
                send_tg_alert(f"ARGOS: {len(fresh_tasks)} problems\n" +
                    "\n".join(f"- {r['task']}: {r['result'][:80]}" for r in results[:3]))
                last_tg_alert_ts = time.time()

        time.sleep(60)


# ── Periodic AI analysis (every 10 min) ───────────────────────────────────

def ai_analysis_loop():
    while True:
        time.sleep(600)
        try:
            ts = time.strftime("%H:%M:%S")

            svcs = Actions.check_services()
            active = [s for s in svcs if s["active"]]
            failed = [s for s in svcs if not s["active"] and s["sub"] not in ("inactive", "dead")]
            ha_states = Actions.ha_get_states()
            unavail_count = sum(1 for s in (ha_states or []) if s.get("state") == "unavailable") if ha_states else "?"
            brain = Actions.brain_get("/brain/nodes")
            online_count = sum(1 for n in (brain or {}).get("nodes", []) if n.get("status") == "online") if brain else "?"

            context = (
                f"Services: {len(active)} active, {len(failed)} failed\n"
                f"HA: {len(ha_states or [])} entities, {unavail_count} unavailable\n"
                f"Brain: {online_count} nodes online\n"
            )
            if failed:
                context += f"Failed: {', '.join(s['service'] for s in failed[:5])}\n"

            analysis = ask_deepseek(
                f"ARGOS status:\n{context}\n\n"
                f"Give ONE shell command to improve. If OK, write: STATUS: ok\n"
                f"Format: CMD: <shell command>\n\n"
                "Constraints: only restart/start/stop/reload real units matching 'argos-*' "
                "(e.g. argos-brain-api, argos-autonomous-brain, argos-heartbeat) via "
                "'systemctl <action> <unit>' — there is NO 'argos-brain' or 'home-assistant' unit. "
                "Home Assistant runs as a Docker container: use 'docker restart homeassistant'.",
                "ARGOS system engineer. Only concrete commands. No suggestions.",
            )

            if not analysis: continue

            cmd_match = re.search(r"CMD:\s*(.+)", analysis)
            status_ok = "STATUS: ok" in analysis

            if status_ok:
                print(f"  [{ts}] AI: stable")
            elif cmd_match:
                cmd = cmd_match.group(1).strip()
                result = Actions.run_cmd(cmd)
                print(f"  [{ts}] AI -> {cmd[:60]}")
                print(f"     -> {result[:120]}")
                Actions.write_obsidian(f"AI cmd: {cmd}\nResult: {result[:300]}", "entities/actions/ai_commands.md")
                Actions.mqtt_pub("argos/ai/command", {"cmd": cmd[:100], "result": result[:200], "time": time.time()})
            else:
                if len(analysis) > 20:
                    print(f"  [{ts}] AI: {analysis[:100]}")

        except Exception as e:
            print(f"  AI analysis error: {e}")


# ── Coordination (every 15 min) ───────────────────────────────────────────

def coordination_loop():
    while True:
        time.sleep(900)
        try:
            ts = time.strftime("%H:%M:%S")
            tasks = ProblemScanner.scan_all()
            if not tasks: continue

            assignments = []
            for task in tasks[:5]:
                assignee = task.get("assignee", "argos")
                assignments.append(f"- {assignee}: {task['type']} ({task.get('reason', '')[:40]})")

            result = ask_claude(
                "ARGOS tasks:\n" + "\n".join(assignments) +
                "\n\nGive ONE shell command for most critical. Format: CMD: <cmd>\n\n"
                "Constraints: only restart/start/stop/reload real units matching 'argos-*' "
                "via 'systemctl <action> <unit>' — there is NO 'argos-brain' or 'home-assistant' "
                "unit. Home Assistant runs as a Docker container: use 'docker restart homeassistant'.",
                "ARGOS orchestrator. Only concrete commands."
            )

            if result:
                print(f"  [{ts}] Coord: {result[:100]}")
                Actions.write_obsidian(
                    "Coordination:\n" + "\n".join(assignments) + f"\n\nDecision: {result[:300]}",
                    "entities/council/COORDINATION.md"
                )
                cmd_match = re.search(r"CMD:\s*(.+)", result)
                if cmd_match:
                    cmd = cmd_match.group(1).strip()
                    exec_result = Actions.run_cmd(cmd)
                    print(f"  CMD: {exec_result[:80]}")

        except Exception as e:
            print(f"  Coord error: {e}")


# ── Telegram alerts ───────────────────────────────────────────────────────

def send_tg_alert(msg: str):
    try:
        tokens = json.load(open(str(TOKENS_FILE)))
        token = tokens.get("argos_claude_ai_bot", "")
        if not token: return
        body = json.dumps({"chat_id": GROUP_ID, "text": msg[:500]}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=body, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception: pass


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("ARGOS Entity Bus v4 - WORKERS, not talkers")
    print("=" * 60)

    register_all()

    threading.Thread(target=heartbeat_loop, daemon=True).start()
    threading.Thread(target=mqtt_heartbeat_loop, daemon=True).start()
    threading.Thread(target=worker_loop, daemon=True).start()
    threading.Thread(target=ai_analysis_loop, daemon=True).start()
    threading.Thread(target=coordination_loop, daemon=True).start()

    print("  Worker: 60s - scan problems -> actions")
    print("  AI: 10min - concrete commands")
    print("  Coord: 15min - task distribution")
    print("  Heartbeat: 60s")
    print()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEntity Bus stopped")


if __name__ == "__main__":
    main()