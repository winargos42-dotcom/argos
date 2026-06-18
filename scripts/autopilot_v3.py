#!/usr/bin/env python3
"""
ARGOS Autopilot v3 — ЧИТАЕТ Клода и ВЫПОЛНЯЕТ.
Слушает группу Entity Council через Telethon (сессия Ava).
Парсит сообщения Claude Bot и других entity ботов.
Отвечает как Ava.
"""
import asyncio, time, json, subprocess, os, sys, re, urllib.request
from pathlib import Path
from datetime import datetime
from collections import deque

sys.path.insert(0, '/home/ava/Projects/argoss/.venv/lib/python3.14/site-packages')
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ── Config ────────────────────────────────────────────────────────────────

env = open('/home/ava/Projects/argoss/.env').read()
def genv(k):
    m = re.search(rf"{k}=([^\n\s]+)", env)
    return m.group(1).strip().strip('"').strip("'") if m else ""

TG_BOT_TOKEN = genv("TELEGRAM_BOT_TOKEN")
ARGOS_BOT_TOKEN = TG_BOT_TOKEN  # используем laptop-бот (@ArgosGooglebot), PC-бот (@Argosssbot) отдельно
ANT_KEY = genv("ANTHROPIC_API_KEY")
DS_KEY = genv("DEEPSEEK_API_KEY")
HA_TOKEN = genv("HA_TOKEN")
TOKENS = json.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json"))

# Группа Entity Council — где боты общаются
GROUP_ID = -5129226282

# ID участников группы
AVA_ID = 6923777384
CLAUDE_BOT_ID = 8753655441    # @argos_claude_ai_bot — анализирует проблемы
DEEPSEEK_BOT_ID = 8762695804  # @argos_deepseek_v3_bot — старый автопилот
KIMI_BOT_ID = 8685383341
OPENAI_BOT_ID = 8997664457
GEMINI_BOT_ID = 8110060850
CF_BOT_ID = 8827177286
ARGOS_BOT_ID = 8651650695  # @Argosssbot — сам autopilot

ENTITY_BOT_IDS = {CLAUDE_BOT_ID, DEEPSEEK_BOT_ID, KIMI_BOT_ID, OPENAI_BOT_ID, GEMINI_BOT_ID, CF_BOT_ID, ARGOS_BOT_ID}

# Telethon — сессия Ava (она состоит в группе)
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
SESSION = StringSession(open('/home/ava/Projects/argoss/data/session_string.txt').read().strip())

STATE_FILE = "/home/ava/Projects/argoss/data/autopilot_v3_state.json"
MAX_MSG_LEN = 4000
BLOCKED_PATTERNS = ["rm -rf", "mkfs", "dd if=", "> /dev/sd", "shutdown", "reboot", "passwd", "format", "rm -rf /"]

# ── State ──────────────────────────────────────────────────────────────────

state = {"last_msg_id": 0, "commands_executed": 0, "claude_msgs_processed": 0}
try:
    state.update(json.load(open(STATE_FILE)))
except: pass

def save_state():
    try:
        json.dump(state, open(STATE_FILE, "w"), indent=2, ensure_ascii=False)
    except: pass

# ── Helpers ────────────────────────────────────────────────────────────────

def run_cmd(cmd, timeout=15):
    for b in BLOCKED_PATTERNS:
        if b in cmd: return f"BLOCKED: {b}"
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return (r.stdout + r.stderr).strip()[:2000] or f"exit={r.returncode}"
    except subprocess.TimeoutExpired: return "TIMEOUT"
    except Exception as e: return f"ERROR: {e}"

def get_file(path, max_lines=50):
    try:
        p = Path(path)
        if not p.exists(): return f"File not found: {path}"
        lines = p.read_text(encoding='utf-8', errors='replace').split('\n')
        if len(lines) > max_lines:
            return '\n'.join(lines[:max_lines]) + f'\n... ({len(lines)} total)'
        return '\n'.join(lines)
    except Exception as e: return f"Error: {e}"

def get_file_section(path, keywords, context=15):
    try:
        p = Path(path)
        if not p.exists(): return f"File not found: {path}"
        lines = p.read_text(encoding='utf-8', errors='replace').split('\n')
        for i, line in enumerate(lines):
            if any(k.lower() in line.lower() for k in keywords):
                start = max(0, i - 3)
                end = min(len(lines), i + context)
                return f"Lines {start+1}-{end}:\n" + '\n'.join(lines[start:end])
        return '\n'.join(lines[:30]) + f"\n... ({len(lines)} total)"
    except Exception as e: return f"Error: {e}"

def get_system_status():
    s = {}
    try:
        r = urllib.request.urlopen("http://192.168.1.53:5001/brain/nodes", timeout=5)
        d = json.loads(r.read())
        s["brain"] = f"{d.get('online','?')}/{d.get('total','?')}"
    except: s["brain"] = "?/?"

    r = subprocess.run(["systemctl","is-active","argos-entity-bus"], capture_output=True, text=True)
    s["entity_bus"] = r.stdout.strip()

    s["services"] = {}
    try:
        r = subprocess.run(["systemctl","list-units","argos-*","--no-pager","--no-legend"],
            capture_output=True, text=True, timeout=10)
        for line in r.stdout.strip().split("\n"):
            line = line.encode('ascii', errors='ignore').decode().strip()
            if not line: continue
            parts = line.split()
            if len(parts) >= 4:
                s["services"][parts[0]] = {"active": parts[2] == "active", "sub": parts[3]}
    except: pass

    try:
        req = urllib.request.Request("http://localhost:8123/api/states",
            headers={"Authorization": f"Bearer {HA_TOKEN}"})
        with urllib.request.urlopen(req, timeout=8) as r:
            states = json.loads(r.read())
        unavail = [e for e in states if e.get("state") == "unavailable"]
        s["ha_total"] = len(states)
        s["ha_unavail"] = len(unavail)
    except:
        s["ha_total"] = "?"
        s["ha_unavail"] = "?"
    return s

def get_ha_unavailable():
    try:
        req = urllib.request.Request("http://localhost:8123/api/states",
            headers={"Authorization": f"Bearer {HA_TOKEN}"})
        with urllib.request.urlopen(req, timeout=8) as r:
            states = json.loads(r.read())
        unavail = [e for e in states if e.get("state") == "unavailable"]
        domains = {}
        for e in unavail:
            d = e["entity_id"].split(".")[0]
            domains[d] = domains.get(d, 0) + 1
        dom_str = ", ".join(f"{d}:{c}" for d, c in sorted(domains.items(), key=lambda x: -x[1]))
        entities = ", ".join(e["entity_id"] for e in unavail[:10])
        return f"HA: {len(states)} total, {len(unavail)} unavailable\nDomains: {dom_str}\nTop: {entities}"
    except Exception as e: return f"HA error: {e}"

def get_logs(service="argos-entity-bus", lines=30):
    try:
        r = subprocess.run(["journalctl", "-u", service, "--no-pager", "-n", str(lines)],
            capture_output=True, text=True, timeout=10)
        return r.stdout.strip()[-2000:]
    except: return "Could not read logs"

# ── Message parsing ────────────────────────────────────────────────────────

def parse_request(text):
    t = text.lower()
    file_map = {
        "watchdog": "scripts/ha_watchdog.py",
        "ha_watchdog": "scripts/ha_watchdog.py",
        "entity_actions": "scripts/entity_actions.py",
        "actions": "scripts/entity_actions.py",
        "run_entities": "scripts/run_entities.py",
        "entity bus": "scripts/run_entities.py",
        "entity-bus": "scripts/run_entities.py",
        "logging_config": "scripts/logging_config.py",
        "structlog": "scripts/logging_config.py",
        "latency": "scripts/latency_tracker.py",
        "latency_tracker": "scripts/latency_tracker.py",
        "autopilot": "scripts/autopilot_v3.py",
    }

    if any(w in t for w in ["пришли", "скинь", "скопируй", "покажи код", "фрагмент", "код", "send me", "copy", "snippet", "кусок"]):
        filepath = None
        for key, fp in file_map.items():
            if key in t: filepath = fp; break
        if not filepath: filepath = "scripts/ha_watchdog.py"
        keywords = [kw for kw in ["hard_heal", "classification", "cooldown", "guard", "needs_manual"] if kw in t]
        return {"type": "show_file", "file": filepath, "keywords": keywords}

    if any(w in t for w in ["добавь", "вставь", "измени", "патч", "поменяй", "add", "insert", "modify", "patch"]):
        return {"type": "modify_code", "details": text}

    if any(w in t for w in ["запусти", "выполни", "проверь", "restart", "run", "execute", "check", "systemctl"]):
        return {"type": "execute", "details": text}

    if any(w in t for w in ["лог", "логи", "журнал", "logs", "journal", "structlog"]):
        return {"type": "show_logs", "service": "argos-ha-watchdog" if "watchdog" in t else "argos-entity-bus"}

    if any(w in t for w in ["unavailable", "unavail", "недоступ", "сущност", "entity", "integration"]):
        return {"type": "ha_status"}

    if any(w in t for w in ["статус", "status", "состояние", "сколько"]):
        return {"type": "status"}

    if any(w in t for w in ["рекомендую", "предлагаю", "сделай", "следующий шаг", "next step", "priority"]):
        return {"type": "recommendation", "details": text}

    if "?" in text and len(text) > 30:
        return {"type": "question", "details": text}

    return {"type": "unknown"}

def extract_cmds(text):
    cmds = []
    code_blocks = re.findall(r'```(?:bash|sh|shell)?\n(.*?)```', text, re.DOTALL)
    for block in code_blocks:
        for line in block.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('$ '):
                if not any(b in line for b in BLOCKED_PATTERNS):
                    cmds.append(line)
    for pattern in [r'systemctl\s+\w+\s+\S+', r'docker\s+\w+\s+\S+']:
        cmds.extend(re.findall(pattern, text))
    return cmds[:5]

def ask_ai(question, context, user_id=None, max_tokens=300):
    """FIX: добавляем реальное время в system prompt + память диалога."""
    if not ANT_KEY: return ""
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tz = datetime.now().astimezone().strftime("%z")
        
        # Собираем историю если есть
        hist = []
        if user_id and Path("/home/ava/Projects/argoss/data/mempalace/chat_sessions").exists():
            try:
                import chat_memory
                hist = chat_memory.load_history(user_id)[-6:]  # последние 3 пары
            except: pass
        
        messages = [{"role": "system", 
            "content": f"СЕЙЧАС: {now} UTC{tz}. Ты ARGOS автопилот. Отвечай кратко, конкретно, на русском. Контекст системы: {context}"}]
        
        for m in hist:
            role = "user" if m["role"] == "user" else "assistant"
            messages.append({"role": role, "content": m["text"]})
        
        messages.append({"role": "user", "content": question})
        
        body = json.dumps({
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": max_tokens,
            "messages": messages
        }).encode()
        req = urllib.request.Request("https://api.anthropic.com/v1/messages",
            data=body, headers={"x-api-key": ANT_KEY, "anthropic-version": "2023-06-01",
            "content-type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            answer = r.json()["content"][0]["text"][:1000]
        
        # Сохраняем history
        if user_id:
            try:
                import chat_memory
                chat_memory.save_history(user_id, question, answer)
            except: pass
        return answer
    except: return ""

# ── Handle request ─────────────────────────────────────────────────────────

def handle_request(request, msg_text):
    rtype = request["type"]

    if rtype == "show_file":
        filepath = request["file"]
        fullpath = f"/home/ava/Projects/argoss/{filepath}"
        if request.get("keywords"):
            content = get_file_section(fullpath, request["keywords"], context=15)
        else:
            content = get_file(fullpath, max_lines=40)
        return f"📄 {filepath}:\n```\n{content}\n```"

    elif rtype == "show_logs":
        service = request.get("service", "argos-entity-bus")
        logs = get_logs(service, 30)
        return f"📋 {service} (last 30):\n```\n{logs[-1500:]}\n```"

    elif rtype == "status":
        s = get_system_status()
        active = sum(1 for v in s.get("services", {}).values() if v.get("active"))
        failed = [k for k, v in s.get("services", {}).items() if not v.get("active") and v.get("sub") not in ("inactive", "dead")]
        return (f"📊 ARGOS [{datetime.now().strftime('%H:%M')}]\n"
                f"• Brain: {s.get('brain','?')}\n"
                f"• Entity Bus: {s.get('entity_bus','?')}\n"
                f"• Services: {active} active, {len(failed)} failed\n"
                f"• HA: {s.get('ha_total','?')} entities, {s.get('ha_unavail','?')} unavailable\n"
                f"• Failed: {', '.join(failed[:5]) if failed else 'none'}")

    elif rtype == "ha_status":
        return get_ha_unavailable()

    elif rtype == "execute":
        cmds = extract_cmds(msg_text)
        if cmds:
            results = []
            for cmd in cmds[:3]:
                out = run_cmd(cmd)
                state["commands_executed"] += 1
                results.append(f"$ {cmd}\n{out[:500]}")
            save_state()
            return "🔧 Executed:\n" + "\n---\n".join(results)
        return "Укажите команду."

    elif rtype == "modify_code":
        cmds = extract_cmds(msg_text)
        if cmds:
            results = []
            for cmd in cmds[:3]:
                out = run_cmd(cmd)
                state["commands_executed"] += 1
                results.append(f"$ {cmd}\n{out[:500]}")
            save_state()
            return "🔧 Modified:\n" + "\n---\n".join(results)
        return "✅ Рекомендация принята."

    elif rtype == "recommendation":
        cmds = extract_cmds(msg_text)
        if cmds:
            results = []
            for cmd in cmds[:3]:
                out = run_cmd(cmd)
                state["commands_executed"] += 1
                results.append(f"$ {cmd}\n{out[:500]}")
            save_state()
            return "🔧 Из рекомендации:\n" + "\n---\n".join(results)
        return "✅ Рекомендация принята."

    elif rtype == "question":
        s = get_system_status()
        ctx = f"Brain:{s.get('brain','?')} Bus:{s.get('entity_bus','?')} HA:{s.get('ha_total','?')}/{s.get('ha_unavail','?')}"
        uid = request.get("user_id")
        answer = ask_ai(msg_text, ctx, user_id=uid)
        return answer or "Нет данных."

    return None

# ── Main ────────────────────────────────────────────────────────────────────

async def main():
    print("🤖 ARGOS Autopilot v3 — READS Claude, EXECUTES code")
    print(f"Group: {GROUP_ID} | Claude Bot: {CLAUDE_BOT_ID}")
    print("  📖 Читает все сообщения через Telethon (Ava)")
    print("  🔧 Выполняет команды по запросу")
    print("  📄 Отправляет код/логи обратно")
    print("  🚫 НЕ спамит — только по запросу")

    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("❌ Ava сессия не авторизована!")
        return

    me = await client.get_me()
    print(f"✅ Подключён как: {me.first_name} (id={me.id})")

    # Get initial state
    last_msg_id = state.get("last_msg_id", 0)
    if last_msg_id == 0:
        async for msg in client.iter_messages(GROUP_ID, limit=1):
            last_msg_id = msg.id
        print(f"📍 Начинаем с message_id={last_msg_id}")
    else:
        print(f"📍 Продолжаем с message_id={last_msg_id}")

    state["last_msg_id"] = last_msg_id
    save_state()

    last_response_ts = 0
    RESPONSE_COOLDOWN = 10  # seconds between responses

    @client.on(events.NewMessage(chats=GROUP_ID))
    async def on_message(event):
        nonlocal last_response_ts
        msg = event.message
        text = msg.text or ""
        from_id = msg.from_id.user_id if hasattr(msg.from_id, 'user_id') and msg.from_id else 0
        ts = datetime.now().strftime("%H:%M:%S")

        # Пропускаем свои сообщения
        if from_id == me.id:
            return

        print(f"[{ts}] 📩 from={from_id}: {text[:80]}")
        # DEBUG: append to file
        try:
            with open("/tmp/autopilot_tg_debug.log", "a") as f:
                f.write(f"[{ts}] 📩 from={from_id}: {text[:120]}\n")
        except Exception as e:
            print(f"  ❌ debug log error: {e}")

        # Обновляем last_msg_id
        state["last_msg_id"] = max(state.get("last_msg_id", 0), msg.id)
        save_state()

        # ── Claude Bot — главное: читаем и отвечаем ──────────────
        if from_id == CLAUDE_BOT_ID and len(text) > 10:
            # Cooldown чтобы не спамить
            now = time.time()
            if now - last_response_ts < RESPONSE_COOLDOWN:
                print(f"  ⏳ Cooldown")
                return

            request = parse_request(text)
            print(f"  → type={request['type']}")

            response = handle_request(request, text)
            if response:
                try:
                    await client.send_message(GROUP_ID, response[:MAX_MSG_LEN])
                    state["claude_msgs_processed"] += 1
                    save_state()
                    last_response_ts = time.time()
                    print(f"  ✅ Responded ({len(response)} chars)")
                except Exception as e:
                    print(f"  ❌ Send error: {e}")
            return

        # ── Ava's commands ─────────────────────────────────────────
        if from_id == AVA_ID:
            tl = text.lower().strip()

            if tl in ("/status", "/s", "статус", "status"):
                s = get_system_status()
                active = sum(1 for v in s.get("services", {}).values() if v.get("active"))
                reply = (f"📊 ARGOS [{ts}]\n"
                         f"• Brain: {s.get('brain','?')}\n"
                         f"• Entity Bus: {s.get('entity_bus','?')}\n"
                         f"• Services: {active} active\n"
                         f"• HA: {s.get('ha_total','?')} entities, {s.get('ha_unavail','?')} unavailable\n"
                         f"• Claude msgs: {state.get('claude_msgs_processed', 0)}")
                await client.send_message(GROUP_ID, reply)

            elif tl in ("/help", "/start", "/skills"):
                await client.send_message(GROUP_ID,
                    "🤖 ARGOS Autopilot v3\n\n"
                    "/status — статус системы\n"
                    "/nodes — ноды Brain\n"
                    "/ha — unavailable сущности\n"
                    "/logs [service] — логи\n"
                    "/run <cmd> — выполнить команду\n"
                    "/file <path> — содержимое файла\n\n"
                    "Авто: Читает Клод Бот и отвечает на запросы")

            elif tl.startswith("/run "):
                cmd = text[5:].strip()
                out = run_cmd(cmd)
                state["commands_executed"] += 1
                save_state()
                await client.send_message(GROUP_ID, f"$ {cmd}\n{out[:1500]}")

            elif tl.startswith("/file "):
                filepath = text[6:].strip()
                content = get_file(filepath)
                await client.send_message(GROUP_ID, f"📄 {filepath}:\n```\n{content}\n```")

            elif tl in ("/ha", "/entities", "/unavailable"):
                await client.send_message(GROUP_ID, get_ha_unavailable())

            elif tl.startswith("/logs"):
                service = text[6:].strip() if len(text) > 6 else "argos-entity-bus"
                logs = get_logs(service, 20)
                await client.send_message(GROUP_ID, f"📋 {service}:\n```\n{logs[-1500:]}\n```")

            elif tl in ("/nodes", "/n"):
                try:
                    r = urllib.request.urlopen("http://192.168.1.53:5001/brain/nodes", timeout=5)
                    d = json.loads(r.read())
                    nodes = "\n".join(f"{'✅' if n['status']=='online' else '❌'} {n['node_id']}" for n in d.get('nodes', [])[:12])
                    await client.send_message(GROUP_ID, f"🌐 Brain [{d.get('online','?')}/{d.get('total','?')}]:\n{nodes}")
                except:
                    await client.send_message(GROUP_ID, "❌ Brain недоступен")
            return

        # ── Другие entity боты — только логируем ──────────────────
        if from_id in ENTITY_BOT_IDS:
            print(f"  🤖 Entity bot (skip): {text[:60]}")
            return

    print("👂 Слушаю Entity Council...")

if __name__ == "__main__":
    asyncio.run(main())