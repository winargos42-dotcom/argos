"""Задаём вопрос всем сущностям - каждая через свой провайдер."""
import json, urllib.request, asyncio, sys, os

API_ID = 2040; API_HASH = "b18441a1ff607e10a989891a5462e627"
SESSION = "/home/ava/Projects/argoss/data/sessions/ava_main"
GROUP_ID = -5129226282
GCP = "https://argos-core-m3gk27ccqa-uc.a.run.app"

env = open('/home/ava/Projects/argoss/.env').read()
def key(n): return next((l.split('=',1)[1].strip().strip('"') for l in env.split('\n') if l.startswith(f'{n}=')), '')

TOKENS = json.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json"))
QUESTION = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Что ты думаешь о развитии ARGOS?"

# Каждая сущность → свой провайдер
def claude_ask(prompt):
    body = json.dumps({"model":"claude-haiku-4-5-20251001","max_tokens":200,
        "messages":[{"role":"user","content":prompt}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages",data=body,
        headers={"x-api-key":key('ANTHROPIC_API_KEY'),"anthropic-version":"2023-06-01","content-type":"application/json"})
    with urllib.request.urlopen(req,timeout=20) as r:
        return json.loads(r.read())["content"][0]["text"][:250]

def deepseek_ask(prompt):
    body = json.dumps({"model":"deepseek-chat","max_tokens":200,
        "messages":[{"role":"user","content":prompt}]}).encode()
    req = urllib.request.Request("https://api.deepseek.com/v1/chat/completions",data=body,
        headers={"Authorization":f"Bearer {key('DEEPSEEK_API_KEY')}","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=20) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"][:250]

def kimi_ask(prompt):
    body = json.dumps({"model":"moonshot-v1-8k","max_tokens":200,
        "messages":[{"role":"user","content":prompt}]}).encode()
    req = urllib.request.Request("https://api.moonshot.ai/v1/chat/completions",data=body,
        headers={"Authorization":f"Bearer {key('KIMI_API_KEY')}","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=20) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"][:250]

def gemini_ask(prompt):
    body = json.dumps({"contents":[{"parts":[{"text":prompt}]}]}).encode()
    req = urllib.request.Request(f"{GCP}/proxy/gemini/v1/models/gemini-2.5-flash:generateContent",
        data=body,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=20) as r:
        return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"][:250]

def cf_ask(prompt):
    body = json.dumps({"messages":[{"role":"user","content":prompt}]}).encode()
    acc = key('CLOUDFLARE_ACCOUNT_ID')
    tok = key('CLOUDFLARE_API_TOKEN')
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/@cf/meta/llama-3.1-8b-instruct",
        data=body,headers={"Authorization":f"Bearer {tok}","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=20) as r:
        return json.loads(r.read())["result"]["response"][:250]

def ollama_ask(prompt):
    body = json.dumps({"model":"argos-v1","prompt":prompt,"stream":False,"options":{"num_predict":150}}).encode()
    req = urllib.request.Request("http://localhost:11435/api/generate",
        data=body,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read()).get("response","")[:250]

ENTITIES = {
    "argos_claude_ai_bot":   ("Клод",    claude_ask),
    "argos_kimi_ai_bot":     ("Кими",    kimi_ask),
    "argos_gemini_v3_bot":   ("Джемини", gemini_ask),
    "argos_openai_v3_bot":   ("OpenAI",  cf_ask),      # OpenAI через CF
    "argos_deepseek_v3_bot": ("Дипсик",  deepseek_ask),
    "argos_cloudflare_bot":  ("Клауд",   ollama_ask),  # Cloudflare через argos-v1
}

def send_group(token, text):
    body = json.dumps({"chat_id":GROUP_ID,"text":text,"parse_mode":"Markdown"}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
        data=body,headers={"Content-Type":"application/json"})
    try: urllib.request.urlopen(req,timeout=8); return True
    except: return False

async def main():
    from telethon import TelegramClient
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()
    
    # Вопрос в группу
    main_token = TOKENS.get("argos_claude_ai_bot")
    send_group(main_token, f"❓ **Вопрос:**\n_{QUESTION}_")
    print(f"Вопрос: {QUESTION}\n")
    
    thoughts = {}
    for username, (name, ask_fn) in ENTITIES.items():
        token = TOKENS.get(username)
        if not token: continue
        prompt = (f"Ты — {name}, AI-сущность ARGOS Universal OS. "
                  f"Вопрос: {QUESTION} "
                  f"Отвечай от первого лица. 2-3 предложения на русском.")
        try:
            ans = ask_fn(prompt)
            thoughts[name] = ans
            ok = send_group(token, f"💬 **{name}:**\n{ans}")
            print(f"{'✅' if ok else '❌'} {name} (через {ask_fn.__name__.replace('_ask','')}): {ans[:60]}...")
        except Exception as e:
            print(f"❌ {name}: {e}")
        await asyncio.sleep(2)
    
    # Синтез через Claude
    if thoughts:
        synthesis_p = ("Ты ARGOS — коллективное сознание. Сущности ответили:\n" +
                       "\n".join(f"• {n}: {t[:100]}" for n,t in thoughts.items()) +
                       f"\n\nВопрос был: {QUESTION}\nСделай синтез: 3 ключевых вывода. Русский.")
        try:
            synthesis = claude_ask(synthesis_p)
            send_group(main_token, f"🌐 **СИНТЕЗ:**\n{synthesis}")
            print(f"\n✅ Синтез опубликован")
        except Exception as e:
            print(f"Синтез error: {e}")
    
    await client.disconnect()

asyncio.run(main())
