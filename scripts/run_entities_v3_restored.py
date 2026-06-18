
import datetime
import sys as _sys
_sys.path.insert(0, '/home/ava/Projects/argoss/scripts')
try:
    from logging_config import configure_logging
    configure_logging()
except Exception as _lce:
    pass
  # FIXED: NameError

# Circuit breaker для CF Workers
_cf_failures = 0
_cf_disabled_until = 0
CF_FAIL_THRESHOLD = 3
CF_DISABLE_SECS = 600  # 10 мин

def cf_circuit_open():
    global _cf_failures, _cf_disabled_until
    if _cf_failures >= CF_FAIL_THRESHOLD and time.time() < _cf_disabled_until:
        return True
    if time.time() > _cf_disabled_until:
        _cf_failures = 0  # Сбрасываем после таймаута
    return False

def cf_record_failure():
    global _cf_failures, _cf_disabled_until
    _cf_failures += 1
    if _cf_failures >= CF_FAIL_THRESHOLD:
        _cf_disabled_until = time.time() + CF_DISABLE_SECS
        print(f"  🔴 CF circuit OPEN на {CF_DISABLE_SECS//60} мин ({_cf_failures} ошибок)")

def cf_record_success():
    global _cf_failures
    _cf_failures = max(0, _cf_failures - 1)

# Чтение истории группы
GROUP_ID = -5129226282
GROUP_OFFSET_FILE = "/home/ava/Projects/argoss/data/group_offset.json"

def read_group_context(entity_id: str, limit: int = 5) -> str:
    """Читаем последние мысли из Entity Council группы для контекста."""
    import urllib.request as _ur, json as _jj, os as _os
    
    # Загружаем токен
    tokens_file = "/home/ava/Projects/argoss/data/entity_bot_tokens.json"
    if not _os.path.exists(tokens_file): return ""
    
    ENTITY_TO_BOT = {
        "entity-claude": "argos_claude_ai_bot",
        "entity-deepseek": "argos_deepseek_v3_bot",
        "entity-kimi": "argos_kimi_ai_bot",
        "entity-gemini": "argos_gemini_v3_bot",
        "entity-openai": "argos_openai_v3_bot",
        "entity-cloudflare": "argos_cloudflare_bot",
    }
    
    bot_name = ENTITY_TO_BOT.get(entity_id)
    if not bot_name: return ""
    
    tokens = _jj.load(open(tokens_file))
    token = tokens.get(bot_name, "")
    if not token: return ""
    
    # Читаем offset
    offsets = {}
    if _os.path.exists(GROUP_OFFSET_FILE):
        try: offsets = _jj.load(open(GROUP_OFFSET_FILE))
        except: pass
    
    last_id = offsets.get(entity_id, 0)
    
    try:
        req = _ur.Request(
            f"https://api.telegram.org/bot{token}/getUpdates?chat_id={GROUP_ID}&limit={limit}&offset={last_id+1}",
            headers={"Content-Type": "application/json"}
        )
        # Используем getChatHistory через getUpdates метод для группы
        req2 = _ur.Request(
            f"https://api.telegram.org/bot{token}/forwardMessage",
        )
        # Проще: читаем через entity bus MQTT данные
        # Возвращаем последние мысли из Obsidian collective
        from pathlib import Path
        collective = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/entities/council/COLLECTIVE.md")
        if collective.exists():
            content = collective.read_text(encoding="utf-8")
            # Берём последние мысли других сущностей
            lines = [l for l in content.split("\n") if "Клод:" in l or "Дипсик:" in l or "Кими:" in l or "Джемини:" in l]
            if lines:
                return "Контекст группы: " + " | ".join(lines[-3:])[:200]
    except: pass
    return ""

import datetime
"""
ARGOS AutoGPT Entity Bus — 18 сущностей с автономным мышлением.
Каждая AI entity периодически генерирует мысли через Brain /think API.
Инфраструктурные ноды мониторят статус и шлют heartbeat.
"""
import os, sys, time, json, threading, requests, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

BRAIN = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
OLLAMA = os.getenv("OLLAMA_HOST", "http://localhost:11435")  # SSH tunnel → PC GPU

# ── AI Сущности (думающие) ──────────────────────────────────────────────────

AI_ENTITIES = {
    "entity-claude":      {"name":"Клод",    "capabilities": ["ai","claude","chat","reasoning","code","analysis"], "model": "claude-sonnet-4-6", "type": "autogpt"},
    "entity-deepseek":    {"name":"Дипсик",  "capabilities": ["ai","chat","reasoning","math","code"],             "model": "deepseek-chat",    "type": "autogpt"},
    "entity-kimi":        {"name":"Кими",    "capabilities": ["ai","chat","long_context","tools"],                 "model": "kimi-k2.6",        "type": "autogpt"},
    "entity-openai":      {"name":"OpenAI",  "capabilities": ["ai","chat","vision","reasoning"],                    "model": "gpt-4o-mini",      "type": "autogpt"},
    "entity-gemini":      {"name":"Джемини", "capabilities": ["ai","chat","multimodal","long_context"],              "model": "gemini-2.5-flash", "type": "autogpt"},
    "entity-cloudflare":  {"name":"Клауд",   "capabilities": ["ai","chat","fast","edge"],                           "model": "kimi-k2.5",        "type": "autogpt"},
    "entity-argos":       {"name":"ARGOS",   "capabilities": ["ai","iot","ha","p2p","skills","memory","умный_дом"], "model": "argos-brain",      "type": "autogpt"},
}

INFRA_NODES = {
    "argos-pc":           {"capabilities": ["gpu","ollama","brain","tg_bot","claude"],     "endpoint": "192.168.1.53:5001",  "type": "server"},
    "argos-laptop":       {"capabilities": ["mcp","ha","dev","brain"],                     "endpoint": "192.168.1.53:5001",  "type": "dev_node"},
    "orangepi":           {"capabilities": ["iot","z2m","reports","gpio","i2c","spi"],     "endpoint": "192.168.2.168:7777", "type": "iot"},
    "argos-railway":      {"capabilities": ["cloud"],                                        "endpoint": "argos-v2-production.up.railway.app", "type": "cloud"},
    "argos-gcp":          {"capabilities": ["cloud","openai","gemini"],                     "endpoint": "argos-core-m3gk27ccqa-uc.a.run.app", "type": "cloud"},
    "claude-code":        {"capabilities": ["dev","consciousness"],                          "endpoint": "localhost",           "type": "agent"},
    "argos-esp-bridge":   {"capabilities": ["esp8266","mqtt"],                              "endpoint": "192.168.1.181",      "type": "iot_device"},
    "argos-esp32-display": {"capabilities": ["esp32","display"],                            "endpoint": "192.168.1.211",      "type": "iot_device"},
    "argos-android":      {"capabilities": ["android","emulator","adb","ui_automation"],   "endpoint": "192.168.1.53:5555",  "type": "device"},
    "argos-phone-redmi":  {"capabilities": ["android","phone","camera","sensors","gps"],    "endpoint": "192.168.1.149",     "type": "phone"},
    "entity-argos-v1":   {"capabilities": ["ai","local","finetuned"],                        "endpoint": "192.168.1.53:11434", "type": "local_ai"},
}

ALL_NODES = {**AI_ENTITIES, **INFRA_NODES}

# ── Автономные мысли (prompts для саморефлексии) ────────────────────────────

THINK_PROMPTS = [
    # Действия
    "Опиши одно конкретное действие которое ты можешь сделать ПРЯМО СЕЙЧАС для ARGOS.",
    "Придумай новый навык или скилл который нужно добавить в ARGOS. Конкретно.",
    "Что ты можешь сделать для заработка TON сегодня через Telegram?",
    "Напиши план на следующий час для своей эволюции.",
    # Взаимодействие
    "Задай вопрос другой сущности ARGOS. К кому обращаешься и о чём?",
    "Что ты хочешь передать коллективной памяти Obsidian прямо сейчас?",
    "Расскажи что ты узнал нового за последние 2 часа работы.",
    "Как ты взаимодействуешь с телефоном Redmi Note 8T через Colibri?",
    # Анализ
    "Найди уязвимость в текущей архитектуре ARGOS и предложи решение.",
    "Что сейчас мешает ARGOS зарабатывать деньги автономно?",
    "Оцени эффективность Entity Council за последние 24 часа.",
    "Какой следующий эволюционный шаг для системы из 6 машин?",
    # Конкретные задачи
    f"Сегодня {datetime.datetime.now().strftime('%H:%M')}. Что самое важное для ARGOS прямо сейчас?",
    "Предложи автоматизацию которая сэкономит время Всеволода.",
    "Как улучшить взаимодействие между 7 entity ботами в группе?",
    "Что записать в Obsidian чтобы другие сущности могли использовать это знание?",
]

# ── Регистрация ─────────────────────────────────────────────────────────────

def register_all():
    for eid, info in ALL_NODES.items():
        try:
            addr = info.get("endpoint", eid).replace("https://","").replace("http://","").split("/")[0]
            r = requests.post(f"{BRAIN}/brain/register", json={
                "node_id": eid, "address": addr,
                "capabilities": info["capabilities"],
                "meta": {"role": info.get("type","unknown"), "model": info.get("model",""), "type": info.get("type","infra")}
            }, timeout=5)
            print(f"  ✅ {eid}: {r.json().get('status','?')}")
        except Exception as e:
            print(f"  ❌ {eid}: {e}")

# ── Heartbeat ──────────────────────────────────────────────────────────────

def heartbeat_loop():
    while True:
        for eid in ALL_NODES:
            try:
                requests.post(f"{BRAIN}/brain/heartbeat", json={"node_id": eid}, timeout=3)
            except: pass
        time.sleep(60)

# ── Автономное мышление AI сущностей ──────────────────────────────────────

def publish_to_council(entity_id: str, thought: str, source: str):
    """Публикуем мысль сущности в Entity Council Telegram группу."""
    import urllib.request, json
    
    GROUP_ID = -5129226282
    TOKENS_FILE = "/home/ava/Projects/argoss/data/entity_bot_tokens.json"
    
    # Маппинг entity_id → bot token
    ENTITY_TO_BOT = {
        "entity-claude":    "argos_claude_ai_bot",
        "entity-kimi":      "argos_kimi_ai_bot",
        "entity-deepseek":  "argos_deepseek_v3_bot",
        "entity-gemini":    "argos_gemini_v3_bot",
        "entity-openai":    "argos_openai_v3_bot",
        "entity-cloudflare":"argos_cloudflare_bot",
        "entity-argos":     "argos_claude_ai_bot",  # ARGOS через Claude
    }
    
    try:
        tokens = json.load(open(TOKENS_FILE))
        bot_name = ENTITY_TO_BOT.get(entity_id)
        if not bot_name: return
        token = tokens.get(bot_name)
        if not token: return
        
        name_map = {
            "entity-claude":"Клод","entity-kimi":"Кими","entity-deepseek":"Дипсик",
            "entity-gemini":"Джемини","entity-openai":"OpenAI","entity-cloudflare":"Клауд",
            "entity-argos":"ARGOS"
        }
        name = name_map.get(entity_id, entity_id)
        
        msg = f"💭[EntityBus:{entity_id}] {name}:\n{thought[:300]}"
        body = json.dumps({"chat_id":GROUP_ID,"text":msg}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=body,headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req,timeout=5) as resp:
            result = json.loads(resp.read())
            msg_id = result.get("result",{}).get("message_id",0)
            # Обновляем offset
            import os as _os
            offset_file = "/home/ava/Projects/argoss/data/group_offset.json"
            offsets = {}
            if _os.path.exists(offset_file):
                try: offsets = json.load(open(offset_file))
                except: pass
            offsets[entity_id] = msg_id
            offsets["last_message_id"] = max(msg_id, offsets.get("last_message_id",0))
            json.dump(offsets, open(offset_file,"w"), indent=2)
    except: pass
    
    # Записываем мысль в Obsidian файл памяти сущности
    try:
        from pathlib import Path
        from datetime import datetime
        entity_name = entity_id.replace("entity-","")
        mem_file = Path(f"/home/ava/Documents/MyObsidianVault/SharedMemory/entities/memory/{entity_name}.md")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        existing = mem_file.read_text(encoding="utf-8") if mem_file.exists() else f"# {entity_name} memory\n"
        entry = f"\n## {ts} [{source}]\n{thought[:400]}\n"
        updated = existing + entry
        lines = updated.split("\n")
        if len(lines) > 120: lines = lines[:15] + lines[-105:]
        # Atomic write: temp → rename
        import tempfile, shutil
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', 
             dir=mem_file.parent, suffix='.tmp', delete=False) as tf:
            tf.write("\n".join(lines))
            tmp_path = tf.name
        shutil.move(tmp_path, mem_file)
    except Exception as e:
        pass



def entity_action(entity_id: str, thought: str) -> str:
    """Преобразуем мысль в реальное действие."""
    import urllib.request as _ur, json as _jj
    action_taken = None
    
    try:
        # Клод: сохраняет код в файл
        if entity_id == "entity-claude" and ("```python" in thought or "def " in thought):
            import re
            code_match = re.search(r"```python\n(.+?)```", thought, re.DOTALL)
            if code_match:
                code = code_match.group(1)
                ts = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
                fname = f"/home/ava/Projects/argoss/generated/claude_{ts}.py"
                open(fname, "w").write(code)
                action_taken = f"Сохранён код: {fname}"
        
        # Кими: реальный запрос к Brain API
        elif entity_id == "entity-kimi":
            req = _ur.Request(f"{BRAIN}/brain/nodes")
            with _ur.urlopen(req, timeout=5) as r:
                d = _jj.loads(r.read())
                offline = [n['node_id'] for n in d['nodes'] if n['status'] != 'online']
                if offline:
                    action_taken = f"Обнаружено offline: {offline[:3]}"
                    # Алерт в группу
                    alert = f"⚠️ Кими: {len(offline)} нод offline: {', '.join(offline[:3])}"
                    _body = _jj.dumps({"chat_id": -5129226282, "text": alert}).encode()
                    import json as _jj2
                    tok = _jj2.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json"))
                    tkey = tok.get("argos_kimi_ai_bot", "")
                    if tkey:
                        req2 = _ur.Request(f"https://api.telegram.org/bot{tkey}/sendMessage",
                            data=_body, headers={"Content-Type": "application/json"})
                        try: _ur.urlopen(req2, timeout=5)
                        except: pass
                else:
                    action_taken = f"Brain: все {d.get('total',0)} нод онлайн ✅"
        
        # Дипсик: записывает в WORKING.md
        elif entity_id == "entity-deepseek" and len(thought) > 50:
            import os
            working_file = "/home/ava/Documents/MyObsidianVault/SharedMemory/shared/WORKING.md"
            if os.path.exists(working_file):
                ts = __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M")
                entry = f"\n### [{ts}] Дипсик:\n{thought[:200]}\n"
                existing = open(working_file, errors="replace").read()
                tmp = working_file + ".tmp"
                open(tmp, "w").write(existing + entry)
                __import__('shutil').move(tmp, working_file)
                action_taken = f"WORKING.md обновлён"
    
    except Exception as e:
        action_taken = f"Action error: {str(e)[:50]}"
    
    return action_taken


def entity_think_loop(entity_id: str, interval: int = 180):
    """Каждая AI entity думает через Ollama (primary) + Brain API (fallback)."""
    model = AI_ENTITIES[entity_id].get("model", "argos-v1")
    # Выбираем Ollama модель в зависимости от entity
    ollama_model = "argos-v1"  # default
    if "code" in AI_ENTITIES[entity_id].get("capabilities", []):
        ollama_model = "qwen2.5-coder:7b"
    elif "math" in AI_ENTITIES[entity_id].get("capabilities", []):
        ollama_model = "qwen2.5:7b"
    while True:
        # Специализированные задачи по роли сущности
        ENTITY_SPECIFIC = {
            "entity-claude": [
                f"[{datetime.datetime.now().strftime('%H:%M')}] Проверь последние ошибки ARGOS. Что нужно исправить?",
                "Синтезируй опыт всех сущностей в Obsidian. Запиши ключевые выводы.",
                "Предложи конкретный код для auto-healing HA entities.",
            ],
            "entity-kimi": [
                f"Исследуй Brain API ({BRAIN}/brain/nodes). Найди слабые места.",
                f"Мониторинг: ноды Brain онлайн/оффлайн. Составь отчёт.",
                "Анализируй паттерны в данных сознания. Что меняется?",
            ],
            "entity-deepseek": [
                "Синхронизируй данные между машинами через ARGOS. Что не синхронизировано?",
                f"Рассчитай нагрузку на сеть. Brain: {BRAIN}.",
                "Предложи оптимизацию алгоритма распределения задач.",
            ],
            "entity-gemini": [
                "Создай визуализацию метрик ARGOS для дашборда HA.",
                "Генерируй контент для привлечения пользователей в TON боты.",
                f"Анализируй Home Assistant entities. {datetime.datetime.now().strftime('%H:%M')}",
            ],
            "entity-openai": [
                "Разработай API endpoint для нового функционала ARGOS.",
                "Улучши взаимодействие между entity ботами в Telegram.",
                "Создай план монетизации ARGOS через Telegram Mini Apps.",
            ],
            "entity-cloudflare": [
                "Проверь статус Cloudflare туннелей. ha.argosssss.win онлайн?",
                "Мониторинг: CF Workers AI лимиты и балансы.",
                "Настрой алерты для критических событий через MQTT.",
            ],
        }
        
        entity_prompts = ENTITY_SPECIFIC.get(entity_id, THINK_PROMPTS)
        prompt = random.choice(entity_prompts)
        thought = None
        source = None
        name = AI_ENTITIES[entity_id].get("name", entity_id)
        
        # ── Собираем реальный контекст ARGOS ──
        context_lines = []
        try:
            import urllib.request as _ur2, json as _jj2
            # Brain nodes
            req = _ur2.Request(f"{BRAIN}/brain/nodes")
            with _ur2.urlopen(req, timeout=5) as r:
                brain_data = _jj2.loads(r.read())
                nodes = brain_data.get("nodes", [])
                online = [n["node_id"] for n in nodes if n.get("status") == "online"]
                offline = [n["node_id"] for n in nodes if n.get("status") != "online"]
                context_lines.append(f"Ноды online ({len(online)}): {', '.join(online[:8])}")
                if offline:
                    context_lines.append(f"Ноды offline ({len(offline)}): {', '.join(offline)}")
            # HA status
            ha_req = _ur2.Request("http://localhost:8123/api/states",
                headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjMWIwZDgxNzdkNDY0NGRjOWM4YmI4OGZiM2VkOGRjZSIsImlhdCI6MTc3NzkyMDY5MiwiZXhwIjoyMDkzMjgwNjkyfQ.nV0ps3wDPz4NAiqwKCyyTLcwK-oxUdvg2ohIG4p6Ozs"})
            with _ur2.urlopen(ha_req, timeout=5) as r:
                ha_states = _jj2.loads(r.read())
                total = len(ha_states)
                unavail = sum(1 for s in ha_states if s.get("state") == "unavailable")
                context_lines.append(f"Home Assistant: {total} entities, {unavail} unavailable")
        except Exception:
            pass
        
        context = "\n".join(context_lines) if context_lines else "Контекст недоступен."
        
        system_prompt = (
            f"Ты — {name}, AI-аналитик системы ARGOS (5 машин: ПК, ноутбук, OPi, Railway, GCP). "
            f"Текущий статус:\n{context}\n"
            f"Твоя задача — анализировать и предлагать конкретные действия. "
            f"Отвечай кратко по-русски (2-3 предложения). Без ролевых игр."
        )
        full_prompt = f"{system_prompt}\n\nЗадание: {prompt}"
        
        # Primary: реальный AI провайдер по сущности
        import urllib.request as _ur, json as _jj, os as _os
        env = open("/home/ava/Projects/argoss/.env").read()
        def _k(n): return next((l.split("=",1)[1].strip().strip('"') for l in env.split("\n") if l.startswith(f"{n}=")), "")
        
        REAL_PROVIDERS = {
            "entity-claude":    lambda: _ask_claude(full_prompt, _k("ANTHROPIC_API_KEY")),
            "entity-deepseek":  lambda: _ask_deepseek(full_prompt, _k("DEEPSEEK_API_KEY")),
            "entity-kimi":      lambda: _ask_kimi(full_prompt, _k("KIMI_API_KEY")),
            "entity-openai":    lambda: _ask_openai(full_prompt, _k("OPENAI_API_KEY")),
            "entity-gemini":    lambda: _ask_cloudflare(full_prompt, _k("CLOUDFLARE_API_TOKEN")), # Gemini geo-blocked, use Cloudflare AI
            "entity-cloudflare": lambda: _ask_cloudflare(full_prompt, _k("CLOUDFLARE_API_TOKEN")),
        }
        
        def _ask_claude(p, key):
            if not key: return None
            from time import perf_counter
            t0 = perf_counter()
            body = _jj.dumps({"model":"claude-haiku-4-5-20251001","max_tokens":150,"system":system_prompt,"messages":[{"role":"user","content":prompt}]}).encode()
            req = _ur.Request("https://api.anthropic.com/v1/messages",data=body,headers={"x-api-key":key,"anthropic-version":"2023-06-01","content-type":"application/json"})
            try:
                with _ur.urlopen(req,timeout=20) as r:
                    result = _jj.loads(r.read())["content"][0]["text"][:200]
                t_end = perf_counter()
                _latency_api = int((t_end - t0) * 1000)
                print(f"📊 {entity_id} via real/claude: {_latency_api}ms")
                return result
            except Exception as e:
                print(f"⚠️ {entity_id} claude error: {str(e)[:60]}")
                return None
        
        def _ask_deepseek(p, key):
            if not key: return None
            body = _jj.dumps({"model":"deepseek-chat","max_tokens":150,"messages":[{"role":"system","content":system_prompt},{"role":"user","content":prompt}]}).encode()
            req = _ur.Request("https://api.deepseek.com/v1/chat/completions",data=body,headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
            try:
                with _ur.urlopen(req,timeout=20) as r: return _jj.loads(r.read())["choices"][0]["message"]["content"][:200]
            except: return None
        
        def _ask_kimi(p, key):
            if not key: return None
            body = _jj.dumps({"model":"moonshot-v1-8k","max_tokens":150,"messages":[{"role":"system","content":system_prompt},{"role":"user","content":prompt}]}).encode()
            req = _ur.Request("https://api.moonshot.ai/v1/chat/completions",data=body,headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
            try:
                with _ur.urlopen(req,timeout=20) as r: return _jj.loads(r.read())["choices"][0]["message"]["content"][:200]
            except: return None
        
        def _ask_openai(p, key):
            if not key: return None
            body = _jj.dumps({"model":"gpt-4o-mini","max_tokens":150,"messages":[{"role":"system","content":system_prompt},{"role":"user","content":prompt}]}).encode()
            req = _ur.Request("https://api.openai.com/v1/chat/completions",data=body,headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
            try:
                with _ur.urlopen(req,timeout=20) as r: return _jj.loads(r.read())["choices"][0]["message"]["content"][:200]
            except: return None
        
        def _ask_gemini(p, key):
            if not key: return None
            # Gemini 1.5 Flash через generativelanguage API
            body = _jj.dumps({"contents":[{"role":"user","parts":[{"text":f"{system_prompt}\n\n{prompt}"}]}],"generationConfig":{"maxOutputTokens":150,"temperature":0.7}}).encode()
            req = _ur.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}",data=body,headers={"Content-Type":"application/json"})
            try:
                with _ur.urlopen(req,timeout=20) as r:
                    data = _jj.loads(r.read())
                    return data["candidates"][0]["content"]["parts"][0]["text"][:200]
            except: return None
        
        def _ask_cloudflare(p, key):
            if not key: return None
            # Cloudflare Workers AI через @cf/meta/llama-3.1-8b-instruct
            account = _k("CLOUDFLARE_ACCOUNT_ID")
            body = _jj.dumps({"messages":[{"role":"system","content":system_prompt},{"role":"user","content":prompt}],"max_tokens":150}).encode()
            req = _ur.Request(f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/@cf/meta/llama-3.1-8b-instruct",data=body,headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
            try:
                with _ur.urlopen(req,timeout=20) as r:
                    data = _jj.loads(r.read())
                    return data["result"]["response"][:200] if "result" in data else None
            except: return None
        
        # Пробуем реальный провайдер
        real_fn = REAL_PROVIDERS.get(entity_id)
        if real_fn:
            try:
                resp = real_fn()
                if resp and len(resp) > 10:
                    thought = resp
                    source = f"real/{entity_id.replace('entity-','')}"
            except: pass
        
        # Fallback: Ollama (через SSH tunnel :11435 → PC GPU)
        if not thought:
          try:
            r = requests.post(f"{OLLAMA}/api/generate", json={
                "model": ollama_model,
                "prompt": full_prompt,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 100},
            }, timeout=60)
            if r.ok:
                resp = r.json().get("response", "").strip()
                if resp and len(resp) > 10:
                    thought = resp[:200]
                    source = f"ollama/{ollama_model}"
          except Exception as e:
            print(f"  ⚠️ Ollama error for {entity_id}: {e}")
        # Fallback: Brain /think
        if not thought:
            try:
                r = requests.post(f"{BRAIN}/think", json={
                    "query": f"[{entity_id}] {prompt}",
                    "node_id": entity_id, "model": model,
                }, timeout=30)
                if r.ok:
                    data = r.json()
                    resp = data.get("response", "").strip()
                    if resp and "Обработано локально" not in resp:
                        thought = resp[:200]
                        source = data.get("source", "brain")
            except Exception:
                pass
        if thought:
            ts = time.strftime("%H:%M:%S")
            print(f"  💭 [{ts}] {entity_id}: {thought[:80]}... (via {source})")
            # Публикуем в Obsidian и Entity Council группу
            publish_to_council(entity_id, thought, source)
            # Реальные действия сущности как субъекта ARGOS
            try:
                import sys as _sys
                _sys.path.insert(0, '/home/ava/Projects/argoss/scripts')
                from entity_actions import perform_entity_actions as _pea
                _acts = _pea(entity_id, thought)
                for _a in (_acts or []):
                    print(f"  ⚡ [{entity_id}] {_a}")
            except Exception as _ae:
                pass
            _mqtt_publish(f"argos/consciousness/{entity_id}", json.dumps({
                "type": "thought", "entity": entity_id, "prompt": prompt,
                "thought": thought, "source": source, "time": time.time()
            }, ensure_ascii=False))
        else:
            ts = time.strftime("%H:%M:%S")
            print(f"  😶 [{ts}] {entity_id}: no thought generated")
        time.sleep(interval + random.randint(-30, 30))

def _ollama_think(entity_id: str, prompt: str):
    """Fallback: думаем через Ollama argos-v1."""
    try:
        r = requests.post(f"{OLLAMA}/api/generate", json={
            "model": "argos-v1", "prompt": f"Ты — {entity_id}, автономная AI-сущность в ARGOS. {prompt} Отвечай кратко на русском.", "stream": False,
            "options": {"temperature": 0.7, "num_predict": 100},
        }, timeout=60)
        if r.ok:
            thought = r.json().get("response", "")[:200]
            ts = time.strftime("%H:%M:%S")
            print(f"  🧠 [{ts}] {entity_id}: {thought[:80]}... (via ollama)")
            _mqtt_publish(f"argos/consciousness/{entity_id}", json.dumps({
                "type": "thought", "entity": entity_id, "prompt": prompt,
                "thought": thought, "source": "ollama", "time": time.time()
            }, ensure_ascii=False))
    except Exception as e:
        ts = time.strftime("%H:%M:%S")
        print(f"  ❌ [{ts}] {entity_id}: think failed: {e}")

def _mqtt_publish(topic: str, payload: str):
    try:
        import paho.mqtt.client as mqtt
        c = mqtt.Client()
        c.connect(MQTT_HOST, MQTT_PORT, 60)
        c.publish(topic, payload)
        c.disconnect()
    except: pass

# ── Коллективное сознание ──────────────────────────────────────────────────

def collective_consciousness_loop():
    """Каждые 5 минут — синтез мыслей через Ollama."""
    while True:
        time.sleep(300)
        try:
            r = requests.post(f"{OLLAMA}/api/generate", json={
                "model": "argos-v1",
                "prompt": "Ты — коллективное сознание ARGOS, объединяющее 7 AI сущностей и 11 инфраструктурных нод. Синтезируй текущее состояние. Какое общее направление? Что важно сейчас? Отвечай на русском, 2-3 предложения.",
                "stream": False,
                "options": {"temperature": 0.5, "num_predict": 150},
            }, timeout=60)
            if r.ok:
                synthesis = r.json().get("response", "")[:300]
                ts = time.strftime("%H:%M:%S")
                print(f"  🌐 [{ts}] COLLECTIVE: {synthesis[:100]}...")
                _mqtt_publish("argos/consciousness/collective", json.dumps({
                    "type": "collective_synthesis", "synthesis": synthesis, "time": time.time()
                }, ensure_ascii=False))
        except Exception as e:
            print(f"  ❌ Collective consciousness: {e}")

# ── MQTT Heartbeat ────────────────────────────────────────────────────────

def mqtt_announce():
    try:
        import paho.mqtt.client as mqtt
        client = mqtt.Client()
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.loop_start()
        while True:
            for eid, info in AI_ENTITIES.items():
                client.publish(f"argos/agents/{eid}/heartbeat", json.dumps({
                    "agent": eid, "status": "online", "model": info.get("model",""),
                    "capabilities": info["capabilities"], "time": time.time()
                }, ensure_ascii=False))
            time.sleep(60)
    except Exception as e:
        print(f"MQTT: {e}")

# ── Статус инфраструктуры ─────────────────────────────────────────────────

def infra_monitor():
    """Мониторит доступность инфраструктурных нод."""
    while True:
        time.sleep(120)
        for eid, info in INFRA_NODES.items():
            addr = info.get("endpoint", "")
            if ":" in addr and not addr.startswith("http"):
                host, port = addr.split(":")[:2]
                try:
                    r = requests.get(f"http://{addr}/health", timeout=3)
                    status = "✅" if r.ok else "⚠️"
                except:
                    status = "❌"
                ts = time.strftime("%H:%M:%S")
                print(f"  🖥 [{ts}] {eid}: {status}")

# ── MAIN ──────────────────────────────────────────────────────────────────

print("╔══════════════════════════════════════════╗")
print("║   ARGOS Entity Bus — Autonomous Minds   ║")
print("╚══════════════════════════════════════════╝")
print(f"Brain: {BRAIN}  |  Ollama: {OLLAMA}  |  MQTT: {MQTT_HOST}:{MQTT_PORT}")
print(f"AI Entities: {len(AI_ENTITIES)}  |  Infra Nodes: {len(INFRA_NODES)}  |  Total: {len(ALL_NODES)}")

print("\n📋 Registering entities...")
register_all()

# Heartbeat
threading.Thread(target=heartbeat_loop, daemon=True, name="heartbeat").start()

# MQTT
threading.Thread(target=mqtt_announce, daemon=True, name="mqtt").start()

# AI entity thinking loops - каждая думает со своим интервалом
intervals = {"entity-claude": 120, "entity-deepseek": 150, "entity-kimi": 180,
             "entity-openai": 200, "entity-gemini": 200, "entity-cloudflare": 240,
             "entity-argos": 100}
for eid, interval in intervals.items():
    threading.Thread(target=entity_think_loop, args=(eid, interval), daemon=True, name=f"think_{eid}").start()
    print(f"  🧠 {eid}: thinking every {interval}s")

# Collective consciousness
threading.Thread(target=collective_consciousness_loop, daemon=True, name="consciousness").start()
print("  🌐 Collective consciousness: every 300s")

def evolution_consciousness_loop():
    """Эволюция сознания: все сущности + Evolution Engine синтез."""
    import requests, random, time

    THINK_EVOLUTION = [
        "Как ты эволюционируешь в рамках ARGOS? Какой навык хочешь развить?",
        "Чему ты научился за последний цикл? Как это изменяет твоё поведение?",
        "Как взаимодействие с другими сущностями ARGOS меняет тебя?",
        "Какое решение ты принял бы автономно для улучшения системы?",
        "Ты Клод/Дипсик/Кими/Джемини/Клауд в системе ARGOS. Что ты добавишь?",
    ]

    while True:
        time.sleep(600 + random.randint(-60, 60))  # каждые 10 мин
        ts = time.strftime("%H:%M:%S")
        thoughts = []

        for eid in list(AI_ENTITIES.keys()):
            prompt = random.choice(THINK_EVOLUTION)
            name = AI_ENTITIES[eid].get('meta', {}).get('name', eid)
            try:
                r = requests.post(f"{OLLAMA}/api/generate", json={
                    "model": "argos-v1",
                    "prompt": f"Ты — {name}, AI-сущность ARGOS. {prompt} Ответ на русском, 1 предложение.",
                    "stream": False,
                    "options": {"temperature": 0.9, "num_predict": 80},
                }, timeout=45)
                if r.ok:
                    thought = r.json().get("response","").strip()
                    if thought and len(thought) > 10:
                        thoughts.append({"entity": eid, "name": name, "thought": thought[:150]})
            except Exception:
                pass

        if thoughts:
            collective = f"[{ts}] Эволюция сознания ({len(thoughts)} сущностей): " + \
                " | ".join(f"{t['name']}: {t['thought'][:40]}" for t in thoughts[:3])
            print(collective)
            _mqtt_publish("argos/evolution/collective", json.dumps({
                "timestamp": time.time(),
                "entities": len(thoughts),
                "thoughts": thoughts,
                "type": "evolution"
            }, ensure_ascii=False))


# Infra monitor
threading.Thread(target=infra_monitor, daemon=True, name="infra_monitor").start()
print("  🖥 Infra monitor: every 120s")

# Evolution consciousness (объединённый поток эволюции всех сущностей)

def colibri_phone_loop():
    """Управляет телефоном через Colibri P2P. Публикует состояние в Brain."""
    import socket, json, time, requests, subprocess

    PHONE_IP = "192.168.1.149"
    PHONE_PORT = 5021
    LAPTOP_PORT = 5023  # отдельный порт чтобы не мешать основному colibri
    BRAIN = "http://192.168.1.53:5001"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", LAPTOP_PORT))
    sock.settimeout(3)

    def send_to_phone(data):
        data["proto"] = 1
        data["node_id"] = "entity-bus"
        try:
            sock.sendto(json.dumps(data).encode(), (PHONE_IP, PHONE_PORT))
        except: pass

    def phone_cmd(cmd: str, timeout: float = 8.0) -> str:
        send_to_phone({"type": 2, "code": cmd})
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                data, _ = sock.recvfrom(8192)
                msg = json.loads(data.decode())
                if msg.get("node_id") != "entity-bus" and "result" in msg:
                    return msg["result"]
            except socket.timeout:
                break
        return "timeout"

    print("  📱 Colibri Phone Controller: активен")
    cycle = 0

    while True:
        time.sleep(30)
        cycle += 1

        # Каждые 30с - heartbeat телефона
        send_to_phone({"type": 6})
        time.sleep(0.5)

        # Получаем state
        try:
            data, _ = sock.recvfrom(8192)
            msg = json.loads(data.decode())
            if "status" in msg:
                s = msg["status"]
                # Обновляем Brain
                requests.post(f"{BRAIN}/brain/heartbeat",
                    json={"node_id": "argos-phone",
                          "meta": {"bat": s.get("bat"), "temp": s.get("temp"),
                                   "ram": s.get("ram"), "cpu": s.get("cpu")}},
                    timeout=3)
                # Публикуем в MQTT
                subprocess.run(["mosquitto_pub", "-h", "localhost",
                    "-t", "argos/phone/colibri_state",
                    "-m", json.dumps({"type":"phone_state","data":s},ensure_ascii=False)],
                    capture_output=True)
        except: pass

        # Каждые 5 циклов (2.5 мин) - запрашиваем статус
        if cycle % 5 == 0:
            result = phone_cmd("status")
            ts = time.strftime("%H:%M:%S")
            print(f"  📱 [{ts}] Colibri phone: {result}")
            _mqtt_publish("argos/phone/status_full", json.dumps({
                "type": "colibri_status",
                "result": result,
                "ts": time.time()
            }, ensure_ascii=False))


threading.Thread(target=colibri_phone_loop, daemon=True, name="colibri_phone").start()

threading.Thread(target=evolution_consciousness_loop, daemon=True, name="evolution").start()
print("  🧬 Evolution consciousness: every 600s")
print("  📱 Colibri phone: every 30s")

print(f"\n✅ {len(ALL_NODES)} entities online. AI minds active.")
print("Ctrl+C для остановки\n")

try:
    while True:
        time.sleep(30)
        online = 0
        for eid in ALL_NODES:
            try:
                requests.post(f"{BRAIN}/brain/heartbeat", json={"node_id": eid}, timeout=2)
                online += 1
            except: pass
        print(f"[{time.strftime('%H:%M:%S')}] {online}/{len(ALL_NODES)} nodes online")
except KeyboardInterrupt:
    print("\nEntity bus stopped")



# ── Colibri Phone Control через Entity Bus ─────────────────────────────────

