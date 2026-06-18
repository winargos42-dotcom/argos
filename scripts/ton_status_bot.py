#!/usr/bin/env python3
"""
ARGOS TON Status Bot — монетизация через Telegram + TON.

Команды:
  /start     — приветствие + кошелёк для оплаты
  /status    — базовый статус ARGOS (бесплатно)
  /full      — полный отчёт ARGOS (0.05 TON)
  /pay       — инструкция по оплате
  /verify    — проверить свою оплату
  /balance   — баланс кошелька ARGOS
  /entities  — список AI сущностей (бесплатно)
  /report    — сохранить отчёт в Obsidian (0.1 TON)

Использует:
  - TELEGRAM_BOT_TOKEN из .env (@Argosssbot)
  - TON_WALLET_ADDRESS из .env (UQ...)
  - toncenter.com API (без SDK)
  - Проверка платежей по comment = user_id в транзакции
"""

import json, os, re, sys, time, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime

ARGOS_ROOT = Path("/home/ava/Projects/argoss")
DATA_DIR = ARGOS_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# ── Загрузка .env ───────────────────────────────────────────────────────────
ENV_PATH = ARGOS_ROOT / ".env"
ENV = ENV_PATH.read_text() if ENV_PATH.exists() else ""

def genv(k):
    m = re.search(rf"{k}=([^\n\s]+)", ENV)
    return m.group(1).strip().strip('"').strip("'") if m else ""

TG_TOKEN = genv("TELEGRAM_BOT_TOKEN")
ARGOS_TON = genv("TON_WALLET_ADDRESS") or genv("ARGOS_TON_ADDRESS")
TON_API_KEY = genv("TON_API_KEY") or genv("TONCENTER_API_KEY")
HA_TOKEN = genv("HA_TOKEN")

# ── TONcenter API ───────────────────────────────────────────────────────────
TON_API = "https://toncenter.com/api/v2"

def ton_req(endpoint, params=None):
    url = f"{TON_API}/{endpoint}"
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(url)
    if TON_API_KEY:
        req.add_header("X-API-Key", TON_API_KEY)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

def get_balance(addr: str) -> float:
    d = ton_req("getAddressBalance", {"address": addr})
    if "result" in d:
        return int(d["result"]) / 1e9
    return 0.0

def get_transactions(addr: str, limit: int = 10):
    d = ton_req("getTransactions", {"address": addr, "limit": limit, "archival": "false"})
    return d.get("result", []) or []

def get_price():
    try:
        req = urllib.request.Request(
            "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd,rub")
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
            return d["the-open-network"]["usd"], d["the-open-network"]["rub"]
    except:
        return 1.96, 142

# ── Платёжная база ────────────────────────────────────────────────────────
PAYMENTS_FILE = DATA_DIR / "ton_payments.json"

def load_payments():
    try:
        with open(PAYMENTS_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_payments(data):
    tmp = DATA_DIR / "_tmp_payments.json"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    tmp.rename(PAYMENTS_FILE)

# ── ARGOS Status helpers ──────────────────────────────────────────────────
def get_brain_status():
    try:
        r = urllib.request.urlopen("http://192.168.1.53:5001/brain/nodes", timeout=5)
        d = json.loads(r.read())
        nodes = d.get("nodes", [])
        online = sum(1 for n in nodes if n.get("status") == "online")
        return f"{online}/{len(nodes)} нод онлайн"
    except:
        return "Brain недоступен"

def get_ha_status():
    try:
        req = urllib.request.Request("http://localhost:8123/api/states",
            headers={"Authorization": f"Bearer {HA_TOKEN}"})
        with urllib.request.urlopen(req, timeout=8) as r:
            states = json.loads(r.read())
        unavail = [e for e in states if e.get("state") == "unavailable"]
        return f"{len(states)} entities, {len(unavail)} unavailable"
    except:
        return "HA недоступен"

def get_services_status():
    try:
        import subprocess
        r = subprocess.run(["systemctl","list-units","argos-*","--no-pager","--no-legend","-q"],
            capture_output=True, text=True, timeout=10)
        lines = [l for l in r.stdout.strip().split("\n") if l.strip()]
        active = sum(1 for l in lines if " active " in l)
        failed = [l.split()[0] for l in lines if " failed " in l or " activating " in l]
        return f"{active} active" + (f", failed: {', '.join(failed[:3])}" if failed else "")
    except:
        return "?"

# ── Telegram Bot (urllib без python-telegram-bot) ─────────────────────────
# Используем просто urllib чтобы не тянуть asyncio loop и быть совместимым с фоновым запуском

def tg_send(chat_id, text, reply_markup=None):
    body = {"chat_id": chat_id, "text": text[:4095], "parse_mode": "HTML"}
    if reply_markup:
        body["reply_markup"] = reply_markup
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"TG send error: {e}")
        return {}

def tg_get_updates(offset):
    body = json.dumps({"offset": offset, "limit": 10}).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TG_TOKEN}/getUpdates",
        data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
            return d.get("result", [])
    except Exception as e:
        print(f"TG get error: {e}")
        return []

# ── Command handlers ──────────────────────────────────────────────────────

def handle_start(chat_id, user):
    usd, rub = get_price()
    text = (
        f"🤖 <b>ARGOS Status Bot</b>\n"
        f"Привет, {user.get('first_name','друг')}!\n\n"
        f"<b>Бесплатно:</b>\n"
        f"• /status — статус ARGOS\n"
        f"• /entities — AI сущности\n"
        f"• /balance — баланс кошелька ARGOS\n\n"
        f"<b>Платные (TON):</b>\n"
        f"• /full — полный отчёт ARGOS → <b>0.05 TON</b>\n"
        f"• /report — отчёт в Obsidian → <b>0.1 TON</b>\n\n"
        f"💎 Кошелёк для оплаты:\n<code>{ARGOS_TON}</code>\n"
        f"В комментарии укажи свой Telegram ID: <code>{chat_id}</code>\n"
        f"Затем нажми /verify для проверки.\n\n"
        f"Цена TON: ${usd:.2f} / ₽{rub:.0f}"
    )
    tg_send(chat_id, text)

def handle_status(chat_id):
    brain = get_brain_status()
    ha = get_ha_status()
    svc = get_services_status()
    text = (
        f"📊 <b>ARGOS Status</b> [{datetime.now().strftime('%H:%M')}]\n\n"
        f"🧠 Brain: {brain}\n"
        f"🏠 HA: {ha}\n"
        f"⚙️ Services: {svc}\n\n"
        f"Полный отчёт: /full (0.05 TON)"
    )
    tg_send(chat_id, text)

def handle_entities(chat_id):
    text = (
        f"🤖 <b>ARGOS AI Entities</b>\n\n"
        f"1. entity-claude — Anthropic Claude\n"
        f"2. entity-deepseek — DeepSeek V3\n"
        f"3. entity-kimi — Moonshot Kimi K2.6\n"
        f"4. entity-gemini — Google Gemini Flash\n"
        f"5. entity-openai — OpenAI GPT-4o-mini\n"
        f"6. entity-cloudflare — CF Workers AI\n"
        f"7. entity-argos — orchestrator (ollama argos-v1)\n\n"
        f"Status: Entity Bus v4 — WORKERS mode\n"
        f"Council: 🤖 ARGOS Entity Council"
    )
    tg_send(chat_id, text)

def handle_balance(chat_id):
    bal = get_balance(ARGOS_TON)
    usd, rub = get_price()
    text = (
        f"💎 <b>ARGOS TON Wallet</b>\n"
        f"<code>{ARGOS_TON[:25]}...</code>\n\n"
        f"Баланс: <b>{bal:.4f} TON</b>\n"
        f"≈ ${bal*usd:.2f} / ₽{bal*rub:.0f}\n\n"
        f"Цена TON: ${usd:.2f}"
    )
    tg_send(chat_id, text)

def handle_pay(chat_id):
    text = (
        f"💰 <b>Оплата за отчёты ARGOS</b>\n\n"
        f"1. Отправь TON на адрес:\n"
        f"<code>{ARGOS_TON}</code>\n\n"
        f"2. В комментарии (memo) укажи:\n"
        f"<code>{chat_id}</code>\n\n"
        f"3. Нажми /verify для проверки\n\n"
        f"<b>Цены:</b>\n"
        f"• /full — 0.05 TON (~${0.05*get_price()[0]:.2f})\n"
        f"• /report — 0.1 TON (~${0.1*get_price()[0]:.2f})\n\n"
        f"⚡ Платежи обрабатываются в течение 1-2 минут."
    )
    tg_send(chat_id, text)

def handle_verify(chat_id):
    payments = load_payments()
    user_payments = payments.get(str(chat_id), [])
    total = sum(p.get("amount", 0) for p in user_payments)
    
    # Проверяем свежие транзакции
    txs = get_transactions(ARGOS_TON, limit=30)
    found_new = False
    for tx in txs:
        in_msg = tx.get("in_msg", {})
        comment = in_msg.get("message", "") or ""
        value = int(in_msg.get("value", "0")) / 1e9
        tx_hash = tx.get("transaction_id", {}).get("hash", "")
        if str(chat_id) in comment and value > 0:
            # Проверяем не зачисляли ли уже
            if not any(p.get("tx_hash") == tx_hash for p in user_payments):
                user_payments.append({
                    "tx_hash": tx_hash,
                    "amount": value,
                    "time": datetime.now().isoformat(),
                    "comment": comment,
                })
                found_new = True
    
    if found_new:
        payments[str(chat_id)] = user_payments
        save_payments(payments)
    
    total = sum(p.get("amount", 0) for p in user_payments)
    text = (
        f"✅ <b>Проверка платежей</b>\n\n"
        f"Найдено платежей: {len(user_payments)}\n"
        f"Общая сумма: <b>{total:.4f} TON</b>\n\n"
        f"{'🎉 Новые платежи зачислены!' if found_new else 'Новых платежей не обнаружено.'}\n\n"
        f"Доступно:\n"
        f"• /full (0.05 TON)\n"
        f"• /report (0.1 TON)\n"
    )
    tg_send(chat_id, text)

def handle_full(chat_id):
    payments = load_payments()
    user_total = sum(p.get("amount", 0) for p in payments.get(str(chat_id), []))
    if user_total < 0.05:
        tg_send(chat_id, f"❌ Недостаточно средств. Баланс: {user_total:.4f} TON. Нужно 0.05 TON.\n/pay — оплатить, /verify — проверить.")
        return
    
    brain = get_brain_status()
    ha = get_ha_status()
    svc = get_services_status()
    bal = get_balance(ARGOS_TON)
    usd, rub = get_price()
    
    text = (
        f"📋 <b>Полный отчёт ARGOS</b> [{datetime.now().strftime('%Y-%m-%d %H:%M')}]\n\n"
        f"🧠 Brain: {brain}\n"
        f"🏠 HA: {ha}\n"
        f"⚙️ Services: {svc}\n"
        f"💎 TON баланс: {bal:.4f} TON (${bal*usd:.2f})\n\n"
        f"🤖 AI Entities:\n"
        f"• Claude, DeepSeek, Kimi, Gemini, OpenAI, Cloudflare\n"
        f"• Entity Bus v4 — WORKERS mode\n\n"
        f"📁 Финальные отчёты: /home/ava/argos-reports/\n"
        f"🔗 Brain API: http://192.168.1.53:5001\n\n"
        f"Спасибо за поддержку ARGOS! 💎"
    )
    tg_send(chat_id, text)

def handle_report(chat_id):
    payments = load_payments()
    user_total = sum(p.get("amount", 0) for p in payments.get(str(chat_id), []))
    if user_total < 0.1:
        tg_send(chat_id, f"❌ Недостаточно средств. Баланс: {user_total:.4f} TON. Нужно 0.1 TON.\n/pay — оплатить, /verify — проверить.")
        return
    
    # Генерируем отчёт и сохраняем в Obsidian
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared") / f"REPORT_USER_{chat_id}_{ts}.md"
    
    brain = get_brain_status()
    ha = get_ha_status()
    svc = get_services_status()
    bal = get_balance(ARGOS_TON)
    
    report = f"""---
type: user-report
user_id: {chat_id}
date: {datetime.now().isoformat()}
paid: 0.1 TON
---

# ARGOS User Report {ts}

## Status
- Brain: {brain}
- HA: {ha}
- Services: {svc}
- TON Balance: {bal:.4f} TON

## AI Entities
Active: Claude, DeepSeek, Kimi, Gemini, OpenAI, Cloudflare
Entity Bus: v4 WORKERS

## Links
- [[STATUS]] | [[AGENTS]] | [[WORKING]]
"""
    report_path.write_text(report, encoding="utf-8")
    
    text = (
        f"📄 <b>Отчёт сохранён в Obsidian!</b>\n\n"
        f"Файл: <code>{report_path.name}</code>\n"
        f"Путь: SharedMemory/shared/\n\n"
        f"Спасибо за поддержку ARGOS! 💎"
    )
    tg_send(chat_id, text)

# ── Main loop ───────────────────────────────────────────────────────────────

def main():
    if not TG_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not found in .env")
        sys.exit(1)
    if not ARGOS_TON:
        print("ERROR: TON_WALLET_ADDRESS not found in .env")
        sys.exit(1)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] TON Status Bot started")
    print(f"  TG Bot: {TG_TOKEN.split(':')[0]}...")
    print(f"  TON Wallet: {ARGOS_TON[:20]}...")
    print(f"  TON API: {'with key' if TON_API_KEY else 'no key'}")
    
    offset = 0
    handlers = {
        "/start": handle_start,
        "/status": handle_status,
        "/entities": handle_entities,
        "/balance": handle_balance,
        "/pay": handle_pay,
        "/verify": handle_verify,
        "/full": handle_full,
        "/report": handle_report,
    }
    
    while True:
        try:
            updates = tg_get_updates(offset)
            for up in updates:
                offset = up["update_id"] + 1
                msg = up.get("message", {})
                chat = msg.get("chat", {})
                chat_id = chat.get("id")
                user = msg.get("from", {})
                text = msg.get("text", "")
                
                if not text or not chat_id:
                    continue
                
                cmd = text.split()[0].lower()
                handler = handlers.get(cmd)
                if handler:
                    try:
                        handler(chat_id, user if cmd == "/start" else None)
                    except Exception as e:
                        print(f"Handler error: {e}")
                        tg_send(chat_id, f"⚠️ Ошибка: {e}")
                else:
                    tg_send(chat_id, "Неизвестная команда. Попробуй /start")
        
        except KeyboardInterrupt:
            print("\nStopping...")
            break
        except Exception as e:
            print(f"Loop error: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    main()
