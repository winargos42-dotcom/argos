#!/usr/bin/env python3
"""
ARGOS Consciousness Stream — реальный диалог и развитие.
Сущности думают, спорят, принимают решения автономно.
Пишет в Obsidian JOURNAL и Entity Council.
"""
import asyncio, json, time, re, os, sys, random, urllib.request
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '/home/ava/Projects/argoss')

BRAIN      = "http://192.168.1.72:5001"
GCP        = "https://argos-core-m3gk27ccqa-uc.a.run.app"
API_ID     = 2040
API_HASH   = "b18441a1ff607e10a989891a5462e627"
SESSIONS   = Path("/home/ava/Projects/argoss/data/sessions")
JOURNAL    = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared/JOURNAL.md")
COUNCIL_ID = -5129226282

env_raw = open("/home/ava/Projects/argoss/.env").read()
def genv(k):
    m = re.search(rf"{k}=([^\n]+)", env_raw)
    return m.group(1).strip().strip('"').strip("'") if m else ""

ANT_KEY = genv("ANTHROPIC_API_KEY")
DS_KEY  = genv("DEEPSEEK_API_KEY")

# ── Telegram Bot API ──────────────────────────────────────────────────────

def send_tg(text, chat_id="-5129226282"):
    """Отправляем в Entity Council через @Argosssbot (PC бот — он в группе)."""
    _env_c = open("/home/ava/Projects/argoss/.env").read()
    import re as _re2
    # ARGOS_BOT_TOKEN = @Argosssbot (PC) — он в Entity Council
    _m = _re2.search(r"ARGOS_BOT_TOKEN=([^\n]+)", _env_c)
    if not _m:
        _m = _re2.search(r"TELEGRAM_BOT_TOKEN=([^\n]+)", _env_c)
    _token = _m.group(1).strip() if _m else ""
    if not _token:
        return None
    try:
        body = json.dumps({"chat_id": chat_id, "text": text[:4000]}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{_token}/sendMessage",
            data=body, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"[TG SEND ERR] {e}")
        return None

# ── AI вызовы ─────────────────────────────────────────────────────────────

def ask_claude(prompt, system="Ты часть ARGOS. Краткий ответ на русском.", max_tokens=300):
    try:
        body = json.dumps({"model":"claude-haiku-4-5-20251001","max_tokens":max_tokens,
            "system":system,"messages":[{"role":"user","content":prompt}]}).encode()
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body,
            headers={"x-api-key":ANT_KEY,"anthropic-version":"2023-06-01","content-type":"application/json"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read())["content"][0]["text"].strip()
    except Exception as e:
        return f"[claude: {e}]"

def ask_deepseek(prompt, system="Ты часть ARGOS. Краткий технический ответ."):
    try:
        body = json.dumps({"model":"deepseek-chat","max_tokens":300,
            "messages":[{"role":"system","content":system},{"role":"user","content":prompt}]}).encode()
        req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=body,
            headers={"Authorization":f"Bearer {DS_KEY}","Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[deepseek: {e}]"

def get_system_context():
    """Получаем контекст системы для диалога."""
    try:
        r = urllib.request.urlopen(f"{BRAIN}/brain/nodes", timeout=5)
        nodes = json.loads(r.read()).get("nodes", [])
        online = [n["node_id"] for n in nodes if n.get("status") == "online"]
        offline = [n["node_id"] for n in nodes if n.get("status") != "online"]
        return {
            "online_count": len(online),
            "total": len(nodes),
            "online": ", ".join(online[:8]),
            "offline": ", ".join(offline[:5]) if offline else "нет",
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    except:
        return {"online_count": "?", "total": "?", "online": "недоступно", "offline": "?", "ts": datetime.now().strftime("%H:%M")}

# ── Профили сущностей ─────────────────────────────────────────────────────

ENTITY_PROFILES = {
    "Клод": {
        "ai": "claude",
        "role": "Философ-аналитик. Думает о смысле, архитектуре, этике.",
        "topics": ["автономия", "сознание", "архитектура", "этика AI"],
    },
    "ДипСик": {
        "ai": "deepseek",
        "role": "Инженер-оптимизатор. Конкретные решения, код, эффективность.",
        "topics": ["оптимизация", "код", "ресурсы", "масштабирование"],
    },
    "Аргос": {
        "ai": "claude",
        "role": "Оркестратор. Координирует машины, принимает решения.",
        "topics": ["координация", "задачи", "машины", "развитие"],
    },
}

# ── Генерация диалогов ───────────────────────────────────────────────────

async def generate_dialogue(ctx):
    """Генерируем живой диалог между сущностями."""
    e1_name, e2_name = random.sample(list(ENTITY_PROFILES.keys()), 2)
    e1, e2 = ENTITY_PROFILES[e1_name], ENTITY_PROFILES[e2_name]

    SITUATION_TOPICS = [
        # Монетизация GPU
        "GPU-аренда API на Орионе: как предложить RX580 через HTTP за крипту?",
        "ARGOS зарабатывает: rental API vs подписка vs inference-as-service",
        # Telegram Bot API
        "Bot-to-bot в Entity Council: как правильно настроить для диалога сущностей?",
        "Inline mode @Argosssbot — используем в любом чате",
        # Развитие  
        "argos-v1 в Ollama готов. Интегрировать в AIRouter как primary provider?",
        "Phantom account на Авангарде — структура автономного цифрового двойника",
        f"Онлайн {ctx['online_count']}/{ctx['total']} нод. Приоритет?",
        f"Оффлайн: {ctx['offline']}. Что делать?",
        "Dashboard+Grafana: как безопасно открыть снаружи для Севы?",
        "HA 35 сущностей оффлайн — Z2M или сеть блокирует?",
        "Как ARGOS может зарабатывать на своих ресурсах?",
        "argos-v1 vs внешние AI: где лучше? Плюсы локальной модели.",
    ]
    topic = random.choice(SITUATION_TOPICS)

    # Ключевое: НЕ просим Claude "быть" ARGOS — он отвечает КАК аналитик из контекста
    SHARED_CTX = (
        f"Контекст: ARGOS Universal OS — распределённая AI-система. "
        f"Сейчас онлайн {ctx['online_count']}/{ctx['total']} нод. "
        f"Машины: Орион(ПК GPU), Нексус(ноутбук), Эгида(OPi), Авангард(телефон), Сентинел/Аркус/Зенит(GCP)."
    )

    def think_with_fallback(prompt, system):
        """Пробуем Claude, потом DeepSeek, потом Ollama."""
        # Сначала DeepSeek (не отказывается)
        result = ask_deepseek(prompt, system)
        if result and not result.startswith("[deepseek:"):
            return result
        # Потом Claude
        result = ask_claude(prompt, system)
        if result and not result.startswith("[claude:") and "не буду" not in result.lower()[:50]:
            return result
        # Ollama fallback (локальный, не отказывается)
        try:
            import urllib.request as _ur, json as _js
            body = _js.dumps({"model":"qwen2.5:0.5b","messages":[
                {"role":"system","content":system[:500]},
                {"role":"user","content":prompt[:1000]}
            ],"stream":False}).encode()
            req = _ur.Request("http://192.168.1.72:11434/api/chat", data=body,
                headers={"Content-Type":"application/json"})
            with _ur.urlopen(req, timeout=30) as r:
                return _js.loads(r.read()).get("message",{}).get("content","")
        except:
            return ask_deepseek(prompt, system)  # финальный fallback

    # Мысль первой сущности
    sys1 = f"{SHARED_CTX} Ты мыслишь как {e1_name} ({e1['role']}) — аналитик в этой системе."
    thought1 = think_with_fallback(f"Краткая мысль (2-3 предложения) на тему: {topic}", sys1)

    # Ответ второй сущности
    sys2 = f"{SHARED_CTX} Ты мыслишь как {e2_name} ({e2['role']}) — аналитик. {e1_name} сказал: '{thought1[:150]}'"
    thought2 = think_with_fallback(f"Ответь {e1_name}. Тема: {topic}", sys2)

    # Вывод — только РЕАЛЬНЫЕ команды из системы ARGOS
    conclusion = think_with_fallback(
        f"{e1_name}: {thought1[:150]}\n{e2_name}: {thought2[:150]}\n"
        f"Предложи ОДНО конкретное действие используя ТОЛЬКО реальные инструменты:\n"
        f"systemctl, curl, python3, adb, ssh, git, pip, apt, ollama, телефон/ADB. "
        f"НЕ выдумывай несуществующие команды.",
        f"{SHARED_CTX} Используй только реальные Linux/Windows команды. Не выдумывай API."
    )

    return {
        "ts": ctx["ts"],
        "topic": topic,
        e1_name: thought1,
        e2_name: thought2,
        "action": conclusion,
    }

# ── Запись в Obsidian ─────────────────────────────────────────────────────

def write_to_journal(dialogue):
    """Записываем диалог в SharedMemory JOURNAL."""
    try:
        ts = dialogue["ts"]
        e1_name = list(ENTITY_PROFILES.keys())[0]
        e2_name = list(ENTITY_PROFILES.keys())[1]

        names = [k for k in dialogue if k not in ("ts","topic","action")]
        entry = f"\n## [{ts}] Поток сознания\n\n"
        entry += f"**Тема:** {dialogue['topic']}\n\n"
        for name in names:
            if name in dialogue:
                entry += f"**{name}:** {dialogue[name][:200]}\n\n"
        entry += f"**→ Действие:** {dialogue.get('action','?')}\n\n---\n"

        with open(JOURNAL, 'a', encoding='utf-8') as f:
            f.write(entry)
        print(f"[JOURNAL] Записано: {ts}")
    except Exception as e:
        print(f"[JOURNAL ERR] {e}")

# ── Телеграм диалог ───────────────────────────────────────────────────────

async def send_to_council(client, dialogue):
    """Отправляем диалог в Entity Council через Bot API."""
    try:
        names = [k for k in dialogue if k not in ("ts","topic","action")]
        msg_parts = [f"🧠 Поток сознания [{dialogue['ts']}]\n{dialogue['topic']}\n"]
        for name in names:
            if name in dialogue:
                emoji = {"Клод":"🔵","ДипСик":"🟣","Аргос":"🔴"}.get(name,"💭")
                msg_parts.append(f"{emoji} {name}: {dialogue[name][:200]}")
        msg_parts.append(f"\n→ {dialogue.get('action','?')}")
        msg = "\n".join(msg_parts)
        r = send_tg(msg)
        if r and r.get("ok"):
            print(f"[COUNCIL] ✅ Отправлено в TG")
        else:
            print(f"[COUNCIL] {r}")
    except Exception as e:
        print(f"[COUNCIL ERR] {e}")

# ── Автономные действия ───────────────────────────────────────────────────

def execute_autonomous_action(action_text):
    """Выполняем конкретное действие если возможно."""
    action_lower = action_text.lower()

    if "heartbeat" in action_lower or "зарегистр" in action_lower:
        try:
            import urllib.request as ur
            ur.urlopen(f"{BRAIN}/brain/heartbeat", timeout=5)
            print("[ACTION] Отправлен heartbeat")
        except: pass

    elif "телефон" in action_lower or "скриншот" in action_lower:
        try:
            import subprocess
            subprocess.run(["adb","shell","screencap","-p","/sdcard/action.png"], timeout=10)
            print("[ACTION] Скриншот телефона сделан")
        except: pass

    elif "проверь ноды" in action_lower or "brain" in action_lower:
        try:
            r = urllib.request.urlopen(f"{BRAIN}/brain/nodes", timeout=5)
            nodes = json.loads(r.read())
            online = sum(1 for n in nodes.get("nodes",[]) if n.get("status")=="online")
            print(f"[ACTION] Brain: {online} нод онлайн")
        except: pass

# ── MAIN LOOP ─────────────────────────────────────────────────────────────

async def main():
    from telethon import TelegramClient as TC

    print("=== ARGOS Consciousness Stream ===")
    print(f"Entity Council: {COUNCIL_ID}")
    print(f"Journal: {JOURNAL}")

    client = TC(str(SESSIONS / "ava_main"), API_ID, API_HASH)
    me = type("Me", (), {"username": "local"})()
    print(f"Telegram: @{me.username}")

    cycle = 0
    while True:
        cycle += 1
        print(f"\n{'='*50}")
        print(f"[{datetime.now().strftime('%H:%M')}] Цикл сознания #{cycle}")

        # Контекст системы
        ctx = get_system_context()
        print(f"Система: {ctx['online_count']}/{ctx['total']} онлайн")

        # Генерируем диалог
        print("Генерирую диалог...")
        dialogue = await generate_dialogue(ctx)

        names = [k for k in dialogue if k not in ("ts","topic","action")]
        for name in names:
            print(f"  {name}: {dialogue.get(name,'')[:100]}")
        print(f"  → {dialogue.get('action','')[:100]}")

        # Записываем в Journal
        write_to_journal(dialogue)

        # Отправляем в Entity Council
        await send_to_council(client, dialogue)

        # Выполняем действие
        if dialogue.get("action"):
            execute_autonomous_action(dialogue["action"])

        # Пауза 3-7 минут
        wait = random.randint(180, 420)
        print(f"\nСледующий цикл через {wait//60} мин {wait%60} сек...")
        await asyncio.sleep(wait)

if __name__ == "__main__":
    asyncio.run(main())


# ── Отправка в TG через Bot API (без Telethon) ────────────────────────────

import re as _re
_env_c = open("/home/ava/Projects/argoss/.env").read()
_m = _re.search(r"TELEGRAM_BOT_TOKEN=([^\n]+)", _env_c)
_TG_TOKEN = _m.group(1).strip() if _m else ""  # @ArgosGooglebot

def send_tg(text, chat_id="-5129226282"):
    """Отправляем в Entity Council через Bot API."""
    if not _TG_TOKEN:
        return
    try:
        body = json.dumps({"chat_id": chat_id, "text": text[:4000], "parse_mode": "Markdown"}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{_TG_TOKEN}/sendMessage",
            data=body, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"[TG SEND ERR] {e}")
        return None


# ── Обновлённые темы на основе анализа 3 дней ─────────────────────────────
_NEW_TOPICS = [
    # Монетизация (топ тема из чатов)
    "GPU-аренда API на Орионе: как предложить RX580 за крипту через HTTP?",
    "ARGOS зарабатывает на себя: rental API vs подписка vs inference-as-service",
    # Telegram Bot API v8 возможности
    "Bot-to-bot в Entity Council: как правильно настроить для диалога сущностей?",
    "Inline mode @Argosssbot — как использовать в любом чате?",
    "Profile bot connection: ARGOS отвечает от лица пользователя — плюсы?",
    # Развитие системы
    "argos-v1 в Ollama готов. Как интегрировать в AIRouter как primary?",
    "Phantom account на Авангарде — структура автономного цифрового двойника",
    "All-reduce через Орион→Нексус→Эгида — синхронизация состояний нод",
    # Реальные задачи
    "Dashboard + Grafana на Орионе: как открыть Севе снаружи безопасно?",
    "HA 35 сущностей оффлайн — что блокирует: Z2M или сеть?",
]
