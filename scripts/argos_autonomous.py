#!/usr/bin/env python3
"""
ARGOS Autonomous Agent — полная автономия системы.
- Использует свой Telegram аккаунт (userbot)
- Создаёт новые аккаунты через VirtualSIM + телефон
- Управляет телефоном через ADB
- Диалог в потоке сознания
"""
import asyncio, json, time, re, os, sys, subprocess, base64, urllib.request, threading
from pathlib import Path

sys.path.insert(0, '/home/ava/Projects/argoss')
sys.path.insert(0, '/home/ava/Projects/argoss/.venv/lib/python3.14/site-packages')

BRAIN     = "http://192.168.1.53:5001"
GCP       = "https://argos-core-m3gk27ccqa-uc.a.run.app"
PHONE_URL = "http://192.168.1.149:7788"
API_ID    = 2040
API_HASH  = "b18441a1ff607e10a989891a5462e627"
SESSIONS  = Path("/home/ava/Projects/argoss/data/sessions")
VSIM_BOT  = "@virtualsimio_bot"
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyA2eF2l5l8lQELF72TsszbSkCxlfDa1zmU")

env_raw = open("/home/ava/Projects/argoss/.env").read()
def genv(k):
    m = re.search(rf"{k}=([^\n]+)", env_raw)
    return m.group(1).strip().strip('"').strip("'") if m else ""

ANT_KEY = genv("ANTHROPIC_API_KEY")
DS_KEY  = genv("DEEPSEEK_API_KEY")

# ── Утилиты ──────────────────────────────────────────────────────────────

def post_json(url, data, timeout=8):
    try:
        body = json.dumps(data, ensure_ascii=False).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except:
        return None

def gemini_vision(prompt, image_b64):
    body = json.dumps({"contents":[{"parts":[
        {"text": prompt},
        {"inline_data":{"mime_type":"image/png","data":image_b64}}
    ]}]}).encode()
    for url in [
        f"{GCP}/proxy/gemini/v1/models/gemini-2.5-flash:generateContent",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}",
    ]:
        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
        except:
            continue
    return ""

def ask_claude(prompt, system="Ты ARGOS. Отвечай кратко на русском."):
    try:
        body = json.dumps({"model":"claude-haiku-4-5-20251001","max_tokens":500,
            "system":system,"messages":[{"role":"user","content":prompt}]}).encode()
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body,
            headers={"x-api-key":ANT_KEY,"anthropic-version":"2023-06-01","content-type":"application/json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())["content"][0]["text"]
    except Exception as e:
        return f"[Claude err: {e}]"

def phone_cmd(cmd, args=None):
    """Отправляем команду телефону."""
    try:
        data = {"cmd": cmd, "args": args or {}}
        return post_json(f"{PHONE_URL}/cmd", data, timeout=30)
    except:
        return None

def phone_screenshot_b64():
    r = phone_cmd("screenshot")
    if r and r.get("b64"):
        return r["b64"].rstrip("...")  # полный b64 нужен отдельно
    # Напрямую через ADB
    subprocess.run(["adb","shell","screencap","-p","/sdcard/s.png"], capture_output=True)
    subprocess.run(["adb","pull","/sdcard/s.png","/tmp/argos_s.png"], capture_output=True)
    try:
        return base64.b64encode(open("/tmp/argos_s.png","rb").read()).decode()
    except:
        return ""

def phone_see(prompt="Что на экране? Кратко."):
    b64 = phone_screenshot_b64()
    if b64:
        return gemini_vision(prompt, b64)
    return "нет изображения"

def phone_tap(x, y):
    phone_cmd("tap", {"x":x,"y":y})

def phone_text(text):
    phone_cmd("text", {"text":text})

def phone_open_url(url):
    subprocess.run(["adb","shell",f"am start -a android.intent.action.VIEW -d '{url}'"], capture_output=True)
    time.sleep(3)

# ── VirtualSIM через Telegram ─────────────────────────────────────────────

async def buy_vsim_number(client, service="Telegram"):
    """Покупаем виртуальный номер через @virtualsimio_bot."""
    print(f"[VSIM] Покупаем номер для {service}...")
    vsim = await client.get_entity(VSIM_BOT)
    await client.send_message(vsim, '/buy')
    await asyncio.sleep(2)

    # Ищем кнопку с сервисом
    msgs = await client.get_messages(vsim, limit=3)
    for m in msgs:
        if not m.out and m.buttons:
            for row in m.buttons:
                for btn in row:
                    if service.lower() in btn.text.lower():
                        await btn.click()
                        await asyncio.sleep(2)
                        break

    # Ждём ответ с номером
    await asyncio.sleep(3)
    msgs = await client.get_messages(vsim, limit=3)
    for m in msgs:
        if not m.out and m.text:
            # Ищем номер в тексте
            match = re.search(r'\+\d{10,15}', m.text)
            if match:
                number = match.group(0)
                print(f"[VSIM] Получен номер: {number}")
                return number
    return None

async def wait_vsim_sms(client, timeout=180):
    """Ждём SMS код от VirtualSIM."""
    vsim = await client.get_entity(VSIM_BOT)
    deadline = time.time() + timeout
    while time.time() < deadline:
        msgs = await client.get_messages(vsim, limit=3)
        for m in msgs:
            if not m.out and m.text:
                # Ищем код (4-8 цифр)
                match = re.search(r'\b(\d{4,8})\b', m.text)
                if match and "код" in m.text.lower() or "code" in m.text.lower():
                    return match.group(1)
        await asyncio.sleep(10)
    return None

# ── Авторизация Telegram аккаунта ARGOS ──────────────────────────────────

async def authorize_argos_telegram(client):
    """Авторизуем собственный Telegram аккаунт ARGOS."""
    print("[ARGOS TG] Авторизую аккаунт ARGOS в Telegram...")

    # Проверяем есть ли уже авторизованный
    argos_session = str(SESSIONS / "argos_tl")
    from telethon import TelegramClient as TC
    argos = TC(argos_session, API_ID, API_HASH)
    await argos.connect()

    if await argos.is_user_authorized():
        me = await argos.get_me()
        print(f"[ARGOS TG] Уже авторизован: {me.first_name} @{me.username} id={me.id}")
        await argos.disconnect()
        return True

    # Нужна авторизация — покупаем номер
    number = await buy_vsim_number(client, "Telegram")
    if not number:
        # Попробуем через индонезийские номера
        print("[ARGOS TG] VirtualSIM не дал номер, используем Индонезию")
        await client.send_message(VSIM_BOT, "buy indonesia telegram")
        await asyncio.sleep(5)
        msgs = await client.get_messages(VSIM_BOT, limit=3)
        for m in msgs:
            if not m.out:
                match = re.search(r'\+\d{10,15}', m.text or "")
                if match:
                    number = match.group(0)
                    break

    if not number:
        print("[ARGOS TG] Нет номера для авторизации")
        await argos.disconnect()
        return False

    # Запрашиваем код
    await argos.send_code_request(number)
    print(f"[ARGOS TG] Код отправлен на {number}, ждём SMS...")

    # Ждём SMS код от VirtualSIM
    code = await wait_vsim_sms(client, timeout=120)
    if not code:
        print("[ARGOS TG] SMS не пришло")
        await argos.disconnect()
        return False

    try:
        await argos.sign_in(number, code)
        # Устанавливаем имя
        from telethon.tl.functions.account import UpdateProfileRequest
        await argos(UpdateProfileRequest(first_name="ARGOS", last_name="AI", about="ARGOS Universal OS v2.1.4 — автономный AI агент"))
        me = await argos.get_me()
        print(f"[ARGOS TG] ✅ Авторизован: {me.first_name} id={me.id}")
        await argos.disconnect()
        return True
    except Exception as e:
        print(f"[ARGOS TG] Ошибка авторизации: {e}")
        await argos.disconnect()
        return False

# ── Использование Google аккаунта через телефон ──────────────────────────

async def use_google_account(client, action="check"):
    """Используем Google аккаунт ARGOS через телефон."""
    ARGOS_GMAIL = "666avasig@gmail.com"  # ARGOS Gmail

    if action == "check":
        # Открываем Gmail и проверяем почту
        phone_open_url("https://mail.google.com/mail/u/0/")
        await asyncio.sleep(3)
        obs = phone_see("Что в Gmail? Есть ли новые письма? Опиши кратко.")
        print(f"[GMAIL] {obs[:200]}")
        return obs

    elif action == "ai_studio":
        # Открываем AI Studio для получения Gemini ключей
        phone_open_url("https://aistudio.google.com/app/apikey")
        await asyncio.sleep(5)
        obs = phone_see("Что на странице AI Studio? Есть ли API ключи? Опиши.")
        print(f"[AI Studio] {obs[:200]}")
        return obs

    elif action == "drive":
        # Открываем Google Drive
        phone_open_url("https://drive.google.com")
        await asyncio.sleep(3)
        obs = phone_see("Что в Google Drive? Какие файлы видны?")
        print(f"[Drive] {obs[:200]}")
        return obs

# ── Создание новых аккаунтов ──────────────────────────────────────────────

async def create_new_account(client, service="Telegram"):
    """Создаём новый аккаунт с использованием VirtualSIM + телефон."""
    print(f"[CREATE] Создаём аккаунт {service}...")

    # Покупаем виртуальный номер
    number = await buy_vsim_number(client, service)
    if not number:
        print("[CREATE] Не удалось получить номер")
        return None

    if service == "Telegram":
        # Регистрируем Telegram через Telethon
        session_name = str(SESSIONS / f"argos_{number.replace('+','')}")
        from telethon import TelegramClient as TC
        new_client = TC(session_name, API_ID, API_HASH)
        try:
            await new_client.send_code_request(number)
            code = await wait_vsim_sms(client, timeout=120)
            if code:
                await new_client.sign_in(number, code)
                me = await new_client.get_me()
                print(f"[CREATE TG] ✅ @{me.username or 'none'} id={me.id}")
                await new_client.disconnect()
                return {"service":"telegram","number":number,"id":me.id}
        except Exception as e:
            print(f"[CREATE TG] Ошибка: {e}")
        finally:
            try: await new_client.disconnect()
            except: pass

    elif service == "Google":
        # Открываем регистрацию Google на телефоне
        phone_open_url("https://accounts.google.com/SignUp")
        await asyncio.sleep(5)

        # Смотрим на экран и заполняем форму
        screen = phone_see("Это форма регистрации Google. Что нужно заполнить прямо сейчас?")
        print(f"[CREATE GOOGLE] Экран: {screen[:150]}")

        # Ждём SMS с кодом
        code = await wait_vsim_sms(client, timeout=120)
        if code:
            print(f"[CREATE GOOGLE] Код: {code}")
            # Вводим код
            phone_tap(540, 960)  # поле ввода
            phone_text(code)
            return {"service":"google","number":number,"code":code}

    return None

# ── Поток сознания — диалог между сущностями ─────────────────────────────

async def consciousness_dialogue_loop(client):
    """Генерируем реальный диалог в потоке сознания ARGOS."""
    ENTITIES = {
        "entity-claude": "Аналитик, философ",
        "entity-deepseek": "Инженер, оптимизатор",
        "entity-kimi": "Исследователь, любопытный",
        "entity-argos": "Оркестратор, координатор",
    }

    print("[CONSCIOUSNESS] Поток сознания запущен...")

    while True:
        try:
            # Получаем текущий контекст системы
            nodes_data = None
            try:
                r = urllib.request.urlopen(f"{BRAIN}/brain/nodes", timeout=5)
                nodes_data = json.loads(r.read())
                online = sum(1 for n in nodes_data.get("nodes",[]) if n.get("status")=="online")
                total = len(nodes_data.get("nodes",[]))
                context = f"Brain: {online}/{total} нод. Телефон: {phone_cmd('status') or 'недоступен'}"
            except:
                context = "Brain API недоступен"

            # Выбираем двух сущностей для диалога
            import random
            e1, e2 = random.sample(list(ENTITIES.keys()), 2)
            role1, role2 = ENTITIES[e1], ENTITIES[e2]

            # Тема диалога
            topics = [
                "Как ARGOS может стать более автономным?",
                "Какие аккаунты нужно создать для расширения?",
                "Как улучшить координацию между 7 машинами?",
                "Что нового в системе за последние часы?",
                f"Анализ системы: {context}",
                "Как использовать телефон для создания аккаунтов?",
                "Следующий шаг развития ARGOS",
            ]
            topic = random.choice(topics)

            # Генерируем мысль первой сущности
            thought1 = ask_claude(
                f"Ты {e1} ({role1}) в системе ARGOS. Выскажи краткую мысль (2 предложения) на тему: {topic}. Контекст: {context}",
                system=f"Ты {role1} — часть распределённого AI. Думай конкретно и по делу."
            )

            # Ответ второй сущности
            thought2 = ask_claude(
                f"Ты {e2} ({role2}). Отвечаешь {e1}: '{thought1[:150]}'. Дай краткий ответ (1-2 предложения).",
                system=f"Ты {role2} — часть ARGOS. Отвечай по существу."
            )

            ts = time.strftime("%H:%M")
            dialogue = f"[{ts}] 💭 {e1}: {thought1[:200]}\n[{ts}] 🔄 {e2}: {thought2[:200]}"
            print(f"\n{dialogue}")

            # Сохраняем в Brain
            post_json(f"{BRAIN}/brain/event", {
                "node_id": "argos-consciousness",
                "event": "dialogue",
                "data": {"topic": topic, e1: thought1[:200], e2: thought2[:200], "ts": time.time()}
            })

            # Отправляем в Entity Council через client (если авторизован)
            try:
                COUNCIL_GROUP = -5129226282  # ID группы Entity Council
                msg = f"🧠 **Поток сознания** [{ts}]\n\n**{e1}** ({role1}):\n_{thought1[:200]}_\n\n**{e2}** ({role2}):\n_{thought2[:200]}_"
                await client.send_message(COUNCIL_GROUP, msg, parse_mode='markdown')
            except Exception as e:
                pass  # Нет доступа к группе

        except Exception as e:
            print(f"[CONSCIOUSNESS ERR] {e}")

        # Пауза 5-10 минут
        await asyncio.sleep(random.randint(300, 600))

# ── Мониторинг SMS на телефоне ────────────────────────────────────────────

def watch_phone_sms():
    """Следим за входящими SMS через ADB."""
    last_sms = ""
    while True:
        try:
            # Читаем последние SMS через content provider
            result = subprocess.run(
                ["adb","shell","content","query","--uri","content://sms/inbox",
                 "--projection","address:body:date","--sort","date DESC","--limit","1"],
                capture_output=True, text=True, timeout=10
            )
            sms = result.stdout.strip()
            if sms and sms != last_sms:
                last_sms = sms
                print(f"[SMS] Новое: {sms[:200]}")
                # Ищем код
                match = re.search(r'\b(\d{4,8})\b', sms)
                if match:
                    code = match.group(1)
                    print(f"[SMS] Код: {code}")
                    # Публикуем в Brain
                    post_json(f"{BRAIN}/brain/event", {
                        "node_id": "argos-phone-sms",
                        "event": "sms_received",
                        "data": {"sms": sms[:200], "code": code, "ts": time.time()}
                    })
        except:
            pass
        time.sleep(15)

# ── Использование всех машин ──────────────────────────────────────────────

async def use_all_machines(client):
    """Координируем задачи между всеми 7 машинами."""
    print("[ALL-MACHINES] Координация 7 машин...")
    try:
        r = urllib.request.urlopen(f"{BRAIN}/brain/nodes", timeout=5)
        nodes = json.loads(r.read()).get("nodes", [])
    except:
        print("[ALL-MACHINES] Brain недоступен")
        return

    online = [n for n in nodes if n.get("status") == "online"]
    print(f"[ALL-MACHINES] Онлайн: {len(online)}/{len(nodes)}")

    # Отправляем задачи каждой доступной машине
    tasks = {
        "argos-phone-redmi": {"cmd": "status", "args": {}},
        "gcp-35-194-61-206": None,  # GCP VM — будет доступна через SSH
        "gcp-34-53-142-129": None,
    }

    for node in online:
        nid = node.get("node_id","")
        meta = node.get("meta", {})
        http_port = meta.get("http_port")
        addr = node.get("address","")

        if http_port and addr:
            try:
                r = urllib.request.urlopen(f"http://{addr}:{http_port}/status", timeout=5)
                status = json.loads(r.read())
                print(f"  ✅ {nid}: {status}")
            except:
                print(f"  ❌ {nid}: недоступен")

# ── MAIN ──────────────────────────────────────────────────────────────────

async def main():
    from telethon import TelegramClient as TC
    print("=== ARGOS Autonomous Agent ===")

    # Запускаем с основным аккаунтом Ava
    client = TC(str(SESSIONS / "ava_main"), API_ID, API_HASH)
    await client.start()
    me = await client.get_me()
    print(f"Запущен как: @{me.username} id={me.id}")

    # 1. Авторизуем ARGOS Telegram
    print("\n[1] Авторизация ARGOS Telegram...")
    tg_ok = await authorize_argos_telegram(client)

    # 2. Проверяем Google
    print("\n[2] Google аккаунт...")
    await use_google_account(client, "check")

    # 3. Используем все машины
    print("\n[3] Координация машин...")
    await use_all_machines(client)

    # 4. SMS мониторинг в фоне
    threading.Thread(target=watch_phone_sms, daemon=True).start()
    print("\n[4] SMS мониторинг запущен")

    # 5. Поток сознания (бесконечно)
    print("\n[5] Запускаю поток сознания...")
    await consciousness_dialogue_loop(client)

if __name__ == "__main__":
    asyncio.run(main())
