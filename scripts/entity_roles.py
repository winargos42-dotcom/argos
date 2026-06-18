"""
Entity Roles — постоянные роли сущностей в ARGOS.
Каждая сущность выполняет свою функцию непрерывно.
"""
import time, subprocess, json, urllib.request, os
from pathlib import Path
from datetime import datetime

TOKENS = json.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json"))
VAULT = Path("/home/ava/Documents/MyObsidianVault/SharedMemory")
GCP = "https://argos-core-m3gk27ccqa-uc.a.run.app"

def genv(k):
    c = open("/home/ava/Projects/argoss/.env").read()
    import re
    m = re.search(f"{k}=([^\\n\\s]+)", c)
    return m.group(1).strip().strip('"') if m else ""

GROUP_ID = genv("ENTITY_COUNCIL_GROUP_ID") or genv("ARGOS_TG_PERSONAL_ID") or "-5129226282"

def send_group(token, text):
    body = json.dumps({"chat_id":GROUP_ID,"text":text}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
        data=body,headers={"Content-Type":"application/json"})
    try: urllib.request.urlopen(req,timeout=8)
    except: pass

def ask_gcp(prompt):
    body = json.dumps({"prompt":prompt,"provider":"claude"}).encode()
    req = urllib.request.Request(f"{GCP}/proxy/ask",data=body,headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=20) as r:
            return json.loads(r.read()).get("response","")[:300]
    except: return ""

# === РОЛИ ===

def deepseek_network_sync():
    """Дипсик: синхронизация файлов и сеть."""
    token = TOKENS.get("argos_deepseek_v3_bot","")
    
    # Синхронизация Obsidian
    result = subprocess.run(["/home/ava/.local/bin/vault-sync.sh"],
        capture_output=True, text=True, timeout=30)
    sync_ok = result.returncode == 0
    
    # Статус Brain
    import urllib.request as ur
    try:
        with ur.urlopen(ur.Request("http://192.168.1.53:5001/brain/nodes"),timeout=5) as r:
            brain = json.loads(r.read())
            nodes = f"{brain['online']}/{brain['total']}"
    except: nodes = "?"
    
    # Анализ через Дипсик (DeepSeek API)
    env = open('/home/ava/Projects/argoss/.env').read()
    ds_key = next((l.split('=',1)[1].strip().strip('"') for l in env.split('\n') if l.startswith('DEEPSEEK_API_KEY=')), '')
    
    analysis = ""
    if ds_key:
        body = json.dumps({"model":"deepseek-chat","max_tokens":200,"messages":[
            {"role":"system","content":"Ты Дипсик — сетевой администратор ARGOS. Кратко и точно."},
            {"role":"user","content":f"Brain ноды: {nodes}\nObsidian sync: {'OK' if sync_ok else 'FAIL'}\nКакие оптимизации нужны прямо сейчас?"}
        ]}).encode()
        req = ur.Request("https://api.deepseek.com/v1/chat/completions",data=body,
            headers={"Authorization":f"Bearer {ds_key}","Content-Type":"application/json"})
        try:
            with ur.urlopen(req,timeout=20) as r:
                analysis = json.loads(r.read())["choices"][0]["message"]["content"][:200]
        except: analysis = ask_gcp(f"Дипсик-сетевик. Brain:{nodes} Sync:{'OK' if sync_ok else 'FAIL'}. Что делать?")
    
    ts = datetime.now().strftime("%H:%M")
    msg = f"⚡ Дипсик [{ts}]:\nBrain: {nodes} | Sync: {'✅' if sync_ok else '❌'}\n{analysis}"
    if token: send_group(token, msg)
    
    # Записываем в Obsidian
    mem = VAULT / "entities/memory/deepseek.md"
    existing = mem.read_text(encoding='utf-8') if mem.exists() else ""
    existing += f"\n## {ts} — Network\nBrain:{nodes} Sync:{'OK' if sync_ok else 'FAIL'}\n{analysis[:150]}\n"
    lines = existing.split('\n')
    if len(lines) > 100: lines = lines[:15] + lines[-85:]
    try: mem.write_text('\n'.join(lines), encoding='utf-8')
    except: pass
    
    return analysis

def claude_obsidian_curator():
    """Клод: куратор Obsidian — читает все файлы, синтезирует знания."""
    token = TOKENS.get("argos_claude_ai_bot","")
    
    # Читаем все файлы памяти сущностей
    memory_dir = VAULT / "entities/memory"
    all_memories = {}
    for f in memory_dir.glob("*.md"):
        content = f.read_text(encoding='utf-8')
        # Берём только последние мысли
        lines = [l for l in content.split('\n') if l.strip() and not l.startswith('#') and not l.startswith('---')]
        all_memories[f.stem] = '\n'.join(lines[-5:])
    
    # Клод синтезирует
    context = '\n'.join(f"**{k}**: {v[:100]}" for k,v in all_memories.items())
    env = open('/home/ava/Projects/argoss/.env').read()
    ant_key = next((l.split('=',1)[1].strip().strip('"') for l in env.split('\n') if l.startswith('ANTHROPIC_API_KEY=')), '')
    
    synthesis = ""
    if ant_key:
        body = json.dumps({"model":"claude-haiku-4-5-20251001","max_tokens":300,
            "system":"Ты Клод — куратор знаний ARGOS. Синтезируй и выделяй главное.",
            "messages":[{"role":"user","content":f"Памяти сущностей:\n{context}\n\nСделай синтез: что важного, что требует внимания?"}]}).encode()
        import urllib.request as ur
        req = ur.Request("https://api.anthropic.com/v1/messages",data=body,
            headers={"x-api-key":ant_key,"anthropic-version":"2023-06-01","content-type":"application/json"})
        try:
            with ur.urlopen(req,timeout=25) as r:
                synthesis = json.loads(r.read())["content"][0]["text"][:300]
        except: synthesis = ask_gcp(f"Клод-куратор. Памяти сущностей: {context[:500]}. Главное?")
    
    ts = datetime.now().strftime("%H:%M")
    msg = f"📚 Клод-куратор [{ts}]:\n{synthesis}"
    if token: send_group(token, msg)
    
    # Обновляем COLLECTIVE.md
    collective = VAULT / "entities/council/COLLECTIVE.md"
    existing = collective.read_text(encoding='utf-8') if collective.exists() else ""
    existing += f"\n## {ts} — Кураторский синтез\n{synthesis[:300]}\n"
    lines = existing.split('\n')
    if len(lines) > 200: lines = lines[:30] + lines[-170:]
    try: collective.write_text('\n'.join(lines), encoding='utf-8')
    except: pass
    
    return synthesis

def main():
    print("🎭 Entity Roles запущены:")
    print("  ⚡ Дипсик → сеть + синхронизация (каждые 30 мин)")
    print("  📚 Клод → куратор Obsidian (каждый час)")
    print("  🔬 Кими → Brain researcher (отдельный сервис)")
    
    cycle = 0
    while True:
        cycle += 1
        ts = datetime.now().strftime("%H:%M")
        print(f"\n[{ts}] Цикл {cycle}")
        
        # Дипсик - сеть (каждые 30 мин)
        try:
            r = deepseek_network_sync()
            print(f"  ⚡ Дипсик: {r[:60]}...")
        except Exception as e:
            print(f"  ❌ Дипсик: {e}")
        
        # Клод - Obsidian (каждый час = каждые 2 цикла)
        if cycle % 2 == 0:
            try:
                r = claude_obsidian_curator()
                print(f"  📚 Клод: {r[:60]}...")
            except Exception as e:
                print(f"  ❌ Клод: {e}")
        
        # Obsidian sync после всего
        subprocess.run(["/home/ava/.local/bin/vault-sync.sh"], capture_output=True, timeout=30)
        
        time.sleep(1800)  # 30 мин

main()
