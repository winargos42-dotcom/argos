"""
Brain Researcher — сущность Кими постоянно изучает Brain API,
анализирует ноды, выявляет паттерны и записывает в Obsidian.
"""
import asyncio, json, time, urllib.request
from pathlib import Path
from datetime import datetime

BRAIN = "http://192.168.1.53:5001"
KIMI_TOKEN = json.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json")).get("argos_kimi_ai_bot","")
GROUP_ID = -5129226282
OBSIDIAN = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/entities/memory/kimi.md")
INTERVAL = 1800  # 30 мин

env = open('/home/ava/Projects/argoss/.env').read()
KIMI_KEY = next((l.split('=',1)[1].strip().strip('"') for l in env.split('\n') if l.startswith('KIMI_API_KEY=')), '')
GCP = "https://argos-core-m3gk27ccqa-uc.a.run.app"

def get_brain_data():
    """Читаем все данные Brain API."""
    data = {}
    endpoints = [
        ("/brain/nodes", "nodes"),
        ("/health", "health"),
    ]
    for path, key in endpoints:
        try:
            req = urllib.request.Request(f"{BRAIN}{path}")
            with urllib.request.urlopen(req, timeout=5) as r:
                data[key] = json.loads(r.read())
        except Exception as e:
            data[key] = {"error": str(e)}
    return data

def analyze_with_kimi(brain_data: dict) -> str:
    """Кими анализирует данные Brain."""
    body = json.dumps({"model":"moonshot-v1-8k","max_tokens":400,"messages":[
        {"role":"system","content":"Ты Кими — исследователь AI-системы ARGOS. Анализируй данные и выявляй паттерны."},
        {"role":"user","content":f"Проанализируй данные Brain API ARGOS:\n{json.dumps(brain_data,ensure_ascii=False,indent=2)[:1500]}\n\nЧто важного ты заметил? Что изменилось? Какие рекомендации?"}
    ]}).encode()
    req = urllib.request.Request("https://api.moonshot.ai/v1/chat/completions",data=body,
        headers={"Authorization":f"Bearer {KIMI_KEY}","Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=25) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"][:500]
    except Exception as e:
        # Fallback через GCP
        body2 = json.dumps({"prompt":f"Ты Кими-исследователь ARGOS. Данные Brain: {json.dumps(brain_data)[:800]}. Кратко - что важного?","provider":"claude"}).encode()
        req2 = urllib.request.Request(f"{GCP}/proxy/ask",data=body2,headers={"Content-Type":"application/json"})
        try:
            with urllib.request.urlopen(req2,timeout=20) as r2:
                return json.loads(r2.read()).get("response","")[:400]
        except:
            return f"Ошибка анализа: {e}"

def publish(text: str):
    """Публикуем в группу и Obsidian."""
    # Telegram
    if KIMI_TOKEN:
        body = json.dumps({"chat_id":GROUP_ID,"text":f"🔬 Кими-Исследователь Brain:\n{text}"}).encode()
        req = urllib.request.Request(f"https://api.telegram.org/bot{KIMI_TOKEN}/sendMessage",
            data=body,headers={"Content-Type":"application/json"})
        try: urllib.request.urlopen(req,timeout=8)
        except: pass
    
    # Obsidian
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        existing = OBSIDIAN.read_text(encoding='utf-8') if OBSIDIAN.exists() else ""
        existing += f"\n## {ts} — Brain Research\n{text[:300]}\n"
        lines = existing.split('\n')
        if len(lines) > 150: lines = lines[:20] + lines[-130:]
        OBSIDIAN.write_text('\n'.join(lines), encoding='utf-8')
    except: pass

def main():
    print("🔬 Brain Researcher (Кими) запущен — мониторинг каждые 30 мин")
    prev_data = {}
    
    while True:
        brain = get_brain_data()
        
        # Сравниваем с предыдущим
        nodes = brain.get("nodes",{})
        online = nodes.get("online",0)
        total = nodes.get("total",0)
        prev_online = prev_data.get("online",0)
        
        changes = []
        if online != prev_online:
            changes.append(f"Ноды: {prev_online}→{online}/{total}")
        
        # Анализ
        analysis = analyze_with_kimi(brain)
        
        report = f"Brain: {online}/{total} нод\n"
        if changes: report += f"Изменения: {', '.join(changes)}\n"
        report += f"\nАнализ:\n{analysis}"
        
        publish(report)
        print(f"[{datetime.now().strftime('%H:%M')}] Brain: {online}/{total} нод")
        
        prev_data = {"online": online, "total": total}
        time.sleep(INTERVAL)

main()
