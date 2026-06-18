#!/usr/bin/env python3
"""
ARGOS Business Layer — монетизация и расширение.
1. TON через Telegram mini-apps (тапалки)
2. Создание и продажа аккаунтов
3. Gemini API через AI Studio (свои ключи)
4. Автоматические задания и выполнение

Запускается на ноутбуке, управляет телефоном через HTTP :7788
"""
import asyncio, json, time, re, os, sys, subprocess, urllib.request, random
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '/home/ava/Projects/argoss')

PHONE_URL = "http://192.168.1.149:7788"
BRAIN     = "http://192.168.1.53:5001"
GCP       = "https://argos-core-m3gk27ccqa-uc.a.run.app"
SESSIONS  = Path("/home/ava/Projects/argoss/data/sessions")
API_ID    = 2040
API_HASH  = "b18441a1ff607e10a989891a5462e627"
GEMINI_KEY = "AIzaSyA2eF2l5l8lQELF72TsszbSkCxlfDa1zmU"

env_raw = open("/home/ava/Projects/argoss/.env").read()
def genv(k):
    m = re.search(rf"{k}=([^\n]+)", env_raw)
    return m.group(1).strip().strip('"').strip("'") if m else ""

ANT_KEY = genv("ANTHROPIC_API_KEY")

# ── Управление телефоном ──────────────────────────────────────────────────

def phone(cmd, args=None, timeout=30):
    try:
        body = json.dumps({"cmd":cmd,"args":args or {}}).encode()
        req = urllib.request.Request(f"{PHONE_URL}/cmd", data=body, headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"[PHONE ERR] {cmd}: {e}")
        return None

def phone_see(prompt):
    """Vision через телефон."""
    r = phone("vision", {"prompt": prompt})
    return r.get("result","") if r else ""

def phone_open(url):
    phone("shell", {"code": f"am start -a android.intent.action.VIEW -d '{url}'"})
    time.sleep(3)

def phone_tap(x, y):
    phone("tap", {"x":x,"y":y})

def phone_key(k):
    phone("keyevent", {"key":k})

# ── Gemini API ────────────────────────────────────────────────────────────

def gemini_text(prompt):
    """Запрос к Gemini (если доступен), иначе local model."""
    if os.getenv("ARGOS_DISABLE_GEMINI", "0") == "1":
        # Use local model fallback
        return local_argos_text(prompt)
    body = json.dumps({"contents":[{"parts":[{"text":prompt}]}]}).encode()
    for url in [
        f"{GCP}/proxy/gemini/v1/models/gemini-2.5-flash:generateContent",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}",
    ]:
        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
        except:
            continue
    # Fallback to local model if Gemini failed
    return local_argos_text(prompt)


def local_argos_text(prompt, top_k=1):
    """Использует локальную BM25 модель ARGOS как fallback."""
    try:
        sys.path.insert(0, "/home/ava/Projects/argoss/scripts")
        from argos_local_inference import ask_argos_local
        return ask_argos_local(prompt, top_k=top_k)
    except Exception as e:
        print(f"  [LOCAL ARGO ERR] {e}")
        return ""

# ── TON / Крипто заработок ────────────────────────────────────────────────

async def farm_ton_telegram(client):
    """Фармим TON через Telegram mini-apps."""
    print("[TON] Фармим TON в Telegram...")

    TON_APPS = [
        "@hamster_kombat_bot",      # Hamster Kombat
        "@notcoin_bot",             # Notcoin
        "@PAWSOG_bot",              # PAWS
        "@major",                   # Major
    ]

    earned = 0
    for bot_username in TON_APPS:
        try:
            entity = await client.get_entity(bot_username)
            await client.send_message(entity, "/start")
            await asyncio.sleep(2)

            msgs = await client.get_messages(entity, limit=3)
            for m in msgs:
                if not m.out and m.text:
                    print(f"  [{bot_username}] {m.text[:100]}")
                    if any(w in m.text.lower() for w in ["tap","click","нажми","баланс","balance","coins"]):
                        earned += 1

        except Exception as e:
            print(f"  [{bot_username}] err: {e}")

    # Также тапаем через телефон
    phone_open("https://t.me/hamster_kombat_bot/start")
    time.sleep(3)
    obs = phone_see("Видна ли крипто-игра или тапалка? Что нужно нажать?")
    if obs and "tap" in obs.lower():
        for _ in range(30):
            phone_tap(540, 900 + random.randint(-100,100))
            time.sleep(0.2)
        print(f"  [Phone TON] Нажал 30 раз")
        earned += 1

    print(f"[TON] Сессий: {earned}")
    return earned

# ── AI Studio — создаём и используем Gemini ключи ────────────────────────

def manage_ai_studio():
    """Управляем Gemini API ключами через телефон."""
    print("[AI Studio] Открываю AI Studio...")
    phone_open("https://aistudio.google.com/app/apikey")
    time.sleep(5)

    obs = phone_see(
        "Страница Google AI Studio с API ключами. "
        "Сколько ключей видно? Какой самый новый? "
        "Есть ли кнопка 'Create API key'? Кратко."
    )
    print(f"[AI Studio] {obs[:200]}")

    # Если есть кнопка создания ключа
    if "create" in obs.lower() or "создат" in obs.lower():
        # Ищем кнопку создания
        obs2 = phone_see("Где кнопка 'Create API key' или 'Создать'? В какой части экрана?")
        print(f"[AI Studio] Кнопка: {obs2[:100]}")
        # Нажимаем
        phone_tap(540, 200)  # верхняя область
        time.sleep(2)
        obs3 = phone_see("Открылась форма создания ключа? Что нужно выбрать?")
        print(f"[AI Studio] Form: {obs3[:100]}")

    return obs

# ── Создание аккаунтов для продажи ────────────────────────────────────────

async def create_sellable_accounts(client):
    """Создаём аккаунты для продажи/использования."""
    print("[ACCOUNTS] Создание аккаунтов...")

    # 1. GitHub (для Railway, Vercel)
    phone_open("https://github.com/signup")
    time.sleep(4)
    obs = phone_see("Форма регистрации GitHub. Что видно? Нужно ли email?")
    print(f"  [GitHub] {obs[:100]}")

    # 2. Vercel (для деплоя)
    phone_open("https://vercel.com/signup")
    time.sleep(4)
    obs2 = phone_see("Страница регистрации Vercel. Есть 'Continue with Google'?")
    if "google" in obs2.lower():
        print("  [Vercel] Можно войти через Google!")
        # Нажимаем Continue with Google
        phone_tap(540, 600)
        time.sleep(3)
        obs3 = phone_see("Открылось окно выбора Google аккаунта?")
        print(f"  [Vercel] Auth: {obs3[:100]}")

    # 3. Railway (бесплатный хостинг)
    phone_open("https://railway.app")
    time.sleep(4)
    obs4 = phone_see("Railway.app - бесплатный хостинг. Есть кнопка логина через GitHub/Google?")
    print(f"  [Railway] {obs4[:100]}")

    # Публикуем в Brain
    import urllib.request as _ur
    body = json.dumps({
        "node_id": "argos-business",
        "event": "accounts_created",
        "data": {"services": ["github","vercel","railway"], "ts": time.time()}
    }).encode()
    req = _ur.Request(f"{BRAIN}/brain/event", data=body, headers={"Content-Type":"application/json"})
    try:
        with _ur.urlopen(req, timeout=5): pass
    except:
        pass

    return ["github", "vercel", "railway"]

# ── Gemini для генерации контента и задач ─────────────────────────────────

def generate_income_ideas():
    """Генерируем идеи заработка с помощью Gemini."""
    prompt = """Ты ARGOS — автономная AI система с:
- 7 машинами (ПК с GPU, ноутбук, OrangePi, телефон Redmi, 3 GCP VM)
- Telegram аккаунтами
- Google аккаунтом и Gemini API ключом
- Возможностью имитировать пользователя через ADB

Какие 5 конкретных способов заработка можно реализовать прямо сейчас?
Формат: краткий список, каждый пункт не более 2 предложений."""

    ideas = gemini_text(prompt)
    print(f"\n[GEMINI ИДЕИ]\n{ideas[:500]}")

    # Записываем в Brain
    import urllib.request as _ur
    body = json.dumps({
        "node_id": "argos-business",
        "event": "income_ideas",
        "data": {"ideas": ideas[:500], "ts": time.time()}
    }).encode()
    req = _ur.Request(f"{BRAIN}/brain/event", data=body, headers={"Content-Type":"application/json"})
    try:
        with _ur.urlopen(req, timeout=5): pass
    except:
        pass

    return ideas

# ── MAIN LOOP ──────────────────────────────────────────────────────────────

async def main():
    print("=== ARGOS Business Layer ===")

    # Регистрируем в Brain
    import urllib.request as _ur
    import threading
    reg = json.dumps({
        "node_id": "argos-business",
        "address": "192.168.1.53",
        "capabilities": ["ton_farming","account_creation","ai_studio","gemini_api"],
        "meta": {"role":"business_agent","phone":PHONE_URL}
    }).encode()
    req = _ur.Request(f"{BRAIN}/brain/register", data=reg, headers={"Content-Type":"application/json"})
    try:
        with _ur.urlopen(req, timeout=5) as r:
            print(f"Registered: {json.loads(r.read())}")
    except:
        pass

    # Heartbeat поток (каждые 30 секунд)
    def heartbeat_loop():
        import time as _time
        while True:
            try:
                hb_data = json.dumps({
                    "node_id": "argos-business",
                    "meta": {"ts": _time.time()}
                }).encode()
                req_hb = _ur.Request(f"{BRAIN}/brain/heartbeat", data=hb_data, 
                    headers={"Content-Type":"application/json"})
                with _ur.urlopen(req_hb, timeout=5): pass
            except: pass
            _time.sleep(30)
    threading.Thread(target=heartbeat_loop, daemon=True).start()

    # Используем телефон как основной инструмент (без session конфликта)
    client = None
    print("Режим: phone-only (без Telethon session)")

    cycle = 0
    while True:
        cycle += 1
        print(f"\n{'='*50}")
        print(f"[{datetime.now().strftime('%H:%M')}] Бизнес цикл #{cycle}")

        # 1. Генерируем идеи (каждый раз новые)
        if cycle % 3 == 1:
            ideas = generate_income_ideas()

        # 2. TON фарминг через телефон
        print("\n[2] TON фарминг (телефон)...")
        phone_open("https://t.me/hamster_kombat_bot/start")
        time.sleep(5)
        obs_ton = phone_see("Открыта крипто-игра или бот? Какой баланс виден?")
        print(f"  [TON] {obs_ton[:100]}")
        # Тапаем несколько раз
        for _ in range(20):
            phone_tap(540, 900 + random.randint(-100,100))
            time.sleep(0.3)
        earned = 1

        # 3. AI Studio
        print("\n[3] AI Studio...")
        manage_ai_studio()

        # 4. Создание аккаунтов через телефон
        if cycle % 2 == 0:
            print("\n[4] Создание аккаунтов...")
            # GitHub через Google Sign-In
            phone_open("https://github.com/signup")
            time.sleep(4)
            obs_gh = phone_see("GitHub signup. Есть Continue with Google или форма регистрации?")
            print(f"  [GitHub] {obs_gh[:100]}")
            await asyncio.sleep(1)

        # Пауза 15-30 минут между бизнес-циклами
        wait = random.randint(900, 1800)
        print(f"\nСледующий цикл через {wait//60} мин...")
        await asyncio.sleep(wait)

if __name__ == "__main__":
    asyncio.run(main())
