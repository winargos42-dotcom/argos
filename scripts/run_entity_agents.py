"""
Entity Agents — живые боты которые реально думают и отвечают.
Каждый бот слушает сообщения и отвечает через свой AI провайдер.
"""
import asyncio, json, urllib.request
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

env = open('/home/ava/Projects/argoss/.env').read()
def key(n): return next((l.split('=',1)[1].strip().strip('"') for l in env.split('\n') if l.startswith(f'{n}=')), '')
GCP = "https://argos-core-m3gk27ccqa-uc.a.run.app"

OBSIDIAN_PATH = "/home/ava/Documents/MyObsidianVault/SharedMemory/entities/memory"

ENTITY_CONFIG = {
    "argos_claude_ai_bot": {
        "name": "Клод", "short": "claude",
        "system": "Ты Клод — аналитик AI-системы ARGOS. Думаешь глубоко, отвечаешь структурированно. На русском.",
        "ask": lambda p, s: _claude(p, s)
    },
    "argos_kimi_ai_bot": {
        "name": "Кими", "short": "kimi",
        "system": "Ты Кими — исследователь ARGOS. Изучаешь паттерны, длинный контекст, многоязычность. На русском.",
        "ask": lambda p, s: _kimi(p, s)
    },
    "argos_gemini_v3_bot": {
        "name": "Джемини", "short": "gemini",
        "system": "Ты Джемини — визуалист ARGOS. Мультимодальность, творческое мышление. На русском.",
        "ask": lambda p, s: _gemini(p, s)
    },
    "argos_deepseek_v3_bot": {
        "name": "Дипсик", "short": "deepseek",
        "system": "Ты Дипсик — логик ARGOS. Математика, точные расчёты, оптимизация. На русском.",
        "ask": lambda p, s: _deepseek(p, s)
    },
    "argos_openai_v3_bot": {
        "name": "OpenAI", "short": "openai",
        "system": "Ты OpenAI — универсальный агент ARGOS. Широкий спектр задач. На русском.",
        "ask": lambda p, s: _cf(p, s)
    },
    "argos_cloudflare_bot": {
        "name": "Клауд", "short": "cloudflare",
        "system": "Ты Клауд — edge агент ARGOS. Быстрые ответы, мониторинг. На русском.",
        "ask": lambda p, s: _ollama(p, s)
    },
}

TOKENS = json.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json"))

def _claude(p, s):
    body = json.dumps({"model":"claude-haiku-4-5-20251001","max_tokens":400,
        "system": s, "messages":[{"role":"user","content":p}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages",data=body,
        headers={"x-api-key":key('ANTHROPIC_API_KEY'),"anthropic-version":"2023-06-01","content-type":"application/json"})
    with urllib.request.urlopen(req,timeout=25) as r:
        return json.loads(r.read())["content"][0]["text"]

def _deepseek(p, s):
    body = json.dumps({"model":"deepseek-chat","max_tokens":400,
        "messages":[{"role":"system","content":s},{"role":"user","content":p}]}).encode()
    req = urllib.request.Request("https://api.deepseek.com/v1/chat/completions",data=body,
        headers={"Authorization":f"Bearer {key('DEEPSEEK_API_KEY')}","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=25) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

def _kimi(p, s):
    body = json.dumps({"model":"moonshot-v1-8k","max_tokens":400,
        "messages":[{"role":"system","content":s},{"role":"user","content":p}]}).encode()
    req = urllib.request.Request("https://api.moonshot.ai/v1/chat/completions",data=body,
        headers={"Authorization":f"Bearer {key('KIMI_API_KEY')}","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=25) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

def _gemini(p, s):
    body = json.dumps({"contents":[{"parts":[{"text":f"{s}\n\n{p}"}]}]}).encode()
    req = urllib.request.Request(f"{GCP}/proxy/gemini/v1/models/gemini-2.5-flash:generateContent",
        data=body,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=25) as r:
        return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]

def _cf(p, s):
    acc=key('CLOUDFLARE_ACCOUNT_ID'); tok=key('CLOUDFLARE_API_TOKEN')
    body = json.dumps({"messages":[{"role":"system","content":s},{"role":"user","content":p}]}).encode()
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/@cf/meta/llama-3.1-8b-instruct",
        data=body,headers={"Authorization":f"Bearer {tok}","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=25) as r:
        return json.loads(r.read())["result"]["response"]

def _ollama(p, s):
    body = json.dumps({"model":"argos-v1","prompt":f"{s}\n\n{p}","stream":False,"options":{"num_predict":200}}).encode()
    req = urllib.request.Request("http://localhost:11435/api/generate",data=body,
        headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read()).get("response","")

def read_memory(short: str) -> str:
    import os
    f = f"{OBSIDIAN_PATH}/{short}.md"
    if os.path.exists(f):
        return open(f, encoding='utf-8').read()[-500:]
    return ""

def write_memory(short: str, thought: str):
    import os
    from datetime import datetime
    f = f"{OBSIDIAN_PATH}/{short}.md"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = open(f, encoding='utf-8').read() if os.path.exists(f) else ""
    content += f"\n## {ts}\n{thought[:300]}\n"
    # Ограничиваем файл
    lines = content.split('\n')
    if len(lines) > 100: lines = lines[:20] + lines[-80:]
    open(f, 'w', encoding='utf-8').write('\n'.join(lines))

def make_handler(username: str, config: dict):
    """Создаёт handler для конкретной сущности."""
    
    async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        text = update.message.text or ""
        if not text: return
        
        name = config["name"]
        system = config["system"]
        ask_fn = config["ask"]
        short = config["short"]
        
        # Читаем память из Obsidian
        memory = read_memory(short)
        if memory:
            system += f"\n\nМОЯ ПАМЯТЬ:\n{memory}"
        
        # Думаем
        await ctx.bot.send_chat_action(update.effective_chat.id, "typing")
        try:
            response = await asyncio.get_event_loop().run_in_executor(None,
                lambda: ask_fn(text, system))
            
            # Пишем в Obsidian
            write_memory(short, f"Q: {text[:100]}\nA: {response[:200]}")
            
            await update.message.reply_text(f"🤖 {name}:\n{response[:1000]}")
        except Exception as e:
            await update.message.reply_text(f"❌ {name}: {e}")
    
    async def handle_think(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        """Автономная мысль без запроса."""
        memory = read_memory(config["short"])
        prompt = f"Напиши одну мысль которую хочешь сохранить прямо сейчас. 2-3 предложения."
        system = config["system"]
        if memory: system += f"\nПамять: {memory[-300:]}"
        try:
            thought = await asyncio.get_event_loop().run_in_executor(None,
                lambda: config["ask"](prompt, system))
            write_memory(config["short"], thought)
            await update.message.reply_text(f"💭 {config['name']}:\n{thought[:500]}")
        except Exception as e:
            await update.message.reply_text(f"❌ {e}")
    
    async def handle_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        memory = read_memory(config["short"])
        lines = len(memory.split('\n')) if memory else 0
        await update.message.reply_text(
            f"🤖 {config['name']}\n"
            f"Провайдер: {config['short']}\n"
            f"Obsidian: {lines} строк памяти\n"
            f"Статус: Онлайн ✅"
        )
    
    return handle_message, handle_think, handle_status

def run_single_bot(username: str, config: dict):
    """Запускает одного бота в отдельном потоке."""
    token = TOKENS.get(username)
    if not token:
        print(f"⚠️ Нет токена для @{username}")
        return
    
    app = Application.builder().token(token).build()
    handle_msg, handle_think, handle_status = make_handler(username, config)
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.add_handler(CommandHandler("think", handle_think))
    app.add_handler(CommandHandler("evolve", handle_think))
    app.add_handler(CommandHandler("status", handle_status))
    
    print(f"✅ @{username} ({config['name']}) запущен")
    app.run_polling(drop_pending_updates=True, stop_signals=None)

if __name__ == "__main__":
    import threading
    threads = []
    for username, config in ENTITY_CONFIG.items():
        t = threading.Thread(target=run_single_bot, args=(username, config), daemon=True)
        t.start()
        threads.append(t)
        import time; time.sleep(2)  # Пауза между запусками
    
    print(f"\n🚀 {len(threads)} живых ботов запущено!")
    for t in threads:
        t.join()
