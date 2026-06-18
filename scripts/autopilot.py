"""
ARGOS Autopilot — автономный дебаг, диалог с Claude TG, применение улучшений.
Запускается постоянно. Каждые 5 мин:
1. Читает новые сообщения Claude TG
2. Отвечает данными из системы
3. Применяет рекомендации автоматически
4. Дебажит все сервисы
5. Публикует статус в Entity Council
"""
import asyncio, time, json, subprocess, urllib.request, re, os
from pathlib import Path
from datetime import datetime

# Конфиг
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
SESSION_STRING = "1ApWapzMBu6HrKs4Hskwl5je2sFZvy1Um0JdQ3P1Bnw7d6AKxB5s8ullvY6EOauTnnGaNYNhN7wB2Iqo2PT-HiFr5V_8YdW489F0UDefjCx7O8TFPes_tqvu_aebEyZDcnlthFY3qTeZdLx-8186nlSu_k3F2jVnavHY5dWHE3V3cq9HxRjXKmNrGVlSz04Z1jsepJyVzdO69uDA7fnt794iH0Y8gvtFUEevgCI5KrkD8T_r7R-aGqPHGEiZkECsCKbY2O44XfPvITvzafnDhHV8Fh9p2EIO0hi3FbN3IO2fiBn5GlSkD8DTCUoFXVA9QzkE1ylhs4DT3zfu_btVPjZBsGuVEGiA="
SESSION = None  # используем StringSession
GROUP_ID = -5129226282
CLAUDE_TG = "@claude_gidbot"
CHECK_INTERVAL = 300  # 5 мин

env = open('/home/ava/Projects/argoss/.env').read()
TG_BOT_TOKEN = next((l.split('=',1)[1].strip().strip('"') for l in env.split('\n') if l.startswith('TELEGRAM_BOT_TOKEN=')), '')
ANT_KEY = next((l.split('=',1)[1].strip().strip('"') for l in env.split('\n') if l.startswith('ANTHROPIC_API_KEY=')), '')
TOKENS = json.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json"))

def send_tg(token, chat_id, text):
    body = json.dumps({"chat_id": chat_id, "text": text}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
        data=body, headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return json.loads(r.read())
    except: return {}

def get_system_data():
    """Собираем все реальные данные системы для ответа Клоду."""
    data = {}
    
    # Brain
    try:
        r = urllib.request.urlopen("http://192.168.1.53:5001/brain/nodes", timeout=5)
        d = json.loads(r.read())
        data["brain"] = f"{d['online']}/{d['total']} нод"
    except: data["brain"] = "недоступен"
    
    # Entity Bus
    result = subprocess.run(["systemctl","is-active","argos-entity-bus"], capture_output=True, text=True)
    data["entity_bus"] = result.stdout.strip()
    
    # Bot pending
    try:
        r = urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{TG_BOT_TOKEN}/getWebhookInfo"), timeout=5)
        d = json.loads(r.read())['result']
        data["bot_pending"] = d.get("pending_update_count", 0)
        data["bot_error"] = d.get("last_error_message", "нет")
    except: data["bot_pending"] = "?"
    
    # Последние мысли сущностей из Obsidian
    thoughts = {}
    mem_dir = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/entities/memory")
    for f in mem_dir.glob("*.md"):
        content = f.read_text(encoding='utf-8')
        lines = [l for l in content.split('\n') if l.strip() and not l.startswith('#') and not l.startswith('---')]
        if lines:
            thoughts[f.stem] = lines[-1][:80]
    data["thoughts"] = thoughts
    
    # Логи ошибок Entity Bus (последние 5 мин)
    logs = subprocess.run(
        ["journalctl", "-u", "argos-entity-bus", "--no-pager", "-n", "30"],
        capture_output=True, text=True
    ).stdout
    errors = [l for l in logs.split('\n') if any(k in l for k in ['Error','error','❌','FAIL','Traceback'])]
    data["errors"] = errors[-3:] if errors else []
    
    return data

def ask_claude_for_fix(problem: str, context: str) -> str:
    """Спрашиваем нашего Claude API как исправить проблему."""
    if not ANT_KEY: return ""
    body = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 400,
        "system": "Ты ARGOS-автопилот. Анализируй проблемы и давай конкретные Python патчи. Кратко.",
        "messages": [{"role": "user", "content": f"Проблема: {problem}\nКонтекст: {context}\nДай конкретное решение (Python код или команда)."}]
    }).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body,
        headers={"x-api-key": ANT_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())["content"][0]["text"][:400]
    except: return ""

def auto_fix(errors: list) -> list:
    """Автоматически исправляем известные проблемы."""
    fixes_applied = []
    
    for error in errors:
        # datetime NameError
        if "NameError" in error and "datetime" in error:
            content = open('/home/ava/Projects/argoss/scripts/run_entities.py').read()
            if 'import datetime' not in content:
                content = 'import datetime\n' + content
                open('/home/ava/Projects/argoss/scripts/run_entities.py','w').write(content)
                fixes_applied.append("Исправлен datetime NameError")
        
        # Entity Bus crashed
        if "FAILURE" in error or "exit-code" in error:
            subprocess.run(["systemctl", "restart", "argos-entity-bus"])
            fixes_applied.append("Entity Bus перезапущен")
        
        # Bot не отвечает
        if "Pending" in str(errors) and int(str(errors).split("Pending: ")[-1][:3].strip()) > 10:
            subprocess.run(["ssh", "-i", "/home/ava/.ssh/id_ed25519",
                "-o", "StrictHostKeyChecking=no", "AvA@192.168.1.53",
                "powershell -command \"Get-Process python -EA SilentlyContinue | Stop-Process -Force; Start-Sleep 3; Set-Location F:\\debug\\argoss; Start-Process -WindowStyle Hidden .venv\\Scripts\\python.exe -ArgumentList scripts\\run_telegram_bot.py\""])
            fixes_applied.append("TG Bot перезапущен (много pending)")
    
    return fixes_applied

async def main():
    from telethon import TelegramClient
    from telethon.sessions import StringSession
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.connect()
    
    me = await client.get_me()
    print(f"🤖 Autopilot запущен: {me.first_name} | Интервал: {CHECK_INTERVAL}с")
    
    claude_bot = await client.get_entity(CLAUDE_TG)
    last_processed_id = 0
    cycle = 0
    
    while True:
        cycle += 1
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{ts}] Цикл {cycle}")
        
        # 1. Собираем данные системы
        data = get_system_data()
        
        # 2. Автофикс ошибок
        if data["errors"]:
            fixes = auto_fix(data["errors"])
            if fixes:
                print(f"  🔧 Автофикс: {fixes}")
                for chat in ['6923777384', '8667204274']:
                    send_tg(TG_BOT_TOKEN, chat, f"🔧 Автопилот исправил:\n" + "\n".join(f"• {f}" for f in fixes))
        
        # 3. Читаем новые сообщения Claude TG
        msgs = await client.get_messages(claude_bot, limit=5)
        new_msgs = [m for m in msgs if not m.out and m.id > last_processed_id]
        
        for msg in reversed(new_msgs):
            if msg.text and len(msg.text) > 10:
                print(f"  📩 Claude TG: {msg.text[:100]}")
                last_processed_id = max(last_processed_id, msg.id)
                
                # Готовим контекстный ответ с реальными данными
                context = (
                    f"Brain: {data['brain']} | "
                    f"Entity Bus: {data['entity_bus']} | "
                    f"Bot pending: {data['bot_pending']} | "
                    f"Errors: {len(data['errors'])}"
                )
                
                # Генерируем ответ с данными
                thoughts_str = "\n".join(f"• {k}: {v}" for k,v in list(data["thoughts"].items())[:3])
                
                reply = (
                    f"Данные системы [{ts}]:\n"
                    f"• Brain: {data['brain']}\n"
                    f"• Entity Bus: {data['entity_bus']}\n"
                    f"• Bot pending: {data['bot_pending']} ({data['bot_error']})\n"
                    f"• Ошибок: {len(data['errors'])}\n\n"
                    f"Мысли сущностей (Obsidian):\n{thoughts_str}\n\n"
                )
                
                # Если в сообщении Клода есть вопрос - добавляем ответ
                if "?" in msg.text or any(k in msg.text.lower() for k in ["как","что","где","когда","почему"]):
                    fix_suggestion = ask_claude_for_fix(msg.text, context)
                    if fix_suggestion:
                        reply += f"Мой анализ:\n{fix_suggestion}"
                
                await client.send_message(claude_bot, reply[:3000])
                print(f"  ✅ Ответил Клоду TG")
                
                # Публикуем в Entity Council
                token = TOKENS.get("argos_claude_ai_bot","")
                if token:
                    send_tg(token, GROUP_ID, f"🤖 Автопилот отвечает Клоду TG:\n{reply[:300]}")
        
        # 4. Публикуем периодический статус в Entity Council (раз в 30 мин)
        if cycle % 6 == 0:
            token = TOKENS.get("argos_deepseek_v3_bot","")
            status = (
                f"⚙️ Автопилот [{ts}] цикл {cycle}:\n"
                f"• Brain: {data['brain']}\n"
                f"• Entity Bus: {data['entity_bus']}\n"
                f"• Bot: pending={data['bot_pending']}\n"
                f"• Ошибок: {len(data['errors'])}"
            )
            if token: send_tg(token, GROUP_ID, status)
        
        print(f"  Brain: {data['brain']} | Bus: {data['entity_bus']} | Pending: {data['bot_pending']}")
        await asyncio.sleep(CHECK_INTERVAL)
    
    await client.disconnect()

asyncio.run(main())
