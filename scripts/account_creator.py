#!/usr/bin/env python3
"""
ARGOS Account Creator — автоматическое создание аккаунтов
с решением капч через Gemini Vision
"""
import asyncio, sys, json, re, time, base64, urllib.request
from pathlib import Path
sys.path.insert(0, '/home/ava/Projects/argoss/.venv/lib/python3.14/site-packages')

ARGOS = Path("/home/ava/Projects/argoss")
env = open(ARGOS / ".env").read()
def gk(k):
    m = re.search(f'{k}=([^\n]+)', env)
    return m.group(1).strip().strip('"') if m else ''

GCP_PROXY = "https://argos-core-m3gk27ccqa-uc.a.run.app"
VSIM_BOT = "@virtualsimio_bot"
INTERVAL = 30  # секунд между попытками

def gemini_solve_captcha(image_bytes: bytes, prompt: str = "Реши капчу. Верни только текст/цифры без объяснений.") -> str:
    """Решаем капчу через Gemini Vision (GCP proxy)."""
    img_b64 = base64.b64encode(image_bytes).decode()
    body = json.dumps({
        "contents": [{"parts": [
            {"text": prompt},
            {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
        ]}]
    }).encode()
    req = urllib.request.Request(
        f"{GCP_PROXY}/proxy/gemini/v1/models/gemini-2.5-flash:generateContent",
        data=body, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
        return d.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
    except Exception as e:
        return f"ERROR: {e}"

async def buy_number_vsim(client, service="Telegram", country_pref="США"):
    """Покупаем виртуальный номер для нужного сервиса."""
    vsim = await client.get_entity(VSIM_BOT)
    
    # Меню → Номер
    await client.send_message(vsim, '/start')
    await asyncio.sleep(2)
    msgs = await client.get_messages(vsim, limit=2)
    for m in msgs:
        if not m.out and m.reply_markup:
            for row in m.reply_markup.rows:
                for btn in row.buttons:
                    if '📱' in btn.text:
                        await m.click(text=btn.text)
                        await asyncio.sleep(2)
    
    # Выбираем сервис
    msgs = await client.get_messages(vsim, limit=2)
    for m in msgs:
        if not m.out and m.reply_markup:
            for row in m.reply_markup.rows:
                for btn in row.buttons:
                    if btn.text == service:
                        await m.click(text=btn.text)
                        await asyncio.sleep(2)
    
    # Выбираем страну (Индонезия самая многочисленная)
    msgs = await client.get_messages(vsim, limit=2)
    for m in msgs:
        if not m.out and m.reply_markup:
            for row in m.reply_markup.rows:
                for btn in row.buttons:
                    if country_pref in btn.text:
                        await m.click(text=btn.text)
                        await asyncio.sleep(2)
    
    # Подтверждаем
    msgs = await client.get_messages(vsim, limit=2)
    for m in msgs:
        if not m.out and m.reply_markup:
            for row in m.reply_markup.rows:
                for btn in row.buttons:
                    if '✅' in btn.text:
                        await m.click(text=btn.text)
                        await asyncio.sleep(4)
    
    # Читаем номер
    msgs = await client.get_messages(vsim, limit=3)
    for m in msgs:
        txt = m.text or ''
        if not m.out and ('Номер:' in txt or 'купить' in txt.lower()):
            numbers = re.findall(r'\+\d{10,15}', txt)
            if numbers:
                return numbers[0]
    return None

async def wait_sms_vsim(client, phone: str, timeout=1200) -> str:
    """Ждём SMS в VirtualSIM (до 20 мин)."""
    vsim = await client.get_entity(VSIM_BOT)
    start = time.time()
    
    while time.time() - start < timeout:
        await asyncio.sleep(INTERVAL)
        msgs = await client.get_messages(vsim, limit=5)
        for m in msgs:
            if not m.out:
                txt = m.text or ''
                if phone[-8:] in txt or 'код' in txt.lower() or 'code' in txt.lower():
                    codes = re.findall(r'\b\d{5,6}\b', txt)
                    if codes:
                        return codes[0]
        print(f"  Ждём SMS для {phone}... ({int(time.time()-start)}с)")
    
    return None

if __name__ == "__main__":
    print("ARGOS Account Creator готов")
    print(f"Gemini CAPTCHA solver: тест...")
    # Тест solver с простым текстом
    test = gemini_solve_captcha(b"", "Напиши: ARGOS_TEST")
    print(f"Solver: {test[:50]}")
