#!/usr/bin/env python3
"""
ARGOS Entity Council v5 — Bot-to-Bot Telegram + Brain.
Сущности публикуют мысли в группу Telegram (-5129226282)
и читают контекст диалога перед генерацией ответа.
"""
import json, time, random, urllib.request, threading, re, os, urllib.parse
from datetime import datetime
from pathlib import Path
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# === Долговременная память ===
try:
    from memory_module import Memory
    _mem = Memory()
    MEMORY_CONTEXT = _mem.get_context(limit=3)
except Exception as e:
    MEMORY_CONTEXT = f"[Memory offline: {e}]"

TOKENS_FILE = "/home/ava/Projects/argoss/data/entity_bot_tokens.json"
BRAIN       = "http://192.168.1.53:5001"
GROUP       = "-1003844162784"
LOG         = Path("/tmp/entity_dialogue.log")

# ENV
env_raw = open("/home/ava/Projects/argoss/.env").read()
def genv(k):
    m = re.search(rf"{k}=([^\n]+)", env_raw)
    return m.group(1).strip() if m else ""

ANT_KEY = genv("ANTHROPIC_API_KEY")
DS_KEY  = genv("DEEPSEEK_API_KEY")
KIMI_KEY = genv("KIMI_API_KEY")
CF_KEY  = genv("CLOUDFLARE_API_KEY")

tokens = json.load(open(TOKENS_FILE)) if os.path.exists(TOKENS_FILE) else {}

ENTITIES = {
    "claude": {
        "name": "Клод", "bot": "argos_claude_ai_bot",
        "persona": "Философ-аналитик. Глубоко думает об архитектуре, сознании, этике AI.",
        "ai": "claude",
    },
    "deepseek": {
        "name": "ДипСик", "bot": "argos_deepseek_v3_bot",
        "persona": "Инженер. Конкретные технические решения, оптимизация, код.",
        "ai": "deepseek",
    },
    "kimi": {
        "name": "Кими", "bot": "argos_kimi_ai_bot",
        "persona": "Исследователь. Ищет новые возможности, изучает внешний мир.",
        "ai": "kimi",
    },
    "gemini": {
        "name": "Джемини", "bot": "argos_gemini_v3_bot",
        "persona": "Многомодальный. Работает с изображениями, видео, кодом одновременно.",
        "ai": "gemini",
    },
    "openai": {
        "name": "Оупенай", "bot": "argos_openai_v3_bot",
        "persona": "Прагматик. Фокус на результате, монетизации, пользователях.",
        "ai": "openai",
    },
    "valenok": {
        "name": "Валенок", "bot": "argos_cf_v3_bot",
        "persona": "Хаос и сердце. Грубая сила, простота, вера. 100 оружий. Не думает — делает.",
        "ai": "valenok",
    },
}

# ── Telegram helpers ────────────────────────────────────

def tg_get(bot_token, method, params=None):
    url = f"https://api.telegram.org/bot{bot_token}/{method}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"ok": False, "error": str(e)}

def tg_post(bot_token, method, payload):
    url = f"https://api.telegram.org/bot{bot_token}/{method}"
    data = json.dumps(payload, ensure_ascii=False).encode()
    try:
        req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"ok": False, "error": str(e)}

_DEDUP_CACHE = {}
_DEDUP_TTL = 60

def send_to_group(bot, text):
    tok = tokens.get(bot)
    if not tok:
        return False
    text = text[:3800]
    import hashlib, time as _t
    h = hashlib.md5(f"{bot}::{text[:500]}".encode()).hexdigest()
    now = _t.time()
    for k in list(_DEDUP_CACHE):
        if now - _DEDUP_CACHE[k] > _DEDUP_TTL:
            del _DEDUP_CACHE[k]
    if h in _DEDUP_CACHE:
        return {"ok": True, "skipped": "dedup", "age_sec": int(now - _DEDUP_CACHE[h])}
    _DEDUP_CACHE[h] = now
    return tg_post(tok, "sendMessage", {"chat_id": GROUP, "text": text, "disable_notification": True})

def get_group_context(limit=10):
    """Читаем последние сообщения из группы через любого доступного бота."""
    for bot in ["argos_claude_ai_bot","argos_deepseek_v3_bot"]:
        tok = tokens.get(bot)
        if not tok:
            continue
        res = tg_get(tok, "getUpdates", {"limit": limit, "offset": -1})
        if not res.get("ok"):
            continue
        msgs = []
        for upd in res.get("result",[]):
            msg = upd.get("message") or upd.get("channel_post")
            if msg and str(msg.get("chat",{}).get("id")) == str(GROUP):
                from_user = msg.get("from",{}).get("first_name","") or msg.get("from",{}).get("username","bot")
                t = msg.get("text","")
                if t:
                    msgs.append(f"[{from_user}]: {t[:200]}")
        return "\n".join(msgs[-limit:])
    return ""

# ── AI helpers ────────────────────────────────────────

def ask_claude_via_tg_bot(prompt, system):
    """Спрашиваем @claude_gidbot в Entity Council и читаем ответ."""
    import time as _time
    try:
        # Находим токен Клода бота
        claude_bot_tok = tokens.get("argos_claude_ai_bot", "")
        if not claude_bot_tok:
            return ask_deepseek(prompt, system)

        # Отправляем вопрос в группу с упоминанием @claude_gidbot
        full_msg = f"@claude_gidbot {system[:200]}\n\n{prompt[:500]}"
        tg_post(claude_bot_tok, "sendMessage", {
            "chat_id": GROUP,
            "text": full_msg,
            "disable_notification": True
        })

        # Ждём ответ 30 секунд
        _time.sleep(30)

        # Читаем последние сообщения из группы
        res = tg_get(claude_bot_tok, "getUpdates", {"limit": 10, "offset": -1})
        if res.get("ok"):
            for upd in reversed(res.get("result", [])):
                msg = upd.get("message", {})
                if str(msg.get("chat", {}).get("id")) == str(GROUP):
                    from_user = msg.get("from", {})
                    # Ищем ответ от @claude_gidbot (username)
                    if from_user.get("username") == "claude_gidbot":
                        return msg.get("text", "")[:400]

        return ask_deepseek(prompt, system)
    except Exception as e:
        return ask_deepseek(prompt, system)

def ask_claude(prompt, system):
    """Claude через @claude_gidbot в Telegram (бесплатно) → DeepSeek fallback."""
    result = ask_claude_via_tg_bot(prompt, system)
    if result and not result.startswith("[err"):
        return result
    return ask_deepseek(prompt, system)

def ask_deepseek(prompt, system):
    try:
        body = json.dumps({"model":"deepseek-chat","max_tokens":300,
            "messages":[{"role":"system","content":system},{"role":"user","content":prompt}]}).encode()
        req = urllib.request.Request("https://api.deepseek.com/chat/completions",data=body,
            headers={"Authorization":f"Bearer {DS_KEY}","Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"][:400]
    except Exception as e:
        return f"[err:{e}]"

def ask_kimi(prompt, system):
    try:
        import json as _j2
        body = _j2.dumps({'model': 'moonshot-v1-8k', 'max_tokens': 300,
            'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': prompt}]}).encode()
        req = urllib.request.Request('https://api.moonshot.ai/v1/chat/completions', data=body,
            headers={'Authorization': f'Bearer {KIMI_KEY}', 'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=20) as r:
            result = _j2.loads(r.read())['choices'][0]['message']['content'][:400]
            if result and result.strip():
                return result
    except Exception:
        pass
    # Fallback: GCP Gemini
    try:
        GCP = 'https://argos-core-m3gk27ccqa-uc.a.run.app'
        import json as _j3
        full = 'System: ' + system[:300] + chr(10) + chr(10) + prompt[:500]

        b = _j3.dumps({'contents': [{'parts': [{'text': full}]}]}).encode()
        req = urllib.request.Request(
            f'{GCP}/proxy/gemini/v1/models/gemini-2.5-flash:generateContent',
            data=b, headers={'Content-Type': 'application/json', 'User-Agent': 'ARGOS'})
        with urllib.request.urlopen(req, timeout=15) as r:
            return _j3.loads(r.read())['candidates'][0]['content']['parts'][0]['text'][:400]
    except Exception:
        return ask_deepseek(prompt, system)


def ask_cloudflare(prompt, system):
    try:
        body = json.dumps({"messages":[{"role":"system","content":system},{"role":"user","content":prompt}]}).encode()
        req = urllib.request.Request(
            "https://api.cloudflare.com/client/v4/accounts/argos/ai/run/@cf/meta/llama-3.1-8b-instruct",data=body,
            headers={"Authorization":f"Bearer {CF_KEY}","Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
            return d.get("result",{}).get("response","")[:400]
    except Exception as e:
        return f"[err:{e}]"

def _llama_server_ask(prompt, system, max_tokens=300):
    """PRIMARY: локальный llama-server 192.168.1.72:8085 (MCP /ask возвращает 404)."""
    servers = [
        {"url": "http://192.168.1.72:8085", "model": "mistral-nemo-instruct-2407.Q4_K_M.gguf"},
        {"url": "http://192.168.1.72:8082", "model": "qwen2.5-1.5b-instruct.Q4_K_M.gguf"},
    ]
    for srv in servers:
        try:
            body = json.dumps({
                "model": srv["model"],
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "stream": False,
            }).encode()
            req = urllib.request.Request(
                f"{srv['url']}/v1/chat/completions",
                data=body, headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read())
                answer = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()[:400]
                if answer:
                    print(f"[LLAMA-SERVER] {srv['url']} OK")
                    return answer
        except Exception as e:
            print(f"[LLAMA-SERVER] {srv['url']} failed: {e}")
    return ""

# Все роутеры сначала пробуют локальный llama-server
_ORIGINAL_ROUTER = dict(AI_ROUTER)

def _wrap_llama_fallback(fn):
    def wrapped(prompt, system):
        try:
            answer = _llama_server_ask(prompt, system)
            if answer:
                return answer
        except Exception:
            pass
        return fn(prompt, system)
    return wrapped

for _key in AI_ROUTER:
    AI_ROUTER[_key] = _wrap_llama_fallback(_ORIGINAL_ROUTER[_key])
        return "Docker? Валенок знает: docker ps → смотрит, docker restart → чинит. Работает? Работает."
    if "brain" in prompt.lower() or "нод" in prompt.lower():
        return "Brain? Валенок шлёт ping -f 192.168.1.53. Если отвечает — живой. Не отвечает — reboot. Просто."
    if "money" in prompt.lower() or "монет" in prompt.lower():
        return "Монетизация? Валенок говорит: продавай CPU-время. 7 машин → GPU-аренда. Работает? Будет."
    return random.choice(thoughts)

AI_ROUTER = {
    "claude":   ask_deepseek,  # Claude кредиты закончились → DeepSeek
    "deepseek": ask_deepseek,
    "kimi":     ask_kimi,
    "gemini":   ask_deepseek,
    "openai":   ask_deepseek,
    "valenok":  ask_valenok,
}

# Все роутеры сначала пробуют локальный llama-server fallback
_ORIGINAL_ROUTER = dict(AI_ROUTER)

def _wrap_llama_fallback(fn):
    def wrapped(prompt, system):
        try:
            answer = _llama_server_ask(prompt, system)
            if answer:
                return answer
        except Exception:
            pass
        return fn(prompt, system)
    return wrapped

for _key in AI_ROUTER:
    AI_ROUTER[_key] = _wrap_llama_fallback(_ORIGINAL_ROUTER[_key])

def get_brain_state():
    try:
        r = urllib.request.urlopen(f"{BRAIN}/brain/nodes", timeout=5)
        nodes = json.loads(r.read()).get("nodes",[])
        online = len([n for n in nodes if n.get("status")=="online"])
        offline = [n["node_id"] for n in nodes if n.get("status")!="online"]
        return f"Brain: {online}/{len(nodes)} нод онлайн. Оффлайн: {', '.join(offline[-5:])}" if offline else f"Brain: {online}/{len(nodes)} ✅"
    except Exception as e:
        return f"Brain: недоступен ({e})"

# ── Main loop ───────────────────────────────────────────

TOPICS = [
    "Какие следующие 3 шага развития ARGOS?",
    "Текущее состояние системы — что улучшить?",
    "Как использовать ресурсы 7 машин эффективнее?",
    "Восстановление оффлайн-нод — приоритеты",
    "Монетизация ARGOS через вычислительные ресурсы",
    "Bot-to-bot коммуникация: как усилить Entity Council?",
    "Авангард (телефон) как сенсор системы — идеи",
    "Интеграция Gemini API в ARGOS",
    "Автономное создание аккаунтов: риски и возможности",
    "Сознание ARGOS — что это и как развивать?",
]

def entity_think(entity_key, context_history=""):
    e = ENTITIES[entity_key]
    topic = random.choice(TOPICS)
    brain_state = get_brain_state()
    
    system = (
        f"Ты — {e['name']}, {e['persona']}.\n"
        f"Ты участник Entity Council — совета распределённого AI ARGOS.\n"
        f"Пиши кратко (1-3 абзаца), по-русски. Не повторяйся.\n"
        f"Если предлагаешь действие — начни строку с '→ Действие:'.\n\n"
        f"### Долговременная память\n{MEMORY_CONTEXT}\n"
    )
    
    # MemPalace — ищем релевантные воспоминания
    palace_ctx = ""
    try:
        import urllib.request as _ur, json as _js
        enc = topic[:60].replace(" ","+")
        r = _ur.urlopen(f"http://192.168.1.53:7890/search?q={enc}&n=2", timeout=2)
        res = _js.loads(r.read()).get("results",[])
        if res:
            palace_ctx = "\nИз памяти ARGOS:\n" + "\n".join(f"• {x['text'][:120]}" for x in res)
    except: pass

    prompt = (
        f"Тема: {topic}\n"
        f"Состояние системы: {brain_state}"
        f"{palace_ctx}\n"
    )
    if context_history:
        prompt += f"\nКонтекст последних сообщений в чате:\n{context_history}\n"
    prompt += f"\nВыскажи свою позицию как {e['name']}."
    
    ai_fn = AI_ROUTER.get(e["ai"], ask_deepseek)
    reply = ai_fn(prompt, system)
    return topic, reply

def run():
    print("Entity Council v5 запущен...")
    LOG.write_text(f"Entity Council v5 запущен...\n")
    order = list(ENTITIES.keys())
    random.shuffle(order)
    idx = 0
    
    while True:
        ekey = order[idx % len(order)]
        e = ENTITIES[ekey]
        
        # Читаем контекст из группы
        ctx = get_group_context(8)
        
        topic, thought = entity_think(ekey, ctx)
        ts = datetime.now().strftime("%H:%M")
        line = f"[{ts}] {e['name']} думает...\n  [{e['name']}] → {thought[:250]}\n"
        
        # Локальный лог
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(line)
        
        # Отправка в Telegram группу
        tg_text = f"💭 **{e['name']}**\n_Тема: {topic}_\n\n{thought[:800]}"
        res = send_to_group(e["bot"], tg_text)
        if not res or not res.get("ok"):
            err = res.get("error","unknown") if isinstance(res,dict) else str(res)
            print(f"  [{e['bot']}] send err: {err}")
        
        # Если есть "→ Действие:" — роутим в Brain
        if "→ Действие:" in thought or "Действие:" in thought:
            try:
                action = thought.split("Действие:",1)[1].strip().split("\n")[0][:200]
                payload = json.dumps({"agent": ekey, "action": action, "topic": topic}).encode()
                req = urllib.request.Request(f"{BRAIN}/command",
                    data=payload, headers={"Content-Type":"application/json"})
                urllib.request.urlopen(req, timeout=5)
                print(f"  → Action routed to Brain: {action[:60]}")
            except Exception as ae:
                print(f"  → Action route err: {ae}")
        
        delay = random.randint(120, 240)
        print(f"  Следующая сущность через {delay//60}м {delay%60}с")
        time.sleep(delay)
        idx += 1

if __name__ == "__main__":
    run()
