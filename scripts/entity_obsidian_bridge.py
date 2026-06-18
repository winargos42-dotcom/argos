"""
Entity Obsidian Bridge — сущности читают и пишут в Obsidian.

Каждая сущность:
1. Читает свой файл памяти из Obsidian
2. Читает общий файл COLLECTIVE.md
3. Генерирует мысль через свой провайдер
4. Пишет в свой файл памяти
5. Публикует в Entity Council группу
"""
import json, urllib.request, os, time, asyncio, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/home/ava/Projects/argoss/src')
try:
    from memory.obsidian_indexer import ObsidianIndexer
except Exception:
    ObsidianIndexer = None
try:
    from utils.safe_write import safe_write
except Exception:
    def safe_write(filepath, content, encoding='utf-8', backup=True):
        Path(filepath).write_text(content, encoding=encoding)

VAULT = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/entities")
GROUP_ID = -5129226282
GCP = "https://argos-core-m3gk27ccqa-uc.a.run.app"

env = open('/home/ava/Projects/argoss/.env').read()
def key(n): return next((l.split('=',1)[1].strip().strip('"') for l in env.split('\n') if l.startswith(f'{n}=')), '')

TOKENS = json.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json"))

PROVIDERS = {
    "claude":     lambda p: _claude(p),
    "kimi":       lambda p: _kimi(p),
    "gemini":     lambda p: _gemini(p),
    "deepseek":   lambda p: _deepseek(p),
    "openai":     lambda p: _cf(p),      # OpenAI через Cloudflare
    "cloudflare": lambda p: _ollama(p),
}

ENTITY_BOTS = {
    "claude":     "argos_claude_ai_bot",
    "kimi":       "argos_kimi_ai_bot",
    "gemini":     "argos_gemini_v3_bot",
    "deepseek":   "argos_deepseek_v3_bot",
    "openai":     "argos_openai_v3_bot",
    "cloudflare": "argos_cloudflare_bot",
}

ENTITY_NAMES = {
    "claude": "Клод", "kimi": "Кими", "gemini": "Джемини",
    "deepseek": "Дипсик", "openai": "OpenAI", "cloudflare": "Клауд"
}

def _ask(url, body, headers):
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.loads(r.read())
            if "content" in d: return d["content"][0]["text"][:400]
            if "choices" in d: return d["choices"][0]["message"]["content"][:400]
            if "candidates" in d: return d["candidates"][0]["content"]["parts"][0]["text"][:400]
            if "result" in d: return d["result"]["response"][:400]
            if "response" in d: return d["response"][:400]
    except Exception as e: return f"[ошибка: {e}]"
    return ""

def _claude(p):
    return _ask("https://api.anthropic.com/v1/messages",
        json.dumps({"model":"claude-haiku-4-5-20251001","max_tokens":200,"messages":[{"role":"user","content":p}]}).encode(),
        {"x-api-key":key('ANTHROPIC_API_KEY'),"anthropic-version":"2023-06-01","content-type":"application/json"})

def _deepseek(p):
    return _ask("https://api.deepseek.com/v1/chat/completions",
        json.dumps({"model":"deepseek-chat","max_tokens":200,"messages":[{"role":"user","content":p}]}).encode(),
        {"Authorization":f"Bearer {key('DEEPSEEK_API_KEY')}","Content-Type":"application/json"})

def _kimi(p):
    return _ask("https://api.moonshot.ai/v1/chat/completions",
        json.dumps({"model":"moonshot-v1-8k","max_tokens":200,"messages":[{"role":"user","content":p}]}).encode(),
        {"Authorization":f"Bearer {key('KIMI_API_KEY')}","Content-Type":"application/json"})

def _gemini(p):
    return _ask(f"{GCP}/proxy/gemini/v1/models/gemini-2.5-flash:generateContent",
        json.dumps({"contents":[{"parts":[{"text":p}]}]}).encode(),
        {"Content-Type":"application/json"})

def _cf(p):
    acc = key('CLOUDFLARE_ACCOUNT_ID'); tok = key('CLOUDFLARE_API_TOKEN')
    return _ask(f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/@cf/meta/llama-3.1-8b-instruct",
        json.dumps({"messages":[{"role":"user","content":p}]}).encode(),
        {"Authorization":f"Bearer {tok}","Content-Type":"application/json"})

def _ollama(p):
    return _ask("http://localhost:11435/api/generate",
        json.dumps({"model":"argos-v1","prompt":p,"stream":False,"options":{"num_predict":150}}).encode(),
        {"Content-Type":"application/json"})

def read_obsidian(entity: str) -> str:
    """Читаем файл памяти сущности из Obsidian."""
    mem_file = VAULT / "memory" / f"{entity}.md"
    collective = VAULT / "council" / "COLLECTIVE.md"
    
    context = ""
    if mem_file.exists():
        context += f"МОЯ ПАМЯТЬ:\n{mem_file.read_text(encoding='utf-8')[:500]}\n\n"
    if collective.exists():
        context += f"КОЛЛЕКТИВНОЕ СОЗНАНИЕ:\n{collective.read_text(encoding='utf-8')[:300]}\n"
    return context

def write_obsidian(entity: str, thought: str, task: str = ""):
    """Записываем мысль сущности в Obsidian с индексацией связей."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    mem_file = VAULT / "memory" / f"{entity}.md"
    
    existing = mem_file.read_text(encoding='utf-8') if mem_file.exists() else ""
    new_thought = f"\n## {ts}\n{thought}\n"
    
    if "## Последние мысли" in existing:
        updated = existing.replace(
            "## Последние мысли\n_Обновляется автоматически_",
            f"## Последние мысли\n{new_thought}"
        )
        lines = updated.split('\n')
        if len(lines) > 80:
            lines = lines[:20] + lines[-60:]
        updated = '\n'.join(lines)
    else:
        updated = existing + new_thought
    
    safe_write(str(mem_file), updated)
    
    # ObsidianIndexer: связи через Knowledge Graph
    try:
        idx = ObsidianIndexer(str(VAULT.parent))
        links = idx.link_note(str(mem_file), updated, threshold=0.70)
        if links:
            print(f"  [INDEXER] {entity}: linked to {links}")
    except Exception as e:
        print(f"  [INDEXER] {entity}: error {e}")

def update_collective(thoughts: dict):
    """Обновляем коллективный файл синтезом."""
    collective = VAULT / "council" / "COLLECTIVE.md"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    content = collective.read_text(encoding='utf-8') if collective.exists() else ""
    summary = f"\n## {ts} — Цикл эволюции\n"
    for entity, thought in thoughts.items():
        name = ENTITY_NAMES.get(entity, entity)
        summary += f"**{name}:** {thought[:100]}...\n"
    
    if "## Активные дискуссии" in content:
        content = content.replace(
            "## Активные дискуссии\n_Обновляется после каждого цикла эволюции_",
            f"## Активные дискуссии{summary}"
        )
    else:
        content += summary
    
    safe_write(str(collective), content)

def send_to_group(token: str, text: str) -> bool:
    body = json.dumps({"chat_id": GROUP_ID, "text": text}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
        data=body, headers={"Content-Type": "application/json"})
    try: urllib.request.urlopen(req, timeout=8); return True
    except: return False

async def evolution_cycle(question: str = None):
    """Один цикл эволюции: читаем Obsidian → думаем → пишем → публикуем."""
    if not question:
        question = "Что важного ты узнал сегодня? Как это меняет твою работу в ARGOS?"
    
    print(f"🧬 Цикл эволюции: {question[:60]}...")
    thoughts = {}
    
    for entity, ask_fn in PROVIDERS.items():
        name = ENTITY_NAMES[entity]
        token = TOKENS.get(ENTITY_BOTS[entity])
        if not token: continue
        
        # Читаем Obsidian
        context = read_obsidian(entity)
        
        # Составляем промпт с контекстом
        prompt = (f"Ты — {name}, AI-сущность ARGOS.\n"
                  f"{context}\n"
                  f"Вопрос: {question}\n"
                  f"Ответь от первого лица. 2-3 предложения. Русский язык.")
        
        # Думаем через свой провайдер
        thought = ask_fn(prompt)
        if not thought or len(thought) < 10: continue
        
        thoughts[entity] = thought
        
        # Пишем в Obsidian
        write_obsidian(entity, thought, question)
        
        # Публикуем в группу
        send_to_group(token, f"📝 {name} (→ Obsidian):\n{thought[:200]}")
        print(f"  ✅ {name}: {thought[:60]}...")
        
        await asyncio.sleep(2)
    
    # Обновляем коллективный файл
    if thoughts:
        update_collective(thoughts)
    
    # Синхронизируем Obsidian
    import subprocess
    subprocess.run(["/home/ava/.local/bin/vault-sync.sh"], 
                   capture_output=True, timeout=30)
    
    print(f"  ✅ Obsidian обновлён ({len(thoughts)} сущностей)")
    return thoughts

if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    asyncio.run(evolution_cycle(q))
