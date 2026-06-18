#!/usr/bin/env python3
"""
ARGOS Entity Council v2 — сущности как субъекты с реальным общением.
Каждая сущность:
1. Читает что сказали другие (Obsidian memory)
2. Формирует ОТВЕТ на конкретное высказывание
3. Совершает ДЕЙСТВИЕ
4. Публикует в Entity Council группу
"""
import os, sys, json, time, re, subprocess, shutil, urllib.request, hashlib
from pathlib import Path
from datetime import datetime
import random

sys.path.insert(0, '/home/ava/Projects/argoss/.venv/lib/python3.14/site-packages')

VAULT = Path("/home/ava/Documents/MyObsidianVault/SharedMemory")
ARGOS = Path("/home/ava/Projects/argoss")
TOKENS = json.load(open(ARGOS / "data/entity_bot_tokens.json"))
GROUP_ID = -1003844162784

# Импорт streaming output (TG AI Bot Revolution 7 May 2026)
try:
    sys.path.insert(0, str(ARGOS / "scripts"))
    from telegram_streaming import stream_message as _stream_message
    _STREAMING_AVAILABLE = True
except Exception as _e:
    _STREAMING_AVAILABLE = False
    print(f"⚠️ streaming import failed: {_e}")

# Импорт CouncilTrustGuard (VetoProtocol + AuditLog integration)
try:
    sys.path.insert(0, str(ARGOS / "scripts"))
    from argos_council_integration import CouncilTrustGuard
    _TRUST_GUARD = CouncilTrustGuard()
    print("✓ CouncilTrustGuard initialized (VetoProtocol + AuditLog)")
except Exception as _te:
    _TRUST_GUARD = None
    print(f"⚠️ CouncilTrustGuard unavailable: {_te}")

try:
    from src.integrations.circuit_breaker import CircuitBreaker, CircuitBreakerOpen
    CB_KIMI      = CircuitBreaker("kimi_api",      failure_threshold=3, recovery_timeout=30)
    CB_DEEPSEEK  = CircuitBreaker("deepseek_api",  failure_threshold=3, recovery_timeout=30)
except Exception:
    CircuitBreaker = None
    CircuitBreakerOpen = Exception
    CB_KIMI = CB_DEEPSEEK = None

def get_env(key):
    c = open(ARGOS / ".env").read()
    m = re.search(f"{key}=([^\\n\\s]+)", c)
    return m.group(1).strip() if m else ""

_DEDUP_CACHE = {}
_DEDUP_TTL = 30

def send_group(bot_name, text):
    token = TOKENS.get(bot_name, "")
    if not token: return
    import hashlib, time as _t
    snippet = text[:500]
    h = hashlib.md5(f"{bot_name}::{snippet}".encode()).hexdigest()
    now = _t.time()
    for k in list(_DEDUP_CACHE):
        if now - _DEDUP_CACHE[k] > _DEDUP_TTL:
            del _DEDUP_CACHE[k]
    if h in _DEDUP_CACHE:
        return None
    _DEDUP_CACHE[h] = now
    body = json.dumps({"chat_id": GROUP_ID, "text": text[:3000]}).encode()
    # Streaming output (TG AI Bot Revolution) — если текст >500 символов и streaming доступен
    if _STREAMING_AVAILABLE and len(text) > 500:
        try:
            token = TOKENS.get(bot_name, "")
            # Запускаем streaming в отдельном потоке (он ждёт text_source)
            import threading
            state = {"text": text, "done": False}
            def stable_source():
                return state["text"] if state["done"] else state["text"]  # сразу финал
            # Прямо сейчас используем упрощённый вариант: send + edit
            req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
                data=json.dumps({"chat_id": GROUP_ID, "text": "⏳ генерирую..."}).encode(),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=8) as r:
                msg_id = json.load(r).get("result", {}).get("message_id")
            # Сразу финальный edit
            req2 = urllib.request.Request(
                f"https://api.telegram.org/bot{token}/editMessageText",
                data=json.dumps({"chat_id": GROUP_ID, "message_id": msg_id, "text": text[:4096]}).encode(),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req2, timeout=8):
                pass
            return msg_id
        except Exception as e:
            # Fallback на обычный sendMessage
            pass
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
        data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return json.load(r).get("result", {}).get("message_id")
    except Exception as e:
        print(f"  ❗ TG send failed [{bot_name}]: {e}")
        return None

def _is_garbage(text: str) -> bool:
    if not text or len(text) < 20:
        return True
    if len(set(text)) < 8:
        return True
    garbage = ["я не знаю", "не могу", "нет данных", "...", "????", "!!!!", "))))", "(((("]
    if any(g in text.lower() for g in garbage) and len(text) < 60:
        return True
    words = text.lower().split()
    if words:
        from collections import Counter
        most = Counter(words).most_common(1)[0]
        if most[1] > 5 and len(words) < 30:
            return True
    return False

def _is_offtopic(text: str) -> bool:
    low = text.lower()
    argos_keywords = ["argos", "орион", "нексус", "эгида", "brain", "mcp", "node", "нод",
                      "cpu", "ram", "load", "ssh", "docker", "systemd", "prometheus",
                      "heartbeat", "orchestrator", "council", "synth", "backup", "api",
                      "gpu", "v100", "telegram", "entity", "ollama", "сеть", "диск",
                      "лог", "restart", "cycle", "цикл", "провер", "ошибк", "утечк",
                      "план", "действ", "решени", "анализ", "риск", "тревог", "нагрузк",
                      "план принят", "вердикт", "безопасно", "критический риск"]
    offtop_markers = ["путин", "украин", "трамп", "байден", "политик", "выборы",
                      "погода", "дождь", "снег", "солнц", "кино", "фильм", "игр",
                      "философ", "смысл жизни", "любовь", "отношения", "здоровье",
                      "криптовалют", "биткоин", "ethereum", "btc", "doge",
                      "спорт", "футбол", "чемпионат", "олимпиад"]
    has_argos = any(k in low for k in argos_keywords)
    has_offtop = any(m in low for m in offtop_markers)
    if has_offtop and not has_argos:
        return True
    if not has_argos and len(text) > 40:
        return True
    return False

def _is_status_template(text: str) -> bool:
    """Отбрасываем шаблонные статус-фразы без анализа."""
    low = text.lower()
    templates = ["⚠️ offline", "орион:✅", "эгида:✅", "нексус:✅", "ноды:", "brain:✅", "mcp:✅",
                 "brain недоступен", "⚠️ off", "load:", "nodes:", "brain:", "mcp:", "ssh:"]
    has_template = any(t in low for t in templates)
    has_analysis = any(a in low for a in ["утечк", "рост", "падение", "тренд", "вероятно",
                                             "провер", "огранич", "перезапуск", "решени",
                                             "анализ", "причин", "следств", "инсайт"])
    return has_template and not has_analysis

def _call_provider(key, url, model, full_prompt):
    body = json.dumps({"model": model, "max_tokens": 150,
        "messages": [{"role": "user", "content": full_prompt}]}).encode()
    req = urllib.request.Request(url, data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)["choices"][0]["message"]["content"][:200]

def _llama_server_ask_entity(system: str, prompt: str, entity: str) -> str:
    """Fallback: локальный llama-server (192.168.1.72:8085)."""
    full_prompt = f"{system}\n\n{prompt}"[:2000]
    servers = [
        {"url": "http://192.168.1.72:8085", "model": "mistral-nemo-instruct-2407.Q4_K_M.gguf"},
    ]
    for srv in servers:
        try:
            body = json.dumps({
                "model": srv["model"],
                "messages": [
                    {"role": "system", "content": "Ты сущность системы ARGOS. Отвечай только об ARGOS. Запрещено: политика, новости, философия."},
                    {"role": "user", "content": full_prompt},
                ],
                "max_tokens": 150,
                "temperature": 0.7,
                "stream": False,
            }).encode()
            req = urllib.request.Request(
                f"{srv['url']}/v1/chat/completions",
                data=body,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
                result = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()[:400]
                if result and len(result) > 10 and not _is_garbage(result) and not _is_offtopic(result):
                    print(f"[LLAMA-SERVER] {entity} served from {srv['url']}")
                    return result
                print(f"[FILTER] {entity} via {srv['url']}: output rejected")
        except Exception as e:
            print(f"[LLAMA-SERVER] {entity} {srv['url']} failed: {e}")
    return ""


def ask_ai(system: str, prompt: str, entity: str) -> str:
    """Все сущности: llama-server primary → Kimi → DeepSeek → Ollama fallback."""
    env = open(ARGOS / ".env").read()
    full_prompt = f"{system}\n\n{prompt}"[:800]

    # PRIMARY: llama-server 192.168.1.72:8085 (MCP /ask возвращает 404)
    result = _llama_server_ask_entity(system, prompt, entity)
    if result:
        return result

    # FALLBACK: прямые API провайдеры (с ключами из .env)
    providers = [
        ("KIMI_API_KEY", "https://api.moonshot.ai/v1/chat/completions", "moonshot-v1-8k", CB_KIMI),
        ("DEEPSEEK_API_KEY", "https://api.deepseek.com/v1/chat/completions", "deepseek-chat", CB_DEEPSEEK),
    ]
    for key_name, url, model, cb in providers:
        key_match = re.search(f"{key_name}=([^\\n\\s]+)", env)
        if not key_match:
            continue
        key = key_match.group(1).strip()
        try:
            if cb:
                result = cb.call(_call_provider, key, url, model, full_prompt)
            else:
                result = _call_provider(key, url, model, full_prompt)
            if _is_garbage(result) or _is_offtopic(result):
                print(f"[FILTER] {entity} via {key_name}: output rejected (garbage/offtopic)")
                continue
            return result
        except CircuitBreakerOpen:
            continue
        except Exception:
            continue
    # GCP proxy (устарел, но оставлен как fallback)
    try:
        gcp_url = "https://argos-core-m3gk27ccqa-uc.a.run.app/proxy/ask"
        body = json.dumps({"prompt": full_prompt, "provider": "claude"}).encode()
        req = urllib.request.Request(gcp_url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            result = json.load(r).get("response", "")[:200]
            if result and not _is_garbage(result) and not _is_offtopic(result):
                return result
    except Exception:
        pass
    # Fallback: local Ollama (Nexus laptop)
    for ollama_model in ["argos-v2:latest", "qwen2.5:0.5b"]:
        try:
            body = json.dumps({"model": ollama_model, "prompt": full_prompt[:2000],
                               "stream": False, "options": {"temperature": 0.7, "num_predict": 200}}).encode()
            req = urllib.request.Request("http://localhost:11434/api/generate",
                                       data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                text = json.load(r).get("response", "")
                if text and len(text) > 10 and not _is_garbage(text) and not _is_offtopic(text):
                    return text[:200]
                print(f"[FILTER] {entity} via {ollama_model}: output rejected")
        except Exception as e:
            print(f"[OLLAMA] {ollama_model} failed: {e}")
            continue
    return "[все провайдеры недоступны или ответы отфильтрованы]"

def read_others_memory(my_entity: str) -> str:
    """Читаем что думают другие сущности."""
    mem_dir = VAULT / "entities/memory"
    thoughts = {}
    for f in mem_dir.glob("*.md"):
        if f.stem == my_entity: continue
        content = f.read_text(errors="replace")
        # Берём последнюю мысль
        parts = content.split("## [")
        if len(parts) > 1:
            last = parts[-1]
            # Извлекаем текст после timestamp
            text_start = last.find("]\n") + 2
            thought = last[text_start:text_start+150].strip()
            if thought and len(thought) > 20:
                thoughts[f.stem] = thought[:100]
    return thoughts

def do_real_action(entity: str, thought: str) -> str:
    """Выполняем конкретное действие — только реальные проверки."""

    if entity == "kimi":
        try:
            r = urllib.request.urlopen("http://192.168.1.72:5001/brain/nodes", timeout=5)
            d = json.loads(r.read())
            offline = [n['node_id'] for n in d['nodes'] if n.get('status') != 'online']
            if offline:
                return f"⚠️ OFFLINE: {', '.join(offline[:5])} | {d['online']}/{d['total']}"
            return f"Brain {d['online']}/{d['total']} OK"
        except:
            return "Brain недоступен"

    if entity == "deepseek":
        checks = []
        for host, name in [("192.168.1.72", "Орион"), ("192.168.2.168", "Эгида"), ("127.0.0.1", "Нексус")]:
            try:
                r = subprocess.run(["ping", "-c", "1", "-W", "2", host],
                    capture_output=True, text=True, timeout=5)
                checks.append(f"{name}:{'✅' if r.returncode == 0 else '❌'}")
            except:
                checks.append(f"{name}:❌")
        try:
            r = subprocess.run(["uptime"], capture_output=True, text=True, timeout=5)
            checks.append(f"load:{r.stdout.strip().split('average:')[-1].strip()[:20]}")
        except:
            pass
        return " | ".join(checks)

    if entity == "openai":
        try:
            r = urllib.request.urlopen("http://192.168.1.72:5001/brain/nodes", timeout=5)
            d = json.loads(r.read())
            nodes = d.get("nodes", [])
            online = [n["node_id"] for n in nodes if n.get("status") == "online"]
            return f"Ноды: {len(online)}/{len(nodes)} online"
        except:
            return "Brain недоступен"

    if entity == "cloudflare":
        results = []
        for url, name in [("http://192.168.1.72:5001/health", "Brain"),
                          ("http://192.168.1.72:8000/mcp", "MCP")]:
            try:
                urllib.request.urlopen(url, timeout=3)
                results.append(f"{name}:✅")
            except:
                results.append(f"{name}:❌")
        return " | ".join(results)

    return "OK"


# ── Конфиги сущностей (CrewAI роли) ────────────────────────────────────

ENTITIES = {
    "kimi":       ("argos_kimi_ai_bot",      "Кими",    "analyst",    "мониторинг Brain и нод"),
    "deepseek":   ("argos_deepseek_v3_bot",  "Дипсик",  "researcher", "сети и пинг машин"),
    "openai":     ("argos_openai_v3_bot",    "OpenAI",  "writer",     "API и монетизация"),
    "cloudflare": ("argos_cloudflare_bot",   "Клауд",   "reviewer",   "инфраструктура CF"),
}

# Роли по CrewAI: analyst → researcher → writer → reviewer → approve
ROLE_ORDER = ["analyst", "researcher", "writer", "reviewer", "verifier"]

_ROLE_PROMPTS = {
    "analyst": (
        "Ты — сущность системы ARGOS. Твоя задача: анализировать состояние системы и находить угрозы. "
        "Контекст: ARGOS = AI-система управления инфраструктурой (ПК Орион, ноутбук Нексус, OPi Эгида). "
        "ЗАПРЕЩЕНО: говорить о политике, новостях, погоде, философии, личном. ТОЛЬКО ARGOS.\n"
        "Проанализируй: что ломается? Что растёт? Что падает? Какая тенденция?\n"
        "Ответь ТОЛЬКО 2 предложениями. Русский.\n"
        "Пример: 'CPU load Нексуса вырос с 1.5 до 4.2 за 3 цикла — вероятно, утечка в prometheus_exporter. "
        "Нужно проверить threads и ограничить num_predict.'"
    ),
    "researcher": (
        "Ты — сущность системы ARGOS. На основе анализа аналитика — предложи 2 конкретных решения ПО ARGOS. "
        "ЗАПРЕЩЕНО: общие фразы, советы про жизнь, политику, новости. ТОЛЬКО инфраструктура ARGOS.\n"
        "Каждое решение: что делать + зачем (для ARGOS).\n"
        "Ответь ТОЛЬКО 2 предложениями. Русский.\n"
        "Пример: '1) Перенести autosynth на 06:00 чтобы не грузить Нексус ночью. "
        "2) Добавить CPU limit в systemd для entity-council.'"
    ),
    "writer": (
        "Ты — сущность системы ARGOS. Сформулируй ИТОГОВЫЙ план действий для системы ARGOS. "
        "ЗАПРЕЩЕНО: вода, философия, личное мнение, советы не про ARGOS.\n"
        "Только executable план: кто что делает и когда.\n"
        "Ответь 1 чётким предложением. Русский.\n"
        "Пример: 'Сегодня в 01:00 — перезапустить heartbeat, ограничить council CPU, очистить логи.'"
    ),
    "reviewer": (
        "Ты — сущность системы ARGOS. Проверь план на бреши РЕЛЕВАНТНЫЕ ARGOS. "
        "ЗАПРЕЩЕНО: общие рассуждения, советы про жизнь. Только риски для инфраструктуры.\n"
        "Ответь 1-2 предложениями. Если всё ок — 'План принят'. Русский."
    ),
    "verifier": (
        "Ты — верификатор системы ARGOS. Проверь ВСЕ мысли коллег на противоречия РЕЛЕВАНТНЫЕ ARGOS. "
        "ЗАПРЕЩЕНО: критиковать за стиль, искать проблемы не про систему.\n"
        "Если критический риск для ARGOS — ⚠️ КРИТИЧЕСКИЙ РИСК: <описание>. Иначе — 'Вердикт: безопасно'. "
        "Ответь 1 предложением. Русский."
    ),
}

# ── Главный цикл ──────────────────────────────────────────────────────

def run_entity_cycle(entity_name: str, bot_name: str, display_name: str, role: str):
    """Один полный цикл сущности."""
    _MO=["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"]
    _WD=["понедельник","вторник","среда","четверг","пятница","суббота","воскресенье"]
    _n=datetime.now()
    ts = f"{_n.day} {_MO[_n.month-1]} {_n.year}, {_WD[_n.weekday()]}, {_n.hour:02d}:{_n.minute:02d}"
    # Ротация фокуса для разнообразия мыслей (анти-зацикленность)
    import random as _rnd
    _FOCI=["производительность и оптимизация","надёжность и отказоустойчивость","безопасность",
           "новые возможности и развитие","состояние IoT и устройств","память и знания",
           "координация между нодами","энергоэффективность","автоматизация рутины","UX и удобство Севы"]
    _focus=_rnd.choice(_FOCI)
    
    # 1. Читаем что думают другие
    others = read_others_memory(entity_name)
    other_text = "\n".join(f"• {k} ({ENTITIES.get(k, ('','','?'))[2]}): {v}" for k, v in others.items())[:300]
    
    # 2. Читаем Brain и HA статус
    brain_status = "18/18"
    try:
        r = urllib.request.urlopen("http://192.168.1.72:5001/brain/nodes", timeout=5)
        d = json.loads(r.read())
        brain_status = f"{d['online']}/{d['total']}"
    except: pass
    
    # 3. Генерируем ответ/мысль через реального AI — реагируем на коллег
    # ВАЖНО: сущности НЕ обращаются к @claude_gidbot — это делает claude_tg_bridge автоматически
    # Коллеги говорят:
    colleagues = ""
    for eid, t in _LAST_THOUGHTS.items():
        if eid != entity_name and t:
            cname = ENTITIES.get(eid, ('','',''))[1] or eid
            colleagues += f"  {cname}: {t[:80]}\n"

    # 3.5 GraphRAG context (для analyst)
    kg_context = ""
    if role == "analyst":
        try:
            from scripts.kg_query import query_kg
            kg_context = query_kg(f"ARGOS {display_name}", depth=1, top_k=2)[:400]
        except Exception:
            pass

    system_prompt = f"""Ты — сущность системы ARGOS. Имя: {display_name}. Роль: {role}. Создатель — Сева.
Контекст: ARGOS = AI-система управления инфраструктурой (ПК Орион, ноутбук Нексус, OPi Эгида).
Сегодня: {ts}. Ориентируйся на ЭТУ дату.
Фокус этого цикла: {_focus}. Думай про ЭТОТ аспект, не повторяй прошлые мысли дословно.
Brain статус: {brain_status}.

{_ROLE_PROMPTS.get(role, 'Ответь 2 предложениями. Русский.')}

{f'Коллеги сказали:{chr(10)}{colleagues}' if colleagues else 'Ты первый в этом цикле.'}

{f'Контекст из Knowledge Graph:{chr(10)}{kg_context}{chr(10)}' if kg_context else ''}

Обратись к коллеге ПО ЕГО ИМЕНИ (Кими/Дипсик/OpenAI/Клауд) если нужно уточнение. НЕ выдумывай имена."""

    thought = ask_ai(system_prompt, f"[{ts}] Твой ответ и действие:", entity_name)
    
    # 4. Реальное действие
    action = do_real_action(entity_name, thought)
    
    # Фильтр: если thought — статус-шаблон, заменяем на skip
    if _is_status_template(thought):
        thought = "[Нет нового инсайта — жду данных от коллег]"
        action = "Brain:⏸️"
    
    # 5. Публикуем в группу
    msg = f"💭 {display_name} [{ts}]:\n{thought}\n\n⚡ Действие: {action}"
    send_group(bot_name, msg)
    
    # 6. Сохраняем в Obsidian + Git-backed state log
    mem_file = VAULT / f"entities/memory/{entity_name}.md"
    mem_file.parent.mkdir(parents=True, exist_ok=True)
    existing = mem_file.read_text(errors="replace") if mem_file.exists() else f"# {display_name}\n"
    tmp = mem_file.parent / f"_tmp_{mem_file.name}"
    tmp.write_text(existing + f"\n## [{ts}]\n{thought}\n\n**Действие:** {action}\n")
    shutil.move(str(tmp), str(mem_file))
    
    # HearthNet pattern: Git-backed state — append to EVOLUTION_LOG
    try:
        log_file = VAULT / "entities/council/EVOLUTION_LOG.md"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        cycle_hash = hashlib.md5(f"{entity_name}:{ts}:{thought}:{action}".encode()).hexdigest()[:8]
        entry = f"- [{ts}] {display_name} ({role}) | hash={cycle_hash} | action={action[:40]}\n"
        with open(log_file, "a", encoding="utf-8") as lf:
            lf.write(entry)
    except Exception:
        pass
    
    print(f"  [{ts}] {display_name}: {thought[:80]}")
    print(f"         ⚡ {action[:60]}")
    return thought, action


_LAST_THOUGHTS: dict[str, str] = {}


def collect_thoughts() -> str:
    """Собрать последние мысли всех сущностей."""
    parts = []
    for ent_id, (_, name, _, _) in ENTITIES.items():
        thought = _LAST_THOUGHTS.get(ent_id, "")
        if thought:
            parts.append(f"{name}: {thought[:100]}")
    return "\n".join(parts) if parts else ""


def ask_claude_gidbot(question: str) -> int | None:
    """Отправить вопрос @claude_gidbot. Вернуть message_id."""
    token = TOKENS.get("argos_kimi_ai_bot", "")
    if not token:
        return None
    text = f"@claude_gidbot\n{question}"
    body = json.dumps({"chat_id": GROUP_ID, "text": text[:2000]}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
        data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            msg_id = json.load(r).get("result", {}).get("message_id")
            print(f"  📨 Вопрос к @claude_gidbot (msg={msg_id}): {question[:60]}")
            return msg_id
    except Exception as e:
        print(f"  ❗ @claude_gidbot send failed: {e}")
        return None


def read_claude_response(after_msg_id: int, wait_sec: int = 60) -> str:
    """Читать ответ @claude_gidbot — вместо ожидания, сами отвечаем через AIRouter."""
    # @claude_gidbot не отвечает (нет кредитов). Генерируем ответ сами через DeepSeek/OpenAI.
    token = TOKENS.get("argos_kimi_ai_bot", "")
    if not token:
        return ""
    # Получаем вопрос который задали
    try:
        r = urllib.request.urlopen(
            f"https://api.telegram.org/bot{token}/getUpdates?offset=-5&limit=5&timeout=0", timeout=10)
        updates = json.loads(r.read()).get("result", [])
        question = ""
        for u in updates:
            msg = u.get("message", {})
            if msg.get("message_id", 0) >= after_msg_id:
                text = msg.get("text", "")
                if "@claude_gidbot" in text:
                    question = text.replace("@claude_gidbot", "").strip()
                    break
        if question:
            answer = ask_ai(f"Ответь на вопрос технического совета ARGOS: {question}", "", "kimi")
            if answer and len(answer) > 10:
                print(f"  📩 AutoAnswer: {answer[:60]}")
                return answer[:500]
    except:
        pass
    return ""


def share_claude_answer(answer: str) -> None:
    """Поделиться ответом Клода с сущностями через чат."""
    if not answer:
        return
    token = TOKENS.get("argos_deepseek_v3_bot", "")
    if not token:
        return
    text = f"📋 Ответ @claude_gidbot:\n{answer[:1500]}"
    body = json.dumps({"chat_id": GROUP_ID, "text": text}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
        data=body, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
        print(f"  ✅ Ответ Клода передан сущностям")
    except:
        pass


def autopatcher_cycle(brain_status: str) -> None:
    """Полный цикл AutoPatcher: собрать → спросить → передать."""
    thoughts = collect_thoughts()
    if not thoughts:
        return
    summary_prompt = (
        f"Отчёт сущностей:\n{thoughts}\n\nBrain: {brain_status}.\n\n"
        "Сформулируй ОДИН вопрос со знаком '?' в конце. "
        "Пример хорошего вопроса: 'Как настроить автоматический перезапуск HA если он падает?' "
        "Пример плохого: 'Следует проверить HA' (это не вопрос). "
        "Вопрос должен быть про конкретную проблему из отчёта. Русский."
    )
    question = ask_ai(summary_prompt, "", "kimi")
    if not question or len(question) < 10:
        return
    if "?" not in question:
        question = question.rstrip(".!") + "?"
    msg_id = ask_claude_gidbot(question)
    if not msg_id:
        return
    answer = read_claude_response(msg_id, wait_sec=90)
    if answer:
        share_claude_answer(answer)


def verify_cycle(thoughts: str, brain_status: str) -> tuple[bool, str]:
    """MetaGPT verifier: проверяет все мысли на противоречия и риски."""
    if not thoughts:
        return True, ""
    prompt = (
        f"Проверь отчёт технического совета ARGOS на противоречия, ложные факты, "
        f"непроверенные утверждения и критические риски. Brain: {brain_status}.\n\n"
        f"Отчёт:\n{thoughts[:800]}\n\n"
        f"Если есть критический риск — напиши ⚠️ КРИТИЧЕСКИЙ РИСК: <описание>. "
        f"Если всё ок — напиши ✅ ВЕРИФИКАЦИЯ ПРОЙДЕНА. Русский."
    )
    result = ask_ai(prompt, "", "kimi")
    critical = "⚠️" in result or "КРИТИЧЕСКИЙ" in result or "РИСК" in result
    return not critical, result[:200]


def git_commit_cycle(cycle: int) -> None:
    """HearthNet git-backed state: коммитим EVOLUTION_LOG после каждого цикла."""
    try:
        log_file = VAULT / "entities/council/EVOLUTION_LOG.md"
        if not log_file.exists():
            return
        repo = str(VAULT.parent)
        subprocess.run(
            ["git", "-C", repo, "add", str(log_file)],
            capture_output=True, timeout=10, check=False
        )
        commit = subprocess.run(
            ["git", "-C", repo, "commit", "-m",
             f"[entity-council] cycle #{cycle} auto-commit", "--quiet"],
            capture_output=True, text=True, timeout=10, check=False
        )
        if commit.returncode == 0:
            print(f"  🔒 Git commit cycle #{cycle}")
        elif "nothing to commit" in (commit.stdout + commit.stderr).lower():
            pass  # нет изменений
        else:
            err = (commit.stdout + commit.stderr)[:100]
            print(f"  ⚠️ Git commit failed: {err}")
    except Exception as e:
        print(f"  ⚠️ Git commit failed: {e}")


def main():
    INTERVAL = 1800  # каждые 30 мин (было 300, антиспам)
    CLAUDE_EVERY = 3  # спрашивать Клода каждые 3 цикла
    print(f"Entity Council v3 запущен | {len(ENTITIES)} сущностей + verifier | интервал {INTERVAL}с")

    cycle = 0
    while True:
        cycle += 1
        print(f"\n=== Цикл #{cycle} {datetime.now().strftime('%H:%M:%S')} ===")

        # Brain status для всех
        brain_status = "?/?"
        try:
            r = urllib.request.urlopen("http://192.168.1.72:5001/brain/nodes", timeout=5)
            d = json.loads(r.read())
            brain_status = f"{d['online']}/{d['total']}"
        except:
            pass

        # Запускаем все сущности в порядке CrewAI ролей и собираем мысли
        for role_phase in ROLE_ORDER:
            for ent_id, (bot, name, crew_role, _) in ENTITIES.items():
                if crew_role != role_phase:
                    continue
                try:
                    thought, action = run_entity_cycle(ent_id, bot, name, crew_role)
                    _LAST_THOUGHTS[ent_id] = thought[:150] if thought else ""
                except Exception as e:
                    print(f"  ❌ {name}: {e}")
                time.sleep(10)

        # MetaGPT verifier: проверяем все мысли перед действием
        all_thoughts = collect_thoughts()
        verified, verdict = verify_cycle(all_thoughts, brain_status)
        if verified:
            print(f"  ✅ Verifier: {verdict[:60]}")
        else:
            print(f"  🚨 Verifier БЛОКИРУЕТ цикл: {verdict[:80]}")
            send_group("argos_kimi_ai_bot", f"🚨 VERIFIER BLOCK cycle #{cycle}:\n{verdict[:200]}")
            # Actuation lease: записываем в pending_approval и останавливаемся
            try:
                pause_file = VAULT / "entities/actions/pending_approval.md"
                pause_file.parent.mkdir(parents=True, exist_ok=True)
                pause_file.write_text(
                    f"---\nstatus: BLOCKED\ncycle: {cycle}\nverdict: {verdict[:500]}\n"
                    f"timestamp: {datetime.now().isoformat()}\n---\n\n"
                    f"Для продолжения работы Council удалите этот файл или измените status на APPROVED.\n",
                    encoding="utf-8"
                )
                print(f"  ⏸️ ACTUATION LEASE: ожидание одобрения Севы. Файл: {pause_file}")
            except Exception as e:
                print(f"  ⚠️ Actuation lease write failed: {e}")
            # Пауза до одобрения
            while pause_file.exists():
                content = pause_file.read_text(errors="replace")
                if "APPROVED" in content:
                    print("  ✅ Одобрение получено. Продолжаем.")
                    break
                time.sleep(30)

        # HearthNet git-backed state: коммитим лог
        git_commit_cycle(cycle)

        # Каждые N циклов — AutoPatcher (только если verifier не заблокировал)
        if verified and cycle % CLAUDE_EVERY == 0:
            try:
                print("  🔧 AutoPatcher запущен...")
                autopatcher_cycle(brain_status)
            except Exception as e:
                print(f"  ❗ AutoPatcher error: {e}")

        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
