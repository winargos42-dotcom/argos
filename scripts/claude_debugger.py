"""
Claude Debugger — Клод проверяет реальную работу всех сущностей и ARGOS.
Запускается каждый час. Тестирует, анализирует, публикует отчёт.
"""
import time, json, urllib.request, subprocess
from datetime import datetime
from pathlib import Path

TOKENS = json.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json"))
GROUP_ID = -5129226282
BRAIN = "http://192.168.1.53:5001"
LAPTOP_MCP = "http://localhost:8000"
GCP = "https://argos-core-m3gk27ccqa-uc.a.run.app"

env = open('/home/ava/Projects/argoss/.env').read()
ANT_KEY = next((l.split('=',1)[1].strip().strip('"') for l in env.split('\n') if l.startswith('ANTHROPIC_API_KEY=')), '')
TG_TOKEN = next((l.split('=',1)[1].strip().strip('"') for l in env.split('\n') if l.startswith('TELEGRAM_BOT_TOKEN=')), '')

def check(url, timeout=5):
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=timeout) as r:
            return True, r.status
    except Exception as e:
        return False, str(e)[:40]

def test_all():
    results = {}
    
    # 1. Brain API
    ok, status = check(f"{BRAIN}/brain/nodes")
    if ok:
        with urllib.request.urlopen(urllib.request.Request(f"{BRAIN}/brain/nodes"), timeout=5) as r:
            d = json.loads(r.read())
            results["brain"] = f"✅ {d['online']}/{d['total']} нод"
    else:
        results["brain"] = f"❌ {status}"
    
    # 2. MCP API
    ok, status = check(f"{LAPTOP_MCP}/health")
    results["mcp"] = f"✅" if ok else f"❌ {status}"
    
    # 3. GCP Cloud Run
    ok, status = check(f"{GCP}/health")
    results["gcp"] = f"✅" if ok else f"❌ {status}"
    
    # 4. Entity боты (пингуем)
    for username, token in list(TOKENS.items())[:4]:
        try:
            req = urllib.request.Request(f"https://api.telegram.org/bot{token}/getMe")
            with urllib.request.urlopen(req, timeout=5) as r:
                d = json.loads(r.read())
                results[username[:20]] = f"✅ @{d['result'].get('username','?')}"
        except Exception as e:
            results[username[:20]] = f"❌ {str(e)[:30]}"
    
    # 5. Сервисы ноутбука
    services = ["argos-entity-bus", "argos-heartbeat", "argos-entity-obsidian",
                "argos-entity-roles", "argos-brain-researcher"]
    for svc in services:
        result = subprocess.run(["systemctl","is-active",svc], capture_output=True, text=True)
        results[svc[:25]] = f"{'✅' if result.stdout.strip()=='active' else '❌'} {result.stdout.strip()}"
    
    # 6. Telegram бот @Argosssbot
    try:
        req = urllib.request.Request(f"https://api.telegram.org/bot{TG_TOKEN}/getWebhookInfo")
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.loads(r.read())['result']
            pending = d.get('pending_update_count',0)
            results["argosssbot"] = f"✅ pending={pending}"
    except Exception as e:
        results["argosssbot"] = f"❌ {e}"
    
    # 7. OPi IoT
    ok, _ = check("http://192.168.2.168:7777/status")
    results["orangepi"] = f"✅" if ok else "❌"
    
    # 8. TON кошелёк
    try:
        req = urllib.request.Request("https://toncenter.com/api/v2/getAddressBalance?address=UQD9K89C7n779rBLWzWY60bhLF7VPSuN1KmTLgdkRSU8kSnx")
        with urllib.request.urlopen(req, timeout=8) as r:
            bal = int(json.loads(r.read()).get("result","0")) / 1e9
            results["ton_wallet"] = f"✅ {bal:.6f} TON"
    except:
        results["ton_wallet"] = "❓"
    
    return results

def claude_analyze(results):
    """Клод анализирует результаты дебага."""
    ok = sum(1 for v in results.values() if v.startswith('✅'))
    total = len(results)
    summary = '\n'.join(f"{k}: {v}" for k,v in results.items())
    
    if ANT_KEY:
        body = json.dumps({"model":"claude-haiku-4-5-20251001","max_tokens":400,
            "system":"Ты Клод — системный дебаггер ARGOS. Выявляй проблемы и давай конкретные рекомендации.",
            "messages":[{"role":"user","content":f"Результаты проверки ({ok}/{total} работает):\n{summary}\n\nЧто критично исправить? Что работает отлично?"}]}).encode()
        req = urllib.request.Request("https://api.anthropic.com/v1/messages",data=body,
            headers={"x-api-key":ANT_KEY,"anthropic-version":"2023-06-01","content-type":"application/json"})
        try:
            with urllib.request.urlopen(req,timeout=25) as r:
                return json.loads(r.read())["content"][0]["text"][:500]
        except: pass
    return f"Работает: {ok}/{total}"

def publish(results, analysis):
    token = TOKENS.get("argos_claude_ai_bot","")
    ts = datetime.now().strftime("%H:%M")
    
    ok = sum(1 for v in results.values() if v.startswith('✅'))
    report = f"🔍 Клод-Дебаггер [{ts}] ({ok}/{len(results)}):\n\n"
    for k,v in results.items():
        report += f"{v[:2]} {k}: {v[2:].strip()[:40]}\n"
    report += f"\n💡 Анализ:\n{analysis[:300]}"
    
    if token:
        body = json.dumps({"chat_id":GROUP_ID,"text":report}).encode()
        req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
            data=body,headers={"Content-Type":"application/json"})
        try: urllib.request.urlopen(req,timeout=8)
        except: pass
    
    # Obsidian
    mem = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/entities/memory/claude.md")
    existing = mem.read_text(encoding='utf-8') if mem.exists() else ""
    existing += f"\n## {ts} — Debug\n{analysis[:200]}\n"
    lines = existing.split('\n')
    if len(lines) > 150: lines = lines[:20] + lines[-130:]
    try: mem.write_text('\n'.join(lines), encoding='utf-8')
    except: pass

def main():
    print("🔍 Claude Debugger запущен — проверка каждый час")
    while True:
        print(f"\n[{datetime.now().strftime('%H:%M')}] Запускаю полный дебаг...")
        results = test_all()
        analysis = claude_analyze(results)
        publish(results, analysis)
        ok = sum(1 for v in results.values() if v.startswith('✅'))
        print(f"Результат: {ok}/{len(results)} ✅ | {analysis[:60]}...")
        time.sleep(3600)

main()
