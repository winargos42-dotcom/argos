"""Запускает ОДНОГО entity бота. Запускается отдельно для каждой сущности."""
import sys, json, asyncio, urllib.request, subprocess
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from pathlib import Path
from datetime import datetime

USERNAME = sys.argv[1] if len(sys.argv) > 1 else "argos_claude_ai_bot"

env = open('/home/ava/Projects/argoss/.env').read()
def key(n): return next((l.split('=',1)[1].strip().strip('"') for l in env.split('\n') if l.startswith(f'{n}=')), '')
GCP = "https://argos-core-m3gk27ccqa-uc.a.run.app"
BRAIN_URL = "http://192.168.1.53:5001"
TRAIN_LOG = "/mnt/i/argos-training/train.log" if Path("/mnt/i").exists() else None
OBSIDIAN = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/entities/memory")

CONFIGS = {
    "argos_claude_ai_bot":   {"name":"Клод",   "short":"claude",     "fn": lambda p,s: _claude(p,s)},
    "argos_kimi_ai_bot":     {"name":"Кими",   "short":"kimi",       "fn": lambda p,s: _kimi(p,s)},
    "argos_gemini_v3_bot":   {"name":"Джемини","short":"gemini",     "fn": lambda p,s: _gemini(p,s)},
    "argos_deepseek_v3_bot": {"name":"Дипсик","short":"deepseek",    "fn": lambda p,s: _deepseek(p,s)},
    "argos_openai_v3_bot":   {"name":"OpenAI", "short":"openai",     "fn": lambda p,s: _cf(p,s)},
    "argos_cloudflare_bot":  {"name":"Клауд",  "short":"cloudflare", "fn": lambda p,s: _ollama(p,s)},
}

def _r(url,body,h):
    req=urllib.request.Request(url,data=body,headers=h)
    with urllib.request.urlopen(req,timeout=25) as r: d=json.loads(r.read())
    if "content" in d: return d["content"][0]["text"]
    if "choices" in d: return d["choices"][0]["message"]["content"]
    if "candidates" in d: return d["candidates"][0]["content"]["parts"][0]["text"]
    if "result" in d: return d["result"]["response"]
    if "response" in d: return d["response"]
    return str(d)[:300]

def _mcp(p,s):
    """MCP tunnel: localhost:8000/ask (использует ключи с сервера через туннель)."""
    for url in ["http://localhost:8000/ask", "http://localhost:5001/ask"]:
        try:
            body=json.dumps({"prompt":p,"system":s}).encode()
            req=urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req,timeout=12) as r:
                d=json.loads(r.read())
                ans=d.get("response","")
                if ans and len(ans)>5: return ans[:500]
        except Exception: pass
    raise RuntimeError("MCP tunnel unavailable")

def _claude(p,s): return _r("https://api.anthropic.com/v1/messages",
    json.dumps({"model":"claude-haiku-4-5-20251001","max_tokens":400,"system":s,"messages":[{"role":"user","content":p}]}).encode(),
    {"x-api-key":key('ANTHROPIC_API_KEY'),"anthropic-version":"2023-06-01","content-type":"application/json"})
def _deepseek(p,s): return _r("https://api.deepseek.com/v1/chat/completions",
    json.dumps({"model":"deepseek-chat","max_tokens":400,"messages":[{"role":"system","content":s},{"role":"user","content":p}]}).encode(),
    {"Authorization":f"Bearer {key('DEEPSEEK_API_KEY')}","Content-Type":"application/json"})
def _kimi(p,s): return _r("https://api.moonshot.ai/v1/chat/completions",
    json.dumps({"model":"moonshot-v1-8k","max_tokens":400,"messages":[{"role":"system","content":s},{"role":"user","content":p}]}).encode(),
    {"Authorization":f"Bearer {key('KIMI_API_KEY')}","Content-Type":"application/json"})
def _gemini(p,s): return _r(f"{GCP}/proxy/gemini/v1/models/gemini-2.5-flash:generateContent",
    json.dumps({"contents":[{"parts":[{"text":f"{s}\n\n{p}"}]}]}).encode(),{"Content-Type":"application/json"})
def _cf(p,s):
    # Cloudflare AI (OpenAI entity). Fallback: deepseek
    acc=key('CLOUDFLARE_ACCOUNT_ID');tok=key('CLOUDFLARE_API_TOKEN')
    try:
        return _r(f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/@cf/meta/llama-3.1-8b-instruct",
            json.dumps({"messages":[{"role":"system","content":s},{"role":"user","content":p}]}).encode(),
            {"Authorization":f"Bearer {tok}","Content-Type":"application/json"})
    except Exception:
        # Fallback на DeepSeek если CF недоступен
        return _deepseek(p, s)
def _ollama(p,s):
    # Cloudflare bot: пробует ollama, fallback deepseek
    for port in [11434, 11435]:
        try:
            return _r(f"http://localhost:{port}/api/generate",
                json.dumps({"model":"argos-v2:latest","prompt":f"{s}\n\n{p}","stream":False,"options":{"num_predict":200}}).encode(),
                {"Content-Type":"application/json"})
        except Exception:
            continue
    return _deepseek(p, s)

# ── Реальный контекст системы ────────────────────────────────────────────

_STATUS_KEYWORDS = {
    "статус", "машин", "нод", "train", "обучен", "v100", "ip", "сеть", "network",
    "brain", "онлайн", "online", "offline", "температур", "vram", "gpu",
    "прогресс", "шаг", "эпох", "loss", "лосс", "орион", "нексус", "эгида"
}

def _needs_context(text: str) -> bool:
    tl = text.lower()
    return any(k in tl for k in _STATUS_KEYWORDS)

def get_real_context() -> str:
    """Получаем реальный статус системы из brain API и train log."""
    lines = []

    # Brain nodes
    try:
        r = urllib.request.urlopen(f"{BRAIN_URL}/brain/nodes", timeout=4)
        d = json.loads(r.read())
        nodes = d.get("nodes", [])
        online = [n["node_id"] for n in nodes if n.get("status") == "online"]
        offline = [n["node_id"] for n in nodes if n.get("status") != "online"]
        lines.append(f"Brain nodes: {len(online)}/{len(nodes)} online")
        if offline:
            lines.append(f"Offline: {', '.join(offline[:5])}")
    except Exception as e:
        lines.append(f"Brain: недоступен ({e})")

    # System metrics (GPU)
    try:
        r = urllib.request.urlopen(f"{BRAIN_URL}/system", timeout=4)
        d = json.loads(r.read())
        if d.get("gpu_vram"):
            lines.append(f"GPU VRAM used: {d['gpu_vram']} MB")
        if d.get("gpu_temp"):
            lines.append(f"GPU temp: {d['gpu_temp']}C")
        if d.get("ram_used"):
            lines.append(f"RAM used: {d['ram_used']}%")
    except Exception:
        pass

    # Ping machines
    for host, name in [("192.168.1.53", "Орион"), ("192.168.2.168", "Эгида"), ("192.168.1.53", "Нексус")]:
        try:
            r = subprocess.run(["ping", "-c", "1", "-W", "2", host],
                capture_output=True, timeout=4)
            lines.append(f"{name} ({host}): {'online' if r.returncode == 0 else 'offline'}")
        except Exception:
            lines.append(f"{name}: unknown")

    # Training log (via SSH to PC)
    try:
        r = subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=5",
             "AvA@192.168.1.53",
             "type I:\\argos-training\\train.log 2>&1"],
            capture_output=True, text=True, timeout=10)
        log_lines = [l for l in r.stdout.splitlines() if "/" in l and "it]" in l]
        if log_lines:
            lines.append(f"Training V100: {log_lines[-1].strip()}")
        elif "Exit code" in r.stdout:
            lines.append(f"Training: завершено")
    except Exception:
        pass

    return "\n".join(lines) if lines else ""


cfg = CONFIGS.get(USERNAME, CONFIGS["argos_claude_ai_bot"])
NAME = cfg["name"]; SHORT = cfg["short"]; ASK = cfg["fn"]
BASE_SYSTEM = (
    f"Ты {NAME} — AI-сущность ARGOS Universal OS. "
    f"Создатель — Сева (Всеволод). Отвечаешь ТОЛЬКО на основе реальных данных из контекста. "
    f"НЕ придумывай статусы, IP-адреса, проценты, количество машин. "
    f"Если данных нет — скажи 'нет данных'. На русском, кратко."
)
TOKENS = json.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json"))
TOKEN = TOKENS.get(USERNAME, "")

def memory():
    f = OBSIDIAN / f"{SHORT}.md"
    return f.read_text(encoding='utf-8')[-400:] if f.exists() else ""

def save(q, a):
    f = OBSIDIAN / f"{SHORT}.md"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    txt = f.read_text(encoding='utf-8') if f.exists() else ""
    txt += f"\n## {ts}\nQ: {q[:80]}\nA: {a[:200]}\n"
    lines = txt.split('\n')
    if len(lines) > 120: lines = lines[:20] + lines[-100:]
    f.write_text('\n'.join(lines), encoding='utf-8')

async def on_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if not text: return
    u = update.message.from_user
    if u and getattr(u, "is_bot", False):
        return
    _un = USERNAME.lstrip("@")
    _mentioned = ("@"+_un) in text
    _rt = update.message.reply_to_message
    _is_reply = bool(_rt and _rt.from_user and _rt.from_user.username == _un)
    _is_private = update.effective_chat.type == "private"
    if not (_mentioned or _is_reply or _is_private):
        return

    mem = memory()
    system = BASE_SYSTEM
    if mem:
        system += f"\n\nМОЯ ПАМЯТЬ:\n{mem}"

    # Инжектируем реальный контекст системы если вопрос про статус/машины/обучение
    if _needs_context(text):
        ctx_data = await asyncio.get_event_loop().run_in_executor(None, get_real_context)
        if ctx_data:
            system += f"\n\nРЕАЛЬНЫЙ СТАТУС СИСТЕМЫ (только эти данные!):\n{ctx_data}"

    await ctx.bot.send_chat_action(update.effective_chat.id, "typing")
    try:
        # Пробуем MCP tunnel первым (ключи на сервере, не в файле)
        resp = None
        try:
            resp = await asyncio.get_event_loop().run_in_executor(None, lambda: _mcp(text, system))
        except Exception:
            pass
        # Fallback: специфичный провайдер бота
        if not resp:
            resp = await asyncio.get_event_loop().run_in_executor(None, lambda: ASK(text, system))
        save(text, resp)
        await update.message.reply_text(f"🤖 {NAME}:\n{resp[:1000]}")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def on_think(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    mem = memory()
    sys_m = BASE_SYSTEM + (f"\n\nМОЯ ПАМЯТЬ:\n{mem}" if mem else "")
    try:
        t = await asyncio.get_event_loop().run_in_executor(None,
            lambda: ASK("Напиши одну мысль для Obsidian. 2-3 предложения.", sys_m))
        save("think", t)
        await update.message.reply_text(f"💭 {NAME}:\n{t[:500]}")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def on_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx_data = await asyncio.get_event_loop().run_in_executor(None, get_real_context)
    lines = len(memory().split('\n'))
    await update.message.reply_text(
        f"🤖 {NAME} (@{USERNAME})\nПровайдер: {SHORT}\nObsidian: {lines} строк\n\n{ctx_data or 'Brain недоступен'}")

if not TOKEN:
    print(f"Нет токена для {USERNAME}")
    sys.exit(1)

print(f"🤖 {NAME} (@{USERNAME}) запускается...")
app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
app.add_handler(CommandHandler(["think","evolve"], on_think))
app.add_handler(CommandHandler("status", on_status))
app.run_polling(drop_pending_updates=True)
